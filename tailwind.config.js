/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./**/*.html', '!./node_modules/**'],
  theme: {
    extend: {
      colors: {
        ink:          '#0E0E10',
        'ink-2':      '#1A1A1E',
        navy:         '#0D1E35',
        'navy-2':     '#162843',
        paper:        '#F4F2ED',
        'paper-2':    '#E9E6DE',
        accent:       '#1B3A6B',
        'accent-h':   '#142d54',
        'accent-ink': '#2E5BA6',
        muted:        '#4A4A47',
        'muted-ink':  '#5E5E65',
        'line-light': '#D9D4C8',
      },
      fontFamily: {
        serif: ['"Noto Serif JP"', 'serif'],
        mono:  ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
    }
  },
  plugins: [],
}
