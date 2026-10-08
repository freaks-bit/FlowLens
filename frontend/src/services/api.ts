const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

export type HealthResponse = {
  status: string
  service: string
}

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`)

  if (!response.ok) {
    throw new Error(`Health request failed: ${response.status}`)
  }

  return response.json()
}