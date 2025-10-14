import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from "recharts";
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

interface StackedBarCardProps {
  title: string;
  endpoint: string;
  params?: Record<string, any>;
  refreshKey?: number;
  height?: number;
}

// Color palette for severity levels
const SEVERITY_COLORS: Record<string, string> = {
  "C0 - No Ill Effect": "#10b981",   // green
  "C1 - Minor": "#3b82f6",           // blue
  "C2 - Serious": "#f59e0b",         // amber
  "C3 - Severe": "#ef4444",          // red
  "C4 - Major": "#dc2626",           // dark red
  "C5 - Catastrophic": "#7f1d1d",    // very dark red
};

export function StackedBarCard({ 
  title, 
  endpoint, 
  params = {}, 
  refreshKey = 0,
  height = 500 
}: StackedBarCardProps) {
  const [data, setData] = useState<any[]>([]);
  const [legend, setLegend] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // Build query params
        const queryParams = new URLSearchParams();
        Object.entries(params).forEach(([key, value]) => {
          if (value !== undefined && value !== null) {
            if (Array.isArray(value)) {
              value.forEach(v => queryParams.append(key, v));
            } else {
              queryParams.append(key, String(value));
            }
          }
        });

        const url = `${API_BASE}${endpoint}${queryParams.toString() ? `?${queryParams.toString()}` : ""}`;
        const response = await axios.get(url);
        
        // Transform API response to Recharts format
        // API format: { labels: [...], series: [{ name: "C0", data: [...] }, ...], legend: [...] }
        // Recharts format: [{ name: "Type1", C0: 5, C1: 10, ... }, ...]
        
        const apiData = response.data;
        
        if (!apiData.labels || !apiData.series) {
          setData([]);
          setLegend([]);
          return;
        }

        // Transform data
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

        setData(transformedData);
        setLegend(apiData.legend || apiData.series.map((s: any) => s.name));
        
      } catch (err: any) {
        console.error("Error fetching stacked bar data:", err);
        setError(err.message || "Failed to load data");
        setData([]);
        setLegend([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [endpoint, JSON.stringify(params), refreshKey]);

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const total = payload.reduce((sum: number, entry: any) => sum + (entry.value || 0), 0);
      
      return (
        <div className="bg-white dark:bg-gray-800 p-3 border border-gray-200 dark:border-gray-700 rounded shadow-lg">
          <p className="font-semibold mb-2">{label}</p>
          <div className="space-y-1">
            {payload.map((entry: any, index: number) => (
              <div key={index} className="flex items-center justify-between gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <div 
                    className="w-3 h-3 rounded" 
                    style={{ backgroundColor: entry.color }}
                  />
                  <span>{entry.name}:</span>
                </div>
                <span className="font-medium">{entry.value}</span>
              </div>
            ))}
            <div className="border-t border-gray-200 dark:border-gray-700 mt-2 pt-2">
              <div className="flex justify-between font-semibold text-sm">
                <span>Total:</span>
                <span>{total}</span>
              </div>
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
              margin={{ top: 20, right: 30, left: 20, bottom: 80 }}
            >
              <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
              <XAxis 
                dataKey="name" 
                angle={-45}
                textAnchor="end"
                height={100}
                interval={0}
                tick={{ fontSize: 12 }}
                className="text-gray-600 dark:text-gray-400"
              />
              <YAxis 
                tick={{ fontSize: 12 }}
                className="text-gray-600 dark:text-gray-400"
                label={{ value: 'Number of Incidents', angle: -90, position: 'insideLeft' }}
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
                  fill={SEVERITY_COLORS[severityLevel] || "#6b7280"}
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
