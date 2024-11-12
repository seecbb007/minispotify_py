
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './spotify_app/templates/**/*.html',
    './**/*.html',
    './spotify_app/**/*.html',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: "#ff77e9",
        customGreen: "#ccd5ae",
        customPink: '#ff77e9',
      },
    },
  },
  plugins: [],
};
