import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

st.set_page_config(page_title="API Firewall Dashboard", layout="wide")

LOG_FILE = "backend/firewall_logs.json"

@st.cache_data(ttl=30)
def load_logs():
    """Load and parse firewall logs."""
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame()
    
    logs = []
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))
    except Exception as e:
        st.error(f"Error loading logs: {e}")
        return pd.DataFrame()
    
    if not logs:
        return pd.DataFrame()
    
    df = pd.DataFrame(logs)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def main():
    st.title("🛡️ API Firewall - Real-time Security Dashboard")
    
    # Load data
    df = load_logs()
    
    if df.empty:
        st.warning("No firewall logs found. Start making requests to see data.")
        return
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Time filter
    time_range = st.sidebar.selectbox(
        "Time Range",
        ["Last Hour", "Last 24 Hours", "Last 7 Days", "All Time"]
    )
    
    now = datetime.now()
    if time_range == "Last Hour":
        start_time = now - timedelta(hours=1)
    elif time_range == "Last 24 Hours":
        start_time = now - timedelta(days=1)
    elif time_range == "Last 7 Days":
        start_time = now - timedelta(days=7)
    else:
        start_time = df['timestamp'].min()
    
    filtered_df = df[df['timestamp'] >= start_time]
    
    # Threat type filter
    threat_types = filtered_df['threat_type'].unique()
    selected_threats = st.sidebar.multiselect(
        "Threat Types",
        threat_types,
        default=threat_types
    )
    
    filtered_df = filtered_df[filtered_df['threat_type'].isin(selected_threats)]
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_requests = len(filtered_df)
    blocked_requests = len(filtered_df[filtered_df['threat_type'] != 'None'])
    allowed_requests = total_requests - blocked_requests
    block_rate = (blocked_requests / total_requests * 100) if total_requests > 0 else 0
    
    with col1:
        st.metric("Total Requests", total_requests)
    with col2:
        st.metric("Blocked Requests", blocked_requests)
    with col3:
        st.metric("Allowed Requests", allowed_requests)
    with col4:
        st.metric("Block Rate", f"{block_rate:.1f}%")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Threat Types Distribution")
        threat_counts = filtered_df['threat_type'].value_counts()
        fig_pie = px.pie(
            values=threat_counts.values,
            names=threat_counts.index,
            title="Distribution of Threat Types"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Requests Over Time")
        hourly_data = filtered_df.set_index('timestamp').resample('H').size()
        fig_line = px.line(
            x=hourly_data.index,
            y=hourly_data.values,
            title="Requests per Hour"
        )
        fig_line.update_layout(xaxis_title="Time", yaxis_title="Request Count")
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Top IPs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Client IPs")
        top_ips = filtered_df['client_ip'].value_counts().head(10)
        fig_bar = px.bar(
            x=top_ips.values,
            y=top_ips.index,
            orientation='h',
            title="Most Active IP Addresses"
        )
        fig_bar.update_layout(yaxis_title="IP Address", xaxis_title="Request Count")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("Status Code Distribution")
        status_counts = filtered_df['status_code'].value_counts()
        fig_status = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            title="HTTP Status Codes"
        )
        fig_status.update_layout(xaxis_title="Status Code", yaxis_title="Count")
        st.plotly_chart(fig_status, use_container_width=True)
    
    # Recent threats table
    st.subheader("Recent Security Events")
    
    # Filter for threats only
    threats_df = filtered_df[filtered_df['threat_type'] != 'None'].copy()
    
    if not threats_df.empty:
        # Show recent threats
        recent_threats = threats_df.sort_values('timestamp', ascending=False).head(20)
        
        # Format for display
        display_df = recent_threats[['timestamp', 'client_ip', 'method', 'url', 'threat_type', 'status_code']].copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "timestamp": "Time",
                "client_ip": "Client IP",
                "method": "Method",
                "url": "URL",
                "threat_type": "Threat Type",
                "status_code": "Status"
            }
        )
    else:
        st.info("No security threats detected in the selected time range.")
    
    # Auto-refresh
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    # Auto-refresh every 30 seconds
    st.sidebar.markdown("---")
    if st.sidebar.checkbox("Auto-refresh (30s)"):
        import time
        time.sleep(30)
        st.rerun()

if __name__ == "__main__":
    main()