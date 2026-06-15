"""
Reliance Slate - Investor Readiness Platform
Interactive Dashboard for Investors
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

# Import custom modules
import sys
sys.path.append('src')
from financial_model import RelianceSlateFinancialModel
from unit_economics import UnitEconomicsCalculator
from market_sizing import MarketSizingAnalysis

# Page configuration
st.set_page_config(
    page_title="Reliance Slate - Investor Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3c72;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1e3c72;
    }
    .stButton button {
        background-color: #1e3c72;
        color: white;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize models
@st.cache_resource
def load_models():
    financial_model = RelianceSlateFinancialModel()
    ue_model = UnitEconomicsCalculator()
    market_model = MarketSizingAnalysis()
    return financial_model, ue_model, market_model

financial_model, ue_model, market_model = load_models()

# Sidebar
with st.sidebar:
    st.image("https://www.reliance.com/assets/images/reliance-logo.png", use_column_width=True)
    st.title("📊 Navigation")
    
    page = st.radio(
        "Select Section",
        ["🏠 Dashboard Overview", "💰 Financial Projections", "📈 Unit Economics", 
         "🌍 Market Sizing", "📊 Growth Metrics", "📥 Export Data"]
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Scenario Settings")
    
    scenario = st.selectbox(
        "Select Scenario",
        ["Base Case", "Conservative", "Aggressive"]
    )
    
    growth_rate = st.slider(
        "SMB Monthly Growth Rate",
        min_value=0.05,
        max_value=0.25,
        value=0.12,
        step=0.01,
        format="%.0f%%"
    )
    
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("For investor inquiries: **investors@reliance.com**")

# Main content
if page == "🏠 Dashboard Overview":
    st.markdown('<div class="main-header">Reliance Slate - Investor Dashboard</div>', unsafe_allow_html=True)
    
    # Generate data
    df = financial_model.generate_projections()
    ue_metrics = ue_model.get_all_metrics()
    market_metrics = market_model.get_market_metrics()
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Year 3 Revenue", f"₹{df['Total_Revenue'].iloc[-1]/1e7:.1f} Cr", delta="3-Year CAGR: 85%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Customers", f"{df['Total_Customers'].iloc[-1]:,}", delta="End of Year 3")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("SMB LTV:CAC", f"{ue_metrics['SMB']['LTV_CAC_Ratio']:.1f}x", delta="Excellent (>3x)")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        gross_margin = df['Gross_Margin'].iloc[-1]
        st.metric("Gross Margin", f"{gross_margin:.1%}", delta="Industry Leading")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Revenue Growth Trajectory")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Month'], y=df['Total_Revenue']/1e6,
            mode='lines+markers',
            name='Monthly Revenue (₹M)',
            line=dict(color='#1e3c72', width=3),
            marker=dict(size=6)
        ))
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Revenue (₹ Millions)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👥 Customer Growth")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['Month'][::3], y=df['SMB_Customers'][::3],
            name='SMB Customers', marker_color='#2E86AB'
        ))
        fig.add_trace(go.Bar(
            x=df['Month'][::3], y=df['Enterprise_Customers'][::3],
            name='Enterprise Customers', marker_color='#A23B72'
        ))
        fig.update_layout(
            barmode='stack',
            xaxis_title="Quarter",
            yaxis_title="Number of Customers",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Market Opportunity Section
    st.markdown("---")
    st.subheader("🎯 Market Opportunity")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("TAM", f"₹{market_metrics['TAM_Cr']:.0f} Cr", "Total Addressable Market")
    with col2:
        st.metric("SAM", f"₹{market_metrics['SAM_Cr']:.0f} Cr", "Serviceable Addressable Market")
    with col3:
        st.metric("SOM Year 3", f"₹{market_metrics['SOM_Year3_Cr']:.0f} Cr", "Target Market Share: 0.5%")

elif page == "💰 Financial Projections":
    st.title("💰 3-Year Financial Projections")
    
    # Generate projections
    df = financial_model.generate_projections()
    
    # Yearly Summary
    st.subheader("📊 Yearly Summary")
    yearly = df.groupby(df['Month'].str[:4]).agg({
        'Total_Revenue': 'sum',
        'Total_Customers': 'mean',
        'Gross_Margin': 'mean',
        'Operating_Margin': 'mean'
    }).round(2)
    
    st.dataframe(yearly, use_container_width=True)
    
    # Revenue Chart
    st.subheader("📈 Revenue Projection")
    fig = make_subplots(rows=2, cols=2, subplot_titles=('Monthly Revenue', 'Customer Growth', 'Profit Margins', 'Revenue Breakdown'))
    
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Total_Revenue']/1e6, mode='lines', name='Revenue (₹M)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Total_Customers'], mode='lines', name='Customers'), row=1, col=2)
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Gross_Margin']*100, mode='lines', name='Gross Margin %'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Operating_Margin']*100, mode='lines', name='Operating Margin %'), row=2, col=1)
    
    fig.update_layout(height=600, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Data Table
    with st.expander("View Detailed Monthly Data"):
        st.dataframe(df, use_container_width=True)

elif page == "📈 Unit Economics":
    st.title("📈 Unit Economics Analysis")
    
    ue_metrics = ue_model.get_all_metrics()
    
    # Comparison Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏪 SMB Segment")
        smb = ue_metrics['SMB']
        st.metric("Customer Acquisition Cost (CAC)", f"₹{smb['CAC']:,.0f}")
        st.metric("Lifetime Value (LTV)", f"₹{smb['LTV']:,.0f}")
        st.metric("LTV:CAC Ratio", f"{smb['LTV_CAC_Ratio']:.1f}x", delta="Target: >3x")
        st.metric("Payback Period", f"{smb['Payback_Months']:.1f} months", delta="Target: <12 months")
        st.metric("Monthly Revenue per Customer", f"₹{smb['Monthly_Revenue']:,.0f}")
        st.metric("Gross Margin", f"{smb['Gross_Margin']:.1%}")
    
    with col2:
        st.markdown("### 🏢 Enterprise Segment")
        ent = ue_metrics['Enterprise']
        st.metric("Customer Acquisition Cost (CAC)", f"₹{ent['CAC']:,.0f}")
        st.metric("Lifetime Value (LTV)", f"₹{ent['LTV']:,.0f}")
        st.metric("LTV:CAC Ratio", f"{ent['LTV_CAC_Ratio']:.1f}x", delta="Target: >3x")
        st.metric("Payback Period", f"{ent['Payback_Months']:.1f} months", delta="Target: <12 months")
        st.metric("Monthly Revenue per Customer", f"₹{ent['Monthly_Revenue']:,.0f}")
        st.metric("Gross Margin", f"{ent['Gross_Margin']:.1%}")
    
    # Visualization
    st.subheader("📊 Unit Economics Comparison")
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=('LTV:CAC Ratio', 'Payback Period (Months)'))
    
    fig.add_trace(go.Bar(x=['SMB', 'Enterprise'], y=[smb['LTV_CAC_Ratio'], ent['LTV_CAC_Ratio']], 
                         marker_color=['#2E86AB', '#A23B72']), row=1, col=1)
    fig.add_hline(y=3, line_dash="dash", line_color="green", row=1, col=1)
    
    fig.add_trace(go.Bar(x=['SMB', 'Enterprise'], y=[smb['Payback_Months'], ent['Payback_Months']],
                         marker_color=['#2E86AB', '#A23B72']), row=1, col=2)
    fig.add_hline(y=12, line_dash="dash", line_color="red", row=1, col=2)
    
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif page == "🌍 Market Sizing":
    st.title("🌍 Market Sizing Analysis")
    
    market_metrics = market_model.get_market_metrics()
    
    # TAM/SAM/SOM Visualization
    st.subheader("Market Opportunity Pyramid")
    
    fig = go.Figure()
    
    fig.add_trace(go.Funnel(
        name = "Market Size",
        y = ["SOM Year 3", "SOM Year 2", "SOM Year 1", "SAM", "TAM"],
        x = [market_metrics['SOM_Year3_Cr'], market_metrics['SOM_Year2_Cr'], 
             market_metrics['SOM_Year1_Cr'], market_metrics['SAM_Cr'], market_metrics['TAM_Cr']],
        textposition = "inside",
        textinfo = "value+percent initial",
        marker = {"color": ["#2E86AB", "#A23B72", "#F18F01", "#1e3c72", "#764ba2"]}
    ))
    
    fig.update_layout(title="TAM/SAM/SOM Analysis (₹ Crore)", height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Market Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Addressable Market (TAM)", f"₹{market_metrics['TAM_Cr']:.0f} Cr")
        st.caption("All Indian businesses needing digital solutions")
    with col2:
        st.metric("Serviceable Addressable (SAM)", f"₹{market_metrics['SAM_Cr']:.0f} Cr")
        st.caption("Businesses reachable via Jio network")
    with col3:
        st.metric("Serviceable Obtainable (SOM)", f"₹{market_metrics['SOM_Year3_Cr']:.0f} Cr")
        st.caption("3-year realistic target")
    
    # Market Growth
    st.subheader("📈 Market Growth Projection")
    years = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
    market_size = [market_metrics['SOM_Year1_Cr'], market_metrics['SOM_Year2_Cr'], 
                   market_metrics['SOM_Year3_Cr'], market_metrics['SOM_Year3_Cr'] * 2,
                   market_metrics['SOM_Year3_Cr'] * 4]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=market_size, mode='lines+markers', 
                             line=dict(width=3, color='#1e3c72'),
                             marker=dict(size=10)))
    fig.update_layout(xaxis_title="Year", yaxis_title="Market Size (₹ Crore)", height=400)
    st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Growth Metrics":
    st.title("📊 Growth Metrics & KPIs")
    
    df = financial_model.generate_projections()
    
    # Calculate metrics
    df['MRR_Growth'] = df['Total_Revenue'].pct_change() * 100
    df['Rule_of_40'] = df['MRR_Growth'].rolling(3).mean() + (df['Operating_Margin'] * 100)
    
    # Metrics Dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Rule of 40", f"{df['Rule_of_40'].iloc[-1]:.0f}", 
                  delta="Benchmark: 40+", delta_color="normal")
    with col2:
        st.metric("Net Revenue Retention", "95%", delta="Above Industry Avg")
    with col3:
        st.metric("Gross Margin", f"{df['Gross_Margin'].iloc[-1]:.1%}", delta="Improving")
    with col4:
        st.metric("CAC Payback (SMB)", "3.2 months", delta="Excellent")
    
    # Rule of 40 Chart
    st.subheader("Rule of 40 Performance")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Month'], y=df['Rule_of_40'], mode='lines',
                             name='Rule of 40', line=dict(color='#1e3c72', width=3)))
    fig.add_hline(y=40, line_dash="dash", line_color="red", 
                  annotation_text="SaaS Benchmark (40)")
    fig.update_layout(xaxis_title="Month", yaxis_title="Score", height=400)
    st.plotly_chart(fig, use_container_width=True)

elif page == "📥 Export Data":
    st.title("📥 Export Financial Data")
    
    st.markdown("""
    <div class="highlight">
    <h3>📊 Download Complete Financial Package</h3>
    <p>Get the full Excel report with all calculations, projections, and analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate all data
    df = financial_model.generate_projections()
    ue_metrics = ue_model.get_all_metrics()
    market_metrics = market_model.get_market_metrics()
    
    # Create Excel file in memory
    from io import BytesIO
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Financial_Projections', index=False)
        
        ue_df = pd.DataFrame(ue_metrics).T
        ue_df.to_excel(writer, sheet_name='Unit_Economics')
        
        market_df = pd.DataFrame([market_metrics])
        market_df.to_excel(writer, sheet_name='Market_Sizing')
        
        summary = pd.DataFrame({
            'Metric': ['Year 3 Revenue (Cr)', 'Year 3 Customers', 'SMB LTV:CAC', 
                      'Enterprise LTV:CAC', 'Gross Margin', 'Rule of 40'],
            'Value': [f"{df['Total_Revenue'].iloc[-1]/1e7:.1f}", 
                     f"{df['Total_Customers'].iloc[-1]:,}",
                     f"{ue_metrics['SMB']['LTV_CAC_Ratio']:.1f}x",
                     f"{ue_metrics['Enterprise']['LTV_CAC_Ratio']:.1f}x",
                     f"{df['Gross_Margin'].iloc[-1]:.1%}",
                     f"{df['Rule_of_40'].iloc[-1]:.0f}"]
        })
        summary.to_excel(writer, sheet_name='Executive_Summary', index=False)
    
    output.seek(0)
    
    st.download_button(
        label="📥 Download Excel Report",
        data=output,
        file_name="Reliance_Slate_Investor_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.markdown("---")
    st.markdown("### 📋 Quick Summary for Investors")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Key Highlights:**")
        st.markdown("""
        - ✅ 3-Year Revenue Target: ₹164 Cr
        - ✅ SMB LTV:CAC: 12.5x (Excellent)
        - ✅ Payback Period: 3.2 months
        - ✅ Rule of 40: 47 (Above Benchmark)
        """)
    with col2:
        st.markdown("**Reliance Advantage:**")
        st.markdown("""
        - 🚀 35% Lower CAC via Jio Network
        - 🚀 20% Lower Churn via Brand Trust
        - 🚀 Access to 450M+ Jio Users
        - 🚀 Existing Retail Distribution
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 1rem;">
    <p>Reliance Slate - Investor Readiness Platform | Confidential - For Authorized Investors Only</p>
    <p>Data as of March 2024 | Projections are forward-looking statements</p>
</div>
""", unsafe_allow_html=True)
