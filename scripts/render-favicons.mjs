/**
 * Render light-variant favicons from /favicon.svg (not matrix.jpg).
 * Outputs: images/favicon-16.png, favicon-32.png, favicon-48.png,
 *          apple-touch-icon.png, favicon.ico
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { Resvg } from '@resvg/resvg-js';
import pngToIco from 'png-to-ico';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const svg = readFileSync(join(root, 'favicon.svg'), 'utf8');
const outDir = join(root, 'images');

function renderPng(size, name) {
  const resvg = new Resvg(svg, {
    fitTo: { mode: 'width', value: size },
    font: { loadSystemFonts: true, defaultFontFamily: 'Segoe UI' },
  });
  const png = resvg.render().asPng();
  const path = join(outDir, name);
  writeFileSync(path, png);
  console.log(`${name}: ${size}x${size} (${png.length} bytes)`);
  return path;
}

const p16 = renderPng(16, 'favicon-16.png');
const p32 = renderPng(32, 'favicon-32.png');
const p48 = renderPng(48, 'favicon-48.png');
renderPng(180, 'apple-touch-icon.png');

const ico = await pngToIco([p16, p32, p48]);
writeFileSync(join(outDir, 'favicon.ico'), ico);
console.log(`favicon.ico: ${ico.length} bytes`);
