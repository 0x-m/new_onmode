module.exports = {
  content: ["./**/*.{html, js}", "./**/**/*.{html, .js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui')
  ],
   daisyui: {
    themes: ["light"],
  },
}
