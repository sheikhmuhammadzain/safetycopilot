from __future__ import annotations

from typing import Optional

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def _to_days(series: pd.Series) -> pd.Series:
    try:
        if series is None:
            return series
        s = series
        if np.issubdtype(s.dtype, np.timedelta64):
            return s.dt.total_seconds() / 86400.0
        if np.issubdtype(s.dtype, np.datetime64):
            return pd.to_numeric(s, errors='coerce')
        return pd.to_numeric(s, errors='coerce')
    except Exception:
        return pd.to_numeric(series, errors='coerce')


def create_unified_hse_scorecard(incident_df, hazard_df, audit_df, inspection_df):
    fig = make_subplots(
        rows=1, cols=4,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}, {'type': 'indicator'}]],
        subplot_titles=['Incidents', 'Hazards', 'Audits Completed', 'Inspections'],
        horizontal_spacing=0.08,
    )
    inc_count = len(incident_df) if isinstance(incident_df, pd.DataFrame) else 0
    haz_count = len(hazard_df) if isinstance(hazard_df, pd.DataFrame) else 0
    audits_completed = 0
    if isinstance(audit_df, pd.DataFrame) and 'audit_status' in audit_df.columns:
        audits_completed = (audit_df['audit_status'].astype(str).str.lower() == 'closed').sum()
    insp_count = len(inspection_df) if isinstance(inspection_df, pd.DataFrame) else 0
    fig.add_trace(go.Indicator(mode="number", value=inc_count, number={'font': {'size': 48}, 'valueformat': ",d"}), row=1, col=1)
    fig.add_trace(go.Indicator(mode="number", value=haz_count, number={'font': {'size': 48}, 'valueformat': ",d"}), row=1, col=2)
    fig.add_trace(go.Indicator(mode="number", value=audits_completed, number={'font': {'size': 48}, 'valueformat': ",d"}), row=1, col=3)
    fig.add_trace(go.Indicator(mode="number", value=insp_count, number={'font': {'size': 48}, 'valueformat': ",d"}), row=1, col=4)
    fig.update_layout(title={"text": "Unified HSE Scorecard", "x": 0.01, "xanchor": "left"}, height=260, margin=dict(t=50, l=30, r=20, b=20), showlegend=False)
    return fig


def create_hse_performance_index(df: Optional[pd.DataFrame]):
    if df is None or len(df) == 0 or 'department' not in df.columns:
        return go.Figure()
    cp = df.copy()
    for c in ['severity_score', 'risk_score']:
        if c not in cp.columns:
            cp[c] = np.nan
        cp[c] = pd.to_numeric(cp[c], errors='coerce')
    if 'reporting_delay_days' not in cp.columns:
        cp['reporting_delay_days'] = np.nan
    cp['reporting_delay_days'] = _to_days(cp['reporting_delay_days'])
    if 'resolution_time_days' not in cp.columns:
        cp['resolution_time_days'] = np.nan
    cp['resolution_time_days'] = _to_days(cp['resolution_time_days'])
    for c in ['root_cause_is_missing', 'corrective_actions_is_missing']:
        if c not in cp.columns:
            cp[c] = np.nan
        cp[c] = pd.to_numeric(cp[c].astype(float), errors='coerce')
    dept_metrics = cp.groupby('department').agg({
        'severity_score': 'mean',
        'risk_score': 'mean',
        'reporting_delay_days': 'mean',
        'resolution_time_days': 'mean',
        'root_cause_is_missing': 'mean',
        'corrective_actions_is_missing': 'mean'
    }).fillna(0)
    sev = dept_metrics['severity_score'].clip(lower=0, upper=5)
    risk = dept_metrics['risk_score'].clip(lower=0, upper=5)
    rep = dept_metrics['reporting_delay_days'].clip(lower=0, upper=30)
    res = dept_metrics['resolution_time_days'].clip(lower=0, upper=60)
    rc_miss = dept_metrics['root_cause_is_missing'].clip(lower=0, upper=1)
    ca_miss = dept_metrics['corrective_actions_is_missing'].clip(lower=0, upper=1)
    idx = ((5 - sev)/5 * 0.25 + (5 - risk)/5 * 0.25 + (30 - rep)/30 * 0.2 + (60 - res)/60 * 0.2 + (1 - rc_miss) * 0.05 + (1 - ca_miss) * 0.05) * 100
    dept_metrics = dept_metrics.assign(hse_index=idx)
    fig = px.bar(dept_metrics.reset_index(), x='hse_index', y='department', orientation='h', color='hse_index', color_continuous_scale=['red', 'yellow', 'green'], title='HSE Performance Index by Department (0-100)')
    fig.update_layout(height=520, margin=dict(t=60, l=160, r=40, b=40), yaxis=dict(automargin=True))
    return fig


