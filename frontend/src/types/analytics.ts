export type OccupancyStatus =
  | 'normal'
  | 'warning'
  | 'critical'

export type EventDirection = 'IN' | 'OUT'

export interface ZoneOccupancy {
  zone_id: number
  zone_name: string
  capacity: number
  occupancy: number
  available_capacity: number
  utilization_percent: number
  status: OccupancyStatus
}

export interface SiteOccupancy {
  site_id: number
  site_name: string
  total_capacity: number
  total_occupancy: number
  available_capacity: number
  utilization_percent: number
  zones: ZoneOccupancy[]
}

export interface OccupancyHistoryPoint {
  timestamp: string
  occupancy: number
}

export interface ZoneOccupancyHistory {
  zone_id: number
  zone_name: string
  start_at: string
  end_at: string
  points: OccupancyHistoryPoint[]
}

export interface RecentCountEvent {
  event_id: number
  sensor_id: number
  sensor_name: string
  zone_id: number
  zone_name: string
  direction: EventDirection
  count: number
  occurred_at: string
}

export interface HealthResponse {
  status: string
  service: string
  database: string
}