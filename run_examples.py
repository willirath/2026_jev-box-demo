# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx", "pillow", "python-dotenv"]
# ///
"""Run the example images in examples.txt through Jev, like the web app does.

Each line of examples.txt is `<expected> <url>`, with expected `hotdog` or `not`.
Writes annotated images to results/.
"""

import base64
import io
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv
from PIL import Image, ImageDraw

load_dotenv()
URL = "https://openrouter.ai/api/alpha/decisions"
MODEL = os.environ.get("JEV_MODEL", "typesafe/jev-1.14")
MAX_SIDE = 768
QUESTIONS = {
    "hotdog": {"type": "noul", "instructions": "The image shows a hot dog (a sausage served in a split bun)."},
    "where": {"type": "box", "instructions": "the hot dog"},
}
UA = {"User-Agent": "jev-box-demo/0.1 (https://git.geomar.de/willi-rath/2026_jev-box-demo)"}


def load(url):
    r = httpx.get(url, headers=UA, follow_redirects=True, timeout=30)
    r.raise_for_status()
    img = Image.open(io.BytesIO(r.content)).convert("RGB")
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    return img


def classify(img):
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    r = httpx.post(
        URL,
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
        json={"model": MODEL, "state": [{"type": "image_url", "image_url": {"url": uri}}], "questions": QUESTIONS},
        timeout=60,
    )
    if r.is_error:
        raise RuntimeError(f"{r.status_code}: {r.text}")
    return r.json()


def main(path="examples.txt"):
    out = Path("results")
    out.mkdir(exist_ok=True)
    lines = [l.split(maxsplit=1) for l in Path(path).read_text().splitlines() if l.strip() and not l.startswith("#")]
    correct = cost = 0
    for i, (expected, url) in enumerate(lines):
        try:
            img = load(url)
            resp = classify(img)
        except Exception as e:
            print(f"{i:2d}  ERROR  {url}\n    {e}")
            continue
        p = resp["answers"]["hotdog"]["noul"]
        b = resp["answers"]["where"]["box"]
        got = "hotdog" if p >= 0.5 else "not"
        correct += got == expected
        cost += resp.get("usage", {}).get("cost", 0)
        print(f"{i:2d}  {'ok ' if got == expected else 'BAD'}  p={p:.2f}  expected={expected:6s}  {url}")
        if got == "hotdog":
            w, h = img.size
            ImageDraw.Draw(img).rectangle(
                [b["left"] * w, b["top"] * h, b["right"] * w, b["bottom"] * h], outline="lime", width=4
            )
        img.save(out / f"{i:02d}_{got}_{p:.2f}.jpg")
    print(f"\n{correct}/{len(lines)} correct, total cost ${cost:.6f}, model {MODEL}")


if __name__ == "__main__":
    main(*sys.argv[1:])
