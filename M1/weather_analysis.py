import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Data loading and preprocessing
def load_data(file_path):
    try:
        
        df = pd.read_csv(file_path, low_memory=False)
        
        
        print("Raw data before cleaning:")
        print(df.head())
        
        
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')
        
        
        df['mean_temp'] = pd.to_numeric(df['mean_temp'], errors='coerce')
        
        
        df.dropna(subset=['mean_temp', 'date'], inplace=True)
        
        return df
    except FileNotFoundError:
        print("Error: The file was not found.")
        return pd.DataFrame()

def analyze_monthly_temperature_trend(df):
    # Calculate monthly average temperatures
    monthly_temps = df.groupby(df['date'].dt.to_period('M'))['mean_temp'].mean().reset_index()
    monthly_temps['date'] = monthly_temps['date'].dt.to_timestamp()

    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_temps, x='date', y='mean_temp', marker='o')
    plt.title('Average Monthly Temperature Trend in London')
    plt.xlabel('Date')
    plt.ylabel('Mean Temperature (°C)')
    plt.grid(True)
    plt.savefig('monthly_temp_trend.png')
    plt.close()
    
    return monthly_temps

def analyze_temp_cloud_correlation(df):
    # Calculate correlation between mean temperature and cloud cover
    correlation = df['mean_temp'].corr(df['cloud_cover'])
    
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='mean_temp', y='cloud_cover', data=df, alpha=0.5)
    plt.title('Mean Temperature vs Cloud Cover')
    plt.xlabel('Mean Temperature (°C)')
    plt.ylabel('Cloud Cover (units)')
    plt.savefig('temp_cloud_correlation.png')
    plt.close()
    
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[['mean_temp', 'cloud_cover']].corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.savefig('correlation_heatmap.png')
    plt.close()
    
    return correlation

def analyze_extreme_weather(df):
    # Group by month and calculate statistics
    monthly_stats = df.groupby(df['date'].dt.month).agg({
        'mean_temp': ['mean', 'std'],
        'precipitation': ['mean', 'max']
    }).round(2)
    
    return monthly_stats

def main():
    
    df = load_data('weather_data.csv')
    
    
    print("DataFrame after loading and cleaning:")
    print(df.head())
    print("\nDataFrame info:")
    print(df.info())
    
   
    if not df.empty:
        monthly_temps = analyze_monthly_temperature_trend(df)
        correlation = analyze_temp_cloud_correlation(df)
        extreme_weather = analyze_extreme_weather(df)
        
        
        print("\nMean Temperature-Cloud Cover Correlation:", correlation)
        print("\nMonthly Weather Statistics:")
        print(extreme_weather)
    else:
        print("The DataFrame is empty after cleaning. Please check the data and cleaning steps.")

if __name__ == "__main__":
    main() 