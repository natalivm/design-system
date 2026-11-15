import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// GitHub Pages serves the site at https://<user>.github.io/<repo>/.
// BASE_PATH is set by the deploy workflow; '/design-system/' matches this repo.
export default defineConfig({
  base: process.env.BASE_PATH || '/design-system/',
  plugins: [react()],
  server: { fs: { allow: ['..'] } },
  build: { outDir: 'dist', chunkSizeWarningLimit: 900 }
});
