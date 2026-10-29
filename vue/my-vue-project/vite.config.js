import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // 接口和媒体文件都直连 Django（8000）。接口请求在 src/utils/request.js
      // 里写的是全地址，这里只代理相对路径，主要是让文章封面能显示出来。
      '/media': 'http://127.0.0.1:8000',
    },
  },
})
