function extractHostname(url) {
  try {
    const u = new URL(url)
    return u.hostname.replace('www.', '')
  } catch (_e) {
    return url
  }
}

export default function SourceCard({ url }) {
  const host = extractHostname(url)
  return (
    <a className="source-card" href={url} target="_blank" rel="noreferrer">
      <div className="favicon">
        <img
          src={`https://www.google.com/s2/favicons?domain=${host}&sz=64`}
          alt="favicon"
        />
      </div>
      <div className="source-meta">
        <div className="source-title">{host}</div>
        <div className="source-url">{url}</div>
      </div>
    </a>
  )
}


