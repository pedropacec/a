// Renderiza o flyer animado em MP4.
// Uso: node render.mjs [feed|story|still|orig-feed|orig-story|orig-still] [dir-de-frames]
//   feed/story/still           -> versão redesenhada (flyer.html)
//   orig-feed/orig-story/...   -> flyer original + fumaça (flyer-original.html;
//                                 requer arte/flyer-original.png)
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(execSync('npm root -g').toString().trim() + '/playwright')); }
import { mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const mode = process.argv[2] || 'feed';
const framesDir = resolve(process.argv[3] || `${here}/frames-${mode}`);
mkdirSync(framesDir, { recursive: true });
mkdirSync(`${here}/out`, { recursive: true });

const orig = mode.startsWith('orig-');
const sub = orig ? mode.slice(5) : mode;          // feed | story | still
const pageFile = orig ? 'flyer-original.html' : 'flyer.html';
const story = sub === 'story';
const width = 1080, height = story ? 1920 : 1350;
const url = `file://${here}/${pageFile}?render=1${story ? '&format=story' : ''}`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width, height } });
await page.goto(url, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);

if (sub === 'still') {
  await page.evaluate(() => renderFrame(10));
  const stillFile = orig ? 'preview-still-original.png' : 'preview-still.png';
  await page.screenshot({ path: `${here}/out/${stillFile}` });
  console.log(`still -> out/${stillFile}`);
} else {
  const total = await page.evaluate(() => window.TOTAL_FRAMES);
  for (let i = 0; i < total; i++) {
    await page.evaluate(n => renderFrame(n), i);
    await page.screenshot({ path: `${framesDir}/f${String(i).padStart(4, '0')}.png` });
    if (i % 24 === 0) console.log(`frame ${i}/${total}`);
  }
  const outFile = `${here}/out/divine-therapy-${orig ? 'original-' : ''}${sub}.mp4`;
  execSync(
    `ffmpeg -y -v error -framerate 24 -i "${framesDir}/f%04d.png" ` +
    `-c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow -movflags +faststart "${outFile}"`,
    { stdio: 'inherit' }
  );
  console.log(`ok -> ${outFile}`);
}
await browser.close();
