# frontend/
The web interface: React + TypeScript, built with Vite and styled with Tailwind.

## Run it
It needs [Node.js](https://nodejs.org/) 20 or newer. From this folder:

```bash
npm install
npm run dev
```

Then open http://localhost:5173. The backend has to be running too (`uv run uvicorn bioage.app.api:app` from the root): Vite sends it the `/api` requests. `npm run build` leaves the static site in `dist/`, which FastAPI will serve, and `npm run lint` checks the code.

## Screens
Every screen opens directly with `?demo=<name>`, with made-up data and without the backend. Best seen at phone size (in the browser's developer tools, device toolbar).

| Screen | Link |
|---|---|
| Landing, with the fine print at the bottom | http://localhost:5173 |
| Question: sex | http://localhost:5173/?demo=sex |
| Question: age | http://localhost:5173/?demo=age |
| Question: weight | http://localhost:5173/?demo=weight |
| Question: height | http://localhost:5173/?demo=height |
| Question: smoking | http://localhost:5173/?demo=smoking |
| Question: exercise | http://localhost:5173/?demo=physical_activity |
| Question: hours sitting | http://localhost:5173/?demo=sedentary_hours |
| Question: hours of sleep | http://localhost:5173/?demo=sleep_hours |
| Loading: reading the PDF | http://localhost:5173/?demo=reading |
| Loading: calculating | http://localhost:5173/?demo=calculating |
| Impossible value window | http://localhost:5173/?demo=odd_value |
| Result | http://localhost:5173/?demo=result |
| Result with the red and grey warnings | http://localhost:5173/?demo=older |
| Error: unreadable PDF | http://localhost:5173/?demo=unreadable |
| Error: too few values | http://localhost:5173/?demo=too_few |
| Error: impossible value confirmed | http://localhost:5173/?demo=impossible |
| Error: impossible BMI | http://localhost:5173/?demo=impossible_bmi |
| Error: under 16 | http://localhost:5173/?demo=too_young |
| Error: over 90 | http://localhost:5173/?demo=too_old |
| Error: no answer from the server | http://localhost:5173/?demo=unavailable |
| Error: the server failed | http://localhost:5173/?demo=failed |

## Structure
```
frontend/
├── public/               # Served as they are (favicon)
├── src/
│   ├── components/       # Pieces shared by several screens
│   ├── config/           # Settings written by hand (questions, texts)
│   ├── pages/            # One file per screen
│   ├── utils/            # Requests to the backend and shared functions
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
└── vite.config.ts        # Vite plugins and where the backend is
```

Not in git, rebuilt by npm: `node_modules/` (installed libraries, like `.venv`) and `dist/` (the built site).

`package.json` and `package-lock.json` have no header comment because JSON does not allow comments.

Fonts and icons are bundled with the app instead of loaded from Google Fonts, so no third party sees who visits the site.
