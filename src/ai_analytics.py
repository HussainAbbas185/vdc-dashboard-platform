"""
AI-Powered Analytics Engine
Automated pattern discovery, clustering, and predictive analytics
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')


def auto_analyze_dataset(df, max_samples=10000):
    """
    Automatically analyze a dataset and return insights
    
    Returns:
        dict: Contains insights, patterns, anomalies, and recommendations
    """
    insights = {
        'summary': {},
        'quality': {},
        'patterns': {},
        'anomalies': {},
        'recommendations': []
    }
    
    # Sample if too large
    if len(df) > max_samples:
        df_sample = df.sample(n=max_samples, random_state=42)
    else:
        df_sample = df.copy()
    
    # 1. BASIC SUMMARY
    insights['summary'] = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'duplicate_rows': df.duplicated().sum(),
        'columns': list(df.columns)
    }
    
    # 2. DATA QUALITY ANALYSIS
    quality = {}
    for col in df.columns:
        null_pct = (df[col].isnull().sum() / len(df)) * 100
        unique_count = df[col].nunique()
        unique_pct = (unique_count / len(df)) * 100
        
        quality[col] = {
            'null_percentage': round(null_pct, 2),
            'unique_values': unique_count,
            'unique_percentage': round(unique_pct, 2),
            'data_type': str(df[col].dtype)
        }
        
        # Quality recommendations
        if null_pct > 50:
            insights['recommendations'].append(f"⚠️ Column '{col}' has {null_pct:.1f}% missing values - consider dropping or imputing")
        if unique_pct > 95 and len(df) > 100:
            insights['recommendations'].append(f"🔑 Column '{col}' appears to be a unique identifier")
        if unique_count == 1:
            insights['recommendations'].append(f"❌ Column '{col}' has only one unique value - consider removing")
    
    insights['quality'] = quality
    
    # 3. PATTERN DISCOVERY (Numeric columns only)
    numeric_cols = df_sample.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 2:
        # Correlation analysis
        corr_matrix = df_sample[numeric_cols].corr()
        high_corr = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    high_corr.append({
                        'col1': corr_matrix.columns[i],
                        'col2': corr_matrix.columns[j],
                        'correlation': round(corr_val, 3)
                    })
        
        insights['patterns']['high_correlations'] = high_corr
        
        if high_corr:
            for item in high_corr[:3]:  # Top 3
                insights['recommendations'].append(
                    f"🔗 Strong correlation ({item['correlation']}) between '{item['col1']}' and '{item['col2']}'"
                )
    
    # 4. CLUSTERING ANALYSIS
    if len(numeric_cols) >= 2 and len(df_sample) >= 10:
        try:
            # Prepare data
            X = df_sample[numeric_cols].fillna(df_sample[numeric_cols].mean())
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Optimal clusters (elbow method simplified)
            optimal_k = min(5, len(df_sample) // 10)
            if optimal_k >= 2:
                kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
                clusters = kmeans.fit_predict(X_scaled)
                
                cluster_sizes = pd.Series(clusters).value_counts().to_dict()
                insights['patterns']['clusters'] = {
                    'optimal_k': optimal_k,
                    'cluster_sizes': cluster_sizes,
                    'cluster_labels': clusters.tolist()[:100]  # First 100 for preview
                }
                
                insights['recommendations'].append(
                    f"📊 Data naturally groups into {optimal_k} clusters - useful for segmentation"
                )
        except Exception as e:
            insights['patterns']['clusters'] = {'error': str(e)}
    
    # 5. ANOMALY DETECTION
    if len(numeric_cols) >= 1 and len(df_sample) >= 20:
        try:
            X = df_sample[numeric_cols].fillna(df_sample[numeric_cols].mean())
            
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomalies = iso_forest.fit_predict(X)
            
            anomaly_count = (anomalies == -1).sum()
            anomaly_pct = (anomaly_count / len(anomalies)) * 100
            
            insights['anomalies'] = {
                'count': int(anomaly_count),
                'percentage': round(anomaly_pct, 2),
                'indices': np.where(anomalies == -1)[0].tolist()[:50]  # First 50
            }
            
            if anomaly_pct > 5:
                insights['recommendations'].append(
                    f"🚨 {anomaly_pct:.1f}% of records are statistical outliers - investigate for data quality issues"
                )
        except Exception as e:
            insights['anomalies'] = {'error': str(e)}
    
    # 6. CATEGORICAL INSIGHTS
    categorical_cols = df_sample.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if categorical_cols:
        cat_insights = {}
        for col in categorical_cols[:5]:  # Top 5 categorical columns
            value_counts = df_sample[col].value_counts().head(10)
            cat_insights[col] = {
                'top_values': value_counts.to_dict(),
                'cardinality': df[col].nunique()
            }
            
            # High cardinality warning
            if df[col].nunique() > len(df) * 0.5:
                insights['recommendations'].append(
                    f"⚡ Column '{col}' has high cardinality - may need encoding for ML"
                )
        
        insights['patterns']['categorical'] = cat_insights
    
    return insights


def auto_profile_data(df):
    """
    Generate comprehensive data profile report
    """
    profile = {
        'overview': {},
        'statistics': {},
        'distributions': {}
    }
    
    # Overview
    profile['overview'] = {
        'rows': len(df),
        'columns': len(df.columns),
        'missing_cells': df.isnull().sum().sum(),
        'missing_percentage': round((df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2),
        'duplicate_rows': df.duplicated().sum(),
        'memory_mb': round(df.memory_usage(deep=True).sum() / 1024**2, 2)
    }
    
    # Column statistics
    stats = {}
    for col in df.columns:
        col_stats = {
            'dtype': str(df[col].dtype),
            'missing': int(df[col].isnull().sum()),
            'missing_pct': round((df[col].isnull().sum() / len(df)) * 100, 2),
            'unique': int(df[col].nunique())
        }
        
        if df[col].dtype in ['int64', 'float64']:
            col_stats.update({
                'mean': round(df[col].mean(), 2) if not df[col].isnull().all() else None,
                'median': round(df[col].median(), 2) if not df[col].isnull().all() else None,
                'std': round(df[col].std(), 2) if not df[col].isnull().all() else None,
                'min': round(df[col].min(), 2) if not df[col].isnull().all() else None,
                'max': round(df[col].max(), 2) if not df[col].isnull().all() else None
            })
        
        stats[col] = col_stats
    
    profile['statistics'] = stats
    
    return profile


def suggest_visualizations(df):
    """
    Suggest appropriate visualizations based on data types
    """
    suggestions = []
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Numeric visualizations
    if len(numeric_cols) >= 1:
        suggestions.append({
            'type': 'histogram',
            'columns': numeric_cols[:5],
            'description': 'Distribution of numeric values'
        })
    
    if len(numeric_cols) >= 2:
        suggestions.append({
            'type': 'scatter',
            'columns': numeric_cols[:2],
            'description': 'Relationship between two numeric variables'
        })
        
        suggestions.append({
            'type': 'correlation_heatmap',
            'columns': numeric_cols,
            'description': 'Correlation matrix heatmap'
        })
    
    # Categorical visualizations
    if len(categorical_cols) >= 1:
        suggestions.append({
            'type': 'bar',
            'columns': categorical_cols[:3],
            'description': 'Count of categorical values'
        })
    
    # Mixed visualizations
    if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
        suggestions.append({
            'type': 'box',
            'columns': [categorical_cols[0], numeric_cols[0]],
            'description': 'Distribution of numeric values by category'
        })
    
    return suggestions


def detect_data_issues(df):
    """
    Detect common data quality issues
    """
    issues = []
    
    for col in df.columns:
        # Missing values
        missing_pct = (df[col].isnull().sum() / len(df)) * 100
        if missing_pct > 0:
            severity = 'High' if missing_pct > 50 else 'Medium' if missing_pct > 20 else 'Low'
            issues.append({
                'column': col,
                'issue': 'Missing Values',
                'severity': severity,
                'details': f'{missing_pct:.1f}% missing',
                'suggestion': 'Impute with mean/median or drop column' if missing_pct > 50 else 'Impute missing values'
            })
        
        # Constant values
        if df[col].nunique() == 1:
            issues.append({
                'column': col,
                'issue': 'Constant Value',
                'severity': 'Medium',
                'details': 'All values are identical',
                'suggestion': 'Consider removing this column'
            })
        
        # High cardinality for categorical
        if df[col].dtype == 'object' and df[col].nunique() > len(df) * 0.9:
            issues.append({
                'column': col,
                'issue': 'High Cardinality',
                'severity': 'Low',
                'details': f'{df[col].nunique()} unique values',
                'suggestion': 'May be an identifier or needs encoding'
            })
    
    return issues
