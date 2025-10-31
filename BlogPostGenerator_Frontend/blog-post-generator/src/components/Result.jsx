import { useState } from 'react'
import SourceCard from './SourceCard'

export default function Result({ answer, references, onNew }) {
  const [copied, setCopied] = useState(false)

  async function copyAnswer() {
    try {
      await navigator.clipboard.writeText(answer || '')
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch (_e) {}
  }

  return (
    <div className="result-layout">
      <div className="result-main">
        <div className="result-header">
          <h2 className="gradient-text big-title">Generated Blog Post</h2>
          <div className="result-actions">
            <button className="btn secondary" onClick={onNew}>New Post</button>
            <button
              className={`btn copy-btn ${copied ? 'copied' : ''}`}
              onClick={copyAnswer}
            >
              <span className="copy-label">{copied ? 'Copied' : 'Copy'}</span>
              <span className="copy-sparkle" aria-hidden />
            </button>
          </div>
        </div>
        <div className="answer-box larger-text">
          {answer ? answer : 'No content.'}
        </div>
      </div>

      <aside className="result-aside">
        <div className="aside-title">References</div>
        <div className="sources-grid">
          {(references || []).map((u, i) => (
            <SourceCard key={i} url={u} />
          ))}
        </div>
      </aside>
    </div>
  )
}


