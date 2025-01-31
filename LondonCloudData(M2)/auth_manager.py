from firebase_admin import auth
from typing import Dict

class AuthManager:
    """Manages user authentication for the WeatherDashboard."""

    @staticmethod
    def create_user(email: str, password: str) -> Dict:
        """
        Create a new user account.

        Args:
            email: User's email address
            password: User's password

        Returns:
            Dict containing user information

        Raises:
            auth.AuthError: If user creation fails
        """
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            return {'uid': user.uid, 'email': user.email}
        except auth.AuthError as e:
            raise auth.AuthError(f"Failed to create user: {str(e)}")

    @staticmethod
    def verify_token(id_token: str) -> Dict:
        """
        Verify a user's ID token.

        Args:
            id_token: Firebase ID token

        Returns:
            Dict containing verified token claims

        Raises:
            auth.AuthError: If token verification fails
        """
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except auth.AuthError as e:
            raise auth.AuthError(f"Invalid token: {str(e)}")