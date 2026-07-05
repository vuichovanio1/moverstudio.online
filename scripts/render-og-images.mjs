import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const svgPath = join(root, 'og-image.svg');
const svg = readFileSync(svgPath, 'utf8');

function render(width, height, outName) {
  const resvg = new Resvg(svg, {
    fitTo: { mode: 'width', value: width },
    font: {
      loadSystemFonts: true,
      defaultFontFamily: 'Segoe UI',
    },
  });
  const png = resvg.render();
  const outPath = join(root, outName);
  writeFileSync(outPath, png.asPng());
  console.log(`${outName}: ${png.width}x${png.height} (${png.asPng().length} bytes)`);
}

// Facebook/Meta recommended 1200x630; optional 2x asset for other uses
render(1200, 630, 'og-image.png');
render(1200, 630, 'og-image-small.png');
