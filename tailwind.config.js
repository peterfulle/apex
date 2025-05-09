/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./core/templates/**/*.html",
    "./templates/**/*.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2a4699',
        secondary: '#10b981',
        accent: '#f59e0b'
      },
      fontFamily: {
        display: ['Montserrat', 'sans-serif'],
        sans: ['Inter', 'sans-serif']
      }
    },
  },
  plugins: [],
}