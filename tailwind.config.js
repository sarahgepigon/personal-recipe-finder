/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',  // Ensure Tailwind scans your templates for classes
    './static/**/*.js',    // Scan JS files if needed
  ],
  theme: {
    extend: {
      colors: {
        'neon-green': '#39FF14',  // Custom neon-green color
      },
    },
  },
  plugins: [],
}