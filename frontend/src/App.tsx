import {
  type ChangeEvent,
  useCallback,
  useEffect,
  useState,
} from 'react'

import './App.css'

import ActiveAlertsPanel from './components/ActiveAlertsPanel'
import OccupancyHistoryChart from './components/OccupancyHistoryChart'
import RecentActivityFeed from './components/RecentActivityFeed'

import {
  getHealth,
  getRecentCountEvents,
  getSiteOccupancy,
  getZoneOccupancyHistory,
} from './services/api'

import type {
  HealthResponse,
  RecentCountEvent,
  SiteOccupancy,
  ZoneOccupancy,
  ZoneOccupancyHistory,
} from './types/analytics'

const SITE_ID = 1
const DEFAULT_HISTORY_ZONE_ID = 1
const DEFAULT_HISTORY_DAYS = 14
const RECENT_EVENT_LIMIT = 8

const HISTORY_RANGE_OPTIONS = [
  {
    label: '24 hours',
    days: 1,
  },
  {
    label: '7 days',
    days: 7,
  },
  {
    label: '14 days',
    days: 14,
  },
  {
    label: '30 days',
    days: 30,
  },
]

function formatPercent(value: number) {
  return `${value.toFixed(2)}%`
}

function statusLabel(
  status: ZoneOccupancy['status'],
) {
  if (status === 'critical') {
    return 'Critical'
  }

  if (status === 'warning') {
    return 'Warning'
  }

  return 'Normal'
}

function getHistoryRange(days: number) {
  const endAt = new Date()

  const startAt = new Date(
    endAt.getTime() -
      days * 24 * 60 * 60 * 1000,
  )

  return {
    startAt: startAt.toISOString(),
    endAt: endAt.toISOString(),
  }
}

