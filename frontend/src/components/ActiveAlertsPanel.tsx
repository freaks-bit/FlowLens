import type {
  ZoneOccupancy,
} from '../types/analytics'

interface ActiveAlertsPanelProps {
  zones: ZoneOccupancy[]
}

function formatAlertValue(
  ruleType: string,
  value: number,
) {
  if (ruleType === 'utilization_percent') {
    return `${value.toFixed(2)}%`
  }

  return `${value.toLocaleString()} people`
}

function ActiveAlertsPanel({
  zones,
}: ActiveAlertsPanelProps) {
  const activeAlerts = zones.flatMap(
    (zone) =>
      zone.triggered_alerts.map(
        (alert) => ({
          ...alert,
          zone_id: zone.zone_id,
          zone_name: zone.zone_name,
        }),
      ),
  )

  if (activeAlerts.length === 0) {
    return (
      <article className="alerts-card alerts-clear">
        <div className="alerts-clear-icon">
          ✓
        </div>

        <div>
          <strong>
            No active occupancy alerts
          </strong>

          <p>
            All monitored zones are currently
            below their configured alert
            thresholds.
          </p>
        </div>
      </article>
    )
  }

  return (
    <article className="alerts-card">
      <div className="alerts-list">
        {activeAlerts.map((alert) => (
          <div
            className="alert-item"
            key={alert.rule_id}
          >
            <div className="alert-indicator">
              !
            </div>

            <div className="alert-details">
              <div className="alert-main-row">
                <div>
                  <strong>
                    {alert.name}
                  </strong>

                  <span>
                    Zone {alert.zone_id} —{' '}
                    {alert.zone_name}
                  </span>
                </div>

                <span className="alert-triggered-badge">
                  Triggered
                </span>
              </div>

              <div className="alert-values">
                <div>
                  <span>
                    Current
                  </span>

                  <strong>
                    {formatAlertValue(
                      alert.rule_type,
                      alert.current_value,
                    )}
                  </strong>
                </div>

                <div>
                  <span>
                    Threshold
                  </span>

                  <strong>
                    {formatAlertValue(
                      alert.rule_type,
                      alert.threshold,
                    )}
                  </strong>
                </div>

                <div>
                  <span>
                    Rule type
                  </span>

                  <strong>
                    {alert.rule_type ===
                    'utilization_percent'
                      ? 'Utilization'
                      : 'Occupancy'}
                  </strong>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </article>
  )
}

export default ActiveAlertsPanel