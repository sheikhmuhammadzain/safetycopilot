import { useMemo } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from "recharts";
import { useCachedGet } from "@/hooks/useCachedGet";

interface StackedBarCardProps {
  title: string;
  endpoint: string;
  params?: Record<string, any>;
  refreshKey?: number;
  height?: number;
}

// Color palette for different chart types
const CHART_COLORS: Record<string, string> = {
  // Severity levels
  "C0 - No Ill Effect": "#10b981",   // green
  "C1 - Minor": "#3b82f6",           // blue
  "C2 - Serious": "#f59e0b",         // amber
  "C3 - Severe": "#ef4444",          // red
  "C4 - Major": "#dc2626",           // dark red
  "C5 - Catastrophic": "#7f1d1d",    // very dark red
  
  // Injury types (for penalty chart)
  "Minor Injuries": "#60a5fa",       // light blue
  "Major Injuries": "#ef4444",       // red
  
  // Generic fallback colors
  "Minor": "#60a5fa",
  "Major": "#ef4444",
  "Severe": "#dc2626",
};

export function StackedBarCard({ 
  title, 
  endpoint, 
  params = {}, 
  refreshKey = 0,
  height = 500 
}: StackedBarCardProps) {
  // Use cached API call
  const { data: apiData, error: apiError, loading } = useCachedGet<{
    labels: string[];
    series: Array<{ name: string; data: number[] }>;
    legend?: string[];
    totals?: number[];
  }>(endpoint, params, undefined, refreshKey);

  // Transform API response to Recharts format
  const { data, legend } = useMemo(() => {
    if (!apiData || !apiData.labels || !apiData.series) {
      return { data: [], legend: [] };
    }

    // API format: { labels: [...], series: [{ name: "C0", data: [...] }, ...], legend: [...] }
    // Recharts format: [{ name: "Type1", C0: 5, C1: 10, ... }, ...]
    const transformedData = apiData.labels.map((label: string, index: number) => {
      const item: any = { name: label };
      
      // Add each severity level's count for this incident type
      apiData.series.forEach((series: any) => {
        item[series.name] = series.data[index] || 0;
      });
      
      // Add total if available
      if (apiData.totals && apiData.totals[index]) {
        item.total = apiData.totals[index];
      }
      
      return item;
    });

    const legendData = apiData.legend || apiData.series.map((s: any) => s.name);

    return { data: transformedData, legend: legendData };
  }, [apiData]);

  const error = apiError ? String(apiError) : null;

  // Custom tick component for truncated labels with hover
  const CustomTick = ({ x, y, payload }: any) => {
    const maxLength = 20; // Maximum characters to show
    const text = payload.value || "";
    const truncatedText = text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
    
    return (
      <g transform={`translate(${x},${y})`}>
        <title>{text}</title>
        <text
          x={0}
          y={0}
          dy={16}
          textAnchor="end"
          fill="#64748b"
          fontSize={11}
          transform="rotate(-45)"
          style={{ cursor: 'help' }}
        >
          {truncatedText}
        </text>
      </g>
    );
  };

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const total = payload.reduce((sum: number, entry: any) => sum + (entry.value || 0), 0);
      const isPenaltyChart = title.toLowerCase().includes('penalty');
      
      // Calculate penalties for injury penalty chart
      let minorPenalty = 0;
      let majorPenalty = 0;
      if (isPenaltyChart) {
        const minorEntry = payload.find((p: any) => p.name === 'Minor Injuries');
        const majorEntry = payload.find((p: any) => p.name === 'Major Injuries');
        minorPenalty = (minorEntry?.value || 0) * -3;
        majorPenalty = (majorEntry?.value || 0) * -10;
      }
      
      return (
        <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded shadow-lg min-w-[200px]">
          <p className="font-semibold mb-2 text-sm">{label}</p>
          <div className="space-y-1">
            {payload.map((entry: any, index: number) => (
              <div key={index} className="flex items-center justify-between gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <div 
                    className="w-3 h-3 rounded" 
                    style={{ backgroundColor: entry.color }}
                  />
                  <span className="text-xs">{entry.name}:</span>
                </div>
                <span className="font-medium text-xs">{entry.value}</span>
              </div>
            ))}
            <div className="border-t border-gray-200 dark:border-gray-700 mt-2 pt-2">
              <div className="flex justify-between font-semibold text-sm">
                <span>Total Injuries:</span>
                <span>{total}</span>
              </div>
              {isPenaltyChart && (
                <>
                  <div className="flex justify-between text-xs text-orange-600 dark:text-orange-400 mt-1">
                    <span>Minor Penalty:</span>
                    <span>{minorPenalty} pts</span>
                  </div>
                  <div className="flex justify-between text-xs text-red-600 dark:text-red-400">
                    <span>Major Penalty:</span>
                    <span>{majorPenalty} pts</span>
                  </div>
                  <div className="flex justify-between font-bold text-sm text-red-700 dark:text-red-300 mt-1 pt-1 border-t border-gray-200 dark:border-gray-700">
                    <span>Total Penalty:</span>
                    <span>{minorPenalty + majorPenalty} pts</span>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-semibold">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {loading && (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center h-64 text-destructive">
            <p>Error: {error}</p>
          </div>
        )}

        {!loading && !error && data.length === 0 && (
          <div className="flex items-center justify-center h-64 text-muted-foreground">
            <p>No data available</p>
          </div>
        )}

        {!loading && !error && data.length > 0 && (
          <ResponsiveContainer width="100%" height={height}>
            <BarChart
              data={data}
              margin={{ top: 20, right: 30, left: 20, bottom: 140 }}
            >
              <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
              <XAxis 
                dataKey="name" 
                height={130}
                interval={0}
                tick={<CustomTick />}
              />
              <YAxis 
                tick={{ fontSize: 12 }}
                className="text-gray-600 dark:text-gray-400"
                label={{ 
                  value: title.toLowerCase().includes('penalty') ? 'Injury Count' : 'Number of Incidents', 
                  angle: -90, 
                  position: 'insideLeft' 
                }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                wrapperStyle={{ paddingTop: "20px" }}
                iconType="rect"
              />
              
              {/* Stack bars for each severity level */}
              {legend.map((severityLevel: string) => (
                <Bar
                  key={severityLevel}
                  dataKey={severityLevel}
                  stackId="severity"
                  fill={CHART_COLORS[severityLevel] || "#6b7280"}
                  name={severityLevel}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  );
}
