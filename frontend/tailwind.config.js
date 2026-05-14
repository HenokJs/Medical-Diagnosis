/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    colors: (() => {
      const scale = {
        50: "#caf0f8",
        100: "#90e0ef",
        200: "#00b4d8",
        300: "#0096c7",
        400: "#0077b6",
        500: "#023e8a",
        600: "#03045e",
        700: "#03045e",
        800: "#03045e",
        900: "#03045e",
      };

      return {
        transparent: "transparent",
        current: "currentColor",
        white: "#ffffff",
        black: "#03045e",
        primary: {
          dark: "#03045e",
          blue: "#0077b6",
          DEFAULT: "#0077b6",
          ...scale,
        },
        medical: {
          dark: "#03045e",
          blue: "#0077b6",
          cyan: "#00b4d8",
          softCyan: "#90e0ef",
          light: "#caf0f8",
        },
        gray: scale,
        neutral: scale,
        blue: scale,
        green: scale,
        red: scale,
        amber: scale,
        purple: scale,
        orange: scale,
      };
    })(),
    extend: {
      fontFamily: {
        sans: ['"IBM Plex Sans"', '"Source Sans 3"', "sans-serif"],
      },
      boxShadow: {
        medical:
          "0 1px 3px 0 rgba(3, 4, 94, 0.12), 0 1px 2px 0 rgba(3, 4, 94, 0.08)",
        "medical-lg":
          "0 12px 20px -6px rgba(3, 4, 94, 0.16), 0 4px 8px -4px rgba(3, 4, 94, 0.08)",
      },
      borderRadius: {
        medical: "0.5rem",
      },
    },
  },
  plugins: [],
};
