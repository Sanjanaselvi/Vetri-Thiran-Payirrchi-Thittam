from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from .config import settings
from .exporters import save_pdf
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .models import PromptRequest


router = APIRouter()

templates = Jinja2Templates(
    directory=str(
        settings.template_dir
    )
)


def create_comic(
    payload: PromptRequest
):

    # STEP 1
    # Generate panel outline

    outlines = generate_outline(

        payload.story_prompt,

        payload.character_name,

        payload.setting,

        payload.tone,

        payload.art_style,

        payload.panels
    )

    # STEP 2
    # Generate story

    stories = generate_story(

        outlines,

        payload.character_name,

        payload.tone
    )

    # STEP 3
    # Generate images

    image_urls = []

    for panel in outlines:

        image_url = generate_image(
            panel.image_prompt
        )

        image_urls.append(
            image_url
        )

    # STEP 4
    # Build final layout

    layout = build_comic_layout(

        outlines,

        stories,

        image_urls
    )

    # STEP 5
    # Create title

    title = (
        f"{payload.character_name}'s "
        f"Comic Adventure"
    )

    # STEP 6
    # Export PDF

    pdf_url = save_pdf(
        title,
        layout
    )

    return (
        title,
        layout,
        pdf_url
    )


@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={
            "settings": settings,
            "error": None
        }
    )


@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate(

    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),

    panels: int = Form(5)
):

    try:

        payload = PromptRequest(

            story_prompt=story_prompt,

            character_name=character_name,

            setting=setting,

            tone=tone,

            art_style=art_style,

            panels=panels
        )

        title, layout, pdf_url = (
            create_comic(payload)
        )

        return templates.TemplateResponse(

            request=request,

            name="comic_preview.html",

            context={
                "title": title,
                "layout": layout,
                "pdf_url": pdf_url
            }
        )

    except Exception as error:

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={
                "settings": settings,
                "error": str(error)
            },

            status_code=500
        )


@router.post(
    "/generate-comic/json"
)
async def generate_json(
    payload: PromptRequest
):

    try:

        title, layout, pdf_url = (
            create_comic(payload)
        )

        return {

            "success": True,

            "title": title,

            "panels": [
                panel.model_dump()
                for panel in layout
            ],

            "pdf_url": pdf_url
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.get(
    "/export-success",
    response_class=HTMLResponse
)
async def export_success(

    request: Request,

    pdf_url: str = ""
):

    return templates.TemplateResponse(

        request=request,

        name="export_success.html",

        context={
            "pdf_url": pdf_url
        }
    )


@router.get(
    "/test-image",
    response_class=HTMLResponse
)
async def test_image(

    prompt: str =
    "A cute fox exploring an enchanted forest, comic book style"
):

    try:

        image_url = generate_image(
            prompt
        )

        return HTMLResponse(

            f"""
            <html>
            <head>
            <title>ComicCraft Image Test</title>
            </head>

            <body
                style="
                font-family:Arial;
                text-align:center;
                padding:30px;
                "
            >

            <h1>ComicCraft Image Test</h1>

            <img
                src="{image_url}"
                style="
                max-width:90%;
                border:2px solid black;
                border-radius:10px;
                "
            >

            <p>{prompt}</p>

            </body>
            </html>
            """
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )