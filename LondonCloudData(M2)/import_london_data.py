import pandas as pd
from weather_dashboard import WeatherDashboard
import time
from datetime import datetime

def import_data():
    try:
        # Initialize dashboard
        dashboard = WeatherDashboard('./firebase_credentials.json')
        
        # Load London weather data
        print("Loading London weather data from CSV...")
        df = pd.read_csv('london_weather.csv')
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        total_records = len(df)
        print(f"\nFound {total_records} records to import")
        
        # Save to Firestore one record at a time
        print("\nImporting data to Firebase...")
        processed = 0
        
        for _, row in df.iterrows():
            try:
                weather_data = {
                    'date': row['date'].isoformat(),
                    'mean_temp': float(row['mean_temp']),
                    'max_temp': float(row['max_temp']) if pd.notna(row['max_temp']) else None,
                    'min_temp': float(row['min_temp']) if pd.notna(row['min_temp']) else None,
                    'cloud_cover': float(row['cloud_cover']) if pd.notna(row['cloud_cover']) else None,
                    'precipitation': float(row['precipitation']) if pd.notna(row['precipitation']) else None,
                    'pressure': float(row['pressure']) if pd.notna(row['pressure']) else None,
                    'sunshine': float(row['sunshine']) if pd.notna(row['sunshine']) else None,
                    'snow_depth': float(row['snow_depth']) if pd.notna(row['snow_depth']) else None,
                    'global_radiation': float(row['global_radiation']) if pd.notna(row['global_radiation']) else None
                }
                
                # Initial delay before attempting write
                time.sleep(30)  # Wait 30 seconds before each write
                
                # Save single record
                doc_ref = dashboard.db.collection('london_weather').document(row['date'].strftime('%Y-%m-%d'))
                doc_ref.set(weather_data)
                
                processed += 1
                print(f"Processed {processed}/{total_records} records ({(processed/total_records*100):.1f}%)")
                
                # Extra delay every 5 records
                if processed % 5 == 0:
                    print("Taking a longer break...")
                    time.sleep(60)  # 1 minute break every 5 records
                
            except Exception as e:
                print(f"Error processing record {processed+1}: {str(e)}")
                print("Waiting 5 minutes before retrying...")
                time.sleep(300)  # 5 minute wait on error
                continue
        
        print("\nImport complete!")
        print(f"Successfully imported {processed} records")
        return True
        
    except Exception as e:
        print(f"Error during import: {str(e)}")
        return False

if __name__ == "__main__":
    import_data() 