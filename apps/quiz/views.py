from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import Quiz, Question, Choice, QuizAttempt, AttemptAnswer
from .serializers import QuizSerializer, QuizAttemptSerializer, AttemptAnswerSerializer
from apps.ai.router import AIRouter
from apps.accounts.permissions import IsTeacher, IsStudent, IsAcademyAdmin
from apps.gamification.utils import check_and_award_badges


class QuizListView(generics.ListCreateAPIView):
    """List and Create Quizzes."""
    queryset = Quiz.objects.all().prefetch_related('questions__choices')
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update, and Delete a Quiz."""
    queryset = Quiz.objects.all().prefetch_related('questions__choices')
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]


class AIGenerateQuizView(APIView):
    """
    POST /api/quiz/ai-generate/
    Generates a quiz using Gemini and saves it to the DB.
    """
    permission_classes = [permissions.IsAuthenticated, IsTeacher | IsAcademyAdmin]

    def post(self, request):
        topic = request.data.get('topic')
        count = request.data.get('count', 5)
        academy_id = request.data.get('academy_id')

        if not topic:
            return Response({"error": "Topic is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not academy_id:
            return Response({"error": "Academy ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        router = AIRouter()
        quiz_data = router.generate_quiz(topic, count=count)

        if "error" in quiz_data:
            return Response(quiz_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save generated quiz
        quiz = Quiz.objects.create(
            title=f"Quiz: {topic}",
            description=f"AI-generated quiz about {topic}",
            academy_id=academy_id,
            created_by=request.user,
            category="AI Generated",
            is_ai_generated=True,
            ai_topic=topic
        )

        for i, item in enumerate(quiz_data):
            question = Question.objects.create(
                quiz=quiz,
                text=item['question'],
                points=item.get('points', 1),
                order=i
            )
            for j, choice_text in enumerate(item['choices']):
                Choice.objects.create(
                    question=question,
                    text=choice_text,
                    is_correct=(j == item['correct_index'])
                )

        return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)


class QuizAttemptStartView(APIView):
    """POST /api/quiz/{id}/start/ — Student starts a quiz."""
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request, pk):
        quiz = generics.get_object_or_404(Quiz, pk=pk)
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            student=request.user.student_profile,
            status=QuizAttempt.Status.STARTED
        )
        return Response(QuizAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)


class QuizAttemptSubmitView(APIView):
    """POST /api/quiz/attempt/{id}/submit/ — Student submits answers."""
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request, pk):
        attempt = generics.get_object_or_404(QuizAttempt, pk=pk)
        if attempt.status != QuizAttempt.Status.STARTED:
            return Response({"error": "Attempt already submitted."}, status=status.HTTP_400_BAD_REQUEST)

        answers_data = request.data.get('answers', [])
        total_points = 0
        earned_points = 0

        question_ids = [ans.get('question_id') for ans in answers_data if ans.get('question_id')]
        choice_ids = [ans.get('choice_id') for ans in answers_data if ans.get('choice_id')]

        questions_map = Question.objects.in_bulk(question_ids)
        choices_map = Choice.objects.in_bulk(choice_ids)

        # Validate that all provided IDs actually exist to maintain original fail-fast behavior
        if len(questions_map) != len(set(question_ids)) or len(choices_map) != len(set(choice_ids)):
            return Response({"error": "Invalid question_id or choice_id provided."}, status=status.HTTP_400_BAD_REQUEST)

        attempt_answers = []
        for ans in answers_data:
            q_id = ans.get('question_id')
            c_id = ans.get('choice_id')
            
            question = questions_map.get(q_id)
            choice = choices_map.get(c_id)
            
            is_correct = choice.is_correct
            attempt_answers.append(AttemptAnswer(
                attempt=attempt,
                question=question,
                selected_choice=choice,
                is_correct=is_correct
            ))
            
            total_points += question.points
            if is_correct:
                earned_points += question.points

        if attempt_answers:
            AttemptAnswer.objects.bulk_create(attempt_answers)

        score_percentage = (earned_points / total_points * 100) if total_points > 0 else 0
        attempt.score = score_percentage
        attempt.completed_at = timezone.now()
        
        if score_percentage >= attempt.quiz.pass_percentage:
            attempt.status = QuizAttempt.Status.PASSED
        else:
            attempt.status = QuizAttempt.Status.FAILED
            
        attempt.save()
        check_and_award_badges(attempt.student)
        return Response(QuizAttemptSerializer(attempt).data)
