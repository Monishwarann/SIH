/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        space: {
          900: '#0B0F19',
          800: '#111827',
          700: '#1F2937',
          600: '#374151',
          accent: '#3B82F6',
          alert: '#EF4444',
          success: '#10B981',
          warning: '#F59E0B'
        }
      }
    },
  },
  plugins: [],
}
