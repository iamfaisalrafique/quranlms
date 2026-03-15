import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for per-room chat.
    URL: ws/chat/<room_id>/
    Auth: JWT token passed as ?token= query param.
    """

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f'chat_{self.room_id}'

        # Authenticate via JWT from query string
        token = self._get_token_from_scope()
        if not token:
            await self.close(code=4001)
            return

        user = await self.authenticate_token(token)
        if not user:
            await self.close(code=4001)
            return

        self.user = user

        # Verify user belongs to this room
        room = await self.get_room(self.room_id)
        if not room:
            await self.close(code=4004)
            return

        if not await self.user_in_room(user, room):
            await self.close(code=4003)
            return

        self.room = room

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except (json.JSONDecodeError, ValueError):
            return

        action = data.get('action', 'message')

        if action == 'message':
            content = data.get('content', '').strip()
            if not content:
                return
            await self._handle_message(content)

        elif action == 'typing':
            await self._handle_typing()

        elif action == 'mark_read':
            message_id = data.get('message_id')
            if message_id:
                await self._handle_mark_read(message_id)

    async def _handle_message(self, content: str):
        from apps.chat.pii import redact
        from apps.chat.models import ChatMessage, PIIViolationLog

        clean_content, was_blocked, patterns_found = redact(content)

        # Persist message
        message = await self.save_message(clean_content, was_blocked)

        # Log PII violation
        if was_blocked:
            await self.log_pii_violation(content, patterns_found)

        # Broadcast to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'message_id': message.id,
                'sender_id': self.user.id,
                'sender_name': self.user.get_full_name() or self.user.username,
                'content': clean_content,
                'is_pii_blocked': was_blocked,
                'created_at': message.created_at.isoformat(),
            }
        )

    async def _handle_typing(self):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.typing',
                'sender_id': self.user.id,
                'sender_name': self.user.get_full_name() or self.user.username,
            }
        )

    async def _handle_mark_read(self, message_id: int):
        await self.mark_message_read(message_id)

    # ── Channel layer event handlers ──────────────────────────────────────────

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message_id': event['message_id'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'content': event['content'],
            'is_pii_blocked': event['is_pii_blocked'],
            'created_at': event['created_at'],
        }))

    async def chat_typing(self, event):
        if event['sender_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'sender_id': event['sender_id'],
                'sender_name': event['sender_name'],
            }))

    # ── DB helpers ────────────────────────────────────────────────────────────

    def _get_token_from_scope(self):
        query_string = self.scope.get('query_string', b'').decode()
        params = dict(p.split('=', 1) for p in query_string.split('&') if '=' in p)
        return params.get('token')

    @database_sync_to_async
    def authenticate_token(self, raw_token: str):
        try:
            token = AccessToken(raw_token)
            from django.contrib.auth import get_user_model
            User = get_user_model()
            return User.objects.get(id=token['user_id'])
        except (TokenError, Exception):
            return None

    @database_sync_to_async
    def get_room(self, room_id: str):
        from apps.chat.models import ChatRoom
        try:
            return ChatRoom.objects.get(pk=room_id)
        except ChatRoom.DoesNotExist:
            return None

    @database_sync_to_async
    def user_in_room(self, user, room):
        return user.id in (room.student_id, room.teacher_id)

    @database_sync_to_async
    def save_message(self, content: str, is_pii_blocked: bool):
        from apps.chat.models import ChatMessage
        from django.utils import timezone
        msg = ChatMessage.objects.create(
            room=self.room,
            sender=self.user,
            content=content,
            is_pii_blocked=is_pii_blocked,
        )
        self.room.last_message_at = timezone.now()
        self.room.save(update_fields=['last_message_at'])
        return msg

    @database_sync_to_async
    def log_pii_violation(self, original: str, patterns: list):
        from apps.chat.models import PIIViolationLog
        PIIViolationLog.objects.create(
            room=self.room,
            sender=self.user,
            original_content=original,
            detected_patterns=patterns,
        )

    @database_sync_to_async
    def mark_message_read(self, message_id: int):
        from apps.chat.models import ChatMessage
        from django.utils import timezone
        ChatMessage.objects.filter(
            pk=message_id,
            room=self.room,
        ).exclude(sender=self.user).update(
            is_read=True,
            read_at=timezone.now(),
        )
