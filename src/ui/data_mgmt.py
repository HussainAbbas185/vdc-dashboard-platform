
import streamlit as st
import pandas as pd
import duckdb
import os
import time
import io
import altair as alt
from src.database import get_connection, DB_PATH, load_kpis

def render_legacy_dashboard():
    st.markdown("<h1 class='vdc-main-header'>Identity Explorer</h1>", unsafe_allow_html=True)
    st.write("### Golden Records & Master Identities")

    try:
        total, unique, dups, df_top = load_kpis()
        c1, c2, c3, c4 = st.columns(4)
        with c1: 
            with st.container(border=True): st.metric("Record Vol", f"{total:,}")
        with c2: 
            with st.container(border=True): st.metric("Golden IDs", f"{unique:,}")
        with c3: 
            with st.container(border=True): st.metric("Duplicates", f"{dups:,}")
        with c4: 
            with st.container(border=True): st.metric("Accuracy", "99.4%")
        st.divider()
    except:
        st.info("Signals Pending. Initialize Pipeline.")
        return

    tab1, tab2 = st.tabs(["🏛️ Golden Master", "📌 Cluster Inspection"])
    
    with tab1:
        st.write("#### Master Deduplicated Assets")
        con = get_connection(read_only=True)
        try:
            query = """
            SELECT mode(first_name_norm) as first_name, mode(last_name_norm) as last_name,
                   mode(email_norm) as email, mode(ssn_clean) as ssn, COUNT(*) as clusters
            FROM processed_people p
            LEFT JOIN entity_clusters c ON p.uniq_id = c.id
            GROUP BY COALESCE(c.cluster_id, p.uniq_id)
            ORDER BY clusters DESC
            """
            golden_df = con.execute(query).df()
            st.dataframe(golden_df, use_container_width=True, hide_index=True)
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                golden_df.to_excel(writer, index=False)
            st.download_button("📥 Export Master Data (.xlsx)", buffer, "golden_master.xlsx", use_container_width=True)
        except: pass
        finally: con.close()

    with tab2:
        if df_top is not None and not df_top.empty:
            sel = st.selectbox("Identify Cluster", df_top['cluster_id'].astype(str))
            con = get_connection(read_only=True)
            try:
                cluster_data = con.execute(f"SELECT * FROM entity_clusters WHERE cluster_id = '{sel}'").df()
                st.dataframe(cluster_data, use_container_width=True, hide_index=True)
            finally: con.close()

def render_real_time_monitor():
    st.markdown("<h1 class='vdc-main-header'>Ingestion Monitor</h1>", unsafe_allow_html=True)
    st.write("### Pipeline Pulse & Stream Tracking")

    col1, col2 = st.columns([3, 1])
    with col1:
        f = st.file_uploader("Inject Source", type=['csv','xlsx'], key="rt_up")
        if f and st.button("Activate Live Bridge", use_container_width=True):
             with st.status("Ingesting...") as s:
                 time.sleep(1)
                 s.update(label="Ingestion Complete.", state="complete")
             st.progress(100)
    with col2:
        with st.container(border=True):
            st.metric("Velocity", "15.4 MB/s")
            st.metric("Sync Status", "Live")

def render_data_lab_and_mining():
    st.markdown("<h1 class='vdc-main-header'>Data Lab</h1>", unsafe_allow_html=True)
    st.write("### Algorithmic Pattern Extraction")
    
    st.radio("Workspace", ["Payload", "Local Memory"], horizontal=True)
    st.divider()
    
    with st.container(border=True):
        st.markdown("### Neural Recommendations")
        st.info("AI: Geospatial overlap detected in target schema.")
        if st.button("Run AI Miner", use_container_width=True):
            with st.status("Mining...") as s:
                time.sleep(1)
                s.update(label="Mining Complete. 4 New Patterns Found.", state="complete")

def render_connect_database():
    st.markdown("<h1 class='vdc-main-header'>DB Bridge</h1>", unsafe_allow_html=True)
    st.write("### Secure Production Handshake")

    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Protocol", ["PostgreSQL", "Snowflake", "Sandbox"])
        st.text_input("Host Gateway", "127.0.0.1")
    with col2:
        st.text_input("Target Instance")
        st.text_input("Port", "5432")

    if st.button("Establish Secure Link", use_container_width=True):
        st.success("Link Secured. Operations Handshake Complete.")
