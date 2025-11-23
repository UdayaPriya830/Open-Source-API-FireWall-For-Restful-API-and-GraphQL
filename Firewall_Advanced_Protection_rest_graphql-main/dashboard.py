import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import numpy as np

# Professional dashboard configuration
st.set_page_config(
    page_title="🛡️ API Firewall - Security Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/UdayaPriya830/Open-Source-API-FireWall-For-Restful-API-and-GraphQL',
        'Report a bug': 'https://github.com/UdayaPriya830/Open-Source-API-FireWall-For-Restful-API-and-GraphQL/issues',
        'About': '# API Firewall Dashboard\nReal-time security monitoring for REST and GraphQL APIs'
    }
)

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
    # Header with professional styling
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; text-align: center; margin: 0;">🛡️ API Firewall Security Dashboard</h1>
        <p style="color: #e0e0e0; text-align: center; margin: 0.5rem 0 0 0;">Real-time monitoring & OWASP Top 10 threat detection</p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Enhanced metrics with OWASP categorization
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_requests = len(filtered_df)
    blocked_requests = len(filtered_df[filtered_df['threat_type'] != 'None'])
    allowed_requests = total_requests - blocked_requests
    block_rate = (blocked_requests / total_requests * 100) if total_requests > 0 else 0
    
    # Count OWASP threats
    owasp_threats = len(filtered_df[filtered_df['threat_type'].str.contains('OWASP', na=False)])
    
    with col1:
        st.metric(
            "📊 Total Requests", 
            f"{total_requests:,}",
            delta=f"+{len(filtered_df[filtered_df['timestamp'] >= datetime.now() - timedelta(hours=1)])} (1h)"
        )
    with col2:
        st.metric(
            "🚫 Blocked Requests", 
            f"{blocked_requests:,}",
            delta=f"{block_rate:.1f}% block rate",
            delta_color="inverse"
        )
    with col3:
        st.metric(
            "✅ Allowed Requests", 
            f"{allowed_requests:,}",
            delta=f"{100-block_rate:.1f}% success rate"
        )
    with col4:
        st.metric(
            "⚠️ OWASP Top 10 Threats", 
            f"{owasp_threats:,}",
            delta="Critical security risks",
            delta_color="inverse"
        )
    with col5:
        # Security score calculation
        security_score = max(0, 100 - (block_rate * 2))
        st.metric(
            "🛡️ Security Score", 
            f"{security_score:.0f}/100",
            delta="Higher is better"
        )
    
    # Professional section headers
    st.markdown("---")
    st.markdown("## 📈 **Threat Analysis & Visualization**")
    
    # Enhanced charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 OWASP Top 10 Threat Distribution")
        threat_counts = filtered_df['threat_type'].value_counts()
        
        # Color mapping for different threat types
        colors = {
            'None': '#2ecc71',  # Green for safe
            'SQL Injection (OWASP #3)': '#e74c3c',  # Red for critical
            'XSS Attack (OWASP #3)': '#e67e22',  # Orange
            'Broken Access Control (OWASP #1)': '#9b59b6',  # Purple
            'Prompt Injection (AI/LLM)': '#f39c12'  # Yellow
        }
        
        fig_pie = px.pie(
            values=threat_counts.values,
            names=threat_counts.index,
            title="Security Threat Categories",
            color_discrete_map=colors
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            showlegend=True,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.01)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("📊 Real-time Traffic Analysis")
        
        # Enhanced time series with threat overlay
        hourly_data = filtered_df.set_index('timestamp').resample('H').agg({
            'threat_type': 'count',
            'client_ip': 'nunique'
        }).rename(columns={'threat_type': 'total_requests', 'client_ip': 'unique_ips'})
        
        hourly_threats = filtered_df[filtered_df['threat_type'] != 'None'].set_index('timestamp').resample('H').size()
        
        fig_line = go.Figure()
        
        # Total requests line
        fig_line.add_trace(go.Scatter(
            x=hourly_data.index,
            y=hourly_data['total_requests'],
            mode='lines+markers',
            name='Total Requests',
            line=dict(color='#3498db', width=2)
        ))
        
        # Threats overlay
        fig_line.add_trace(go.Scatter(
            x=hourly_threats.index,
            y=hourly_threats.values,
            mode='lines+markers',
            name='Blocked Threats',
            line=dict(color='#e74c3c', width=2),
            fill='tonexty'
        ))
        
        fig_line.update_layout(
            title="Traffic & Threat Patterns Over Time",
            xaxis_title="Time",
            yaxis_title="Request Count",
            hovermode='x unified',
            showlegend=True
        )
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Advanced analytics section
    st.markdown("---")
    st.markdown("## 🔍 **Advanced Security Analytics**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 Suspicious IP Analysis")
        
        # Enhanced IP analysis with threat correlation
        ip_analysis = filtered_df.groupby('client_ip').agg({
            'threat_type': ['count', lambda x: (x != 'None').sum()],
            'timestamp': ['min', 'max']
        }).round(2)
        
        ip_analysis.columns = ['total_requests', 'threat_count', 'first_seen', 'last_seen']
        ip_analysis['threat_ratio'] = (ip_analysis['threat_count'] / ip_analysis['total_requests'] * 100).round(1)
        ip_analysis = ip_analysis.sort_values('threat_count', ascending=False).head(10)
        
        # Create enhanced bar chart
        fig_bar = px.bar(
            x=ip_analysis['threat_count'],
            y=ip_analysis.index,
            orientation='h',
            title="Top Threat Sources by IP Address",
            color=ip_analysis['threat_ratio'],
            color_continuous_scale='Reds',
            hover_data={'total_requests': ip_analysis['total_requests']}
        )
        fig_bar.update_layout(
            yaxis_title="IP Address", 
            xaxis_title="Threat Count",
            coloraxis_colorbar_title="Threat %"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("📋 Response Status Analysis")
        
        status_counts = filtered_df['status_code'].value_counts()
        
        # Color code status codes
        status_colors = {
            200: '#2ecc71',  # Success - Green
            403: '#e74c3c',  # Forbidden - Red
            404: '#f39c12',  # Not Found - Orange
            500: '#9b59b6'   # Server Error - Purple
        }
        
        colors = [status_colors.get(status, '#95a5a6') for status in status_counts.index]
        
        fig_status = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            title="HTTP Response Status Distribution",
            color=status_counts.index,
            color_discrete_map=status_colors
        )
        
        # Add annotations for status meanings
        annotations = {
            200: "✅ Success",
            403: "🚫 Blocked", 
            404: "❓ Not Found",
            500: "💥 Error"
        }
        
        fig_status.update_layout(
            xaxis_title="HTTP Status Code", 
            yaxis_title="Request Count",
            showlegend=False
        )
        
        # Add text annotations
        for i, (status, count) in enumerate(status_counts.items()):
            if status in annotations:
                fig_status.add_annotation(
                    x=status, y=count,
                    text=annotations[status],
                    showarrow=True,
                    arrowhead=2
                )
        
        st.plotly_chart(fig_status, use_container_width=True)
    
    # OWASP Top 10 breakdown
    st.markdown("---")
    st.markdown("## 🛡️ **OWASP Top 10 Security Analysis**")
    
    # OWASP breakdown
    owasp_data = filtered_df[filtered_df['threat_type'].str.contains('OWASP', na=False)]
    
    if not owasp_data.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            owasp_counts = owasp_data['threat_type'].value_counts()
            fig_owasp = px.bar(
                x=owasp_counts.values,
                y=owasp_counts.index,
                orientation='h',
                title="OWASP Top 10 Threat Detection Summary",
                color=owasp_counts.values,
                color_continuous_scale='Reds'
            )
            fig_owasp.update_layout(
                yaxis_title="OWASP Category",
                xaxis_title="Detection Count",
                height=400
            )
            st.plotly_chart(fig_owasp, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 **OWASP Statistics**")
            total_owasp = len(owasp_data)
            st.metric("Total OWASP Threats", total_owasp)
            
            if total_owasp > 0:
                most_common = owasp_counts.index[0]
                st.info(f"**Most Common:** {most_common}")
                
                # Risk level assessment
                if total_owasp > 50:
                    st.error("🚨 **HIGH RISK** - Multiple OWASP threats detected")
                elif total_owasp > 10:
                    st.warning("⚠️ **MEDIUM RISK** - Some OWASP threats present")
                else:
                    st.success("✅ **LOW RISK** - Minimal OWASP threats")
    
    # Recent threats table with enhanced formatting
    st.markdown("---")
    st.markdown("## 🚨 **Recent Security Events**")
    
    # Filter for threats only
    threats_df = filtered_df[filtered_df['threat_type'] != 'None'].copy()
    
    if not threats_df.empty:
        # Enhanced threat table with severity indicators
        recent_threats = threats_df.sort_values('timestamp', ascending=False).head(20)
        
        # Format for display with enhanced columns
        display_df = recent_threats[['timestamp', 'client_ip', 'method', 'url', 'threat_type', 'status_code']].copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Add severity column
        def get_severity(threat_type):
            if 'OWASP #1' in threat_type or 'OWASP #2' in threat_type or 'OWASP #3' in threat_type:
                return "🔴 Critical"
            elif 'OWASP' in threat_type:
                return "🟡 High"
            elif 'Injection' in threat_type:
                return "🟠 Medium"
            else:
                return "🔵 Low"
        
        display_df['severity'] = display_df['threat_type'].apply(get_severity)
        
        # Reorder columns
        display_df = display_df[['timestamp', 'severity', 'threat_type', 'client_ip', 'method', 'url', 'status_code']]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "timestamp": st.column_config.TextColumn("🕐 Time", width="medium"),
                "severity": st.column_config.TextColumn("⚠️ Severity", width="small"),
                "threat_type": st.column_config.TextColumn("🎯 Threat Type", width="large"),
                "client_ip": st.column_config.TextColumn("🌐 Client IP", width="medium"),
                "method": st.column_config.TextColumn("📝 Method", width="small"),
                "url": st.column_config.TextColumn("🔗 URL", width="large"),
                "status_code": st.column_config.NumberColumn("📊 Status", width="small")
            },
            hide_index=True
        )
    else:
        st.success("🎉 **Excellent!** No security threats detected in the selected time range.")
        st.balloons()  # Celebration for good security
    
    # Enhanced sidebar controls
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 **Dashboard Controls**")
    
    # Manual refresh
    if st.sidebar.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    # Export functionality
    if st.sidebar.button("📥 Export Data"):
        csv = filtered_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"firewall_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Auto-refresh toggle
    auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh (30s)")
    
    # Dashboard info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ **Dashboard Info**")
    st.sidebar.info(
        f"**Last Updated:** {datetime.now().strftime('%H:%M:%S')}\n\n"
        f"**Total Records:** {len(df):,}\n\n"
        f"**Filtered Records:** {len(filtered_df):,}\n\n"
        f"**OWASP Coverage:** ✅ Top 10"
    )
    
    # Auto-refresh implementation
    if auto_refresh:
        import time
        time.sleep(30)
        st.rerun()

if __name__ == "__main__":
    main()