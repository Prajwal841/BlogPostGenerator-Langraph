import axios from 'axios'

// Use relative path so Vite dev proxy handles CORS during development
const API_BASE_URL = ''

export async function generatePost(topic) {
  const controller = new AbortController()
  // 2 minute timeout to handle long generations
  const timeoutId = setTimeout(() => controller.abort(), 120000)
  try {
    const response = await axios.post(
      `${API_BASE_URL}/generate`,
      { question: topic },
      {
        headers: { 'Content-Type': 'application/json' },
        signal: controller.signal,
        timeout: 0,
      }
    )
    return response.data
  } finally {
    clearTimeout(timeoutId)
  }
}


