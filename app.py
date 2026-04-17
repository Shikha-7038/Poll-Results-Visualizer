"""
Streamlit Dashboard for Poll Results Visualizer
Interactive web application to explore poll results
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Poll Results Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with NO red colors in sidebar
st.markdown("""
    <style>
    /* Hide Streamlit default header */
    header {
        visibility: hidden;
    }
    
    /* Main container background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Sidebar styling - Dark blue theme with NO red */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: #1E293B !important;
        padding-top: 2rem !important;
    }
    
    /* Remove default red from sidebar headers */
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #60A5FA !important;
    }
    
    /* Sidebar text styling - White for contrast */
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label {
        color: #F1F5F9 !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar headers (Filter Results) - Blue instead of red */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #60A5FA !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar expander headers */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        color: #F1F5F9 !important;
        background-color: #334155 !important;
    }
    
    /* Sidebar selectbox and multiselect */
    [data-testid="stSidebar"] .stSelectbox > div,
    [data-testid="stSidebar"] .stMultiSelect > div {
        background-color: #334155;
        border: 1px solid #475569;
        border-radius: 8px;
        color: #F1F5F9;
    }
    
    /* Sidebar selectbox text */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span,
    [data-testid="stSidebar"] .stMultiSelect span {
        color: #F1F5F9 !important;
    }
    
    /* Sidebar date input */
    [data-testid="stSidebar"] .stDateInput > div {
        background-color: #334155;
        border: 1px solid #475569;
        border-radius: 8px;
    }
    
    /* Sidebar date input text */
    [data-testid="stSidebar"] .stDateInput input {
        color: #F1F5F9 !important;
    }
    
    /* Sidebar checkbox */
    [data-testid="stSidebar"] .stCheckbox label {
        color: #F1F5F9 !important;
    }
    
    /* Sidebar info box - Blue accent instead of red */
    [data-testid="stSidebar"] .stAlert {
        background-color: #334155;
        border-left: 4px solid #3B82F6;
        color: #F1F5F9;
    }
    
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: #334155;
    }
    
    /* Remove any red from multiselect tags */
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
        background-color: #3B82F6 !important;
        color: white !important;
    }
    
    /* Remove red from selectbox dropdown */
    [data-testid="stSidebar"] .stSelectbox div[role="listbox"] {
        background-color: #334155 !important;
    }
    
    /* Main content header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1E293B;
        margin-top: 1rem;
        margin-bottom: 1rem;
        padding-left: 0.8rem;
        border-left: 4px solid #3B82F6;
    }
    
    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #64748B;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E293B;
    }
    
    /* Chart container */
    .chart-container {
        background: #FFFFFF;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid #E2E8F0;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3B82F6;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #2563EB;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59,130,246,0.3);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #F8FAFC;
        border-radius: 8px;
        font-weight: 600;
        color: #1E293B;
        border: 1px solid #E2E8F0;
    }
    
    /* Dataframe styling */
    .dataframe {
        background-color: #FFFFFF !important;
    }
    
    /* Hide deploy button */
    .stDeployButton {
        display: none;
    }
    
    /* Remove any default red from Streamlit elements */
    .st-emotion-cache-1v0mbdj {
        background-color: #1E293B !important;
    }
    
    /* Remove red from any other Streamlit components */
    .st-emotion-cache-12oz5g7 {
        background-color: #1E293B !important;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load cleaned poll data"""
    try:
        df = pd.read_csv('data/cleaned_poll_data.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Please run main.py first to generate data!")
        return None

def main():
    # Header
    st.markdown('<div class="main-header">📊 Poll Results Visualizer</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data
    df = load_data()
    
    if df is None:
        st.stop()
    
    # Sidebar filters with NO red - using blue instead
    st.sidebar.markdown("## 🔍 Filter Results")
    st.sidebar.markdown("---")
    
    # Date filter
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        min_date = df['date'].min()
        max_date = df['date'].max()
        date_range = st.sidebar.date_input(
            "📅 Date Range",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
        if len(date_range) == 2:
            mask = (df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))
            df = df[mask]
    
    # Region filter
    if 'region' in df.columns:
        regions = st.sidebar.multiselect(
            "🌍 Select Regions",
            options=df['region'].unique(),
            default=list(df['region'].unique())
        )
        if regions:
            df = df[df['region'].isin(regions)]
    
    # Age group filter
    if 'age_group' in df.columns:
        age_groups = st.sidebar.multiselect(
            "👥 Select Age Groups",
            options=df['age_group'].unique(),
            default=list(df['age_group'].unique())
        )
        if age_groups:
            df = df[df['age_group'].isin(age_groups)]
    
    # Gender filter
    if 'gender' in df.columns:
        genders = st.sidebar.multiselect(
            "⚥ Select Genders",
            options=df['gender'].unique(),
            default=list(df['gender'].unique())
        )
        if genders:
            df = df[df['gender'].isin(genders)]
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip:** Use filters to explore specific segments of your data!")
    
    # Display metrics
    st.markdown('<div class="sub-header">📈 Key Metrics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📊 Total Responses</div>
            <div class="metric-value">{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if 'satisfaction_rating' in df.columns:
            avg_sat = df['satisfaction_rating'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">⭐ Avg Satisfaction</div>
                <div class="metric-value">{avg_sat:.2f}/5</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if 'preferred_tool' in df.columns and len(df) > 0:
            top_tool = df['preferred_tool'].mode()[0]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🏆 Most Popular Tool</div>
                <div class="metric-value">{top_tool}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if 'would_recommend' in df.columns and len(df) > 0:
            promoters = df[df['would_recommend'].isin(['Definitely Yes', 'Probably Yes'])].shape[0]
            promoter_rate = (promoters / len(df)) * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">👍 Promoter Rate</div>
                <div class="metric-value">{promoter_rate:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container"><p style="font-weight: bold; font-size: 1.1rem; color: #1E293B;">🏆 Tool Preferences</p>', unsafe_allow_html=True)
        
        if 'preferred_tool' in df.columns and len(df) > 0:
            tool_counts = df['preferred_tool'].value_counts()
            
            # Create bar chart with professional colors
            fig, ax = plt.subplots(figsize=(7, 4.5))
            fig.patch.set_facecolor('#FFFFFF')
            colors = ['#3B82F6', '#14B8A6', '#F59E0B', '#8B5CF6', '#EC4899', '#94A3B8']
            bars = ax.bar(range(len(tool_counts)), tool_counts.values, color=colors[:len(tool_counts)], edgecolor='#E2E8F0', linewidth=1)
            ax.set_xticks(range(len(tool_counts.index)))
            ax.set_xticklabels(tool_counts.index, rotation=45, ha='right', fontsize=9)
            ax.set_ylabel('Number of Votes', fontsize=10, fontweight='bold')
            ax.set_title('Tool Preference Distribution', fontsize=12, fontweight='bold', pad=10)
            ax.set_facecolor('#FFFFFF')
            ax.grid(axis='y', alpha=0.15)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Add value labels
            for bar, count in zip(bars, tool_counts.values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                       str(count), ha='center', va='bottom', fontsize=9, fontweight='bold')
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container"><p style="font-weight: bold; font-size: 1.1rem; color: #1E293B;">⭐ Satisfaction Distribution</p>', unsafe_allow_html=True)
        
        if 'satisfaction_rating' in df.columns and len(df) > 0:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            fig.patch.set_facecolor('#FFFFFF')
            counts, bins, patches = ax.hist(df['satisfaction_rating'], bins=5, edgecolor='#E2E8F0', 
                                           color='#3B82F6', alpha=0.7, rwidth=0.8)
            ax.set_xlabel('Satisfaction Rating', fontsize=10, fontweight='bold')
            ax.set_ylabel('Frequency', fontsize=10, fontweight='bold')
            ax.set_title('Satisfaction Rating Distribution', fontsize=12, fontweight='bold', pad=10)
            ax.set_xticks([1, 2, 3, 4, 5])
            ax.set_xticklabels(['1', '2', '3', '4', '5'])
            ax.set_facecolor('#FFFFFF')
            ax.grid(axis='y', alpha=0.15)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Add count labels
            for i, count in enumerate(counts):
                ax.text(bins[i] + 0.5, count + 0.5, str(int(count)), ha='center', va='bottom', fontweight='bold')
            
            # Add mean line
            mean_rating = df['satisfaction_rating'].mean()
            ax.axvline(mean_rating, color='#F59E0B', linestyle='--', linewidth=2, label=f'Mean: {mean_rating:.2f}')
            ax.legend()
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Second row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container"><p style="font-weight: bold; font-size: 1.1rem; color: #1E293B;">🌍 Regional Preferences</p>', unsafe_allow_html=True)
        
        if 'region' in df.columns and 'preferred_tool' in df.columns and len(df) > 0:
            region_tool = pd.crosstab(df['region'], df['preferred_tool'], normalize='index') * 100
            
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('#FFFFFF')
            region_tool.plot(kind='bar', stacked=True, ax=ax, colormap='Set2', edgecolor='#E2E8F0', linewidth=0.5)
            ax.set_xlabel('Region', fontsize=10, fontweight='bold')
            ax.set_ylabel('Percentage (%)', fontsize=10, fontweight='bold')
            ax.set_title('Tool Preferences by Region', fontsize=12, fontweight='bold', pad=10)
            ax.legend(title='Tool', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
            ax.set_facecolor('#FFFFFF')
            ax.grid(axis='y', alpha=0.15)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container"><p style="font-weight: bold; font-size: 1.1rem; color: #1E293B;">👥 Age Group Analysis</p>', unsafe_allow_html=True)
        
        if 'age_group' in df.columns and 'preferred_tool' in df.columns and len(df) > 0:
            age_tool = pd.crosstab(df['age_group'], df['preferred_tool'], normalize='index') * 100
            
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_facecolor('#FFFFFF')
            age_tool.plot(kind='bar', stacked=True, ax=ax, colormap='Set3', edgecolor='#E2E8F0', linewidth=0.5)
            ax.set_xlabel('Age Group', fontsize=10, fontweight='bold')
            ax.set_ylabel('Percentage (%)', fontsize=10, fontweight='bold')
            ax.set_title('Tool Preferences by Age Group', fontsize=12, fontweight='bold', pad=10)
            ax.legend(title='Tool', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
            ax.set_facecolor('#FFFFFF')
            ax.grid(axis='y', alpha=0.15)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Word cloud section
    st.markdown('<div class="chart-container"><p style="font-weight: bold; font-size: 1.1rem; color: #1E293B;">💬 Feedback Word Cloud</p>', unsafe_allow_html=True)
    
    if 'feedback' in df.columns and len(df) > 0:
        text = ' '.join(df['feedback'].dropna().astype(str))
        if len(text) > 100:
            wordcloud = WordCloud(width=1000, height=500, background_color='white', 
                                 colormap='viridis', max_words=100, 
                                 contour_width=1, contour_color='#3B82F6').generate(text)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor('#FFFFFF')
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title('Most Common Words in Customer Feedback', fontsize=12, fontweight='bold', pad=10)
            st.pyplot(fig)
            plt.close()
        else:
            st.info("💬 Not enough feedback text to generate word cloud. Add more responses!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Raw data section
    st.markdown("---")
    st.markdown('<div class="sub-header">📋 Raw Data Preview</div>', unsafe_allow_html=True)
    
    if st.checkbox("Show raw data"):
        st.dataframe(df.head(100), use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download data as CSV",
            data=csv,
            file_name="filtered_poll_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()