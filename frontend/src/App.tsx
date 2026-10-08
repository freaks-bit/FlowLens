import { useEffect, useState } from 'react'
import './App.css'
import { getHealth } from './services/api'

type ApiState = 'checking' | 'online' | 'offline'

function App() {
  const [apiState, setApiState] = useState<ApiState>('checking')

  useEffect(() => {
    getHealth()
      .then(() => setApiState('online'))
      .catch(() => setApiState('offline'))
  }, [])

  const statusMessage = {
    checking: 'Checking backend connection...',
    online: 'FastAPI backend is connected.',
    offline: 'FastAPI backend is unavailable.',
  }[apiState]

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">SMART SPACE ANALYTICS</p>
        <h1>FlowLens</h1>
        <p className="subtitle">
          Privacy-first occupancy monitoring, visitor analytics,
          and operational insights for smarter physical spaces.
        </p>
        <div className={`status-card status-${apiState}`}>
          <span className="status-dot" />
          {statusMessage}
        </div>
      </section>
    </main>
  )
}

export default App