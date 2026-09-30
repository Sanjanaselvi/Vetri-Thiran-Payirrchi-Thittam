from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont

from .config import settings


def create_demo_image(
    prompt: str,
    output_path: Path
):

    image = Image.new(
        "RGB",
        (
            settings.image_width,
            settings.image_height
        ),
        "white"
    )

    draw = ImageDraw.Draw(image)

    try:

        font = ImageFont.truetype(
            "arial.ttf",
            28
        )

        small_font = ImageFont.truetype(
            "arial.ttf",
            18
        )

    except OSError:

        font = ImageFont.load_default()

        small_font = ImageFont.load_default()

    draw.rectangle(
        (
            20,
            20,
            settings.image_width - 20,
            settings.image_height - 20
        ),
        outline="black",
        width=4
    )

    draw.text(
        (40, 40),
        "ComicCraft",
        fill="black",
        font=font
    )

    draw.text(
        (40, 100),
        "Demo Image",
        fill="black",
        font=font
    )

    short_prompt = prompt[:250]

    draw.text(
        (40, 170),
        short_prompt,
        fill="black",
        font=small_font
    )

    image.save(
        output_path,
        "PNG"
    )


def generate_image(prompt: str):

    filename = (
        f"{uuid4().hex}.png"
    )

    output_path = (
        settings.panels_dir / filename
    )

    # If no Hugging Face key exists,
    # create a demo image.
    if not settings.hf_api_key:

        create_demo_image(
            prompt,
            output_path
        )

        return (
            f"/static/panels/{filename}"
        )

    try:

        from huggingface_hub import InferenceClient

        client = InferenceClient(
            provider=settings.image_provider,
            api_key=settings.hf_api_key
        )

        image = client.text_to_image(
            prompt=prompt,
            model=settings.hf_image_model,
            width=settings.image_width,
            height=settings.image_height,
            num_inference_steps=25
        )

        image.save(
            output_path,
            "PNG"
        )

        return (
            f"/static/panels/{filename}"
        )

    except Exception as error:

        print(
            "Image generation failed:",
            error
        )

        # Fallback so entire project
        # doesn't crash.
        create_demo_image(
            prompt,
            output_path
        )

        return (
            f"/static/panels/{filename}"
        )