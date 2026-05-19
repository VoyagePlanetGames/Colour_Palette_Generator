# 🎨 Colour Palette Generator

Day 92 of 100 Days of Code. Upload an image and the app tells you the **10 most
common colours** in it, with copy-to-clipboard HEX and RGB codes — inspired by
[Flat UI Colors](https://flatuicolors.com/) and the
[coolphptools colour extractor](http://www.coolphptools.com/color_extract#demo).

🔗 **Repo:** https://github.com/VoyagePlanetGames/Colour_Palette_Generator

## How it works

The colour extraction uses **NumPy** (the Day 76 image-processing topic):

1. The upload is shrunk to a 300px thumbnail so even big photos process instantly.
2. Every pixel becomes a row of `[R, G, B]` values in a NumPy array.
3. Pixels are snapped into colour "buckets" so dozens of near-identical shades
   count as one colour instead of crowding out the palette.
4. `np.unique` counts how many pixels landed in each bucket; the busiest 10 win.
5. Each winning swatch is the *average* of the real pixels in its bucket, so the
   colour shown is true to the photo.

## Run it locally

```bash
pip install -r requirements.txt
python main.py
```

Then open http://127.0.0.1:5000 in your browser.

## Tech

- **Flask** — web server and templating
- **Pillow** — opening and resizing images
- **NumPy** — counting and ranking colours
- Vanilla HTML / CSS / JS — drag-and-drop upload and click-to-copy swatches
