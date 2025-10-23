import { SidebarTrigger } from "@/components/ui/sidebar";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { PlotlyCard } from "@/components/charts/PlotlyCard";
import { BarChart3, RefreshCw, Target, TrendingUp, AlertTriangle, Info, Calendar, FileText } from "lucide-react";
import { HeinrichBreakdownModal } from "@/components/modals/HeinrichBreakdownModal";
import { Button } from "@/components/ui/button";
import { useState, useEffect } from "react";
import { Badge } from "@/components/ui/badge";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Skeleton } from "@/components/ui/skeleton";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { 
  BarChart, Bar, LineChart, Line, 
  XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer,
  Area, AreaChart
} from "recharts";
import axios from "axios";
import { PyramidChart } from "@/components/charts/PyramidChart";
import { 
  useSafetyIndex, 
  useIncidentForecast, 
  useLeadingLagging, 
  useRiskTrend, 
  useHeinrichPyramid,
  useActualRiskScore,
  usePotentialRiskScore
} from "@/hooks/useAdvancedAnalytics";
import { useHseMetrics } from "@/hooks/useHseMetrics";
import { HseMetricsCard } from "@/components/analytics/HseMetricsCard";

// API Base URL from environment variable
const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

interface FilterState {
  startDate: string;
  endDate: string;
  location: string;
  department: string;
}

