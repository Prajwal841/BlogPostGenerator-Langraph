export default function Loader({ message = 'Your post is being generated…' }) {
  return (
    <div className="loader">
      <div className="glow-ring">
        <div className="ring" />
        <div className="ring ring2" />
        <div className="ring ring3" />
      </div>
      <div className="typing">
        <span className="dot" />
        <span className="dot" />
        <span className="dot" />
      </div>
      <p className="loader-text shimmer">{message}</p>
      <div className="skeleton">
        <div className="skeleton-line" />
        <div className="skeleton-line" />
        <div className="skeleton-line short" />
      </div>
    </div>
  )
}


