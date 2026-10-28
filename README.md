# Hotdog / Not Hotdog with Jev

- **Code:** <https://github.com/willirath/2026_jev-box-demo>
- **App:** <https://willirath.github.io/2026_jev-box-demo/>, or on GEOMAR GitLab Pages at
  <https://2026-jev-box-demo-daaa4b.pages.geomar.de>

The copy at <https://git.geomar.de/willi-rath/2026_jev-box-demo> only serves the
GEOMAR Pages app. Development happens on GitHub.

A static page that classifies an image as hotdog or not hotdog with TypeSafe's
Jev 1.14 through OpenRouter. It sends the image together with two questions:

- `hotdog`: a `noul` (yes/no) question; the answer is P(hot dog).
- `where`: a `box` question; the answer is a bounding box as fractions of the image size.

A box question always returns a box, even when there is no hot dog, so the page
draws the box only if the `noul` probability is at least 0.5.

## Web app

[public/index.html](public/index.html) is the whole app. GitHub Pages serves
`public/` via [.github/workflows/pages.yml](.github/workflows/pages.yml), and
GitLab Pages via [.gitlab-ci.yml](.gitlab-ci.yml). Each user enters their own
OpenRouter key, which goes straight from the browser to openrouter.ai.
Locally: `python3 -m http.server -d public`.

The example images load from Wikimedia Commons and Flickr. The page shows each
image's author, license, and source from [public/credits.js](public/credits.js).

## Example run

```bash
cp .env.template .env      # then paste an OpenRouter key
uv run run_examples.py     # reads examples.txt, writes results/ and public/presets.js
```

Image input and box questions are early Jev features, and TypeSafe advises
against using them in production.

## Results (2026-10-28, `typesafe/jev-1.14`)

[examples.txt](examples.txt) holds one Flickr hot dog, 4 hot dog images from a
Wikimedia Commons search, one tray of bare sausages from the same search, and 5
random Commons images. Jev got 10 of 11 right, for $0.0007 in total. The page
shows these canned answers, from [public/presets.js](public/presets.js), before a
key is entered. The one miss is the tray of bare sausages with no bun (P = 0.06).
That fits the question's definition of a hot dog as "a sausage served in a split bun".

A visual check of an earlier run with the same images found the boxes rough. Two
fit well. One covered nearly the whole frame, and one left out the bottom half of
the bun. Reruns shift the probabilities by about 0.01.
