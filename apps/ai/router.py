import os
import json
import logging
from google import genai
from django.conf import settings
from decouple import config

logger = logging.getLogger(__name__)

class AIRouter:
    """
    Router for all AI-related tasks (Quiz generation, Tafsir analysis, etc.)
    Uses Google's Gemini Flash by default.
    """
    def __init__(self, model_name="gemini-1.5-flash"):
        api_key = config('GEMINI_API_KEY', default=None)
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment.")
            self.client = None
            self.model_name = model_name
            return
            
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate_quiz(self, topic, count=5):
        """
        Generates a quiz on a given topic in JSON format.
        """
        if not self.client:
            return {"error": "AI model not configured."}

        prompt = f"""
        Generate a quiz with {count} multiple-choice questions about '{topic}'.
        Return ONLY a JSON array of objects. Each object must have:
        - "question": string
        - "points": integer (default 1)
        - "choices": array of strings (exactly 4)
        - "correct_index": integer (0 to 3)
        
        Topic context: Islamic LMS platform. If topic is a Surah name, focus on its meaning and facts.
        Format: JSON only, no markdown blocks.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            # Remove markdown logic if it accidentally adds it
            text = response.text.strip()
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            
            quiz_data = json.loads(text)
            return quiz_data
        except Exception as e:
            logger.exception(f"AI Quiz Generation failed: {e}")
            return {"error": str(e)}
