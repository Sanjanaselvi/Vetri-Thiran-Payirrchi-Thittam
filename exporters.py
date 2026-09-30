from datetime import datetime
from pathlib import Path
from uuid import uuid4

from fpdf import FPDF

from .config import settings
from .models import ComicPanel


def safe_text(text: str):

    return (
        text
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def save_pdf(
    title: str,
    panels: list[ComicPanel]
):

    filename = (
        f"comic_"
        f"{datetime.now():%Y%m%d_%H%M%S}_"
        f"{uuid4().hex[:6]}.pdf"
    )

    output_path = (
        settings.exports_dir /
        filename
    )

    pdf = FPDF(
        format="A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in panels:

        pdf.add_page()

        pdf.set_font(
            "Arial",
            "B",
            18
        )

        pdf.multi_cell(
            0,
            10,
            safe_text(
                f"Panel {panel.panel_number}: "
                f"{panel.title}"
            )
        )

        pdf.ln(4)

        # Convert browser URL to local file.
        image_relative = (
            panel.image_url
            .replace("/static/", "")
        )

        image_path = (
            settings.static_dir /
            image_relative
        )

        if image_path.exists():

            pdf.image(
                str(image_path),
                x=15,
                y=None,
                w=180
            )

            pdf.ln(6)

        pdf.set_font(
            "Arial",
            "I",
            11
        )

        pdf.multi_cell(
            0,
            7,
            safe_text(
                panel.scene_description
            )
        )

        pdf.ln(3)

        pdf.set_font(
            "Arial",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            7,
            "Caption"
        )

        pdf.set_font(
            "Arial",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            safe_text(
                panel.caption
            )
        )

        pdf.set_font(
            "Arial",
            "B",
            11
        )

        pdf.multi_cell(
            0,
            7,
            "Narration"
        )

        pdf.set_font(
            "Arial",
            "",
            11
        )

        pdf.multi_cell(
            0,
            7,
            safe_text(
                panel.narration
            )
        )

        if panel.dialogue:

            pdf.set_font(
                "Arial",
                "B",
                11
            )

            pdf.multi_cell(
                0,
                7,
                "Dialogue"
            )

            pdf.set_font(
                "Arial",
                "",
                11
            )

            pdf.multi_cell(
                0,
                7,
                safe_text(
                    panel.dialogue
                )
            )

    pdf.output(
        str(output_path)
    )

    return (
        f"/static/exports/{filename}"
    )