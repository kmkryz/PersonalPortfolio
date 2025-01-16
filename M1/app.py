import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from weather_analysis import load_data, analyze_monthly_temperature_trend, analyze_temp_cloud_correlation, analyze_extreme_weather

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
        monthly_temps = analyze_monthly_temperature_trend(df)
        
        # Use Streamlit's line_chart with explicit columns
        st.line_chart(monthly_temps.set_index('date')['mean_temp'])
        
        # Temperature and cloud cover correlation analysis
        st.subheader('Temperature vs Cloud Cover Correlation')
        correlation = analyze_temp_cloud_correlation(df)
        st.write(f"Correlation: {correlation:.2f}")
        
        # Display the correlation heatmap
        st.image('correlation_heatmap.png', caption='Correlation Heatmap')
        
        # Extreme weather analysis
        st.subheader('Monthly Weather Statistics')
        extreme_weather = analyze_extreme_weather(df)
        st.write(extreme_weather)
    else:
        st.error("The DataFrame is empty after cleaning. Please check the data and cleaning steps.")
else:
    st.info("Please upload a CSV file to proceed with the analysis.")