def create_psm_breakdown(incident_df: Optional[pd.DataFrame]):
    if incident_df is None:
        return go.Figure()
    psm_counts = incident_df['psm'].value_counts(dropna=True) if 'psm' in incident_df.columns else pd.Series(dtype=int)
    pse_counts = incident_df['pse_category'].value_counts(dropna=True) if 'pse_category' in incident_df.columns else pd.Series(dtype=int)
    fig = make_subplots(rows=1, cols=2, subplot_titles=['PSM Elements', 'PSE Categories'], specs=[[{'type': 'pie'}, {'type': 'bar'}]])
    if not psm_counts.empty:
        fig.add_trace(go.Pie(labels=psm_counts.index, values=psm_counts.values, hole=0.4), row=1, col=1)
    if not pse_counts.empty:
        fig.add_trace(go.Bar(x=pse_counts.values, y=pse_counts.index, orientation='h'), row=1, col=2)
    fig.update_layout(title='Process Safety Management Analysis')
    return fig


def create_data_quality_metrics(incident_df: Optional[pd.DataFrame]):
    if incident_df is None:
        return go.Figure()
    fig = make_subplots(rows=2, cols=3, subplot_titles=['Root Cause Missing', 'Corrective Actions Missing', 'Reporting Delays', 'Resolution Times by Status', '', ''])
    if 'department' in incident_df.columns and 'root_cause_is_missing' in incident_df.columns:
        missing_rc = incident_df.groupby('department')['root_cause_is_missing'].sum()
        fig.add_trace(go.Bar(x=missing_rc.index, y=missing_rc.values, name='Root Cause Missing'), row=1, col=1)
    if 'department' in incident_df.columns and 'corrective_actions_is_missing' in incident_df.columns:
        missing_ca = incident_df.groupby('department')['corrective_actions_is_missing'].sum()
        fig.add_trace(go.Bar(x=missing_ca.index, y=missing_ca.values, name='Actions Missing'), row=1, col=2)
    if 'reporting_delay_days' in incident_df.columns:
        fig.add_trace(go.Histogram(x=_to_days(incident_df['reporting_delay_days']), nbinsx=30, name='Reporting Delay'), row=1, col=3)
    if {'resolution_time_days', 'status'}.issubset(incident_df.columns):
        fig.add_trace(go.Box(y=_to_days(incident_df['resolution_time_days']), x=incident_df['status'], name='Resolution by Status'), row=2, col=1)
    fig.update_layout(title='Data Quality Metrics')
    return fig


def create_audit_inspection_tracker(audit_df: Optional[pd.DataFrame], inspection_df: Optional[pd.DataFrame]):
    fig = make_subplots(rows=2, cols=1, subplot_titles=['Audit Status Over Time', 'Inspection Status Over Time'])
    if isinstance(audit_df, pd.DataFrame) and {'start_date', 'audit_status'}.issubset(audit_df.columns):
        aud = audit_df.copy()
        aud['_m'] = pd.to_datetime(aud['start_date'], errors='coerce').dt.to_period('M')
        # First trace: total audits per month
        totals = aud.groupby(aud['_m']).size()
        fig.add_trace(go.Bar(x=totals.index.astype(str), y=totals.values, name='Audits Total'), row=1, col=1)
        # Additional per-status traces
        timeline = aud.groupby([aud['_m'], 'audit_status']).size().unstack(fill_value=0)
        for status in timeline.columns:
            fig.add_trace(go.Bar(x=timeline.index.astype(str), y=timeline[status], name=str(status)), row=1, col=1)
    if isinstance(inspection_df, pd.DataFrame) and {'start_date', 'audit_status'}.issubset(inspection_df.columns):
        ins = inspection_df.copy()
        ins['_m'] = pd.to_datetime(ins['start_date'], errors='coerce').dt.to_period('M')
        totals = ins.groupby(ins['_m']).size()
        fig.add_trace(go.Bar(x=totals.index.astype(str), y=totals.values, name='Inspections Total'), row=2, col=1)
        timeline = ins.groupby([ins['_m'], 'audit_status']).size().unstack(fill_value=0)
        for status in timeline.columns:
            fig.add_trace(go.Bar(x=timeline.index.astype(str), y=timeline[status], name=str(status)), row=2, col=1)
    fig.update_layout(barmode='stack', title='Audit & Inspection Compliance Tracking')
    return fig


