/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["IBM Plex Sans", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "SFMono-Regular"],
      },
      boxShadow: {
        card: "0 8px 24px rgba(15, 23, 42, 0.06)",
        soft: "0 4px 12px rgba(15, 23, 42, 0.08)",
      },
    },
  },
  plugins: [],
};
