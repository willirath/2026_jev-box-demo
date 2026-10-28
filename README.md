# Hotdog / Not Hotdog with Jev

A static page that classifies an image as hotdog or not hotdog with TypeSafe's
Jev 1.14 through OpenRouter. It sends the image together with two questions:

- `hotdog`: a `noul` (yes/no) question; the answer is P(hot dog).
- `where`: a `box` question; the answer is a bounding box as fractions of the image size.

A box question always returns a box, even when there is no hot dog, so the page
draws the box only if the `noul` probability is at least 0.5.

## Web app

[public/index.html](public/index.html) is the whole app. GitLab Pages serves
`public/` via [.gitlab-ci.yml](.gitlab-ci.yml). Each user enters their own
OpenRouter key, which goes straight from the browser to openrouter.ai.
Locally: `python3 -m http.server -d public`.

## Example run

```bash
cp .env.template .env      # then paste an OpenRouter key
uv run run_examples.py     # reads examples.txt, writes annotated images to results/
```

Image input and box questions are early Jev features, and TypeSafe advises
against using them in production.

## Results (2026-10-28, `typesafe/jev-1.14`)

[examples.txt](examples.txt) holds 5 hot dog images from a Wikimedia Commons
search and 5 random Commons images. Jev got 9 of 10 right, for $0.0006 in total.
The one miss is a tray of bare sausages with no bun (P = 0.05). That fits the
question's definition of a hot dog as "a sausage served in a split bun". The
boxes enclose the hot dog on all four hot dog images.
