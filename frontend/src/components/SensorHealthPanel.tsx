
import { useCallback, useEffect, useState } from 'react'

import { getSiteSensorHealth } from '../services/api'
import type {
  SensorHealthStatus,
  SiteSensorHealth,
} from '../types/analytics'

import './SensorHealthPanel.css'

interface Props {
  siteId: number
}

const statusLabels: Record<SensorHealthStatus, string> = {
  recent: 'Recent data',
  stale: 'Stale',
  offline: 'Offline',
  maintenance: 'Maintenance',
  inactive: 'Inactive',
  never_seen: 'Never seen',
}

function formatLastSeen(timestamp: string | null) {
  if (!timestamp) return 'No events received'

  return new Date(timestamp).toLocaleString(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}

function formatAge(minutes: number | null) {
  if (minutes === null) return 'Never'

  if (minutes >= 1440) {
    return `${Math.floor(minutes / 1440)} days ago`
  }

  if (minutes >= 60) {
    return `${Math.floor(minutes / 60)} hours ago`
  }

  return `${Math.floor(minutes)} minutes ago`
}

export default function SensorHealthPanel({ siteId }: Props) {
  const [data, setData] = useState<SiteSensorHealth | null>(
    null,
  )
  const [error, setError] = useState<string | null>(null)
  const [refreshing, setRefreshing] = useState(false)

  const loadSensors = useCallback(async () => {
    try {
      const result = await getSiteSensorHealth(siteId)
      setData(result)
      setError(null)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to load sensor health',
      )
    }
  }, [siteId])

  useEffect(() => {
    const initialId = window.setTimeout(() => {
      void loadSensors()
    }, 0)

    const intervalId = window.setInterval(() => {
      void loadSensors()
    }, 30000)

    return () => {
      window.clearTimeout(initialId)
      window.clearInterval(intervalId)
    }
  }, [loadSensors])

  async function handleRefresh() {
    setRefreshing(true)

    try {
      await loadSensors()
    } finally {
      setRefreshing(false)
    }
  }

  const otherCount = data
    ? data.maintenance_count +
      data.inactive_count +
      data.never_seen_count
    : 0

  const summaries = data
    ? [
        { label: 'Total', value: data.total_sensors },
        { label: 'Recent', value: data.recent_count },
        { label: 'Stale', value: data.stale_count },
        { label: 'Offline', value: data.offline_count },
        { label: 'Other', value: otherCount },
      ]
    : []

  return (
    <section className="sensor-health-section">
      <div className="section-heading">
        <div>
          <p className="section-kicker">SENSOR OPERATIONS</p>
          <h2>Sensor health</h2>
        </div>

        <div className="sensor-health-actions">
          <span className="updated-text">
            {data
              ? `Checked ${new Date(
                  data.checked_at,
                ).toLocaleTimeString()}`
              : 'Waiting for data'}
          </span>

          <button
            type="button"
            className="refresh-button"
            disabled={refreshing}
            onClick={() => void handleRefresh()}
          >
            {refreshing ? 'Refreshing...' : 'Refresh sensors'}
          </button>
        </div>
      </div>

      <div className="sensor-health-panel">
        <p className="sensor-health-note">
          Activity freshness is based on the last received
          visitor event. Stale data does not necessarily mean
          that a physical sensor is disconnected.
        </p>

        {error && (
          <div className="sensor-health-error" role="alert">
            Sensor health could not be refreshed: {error}
          </div>
        )}

        {!data && !error && (
          <p className="sensor-health-loading">
            Checking sensor activity...
          </p>
        )}

        {data && (
          <>
            <div className="sensor-health-summary">
              {summaries.map((summary) => (
                <div
                  className="sensor-health-summary-item"
                  key={summary.label}
                >
                  <span>{summary.label}</span>
                  <strong>{summary.value}</strong>
                </div>
              ))}
            </div>

            {data.sensors.length === 0 ? (
              <p className="sensor-health-loading">
                No sensors registered for this site.
              </p>
            ) : (
              <div className="sensor-health-grid">
                {data.sensors.map((sensor) => (
                  <article
                    className="sensor-health-card"
                    key={sensor.sensor_id}
                  >
                    <div className="sensor-health-card-top">
                      <div>
                        <p className="sensor-health-zone">
                          {sensor.zone_name}
                        </p>
                        <h3>{sensor.sensor_name}</h3>
                      </div>

                      <span
                        className={`sensor-health-badge sensor-health-${sensor.health_status}`}
                      >
                        {statusLabels[sensor.health_status]}
                      </span>
                    </div>

                    <div className="sensor-health-card-details">
                      <div>
                        <span>Serial number</span>
                        <strong>{sensor.serial_number}</strong>
                      </div>

                      <div>
                        <span>Reported status</span>
                        <strong>{sensor.reported_status}</strong>
                      </div>

                      <div>
                        <span>Last event received</span>
                        <strong>
                          {formatLastSeen(sensor.last_seen_at)}
                        </strong>
                      </div>

                      <div>
                        <span>Time since last event</span>
                        <strong>
                          {formatAge(
                            sensor.minutes_since_last_seen,
                          )}
                        </strong>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </section>
  )
}
