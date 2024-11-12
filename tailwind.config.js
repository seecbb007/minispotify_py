/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './spotify_app/templates/**/*.html',
    './**/*.html',
    './spotify_app/**/*.html',
  ],
  theme: {
    colors: {
      'primary': "#ff77e9",
      'custom-green': "#ccd5ae"  
    },
  },
  plugins: [],
};