
import streamlit as st
import pandas as pd
import altair as alt
import datetime
import numpy as np
import time
from src.audit_logger import log_action, get_audit_trail

def apply_clean_theme(chart):
    """Standard Clean Light theme for Altair."""
    return chart.configure_axis(
        labelColor='#64748b',
        titleColor='#64748b',
        gridColor='#f1f5f9',
        domainColor='#e2e8f0',
        labelFont="Inter",
        titleFont="Inter",
        titleFontWeight=600
    ).configure_view(
        stroke=None
    ).configure_title(
        color='#0f172a',
        fontSize=18,
        font="Inter",
        anchor='start'
    ).configure_legend(
        labelColor='#64748b',
        titleColor='#0f172a'
    )

def render_executive_intelligence_hub():
    st.markdown("<h1 class='vdc-main-header'>Strategic Executive Deck</h1>", unsafe_allow_html=True)
    st.write("### C-Suite Performance & Operational Intelligence")

    # 1. High-Level KPI Matrix
    k1, k2, k3, k4 = st.columns(4)
    with k1: 
        st.metric("Annual Revenue Run Rate", "$42.5M", "+12.4%")
    with k2: 
        st.metric("Operational Efficiency", "94.2%", "+1.8%")
    with k3: 
        st.metric("Active Enterprise Clients", "842", "+45")
    with k4: 
        st.metric("AI Agent ROI", "315%", "+12%")
        
    st.divider()

    # 2. Financial Velocity
    col_fin, col_ops = st.columns([2, 1])
    
    with col_fin:
        st.subheader("Financial Velocity")
        # Revenue Simulation
        months = pd.date_range(end=datetime.datetime.today(), periods=12, freq='M')
        rev_data = pd.DataFrame({
            'Month': months,
            'Revenue': np.linspace(2.5, 4.2, 12) + np.random.normal(0, 0.1, 12),
            'Target': np.linspace(2.8, 4.5, 12)
        }).melt('Month', var_name='Metric', value_name='Amount ($M)')
        
        chart_rev = alt.Chart(rev_data).mark_line(point=True).encode(
            x='Month',
            y='Amount ($M)',
            color=alt.Color('Metric', scale=alt.Scale(range=['#2563eb', '#94a3b8'])),
            tooltip=['Month', 'Metric', 'Amount ($M)']
        ).properties(height=300)
        
        st.altair_chart(apply_clean_theme(chart_rev), use_container_width=True)
        
    with col_ops:
        st.subheader("Compute Allocation")
        # Resource Donut
        alloc_data = pd.DataFrame({
            'Sector': ['R&D', 'Operations', 'Marketing', 'Security'],
            'Budget': [35, 40, 15, 10]
        })
        
        chart_donut = alt.Chart(alloc_data).mark_arc(innerRadius=60).encode(
            theta='Budget',
            color=alt.Color('Sector', scale=alt.Scale(scheme='blues')),
            tooltip=['Sector', 'Budget']
        ).properties(height=300)
        
        st.altair_chart(apply_clean_theme(chart_donut), use_container_width=True)

    st.divider()

    # 3. Strategic Objectives
    
    # 3. Strategic Objectives
    st.subheader("Strategic OKR Tracking")
    
    okr1, okr2 = st.columns(2)
    with okr1:
        with st.container(border=True):
            st.write("**Objective: Market Expansion**")
            st.progress(0.78)
            st.caption("Key Result: Launch in APAC Region (78% Complete)")
            
    with okr2:
         with st.container(border=True):
            st.write("**Objective: Infrastructure Autonomy**")
            st.progress(0.45)
            st.caption("Key Result: Achieve Level 4 Automation (45% Complete)")
    
    st.divider()

    # 4. System Analytics (Fixed & Upgraded)
    
    # Fetch and prepare data
    logs = get_audit_trail()
    if logs:
        df_logs = pd.DataFrame(logs)
        # Ensure timestamp is datetime
        df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])
    else:
        # Fallback for new systems (prevents crash)
        dates = pd.date_range(end=datetime.datetime.now(), periods=10, freq='H')
        df_logs = pd.DataFrame({
            'timestamp': dates,
            'category': ['System', 'Network', 'Security', 'System', 'User'] * 2,
            'action': ['Check'] * 10
        })

    c1, c2 = st.columns([2, 1])
    with c1:
        st.write("#### Throughput Trends")
        if not df_logs.empty:
            # Standard Blue Line with Gradient Area
            chart = alt.Chart(df_logs).mark_area(
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='rgba(37, 99, 235, 0.4)', offset=0),
                           alt.GradientStop(color='rgba(37, 99, 235, 0.0)', offset=1)],
                    x1=1, x2=1, y1=1, y2=0
                ),
                line={'color': '#2563eb', 'strokeWidth': 2}
            ).encode(
                x=alt.X('timestamp:T', title=None, axis=alt.Axis(format='%H:%M')),
                y=alt.Y('count():Q', title=None),
                tooltip=['timestamp', 'count()']
            ).properties(height=300)
            st.altair_chart(apply_clean_theme(chart), use_container_width=True)
        else:
            st.info("No Traffic Data Available")

    with c2:
        st.write("#### Load Sectors")
        if not df_logs.empty:
            dist = alt.Chart(df_logs).mark_arc(innerRadius=60).encode(
                theta='count()', 
                color=alt.Color('category:N', scale=alt.Scale(scheme='blues'), legend=alt.Legend(orient='bottom')),
                tooltip=['category', 'count()']
            ).properties(height=300)
            st.altair_chart(apply_clean_theme(dist), use_container_width=True)
        else:
            st.info("No Categorical Data")

