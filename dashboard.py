
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import json
import time
from mcp_system import run_mcp
from baseline import run_baseline
from config import TASK
from metrics import calculate_improvement, calculate_density

# Page Config
st.set_page_config(page_title="SolariX Control Center", layout="wide")

# --- DATABASE UTILITY ---
def get_blackboard_data():
    try:
        conn = sqlite3.connect("blackboard.db")
        df = pd.read_sql_query("SELECT * FROM updates ORDER BY id DESC LIMIT 10", conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()

# --- HEADER ---
st.title("🛰 SolariX: Agentic OS Dashboard")
st.markdown("Comparing **Stateless Baseline** vs. **Stateful MCP Blackboard** systems.")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("System Controls")
custom_task = st.sidebar.text_area("Modify Task Description:", TASK["description"])
run_btn = st.sidebar.button("Execute Head-to-Head Comparison")

# --- EXECUTION LOGIC ---
if run_btn:
    current_task = {"task_id": "TASK_UI", "description": custom_task}
    
    with st.spinner("🔄 Running Systems..."):
        # Run both systems
        base_res = run_baseline(current_task)
        mcp_res = run_mcp(current_task)
        
        # Calculate Metrics
        base_den = calculate_density(base_res)
        mcp_den = calculate_density(mcp_res)
        density_gain = ((mcp_den - base_den) / base_den) * 100
        token_red = calculate_improvement(base_res["tokens"], mcp_res["tokens"])
        
        # Display Success State
        st.toast("Comparison Complete!", icon="✅")

        # --- METRIC CARDS ---
        c1, c2, c3 = st.columns(3)
        c1.metric("Token Efficiency", f"+{token_red}%", delta_color="normal")
        c2.metric("Info Density Gain", f"+{density_gain:.1f}%")
        c3.metric("MCP Latency", f"{mcp_res['latency']:.3f}s")

        # --- CHARTS ---
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            st.subheader("Token Usage Comparison")
            fig_tokens = px.bar(
                x=["Baseline", "MCP"], 
                y=[base_res["tokens"], mcp_res["tokens"]],
                color=["Baseline", "MCP"],
                labels={'x': 'System', 'y': 'Total Tokens'}
            )
            st.plotly_chart(fig_tokens, use_container_width=True)

        with chart_col2:
            st.subheader("Information Density (Signal/Token)")
            fig_den = px.line(
                x=["Baseline", "MCP"], 
                y=[base_den, mcp_den],
                markers=True,
                labels={'x': 'System', 'y': 'Density Score'}
            )
            st.plotly_chart(fig_den, use_container_width=True)

# --- LIVE BLACKBOARD MONITOR ---
st.divider()
st.subheader("🧠 Real-Time Blackboard (SQLite Bus)")
db_data = get_blackboard_data()

if not db_data.empty:
    # Clean up the JSON for display
    db_data['update_json'] = db_data['update_json'].apply(lambda x: json.loads(x))
    st.table(db_data)
else:
    st.info("Blackboard is empty. Run a task to see shared memory updates.")

# --- AGENT LOGS ---
if 'mcp_res' in locals():
    with st.expander("See Detailed Agent Trace"):
        st.write("**Baseline Progress:**")
        st.write(base_res["progress"])
        st.write("**MCP Progress:**")
        st.write(mcp_res["progress"])