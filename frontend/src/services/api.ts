import type {
  HealthResponse,
  RecentCountEvent,
  SiteOccupancy,
  ZoneOccupancy,
  ZoneOccupancyHistory,
} from '../types/analytics'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  'http://127.0.0.1:8000'

async function apiRequest<T>(
  path: string,
): Promise<T> {
  const response = await fetch(
    `${API_BASE_URL}${path}`,
  )

  if (!response.ok) {
    let message =
      `Request failed with status ${response.status}`

    try {
      const body = await response.json()

      if (body?.detail) {
        message = body.detail
      }
    } catch {
      // Keep the default message if the
      // response is not JSON.
    }

    throw new Error(message)
  }

  return response.json() as Promise<T>
}

export function getHealth():
  Promise<HealthResponse> {
  return apiRequest<HealthResponse>(
    '/api/v1/health',
  )
}

export function getSiteOccupancy(
  siteId: number,
): Promise<SiteOccupancy> {
  return apiRequest<SiteOccupancy>(
    `/api/v1/sites/${siteId}/occupancy`,
  )
}

export function getZoneOccupancy(
  zoneId: number,
): Promise<ZoneOccupancy> {
  return apiRequest<ZoneOccupancy>(
    `/api/v1/zones/${zoneId}/occupancy`,
  )
}

export function getZoneOccupancyHistory(
  zoneId: number,
  startAt: string,
  endAt: string,
): Promise<ZoneOccupancyHistory> {
  const params = new URLSearchParams({
    start_at: startAt,
    end_at: endAt,
  })

  return apiRequest<ZoneOccupancyHistory>(
    `/api/v1/zones/${zoneId}/history?${params.toString()}`,
  )
}

export function getRecentCountEvents(
  limit = 10,
): Promise<RecentCountEvent[]> {
  const params = new URLSearchParams({
    limit: String(limit),
  })

  return apiRequest<RecentCountEvent[]>(
    `/api/v1/events/recent?${params.toString()}`,
  )
}