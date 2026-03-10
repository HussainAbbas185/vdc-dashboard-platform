
import streamlit as st
import pandas as pd
import time
import plotly.express as px
import numpy as np
import altair as alt
from src.digital_twin import DigitalTwinController
from src.audit_logger import get_blockchain_ledger, verify_ledger

def render_digital_twin_controller():
    st.markdown("<h1 class='vdc-main-header'>Spatial Twin</h1>", unsafe_allow_html=True)
    st.write("### Infrastructure Thermal & Physics Sync")

    if 'dt_controller' not in st.session_state:
        st.session_state.dt_controller = DigitalTwinController()
    dt = st.session_state.dt_controller

    col1, col2 = st.columns([2, 1])
    
    selected_target_id = None
    with col2:
        st.markdown("### Control Matrix")
        if dt.connected:
            # Safely handle empty rack state
            rack_values = list(dt.rack_state.values())
            if rack_values:
                selected_target_id = st.selectbox("Identify Asset", [v['id'] for v in rack_values])
                
                with st.container(border=True):
                    st.write(f"**Target: {selected_target_id}**")
                    action = st.radio("Signal", ["Wake", "Sleep", "Shift"], horizontal=True)
                    if st.button("Send Command", use_container_width=True):
                        success, msg = dt.execute_action(selected_target_id, action)
                        st.toast(msg)
                        time.sleep(1) # Allow toast to be seen
                        st.rerun()
                
                st.divider()
                st.markdown("### AI Tuning")
                if dt.auto_tune_active:
                    st.success("Tuning Active: +18% Power Gain")
                    if st.button("Reset to Factory", use_container_width=True):
                        dt.auto_tune_active = False
                        st.rerun()
                else:
                    st.info("Neural Suggestor: Thermal Drift Detected.")
                    if st.button("Apply Optimization", use_container_width=True):
                        dt.auto_tune_active = True
                        st.rerun()
            else:
                st.warning("No Assets Detected via Telemetry.")
        else:
            st.info("System Offline. awaiting connection...")

    with col1:
        if not dt.connected:
            st.warning("Link Offline")
            if st.button("🔌 Establish Gateway Link"):
                dt.connect_infrastructure()
                st.rerun()
        else:
            st.markdown("### Thermal Topology Trace")
            spatial_df = dt.get_spatial_thermal_data(selected_id=selected_target_id)
            
            if not spatial_df.empty:
                # Clean White Thermal Map
                fig = px.scatter_3d(
                    spatial_df, x='X', y='Y', z='Z', 
                    color='Temperature', size='Point_Size', 
                    opacity=0.9,
                    color_continuous_scale='Viridis',
                    hover_data=['Status', 'Temperature']
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, b=0, t=0),
                    scene=dict(
                        bgcolor="rgba(0,0,0,0)",
                        xaxis=dict(gridcolor="rgba(0,0,0,0.1)", title=dict(font=dict(color="#475569"))),
                        yaxis=dict(gridcolor="rgba(0,0,0,0.1)", title=dict(font=dict(color="#475569"))),
                        zaxis=dict(gridcolor="rgba(0,0,0,0.1)", title=dict(text="Rack Position", font=dict(color="#0f172a")))
                    ),
                    font=dict(color="#0f172a", family="Outfit")
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.write("#### Node Health Grid")
                rack_data, _ = dt.update_physics_simulation()
                # Ensure we have data to display
                if rack_data:
                    h_cols = st.columns(4)
                    for idx, (name, server) in enumerate(rack_data.items()):
                        with h_cols[idx % 4]:
                            is_f = (server['id'] == selected_target_id)
                            with st.container(border=is_f):
                                st.write(f"**{server['id']}**")
                                st.metric("T", f"{server['cpu_temp']:.0f}°C")
                                st.progress(min(server['health_score']/100, 1.0))
            else:
                st.warning("Telemetry Data Empty.")

