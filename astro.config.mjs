import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
export default defineConfig({
  site: process.env.SITE_URL || 'https://apostillesteps.com',
  base: process.env.BASE_PATH ?? '/',
  output: 'static',
  trailingSlash: 'always',
  build: { format: 'directory' },
  integrations: [sitemap({ filter: (page) => { const p = new URL(page).pathname; return !p.includes('/kit/download-') && !p.includes('/kit/thanks') && !p.includes('/get-it-done/thanks'); } })],
});
