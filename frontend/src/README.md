# src/
The app code (React + TypeScript):

- `main.tsx`: Entry point; loads fonts and styles and mounts the app.
- `App.tsx`: Keeps the user's data, asks the backend and decides which screen to show.
- `index.css`: Design colors and fonts (Tailwind theme).
- `types.ts`: Types shared by several files.
- `config/`: Settings written by hand (the questions).
- `pages/`: One file per screen.
- `components/`: Pieces shared by several screens.
- `utils/`: Requests to the backend and shared functions.
