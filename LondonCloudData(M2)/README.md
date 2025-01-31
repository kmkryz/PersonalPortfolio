# Weather Dashboard with Cloud Storage

A comprehensive weather tracking system using Firebase/Firestore for cloud storage. This project demonstrates real-time weather updates, user authentication, and historical weather data management.

[Software Demo Video](https://youtu.be/SN1qd3B9zDQ)

## Features

- Real-time weather updates
- User authentication and management
- Historical weather data tracking
- User preferences storage
- Data validation and error handling

## Cloud Database Structure

Using Google Firebase/Firestore with the following collections:

- `user_preferences`: Stores user settings and preferences
  - User ID (document ID)
  - Favorite locations (array)
  - Temperature unit preference
  - Notification settings
- `weather_data`: Stores historical weather data
  - Timestamp (document ID)
  - Location
  - Temperature
  - Humidity
  - Weather conditions
- `london_weather`: Stores specific London weather data
  - Date (document ID)
  - Mean temperature
  - Cloud cover
  - Precipitation

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install firebase-admin pandas
   ```
3. Set up Firebase:
   - Create a Firebase project in the Firebase Console
   - Enable Firestore database
   - Download service account credentials
   - Save credentials as `firebase_credentials.json`
   - Add credentials path to your environment variables

## Usage Examples

```python
# Initialize dashboard
dashboard = WeatherDashboard('path/to/credentials.json')

# Save user preferences
dashboard.save_weather_preferences('user123', {
    'favorite_locations': ['London'],
    'temperature_unit': 'Celsius',
    'notification_enabled': True
})

# Get weather history
history = dashboard.get_london_weather_history(
    start_date=datetime.now() - timedelta(days=30)
)

# Calculate monthly averages
monthly_avg = dashboard.get_monthly_averages()
```

## Development Environment

- Python 3.9+
- firebase-admin library
- pandas library
- Visual Studio Code
- Google Firebase Console

## Useful Websites

- [Firebase Documentation](https://firebase.google.com/docs)
- [Python Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Firestore Data Model](https://firebase.google.com/docs/firestore/data-model)
- [Firebase Security Rules](https://firebase.google.com/docs/firestore/security/get-started)

## Future Work

- Implement real-time weather data updates
- Add user authentication system
- Create a web interface for the dashboard
- Add data visualization features
- Implement weather alerts system
- Add support for multiple weather data sources
