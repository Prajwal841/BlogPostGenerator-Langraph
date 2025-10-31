import { useState } from 'react'
import './App.css'
import { generatePost } from './services/api'
import Loader from './components/Loader'
import Result from './components/Result'
import TypeStream from './components/TypeStream'

function App() {
  const [topic, setTopic] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [answer, setAnswer] = useState('')
  const [references, setReferences] = useState([])

  async function onSubmit(e) {
    e.preventDefault()
    if (!topic.trim()) return
    setIsLoading(true)
    setError('')
    setAnswer('')
    setReferences([])
    try {
      const data = await generatePost(topic.trim())
      const final = data?.final_output || {}
      setAnswer(final.answer || '')
      setReferences(Array.isArray(final.references) ? final.references : [])
    } catch (err) {
      if (err?.code === 'ERR_CANCELED') {
        setError('Request timed out. Please try again.')
      } else {
        setError('Something went wrong. Please try again.')
      }
    } finally {
      setIsLoading(false)
    }
  }

  function resetAll() {
    setTopic('')
    setError('')
    setAnswer('')
    setReferences([])
    setIsLoading(false)
  }

  return (
    <div className="app-shell">
      <header className="header">
        <div className="brand">
          <div className="logo-glow" />
          <span>Blog Post Generator</span>
        </div>
        {(answer || isLoading) && (
          <button className="btn secondary" onClick={resetAll}>New Post</button>
        )}
      </header>

      <main className="content">
        {!answer && !isLoading && (
          <section className="hero">
            <h1 className="gradient-text">Turn Topics into Polished Posts</h1>
            <p className="sub">
              <TypeStream text="Beautiful, fast, and source-aware." intervalMs={260} />
            </p>
            <form className="input-row" onSubmit={onSubmit}>
              <input
                className="topic-input"
                placeholder="Enter a blog topic, e.g. Football evolution in 2025"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
              />
              <button className="btn" type="submit" disabled={!topic.trim()}>
                Generate
              </button>
            </form>
            {error && <div className="error-box">{error}</div>}
          </section>
        )}

        {isLoading && (
          <Loader message="Your post is being generated…" />
        )}

        {!isLoading && answer && (
          <Result
            answer={answer}
            references={references}
            onNew={resetAll}
          />
        )}
      </main>

      {/* footer removed per request */}
    </div>
  )
}

export default App
