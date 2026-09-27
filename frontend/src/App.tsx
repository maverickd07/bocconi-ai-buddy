// Placeholder UI. Build the real frontend here.
// Expected: a chat-like interface that calls POST /ask on the backend
// and displays { answer, sources, verticale }.
// See AGENTS.md and README.md for the full spec.
//
// Backend URL is configured via the VITE_BACKEND_URL env var.
// In dev (docker-compose.dev.yml) it defaults to http://localhost:8000.
// On Railway, set it to your backend service public URL.

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? 'http://localhost:8000';

function App() {
  return (
    <main style={{ padding: 32, fontFamily: 'system-ui' }}>
      <h1>Build me</h1>
      <p>
        Replace this placeholder with the AI Buddy UI. Read{' '}
        <code>AGENTS.md</code> for the spec.
      </p>
      <p>
        <small>Backend URL: <code>{BACKEND_URL}</code></small>
      </p>
    </main>
  );
}

export default App;
