
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './spotify_app/templates/**/*.html',
    './**/*.html',
    './spotify_app/**/*.html',
    './spotify_app/**/*.{html,js}',  // Added .js files
    './**/templates/**/*.html',      // Added for any app's templates
    './static/**/*.js',              // Added for static JS files
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
