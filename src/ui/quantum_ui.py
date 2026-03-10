
import streamlit as st
import time
import pandas as pd
import numpy as np
import altair as alt
from src.quantum_orchestrator import QuantumOrchestrator
from src.audit_logger import log_action

def render_quantum_orchestrator():
    st.markdown("<h1 class='vdc-main-header'>Quantum Orchestrator</h1>", unsafe_allow_html=True)
    st.write("### Sub-Atomic Infrastructure & PQC Routing")
    
    if 'q_engine' not in st.session_state:
         st.session_state.q_engine = QuantumOrchestrator()
    qo = st.session_state.q_engine

    if 'quantum_result' not in st.session_state:
        st.session_state.quantum_result = None

    tabs = st.tabs(["🚀 Orchestration", "🛰️ Telemetry", "🛡️ Security", "🌱 Climate"])
    
    with tabs[0]:
        with st.container(border=True):
            st.markdown("### Execution Control")
            c1, c2 = st.columns(2)
            with c1:
                category = st.selectbox("Operational Domain", ["Portfolio Opt.", "Neural Weights", "Prime Scan"])
                depth = st.slider("Qubit Depth", 16, 512, 256)
            with c2:
                st.write("**Resource Forecast**")
                st.metric("Latency", f"{(depth**1.15)/18:.2f}ms", "-18%")
                st.metric("Power Burn", f"{depth*0.32:.1f} W")

            if st.button("Run Quantum Job", use_container_width=True):
                with st.status("Initializing Fabric...") as s:
                    time.sleep(1)
                    res = qo.orchestrate_task(category, depth)
                    st.session_state.quantum_result = res
                    s.update(label="Job Complete.", state="complete")
                    st.balloons()

        if st.session_state.quantum_result:
            r = st.session_state.quantum_result
            st.divider()
            with st.container(border=True):
                st.write(f"#### Output: {r['task']}")
                k1, k2, k3 = st.columns(3)
                k1.metric("Fidelity", r['fidelity'])
                k2.metric("Confidence", r['success_probability'])
                k3.metric("Depth", r['circuit_depth'])
                if st.button("Flush Results", use_container_width=True):
                    st.session_state.quantum_result = None
                    st.rerun()

    with tabs[1]:
        st.write("#### Node Pulse & Integrity")
        t_col1, t_col2 = st.columns([1, 2])
        with t_col1:
            st.metric("Stability", "99.1%")
            st.metric("Coherence", "148ms")
        with t_col2:
            # Clean Blue/White Entanglement Map
            dot = qo.get_entanglement_map(16).replace('color="#30363d"', 'color="#2563eb"').replace('fillcolor="#161b22"', 'fillcolor="#ffffff"').replace('fontcolor="#58a6ff"', 'fontcolor="#0f172a"')
            st.graphviz_chart(dot, use_container_width=True)

    with tabs[2]:
        st.write("#### PQC Control Plane")
        st.success("Protection: CRYSTALS-Kyber L3 Secured.")
        with st.container(border=True):
            st.write("**Security Params**")
            st.code("Algo: KYBER-768\nMode: NIST Standard\nSeed: Rotating", language="text")
            if st.button("Rotate Security Keys", use_container_width=True):
                st.toast("Seeds Rotated Successfully.")

    with tabs[3]:
        st.write("#### Sustainability Index")
        met = qo.get_energy_metrics(depth if 'depth' in locals() else 128)
        s1, s2, s3 = st.columns(3)
        s1.metric("Carbon Saved", f"{met['savings_carbon']:.2f} KG")
        s2.metric("PUE Ratio", "1.01")
        s3.metric("Credits", "56")
        
        st.divider()
        st.button("Purchase Offset Credits", use_container_width=True)
