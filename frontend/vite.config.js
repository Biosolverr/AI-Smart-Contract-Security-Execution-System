import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // 🔑 Критично для shadcn/ui: @ → src/
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['framer-motion', '@/components/ui'],
        },
      },
    },
  },
  server: {
    port: 3000,
    open: true,
  },
  // 🔐 Для работы с внешними API (GenLayer)
  define: {
    'process.env': process.env,
  },
});
