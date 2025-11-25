import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import netlify from '@astrojs/netlify';

// Switched to hybrid output to support secure admin pages while keeping
// the rest of the site static.
export default defineConfig({
  integrations: [react(), tailwind()],
  output: 'hybrid',
  adapter: netlify(),
  server: {
    port: 3000,
    host: true
  }
});
