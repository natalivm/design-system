// Copies the standalone prototype into public/ as a complete HTML document.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const wrap = (body) => body.trimStart().startsWith('<!doctype')
  ? body
  : `<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<style>html,body{margin:0}</style>\n</head>\n<body>\n${body}\n</body>\n</html>\n`;
for (const [from, to] of [['cashout-prototype.html', 'index.html'], ['onboarding-prototype.html', 'onboarding.html'], ['boost-prototype.html', 'boost.html']]) {
  const out = resolve(here, '../public/prototype', to);
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, wrap(readFileSync(resolve(here, '../../prototype', from), 'utf8')));
  console.log('prototype copied to public/prototype/' + to);
}
