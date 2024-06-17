/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../../templates/**/*.{html, js}"
  ],
  theme: {
    extend: {
      fontFamily: {
        'montserrat': ['Montserrat', 'sans-serif'],
        'lato': ['Lato', 'sans-serif'],
      },
      defaultFont: 'lato',
    }
  },
  daisyui: {
    themes: ["lofi"],
  },
  plugins: [require('daisyui'),],
}