def create_location_risk_treemap(df: Optional[pd.DataFrame]):
    if df is None or not {'location', 'sublocation'}.issubset(df.columns):
        return go.Figure()
    cp = df.copy()
    if 'incident_id' not in cp.columns:
        cp['incident_id'] = 1
    for c in ['severity_score', 'risk_score', 'estimated_cost_impact']:
        if c not in cp.columns:
            cp[c] = np.nan
    location_data = cp.groupby(['location', 'sublocation']).agg({'incident_id': 'count', 'severity_score': 'mean', 'risk_score': 'mean', 'estimated_cost_impact': 'sum'}).reset_index()
    location_data['size'] = location_data['incident_id']
    location_data['hover_text'] = (
        'Count: ' + location_data['incident_id'].astype(str) +
        '<br>Avg Severity: ' + location_data['severity_score'].round(2).astype(str) +
        '<br>Total Cost: ' + location_data['estimated_cost_impact'].round(0).astype(str)
    )
    fig = px.treemap(location_data, path=['location', 'sublocation'], values='size', color='risk_score', hover_data={'hover_text': True}, color_continuous_scale='RdYlGn_r', title='Location Risk Map (Size=Count, Color=Risk)')
    return fig


def create_violation_analysis(hazard_df: Optional[pd.DataFrame]):
    if hazard_df is None:
        return go.Figure()
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=['Violation Types', 'Consequences Distribution', 'Reporting Delays', 'Department Violations'],
        specs=[[{'type': 'xy'}, {'type': 'domain'}], [{'type': 'xy'}, {'type': 'xy'}]]
    )
    if 'violation_type_hazard_id' in hazard_df.columns:
        vc = hazard_df['violation_type_hazard_id'].value_counts()
        fig.add_trace(go.Bar(x=vc.values, y=vc.index, orientation='h', name='Violation Types'), row=1, col=1)
    if 'worst_case_consequence_potential_hazard_id' in hazard_df.columns:
        wc = hazard_df['worst_case_consequence_potential_hazard_id'].value_counts()
        fig.add_trace(go.Pie(labels=wc.index, values=wc.values, name='Consequences', hole=0.3), row=1, col=2)
    if 'reporting_delay_days' in hazard_df.columns:
        fig.add_trace(go.Histogram(x=_to_days(hazard_df['reporting_delay_days']), nbinsx=30, name='Reporting Delay'), row=2, col=1)
    if {'department', 'violation_type_hazard_id'}.issubset(hazard_df.columns):
        heat = hazard_df.pivot_table(index='department', columns='violation_type_hazard_id', values='violation_type_hazard_id', aggfunc='count').fillna(0)
        fig.add_trace(go.Heatmap(z=heat.to_numpy(), x=list(heat.columns.astype(str)), y=list(heat.index.astype(str)), colorscale='YlOrRd', name='Dept x Violation'), row=2, col=2)
    fig.update_layout(title='Hazard Violation Analysis')
    return fig


