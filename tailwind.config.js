
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',           // For global templates folder
    './spotify_app/templates/**/*.html',  // If you have an app-specific folder
    './**/*.html',                     // To ensure all HTML files are covered
    './spotify_app/**/*.html',         // To cover HTML files inside the app folder
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