def render_venture_intelligence():
    st.markdown("<h1 class='vdc-main-header'>Venture Intel</h1>", unsafe_allow_html=True)
    st.write("### High-Growth Asset Monitor")

    try:
        from src.startup_data import get_high_growth_startups
        df = get_high_growth_startups()
        
        v1, v2, v3 = st.columns(3)
        v1.metric("Portfolio Vol", f"${df['equity'].sum()/1000:.2f}B")
        v2.metric("Talent Ratio", f"{df['skill_index'].mean():.2f}")
        v3.metric("Market Status", "Bullish")

        st.divider()
        st.write("#### Market Leaderboard")
        st.dataframe(
            df[['name', 'sector', 'equity', 'skill_index']].sort_values('equity', ascending=False),
            use_container_width=True,
            column_config={
                "name": "Firm",
                "sector": "Sector",
                "equity": st.column_config.NumberColumn("Value ($M)", format="$%dM"),
                "skill_index": st.column_config.ProgressColumn("Talent Index", min_value=0, max_value=1)
            },
            hide_index=True
        )

        st.divider()
        selected = st.selectbox("Identify Target", df['name'].tolist())
        firm = df[df['name'] == selected].iloc[0]
        
        with st.container(border=True):
            f1, f2 = st.columns(2)
            f1.write(f"### **{firm['name']}**")
            f1.write(f"HQ: **{firm['hq']}**")
            f1.write(f"Share Target: **${firm['share_value']}**")
            
            f2.write("**Neural Stack**")
            stack = ["Rust-CoRE", "PQC-Algo", "Web3"] if firm['skill_index'] > 0.9 else ["Python", "Postgres", "AWS"]
            for s in stack: st.code(s, language="text")
            
            if st.button("Download Intel Report", use_container_width=True):
                st.toast("Generating Report...")

    except Exception as e:
        st.error(f"Feed Disrupted: {e}")

def render_social_market_intelligence():
    st.markdown("<h1 class='vdc-main-header'>Social Dynamics</h1>", unsafe_allow_html=True)
    st.write("### Memetic Impact & Prediction")

    horizon = st.slider("Forecasting Horizon", 2025, 2060, 2030)
    st.divider()
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("#### Swarm Inception")
        swarm = st.selectbox("Memetic Logic", ["Logic-Bomb", "Sentiment Seeder", "Factual Anchor"])
        if st.button("Run Deployment", use_container_width=True):
            st.success("Swarm Broadcasting...")
        
        st.divider()
        st.metric("Stability Index", f"{98 - (horizon-2025)*2}%")
    
    with c2:
        st.write("#### Global Sentiment Neural Network")
        
        # Advanced Data Simulation
        dates = pd.date_range(end=datetime.datetime.today(), periods=100)
        data = pd.DataFrame({
            'Date': dates,
            'Positive': np.random.randn(100).cumsum() + 50,
            'Negative': np.random.randn(100).cumsum() + 20,
            'Neutral': np.random.randn(100).cumsum() + 30
        }).melt('Date', var_name='Sentiment', value_name='Score')

        # Multi-Layered Chart
        chart = alt.Chart(data).mark_line(interpolate='basis').encode(
            x='Date',
            y='Score',
            color=alt.Color('Sentiment', scale=alt.Scale(domain=['Positive', 'Negative', 'Neutral'], range=['#22c55e', '#ef4444', '#94a3b8'])),
            tooltip=['Date', 'Sentiment', 'Score']
        ).properties(height=350)
        
        st.altair_chart(apply_clean_theme(chart), use_container_width=True)
        
    st.divider()
    
    # New Virality Engine
    st.subheader("Virality Prediction Engine")
    vp1, vp2, vp3 = st.columns(3)
    
    with vp1:
        st.metric("R-Naught (R0)", "4.2", "+0.3")
    with vp2:
        st.metric("Saturation Point", "88%", "High")
    with vp3:
        st.metric("Decay Rate", "12h", "Slow")
        
    with st.expander("Advanced Virality Parameters"):
        st.slider("Network Density", 0.0, 1.0, 0.75)
        st.slider("Node Permeability", 0.0, 1.0, 0.45)
        st.multiselect("Target Demographics", ["Gen Z", "Millennials", "Gen X", "Boomers"], ["Gen Z", "Millennials"])
