"""Make a review sheet showing one selected PDF region and its source page."""
import argparse
import math
from pathlib import Path

import fitz
from PIL import Image, ImageDraw


def render(page, region, width, height):
    scale = min(width / region.width, height / region.height)
    bitmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=region,
                             colorspace=fitz.csRGB, alpha=False)
    return Image.frombytes("RGB", (bitmap.width, bitmap.height), bitmap.samples)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--page", type=int, required=True, help="Physical page, starting at 1")
    parser.add_argument("--box", type=float, nargs=4, required=True,
                        metavar=("X0", "Y0", "X1", "Y1"),
                        help="PDF points from top left of unrotated visible page")
    parser.add_argument("--expect", action="append", default=[], metavar="TEXT",
                        help="Check one single-line selectable phrase inside the crop; repeatable")
    parser.add_argument("--out", required=True, type=Path, help="Review sheet (.png)")
    args = parser.parse_args()
    if args.out.suffix.lower() != ".png" or args.out.resolve() == args.pdf.resolve():
        parser.error("--out must name a separate PNG file")
    with fitz.open(args.pdf) as doc:
        if not 1 <= args.page <= len(doc):
            parser.error(f"--page must be between 1 and {len(doc)}")
        page = doc[args.page - 1]
        page.set_rotation(0)  # In memory only. Crops and search results use one coordinate system.
        bounds = page.rect
        box = fitz.Rect(*args.box)
        if not all(map(math.isfinite, args.box)) or box.is_empty or not bounds.contains(box):
            parser.error(f"--box must lie inside unrotated page {bounds}")
        for phrase in args.expect:
            hits = page.search_for(phrase)
            inside = [hit for hit in hits if box.contains(hit)]
            if len(inside) != 1:
                positions = ", ".join(str(tuple(round(n, 1) for n in hit)) for hit in hits)
                parser.error(f"{phrase!r}: {len(inside)} hits inside crop; expected one. "
                             f"Page hits: {positions or 'none; inspect image visually'}")
        detail = render(page, box, 810, 660)
        # Render the clean crop before adding a temporary frame to the context view.
        inset = min(1, box.width / 5, box.height / 5)
        outline = fitz.Rect(box.x0 + inset, box.y0 + inset, box.x1 - inset, box.y1 - inset)
        page.draw_rect(outline, color=(0.85, 0.16, 0.06), width=inset * 2)
        whole = render(page, bounds, 520, 660)

    margin = 16
    sheet = Image.new("RGB", (whole.width + detail.width + 3 * margin,
                              max(whole.height, detail.height) + 52), "white")
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 9), f"Source page {args.page} | unrotated", fill="black")
    right = whole.width + 2 * margin
    draw.text((right, 9), f"Crop {tuple(args.box)}", fill="black")
    sheet.paste(whole, (margin, 33))
    sheet.paste(detail, (right, 33))
    sheet.save(args.out)
    print(f"{args.out}: inspect the control, state and orientation in both views.")


if __name__ == "__main__":
    main()
