export type OccupancyStatus = 'normal' | 'warning' | 'critical'

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

export interface HealthResponse {
  status: string
  service: string
  database: string
}