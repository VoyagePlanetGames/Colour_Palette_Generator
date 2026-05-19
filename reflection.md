# Day 92 — Reflection: Colour Palette Generator

🔗 **Live project / source code:** https://github.com/VoyagePlanetGames/Colour_Palette_Generator

## How I approached the project

I started by breaking the brief into two clear halves: the **colour maths** and
the **website around it**. The brief explicitly pointed back to Day 76 (image
processing with NumPy), so I knew the engine should be NumPy rather than a
ready-made library — that kept the project educational instead of just gluing a
package together.

For the maths I worked it out step by step:

1. Open the image with Pillow and shrink it to a thumbnail (speed).
2. Convert it to a NumPy array and reshape it to one row per pixel.
3. The naive idea — count every unique RGB value — fails: a photo has thousands
   of *almost* identical shades, so the "top 10" would be ten versions of the
   same blue. I fixed this by snapping pixels into coarse colour **buckets**
   before counting with `np.unique(..., return_counts=True)`.
4. To keep the swatches accurate I averaged the real pixels inside each winning
   bucket, rather than showing the bucket's corner value.

Then I wrapped it in a small Flask app with a drag-and-drop upload, a base64
image preview (so nothing is saved to disk), and click-to-copy swatches like
Flat UI Colors.

## What was easy

- The Flask scaffolding — routes, templates, handling a file upload — felt
  familiar from earlier days.
- The HTML/CSS. Building a clean, flat, card-based layout went quickly.
- Reading the image with Pillow and handing it to NumPy.

## What was hard

- **Getting a *useful* palette.** The "count unique colours" approach is obvious
  but produces a useless result. Realising *why* and discovering the bucketing
  trick was the real problem-solving moment of the day.
- **Picking the bucket size.** Too small and you get near-duplicates; too large
  and distinct colours merge together. I settled on 24 after testing.
- Processing the image **in memory** instead of saving uploads to disk — I had
  to read the file bytes once and reuse them for both NumPy and the preview.

## My biggest learning

That "most common" is not the same as "most *useful*". The honest pixel count is
mathematically correct but visually pointless — real-world data almost always
needs **grouping or quantising** before counting means anything. That's a
lesson that goes well beyond colours.

## What I'd do differently next time

- Use **k-means clustering** (e.g. scikit-learn) to group colours by actual
  similarity instead of a fixed grid — it would handle gradients far better.
- Let the user choose how many colours to extract.
- Add a "download palette" button (CSS variables or a `.png` strip).
- Show each colour's name, not just its HEX code.
- Write a couple of automated tests for `extract_colours` so I can refactor the
  bucket logic with confidence.

## How I'll improve for the next project

Prototype the *hard* part first. I spent time polishing the UI before I was sure
the colour extraction gave good results — next time I'll validate the core logic
in a plain script before building anything around it.
