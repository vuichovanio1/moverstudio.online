# Brand assets (images/)

## Favicons — light variant

Source: `/favicon.svg` (cream grid + M logo).

Regenerate PNG/ICO/apple-touch:

```bash
npm run render:favicons
```

Outputs: `favicon-16.png`, `favicon-32.png`, `favicon-48.png`, `apple-touch-icon.png`, `favicon.ico`.

## OG image — light variant

Source: `/og-image.svg`.

Regenerate PNG:

```bash
npm run render:og
```

Outputs: `/og-image.png`, `/og-image-small.png`.

All HTML pages reference `https://moverstudio.online/og-image.png?v=2`.

## Legacy (do not use for favicons/OG)

- `matrix.jpg`, `matrix-og.webp`, `matrix.svg` — old dark “matrix rain” branding.
