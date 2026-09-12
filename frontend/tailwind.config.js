/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#070b14',
          900: '#0b1120',
          800: '#111a2e',
          700: '#182238',
          600: '#22304a',
        },
        accent: {
          blue: '#3b82f6',
          cyan: '#22d3ee',
          green: '#22c55e',
          red: '#ef4444',
          gold: '#f5b942',
        },
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        card: '0 8px 30px -12px rgba(0,0,0,0.5)',
        glow: '0 0 0 1px rgba(59,130,246,0.15), 0 8px 30px -8px rgba(59,130,246,0.25)',
      },
    },
  },
  plugins: [],
}
