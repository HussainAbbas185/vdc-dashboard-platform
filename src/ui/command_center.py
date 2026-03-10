
import streamlit as st
import time
from src.market_intelligence import get_global_market_pulse

def render_command_center():
    """
    🌎 GLOBAL COMMAND CENTER
    Strategic hub for operational oversight.
    """
    st.markdown("<h1 class='vdc-main-header'>Global Command Center</h1>", unsafe_allow_html=True)
    st.write("### Operational Traffic & KPIs")
    
    try:
        metrics, df_trends = get_global_market_pulse()
        
        # 1. CORE KPIS
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            with st.container(border=True):
                st.metric("Ingestion", f"{metrics['global_internet_traffic_pb']} PB/s", "Stable")
        with col2:
            with st.container(border=True):
                st.metric("Neural Nodes", f"{metrics['active_ai_agents_b']} B", "Active")
        with col3:
            with st.container(border=True):
                st.metric("Load", f"{metrics['cloud_compute_usage_pct']}%", "-2%")
        with col4:
            with st.container(border=True):
                st.metric("Unit Cost", f"${metrics['crypto_market_cap_t']}", "Volatile")
        
        st.divider()
        
        # 2. TRENDS & SECURITY
        c1, c2 = st.columns([2, 1])
        with c1:
            st.write("#### Global Trend Matrix")
            st.dataframe(
                df_trends,
                use_container_width=True,
                column_config={
                    "topic": "Sector",
                    "growth": "Trend",
                    "sentiment": "AI Pulse",
                    "impact": st.column_config.ProgressColumn("Index", min_value=0, max_value=100)
                },
                hide_index=True
            )
        
        with c2:
            st.write("#### Security Status")
            level = metrics['cyber_threat_level']
            
            # Clean White/Status Color
            color_border = "#ef4444" if level == "High" else "#22c55e"
            color_bg = "#fef2f2" if level == "High" else "#f0fdf4"
            
            st.markdown(f"""
                <div style='border: 1px solid {color_border}; padding: 25px; background: {color_bg}; text-align: center; border-radius: 8px;'>
                    <span style='color: {color_border}; font-family: "Inter", sans-serif; font-weight: 700; font-size: 1.5rem;'>{level.upper()} ALERT</span><br>
                    <span style='color: #64748b; font-family: "Inter", sans-serif; font-size: 0.9rem;'>IDS PROTOCOL ACTIVE</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            if st.button("Trigger Security Scrub", use_container_width=True):
                with st.status("Hardening Fabric...") as status:
                    time.sleep(1)
                    status.update(label="Scrub Complete. Channels Secured.", state="complete")

    except Exception as e:
        st.error(f"Link Offline: {e}")