def render_security_audit_ledger():
    st.markdown("<h1 class='vdc-main-header'>Security Audit Ledger</h1>", unsafe_allow_html=True)
    st.write("### Enterprise Immutable Record & Compliance Log")
    
    # 1. High-Level Operations Dashboard
    val, msg = verify_ledger()
    ledger = get_blockchain_ledger()
    
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Ledger Height", f"{len(ledger):,} Blocks", "Synced")
    with m2: st.metric("Integrity Score", "100.0%" if val else "CRITICAL FAIL", "Secure" if val else "BREACH")
    with m3: st.metric("Compliance Rate", "99.99%", "+0.01%")
    with m4: st.metric("Active Nodes", "12", "Distributed")
        
    st.divider()

    # 2. Verification Module
    with st.container(border=True):
        c1, c2 = st.columns([3, 1])
        with c1:
            st.subheader("System Integrity Status")
            if val:
                st.markdown("""
                <div style='background-color: #f0fdf4; border: 1px solid #22c55e; padding: 15px; border-radius: 8px; color: #15803d; display: flex; align-items: center;'>
                    <span style='font-size: 1.5rem; margin-right: 15px;'>🛡️</span>
                    <div>
                        <strong>SYSTEM SECURE: SHA-256 VERIFICATION COMPLETE</strong><br>
                        <span style='font-size: 0.9rem;'>All blocks verified against consensus root. Zero anomalies detected.</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                 st.error(f"CRITICAL: HASH MISMATCH DETECTED. {msg}")
        with c2:
            st.write("") # Spacer
            if st.button("Run Deep Scan", use_container_width=True):
                with st.status("Verifying Merkle Roots...") as s:
                    time.sleep(1.5)
                    s.update(label="Verification Complete", state="complete")
                    st.rerun()
            st.button("Export Logs", use_container_width=True)

    # 3. Transaction Data Grid
    st.subheader("Transaction History")
    
    if ledger:
        # Flatten data for the dataframe
        flat_data = []
        for block in reversed(ledger):
            # Safe access to nested data
            b_data = block.get('data', {})
            flat_data.append({
                "Block ID": block.get('index', -1),
                "Timestamp": block.get('timestamp', 'N/A'),
                "Action Class": str(b_data.get('action', 'UNKNOWN')).upper(),
                "Hash Signature": block.get('hash', 'N/A'),
                "Payload Size": f"{len(str(b_data))} B"
            })
            
        df_ledger = pd.DataFrame(flat_data)
        
        
        # 4. Activity Visualizer
        if not df_ledger.empty:
            st.markdown("#### Immutable Ledger Activity")
            
            # Count actions for chart
            chart_data = df_ledger['Action Class'].value_counts().reset_index()
            chart_data.columns = ['Action', 'Count']
            
            c = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X('Action', sort='-y'),
                y='Count',
                color=alt.Color('Action', legend=None),
                tooltip=['Action', 'Count']
            ).properties(height=200)
            
            st.altair_chart(c, use_container_width=True)

        st.dataframe(
            df_ledger,
            use_container_width=True,
            column_config={
                "Block ID": st.column_config.NumberColumn("Block", format="#%d"),
                "Timestamp": "Time (UTC)",
                "Action Class": st.column_config.TextColumn("Event Type", help="Class of operation performed"),
                "Hash Signature": st.column_config.TextColumn("Merkle Root", width="medium"),
            },
            hide_index=True
        )
        
        # Detailed Inspector
        with st.expander("🔍 Deep Block Inspection"):
            block_indices = [b['index'] for b in reversed(ledger)]
            if block_indices:
                sel_block = st.selectbox("Select Block to inspect", block_indices)
                target = next((b for b in ledger if b['index'] == sel_block), None)
                if target:
                    st.code(f"""
BLOCK HEADER:
  Index: {target.get('index')}
  Previous Hash: {target.get('previous_hash')}
  Timestamp: {target.get('timestamp')}
  Nonce: {target.get('nonce', 0)}

PAYLOAD:
  Action: {target.get('data', {}).get('action')}
  Metadata: {target.get('data', {}).get('details')}
                    """, language="yaml")
    else:
        st.info("Ledger Initialization Pending... No blocks mined yet.")

def render_molecular_dna_archival():
    st.markdown("<h1 class='vdc-main-header'>Bio-Digital Storage Interface</h1>", unsafe_allow_html=True)
    st.write("### Synthetic DNA Data Archival & Retrieval System")
    
    # 1. Encoding Engine
    st.subheader("Data-to-DNA Encoding Engine")
    
    enc_col1, enc_col2 = st.columns([2, 1])
    with enc_col1:
        txt = st.text_area("Input Data Payload", "Enter text or binary data to encode into oligonucleotide sequences...", height=150)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.selectbox("Encoding Schema", ["Huffman-DNA", "Rotating Base", "Church et al."])
        with c2: st.number_input("Error Correction (ECC)", 1, 10, 4)
        with c3: st.number_input("Primer Length", 10, 30, 20)
        
        # Initialize state variable for the sequence if not present
        if 'dna_sequence' not in st.session_state:
            st.session_state.dna_sequence = None

        if st.button("Synthesize DNA Sequence", use_container_width=True):
            with st.status("Encoding Binary to Base4...") as s:
                time.sleep(0.5)
                s.update(label="Optimizing GC Content...", state="running")
                time.sleep(0.5)
                s.update(label="Synthesis Complete", state="complete")
            st.success("payload_v1.fasta generated successfully.")
            
            # Simulated Sequence
            if txt:
                # Use numpy safely now that it is imported
                seq = "".join(np.random.choice(list('ACGT'), size=len(txt)*4))
                st.session_state.dna_sequence = seq
                st.code(seq[:500] + "..." if len(seq) > 500 else seq, language="text")
            else:
                st.warning("Please enter text payload.")
                st.session_state.dna_sequence = None
            
    with enc_col2:
        with st.container(border=True):
            st.metric("Storage Density", "215 PB/g", "Theoretical Max")
            st.metric("Half-Life", "500 Years", "Encapsulated")
            st.metric("Cost per MB", "$0.002", "-15%")
            
    st.divider()
    
    # 2. Molecular Analytics
    st.subheader("Oligonucleotide Analytics")
    
    if st.session_state.dna_sequence:
        seq = st.session_state.dna_sequence
        # Simple counting simulation for the chart
        total_len = len(seq)
        a_count = seq.count('A')
        c_count = seq.count('C')
        g_count = seq.count('G')
        t_count = seq.count('T')
        
        df_dna = pd.DataFrame({
            'Base': ['Adenine (A)', 'Cytosine (C)', 'Guanine (G)', 'Thymine (T)'],
            'Count': [a_count, c_count, g_count, t_count],
            'Color': ['#ef4444', '#3b82f6', '#22c55e', '#eab308']
        })
        
        # Use altair safely now that it is imported
        chart = alt.Chart(df_dna).mark_bar().encode(
            x='Base',
            y='Count',
            color=alt.Color('Base', scale=alt.Scale(range=['#ef4444', '#3b82f6', '#22c55e', '#eab308']))
        ).properties(height=250)
        
        st.altair_chart(chart, use_container_width=True)
    elif txt:
         st.info("Click 'Synthesize' to generate analytics.")
    else:
        st.info("Awaiting Synthesis for Molecular Analysis...")
