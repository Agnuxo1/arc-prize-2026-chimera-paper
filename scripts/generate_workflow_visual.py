"""Render reproducible conceptual diagrams, never experimental metrics."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

def make_frame(title, labels, index):
    """Render one explanatory workflow frame, without data-backed plots."""
    image = Image.new("RGB", (820, 220), (13, 24, 40))
    draw = ImageDraw.Draw(image)
    draw.text((20, 12), title[:95], fill=(240, 249, 254))
    draw.text((20, 40), "CONCEPTUAL RESEARCH PIPELINE - NOT A MEASURED RESULT", fill=(164, 188, 206))
    for k, label in enumerate(labels):
        x = 20 + 202 * k
        draw.rounded_rectangle((x, 72, x + 180, 160), radius=13,
            fill=(36, 67, 87) if k <= index % 4 else (24, 38, 57),
            outline=(101, 161, 188), width=2)
        draw.text((x+10, 109), label[:24], fill=(241, 248, 250))
        if k < len(labels)-1:
            draw.line((x+182, 117, x+199, 117), fill=(96, 225, 212), width=3)
    draw.rounded_rectangle((20, 185, 800, 195), radius=4, fill=(49, 65, 82))
    draw.rounded_rectangle((20, 185, 20+(index+1)*780//14, 195),
        radius=4, fill=(96, 225, 212))
    draw.text((20, 202), "Schematic illustration; no synthetic score or observed sample.", fill=(164, 188, 206))
    return image

def main():
    """Write a GIF and PNG from the same textual conceptual configuration."""
    folder = Path(__file__).resolve().parents[1] / "assets"
    info = json.loads((folder / "workflow.json").read_text(encoding="utf-8"))
    assert len(info["steps"]) == 4
    frames = [make_frame(info["title"], info["steps"], n) for n in range(14)]
    frames[0].save(folder/"workflow.gif", save_all=True,
        append_images=frames[1:], optimize=True, duration=125, loop=0)
    frames[7].save(folder/"workflow.png", optimize=True)
    with Image.open(folder/"workflow.gif") as gif:
        assert gif.n_frames == 14
    print("14 conceptual GIF frames and accessible PNG verified")

if __name__ == "__main__":
    main()
