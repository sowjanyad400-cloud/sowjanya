import time
from functools import lru_cache
from typing import Optional

from google import genai
from google.genai import types

from config import get_settings


@lru_cache
def get_client():
    settings = get_settings()

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Please add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(
    prompt: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
) -> str:

    settings = get_settings()
    client = get_client()

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        system_instruction=system_instruction,
    )

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=config,
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError("Gemini returned an empty response.")

            return text.strip()

        except Exception as exc:
            error_text = str(exc)

            # Retry temporary Gemini availability errors
            if "503" in error_text or "UNAVAILABLE" in error_text:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)
                    continue

            raise RuntimeError(f"Gemini API error: {error_text}") from exc

    raise RuntimeError("Gemini request failed after multiple attempts.")