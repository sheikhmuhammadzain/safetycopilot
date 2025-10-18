import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface HseMetrics {
  total_incidents: number;
  near_miss_ratio: string;
  fatality_actual: number;
  lost_workday_cases_actual: number;
  recordable_injuries_actual: number;
  near_misses_actual: number;
  unsafe_condition: number;
}

export function useHseMetrics() {
  const [data, setData] = useState<HseMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        console.log('Fetching HSE metrics...');
        const response = await axios.get(`${API_BASE}/analytics/advanced/hse-metrics`);
        console.log('HSE metrics response:', response.data);
        setData(response.data);
        setError(null);
      } catch (err) {
        console.error('Error fetching HSE metrics:', err);
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { data, loading, error };
}
