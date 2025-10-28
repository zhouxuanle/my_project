import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  root: path.resolve(__dirname, './'),
  build: {
    outDir: 'dist',
  },
  server: {
    port: 3000,
    open: true,  // This will open the browser automatically
    host: true   // This enables network access
  }
});