# ---------- Additional charts ported from streamlit.py ----------
def create_cost_prediction_analysis(df: Optional[pd.DataFrame]):
    if df is None or 'estimated_cost_impact' not in df.columns:
        return go.Figure()
    numeric_cols = [c for c in ['severity_score','risk_score','reporting_delay_days','resolution_time_days','estimated_manhours_impact'] if c in df.columns]
    sub = df[numeric_cols + ['estimated_cost_impact']].dropna() if numeric_cols else pd.DataFrame()
    fig = make_subplots(rows=2, cols=2, subplot_titles=['Cost Correlations','Cost vs Severity','Cost vs Risk','Cost by Category'])
    if not sub.empty and len(numeric_cols) > 0:
        corrs = sub.corr(numeric_only=True)['estimated_cost_impact'].drop('estimated_cost_impact', errors='ignore')
        if not corrs.empty:
            fig.add_trace(go.Bar(x=corrs.values, y=corrs.index, orientation='h', marker_color=corrs.values, marker_colorscale='RdBu'), row=1, col=1)
    if {'severity_score','estimated_cost_impact'}.issubset(df.columns):
        fig.add_trace(go.Scatter(x=df['severity_score'], y=df['estimated_cost_impact'], mode='markers', marker=dict(size=5)), row=1, col=2)
    if {'risk_score','estimated_cost_impact'}.issubset(df.columns):
        fig.add_trace(go.Scatter(x=df['risk_score'], y=df['estimated_cost_impact'], mode='markers', marker=dict(size=5)), row=2, col=1)
    if {'category','estimated_cost_impact'}.issubset(df.columns):
        fig.add_trace(go.Box(x=df['category'], y=df['estimated_cost_impact']), row=2, col=2)
    fig.update_layout(title='Cost Impact Analysis')
    return fig


# Facility zones used for facility layout heatmap
FACILITY_ZONES = {
    'Admin Building': {'x': 1, 'y': 5, 'area': 'Administration'},
    'EVCM 200': {'x': 2, 'y': 4, 'area': 'EDC/VCM'},
    'EVCM 300': {'x': 3, 'y': 4, 'area': 'EDC/VCM'},
    'PVC I Front End': {'x': 4, 'y': 3, 'area': 'PVC'},
    'PVC III Feedstock': {'x': 5, 'y': 3, 'area': 'PVC'},
    'HPO': {'x': 2, 'y': 2, 'area': 'HPO'},
    'HPO Process Area': {'x': 3, 'y': 2, 'area': 'HPO'},
    'HTDC': {'x': 4, 'y': 1, 'area': 'HTDC'},
    'CA-1650 and HCL Loading': {'x': 5, 'y': 1, 'area': 'Chlor Alkali'},
    'Container Offices': {'x': 1, 'y': 4, 'area': 'Administration'},
    'Manufacturing Facility': {'x': 3, 'y': 3, 'area': 'Main'},
    'Karachi': {'x': 3, 'y': 3, 'area': 'Main'},
}


