"""
Advanced Visualization Studio
Interactive charts, custom dashboards, and business intelligence reports
"""

import altair as alt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_advanced_chart(df, chart_type, x_col=None, y_col=None, color_col=None, **kwargs):
    """
    Create advanced interactive charts using Plotly
    
    Args:
        df: DataFrame
        chart_type: Type of chart (scatter, line, bar, heatmap, etc.)
        x_col, y_col, color_col: Column names
    """
    
    if chart_type == 'scatter_3d' and len(df.select_dtypes(include=['number']).columns) >= 3:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        fig = px.scatter_3d(
            df, 
            x=numeric_cols[0], 
            y=numeric_cols[1], 
            z=numeric_cols[2],
            color=color_col if color_col else None,
            title='3D Scatter Plot'
        )
        return fig
    
    elif chart_type == 'correlation_heatmap':
        numeric_df = df.select_dtypes(include=['number'])
        corr = numeric_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmid=0
        ))
        fig.update_layout(title='Correlation Heatmap', height=600)
        return fig
    
    elif chart_type == 'box':
        fig = px.box(df, x=x_col, y=y_col, color=color_col, title=f'{y_col} Distribution by {x_col}')
        return fig
    
    elif chart_type == 'violin':
        fig = px.violin(df, x=x_col, y=y_col, color=color_col, box=True, title='Violin Plot')
        return fig
    
    elif chart_type == 'sunburst':
        # Requires hierarchical data
        if x_col and y_col:
            fig = px.sunburst(df, path=[x_col, y_col], title='Hierarchical Sunburst')
            return fig
    
    elif chart_type == 'treemap':
        if x_col and y_col:
            fig = px.treemap(df, path=[x_col], values=y_col, title='Treemap Visualization')
            return fig
    
    elif chart_type == 'density_heatmap':
        fig = px.density_heatmap(df, x=x_col, y=y_col, title='2D Density Heatmap')
        return fig
    
    elif chart_type == 'parallel_coordinates':
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()[:6]
        fig = px.parallel_coordinates(
            df, 
            dimensions=numeric_cols,
            color=color_col if color_col else numeric_cols[0],
            title='Parallel Coordinates Plot'
        )
        return fig
    
    elif chart_type == 'scatter_matrix':
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()[:5]
        fig = px.scatter_matrix(df, dimensions=numeric_cols, color=color_col, title='Scatter Matrix')
        return fig
    
    else:
        # Default to simple scatter
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title='Scatter Plot')
        return fig


def create_dashboard_kpi(value, label, delta=None, delta_color="normal"):
    """
    Create a KPI metric card
    """
    return {
        'value': value,
        'label': label,
        'delta': delta,
        'delta_color': delta_color
    }


def generate_executive_summary(df, insights):
    """
    Generate executive summary from data insights
    """
    summary = {
        'headline_metrics': [],
        'key_findings': [],
        'recommendations': []
    }
    
    # Headline metrics
    summary['headline_metrics'] = [
        {'label': 'Total Records', 'value': f"{len(df):,}"},
        {'label': 'Data Quality Score', 'value': f"{calculate_quality_score(df)}/100"},
        {'label': 'Columns Analyzed', 'value': len(df.columns)},
        {'label': 'Insights Generated', 'value': len(insights.get('recommendations', []))}
    ]
    
    # Key findings
    if 'patterns' in insights and 'clusters' in insights['patterns']:
        clusters = insights['patterns']['clusters']
        if 'optimal_k' in clusters:
            summary['key_findings'].append(
                f"Data segments into {clusters['optimal_k']} distinct groups"
            )
    
    if 'anomalies' in insights and 'percentage' in insights['anomalies']:
        anomaly_pct = insights['anomalies']['percentage']
        if anomaly_pct > 5:
            summary['key_findings'].append(
                f"{anomaly_pct:.1f}% of records are statistical outliers"
            )
    
    # Recommendations
    summary['recommendations'] = insights.get('recommendations', [])[:5]
    
    return summary


def calculate_quality_score(df):
    """
    Calculate overall data quality score (0-100)
    """
    score = 100
    
    # Deduct for missing values
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    score -= min(missing_pct, 30)
    
    # Deduct for duplicates
    dup_pct = (df.duplicated().sum() / len(df)) * 100
    score -= min(dup_pct, 20)
    
    # Deduct for constant columns
    constant_cols = sum(1 for col in df.columns if df[col].nunique() == 1)
    score -= (constant_cols / len(df.columns)) * 10
    
    return max(0, int(score))


def create_time_series_forecast(df, date_col, value_col, periods=30):
    """
    Simple time series forecasting visualization
    """
    # This is a placeholder - would use Prophet or similar in production
    df_sorted = df.sort_values(date_col)
    
    fig = px.line(df_sorted, x=date_col, y=value_col, title='Time Series Analysis')
    fig.update_layout(
        xaxis_title=date_col,
        yaxis_title=value_col,
        hovermode='x unified'
    )
    
    return fig


def create_comparison_chart(df, category_col, value_cols):
    """
    Create grouped bar chart for comparing multiple metrics
    """
    fig = go.Figure()
    
    for col in value_cols:
        fig.add_trace(go.Bar(
            name=col,
            x=df[category_col],
            y=df[col]
        ))
    
    fig.update_layout(
        title='Multi-Metric Comparison',
        barmode='group',
        xaxis_title=category_col,
        yaxis_title='Values'
    )
    
    return fig


def export_chart_html(fig, filename):
    """
    Export Plotly figure to standalone HTML
    """
    fig.write_html(filename)
    return filename


def create_gauge_chart(value, max_value, title):
    """
    Create a gauge/speedometer chart for KPIs
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, max_value]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, max_value*0.5], 'color': "lightgray"},
                {'range': [max_value*0.5, max_value*0.8], 'color': "gray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value*0.9
            }
        }
    ))
    
    return fig
