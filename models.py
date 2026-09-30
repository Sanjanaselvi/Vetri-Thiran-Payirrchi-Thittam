from typing import List

from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):

    story_prompt: str = Field(
        ...,
        min_length=5,
        max_length=2000
    )

    character_name: str = Field(
        ...,
        min_length=1,
        max_length=80
    )

    setting: str = Field(
        ...,
        min_length=1,
        max_length=120
    )

    tone: str = Field(
        default="funny",
        max_length=50
    )

    art_style: str = Field(
        default="comic book",
        max_length=80
    )

    panels: int = Field(
        default=5,
        ge=3,
        le=8
    )

    @field_validator(
        "story_prompt",
        "character_name",
        "setting",
        "tone",
        "art_style"
    )
    @classmethod
    def clean_text(cls, value: str) -> str:

        value = " ".join(value.strip().split())

        if not value:
            raise ValueError("This field cannot be empty.")

        return value


class PanelOutline(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    image_prompt: str


class PanelStory(BaseModel):

    panel_number: int

    caption: str = ""

    narration: str = ""

    dialogue: str = ""


class ComicPanel(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    image_prompt: str

    image_url: str

    caption: str

    narration: str

    dialogue: str


class ComicResult(BaseModel):

    title: str

    panels: List[ComicPanel]

    pdf_url: str