from .models import (
    PanelOutline,
    PanelStory,
    ComicPanel
)


def build_comic_layout(
    outlines: list[PanelOutline],
    stories: list[PanelStory],
    image_urls: list[str]
):

    story_map = {
        story.panel_number: story
        for story in stories
    }

    layout = []

    for outline, image_url in zip(
        outlines,
        image_urls
    ):

        story = story_map[
            outline.panel_number
        ]

        panel = ComicPanel(

            panel_number=outline.panel_number,

            title=outline.title,

            scene_description=(
                outline.scene_description
            ),

            image_prompt=(
                outline.image_prompt
            ),

            image_url=image_url,

            caption=story.caption,

            narration=story.narration,

            dialogue=story.dialogue
        )

        layout.append(panel)

    return layout