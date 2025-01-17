import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Function to load and preprocess data
def load_data(file_path):
    try:
        # Load the data with low_memory=False to handle mixed types
        df = pd.read_csv(file_path, low_memory=False)
        
        # Debug: Print the first few rows of the raw data
        print("Raw data before cleaning:")
        print(df.head())
        
        # Convert 'date' column to datetime with the correct format
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')
        
        # Convert 'mean_temp' column to numeric, coercing errors to NaN
        df['mean_temp'] = pd.to_numeric(df['mean_temp'], errors='coerce')
        
        # Drop rows with NaN values in 'mean_temp' or 'date' columns
        df.dropna(subset=['mean_temp', 'date'], inplace=True)
        
        return df
    except FileNotFoundError:
        # Handle the case where the file is not found
        print("Error: The file was not found.")
        return pd.DataFrame()

# Function to analyze monthly temperature trends
def analyze_monthly_temperature_trend(df):
    # Calculate monthly average temperatures
    monthly_temps = df.groupby(df['date'].dt.to_period('M'))['mean_temp'].mean().reset_index()
    monthly_temps['date'] = monthly_temps['date'].dt.to_timestamp()

    # Create the plot using Seaborn for better aesthetics
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_temps, x='date', y='mean_temp', marker='o')
    plt.title('Average Monthly Temperature Trend in London')
    plt.xlabel('Date')
    plt.ylabel('Mean Temperature (°C)')
    plt.grid(True)
    plt.savefig('monthly_temp_trend.png')
    plt.close()
    
    return monthly_temps

# Function to analyze correlation between temperature and cloud cover
def analyze_temp_cloud_correlation(df):
    # Calculate correlation between mean temperature and cloud cover
    correlation = df['mean_temp'].corr(df['cloud_cover'])
    
    # Create scatter plot using Seaborn
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='mean_temp', y='cloud_cover', data=df, alpha=0.5)
    plt.title('Mean Temperature vs Cloud Cover')
    plt.xlabel('Mean Temperature (°C)')
    plt.ylabel('Cloud Cover (units)')
    plt.savefig('temp_cloud_correlation.png')
    plt.close()
    
    # Create a heatmap for correlation matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[['mean_temp', 'cloud_cover']].corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.savefig('correlation_heatmap.png')
    plt.close()
    
    return correlation

# Function to analyze extreme weather statistics
def analyze_extreme_weather(df):
    # Group by month and calculate statistics
    monthly_stats = df.groupby(df['date'].dt.month).agg({
        'mean_temp': ['mean', 'std'],
        'precipitation': ['mean', 'max']
    }).round(2)
    
    return monthly_stats

# Main function to execute the analysis
def main():
    # Load the data
    df = load_data('weather_data.csv')
    
    # Debug: Print the first few rows of the DataFrame
    print("DataFrame after loading and cleaning:")
    print(df.head())
    print("\nDataFrame info:")
    print(df.info())
    
    # Perform analyses
    if not df.empty:
        monthly_temps = analyze_monthly_temperature_trend(df)
        correlation = analyze_temp_cloud_correlation(df)
        extreme_weather = analyze_extreme_weather(df)
        
        # Print results
        print("\nMean Temperature-Cloud Cover Correlation:", correlation)
        print("\nMonthly Weather Statistics:")
        print(extreme_weather)
    else:
        # Inform the user if the DataFrame is empty
        print("The DataFrame is empty after cleaning. Please check the data and cleaning steps.")

# Execute the main function
if __name__ == "__main__":
    main() 