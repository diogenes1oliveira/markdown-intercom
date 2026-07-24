import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  // 1. Define the root directory containing index.html
  // Now Vite will treat /src/mdi-frontend as the root.
  root: path.resolve(__dirname, 'src/mdi-frontend'),

  // 2. Point the public directory to the new location
  // Files in /src/public will be served at the root path ('/')
  publicDir: path.resolve(__dirname, 'src/public'),

  // 3. Configure the build output directory
  // Compiled files will go to the standard 'dist' folder at project root
  build: {
    outDir: path.resolve(__dirname, 'dist'),
    emptyOutDir: true // Cleans the output directory before building
  }
})
