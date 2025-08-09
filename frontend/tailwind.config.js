/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1a1a1a',
        'btn-bg': '#007bff',
        'lightlavender': '#e6e6fa',
        'cool-gray': '#6b7280',
      },
      fontFamily: {
        'switzer': ['Switzer', 'sans-serif'],
        'switzerMedium': ['Switzer-Medium', 'sans-serif'],
        'quicksand': ['Quicksand', 'sans-serif'],
      },
    },
  },
  plugins: [],
} 