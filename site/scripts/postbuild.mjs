// Makes website/index.html the site's home page.
// The React + Three.js build moves to dist/showcase/; the prototype is already at dist/prototype/.
import { copyFileSync, mkdirSync, renameSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const dist = resolve(here, '../dist');
mkdirSync(resolve(dist, 'showcase'), { recursive: true });
renameSync(resolve(dist, 'index.html'), resolve(dist, 'showcase/index.html'));
copyFileSync(resolve(here, '../../website/index.html'), resolve(dist, 'index.html'));
console.log('home page: website/index.html · prototype: prototype/ · 3D site: showcase/');
