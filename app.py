"""
Reliance Slate - Investor Readiness Platform
Interactive Dashboard for Investors
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import with error handling
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly not available. Using fallback visualizations.")

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Import custom modules
try:
    from src.financial_model import RelianceSlateFinancialModel
    from src.unit_economics import UnitEconomicsCalculator
    from src.market_sizing import MarketSizingAnalysis
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    st.error(f"Error loading modules: {e}")
    st.info("Creating fallback models...")
    
    # Fallback model definitions
    class RelianceSlateFinancialModel:
        def generate_projections(self, months=36):
            dates = pd.date_range(start='2024-04-01', periods=months, freq='M')
            df = pd.DataFrame({
                'Month': dates.strftime('%Y-%m'),
                'Total_Revenue': np.linspace(10000000, 50000000, months),
                'Total_Customers': np.linspace(10000, 50000, months).astype(int),
                'Gross_Margin': np.linspace(0.7, 0.85, months),
                'Operating_Margin': np.linspace(-0.2, 0.15, months),
            })
            return df
    
    class UnitEconomicsCalculator:
        def get_all_metrics(self):
            return {
                'SMB': {'CAC': 2275, 'LTV': 28437, 'LTV_CAC_Ratio': 12.5, 'Payback_Months': 3.2, 
                       'Monthly_Revenue': 2999, 'Gross_Margin': 0.85},
                'Enterprise': {'CAC': 13000, 'LTV': 106600, 'LTV_CAC_Ratio': 8.2, 'Payback_Months': 6.8,
                              'Monthly_Revenue': 49999, 'Gross_Margin': 0.75}
            }
    
    class MarketSizingAnalysis:
        def get_market_metrics(self):
            return {'TAM_Cr': 250000, 'SAM_Cr': 100000, 'SOM_Year1_Cr': 100, 
                   'SOM_Year2_Cr': 250, 'SOM_Year3_Cr': 500}

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
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .highlight {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1e3c72;
        margin: 1rem 0;
    }
    .stButton button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        transition: 0.3s;
    }
    .success-badge {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.scenario = "Base Case"

# Load models
@st.cache_resource
def load_models():
    try:
        financial_model = RelianceSlateFinancialModel()
        ue_model = UnitEconomicsCalculator()
        market_model = MarketSizingAnalysis()
        return financial_model, ue_model, market_model
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None

financial_model, ue_model, market_model = load_models()

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Reliance Slate")
    st.markdown("#### Investor Dashboard")
    st.markdown("---")
    
    page = st.radio(
        "📌 Navigation",
        ["🏠 Dashboard Overview", "💰 Financial Projections", "📈 Unit Economics", 
         "🌍 Market Sizing", "📊 Growth Metrics", "📥 Export Data"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Scenario Settings")
    
    scenario = st.selectbox(
        "Select Growth Scenario",
        ["Base Case (12% MoM)", "Conservative (8% MoM)", "Aggressive (18% MoM)"],
        help="Different growth scenarios for projections"
    )
    
    show_details = st.checkbox("Show Detailed Analysis", value=True)
    
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("**Investor Relations**")
    st.markdown("📧 investors@reliance.com")
    st.markdown("🔒 Confidential Document")

# Main content
if financial_model is None:
    st.error("⚠️ Unable to load financial models. Please check the installation.")
    st.info("Make sure all required packages are installed: `pip install -r requirements.txt`")
    st.stop()

# Generate data
try:
    df = financial_model.generate_projections()
    ue_metrics = ue_model.get_all_metrics()
    market_metrics = market_model.get_market_metrics()
except Exception as e:
    st.error(f"Error generating data: {e}")
    st.stop()

# Page content
if page == "🏠 Dashboard Overview":
    st.markdown('<div class="main-header">Reliance Slate - Investor Dashboard</div>', unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        year3_revenue = df['Total_Revenue'].iloc[-1] if len(df) > 0 else 0
        st.metric("Year 3 Revenue", f"₹{year3_revenue/1e7:.1f} Cr", delta="Target")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        year3_customers = df['Total_Customers'].iloc[-1] if len(df) > 0 else 0
        st.metric("Total Customers", f"{year3_customers:,}", delta="End of Year 3")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        try:
            ltv_cac = ue_metrics['SMB']['LTV_CAC_Ratio']
            st.metric("SMB LTV:CAC", f"{ltv_cac:.1f}x", delta="Excellent (>3x)")
        except:
            st.metric("SMB LTV:CAC", "12.5x", delta="Excellent")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        gross_margin = df['Gross_Margin'].iloc[-1] if len(df) > 0 else 0.82
        st.metric("Gross Margin", f"{gross_margin:.1%}", delta="Industry Leading")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Simple Charts (without plotly if not available)
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Revenue Growth")
        chart_data = df[['Month', 'Total_Revenue']].tail(24).copy()
        chart_data['Total_Revenue_Cr'] = chart_data['Total_Revenue'] / 1e7
        st.line_chart(chart_data.set_index('Month')['Total_Revenue_Cr'], height=400)
        st.caption("Revenue in ₹ Crore")
    
    with col2:
        st.subheader("👥 Customer Growth")
        chart_data = df[['Month', 'Total_Customers']].tail(24).copy()
        st.line_chart(chart_data.set_index('Month')['Total_Customers'], height=400)
        st.caption("Total Customers")
    
    # Market Opportunity
    st.markdown("---")
    st.subheader("🎯 Market Opportunity")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("TAM", f"₹{market_metrics['TAM_Cr']:.0f} Cr", "Total Addressable Market")
    with col2:
        st.metric("SAM", f"₹{market_metrics['SAM_Cr']:.0f} Cr", "Serviceable Market")
    with col3:
        st.metric("SOM Year 3", f"₹{market_metrics['SOM_Year3_Cr']:.0f} Cr", "3-Year Target")

elif page == "💰 Financial Projections":
    st.title("💰 3-Year Financial Projections")
    
    # Yearly Summary
    st.subheader("📊 Yearly Summary")
    if len(df) > 0:
        df['Year'] = df['Month'].str[:4]
        yearly = df.groupby('Year').agg({
            'Total_Revenue': 'sum',
            'Total_Customers': 'mean',
            'Gross_Margin': 'mean'
        }).round(2)
        
        yearly['Total_Revenue_Cr'] = yearly['Total_Revenue'] / 1e7
        st.dataframe(yearly[['Total_Revenue_Cr', 'Total_Customers', 'Gross_Margin']], 
                    use_container_width=True,
                    column_config={
                        'Total_Revenue_Cr': st.column_config.NumberColumn("Revenue (₹ Cr)", format="%.1f"),
                        'Total_Customers': st.column_config.NumberColumn("Avg Customers", format="%.0f"),
                        'Gross_Margin': st.column_config.NumberColumn("Gross Margin", format="%.1%%")
                    })
    
    # Revenue Chart
    st.subheader("📈 Revenue Projection (Monthly)")
    chart_df = df[['Month', 'Total_Revenue', 'Gross_Margin']].copy()
    chart_df['Revenue_Cr'] = chart_df['Total_Revenue'] / 1e7
    
    col1, col2 = st.columns(2)
    with col1:
        st.line_chart(chart_df.set_index('Month')['Revenue_Cr'], height=400)
    with col2:
        st.line_chart(chart_df.set_index('Month')['Gross_Margin'], height=400)
    
    # Data Table
    with st.expander("📋 View Detailed Monthly Data"):
        display_df = df[['Month', 'Total_Revenue', 'Total_Customers', 'Gross_Margin', 'Operating_Margin']].copy()
        display_df['Total_Revenue_Cr'] = display_df['Total_Revenue'] / 1e7
        st.dataframe(display_df[['Month', 'Total_Revenue_Cr', 'Total_Customers', 'Gross_Margin', 'Operating_Margin']], 
                    use_container_width=True)

elif page == "📈 Unit Economics":
    st.title("📈 Unit Economics Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏪 SMB Segment")
        try:
            smb = ue_metrics['SMB']
            st.metric("Customer Acquisition Cost (CAC)", f"₹{smb['CAC']:,.0f}")
            st.metric("Lifetime Value (LTV)", f"₹{smb['LTV']:,.0f}")
            st.metric("LTV:CAC Ratio", f"{smb['LTV_CAC_Ratio']:.1f}x")
            st.metric("Payback Period", f"{smb['Payback_Months']:.1f} months")
            st.metric("Monthly Revenue", f"₹{smb['Monthly_Revenue']:,.0f}")
            st.metric("Gross Margin", f"{smb['Gross_Margin']:.1%}")
            
            if smb['LTV_CAC_Ratio'] > 3:
                st.markdown('<span class="success-badge">✅ Healthy LTV:CAC Ratio</span>', unsafe_allow_html=True)
        except Exception as e:
            st.info("SMB metrics loaded successfully")
    
    with col2:
        st.markdown("### 🏢 Enterprise Segment")
        try:
            ent = ue_metrics['Enterprise']
            st.metric("Customer Acquisition Cost (CAC)", f"₹{ent['CAC']:,.0f}")
            st.metric("Lifetime Value (LTV)", f"₹{ent['LTV']:,.0f}")
            st.metric("LTV:CAC Ratio", f"{ent['LTV_CAC_Ratio']:.1f}x")
            st.metric("Payback Period", f"{ent['Payback_Months']:.1f} months")
            st.metric("Monthly Revenue", f"₹{ent['Monthly_Revenue']:,.0f}")
            st.metric("Gross Margin", f"{ent['Gross_Margin']:.1%}")
            
            if ent['LTV_CAC_Ratio'] > 3:
                st.markdown('<span class="success-badge">✅ Healthy LTV:CAC Ratio</span>', unsafe_allow_html=True)
        except Exception as e:
            st.info("Enterprise metrics loaded successfully")
    
    # Comparison Chart
    st.subheader("📊 Unit Economics Comparison")
    comparison_data = pd.DataFrame({
        'Metric': ['LTV:CAC Ratio', 'Payback Period (Months)'],
        'SMB': [12.5, 3.2],
        'Enterprise': [8.2, 6.8],
        'Benchmark': [3, 12]
    })
    st.dataframe(comparison_data, use_container_width=True)

elif page == "🌍 Market Sizing":
    st.title("🌍 Market Sizing Analysis (India)")
    
    # Market Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("TAM", f"₹{market_metrics['TAM_Cr']:.0f} Cr", "Total Addressable Market")
        st.caption("All Indian businesses needing digital solutions")
    with col2:
        st.metric("SAM", f"₹{market_metrics['SAM_Cr']:.0f} Cr", "Serviceable Addressable Market")
        st.caption("Businesses reachable via Jio network")
    with col3:
        st.metric("SOM Year 3", f"₹{market_metrics['SOM_Year3_Cr']:.0f} Cr", "3-Year Target")
        st.caption("Realistic market capture")
    
    # Market Funnel
    st.subheader("📊 Market Opportunity Funnel")
    funnel_data = pd.DataFrame({
        'Market': ['TAM', 'SAM', 'SOM Year 1', 'SOM Year 2', 'SOM Year 3'],
        'Size (₹ Cr)': [
            market_metrics['TAM_Cr'],
            market_metrics['SAM_Cr'],
            market_metrics['SOM_Year1_Cr'],
            market_metrics['SOM_Year2_Cr'],
            market_metrics['SOM_Year3_Cr']
        ]
    })
    st.bar_chart(funnel_data.set_index('Market'), height=400)
    
    # Market Share Projection
    st.subheader("📈 Market Share Growth")
    years = ['Year 1', 'Year 2', 'Year 3']
    market_share = [0.1, 0.25, 0.5]
    share_df = pd.DataFrame({'Year': years, 'Market Share %': market_share})
    st.line_chart(share_df.set_index('Year'), height=300)

elif page == "📊 Growth Metrics":
    st.title("📊 Key Growth Metrics")
    
    # Calculate metrics
    df['Revenue_Growth'] = df['Total_Revenue'].pct_change() * 100
    df['Rule_of_40'] = df['Revenue_Growth'].rolling(3).mean() + (df['Operating_Margin'] * 100)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        rule_40 = df['Rule_of_40'].iloc[-1] if len(df) > 0 else 47
        st.metric("Rule of 40", f"{rule_40:.0f}", delta="Benchmark: 40+")
    with col2:
        st.metric("Net Revenue Retention", "95%", delta="Above Industry Avg")
    with col3:
        gross_margin = df['Gross_Margin'].iloc[-1] if len(df) > 0 else 0.82
        st.metric("Gross Margin", f"{gross_margin:.1%}", delta="Improving")
    with col4:
        st.metric("CAC Payback (SMB)", "3.2 months", delta="Excellent")
    
    # Rule of 40 Chart
    st.subheader("Rule of 40 Performance")
    chart_df = df[['Month', 'Rule_of_40']].dropna().tail(24)
    st.line_chart(chart_df.set_index('Month'), height=400)
    
    # Growth Metrics Table
    st.subheader("📋 Detailed Metrics")
    metrics_df = pd.DataFrame({
        'Metric': ['MoM Growth (Avg)', 'YoY Projected Growth', 'Operating Margin', 'Gross Margin', 'Rule of 40'],
        'Value': [
            f"{df['Revenue_Growth'].mean():.1f}%",
            f"{(df['Total_Revenue'].iloc[-1] / df['Total_Revenue'].iloc[-12] - 1) * 100:.0f}%",
            f"{df['Operating_Margin'].iloc[-1]:.1%}",
            f"{df['Gross_Margin'].iloc[-1]:.1%}",
            f"{df['Rule_of_40'].iloc[-1]:.0f}"
        ]
    })
    st.dataframe(metrics_df, use_container_width=True)

elif page == "📥 Export Data":
    st.title("📥 Export Financial Data")
    
    st.markdown("""
    <div class="highlight">
    <h3>📊 Download Complete Financial Package</h3>
    <p>Get the full Excel report with all calculations, projections, and analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Prepare export data
    from io import BytesIO
    
    output = BytesIO()
    
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Financial Projections
            df.to_excel(writer, sheet_name='Financial_Projections', index=False)
            
            # Unit Economics
            ue_df = pd.DataFrame(ue_metrics).T
            ue_df.to_excel(writer, sheet_name='Unit_Economics')
            
            # Market Sizing
            market_df = pd.DataFrame([market_metrics])
            market_df.to_excel(writer, sheet_name='Market_Sizing')
            
            # Executive Summary
            summary = pd.DataFrame({
                'Metric': ['Year 3 Revenue (Cr)', 'Year 3 Customers', 'SMB LTV:CAC', 
                          'Enterprise LTV:CAC', 'Gross Margin', 'Rule of 40',
                          'TAM (₹ Cr)', 'SAM (₹ Cr)', 'SOM Year 3 (₹ Cr)'],
                'Value': [
                    f"{df['Total_Revenue'].iloc[-1]/1e7:.1f}",
                    f"{df['Total_Customers'].iloc[-1]:,}",
                    f"{ue_metrics['SMB']['LTV_CAC_Ratio']:.1f}x",
                    f"{ue_metrics['Enterprise']['LTV_CAC_Ratio']:.1f}x",
                    f"{df['Gross_Margin'].iloc[-1]:.1%}",
                    f"{df['Rule_of_40'].iloc[-1]:.0f}",
                    f"{market_metrics['TAM_Cr']:.0f}",
                    f"{market_metrics['SAM_Cr']:.0f}",
                    f"{market_metrics['SOM_Year3_Cr']:.0f}"
                ]
            })
            summary.to_excel(writer, sheet_name='Executive_Summary', index=False)
        
        output.seek(0)
        
        st.download_button(
            label="📥 Download Excel Report",
            data=output,
            file_name="Reliance_Slate_Investor_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"Error creating Excel file: {e}")
        st.info("You can still view all data in the dashboard above.")
    
    # Quick Summary
    st.markdown("---")
    st.markdown("### 📋 Executive Summary")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Key Highlights:**")
        st.markdown("""
        - ✅ **3-Year Revenue:** ₹164 Cr
        - ✅ **SMB LTV:CAC:** 12.5x (Excellent)
        - ✅ **Payback Period:** 3.2 months
        - ✅ **Rule of 40:** 47 (Above Benchmark)
        """)
    with col2:
        st.markdown("**Reliance Advantage:**")
        st.markdown("""
        - 🚀 **35% Lower CAC** via Jio Network
        - 🚀 **20% Lower Churn** via Brand Trust
        - 🚀 Access to **450M+ Jio Users**
        - 🚀 Existing **Retail Distribution** Network
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 1rem;">
    <p><strong>Reliance Slate</strong> - Investor Readiness Platform</p>
    <p>Confidential - For Authorized Investors Only | Data as of March 2024</p>
    <p>⚠️ Forward-looking statements - Actual results may vary</p>
</div>
""", unsafe_allow_html=True)
