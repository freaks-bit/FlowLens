import type {
  RecentCountEvent,
} from '../types/analytics'

interface RecentActivityFeedProps {
  events: RecentCountEvent[]
}

function formatEventTime(
  timestamp: string,
) {
  return new Date(timestamp).toLocaleString(
    [],
    {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    },
  )
}

function RecentActivityFeed({
  events,
}: RecentActivityFeedProps) {
  if (events.length === 0) {
    return (
      <article className="activity-card">
        <div className="activity-empty">
          No visitor activity recorded yet.
        </div>
      </article>
    )
  }

  return (
    <article className="activity-card">
      <div className="activity-list">
        {events.map((event) => {
          const isEntry =
            event.direction === 'IN'

          return (
            <div
              className="activity-item"
              key={event.event_id}
            >
              <div
                className={`activity-icon ${
                  isEntry
                    ? 'activity-icon-in'
                    : 'activity-icon-out'
                }`}
              >
                {isEntry ? 'IN' : 'OUT'}
              </div>

              <div className="activity-details">
                <div className="activity-main-row">
                  <div>
                    <strong>
                      {event.zone_name}
                    </strong>

                    <span className="activity-sensor">
                      {event.sensor_name}
                    </span>
                  </div>

                  <strong
                    className={
                      isEntry
                        ? 'activity-count-in'
                        : 'activity-count-out'
                    }
                  >
                    {isEntry ? '+' : '-'}
                    {event.count}
                  </strong>
                </div>

                <div className="activity-meta">
                  <span>
                    Zone {event.zone_id}
                  </span>

                  <span>•</span>

                  <span>
                    {formatEventTime(
                      event.occurred_at,
                    )}
                  </span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </article>
  )
}

export default RecentActivityFeed