export default function Analytics() {
  const [dataset, setDataset] = useState<"incident" | "hazard">("incident");
  const [refreshKey, setRefreshKey] = useState<number>(0);
  const [heinrichBreakdownOpen, setHeinrichBreakdownOpen] = useState<boolean>(false);
  
  // Filter state
  const [filters, setFilters] = useState<FilterState>({
    startDate: "2024-01-01",
    endDate: "2024-12-31",
    location: "",
    department: "",
  });
  
  // Filter options from API
  const [filterOptions, setFilterOptions] = useState<any>(null);
  
  // Advanced analytics hooks with caching
  const { data: safetyIndex, isLoading: safetyLoading, isError: safetyError, error: safetyErrorMsg } = useSafetyIndex(filters, refreshKey);
  const { data: incidentForecast, isLoading: forecastLoading, isError: forecastError, error: forecastErrorMsg } = useIncidentForecast(filters, 4, refreshKey);
  const { data: leadingLagging, isLoading: leadingLoading, isError: leadingError, error: leadingErrorMsg } = useLeadingLagging(filters, refreshKey);
  const { data: riskTrend, isLoading: riskLoading, isError: riskError, error: riskErrorMsg } = useRiskTrend(filters, 3, refreshKey);
  const { data: heinrichData, isLoading: heinrichLoading, isError: heinrichError, error: heinrichErrorMsg } = useHeinrichPyramid(filters, refreshKey);
  const { data: hseMetrics, loading: hseLoading, error: hseError } = useHseMetrics();
  const { data: actualRiskData, isLoading: actualRiskLoading, isError: actualRiskError, error: actualRiskErrorMsg } = useActualRiskScore(refreshKey);
  const { data: potentialRiskData, isLoading: potentialRiskLoading, isError: potentialRiskError, error: potentialRiskErrorMsg } = usePotentialRiskScore(refreshKey);

  // Fetch filter options
  const fetchFilterOptions = async () => {
    try {
      const response = await axios.get(`${API_BASE}/filters/all-filters`);
      setFilterOptions(response.data);
      console.log("Filter options loaded:", response.data);
    } catch (error) {
      console.error("Error fetching filter options:", error);
    }
  };


  // Filter functions
  const handleFilterChange = (key: keyof FilterState, value: string) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const applyFilters = () => {
    console.log("Applying filters:", filters);
    setRefreshKey(Date.now());
  };

  const resetFilters = () => {
    setFilters({
      startDate: "2024-01-01",
      endDate: "2024-12-31",
      location: "",
      department: "",
    });
    // Trigger refresh after resetting filters
    setTimeout(() => setRefreshKey(Date.now()), 100);
  };

  useEffect(() => {
    fetchFilterOptions();
  }, []);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-40">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center space-x-4">
            <SidebarTrigger />
            <div className="flex items-center space-x-2">
              <BarChart3 className="h-6 w-6 text-primary" />
              <div>
                <h1 className="text-2xl font-bold text-foreground">Analytics</h1>
                <p className="text-sm text-muted-foreground">Interactive analytics powered by Safety Copilot</p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {/* <Button
              variant={dataset === "incident" ? "default" : "outline"}
              size="sm"
              onClick={() => setDataset("incident")}
            >
              Incidents
            </Button>
            <Button
              variant={dataset === "hazard" ? "default" : "outline"}
              size="sm"
              onClick={() => setDataset("hazard")}
            >
              Hazards
            </Button> */}
            <Button
              variant="outline"
              size="sm"
              className="ml-2"
              onClick={() => setRefreshKey(Date.now())}
              title="Refresh charts"
            >
              <RefreshCw className="h-4 w-4 mr-1" /> Refresh
            </Button>
          </div>
        </div>
      </header>

      {/* Filters */}
      <div className="p-6 pb-0">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Filters
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Start Date</label>
                <Input
                  type="date"
                  value={filters.startDate}
                  onChange={(e) => handleFilterChange("startDate", e.target.value)}
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">End Date</label>
                <Input
                  type="date"
                  value={filters.endDate}
                  onChange={(e) => handleFilterChange("endDate", e.target.value)}
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Location</label>
                <Select value={filters.location || "all"} onValueChange={(value) => handleFilterChange("location", value === "all" ? "" : value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="All Locations" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Locations</SelectItem>
                    {filterOptions?.locations?.map((loc: string) => (
                      <SelectItem key={loc} value={loc}>
                        {loc}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Department</label>
                <Select value={filters.department || "all"} onValueChange={(value) => handleFilterChange("department", value === "all" ? "" : value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="All Departments" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Departments</SelectItem>
                    {filterOptions?.departments?.map((dept: string) => (
                      <SelectItem key={dept} value={dept}>
                        {dept}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="flex items-end gap-2">
                <Button onClick={applyFilters} className="flex-1">
                  Apply
                </Button>
                <Button onClick={resetFilters} variant="outline">
                  Reset
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <main className="p-6 space-y-8">
        {/* Section 1: Audit/Inspection Tracking
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-foreground">Audit & Inspection Tracking</h2>
          <div className="grid grid-cols-1 gap-6">
            <PlotlyCard title="Audit/Inspection Tracker" endpoint="/analytics/audit-inspection-tracker" height={420} refreshKey={refreshKey} />
          </div>
        </div> */}


  {/* Heinrich's Pyramid */}
          {heinrichLoading ? (
            <Card>
              <CardHeader>
                <Skeleton className="h-6 w-64" />
                <Skeleton className="h-4 w-96 mt-2" />
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <Skeleton className="h-[300px] w-full" />
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <Skeleton className="h-20 w-full" />
                    <Skeleton className="h-20 w-full" />
                    <Skeleton className="h-20 w-full" />
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <Skeleton className="h-16 w-full" />
                    <Skeleton className="h-16 w-full" />
                    <Skeleton className="h-16 w-full" />
                    <Skeleton className="h-16 w-full" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : heinrichError ? (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 text-destructive">
                  <AlertTriangle className="h-5 w-5" />
                  <div>
                    <p className="font-semibold">Failed to load Heinrich's Pyramid</p>
                    <p className="text-sm text-muted-foreground">{(heinrichErrorMsg as any)?.message || String(heinrichErrorMsg)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : heinrichData && (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      <AlertTriangle className="h-5 w-5" />
                      Heinrich's Safety Pyramid
                    </CardTitle>
                    <CardDescription>
                      Complete dataset analysis - Industry standard ratios (1:10:30:600:3000)
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      onClick={() => setHeinrichBreakdownOpen(true)}
                      className="gap-2"
                    >
                      <FileText className="h-4 w-4" />
                      View Breakdown
                    </Button>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Button variant="ghost" size="icon" className="h-8 w-8">
                            <Info className="h-4 w-4" />
                          </Button>
                        </TooltipTrigger>
                      <TooltipContent className="max-w-sm">
                        <p className="font-semibold mb-2">Heinrich's Safety Pyramid (Customized for Our Model)</p>
                        <p className="text-sm mb-2">Shows the relationship between minor and major safety events, emphasizing proactive prevention.</p>
                        <p className="text-sm mb-2"><strong>5 Levels (Top to Bottom):</strong></p>
                        <ul className="text-xs space-y-1 mb-2">
                          <li>• <strong>Level 1:</strong> Fatalities (C4–C5 Injuries)</li>
                          <li>• <strong>Level 2:</strong> Serious Injuries (C3)</li>
                          <li>• <strong>Level 3:</strong> Minor Injuries (C1–C2)</li>
                          <li>• <strong>Level 4:</strong> Near Misses (C0 actual, C3–C5 worst case)</li>
                          <li>• <strong>Level 5:</strong> Unsafe Conditions/At-Risk Behaviors (hazards, observations)</li>
                        </ul>
                        <p className="text-xs text-muted-foreground">These tiers help focus on leading indicators to prevent severe outcomes.</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {/* Map API layers to PyramidChart shape and compute totals */}
                {(() => {
                  const apiLayers = Array.isArray(heinrichData.layers) ? heinrichData.layers : [];
                  const totalEvents = apiLayers.reduce((sum: number, l: any) => sum + (Number(l.count) || 0), 0);
                  const layersForChart = apiLayers.map((l: any) => ({
                    level: l.level,
                    label: l.label,
                    count: Number(l.count) || 0,
                    ratio: 0, // Not used by chart
                    color: l.color || "#7fbf7f",
                  }));

                  return (
                    <>
                      <PyramidChart layers={layersForChart} totalEvents={totalEvents} />

                      {/* Stats */}
                      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="p-4 bg-muted rounded-lg">
                          <span className="text-sm text-muted-foreground">Total Events</span>
                          <p className="text-2xl font-bold">{totalEvents}</p>
                        </div>
                        <div className="p-4 bg-muted rounded-lg">
                          <span className="text-sm text-muted-foreground">Data Coverage</span>
                          <p className="text-2xl font-bold">Whole Dataset</p>
                        </div>
                        <div className="p-4 bg-muted rounded-lg">
                          <span className="text-sm text-muted-foreground">Industry Standard</span>
                          <p className="text-sm font-medium mt-1">1:10:30:600:3000</p>
                        </div>
                      </div>

                      {/* Layer details */}
                      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
                        {apiLayers.map((l: any, idx: number) => (
                          <div key={idx} className="p-3 rounded border flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <div className="w-4 h-4 rounded" style={{ backgroundColor: l.color }}></div>
                              <div>
                                <p className="text-sm font-medium">{l.label}</p>
                                <p className="text-xs text-muted-foreground">Level {l.level}</p>
                              </div>
                            </div>
                            <div className="text-right">
                              <span className="text-lg font-bold">{l.count}</span>
                              <span className="text-xs text-muted-foreground block">{l.percent}%</span>
                            </div>
                          </div>
                        ))}
                      </div>

                      {/* HSE Metrics */}
                      {hseLoading ? (
                        <div className="mt-6 p-4 bg-muted rounded-lg">
                          <p className="text-sm text-muted-foreground">Loading HSE metrics...</p>
                        </div>
                      ) : hseError ? (
                        <div className="mt-6 p-4 bg-destructive/10 rounded-lg">
                          <p className="text-sm text-destructive">Failed to load HSE metrics: {hseError.message}</p>
                        </div>
                      ) : hseMetrics ? (
                        <HseMetricsCard data={hseMetrics} />
                      ) : null}
                    </>
                  );
                })()}
              </CardContent>
            </Card>
          )}


        {/* Section 2: Facility Heatmaps */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-foreground">Facility Risk Visualization</h2>
          <div className="grid grid-cols-1 gap-6">
            <PlotlyCard title="Facility Layout Heatmap" endpoint="/analytics/facility-layout-heatmap" height={600} refreshKey={refreshKey} />
          </div>
        </div>

        {/* Section 3: Advanced Analytics */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-foreground">Advanced Analytics</h2>
{/*           
          Safety Index
          {safetyLoading ? (
            <Card>
              <CardHeader>
                <Skeleton className="h-6 w-48" />
                <Skeleton className="h-4 w-64 mt-2" />
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-center mb-6">
                  <Skeleton className="w-48 h-48 rounded-full" />
                </div>
                <div className="space-y-2">
                  <Skeleton className="h-10 w-full" />
                  <Skeleton className="h-10 w-full" />
                  <Skeleton className="h-10 w-full" />
                </div>
              </CardContent>
            </Card>
          ) : safetyError ? (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 text-destructive">
                  <AlertTriangle className="h-5 w-5" />
                  <div>
                    <p className="font-semibold">Failed to load Safety Index</p>
                    <p className="text-sm text-muted-foreground">{(safetyErrorMsg as any)?.message || String(safetyErrorMsg)}</p>
          </div>
        </div>
              </CardContent>
            </Card>
          ) : safetyIndex && (
        <Card>
          <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
            <CardTitle className="flex items-center gap-2">
                      <Target className="h-5 w-5" />
                      Site Safety Index
            </CardTitle>
                    <CardDescription>Real-time safety health score (0-100)</CardDescription>
                  </div>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <Info className="h-4 w-4" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent className="max-w-sm">
                        <p className="font-semibold mb-2">Site Safety Index</p>
                        <p className="text-sm mb-2">A 0-100 score measuring overall safety health.</p>
                        <p className="text-sm font-mono bg-muted p-2 rounded">
                          Score = 100 - Deductions + Bonuses
                        </p>
                        <ul className="text-xs mt-2 space-y-1">
                          <li>• Serious injuries: -10 each</li>
                          <li>• Minor injuries: -3 each</li>
                          <li>• High-risk hazards: -2 each</li>
                          <li>• Days since last incident: +0.1/day</li>
                          <li>• Completed audits: +0.5 each</li>
                        </ul>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
          </CardHeader>
          <CardContent>
                <div className="flex items-center justify-center mb-6">
                  <div className="relative w-48 h-48">
                    <svg className="w-full h-full" viewBox="0 0 100 100">
                      <circle
                        cx="50"
                        cy="50"
                        r="40"
                        fill="none"
                        stroke="#e5e7eb"
                        strokeWidth="8"
                      />
                      <circle
                        cx="50"
                        cy="50"
                        r="40"
                        fill="none"
                        stroke={safetyIndex.color}
                        strokeWidth="8"
                        strokeDasharray={`${safetyIndex.score * 2.51} 251`}
                        strokeLinecap="round"
                        transform="rotate(-90 50 50)"
                      />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className="text-4xl font-bold">{safetyIndex.score}</span>
                      <span className="text-sm text-muted-foreground">{safetyIndex.rating}</span>
                    </div>
                  </div>
                </div>
                <div className="space-y-2">
                  {safetyIndex.breakdown?.map((item: any, idx: number) => (
                    <div key={idx} className="flex justify-between items-center p-2 bg-muted rounded">
                      <span className="text-sm">{item.factor}</span>
                      <Badge variant={item.impact > 0 ? "default" : "destructive"}>
                        {item.impact > 0 ? "+" : ""}{item.impact}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )} */}

          {/* Leading vs Lagging */}
          {leadingLoading ? (
            <Card>
              <CardHeader>
                <Skeleton className="h-6 w-64" />
                <Skeleton className="h-4 w-80 mt-2" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-[300px] w-full" />
                <div className="mt-4">
                  <Skeleton className="h-20 w-full" />
                </div>
              </CardContent>
            </Card>
          ) : leadingError ? (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 text-destructive">
                  <AlertTriangle className="h-5 w-5" />
                  <div>
                    <p className="font-semibold">Failed to load Leading vs Lagging Indicators</p>
                    <p className="text-sm text-muted-foreground">{(leadingErrorMsg as any)?.message || String(leadingErrorMsg)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : leadingLagging && (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Leading vs Lagging Indicators</CardTitle>
                    <CardDescription>Proactive vs Reactive Safety Measures</CardDescription>
                  </div>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <Info className="h-4 w-4" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent className="max-w-sm">
                        <p className="font-semibold mb-2">Leading vs Lagging Indicators</p>
                        <p className="text-sm mb-2">Compares proactive safety measures vs reactive outcomes.</p>
                        <p className="text-sm font-mono bg-muted p-2 rounded mb-2">
                          Ratio = Leading / Lagging
                        </p>
                        <p className="text-xs mb-2"><strong>Leading (Proactive):</strong></p>
                        <ul className="text-xs space-y-1 mb-2">
                          <li>• Hazards: Records with valid Incident Number</li>
                          <li>• Audits: Records with valid Audit Number</li>
                          <li>• Inspections: Records with valid Audit Number</li>
                          <li>• Near-miss: Actual=C0 & Worst Case≥C3</li>
                        </ul>
                        <p className="text-xs mb-2"><strong>Lagging (Reactive):</strong></p>
                        <ul className="text-xs space-y-1">
                          <li>• Injuries: Count of injury incidents</li>
                          <li>• Incidents: Total incidents with valid number</li>
                          <li>• Fatalities: Injuries with C4/C5 severity</li>
                          <li>• Serious Injuries: Injuries with C3 severity</li>
                        </ul>
                        <p className="text-xs mt-2 text-muted-foreground">Best practice: 5-10:1 ratio</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart
                    data={[
                      {
                        name: "Leading",
                        Hazards: leadingLagging.leading_indicators.Hazards,
                        Audits: leadingLagging.leading_indicators.Audits,
                        Inspections: leadingLagging.leading_indicators.Inspections,
                        "Near-miss": leadingLagging.leading_indicators["Near-miss"],
                      },
                      {
                        name: "Lagging",
                        Injuries: leadingLagging.lagging_indicators.Injuries,
                        Incidents: leadingLagging.lagging_indicators.Incidents,
                        Fatalities: leadingLagging.lagging_indicators.Fatalities,
                        "Serious Injuries": leadingLagging.lagging_indicators["Serious Injuries"],
                      },
                    ]}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Bar dataKey="Hazards" fill="#8bc34a" name="Hazards" />
                    <Bar dataKey="Audits" fill="#4caf50" name="Audits" />
                    <Bar dataKey="Inspections" fill="#66bb6a" name="Inspections" />
                    <Bar dataKey="Near-miss" fill="#81c784" name="Near-miss" />
                    <Bar dataKey="Injuries" fill="#ff9800" name="Injuries" />
                    <Bar dataKey="Incidents" fill="#f44336" name="Incidents" />
                    <Bar dataKey="Fatalities" fill="#b71c1c" name="Fatalities" />
                    <Bar dataKey="Serious Injuries" fill="#d32f2f" name="Serious Injuries" />
                  </BarChart>
                </ResponsiveContainer>
                <div className="mt-4 p-4 bg-muted rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold">Ratio:</span>
                    <Badge style={{ backgroundColor: leadingLagging.color }}>
                      {leadingLagging.ratio_text}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mt-2">
                    {leadingLagging.assessment}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {leadingLagging.recommendation}
                  </p>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Incident Forecast */}
          {/* {forecastLoading ? (
            <Card>
              <CardHeader>
                <Skeleton className="h-6 w-64" />
                <Skeleton className="h-4 w-96 mt-2" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-[400px] w-full" />
              </CardContent>
            </Card>
          ) : forecastError ? (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 text-destructive">
                  <AlertTriangle className="h-5 w-5" />
                  <div>
                    <p className="font-semibold">Failed to load Incident Forecast</p>
                    <p className="text-sm text-muted-foreground">{(forecastErrorMsg as any)?.message || String(forecastErrorMsg)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : incidentForecast && (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Incident Forecast (4 Months)
                    </CardTitle>
                    <CardDescription>Predictive analysis using moving average with trend adjustment</CardDescription>
                  </div>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <Info className="h-4 w-4" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent className="max-w-sm">
                        <p className="font-semibold mb-2">Incident Forecast</p>
                        <p className="text-sm mb-2">Predicts future incident counts based on historical trends.</p>
                        <p className="text-sm font-mono bg-muted p-2 rounded mb-2">
                          Forecast = Average(last 6 months) + Trend
                        </p>
                        <ul className="text-xs space-y-1">
                          <li>• Uses moving average method</li>
                          <li>• Analyzes last 6 months of data</li>
                          <li>• Calculates trend slope</li>
                          <li>• Projects 4 months ahead</li>
                          <li>• Shows confidence intervals (upper/lower bounds)</li>
                        </ul>
                        <p className="text-xs mt-2 text-muted-foreground">Helps anticipate safety resource needs</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart
                    data={[
                      ...incidentForecast.historical.map((d: any) => ({
                        month: d.month,
                        actual: d.count,
                        type: "Historical",
                      })),
                      ...incidentForecast.forecast.map((d: any) => ({
                        month: d.month,
                        predicted: d.predicted_count,
                        lower: d.confidence_lower,
                        upper: d.confidence_upper,
                        type: "Forecast",
                      })),
                    ]}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Line type="monotone" dataKey="actual" stroke="#2196f3" strokeWidth={2} name="Actual" />
                    <Line type="monotone" dataKey="predicted" stroke="#ff9800" strokeWidth={2} strokeDasharray="5 5" name="Predicted" />
                    <Line type="monotone" dataKey="lower" stroke="#e0e0e0" strokeWidth={1} name="Lower Bound" />
                    <Line type="monotone" dataKey="upper" stroke="#e0e0e0" strokeWidth={1} name="Upper Bound" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          )} */}

          {/* Risk Trend Projection */}
          {/* {riskLoading ? (
            <Card>
              <CardHeader>
                <Skeleton className="h-6 w-64" />
                <Skeleton className="h-4 w-80 mt-2" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-[300px] w-full" />
                <div className="mt-4">
                  <Skeleton className="h-16 w-full" />
                </div>
              </CardContent>
            </Card>
          ) : riskError ? (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 text-destructive">
                  <AlertTriangle className="h-5 w-5" />
                  <div>
                    <p className="font-semibold">Failed to load Risk Trend Projection</p>
                    <p className="text-sm text-muted-foreground">{(riskErrorMsg as any)?.message || String(riskErrorMsg)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : riskTrend && (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Risk Trend Projection</CardTitle>
                    <CardDescription>Average risk score trends and forecast</CardDescription>
                  </div>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <Info className="h-4 w-4" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent className="max-w-sm">
                        <p className="font-semibold mb-2">Risk Trend Projection</p>
                        <p className="text-sm mb-2">Shows historical average risk scores and predicts future trends.</p>
                        <p className="text-sm font-mono bg-muted p-2 rounded mb-2">
                          Avg Risk = Sum(Risk Scores) / Total Events
                        </p>
                        <ul className="text-xs space-y-1">
                          <li>• <strong>Risk score:</strong> Calculated from severity × likelihood (1-5 scale)</li>
                          <li>• <strong>Historical data:</strong> Past 6 months of actual risk scores</li>
                          <li>• <strong>Forecast:</strong> Next 3 months prediction based on trend</li>
                          <li>• <strong>Trend analysis:</strong> Shows if risks are increasing or decreasing</li>
                        </ul>
                        <p className="text-xs mt-2 text-muted-foreground">Lower scores indicate better risk management</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart
                    data={[
                      ...riskTrend.historical.map((d: any) => ({
                        month: d.month,
                        risk: d.avg_risk,
                        type: "Historical",
                      })),
                      ...riskTrend.forecast.map((d: any) => ({
                        month: d.month,
                        risk: d.predicted_avg_risk,
                        type: "Forecast",
                      })),
                    ]}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Area type="monotone" dataKey="risk" stroke={riskTrend.trend_color} fill={riskTrend.trend_color} fillOpacity={0.3} />
                  </AreaChart>
                </ResponsiveContainer>
                <div className="mt-4 p-4 bg-muted rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold">Trend:</span>
                    <Badge style={{ backgroundColor: riskTrend.trend_color }}>
                      {riskTrend.trend}
                    </Badge>
                  </div>
            </div>
          </CardContent>
        </Card>
          )} */}

        

          {/* Actual Risk Score */}
          {actualRiskLoading ? (
            <Card>
              <CardHeader>
                <Skeleton className="h-6 w-64" />
                <Skeleton className="h-4 w-80 mt-2" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-[400px] w-full" />
              </CardContent>
            </Card>
          ) : actualRiskError ? (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 text-destructive">
                  <AlertTriangle className="h-5 w-5" />
                  <div>
                    <p className="font-semibold">Failed to load Actual Risk Score</p>
                    <p className="text-sm text-muted-foreground">{(actualRiskErrorMsg as any)?.message || String(actualRiskErrorMsg)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : actualRiskData && actualRiskData.data && actualRiskData.data.length > 0 ? (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      <AlertTriangle className="h-5 w-5 text-orange-500" />
                      Actual Risk Assessment by Department
                    </CardTitle>
                    <CardDescription>
                      Risk scores based on actual injury consequences and frequency
                    </CardDescription>
                  </div>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <Info className="h-4 w-4" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent className="max-w-md">
                        <p className="font-semibold mb-2">Actual Risk Score - Proportion-Based Method</p>
                        <p className="text-sm mb-3">Calculates risk using department's proportional contribution to each severity level:</p>
                        
                        {/* Formula */}
                        <div className="mb-3">
                          <p className="text-xs font-semibold mb-1">Formula:</p>
                          <p className="text-sm font-mono bg-muted p-2 rounded">
                            Risk Score = Σ(Severity × Proportion)
                          </p>
                          <p className="text-xs mt-1 text-muted-foreground">
                            Where Proportion = (Dept Count for Severity) / (Total Count for that Severity)
                          </p>
                        </div>

                        {/* Severity Scores */}
                        <div className="mb-3">
                          <p className="text-xs font-semibold mb-1">Severity Scores:</p>
                          <div className="bg-muted p-2 rounded text-xs font-mono space-y-0.5">
                            <div className="flex justify-between">
                              <span>C0 - No Ill Effect:</span>
                              <span className="font-bold">1</span>
                            </div>
                            <div className="flex justify-between">
                              <span>C1 - Minor:</span>
                              <span className="font-bold">2</span>
                            </div>
                            <div className="flex justify-between">
                              <span>C2 - Serious:</span>
                              <span className="font-bold">3</span>
                            </div>
                            <div className="flex justify-between">
                              <span>C3 - Severe:</span>
                              <span className="font-bold">4</span>
                            </div>
                            <div className="flex justify-between">
                              <span>C4-C5 - Major/Catastrophic:</span>
                              <span className="font-bold">5</span>
                            </div>
                          </div>
                        </div>

                        {/* Details */}
                        <ul className="text-xs space-y-1 mb-2">
                          <li>• Filters: Incident Type = 'injury' only</li>
                          <li>• Weighted by department's share of each severity</li>
                          <li>• Accounts for both frequency AND severity distribution</li>
                          <li>• Normalized 0-1 scale for comparison</li>
                        </ul>
                        
                        <p className="text-xs mt-2 text-muted-foreground font-semibold">⚠️ Higher scores indicate departments dominating high-severity categories</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={Math.max(400, actualRiskData.data.length * 35)}>
                  <BarChart
                    data={actualRiskData.data.slice(0, 20)}
                    layout="vertical"
                    margin={{ top: 10, right: 80, left: 150, bottom: 10 }}
                    barCategoryGap="20%"
                  >
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                    <XAxis type="number" />
                    <YAxis 
                      dataKey="Department" 
                      type="category" 
                      width={140}
                      tick={{ fontSize: 12 }}
                    />
                    <RechartsTooltip 
                      content={({ payload }) => {
                        if (payload && payload.length > 0) {
                          const data = payload[0].payload;
                          return (
                            <div className="bg-background border border-border p-3 rounded shadow-lg">
                              <p className="font-semibold">{data.Department}</p>
                              <div className="mt-2 space-y-1 text-sm">
                                <p>Risk Score: <span className="font-bold text-orange-500">{data.Actual_Risk_Score?.toFixed(3)}</span></p>
                                <p>Normalized: <span className="font-bold">{(data.Normalized_Score * 100).toFixed(1)}%</span></p>
                                <p>Avg Proportion: <span className="font-bold">{data.Avg_Proportion?.toFixed(3)}</span></p>
                                <p>Incident Count: <span className="font-bold">{data.Incident_Count}</span></p>
                              </div>
                            </div>
                          );
                        }
                        return null;
                      }}
                    />
                    <Bar 
                      dataKey="Actual_Risk_Score" 
                      fill="#f97316" 
                      radius={[0, 8, 8, 0]}
                      label={{ 
                        position: 'right', 
                        fill: '#000',
                        fontSize: 13,
                        fontWeight: 'bold'
                      }}
                    />
                  </BarChart>
                </ResponsiveContainer>
                
                {/* Summary Stats */}
                <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-muted rounded-lg">
                    <span className="text-sm text-muted-foreground">Highest Risk</span>
                    <p className="text-xl font-bold mt-1">{actualRiskData.data[0]?.Department || 'N/A'}</p>
                    <p className="text-sm text-muted-foreground mt-1">
                      Score: {actualRiskData.data[0]?.Actual_Risk_Score?.toFixed(3) || 'N/A'}
                    </p>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <span className="text-sm text-muted-foreground">Departments Analyzed</span>
                    <p className="text-xl font-bold mt-1">{actualRiskData.data.length}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      Total: {actualRiskData.metadata?.total_incidents || 'N/A'} incidents
                    </p>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <span className="text-sm text-muted-foreground">Average Risk Score</span>
                    <p className="text-xl font-bold mt-1">
                      {(actualRiskData.data.reduce((sum: number, d: any) => sum + d.Actual_Risk_Score, 0) / actualRiskData.data.length).toFixed(3)}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : null}

          {/* Potential Risk Score */}
          {potentialRiskLoading ? (
            <Card>
              <CardHeader>
                <Skeleton className="h-6 w-64" />
                <Skeleton className="h-4 w-80 mt-2" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-[400px] w-full" />
              </CardContent>
            </Card>
          ) : potentialRiskError ? (
            <Card className="border-destructive">
              <CardContent className="pt-6">
                <div className="flex items-center gap-3 text-destructive">
                  <AlertTriangle className="h-5 w-5" />
                  <div>
                    <p className="font-semibold">Failed to load Potential Risk Score</p>
                    <p className="text-sm text-muted-foreground">{(potentialRiskErrorMsg as any)?.message || String(potentialRiskErrorMsg)}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : potentialRiskData && potentialRiskData.data && potentialRiskData.data.length > 0 ? (
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5 text-yellow-500" />
                      Potential Risk Assessment - Near-Miss Analysis
                    </CardTitle>
                    <CardDescription>
                      Incidents with Minor Actual (C0/C1) but Severe Worst-Case (C3-C5)
                    </CardDescription>
                  </div>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <Info className="h-4 w-4" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent className="max-w-md">
                        <p className="font-semibold mb-2">Potential Risk Score - Proportion-Based Near-Miss</p>
                        <p className="text-sm mb-3">Calculates risk using department's proportional contribution to worst-case severity:</p>
                        
                        {/* Formula */}
                        <div className="mb-3">
                          <p className="text-xs font-semibold mb-1">Formula:</p>
                          <p className="text-sm font-mono bg-muted p-2 rounded">
                            Risk Score = Σ(Worst_Severity × Proportion)
                          </p>
                          <p className="text-xs mt-1 text-muted-foreground">
                            Where Proportion = (Dept Count for Worst Severity) / (Total Count for that Worst Severity)
                          </p>
                        </div>

                        {/* Severity Penalties */}
                        <div className="mb-3">
                          <p className="text-xs font-semibold mb-1">Severity-Based Penalties:</p>
                          <div className="bg-muted p-2 rounded text-xs font-mono space-y-0.5">
                            <div className="flex justify-between">
                              <span>C0 - No Ill Effect:</span>
                              <span className="font-bold">1</span>
                            </div>
                            <div className="flex justify-between">
                              <span>C1 - Minor:</span>
                              <span className="font-bold">2</span>
                            </div>
                            <div className="flex justify-between">
                              <span>C2 - Serious:</span>
                              <span className="font-bold">3</span>
                            </div>
                            <div className="flex justify-between">
                              <span>C3 - Severe:</span>
                              <span className="font-bold">4</span>
                            </div>
                            <div className="flex justify-between">
                              <span>C4 - Major:</span>
                              <span className="font-bold">5</span>
                            </div>
                            <div className="flex justify-between">
                              <span>C5 - Catastrophic:</span>
                              <span className="font-bold">5</span>
                            </div>
                          </div>
                        </div>

                        {/* Details */}
                        <ul className="text-xs space-y-1 mb-2">
                          <li>• Filters: Actual ≤ C1, Worst-Case ≥ C3</li>
                          <li>• Shows what "could have happened"</li>
                          <li>• Accounts for both frequency AND severity distribution</li>
                          <li>• Normalized 0-1 scale for comparison</li>
                        </ul>
                        
                        <p className="text-xs mt-2 text-muted-foreground font-semibold">⚠️ High scores indicate departments that got "lucky" - require proactive intervention</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={Math.max(500, potentialRiskData.data.length * 30)}>
                  <BarChart
                    data={potentialRiskData.data.slice(0, 30)}
                    layout="vertical"
                    margin={{ top: 10, right: 80, left: 180, bottom: 10 }}
                    barCategoryGap="15%"
                  >
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                    <XAxis type="number" />
                    <YAxis 
                      dataKey="Department" 
                      type="category" 
                      width={170}
                      tick={{ fontSize: 12 }}
                    />
                    <RechartsTooltip 
                      content={({ payload }) => {
                        if (payload && payload.length > 0) {
                          const data = payload[0].payload;
                          return (
                            <div className="bg-background border border-border p-3 rounded shadow-lg">
                              <p className="font-semibold">{data.Department}</p>
                              <div className="mt-2 space-y-1 text-sm">
                                <p>Risk Score: <span className="font-bold text-yellow-500">{data.Potential_Risk_Score?.toFixed(3)}</span></p>
                                <p>Normalized: <span className="font-bold">{(data.Normalized_Potential_Score * 100).toFixed(1)}%</span></p>
                                <p>Avg Proportion: <span className="font-bold">{data.Avg_Proportion?.toFixed(3)}</span></p>
                                <p>Near-Miss Count: <span className="font-bold">{data.Near_Miss_Count}</span></p>
                              </div>
                              <p className="text-xs mt-2 text-muted-foreground">Near-misses that could have been serious</p>
                            </div>
                          );
                        }
                        return null;
                      }}
                    />
                    <Bar 
                      dataKey="Potential_Risk_Score" 
                      fill="#f59e0b" 
                      radius={[0, 8, 8, 0]}
                      label={{ 
                        position: 'right', 
                        fill: '#000',
                        fontSize: 13,
                        fontWeight: 'bold'
                      }}
                    />
                  </BarChart>
                </ResponsiveContainer>
                
                {/* Summary Stats */}
                <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-yellow-50 dark:bg-yellow-950/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
                    <span className="text-sm text-muted-foreground">Highest Potential Risk</span>
                    <p className="text-xl font-bold mt-1">{potentialRiskData.data[0]?.Department || 'N/A'}</p>
                    <p className="text-sm text-muted-foreground mt-1">
                      Score: {potentialRiskData.data[0]?.Potential_Risk_Score?.toFixed(3) || 'N/A'}
                    </p>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <span className="text-sm text-muted-foreground">Departments with Near-Misses</span>
                    <p className="text-xl font-bold mt-1">{potentialRiskData.data.length}</p>
                    <p className="text-xs text-muted-foreground mt-1">
                      Total: {potentialRiskData.metadata?.total_near_miss || 'N/A'} near-misses
                    </p>
                  </div>
                  <div className="p-4 bg-muted rounded-lg">
                    <span className="text-sm text-muted-foreground">Average Potential Risk</span>
                    <p className="text-xl font-bold mt-1">
                      {(potentialRiskData.data.reduce((sum: number, d: any) => sum + d.Potential_Risk_Score, 0) / potentialRiskData.data.length).toFixed(3)}
                    </p>
                  </div>
                </div>
                
                {/* Alert Banner */}
                <div className="mt-4 p-4 bg-yellow-50 dark:bg-yellow-950/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5" />
                    <div>
                      <p className="font-semibold text-yellow-900 dark:text-yellow-100">Proactive Safety Insight</p>
                      <p className="text-sm text-yellow-800 dark:text-yellow-200 mt-1">
                        These departments experienced incidents with minor actual consequences but severe potential outcomes. 
                        While no serious injuries occurred, these near-misses indicate systemic vulnerabilities requiring immediate 
                        corrective action to prevent future catastrophic events.
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : null}
        </div>

      </main>

      {/* Heinrich Breakdown Modal */}
      <HeinrichBreakdownModal 
        open={heinrichBreakdownOpen}
        onOpenChange={setHeinrichBreakdownOpen}
        filters={{
          startDate: filters.startDate,
          endDate: filters.endDate
        }}
      />
    </div>
  );
}
