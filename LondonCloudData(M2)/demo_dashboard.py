from weather_dashboard import WeatherDashboard
from auth_manager import AuthManager
from datetime import datetime, timedelta
import time

def weather_update_callback(doc_snapshot, changes, read_time):
    """Callback function for real-time weather updates."""
    for change in changes:
        if change.type.name == 'MODIFIED':
            print(f"Weather update for {change.document.get('location')}: "
                  f"{change.document.get('temperature')}°C")

def main():
    try:
        # Initialize dashboard
        dashboard = WeatherDashboard('./firebase_credentials.json')

        # Create a test user
        auth_manager = AuthManager()
        user = auth_manager.create_user("test@example.com", "password123")
        user_id = user['uid']

        # Demo user preferences
        preferences = {
            'favorite_locations': ['London'],
            'temperature_unit': 'Celsius',
            'notification_enabled': True
        }

        # Save preferences
        print("Saving user preferences...")
        dashboard.save_weather_preferences(user_id, preferences)

        # Add real-time weather listener
        print("Setting up real-time weather updates...")
        dashboard.add_realtime_weather_listener('London', weather_update_callback)

        # Get London weather history
        print("\nRetrieving London weather history...")
        start_date = datetime.now() - timedelta(days=30)
        history = dashboard.get_london_weather_history(start_date=start_date)
        for entry in history:
            print(f"Weather on {entry['date']}: {entry['mean_temp']}°C")

        # Keep the script running to receive real-time updates
        print("\nListening for weather updates (press Ctrl+C to stop)...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping weather updates...")
            dashboard.remove_weather_listener('London')

    except Exception as e:
        print(f"Error in demo: {str(e)}")

if __name__ == "__main__":
    main() 