import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      external: ['styled-components']
    }
  },
  resolve: {
    alias: {
      'styled-components': 'styled-components/dist/styled-components.esm.js'
    }
  }
})
