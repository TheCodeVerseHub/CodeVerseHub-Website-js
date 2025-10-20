import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

// Switched to static output so the site can be deployed to static hosts like
// Netlify. Server-side DB usage should be moved to serverless functions or
// replaced with static data for build-time rendering.
export default defineConfig({
  integrations: [react(), tailwind()],
  // static output for Netlify
  output: 'static',
  server: {
    port: 3000,
    host: true
  }
});
