import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Function to calculate normal distribution PDF
def normal_pdf(x, mu, sigma):
    return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

# Set page config
st.set_page_config(
    page_title="Interactive Normal Distribution Visualizer",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: rgb(220, 245, 236);
    }
    .stSlider {
        margin-bottom: 1.5rem;
    }
    .stMarkdown h1 {
        color: #2c3e50;
        font-family: "Montserrat", sans-serif;
        font-weight: 600;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .stMarkdown h3 {
        color: #2c3e50;
        border-bottom: 1px solid #eee;
        padding-bottom: 0.5rem;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("Interactive Normal Distribution Visualizer")

# Main container with controls and plot
with st.container():
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("### Controls")
        mu = st.slider(
            "μ (Mean)",
            min_value=-5.0,
            max_value=5.0,
            value=0.0,
            step=0.1,
            help="Adjust the mean (μ) of the distribution"
        )
        
        sigma = st.slider(
            "σ (Standard Deviation)",
            min_value=0.1,
            max_value=5.0,
            value=1.0,
            step=0.1,
            help="Adjust the standard deviation (σ) of the distribution"
        )
        
        st.markdown(f"**Current parameters:** μ = {mu:.2f}, σ = {sigma:.2f}")
    
    with col2:
        # Generate plot
        x = np.linspace(-10, 10, 1000)
        y = normal_pdf(x, mu, sigma)
        
        fig = go.Figure()
        
        # Add main line
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            name='PDF',
            line=dict(color='blue', width=2)
        ))
        
        # Add shaded regions with proper transparency
        for n, color in zip([3, 2, 1], ['rgba(0,0,255,0.3)', 'rgba(0,128,0,0.4)', 'rgba(255,0,0,0.5)']):
            x_range = np.linspace(mu + n*sigma, mu - n*sigma, 200)
            y_range = normal_pdf(x_range, mu, sigma)
            fig.add_trace(go.Scatter(
                x=np.concatenate([x_range, x_range[::-1]]),
                y=np.concatenate([y_range, np.zeros_like(y_range)[::-1]]),
                fill='tozeroy',
                fillcolor=color,
                line=dict(width=0),
                name=f'±{n}σ ({[68.2, 95.4, 99.7][n-1]}%)'
            ))
        
        max_height = normal_pdf(mu, mu, sigma) * 1.1
        
        # Add sigma labels to x-axis
        annotations = []
        for n in [1, 2, 3]:
            # Positive sigma labels
            annotations.append(dict(
                x=mu + n*sigma,
                y=0,
                xref='x',
                yref='y',
                text=f'+{n}σ',
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=20,
                font=dict(size=15)
            ))
            # Negative sigma labels
            annotations.append(dict(
                x=mu - n*sigma,
                y=0,
                xref='x',
                yref='y',
                text=f'-{n}σ',
                showarrow=True,
                arrowhead=0,
                ax=0,
                ay=20,
                font=dict(size=15)
            ))
        
        fig.update_layout(
            title='Normal Distribution PDF',
            xaxis_title='x',
            yaxis_title='Probability Density',
            xaxis_range=[-10, 10],
            yaxis_range=[0, max(0.5, max_height)],
            showlegend=True,
            annotations=annotations,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Information section
with st.container():
    st.markdown("### About the Normal Distribution")
    st.markdown('''
    The normal (or Gaussian) distribution is a continuous probability distribution characterized by:
    - **μ (mean)**: The center/location of the peak
    - **σ (standard deviation)**: The spread/width of the curve
        
    Key properties:
    - Symmetric about the mean
    - Follows the empirical rule (68-95-99.7 rule):
        - **±1σ (red area)**: ~68.2% of data falls within 1 standard deviation of the mean
        - **±2σ (green area)**: ~95.4% of data falls within 2 standard deviations
        - **±3σ (blue area)**: ~99.7% of data falls within 3 standard deviations
        
    This distribution appears frequently in nature and statistics due to the Central Limit Theorem.
    ''')