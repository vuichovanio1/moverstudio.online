This folder should contain the source image `matrix.jpg`.

Use the included PowerShell script `convert-images.ps1` (requires ImageMagick `magick`) to generate optimized images and favicons for the site.

Generated files:
- matrix-og.webp      -> OG image (1200x630 recommended)
- favicon-32.png      -> 32x32 PNG favicon
- favicon-16.png      -> 16x16 PNG favicon
- apple-touch-icon.png -> 180x180 PNG for iOS
- matrix.svg          -> Minimal SVG fallback (optional)

Run:
  .\convert-images.ps1
