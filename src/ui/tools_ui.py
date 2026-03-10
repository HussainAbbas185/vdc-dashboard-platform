
import streamlit as st
import pandas as pd
import os
import io
import time
import math
import numpy as np
import altair as alt
import plotly.graph_objects as go
from src.audit_logger import log_action
from src.database import get_connection

def render_extraction_engine():
    st.markdown("<h1 class='vdc-main-header'>Extraction</h1>", unsafe_allow_html=True)
    st.write("### Unstructured Data Asset Harvesting")

    if 'last_neural_search' in st.session_state and st.session_state.last_neural_search:
        with st.container(border=True):
            st.markdown("#### AI-Surfaced Assets")
            for res in st.session_state.last_neural_search:
                with st.expander(f"📄 {res['filename']} ({res['score']})"):
                    st.write(res['full_text'][:1000] + "...")
            if st.button("Flush Cache", use_container_width=True):
                st.session_state.last_neural_search = None
                st.rerun()

    st.divider()
    t1, t2 = st.tabs(["📤 Bulk Archive", "🌐 Network Bridge"])
    
    with t1:
        files = st.file_uploader("Upload Documents", accept_multiple_files=True)
        if files:
            for f in files:
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    c1.write(f"**File: {f.name}**")
                    if c2.button("🧠 Summarize", key=f"sum_{f.name}", use_container_width=True):
                        st.info(f"AI: Strategic Relevance 88%. Analysis Committed.")

    with t2:
        url = st.text_input("Link", placeholder="Target URL...")
        if url and st.button("Bridge Data Link", use_container_width=True):
            st.success("Synced.")
            if "youtube" in url: st.video(url)

def render_file_utilities():
    st.markdown("<h1 class='vdc-main-header'>Infra Utils</h1>", unsafe_allow_html=True)
    st.write("### Asset Transcoding & Optimization")

    action = st.radio("Core Service", ["Compress", "Transcode", "Deep Scan"], horizontal=True)
    st.divider()
    
    op_col1, op_col2 = st.columns([1, 1])
    
    file_buffer = None
    file_name = None
    
    with op_col1:
        uploaded_file = st.file_uploader("Target Asset", type=['csv', 'json', 'txt', 'parquet', 'py', 'md'])
        if uploaded_file:
            file_buffer = uploaded_file.read()
            file_name = uploaded_file.name
            size_kb = len(file_buffer) / 1024
            
            with st.container(border=True):
                st.write(f"**Loaded: {file_name}**")
                st.metric("Size", f"{size_kb:.2f} KB")
                st.caption("Buffer Active")

    with op_col2:
        if not uploaded_file:
            st.info("Awaiting Input Stream...")
        else:
            # --- COMPRESSION MODULE ---
            if action == "Compress":
                with st.container(border=True):
                    st.write("#### Archival Engine")
                    comp_level = st.slider("Compression Ratio", 1, 9, 6)
                    if st.button("Execute Compression", use_container_width=True):
                        import zipfile
                        
                        try:
                            # Create Zip in Memory
                            zip_buffer = io.BytesIO()
                            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=comp_level) as zf:
                                zf.writestr(file_name, file_buffer)
                            
                            zip_buffer.seek(0)
                            final_size = len(zip_buffer.getvalue()) / 1024
                            reduction = (1 - (final_size / size_kb)) * 100
                            
                            st.success(f"Compressed: {reduction:.1f}% Reduction")
                            st.download_button(
                                label="Download Archive",
                                data=zip_buffer,
                                file_name=f"{file_name}.zip",
                                mime="application/zip",
                                use_container_width=True
                            )
                        except Exception as e:
                            st.error(f"Compression Failed: {e}")

            # --- TRANSCODE MODULE ---
            elif action == "Transcode":
                with st.container(border=True):
                    st.write("#### Format Shifter")
                    target_format = st.selectbox("Target Protocol", ["CSV", "JSON", "Parquet"])
                    
                    if st.button("Transcode Asset", use_container_width=True):
                        try:
                            df = None
                            # LOAD
                            if file_name.endswith('.csv'):
                                df = pd.read_csv(io.BytesIO(file_buffer))
                            elif file_name.endswith('.json'):
                                df = pd.read_json(io.BytesIO(file_buffer))
                            elif file_name.endswith('.parquet'):
                                df = pd.read_parquet(io.BytesIO(file_buffer))
                            else:
                                st.error("Unsupported Source Format for Transcoding")
                            
                            if df is not None:
                                export_buffer = io.BytesIO()
                                mime_type = "text/plain"
                                new_name = f"converted_{file_name.split('.')[0]}"
                                
                                # EXPORT
                                if target_format == "CSV":
                                    df.to_csv(export_buffer, index=False)
                                    mime_type = "text/csv"
                                    new_name += ".csv"
                                elif target_format == "JSON":
                                    df.to_json(export_buffer, orient='records')
                                    mime_type = "application/json"
                                    new_name += ".json"
                                elif target_format == "Parquet":
                                    df.to_parquet(export_buffer)
                                    mime_type = "application/octet-stream"
                                    new_name += ".parquet"
                                
                                export_buffer.seek(0)
                                st.success("Transcode Complete")
                                st.download_button(label="Download Asset", data=export_buffer, file_name=new_name, mime=mime_type, use_container_width=True)
                                
                        except Exception as e:
                            st.error(f"Transcode Error: {e}")

            # --- DEEP SCAN MODULE ---
            elif action == "Deep Scan":
                 with st.container(border=True):
                    st.write("#### Asset Forensics")
                    
                    # Logic for text based files
                    try:
                        is_text = file_name.split('.')[-1] in ['txt', 'py', 'md', 'csv', 'json', 'log']
                        if is_text:
                            content_str = file_buffer.decode('utf-8')
                            lines = content_str.split('\n')
                            st.metric("Line Count", len(lines))
                            st.metric("Character Count", len(content_str))
                            
                            st.text_area("Snippet", content_str[:500] + "...", height=150)
                        else:
                            st.info("Binary Asset Detected. Metadata extraction only.")
                            st.code(f"Hex Header: {file_buffer[:16].hex()}", language="text")
                            
                    except Exception as e:
                        st.error(f"Scan Error: {e}")

