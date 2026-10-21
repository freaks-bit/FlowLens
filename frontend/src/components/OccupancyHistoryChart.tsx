import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import type { ZoneOccupancyHistory } from '../types/analytics'

interface OccupancyHistoryChartProps {
  history: ZoneOccupancyHistory
}

function formatAxisDate(timestamp: number) {
  return new Date(timestamp).toLocaleDateString([], {
    month: 'short',
    day: 'numeric',
  })
}

function formatTooltipDate(timestamp: number) {
  return new Date(timestamp).toLocaleString([], {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function OccupancyHistoryChart({
  history,
}: OccupancyHistoryChartProps) {
  const originalPoints = history.points.map((point) => ({
    timestamp: new Date(point.timestamp).getTime(),
    occupancy: point.occupancy,
  }))

  const lastPoint = originalPoints.at(-1)
  const endTimestamp = new Date(history.end_at).getTime()

  const chartData =
    lastPoint && lastPoint.timestamp < endTimestamp
      ? [
          ...originalPoints,
          {
            timestamp: endTimestamp,
            occupancy: lastPoint.occupancy,
          },
        ]
      : originalPoints

  const peakOccupancy = Math.max(
    ...originalPoints.map((point) => point.occupancy),
    0,
  )

  const currentOccupancy =
    originalPoints.at(-1)?.occupancy ?? 0

  return (
    <article className="history-card">
      <div className="history-card-header">
        <div>
          <p className="history-label">
            EVENT-DERIVED OCCUPANCY
          </p>

          <p className="history-description">
            Occupancy reconstructed from visitor IN and OUT
            events.
          </p>
        </div>

        <div className="history-summary-grid">
          <div className="history-summary">
            <span>Current</span>
            <strong>{currentOccupancy}</strong>
          </div>

          <div className="history-summary">
            <span>Peak</span>
            <strong>{peakOccupancy}</strong>
          </div>
        </div>
      </div>

      <div className="history-chart">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{
              top: 20,
              right: 20,
              bottom: 5,
              left: -15,
            }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(148, 163, 184, 0.12)"
              vertical={false}
            />

            <XAxis
              dataKey="timestamp"
              type="number"
              scale="time"
              domain={['dataMin', 'dataMax']}
              tickFormatter={formatAxisDate}
              stroke="#70809f"
              tickLine={false}
              axisLine={false}
              minTickGap={30}
            />

            <YAxis
              allowDecimals={false}
              stroke="#70809f"
              tickLine={false}
              axisLine={false}
            />

            <Tooltip
              labelFormatter={(value) =>
                formatTooltipDate(Number(value))
              }
              formatter={(value) => [
                `${value} people`,
                'Occupancy',
              ]}
              contentStyle={{
                background: '#0f172a',
                border: '1px solid rgba(148, 163, 184, 0.22)',
                borderRadius: '12px',
                color: '#e8eefc',
              }}
              labelStyle={{
                color: '#aebbd6',
              }}
            />

            <Line
              type="stepAfter"
              dataKey="occupancy"
              stroke="#5eead4"
              strokeWidth={3}
              dot={{
                r: 4,
                fill: '#5eead4',
                strokeWidth: 0,
              }}
              activeDot={{
                r: 6,
              }}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="history-footer">
        <span>
          {new Date(history.start_at).toLocaleDateString()}
          {' → '}
          {new Date(history.end_at).toLocaleDateString()}
        </span>

        <span>
          {history.points.length} historical data points
        </span>
      </div>
    </article>
  )
}

export default OccupancyHistoryChart