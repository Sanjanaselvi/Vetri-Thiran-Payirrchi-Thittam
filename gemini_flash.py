from .config import settings
from .gemini_client import generate_text, parse_json
from .models import PanelOutline


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
    panels: int = 5
):

    prompt = f"""
You are the comic outline generator for an application called ComicCraft.

Create exactly {panels} sequential comic panels.

USER STORY:
{story_prompt}

MAIN CHARACTER:
{character_name}

SETTING:
{setting}

TONE:
{tone}

ART STYLE:
{art_style}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "panels": [
        {{
            "panel_number": 1,
            "title": "Short panel title",
            "scene_description": "Describe what happens visually.",
            "image_prompt": "Detailed prompt for an AI image generator."
        }}
    ]
}}

Rules:

1. Generate exactly {panels} panels.
2. Keep the same main character throughout.
3. Keep the setting consistent.
4. Every panel must continue the story.
5. Make the story suitable for a comic.
6. Image prompts must describe:
   - character
   - action
   - environment
   - lighting
   - composition
   - art style
7. Do NOT put dialogue text inside image_prompt.
8. Do NOT include speech bubbles.
"""

    result = generate_text(
        settings.gemini_outline_model,
        prompt,
        json_mode=True
    )

    data = parse_json(result)

    raw_panels = data.get(
        "panels",
        []
    )

    outlines = []

    for panel in raw_panels:

        outlines.append(
            PanelOutline.model_validate(panel)
        )

    if len(outlines) != panels:

        raise RuntimeError(
            f"Expected {panels} panels but Gemini returned "
            f"{len(outlines)} panels."
        )

    return outlines