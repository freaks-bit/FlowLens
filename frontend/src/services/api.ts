import type {
  HealthResponse,
  SiteOccupancy,
  ZoneOccupancy,
} from '../types/analytics'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

async function apiRequest<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`)

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`

    try {
      const body = await response.json()

      if (body?.detail) {
        message = body.detail
      }
    } catch {
      // Keep the default message if the response is not JSON.
    }

    throw new Error(message)
  }

  return response.json() as Promise<T>
}

export function getHealth(): Promise<HealthResponse> {
  return apiRequest<HealthResponse>('/api/v1/health')
}

export function getSiteOccupancy(
  siteId: number,
): Promise<SiteOccupancy> {
  return apiRequest<SiteOccupancy>(
    `/api/v1/analytics/sites/${siteId}/occupancy`,
  )
}

export function getZoneOccupancy(
  zoneId: number,
): Promise<ZoneOccupancy> {
  return apiRequest<ZoneOccupancy>(
    `/api/v1/analytics/zones/${zoneId}/occupancy`,
  )
}