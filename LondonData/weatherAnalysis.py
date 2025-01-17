import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import scipy.stats as stats

def load_data(file):
    try:
        # Load the data with low_memory=False to handle mixed types
        df = pd.read_csv(file, low_memory=False)
        
        # Convert 'date' column to datetime with the correct format
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')
        
        # Convert 'mean_temp' column to numeric, coercing errors to NaN
        df['mean_temp'] = pd.to_numeric(df['mean_temp'], errors='coerce')
        
        # Drop rows with NaN values in 'mean_temp' or 'date' columns
        df.dropna(subset=['mean_temp', 'date'], inplace=True)
        
        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def analyze_monthly_temperature_trend(df):
    # Calculate monthly average temperatures
    monthly_temps = df.groupby(df['date'].dt.to_period('M'))['mean_temp'].mean().reset_index()
    monthly_temps['date'] = monthly_temps['date'].dt.to_timestamp()
    
    # Create figure with better styling for web display
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Overall trend
    sns.lineplot(data=monthly_temps, x='date', y='mean_temp', marker='o', ax=ax1)
    ax1.set_title('Average Monthly Temperature Trend in London', pad=20)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Mean Temperature (°C)')
    ax1.grid(True)
    
    # Plot 2: Seasonal pattern
    seasonal_pattern = df.groupby(df['date'].dt.month)['mean_temp'].mean()
    sns.barplot(x=seasonal_pattern.index, y=seasonal_pattern.values, ax=ax2)
    ax2.set_title('Average Temperature by Month (Seasonal Pattern)', pad=20)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Mean Temperature (°C)')
    ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    plt.tight_layout()
    return fig, monthly_temps

def analyze_temp_cloud_correlation(df):
    # Calculate correlation between mean temperature and cloud cover
    correlation = df['mean_temp'].corr(df['cloud_cover'])
    
    # Create figure with multiple plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Scatter plot with regression line
    sns.regplot(x='mean_temp', y='cloud_cover', data=df, 
                scatter_kws={'alpha':0.5}, line_kws={'color': 'red'}, ax=ax1)
    ax1.set_title(f'Mean Temperature vs Cloud Cover\nCorrelation: {correlation:.3f}')
    ax1.set_xlabel('Mean Temperature (°C)')
    ax1.set_ylabel('Cloud Cover (units)')
    
    # Correlation heatmap
    correlation_matrix = df[['mean_temp', 'cloud_cover']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax2)
    ax2.set_title('Correlation Heatmap')
    
    plt.tight_layout()
    
    # Calculate additional statistics
    correlation_stats = {
        'correlation': correlation,
        'correlation_strength': 'weak' if abs(correlation) < 0.3 else 
                              'moderate' if abs(correlation) < 0.7 else 'strong',
        'p_value': stats.pearsonr(df['mean_temp'], df['cloud_cover'])[1]
    }
    
    return fig, correlation_stats

def analyze_extreme_weather(df):
    # Group by month and calculate statistics
    monthly_stats = df.groupby(df['date'].dt.month).agg({
        'mean_temp': ['mean', 'std'],
        'precipitation': ['mean', 'max']
    }).round(2)
    
    return monthly_stats 