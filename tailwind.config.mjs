/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        vp: {
          bg: '#09090b',
          surface: '#18181b',
          'surface-2': '#27272a',
          accent: '#f59e0b',
          'accent-hover': '#d97706',
          text: '#fafafa',
          muted: '#a1a1aa',
          border: '#3f3f46',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
