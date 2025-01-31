import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from weather_dashboard import WeatherDashboard
from datetime import datetime, timedelta

class WeatherDashboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("London Weather Dashboard")
        self.root.geometry("1200x800")
        
        # Initialize dashboard and load data
        self.dashboard = WeatherDashboard('./firebase_credentials.json')
        self.load_data()
        
        # Create GUI elements
        self.create_widgets()
        
    def load_data(self):
        try:
            print("Loading data from Firebase...")
            start_date = datetime.now() - timedelta(days=365)  # Last year of data
            data = self.dashboard.get_london_weather_history(start_date=start_date)
            
            if not data:  # If no data in Firebase, fall back to CSV
                print("No data in Firebase, loading from CSV...")
                self.df = pd.read_csv('london_weather.csv')
            else:
                # Convert Firebase data to DataFrame
                self.df = pd.DataFrame(data)
            
            # Ensure date column is datetime
            self.df['date'] = pd.to_datetime(self.df['date'])
            print("Data loaded successfully!")
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            # Fallback to CSV if Firebase fails
            print("Falling back to CSV data...")
            self.df = pd.read_csv('london_weather.csv')
            self.df['date'] = pd.to_datetime(self.df['date'])
        
    def create_widgets(self):
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Temperature Trends Tab
        temp_frame = ttk.Frame(notebook)
        notebook.add(temp_frame, text="Temperature Trends")
        self.create_temperature_plot(temp_frame)
        
        # Monthly Analysis Tab
        monthly_frame = ttk.Frame(notebook)
        notebook.add(monthly_frame, text="Monthly Analysis")
        self.create_monthly_plot(monthly_frame)
        
        # Statistics Tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Statistics")
        self.create_statistics(stats_frame)
        
        # Control Panel
        control_frame = ttk.Frame(main_container)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="Refresh Data", 
                  command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Save to Firebase", 
                  command=self.save_to_firebase).pack(side=tk.LEFT, padx=5)
        
    def create_temperature_plot(self, parent):
        fig, ax = plt.subplots(figsize=(11, 5))
        ax.plot(self.df['date'], self.df['mean_temp'])
        ax.set_title('London Temperature Trends')
        ax.set_xlabel('Date')
        ax.set_ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def create_monthly_plot(self, parent):
        # Create a frame to hold both plots
        plots_frame = ttk.Frame(parent)
        plots_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Monthly Box Plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), height_ratios=[1.2, 1])
        fig.suptitle('Monthly Temperature Analysis', y=0.95)
        
        # Create a categorical month column for proper ordering
        months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        self.df['month'] = pd.Categorical(self.df['date'].dt.strftime('%B'), 
                                        categories=months_order, 
                                        ordered=True)
        
        # Box plot
        self.df.boxplot(column='mean_temp', by='month', ax=ax1)
        ax1.set_title('Temperature Distribution by Month')
        ax1.set_ylabel('Temperature (°C)')
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Monthly averages bar plot
        monthly_avg = self.df.groupby('month')['mean_temp'].mean()
        monthly_avg.plot(kind='bar', ax=ax2)
        ax2.set_title('Average Monthly Temperatures')
        ax2.set_ylabel('Temperature (°C)')
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, plots_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_statistics(self, parent):
        # Create a frame with padding
        stats_frame = ttk.Frame(parent, padding="20")
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        stats_text = f"""
        Weather Statistics:
        
        Temperature (°C):
        - Average: {self.df['mean_temp'].mean():.1f}°C
        - Maximum: {self.df['mean_temp'].max():.1f}°C
        - Minimum: {self.df['mean_temp'].min():.1f}°C
        
        Recent Trends:
        - Last Month Average: {self.df.iloc[-30:]['mean_temp'].mean():.1f}°C
        - Last Week Average: {self.df.iloc[-7:]['mean_temp'].mean():.1f}°C
        
        Data Range:
        - From: {self.df['date'].min().strftime('%Y-%m-%d')}
        - To: {self.df['date'].max().strftime('%Y-%m-%d')}
        """
        
        text_widget = tk.Text(stats_frame, height=15, width=50, font=('Arial', 12))
        text_widget.pack(pady=20)
        text_widget.insert(tk.END, stats_text)
        text_widget.config(state='disabled')
        
    def refresh_data(self):
        self.load_data()
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Notebook):
                widget.destroy()
        self.create_widgets()
        
    def save_to_firebase(self):
        print("Data is already in Firebase. No need to save again.")

def main():
    root = tk.Tk()
    app = WeatherDashboardGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()