function App() {
  const [health, setHealth] =
    useState<HealthResponse | null>(null)

  const [site, setSite] =
    useState<SiteOccupancy | null>(null)

  const [history, setHistory] =
    useState<ZoneOccupancyHistory | null>(
      null,
    )

  const [recentEvents, setRecentEvents] =
    useState<RecentCountEvent[]>([])

  const [
    selectedHistoryZoneId,
    setSelectedHistoryZoneId,
  ] = useState(DEFAULT_HISTORY_ZONE_ID)

  const [
    selectedHistoryDays,
    setSelectedHistoryDays,
  ] = useState(DEFAULT_HISTORY_DAYS)

  const [loading, setLoading] =
    useState(true)

  const [refreshing, setRefreshing] =
    useState(false)

  const [
    historyLoading,
    setHistoryLoading,
  ] = useState(false)

  const [error, setError] =
    useState<string | null>(null)

  const [lastUpdated, setLastUpdated] =
    useState<Date | null>(null)

  const fetchDashboard =
    useCallback(async () => {
      try {
        const { startAt, endAt } =
          getHistoryRange(
            selectedHistoryDays,
          )

        setHistoryLoading(true)

        const [
          healthResult,
          siteResult,
          historyResult,
          recentEventsResult,
        ] = await Promise.all([
          getHealth(),

          getSiteOccupancy(SITE_ID),

          getZoneOccupancyHistory(
            selectedHistoryZoneId,
            startAt,
            endAt,
          ),

          getRecentCountEvents(
            RECENT_EVENT_LIMIT,
          ),
        ])

        setHealth(healthResult)
        setSite(siteResult)
        setHistory(historyResult)

        setRecentEvents(
          recentEventsResult,
        )

        setError(null)
        setLastUpdated(new Date())
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : 'Unable to load FlowLens dashboard'

        setHealth(null)
        setError(message)
      } finally {
        setLoading(false)
        setRefreshing(false)
        setHistoryLoading(false)
      }
    }, [
      selectedHistoryZoneId,
      selectedHistoryDays,
    ])

  const handleRefresh = () => {
    setRefreshing(true)
    setError(null)

    void fetchDashboard()
  }

  const handleHistoryZoneChange = (
    event: ChangeEvent<HTMLSelectElement>,
  ) => {
    setSelectedHistoryZoneId(
      Number(event.target.value),
    )
  }

  useEffect(() => {
    const initialLoadId =
      window.setTimeout(() => {
        void fetchDashboard()
      }, 0)

    const intervalId =
      window.setInterval(() => {
        void fetchDashboard()
      }, 15000)

    return () => {
      window.clearTimeout(
        initialLoadId,
      )

      window.clearInterval(
        intervalId,
      )
    }
  }, [fetchDashboard])

  if (loading) {
    return (
      <main className="app-shell center-state">
        <div className="spinner" />

        <p>
          Loading FlowLens analytics...
        </p>
      </main>
    )
  }

  const activeAlertCount =
    site?.zones.reduce(
      (total, zone) =>
        total +
        zone.triggered_alerts.length,
      0,
    ) ?? 0

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">
            SMART SPACE ANALYTICS
          </p>

          <h1>FlowLens</h1>

          <p className="subtitle">
            Live occupancy intelligence for
            smarter physical spaces.
          </p>
        </div>

        <div className="topbar-actions">
          <div
            className={`connection-pill ${
              health?.database ===
              'connected'
                ? 'connection-ok'
                : 'connection-error'
            }`}
          >
            <span className="status-dot" />

            {health?.database ===
            'connected'
              ? 'Backend connected'
              : 'Backend unavailable'}
          </div>

          <button
            className="refresh-button"
            onClick={handleRefresh}
            disabled={refreshing}
          >
            {refreshing
              ? 'Refreshing...'
              : 'Refresh data'}
          </button>
        </div>
      </header>

      {error && (
        <section className="error-banner">
          <strong>
            Unable to refresh dashboard.
          </strong>

          <span>{error}</span>
        </section>
      )}

      {site && (
        <>
          <section className="section-heading">
            <div>
              <p className="section-kicker">
                SITE OVERVIEW
              </p>

              <h2>
                {site.site_name}
              </h2>
            </div>

            <p className="updated-text">
              {lastUpdated
                ? `Updated ${lastUpdated.toLocaleTimeString()}`
                : 'Not updated yet'}
            </p>
          </section>

          <section className="metric-grid">
            <article className="metric-card primary-card">
              <p className="metric-label">
                Current occupancy
              </p>

              <div className="metric-value-row">
                <strong className="metric-value">
                  {site.total_occupancy.toLocaleString()}
                </strong>

                <span className="metric-unit">
                  people
                </span>
              </div>

              <p className="metric-helper">
                Across{' '}
                {site.zones.length}{' '}
                monitored zones
              </p>
            </article>

            <article className="metric-card">
              <p className="metric-label">
                Total zone capacity
              </p>

              <strong className="metric-value">
                {site.total_capacity.toLocaleString()}
              </strong>

              <p className="metric-helper">
                Configured capacity
              </p>
            </article>

            <article className="metric-card">
              <p className="metric-label">
                Available capacity
              </p>

              <strong className="metric-value">
                {site.available_capacity.toLocaleString()}
              </strong>

              <p className="metric-helper">
                Spaces currently available
              </p>
            </article>

            <article className="metric-card">
              <p className="metric-label">
                Site utilization
              </p>

              <strong className="metric-value">
                {formatPercent(
                  site.utilization_percent,
                )}
              </strong>

              <div className="progress-track">
                <div
                  className="progress-fill"
                  style={{
                    width: `${Math.min(
                      site.utilization_percent,
                      100,
                    )}%`,
                  }}
                />
              </div>
            </article>
          </section>

          <section className="alerts-section">
            <div className="section-heading">
              <div>
                <p className="section-kicker">
                  OCCUPANCY ALERTS
                </p>

                <h2>
                  Active alert rules
                </h2>
              </div>

              <span
                className={`alert-count-pill ${
                  activeAlertCount > 0
                    ? 'alert-count-active'
                    : 'alert-count-clear'
                }`}
              >
                {activeAlertCount > 0
                  ? `${activeAlertCount} active`
                  : 'All clear'}
              </span>
            </div>

            <ActiveAlertsPanel
              zones={site.zones}
            />
          </section>

          <section className="history-section">
            <div className="history-section-heading">
              <div>
                <p className="section-kicker">
                  HISTORICAL ANALYTICS
                </p>

                <h2>
                  {history
                    ? `${history.zone_name} occupancy`
                    : 'Zone occupancy'}
                </h2>
              </div>

              <div className="history-controls">
                <div className="history-control">
                  <label
                    htmlFor="history-zone"
                    className="history-control-label"
                  >
                    Historical zone
                  </label>

                  <select
                    id="history-zone"
                    className="history-zone-select"
                    value={
                      selectedHistoryZoneId
                    }
                    onChange={
                      handleHistoryZoneChange
                    }
                    disabled={
                      historyLoading
                    }
                  >
                    {site.zones.map(
                      (zone) => (
                        <option
                          key={
                            zone.zone_id
                          }
                          value={
                            zone.zone_id
                          }
                        >
                          Zone{' '}
                          {zone.zone_id}{' '}
                          —{' '}
                          {zone.zone_name}
                        </option>
                      ),
                    )}
                  </select>
                </div>

                <div className="history-control">
                  <span className="history-control-label">
                    Time range
                  </span>

                  <div className="history-range-buttons">
                    {HISTORY_RANGE_OPTIONS.map(
                      (option) => (
                        <button
                          key={
                            option.days
                          }
                          type="button"
                          className={`history-range-button ${
                            selectedHistoryDays ===
                            option.days
                              ? 'history-range-active'
                              : ''
                          }`}
                          onClick={() =>
                            setSelectedHistoryDays(
                              option.days,
                            )
                          }
                          disabled={
                            historyLoading
                          }
                          aria-pressed={
                            selectedHistoryDays ===
                            option.days
                          }
                        >
                          {
                            option.label
                          }
                        </button>
                      ),
                    )}
                  </div>
                </div>
              </div>
            </div>

            {historyLoading &&
            history ? (
              <div className="history-loading-card">
                <div className="small-spinner" />

                <span>
                  Loading historical
                  data...
                </span>
              </div>
            ) : history ? (
              <OccupancyHistoryChart
                history={history}
              />
            ) : (
              <div className="history-loading-card">
                <span>
                  Historical data is
                  unavailable.
                </span>
              </div>
            )}
          </section>

          <section className="activity-section">
            <div className="section-heading">
              <div>
                <p className="section-kicker">
                  RECENT ACTIVITY
                </p>

                <h2>
                  Visitor event feed
                </h2>
              </div>

              <p className="updated-text">
                Latest{' '}
                {RECENT_EVENT_LIMIT}{' '}
                events
              </p>
            </div>

            <RecentActivityFeed
              events={recentEvents}
            />
          </section>

          <section className="zones-section">
            <div className="section-heading">
              <div>
                <p className="section-kicker">
                  LIVE ZONES
                </p>

                <h2>
                  Occupancy by zone
                </h2>
              </div>
            </div>

            <div className="zone-grid">
              {site.zones.map(
                (zone) => (
                  <article
                    className="zone-card"
                    key={zone.zone_id}
                  >
                    <div className="zone-card-header">
                      <div>
                        <p className="zone-id">
                          Zone{' '}
                          {zone.zone_id}
                        </p>

                        <h3>
                          {
                            zone.zone_name
                          }
                        </h3>
                      </div>

                      <span
                        className={`status-badge status-${zone.status}`}
                      >
                        {statusLabel(
                          zone.status,
                        )}
                      </span>
                    </div>

                    <div className="zone-occupancy-row">
                      <strong>
                        {
                          zone.occupancy
                        }
                      </strong>

                      <span>
                        /{' '}
                        {zone.capacity}{' '}
                        people
                      </span>
                    </div>

                    <div className="progress-track zone-progress">
                      <div
                        className={`progress-fill fill-${zone.status}`}
                        style={{
                          width: `${Math.min(
                            zone.utilization_percent,
                            100,
                          )}%`,
                        }}
                      />
                    </div>

                    <div className="zone-stats">
                      <div>
                        <span>
                          Utilization
                        </span>

                        <strong>
                          {formatPercent(
                            zone.utilization_percent,
                          )}
                        </strong>
                      </div>

                      <div>
                        <span>
                          Available
                        </span>

                        <strong>
                          {
                            zone.available_capacity
                          }
                        </strong>
                      </div>
                    </div>
                  </article>
                ),
              )}
            </div>
          </section>
        </>
      )}
    </main>
  )
}

export default App