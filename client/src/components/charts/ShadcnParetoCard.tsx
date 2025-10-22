import { useMemo, useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useCachedGet } from "@/hooks/useCachedGet";
import { ChartContainer, ChartTooltip, ChartTooltipContent, ChartLegend, ChartLegendContent } from "@/components/ui/chart";
import { ComposedChart, CartesianGrid, XAxis, YAxis, Tooltip, Legend, Bar, Line } from "recharts";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Badge } from "@/components/ui/badge";

type ParetoResponse = {
  labels: string[];
  bars: number[];
  cum_pct: number[]; // 0..100
  incident_type?: string;
  total_count?: number;
};

type IncidentTypeOption = {
  label: string;
  value: string;
  count: number;
};

export default function ShadcnParetoCard({
  title,
  endpoint,
  params,
  height = 260,
  refreshKey,
  showIncidentTypeFilter = false,
}: {
  title: string;
  endpoint: string;
  params?: Record<string, any>;
  height?: number;
  refreshKey?: number;
  showIncidentTypeFilter?: boolean;
}) {
  const [selectedIncidentType, setSelectedIncidentType] = useState<string>("All");
  
  // Fetch incident types for radio buttons (if enabled)
  const { data: incidentTypesData } = useCachedGet<{ incident_types: IncidentTypeOption[] }>(
    showIncidentTypeFilter ? `${endpoint}/incident-types` : "",
    params,
    undefined,
    refreshKey
  );
  
  // Build params with selected incident type
  const chartParams = useMemo(() => {
    if (!showIncidentTypeFilter || selectedIncidentType === "All") {
      return params;
    }
    return { ...params, incident_type: selectedIncidentType };
  }, [params, selectedIncidentType, showIncidentTypeFilter]);
  
  const { data, error, loading } = useCachedGet<ParetoResponse>(endpoint, chartParams, undefined, refreshKey);

  const rows = useMemo(() => {
    if (!data) return [] as any[];
    const labels = data.labels.map((s) => String(s || "").trim()).filter(Boolean);
    return labels.map((label, i) => ({
      label,
      Count: Number(data.bars[i]) || 0,
      "Cumulative %": Number(data.cum_pct[i]) || 0,
    }));
  }, [data]);

  const chartConfig = useMemo(() => ({
    Count: { label: "Count" },
    "Cumulative %": { label: "Cumulative %" },
  }), []);

  // Custom tick component for truncated labels with hover
  const CustomTick = ({ x, y, payload }: any) => {
    const maxLength = 25; // Maximum characters to show
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
          fontSize={10}
          transform="rotate(-45)"
          style={{ cursor: 'help' }}
        >
          {truncatedText}
        </text>
      </g>
    );
  };

  return (
    <Card className="w-full border border-slate-200 bg-white shadow-sm">
      <CardHeader>
        <div className="flex items-start justify-between">
          <CardTitle className="text-base font-semibold text-slate-900">{title}</CardTitle>
          {data?.total_count !== undefined && (
            <Badge variant="secondary" className="ml-2">
              {data.total_count} total
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent>
        {/* Incident Type Filter */}
        {showIncidentTypeFilter && incidentTypesData?.incident_types && (
          <div className="mb-4 p-3 bg-slate-50 rounded-lg border border-slate-200">
            <Label className="text-sm font-medium mb-2 block">Filter by Incident Type</Label>
            <RadioGroup value={selectedIncidentType} onValueChange={setSelectedIncidentType}>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                {incidentTypesData.incident_types.slice(0, 10).map((option) => (
                  <div key={option.value} className="flex items-center space-x-2">
                    <RadioGroupItem value={option.value} id={`type-${option.value}`} />
                    <Label 
                      htmlFor={`type-${option.value}`} 
                      className="text-sm cursor-pointer flex-1"
                    >
                      {option.label} <span className="text-muted-foreground">({option.count})</span>
                    </Label>
                  </div>
                ))}
              </div>
            </RadioGroup>
          </div>
        )}
        {loading && <div className="text-xs text-slate-500">Loading…</div>}
        {error && <div className="text-xs text-red-600">{error}</div>}
        {!loading && !error && rows.length > 0 && (
          <ChartContainer config={chartConfig} className="w-full" style={{ height }}>
            <ComposedChart data={rows} margin={{ top: 40, right: 30, bottom: 100, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="label" tick={<CustomTick />} tickLine={{ stroke: "#cbd5e1" }} axisLine={{ stroke: "#cbd5e1" }} interval={0} height={90} />
              <YAxis yAxisId="left" tick={{ fill: "#64748b", fontSize: 11 }} tickLine={{ stroke: "#cbd5e1" }} axisLine={{ stroke: "#cbd5e1" }} allowDecimals={false} />
              <YAxis yAxisId="right" orientation="right" tick={{ fill: "#64748b", fontSize: 11 }} tickFormatter={(v)=>`${v}%`} tickLine={{ stroke: "#cbd5e1" }} axisLine={{ stroke: "#cbd5e1" }} domain={[0, 100]} />
              <ChartTooltip content={<ChartTooltipContent />} />
              <ChartLegend content={<ChartLegendContent />} verticalAlign="top" height={36} />
              <Bar yAxisId="left" dataKey="Count" fill="hsl(201, 96%, 45%)" radius={[4,4,0,0]} />
              <Line yAxisId="right" type="monotone" dataKey="Cumulative %" stroke="hsl(38, 92%, 55%)" strokeWidth={2} dot={false} />
            </ComposedChart>
          </ChartContainer>
        )}
      </CardContent>
    </Card>
  );
}
