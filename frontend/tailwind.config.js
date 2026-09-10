/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f5f3ff',
          100: '#ede9fe',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          900: '#4c1d95',
        },
        dark: {
          base: '#0B0F19',
          card: '#111827',
          border: '#1F2937',
          input: '#1F2937',
          hover: '#1F2937'
        }
      }
    },
  },
  plugins: [],
}
