/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "background-primary": "#121212",
        "background-secondary": "#1E1E1E",
        "text-primary": "#F5F5F5",
        "text-secondary": "#BBBBBB",
        "accent-purple": "#BB86FC",
        "accent-teal": "#03DAC6",
      },
    },
  },
  plugins: [],
};
