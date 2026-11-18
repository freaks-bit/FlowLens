export type OccupancyStatus =
  | 'normal'
  | 'warning'
  | 'critical'

export type EventDirection = 'IN' | 'OUT'

export interface TriggeredAlert {
  rule_id: number
  name: string
  rule_type:
    | 'utilization_percent'
    | 'occupancy'
  threshold: number
  current_value: number
}

export interface ZoneOccupancy {
  zone_id: number
  zone_name: string
  capacity: number
  occupancy: number
  available_capacity: number
  utilization_percent: number
  status: OccupancyStatus
  triggered_alerts: TriggeredAlert[]
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


export type SensorHealthStatus =
  | 'recent'
  | 'stale'
  | 'offline'
  | 'maintenance'
  | 'inactive'
  | 'never_seen'

export interface SensorHealth {
  sensor_id: number
  sensor_name: string
  serial_number: string
  zone_id: number
  zone_name: string
  reported_status: string
  health_status: SensorHealthStatus
  is_active: boolean
  last_seen_at: string | null
  minutes_since_last_seen: number | null
}

export interface SiteSensorHealth {
  site_id: number
  site_name: string
  checked_at: string
  stale_after_minutes: number
  total_sensors: number
  recent_count: number
  stale_count: number
  offline_count: number
  maintenance_count: number
  inactive_count: number
  never_seen_count: number
  sensors: SensorHealth[]
}
