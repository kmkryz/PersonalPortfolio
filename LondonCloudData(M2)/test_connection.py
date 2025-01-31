from weather_dashboard import WeatherDashboard

def test_connection():
    try:
        dashboard = WeatherDashboard('./firebase_credentials.json')
        print("Successfully connected to Firebase!")
        
        # Test basic operations
        user_id = "test_user"
        test_prefs = {
            'favorite_locations': ['London'],
            'temperature_unit': 'Celsius',
            'notification_enabled': True
        }
        
        # Test saving preferences
        dashboard.save_weather_preferences(user_id, test_prefs)
        print("Successfully saved preferences!")
        
        # Clean up
        dashboard.delete_preference(user_id)
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_connection()
