/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eef3f9',
          100: '#d4e0ef',
          200: '#a9c1df',
          300: '#7ea2cf',
          400: '#5383bf',
          500: '#1e3a5f',
          600: '#1a3254',
          700: '#152a48',
          800: '#11213d',
          900: '#0c1931',
        },
        accent: {
          50: '#fdf6e7',
          100: '#f9e8bf',
          200: '#f4d588',
          300: '#efc251',
          400: '#e8a317',
          500: '#d49212',
          600: '#b87d0f',
          700: '#9c680c',
          800: '#805409',
          900: '#644006',
        },
        risk: {
          low: '#22c55e',
          moderate: '#eab308',
          elevated: '#f97316',
          high: '#ef4444',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
