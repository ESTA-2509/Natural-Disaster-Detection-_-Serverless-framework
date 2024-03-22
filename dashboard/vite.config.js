import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/list': {
        target: 'https://disaster-us-east-1.thienlinh.link',
        changeOrigin: true
      },
      '/upload': {
        target: 'https://disaster-us-east-1.thienlinh.link',
        changeOrigin: true
      }
    }
  }
});
