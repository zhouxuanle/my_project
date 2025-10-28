/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'app-dark': '#282c34',
        'app-hover': '#3a3f47',
      },
      fontSize: {
        'dynamic-sm': 'clamp(11px, 1vw, 15px)',
        'dynamic-base': 'clamp(12px, 1.2vw, 20px)',
      },
      spacing: {
        'dynamic': '1.5vw',
      },
    },
  },
  plugins: [],
}