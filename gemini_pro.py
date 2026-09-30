from .config import settings
from .gemini_client import generate_text, parse_json
from .models import PanelOutline, PanelStory


def generate_story(
    outlines: list[PanelOutline],
    character_name: str,
    tone: str
):

    outline_data = [
        panel.model_dump()
        for panel in outlines
    ]

    prompt = f"""
You are the story writer for ComicCraft.

Main character:
{character_name}

Tone:
{tone}

The following panel outline has already been created:

{outline_data}

Expand the outline into a complete comic story.

For every panel create:

1. Caption
2. Narration
3. Dialogue

Return ONLY valid JSON.

Use exactly this structure:

{{
    "panels": [
        {{
            "panel_number": 1,
            "caption": "Short caption",
            "narration": "Narration for this panel.",
            "dialogue": "Character: \\"Dialogue here\\""
        }}
    ]
}}

Rules:

- Keep the story consistent.
- Keep character names consistent.
- Dialogue should sound natural.
- Narration should be short enough for a comic.
- Do not add extra panels.
"""

    result = generate_text(
        settings.gemini_story_model,
        prompt,
        json_mode=True
    )

    data = parse_json(result)

    raw_panels = data.get(
        "panels",
        []
    )

    stories = []

    for panel in raw_panels:

        stories.append(
            PanelStory.model_validate(panel)
        )

    if len(stories) != len(outlines):

        raise RuntimeError(
            "Gemini returned an incorrect number of story panels."
        )

    return stories