/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        black: '#212427',
        white: '#f7f8fa',
        primary: '#ccff00'
      }
    },
    fontFamily: {
      sans: ['"Raleway"', 'sans-serif'],
      mono: ['"Fira Code"', 'monospace']
    }
  },
  plugins: []
};
