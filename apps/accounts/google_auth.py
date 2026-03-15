"""
Google OAuth helper for IslamicLMS.

Flow:
1. Frontend redirects user to Google with CLIENT_ID and redirect_uri.
2. Google returns a one-time `code` to the frontend.
3. Frontend sends that code to POST /api/auth/google/.
4. exchange_code_for_token() swaps it for access + refresh tokens.
5. get_google_user_info() fetches the user's name, email, and avatar.
6. We create/update the User row and return a JWT pair.
"""
import logging
import requests
from decouple import config

logger = logging.getLogger(__name__)

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def exchange_code_for_token(code: str) -> dict:
    """
    Exchange a Google OAuth2 authorization code for tokens.

    Returns a dict with:
        - access_token
        - refresh_token (present only on first consent)
        - id_token
        - expires_in
    Raises ValueError on failure.
    """
    payload = {
        "code": code,
        "client_id": config("GOOGLE_CLIENT_ID", default=""),
        "client_secret": config("GOOGLE_CLIENT_SECRET", default=""),
        "redirect_uri": config("GOOGLE_REDIRECT_URI", default=""),
        "grant_type": "authorization_code",
    }
    try:
        resp = requests.post(GOOGLE_TOKEN_URL, data=payload, timeout=10)
        data = resp.json()
    except requests.RequestException as exc:
        logger.error("Google token exchange failed: %s", exc)
        raise ValueError("Could not reach Google servers.") from exc

    if "error" in data:
        logger.warning("Google token error: %s", data)
        raise ValueError(data.get("error_description", data["error"]))
    return data


def get_google_user_info(access_token: str) -> dict:
    """
    Fetch the user's profile from Google using an access token.

    Returns a dict with:
        - sub        (unique Google user ID)
        - email
        - name
        - picture    (avatar URL)
        - email_verified
    Raises ValueError on failure.
    """
    try:
        resp = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        data = resp.json()
    except requests.RequestException as exc:
        logger.error("Google userinfo request failed: %s", exc)
        raise ValueError("Could not fetch Google profile.") from exc

    if "error" in data or "email" not in data:
        raise ValueError("Invalid or expired Google access token.")
    return data
