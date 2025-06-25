// nuxt.config.ts
export default defineNuxtConfig({
  compatibilityDate: '2025-06-21',
  modules: ['@nuxtjs/tailwindcss'],
  vite: {
    plugins: []
  },
  nitro: {
    devProxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path: string) => path.replace(/^\/api/, '')
      }
    }
  },
  app: {
    pageTransition: { name: 'page', mode: 'out-in' }
  }
})