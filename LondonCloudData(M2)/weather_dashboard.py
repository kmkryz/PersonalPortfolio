import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin.exceptions import FirebaseError
from datetime import datetime
from typing import Dict, List, Optional, Callable
import json
import pandas as pd

class WeatherDashboard:
    """
    A class to manage weather data and user preferences in Firebase/Firestore.
    Provides functionality for storing and retrieving weather data, managing user
    preferences, and real-time weather updates.
    """

    def __init__(self, credentials_path: str):
        """
        Initialize Firebase connection with credentials.

        Args:
            credentials_path: Path to Firebase credentials JSON file

        Raises:
            FileNotFoundError: If credentials file doesn't exist
            firebase_admin.exceptions.FirebaseError: If Firebase initialization fails
        """
        try:
            # Check if Firebase is already initialized
            try:
                app = firebase_admin.get_app()
            except ValueError:
                # Initialize Firebase only if not already initialized
                cred = credentials.Certificate(credentials_path)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            self._listeners = {}  # Store active listeners
        except Exception as e:
            raise ConnectionError(f"Failed to initialize Firebase: {str(e)}")

    def save_weather_preferences(self, user_id: str, preferences: Dict) -> None:
        """
        Save user preferences for weather tracking.

        Args:
            user_id: Unique identifier for the user
            preferences: Dictionary containing user preferences
                Required fields: favorite_locations, temperature_unit

        Raises:
            ValueError: If preferences format is invalid
            FirebaseError: If database operation fails
        """
        try:
            self._validate_preferences(preferences)
            doc_ref = self.db.collection('user_preferences').document(user_id)
            doc_ref.set(preferences)
        except Exception as e:
            raise FirebaseError(f"Failed to save preferences: {str(e)}")

    def _validate_preferences(self, preferences: Dict) -> None:
        """
        Validate user preferences format.

        Args:
            preferences: Dictionary of user preferences

        Raises:
            ValueError: If preferences format is invalid
        """
        required_fields = ['favorite_locations', 'temperature_unit']
        if not all(field in preferences for field in required_fields):
            raise ValueError("Missing required preference fields")
        
        if not isinstance(preferences['favorite_locations'], list):
            raise ValueError("favorite_locations must be a list")
        
        valid_units = ['Celsius', 'Fahrenheit']
        if preferences['temperature_unit'] not in valid_units:
            raise ValueError(f"temperature_unit must be one of {valid_units}")

    def save_weather_data(self, location: str, data: Dict) -> None:
        """
        Save weather data for a specific location.

        Args:
            location: Location identifier
            data: Weather data dictionary containing temperature, humidity, conditions

        Raises:
            ValueError: If data format is invalid
            FirebaseError: If database operation fails
        """
        try:
            self._validate_weather_data(data)
            timestamp = datetime.now().isoformat()
            doc_ref = self.db.collection('weather_data').document(timestamp)
            weather_data = {
                'location': location,
                'temperature': data['temperature'],
                'humidity': data['humidity'],
                'conditions': data['conditions'],
                'timestamp': timestamp
            }
            doc_ref.set(weather_data)
        except Exception as e:
            raise FirebaseError(f"Failed to save weather data: {str(e)}")

    def add_realtime_weather_listener(self, location: str, callback: Callable) -> None:
        """
        Add a real-time listener for weather updates.

        Args:
            location: Location to monitor
            callback: Function to call when data changes

        Returns:
            None
        """
        doc_ref = self.db.collection('weather_data')
        query = doc_ref.where('location', '==', location)
        self._listeners[location] = query.on_snapshot(callback)

    def remove_weather_listener(self, location: str) -> None:
        """
        Remove real-time listener for a location.

        Args:
            location: Location to stop monitoring
        """
        if location in self._listeners:
            self._listeners[location].unsubscribe()
            del self._listeners[location]

    def save_london_weather_data(self, df):
        """
        Save London weather data from DataFrame to Firestore
        """
        batch = self.db.batch()
        for index, row in df.iterrows():
            doc_ref = self.db.collection('london_weather').document(str(row['date'].date()))
            weather_data = {
                'date': row['date'].isoformat(),
                'mean_temp': float(row['mean_temp']),
                'cloud_cover': float(row['cloud_cover']) if 'cloud_cover' in row else None,
                'precipitation': float(row['precipitation']) if 'precipitation' in row else None
            }
            batch.set(doc_ref, weather_data)
            
            # Commit every 500 records (Firestore batch limit)
            if index % 499 == 0 and index > 0:
                batch.commit()
                batch = self.db.batch()
        
        # Commit any remaining records
        batch.commit()

    def get_user_preferences(self, user_id):
        """
        Retrieve user preferences
        """
        doc_ref = self.db.collection('user_preferences').document(user_id)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None

    def get_weather_history(self, location, limit=10):
        """
        Retrieve weather history for a location
        """
        docs = (self.db.collection('weather_data')
                .where('location', '==', location)
                .order_by('timestamp', direction=firestore.Query.DESCENDING)
                .limit(limit)
                .stream())
        return [doc.to_dict() for doc in docs]

    def get_london_weather_history(self, start_date=None, end_date=None, limit=100):
        """
        Retrieve London weather history with optional date filtering
        """
        query = self.db.collection('london_weather')
        
        if start_date:
            query = query.where('date', '>=', start_date.isoformat())
        if end_date:
            query = query.where('date', '<=', end_date.isoformat())
            
        docs = query.limit(limit).stream()
        return [doc.to_dict() for doc in docs]

    def get_monthly_averages(self):
        """
        Calculate monthly temperature averages from stored data
        """
        docs = self.db.collection('london_weather').stream()
        data = [doc.to_dict() for doc in docs]
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        monthly_avg = df.groupby(df['date'].dt.to_period('M'))['mean_temp'].mean()
        return monthly_avg.to_dict()

    def delete_preference(self, user_id):
        """
        Delete a user's preferences
        """
        doc_ref = self.db.collection('user_preferences').document(user_id)
        doc_ref.delete()

    def update_preference(self, user_id, updates):
        """
        Update specific user preferences
        """
        doc_ref = self.db.collection('user_preferences').document(user_id)
        doc_ref.update(updates) 