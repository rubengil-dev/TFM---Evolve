# frontend/
The web interface: React + TypeScript, built with Vite and styled with Tailwind.

## Run it
It needs [Node.js](https://nodejs.org/) 20 or newer. From this folder:

```bash
npm install
npm run dev
```

Then open http://localhost:5173. `npm run build` leaves the static site in `dist/`, which FastAPI will serve, and `npm run lint` checks the code.

## Structure
```
frontend/
├── public/               # Served as they are (favicon)
├── src/
│   ├── components/       # Pieces shared by several screens
│   ├── config/           # Settings written by hand (questions)
│   ├── pages/            # One file per screen
│   ├── utils/            # Functions used by the components
│   ├── App.tsx           # Decides which screen to show
│   ├── index.css         # Design colors and fonts
│   ├── main.tsx          # Entry point
│   └── types.ts          # Shared types
├── .gitignore            # Kept out of git
├── .oxlintrc.json        # Linter rules
├── index.html            # The only HTML page
├── package.json          # Dependencies and commands
├── package-lock.json     # Exact versions
├── tsconfig.json         # TypeScript entry config
├── tsconfig.app.json     # TypeScript rules for src/
├── tsconfig.node.json    # TypeScript rules for vite.config.ts
└── vite.config.ts        # Vite plugins
```

Not in git, rebuilt by npm: `node_modules/` (installed libraries, like `.venv`) and `dist/` (the built site).

`package.json` and `package-lock.json` have no header comment because JSON does not allow comments.

Fonts and icons are bundled with the app instead of loaded from Google Fonts, so no third party sees who visits the site.
