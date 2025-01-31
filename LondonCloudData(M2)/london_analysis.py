import pandas as pd
import matplotlib.pyplot as plt
from weather_dashboard import WeatherDashboard
from datetime import datetime, timedelta

def analyze_london_weather():
    # Initialize dashboard
    dashboard = WeatherDashboard('./firebase_credentials.json')
    
    # Load data from Firebase
    print("Loading London weather data from Firebase...")
    start_date = datetime.now() - timedelta(days=365)  # Last year of data
    data = dashboard.get_london_weather_history(start_date=start_date)
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Create visualizations
    print("Creating visualizations...")
    
    # 1. Temperature Trends
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df['mean_temp'])
    plt.title('London Temperature Trends')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('temperature_trends.png')
    plt.close()
    
    # 2. Monthly Temperature Box Plot
    plt.figure(figsize=(12, 6))
    df['month'] = df['date'].dt.strftime('%B')
    df.boxplot(column='mean_temp', by='month', figsize=(12, 6))
    plt.title('Monthly Temperature Distribution')
    plt.xlabel('Month')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('monthly_distribution.png')
    plt.close()
    
    # Calculate and print statistics
    print("\nWeather Statistics:")
    print(f"Average Temperature: {df['mean_temp'].mean():.1f}°C")
    print(f"Maximum Temperature: {df['mean_temp'].max():.1f}°C")
    print(f"Minimum Temperature: {df['mean_temp'].min():.1f}°C")
    
    print("\nAnalysis complete! Visualizations saved as PNG files.")

if __name__ == "__main__":
    analyze_london_weather()