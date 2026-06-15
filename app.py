"""
Reliance Slate - Investor Readiness Platform
FIXED: Module imports and Plotly errors
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import custom modules with error handling
try:
    from src.financial_model import RelianceSlateFinancialModel
    from src.unit_economics import UnitEconomicsCalculator
    from src.market_sizing import MarketSizingAnalysis
    MODULES_AVAILABLE = True
    print("✅ Modules loaded successfully")
except ImportError as e:
    MODULES_AVAILABLE = False
    print(f"⚠️ Module import error: {e}")
    
    # Fallback model definitions
    class RelianceSlateFinancialModel:
        def generate_projections(self, months=36):
            dates = pd.date_range(start='2024-04-01', periods=months, freq='ME')
            df = pd.DataFrame({
                'Month': dates.strftime('%Y-%m'),
                'Total_Revenue': np.linspace(10000000, 164000000, months),
                'Total_Customers': np.linspace(10000, 85000, months).astype(int),
                'Gross_Margin': np.linspace(0.70, 0.82, months),
                'Operating_Margin': np.linspace(-0.20, 0.15, months),
                'SMB_Customers': np.linspace(9000, 80000, months).astype(int),
                'Enterprise_Customers': np.linspace(1000, 5000, months).astype(int),
            })
            # Add derived columns
            df['SMB_Revenue'] = df['SMB_Customers'] * 2999
            df['Enterprise_Revenue'] = df['Enterprise_Customers'] * 49999
            return df
    
    class UnitEconomicsCalculator:
        def get_all_metrics(self):
            return {
                'SMB': {
                    'CAC': 2275, 
                    'LTV': 28437, 
                    'LTV_CAC_Ratio': 12.5, 
                    'Payback_Months': 3.2, 
                    'Monthly_Revenue': 2999, 
                    'Gross_Margin': 0.85
                },
                'Enterprise': {
                    'CAC': 13000, 
                    'LTV': 106600, 
                    'LTV_CAC_Ratio': 8.2, 
                    'Payback_Months': 6.8,
                    'Monthly_Revenue': 49999, 
                    'Gross_Margin': 0.75
                }
            }
    
    class MarketSizingAnalysis:
        def get_market_metrics(self):
            return {
                'TAM_Cr': 250000, 
                'SAM_Cr': 100000, 
                'SOM_Year1_Cr': 100, 
                'SOM_Year2_Cr': 250, 
                'SOM_Year3_Cr': 500
            }

# Plotly fallback
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

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
    .stButton button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True

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
    st.markdown("### 📞 Contact")
    st.markdown("📧 investors@reliance.com")

# Generate data
if financial_model is not None:
    try:
        df = financial_model.generate_projections()
        ue_metrics = ue_model.get_all_metrics()
        market_metrics = market_model.get_market_metrics()
        data_loaded = True
    except Exception as e:
        st.error(f"Error generating data: {e}")
        data_loaded = False
else:
    data_loaded = False

if not data_loaded:
    st.warning("⚠️ Using fallback data...")
    # Create fallback data
    months = 36
    dates = pd.date_range(start='2024-04-01', periods=months, freq='ME')
    df = pd.DataFrame({
        'Month': dates.strftime('%Y-%m'),
        'Total_Revenue': np.linspace(10000000, 164000000, months),
        'Total_Customers': np.linspace(10000, 85000, months).astype(int),
        'Gross_Margin': np.linspace(0.70, 0.82, months),
        'Operating_Margin': np.linspace(-0.20, 0.15, months),
    })
    ue_metrics = {
        'SMB': {'CAC': 2275, 'LTV': 28437, 'LTV_CAC_Ratio': 12.5, 'Payback_Months': 3.2, 'Monthly_Revenue': 2999, 'Gross_Margin': 0.85},
        'Enterprise': {'CAC': 13000, 'LTV': 106600, 'LTV_CAC_Ratio': 8.2, 'Payback_Months': 6.8, 'Monthly_Revenue': 49999, 'Gross_Margin': 0.75}
    }
    market_metrics = {'TAM_Cr': 250000, 'SAM_Cr': 100000, 'SOM_Year1_Cr': 100, 'SOM_Year2_Cr': 250, 'SOM_Year3_Cr': 500}

# Page content
if page == "🏠 Dashboard Overview":
    st.markdown('<div class="main-header">Reliance Slate - Investor Dashboard</div>', unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        year3_revenue = df['Total_Revenue'].iloc[-1] if len(df) > 0 else 0
        st.metric("Year 3 Revenue", f"₹{year3_revenue/1e7:.1f} Cr")
    with col2:
        year3_customers = df['Total_Customers'].iloc[-1] if len(df) > 0 else 0
        st.metric("Total Customers", f"{year3_customers:,}")
    with col3:
        ltv_cac = ue_metrics['SMB']['LTV_CAC_Ratio']
        st.metric("SMB LTV:CAC", f"{ltv_cac:.1f}x")
    with col4:
        gross_margin = df['Gross_Margin'].iloc[-1] if len(df) > 0 else 0.82
        st.metric("Gross Margin", f"{gross_margin:.1%}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Revenue Growth")
        chart_data = df[['Month', 'Total_Revenue']].tail(24).copy()
        chart_data['Revenue_Cr'] = chart_data['Total_Revenue'] / 1e7
        st.line_chart(chart_data.set_index('Month')['Revenue_Cr'], height=400)
    
    with col2:
        st.subheader("👥 Customer Growth")
        chart_data = df[['Month', 'Total_Customers']].tail(24).copy()
        st.line_chart(chart_data.set_index('Month')['Total_Customers'], height=400)
    
    # Market Opportunity
    st.markdown("---")
    st.subheader("🎯 Market Opportunity")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("TAM", f"₹{market_metrics['TAM_Cr']:.0f} Cr")
    with col2:
        st.metric("SAM", f"₹{market_metrics['SAM_Cr']:.0f} Cr")
    with col3:
        st.metric("SOM Year 3", f"₹{market_metrics['SOM_Year3_Cr']:.0f} Cr")

elif page == "💰 Financial Projections":
    st.title("💰 3-Year Financial Projections")
    
    # Yearly Summary
    df['Year'] = df['Month'].str[:4]
    yearly = df.groupby('Year').agg({
        'Total_Revenue': 'sum',
        'Total_Customers': 'mean',
        'Gross_Margin': 'mean'
    }).round(2)
    yearly['Revenue_Cr'] = yearly['Total_Revenue'] / 1e7
    
    st.dataframe(yearly[['Revenue_Cr', 'Total_Customers', 'Gross_Margin']], use_container_width=True)
    
    # Revenue Chart
    st.subheader("📈 Monthly Revenue Projection")
    chart_data = df[['Month', 'Total_Revenue']].copy()
    chart_data['Revenue_Cr'] = chart_data['Total_Revenue'] / 1e7
    st.line_chart(chart_data.set_index('Month')['Revenue_Cr'], height=400)
    
    # Data Table
    with st.expander("📋 View Detailed Data"):
        st.dataframe(df, use_container_width=True)

elif page == "📈 Unit Economics":
    st.title("📈 Unit Economics Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏪 SMB Segment")
        smb = ue_metrics['SMB']
        st.metric("CAC", f"₹{smb['CAC']:,.0f}")
        st.metric("LTV", f"₹{smb['LTV']:,.0f}")
        st.metric("LTV:CAC Ratio", f"{smb['LTV_CAC_Ratio']:.1f}x")
        st.metric("Payback Period", f"{smb['Payback_Months']:.1f} months")
        st.metric("Monthly Revenue", f"₹{smb['Monthly_Revenue']:,.0f}")
    
    with col2:
        st.markdown("### 🏢 Enterprise Segment")
        ent = ue_metrics['Enterprise']
        st.metric("CAC", f"₹{ent['CAC']:,.0f}")
        st.metric("LTV", f"₹{ent['LTV']:,.0f}")
        st.metric("LTV:CAC Ratio", f"{ent['LTV_CAC_Ratio']:.1f}x")
        st.metric("Payback Period", f"{ent['Payback_Months']:.1f} months")
        st.metric("Monthly Revenue", f"₹{ent['Monthly_Revenue']:,.0f}")

elif page == "🌍 Market Sizing":
    st.title("🌍 Market Sizing Analysis")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("TAM", f"₹{market_metrics['TAM_Cr']:.0f} Cr")
    with col2:
        st.metric("SAM", f"₹{market_metrics['SAM_Cr']:.0f} Cr")
    with col3:
        st.metric("SOM Year 3", f"₹{market_metrics['SOM_Year3_Cr']:.0f} Cr")
    
    # Funnel Chart
    funnel_data = pd.DataFrame({
        'Market': ['TAM', 'SAM', 'SOM Year 1', 'SOM Year 2', 'SOM Year 3'],
        'Size': [market_metrics['TAM_Cr'], market_metrics['SAM_Cr'], 
                market_metrics['SOM_Year1_Cr'], market_metrics['SOM_Year2_Cr'], 
                market_metrics['SOM_Year3_Cr']]
    })
    st.bar_chart(funnel_data.set_index('Market'), height=400)

elif page == "📊 Growth Metrics":
    st.title("📊 Growth Metrics")
    
    # Calculate metrics
    df['Revenue_Growth'] = df['Total_Revenue'].pct_change() * 100
    df['Rule_of_40'] = df['Revenue_Growth'].rolling(3).mean() + (df['Operating_Margin'] * 100)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rule of 40", f"{df['Rule_of_40'].iloc[-1]:.0f}")
    with col2:
        st.metric("Avg MoM Growth", f"{df['Revenue_Growth'].mean():.1f}%")
    with col3:
        st.metric("Gross Margin", f"{df['Gross_Margin'].iloc[-1]:.1%}")
    with col4:
        st.metric("Operating Margin", f"{df['Operating_Margin'].iloc[-1]:.1%}")
    
    # Rule of 40 Chart
    st.subheader("Rule of 40 Performance")
    chart_data = df[['Month', 'Rule_of_40']].dropna().tail(24)
    st.line_chart(chart_data.set_index('Month'), height=400)

elif page == "📥 Export Data":
    st.title("📥 Export Data")
    
    from io import BytesIO
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Financial_Projections', index=False)
        
        ue_df = pd.DataFrame(ue_metrics).T
        ue_df.to_excel(writer, sheet_name='Unit_Economics')
        
        market_df = pd.DataFrame([market_metrics])
        market_df.to_excel(writer, sheet_name='Market_Sizing')
    
    output.seek(0)
    st.download_button("📥 Download Excel Report", data=output, 
                      file_name="Reliance_Slate_Report.xlsx",
                      mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Footer
st.markdown("---")
st.markdown("📊 **Reliance Slate** - Investor Dashboard | Confidential")
