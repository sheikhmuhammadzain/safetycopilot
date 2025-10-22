import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { getCache, makeKey, setCache } from "@/lib/cache";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const ADVANCED_ANALYTICS_TTL_MS = 1000 * 60 * 60 * 6; // 6 hours

interface FilterParams {
  startDate?: string;
  endDate?: string;
  location?: string;
  department?: string;
}

// Hook for Site Safety Index
export function useSafetyIndex(filters: FilterParams, refreshKey?: number) {
  return useQuery({
    queryKey: ["safety-index", filters, refreshKey ?? 0],
    queryFn: async () => {
      const key = makeKey("/analytics/advanced/site-safety-index", filters);
      if (!refreshKey) {
        const cached = getCache<any>(key);
        if (cached) return cached;
      }
      const params = new URLSearchParams();
      if (filters.startDate) params.append("start_date", filters.startDate);
      if (filters.endDate) params.append("end_date", filters.endDate);
      if (filters.location) params.append("location", filters.location);
      if (filters.department) params.append("department", filters.department);
      
      const response = await axios.get(`${API_BASE}/analytics/advanced/site-safety-index?${params}`);
      setCache(key, response.data, ADVANCED_ANALYTICS_TTL_MS);
      return response.data;
    },
    staleTime: Infinity,
    gcTime: Infinity,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchInterval: false,
  });
}

// Hook for Incident Forecast
export function useIncidentForecast(filters: FilterParams, monthsAhead: number = 4, refreshKey?: number) {
  return useQuery({
    queryKey: ["incident-forecast", filters, monthsAhead, refreshKey ?? 0],
    queryFn: async () => {
      const key = makeKey("/analytics/predictive/incident-forecast", { ...filters, months_ahead: monthsAhead });
      if (!refreshKey) {
        const cached = getCache<any>(key);
        if (cached) return cached;
      }
      const params = new URLSearchParams();
      if (filters.startDate) params.append("start_date", filters.startDate);
      if (filters.endDate) params.append("end_date", filters.endDate);
      if (filters.location) params.append("location", filters.location);
      if (filters.department) params.append("department", filters.department);
      params.append("months_ahead", String(monthsAhead));
      
      const response = await axios.get(`${API_BASE}/analytics/predictive/incident-forecast?${params}`);
      setCache(key, response.data, ADVANCED_ANALYTICS_TTL_MS);
      return response.data;
    },
    staleTime: Infinity,
    gcTime: Infinity,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchInterval: false,
  });
}

// Hook for Leading vs Lagging Indicators
// NOTE: This always uses the full dataset regardless of filters
export function useLeadingLagging(filters: FilterParams, refreshKey?: number) {
  return useQuery({
    queryKey: ["leading-lagging", refreshKey ?? 0], // Removed filters from cache key since data is always the same
    queryFn: async () => {
      const key = "/analytics/predictive/leading-vs-lagging";
      if (!refreshKey) {
        const cached = getCache<any>(key);
        if (cached) return cached;
      }
      
      // No filter parameters - always fetch full dataset
      const response = await axios.get(`${API_BASE}/analytics/predictive/leading-vs-lagging`);
      setCache(key, response.data, ADVANCED_ANALYTICS_TTL_MS);
      return response.data;
    },
    staleTime: Infinity,
    gcTime: Infinity,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchInterval: false,
  });
}

// Hook for Risk Trend Projection
export function useRiskTrend(filters: FilterParams, monthsAhead: number = 3, refreshKey?: number) {
  return useQuery({
    queryKey: ["risk-trend", filters, monthsAhead, refreshKey ?? 0],
    queryFn: async () => {
      const key = makeKey("/analytics/predictive/risk-trend-projection", { ...filters, months_ahead: monthsAhead });
      if (!refreshKey) {
        const cached = getCache<any>(key);
        if (cached) return cached;
      }
      const params = new URLSearchParams();
      if (filters.startDate) params.append("start_date", filters.startDate);
      if (filters.endDate) params.append("end_date", filters.endDate);
      if (filters.location) params.append("location", filters.location);
      if (filters.department) params.append("department", filters.department);
      params.append("months_ahead", String(monthsAhead));
      
      const response = await axios.get(`${API_BASE}/analytics/predictive/risk-trend-projection?${params}`);
      setCache(key, response.data, ADVANCED_ANALYTICS_TTL_MS);
      return response.data;
    },
    staleTime: Infinity,
    gcTime: Infinity,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchInterval: false,
  });
}

// Hook for Heinrich's Pyramid
export function useHeinrichPyramid(filters: FilterParams, refreshKey?: number) {
  return useQuery({
    queryKey: ["heinrich-pyramid", refreshKey ?? 0],
    queryFn: async () => {
      const key = makeKey("/analytics/advanced/heinrich-pyramid", {});
      if (!refreshKey) {
        const cached = getCache<any>(key);
        if (cached) return cached;
      }
      
      // API no longer accepts filters - returns whole dataset
      const response = await axios.get(`${API_BASE}/analytics/advanced/heinrich-pyramid`);
      
      // Transform new API format to match frontend expectations
      // New format: [{Heinrich_Level, Description, Color_Code, Count, Percent}]
      // Expected format: {layers: [{level, label, count, color, percent}]}
      const transformedData = {
        layers: response.data.map((layer: any) => ({
          level: layer.Heinrich_Level,
          label: layer.Description,
          count: layer.Count,
          color: layer.Color_Code,
          percent: layer.Percent,
          heinrich_expected: 0, // Not provided by new API
          anchor: null, // Not provided by new API
        })),
      };
      
      setCache(key, transformedData, ADVANCED_ANALYTICS_TTL_MS);
      return transformedData;
    },
    staleTime: Infinity,
    gcTime: Infinity,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchInterval: false,
  });
}

// Hook for Actual Risk Score
export function useActualRiskScore(refreshKey?: number) {
  return useQuery({
    queryKey: ["actual-risk-score", refreshKey ?? 0],
    queryFn: async () => {
      const key = makeKey("/analytics/advanced/actual-risk-score", {});
      if (!refreshKey) {
        const cached = getCache<any>(key);
        if (cached) return cached;
      }
      
      const response = await axios.get(`${API_BASE}/analytics/advanced/actual-risk-score`);
      setCache(key, response.data, ADVANCED_ANALYTICS_TTL_MS);
      return response.data;
    },
    staleTime: Infinity,
    gcTime: Infinity,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchInterval: false,
  });
}

// Hook for Potential Risk Score
export function usePotentialRiskScore(refreshKey?: number) {
  return useQuery({
    queryKey: ["potential-risk-score", refreshKey ?? 0],
    queryFn: async () => {
      const key = makeKey("/analytics/advanced/potential-risk-score", {});
      if (!refreshKey) {
        const cached = getCache<any>(key);
        if (cached) return cached;
      }
      
      const response = await axios.get(`${API_BASE}/analytics/advanced/potential-risk-score`);
      setCache(key, response.data, ADVANCED_ANALYTICS_TTL_MS);
      return response.data;
    },
    staleTime: Infinity,
    gcTime: Infinity,
    refetchOnWindowFocus: false,
    refetchOnReconnect: false,
    refetchInterval: false,
  });
}