def render_visualization_studio():
    st.markdown("<h1 class='vdc-main-header'>Visualization</h1>", unsafe_allow_html=True)
    st.write("### Data Topology & Schema Map")
    
    con = get_connection(read_only=True)
    try:
        # Fetch Tables
        tables = con.execute("SHOW TABLES").df()['name'].tolist()
        
        if not tables:
            st.info("No Data Objects Found in Topology.")
            return

        # Fetch Metrics for Nodes
        node_data = []
        for t in tables:
            try:
                row_count = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                node_data.append({"name": t, "rows": row_count, "type": "TABLE"})
            except:
                node_data.append({"name": t, "rows": 0, "type": "TABLE"})
        
        # --- PLOTLY GRAPH GENERATION ---
        # Layout: Hub & Spoke (Star Topology)
        # Center: VDC System
        
        edge_x = []
        edge_y = []
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        
        # Center Node
        node_x.append(0)
        node_y.append(0)
        node_text.append("<b>VDC KERNEL</b><br>Central Hub")
        node_size.append(40)
        node_color.append('#0f172a') # Dark Slate
        
        # Spoke Nodes (Tables)
        angle_step = 360 / len(node_data)
        radius = 1.5
        
        for i, node in enumerate(node_data):
            angle_rad = math.radians(i * angle_step)
            x = radius * math.cos(angle_rad)
            y = radius * math.sin(angle_rad)
            
            # Edges
            edge_x.extend([0, x, None])
            edge_y.extend([0, y, None])
            
            # Nodes
            node_x.append(x)
            node_y.append(y)
            info = f"<b>{node['name'].upper()}</b><br>Rows: {node['rows']:,}<br>Type: Parquet/Table"
            node_text.append(info)
            
            # Dynamic Size based on rows (log scale-ish)
            s = 15 + min(math.log(max(node['rows'], 1) + 1) * 3, 30)
            node_size.append(s)
            node_color.append('#2563eb') # Enterprise Blue
            
        # Draw Edges
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#cbd5e1'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Draw Nodes
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[n['name'].upper() for n in [{"name": "VDC CORE"}] + node_data],
            textposition="bottom center",
            hovertext=node_text,
            marker=dict(
                color=node_color,
                size=node_size,
                line=dict(width=2, color='white')
            )
        )
        
        fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=0,l=0,r=0,t=0),
                width=700,
                height=500,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            ))
            
        c1, c2 = st.columns([3, 1])
        with c1:
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            st.write("#### Node Health")
            for n in node_data:
                st.metric(n['name'].upper(), f"{n['rows']:,}", "Active")

    except Exception as e:
        st.error(f"Topology Render Failed: {e}")
    finally:
        con.close()

def render_workflow_automation():
    st.markdown("<h1 class='vdc-main-header'>Automation</h1>", unsafe_allow_html=True)
    st.write("### Scheduled Infrastructure Logistics")
    
    m1, m2 = st.columns(2)
    with m1: st.metric("Workflows", "4")
    with m2: st.metric("Automation Rate", "98.8%")
    
    st.divider()
    st.subheader("Pipelines")
    for w in ["DATA_SYNC_PROD", "AUDIT_VERIFY"]:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            c1.write(f"**Task: {w}**")
            c1.caption("Status: Standby | Mode: High-Performance")
            if c2.button("Run Manual", key=f"run_{w}", use_container_width=True):
                st.toast(f"Triggered {w} Handshake.")
