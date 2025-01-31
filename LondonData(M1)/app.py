import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from weatherAnalysis import load_data, analyze_monthly_temperature_trend, analyze_temp_cloud_correlation, analyze_extreme_weather

# Streamlit app setup
st.title('London Weather Data Analysis')

# File uploader for user to upload the dataset
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    # Load the data
    df = load_data(uploaded_file)
    
    # Display the first few rows of the dataframe
    st.subheader('Data Preview')
    st.write(df.head())
    
    # Perform analyses if the dataframe is not empty
    if not df.empty:
        # Monthly temperature trend analysis
        st.subheader('Average Monthly Temperature Trend')
        fig_temp, monthly_temps = analyze_monthly_temperature_trend(df)  # Unpack both return values
        
        # Display the matplotlib figure
        st.pyplot(fig_temp)
        
        # Temperature and cloud cover correlation analysis
        st.subheader('Temperature vs Cloud Cover Correlation')
        fig_corr, correlation_stats = analyze_temp_cloud_correlation(df)  # Unpack both return values
        
        # Display correlation statistics
        st.write(f"Correlation Coefficient: {correlation_stats['correlation']:.3f}")
        st.write(f"Correlation Strength: {correlation_stats['correlation_strength']}")
        st.write(f"P-value: {correlation_stats['p_value']:.3f}")
        
        # Display the correlation figure
        st.pyplot(fig_corr)
        
        # Extreme weather analysis
        st.subheader('Monthly Weather Statistics')
        extreme_weather = analyze_extreme_weather(df)
        st.write(extreme_weather)
    else:
        # Display an error message if the DataFrame is empty
        st.error("The DataFrame is empty after cleaning. Please check the data and cleaning steps.")
else:
    # Inform the user to upload a CSV file
    st.info("Please upload a CSV file to proceed with the analysis.")