def _zone_heatmap_data(df: pd.DataFrame, zones: dict, data_type: str):
    """
    Generate heatmap data for facility zones, ensuring each row is counted only once.
    Prioritizes location.1 (most specific) > sublocation > location for zone matching.
    """
    zone_counts = {zn: {'count': 0, 'x': info['x'], 'y': info['y'], 'area': info['area']} for zn, info in zones.items()}
    
    if df is None or df.empty:
        x, y, intensity, size, text, hover, labels = [], [], [], [], [], [], []
        for zone_name, data in zone_counts.items():
            x.append(data['x'])
            y.append(data['y'])
            intensity.append(0)
            size.append(30)
            text.append("")
            hover.append(f"{zone_name}<br>Area: {data['area']}<br>{data_type}: 0")
            labels.append(zone_name)
        return {'x': x, 'y': y, 'intensity': intensity, 'size': size, 'text': text, 'hover': hover, 'labels': labels}
    
    # Create a copy to avoid modifying original dataframe
    df_copy = df.copy()
    
    # Helper function to find column by multiple possible names (case-insensitive)
    def find_column(possible_names):
        """Find first matching column name from a list of possibilities"""
        for col in df_copy.columns:
            col_lower = str(col).lower().strip()
            for poss in possible_names:
                if poss.lower().strip() == col_lower:
                    return col
        return None
    
    # Find actual column names (handle different naming conventions)
    loc1_col = find_column(['Location (EPCL)', 'location.1', 'location (epcl)', 'specific location of occurrence', 'location tag'])
    subloc_col = find_column(['Sub-Location', 'sublocation', 'sub-location', 'sub location'])
    loc_col = find_column(['Location', 'location'])
    
    # Sort zone names by length (longest first) to prioritize specific matches
    # E.g., "HPO Process Area" should be checked before "HPO"
    sorted_zones = sorted(zones.keys(), key=len, reverse=True)
    
    # Assign each row to a zone (prioritize location.1 > sublocation > location)
    # Each row is counted only once
    for idx, row in df_copy.iterrows():
        matched_zone = None
        
        # Priority 1: Check specific location column (most specific)
        if loc1_col and pd.notna(row.get(loc1_col)):
            loc1 = str(row[loc1_col]).strip()
            if loc1 and loc1.lower() not in ['nan', 'none', '', 'not specified']:
                for zone_name in sorted_zones:
                    zone_lower = zone_name.lower()
                    loc_lower = loc1.lower()
                    # Bidirectional matching: zone in location OR location in zone
                    if zone_lower in loc_lower or loc_lower in zone_lower:
                        matched_zone = zone_name
                        break
        
        # Priority 2: Check sublocation if location.1 didn't match
        if matched_zone is None and subloc_col and pd.notna(row.get(subloc_col)):
            subloc = str(row[subloc_col]).strip()
            if subloc and subloc.lower() not in ['nan', 'none', '', 'not specified']:
                for zone_name in sorted_zones:
                    zone_lower = zone_name.lower()
                    subloc_lower = subloc.lower()
                    # Bidirectional matching: zone in location OR location in zone
                    if zone_lower in subloc_lower or subloc_lower in zone_lower:
                        matched_zone = zone_name
                        break
        
        # Priority 3: Check location if neither location.1 nor sublocation matched
        if matched_zone is None and loc_col and pd.notna(row.get(loc_col)):
            loc = str(row[loc_col]).strip()
            if loc and loc.lower() not in ['nan', 'none', '', 'not specified']:
                for zone_name in sorted_zones:
                    zone_lower = zone_name.lower()
                    loc_lower = loc.lower()
                    # Bidirectional matching: zone in location OR location in zone
                    if zone_lower in loc_lower or loc_lower in zone_lower:
                        matched_zone = zone_name
                        break
        
        # If a zone was matched, add to counts
        if matched_zone:
            zone_counts[matched_zone]['count'] += 1
    
    # Build the visualization data
    x, y, intensity, size, text, hover, labels = [], [], [], [], [], [], []
    for zone_name, data in zone_counts.items():
        x.append(data['x'])
        y.append(data['y'])
        intensity.append(data['count'])
        size.append(max(30, min(100, data['count'] * 8 + 20)))
        text.append(f"{data['count']}" if data['count'] > 0 else "")
        hover.append(f"{zone_name}<br>Area: {data['area']}<br>{data_type}: {data['count']}<br>Count: {data['count']}")
        labels.append(zone_name)
    return {'x': x, 'y': y, 'intensity': intensity, 'size': size, 'text': text, 'hover': hover, 'labels': labels}


