import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000, // Set the port to the desired value
  },
  build: {
    outDir: 'dist', // Output directory for production build
    assetsDir: 'assets', // Output directory for assets
    minify: 'esbuild', // Minification using esbuild
  },
});