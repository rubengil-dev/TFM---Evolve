/** Entry point: loads fonts and styles and mounts the app inside index.html. */

import '@fontsource-variable/fraunces'
import '@fontsource-variable/fraunces/wght-italic.css'
import '@fontsource-variable/inter'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'

// Always open at the top: no restored scroll, no #anchor left from an earlier visit
window.history.scrollRestoration = 'manual'
if (window.location.hash) window.history.replaceState(null, '', window.location.pathname + window.location.search)

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