def create_facility_layout_heatmap(incident_df: Optional[pd.DataFrame], hazard_df: Optional[pd.DataFrame]):
    inc = incident_df.copy() if isinstance(incident_df, pd.DataFrame) else pd.DataFrame()
    haz = hazard_df.copy() if isinstance(hazard_df, pd.DataFrame) else pd.DataFrame()
    incident_heatmap = _zone_heatmap_data(inc, FACILITY_ZONES, 'Incidents')
    hazard_heatmap = _zone_heatmap_data(haz, FACILITY_ZONES, 'Hazards')
    fig = make_subplots(rows=1, cols=2, subplot_titles=('🔴 Incident Heat Map', '⚠️ Hazard Heat Map'), specs=[[{'type': 'scatter'}, {'type': 'scatter'}]], horizontal_spacing=0.15)
    
    # Incident heatmap - Add bubbles without text first
    fig.add_trace(go.Scatter(
        x=incident_heatmap['x'], 
        y=incident_heatmap['y'], 
        mode='markers',
        marker=dict(
            size=incident_heatmap['size'], 
            color=incident_heatmap['intensity'], 
            colorscale='Reds', 
            showscale=True, 
            colorbar=dict(x=0.45, title='Incidents', len=0.8), 
            line=dict(width=2, color='darkred'), 
            sizemode='diameter', 
            sizeref=2, 
            sizemin=20
        ),
        hovertemplate='<b>%{hovertext}</b><extra></extra>', 
        hovertext=incident_heatmap['hover'], 
        showlegend=False
    ), row=1, col=1)
    
    # Add count text with adaptive colors based on intensity (incidents)
    inc_vals = incident_heatmap['intensity']
    inc_max = max(inc_vals) if inc_vals else 1
    inc_thr = inc_max * 0.4  # Threshold for text color switching
    
    for i, (x, y, count, intensity) in enumerate(zip(incident_heatmap['x'], incident_heatmap['y'], incident_heatmap['text'], inc_vals)):
        if count:  # Only add text if count > 0
            text_color = 'white' if intensity > inc_thr else '#1f2937'
            fig.add_trace(go.Scatter(
                x=[x], y=[y], 
                mode='text',
                text=[count],
                textposition='middle center',
                textfont=dict(size=13, family='Arial Black', color=text_color),
                hoverinfo='skip',
                showlegend=False
            ), row=1, col=1)
    
    # Hazard heatmap - Add bubbles without text first
    fig.add_trace(go.Scatter(
        x=hazard_heatmap['x'], 
        y=hazard_heatmap['y'], 
        mode='markers',
        marker=dict(
            size=hazard_heatmap['size'], 
            color=hazard_heatmap['intensity'], 
            colorscale='YlOrRd', 
            showscale=True, 
            colorbar=dict(x=1.0, title='Hazards', len=0.8), 
            line=dict(width=2, color='darkorange'), 
            sizemode='diameter', 
            sizeref=2, 
            sizemin=20
        ),
        hovertemplate='<b>%{hovertext}</b><extra></extra>', 
        hovertext=hazard_heatmap['hover'], 
        showlegend=False
    ), row=1, col=2)
    
    # Add count text with adaptive colors based on intensity (hazards)
    haz_vals = hazard_heatmap['intensity']
    haz_max = max(haz_vals) if haz_vals else 1
    haz_thr = haz_max * 0.4  # Threshold for text color switching
    
    for i, (x, y, count, intensity) in enumerate(zip(hazard_heatmap['x'], hazard_heatmap['y'], hazard_heatmap['text'], haz_vals)):
        if count:  # Only add text if count > 0
            text_color = 'white' if intensity > haz_thr else '#1f2937'
            fig.add_trace(go.Scatter(
                x=[x], y=[y], 
                mode='text',
                text=[count],
                textposition='middle center',
                textfont=dict(size=13, family='Arial Black', color=text_color),
                hoverinfo='skip',
                showlegend=False
            ), row=1, col=2)
    for c in (1, 2):
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray', zeroline=False, showticklabels=False, range=[0, 6], title='', row=1, col=c)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray', zeroline=False, showticklabels=False, range=[0, 6], title='', row=1, col=c)
    fig.update_layout(height=500, title_text="🏭 Facility Risk Heat Map - Real-time HSE Status", title_font_size=16, showlegend=False, plot_bgcolor='#f8f9fa', paper_bgcolor='white', margin=dict(t=60, l=40, r=40, b=40))
    return fig


def create_3d_facility_heatmap(df: Optional[pd.DataFrame], event_type: str = 'Incidents'):
    if df is None or df.empty:
        return go.Figure()
    x = np.linspace(0, 10, 50)
    y = np.linspace(0, 10, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    zone_centers = {'EVCM': (3, 7), 'PVC': (7, 7), 'HPO': (3, 3), 'HTDC': (7, 3), 'Admin': (1, 8), 'Default': (5, 5)}
    for _, row in df.iterrows():
        loc = str(row.get('location.1', row.get('sublocation', '')))
        cx, cy = zone_centers['Default']
        for zone_key, coords in zone_centers.items():
            if zone_key.lower() in loc.lower():
                cx, cy = coords
                break
        severity = row.get('severity_score', row.get('risk_score', 1))
        if pd.notna(severity):
            Z += float(severity) * np.exp(-((X - cx)**2 + (Y - cy)**2) / 2)
    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Hot', name=event_type, showscale=True, colorbar=dict(title=f"{event_type} Intensity"), contours=dict(z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project=dict(z=True))))])
    fig.update_layout(title=f'3D {event_type} Heat Map - Facility Risk Visualization', scene=dict(xaxis_title='Facility Width', yaxis_title='Facility Length', zaxis_title='Risk Intensity', camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))), height=600, margin=dict(t=40, l=20, r=20, b=20))
    return fig

