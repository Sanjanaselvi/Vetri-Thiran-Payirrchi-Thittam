import json
import re
from functools import lru_cache

from google import genai
from google.genai import types

from .config import settings


@lru_cache(maxsize=1)
def get_client():

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(
    model: str,
    prompt: str,
    json_mode: bool = False
):

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=0.8,
        max_output_tokens=4096
    )

    if json_mode:

        config.response_mime_type = "application/json"

    response = client.models.generate_content(

        model=model,

        contents=prompt,

        config=config
    )

    text = getattr(response, "text", None)

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()


def parse_json(text: str):

    cleaned = text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.I
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned
    )

    try:

        return json.loads(cleaned)

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            f"Gemini returned invalid JSON: {exc}"
        ) from exc