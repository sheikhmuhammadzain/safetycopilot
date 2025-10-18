import { Activity, AlertTriangle, TrendingUp, Shield, Target } from 'lucide-react';
import { HseMetrics } from '@/hooks/useHseMetrics';

interface HseMetricsCardProps {
  data: HseMetrics;
}

export function HseMetricsCard({ data }: HseMetricsCardProps) {
  console.log('HseMetricsCard rendering with data:', data);
  const totalIncidents = Number((data as any)?.total_incidents ?? 0);
  const nearMissRatio = (data as any)?.near_miss_ratio ?? 'N/A';
  const recordables = Number((data as any)?.recordable_injuries_actual ?? 0);
  const unsafe = Number((data as any)?.unsafe_condition ?? 0);
  const fatalities = Number((data as any)?.fatality_actual ?? 0);
  const lostWorkday = Number((data as any)?.lost_workday_cases_actual ?? 0);
  const nearMisses = Number((data as any)?.near_misses_actual ?? 0);
  return (
    <div className="mt-6 space-y-4">
      <div className="flex items-center gap-2 mb-3">
        <Shield className="h-5 w-5 text-primary" />
        <h3 className="text-lg font-semibold">HSE Performance Metrics</h3>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Incidents */}
        <div className="p-4 rounded-lg border bg-card hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm text-muted-foreground mb-1">Total Incidents</p>
              <p className="text-3xl font-bold font-mono">{totalIncidents}</p>
            </div>
            <Activity className="h-5 w-5 text-blue-500 mt-1" />
          </div>
        </div>

        {/* Near-Miss Ratio */}
        <div className="p-4 rounded-lg border bg-card hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm text-muted-foreground mb-1">Near-Miss Ratio</p>
              <p className="text-3xl font-bold font-mono">{nearMissRatio}</p>
            </div>
            <TrendingUp className="h-5 w-5 text-amber-500 mt-1" />
          </div>
        </div>

        {/* Recordable Injuries */}
        <div className="p-4 rounded-lg border bg-card hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm text-muted-foreground mb-1">Recordable Injuries</p>
              <p className="text-3xl font-bold font-mono">{recordables}</p>
            </div>
            <AlertTriangle className="h-5 w-5 text-orange-500 mt-1" />
          </div>
        </div>

        {/* Unsafe Conditions */}
        <div className="p-4 rounded-lg border bg-card hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <p className="text-sm text-muted-foreground mb-1">Unsafe Conditions</p>
              <p className="text-3xl font-bold font-mono">{unsafe}</p>
            </div>
            <Target className="h-5 w-5 text-purple-500 mt-1" />
          </div>
        </div>
      </div>

      {/* Detailed Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="p-3 rounded-lg bg-muted">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Fatalities</span>
            <span className="text-lg font-bold text-red-600 font-mono">{fatalities}</span>
          </div>
        </div>
        <div className="p-3 rounded-lg bg-muted">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Lost Workday Cases</span>
            <span className="text-lg font-bold text-orange-600 font-mono">{lostWorkday}</span>
          </div>
        </div>
        <div className="p-3 rounded-lg bg-muted">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Near Misses</span>
            <span className="text-lg font-bold text-amber-600 font-mono">{nearMisses}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
