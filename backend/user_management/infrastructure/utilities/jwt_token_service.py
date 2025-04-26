import jwt
from datetime import datetime, timedelta, timezone
from backend.user_management.application.utilities.token_service import TokenService

# Store algorithm and secret key in env
class JWTTokenService(TokenService):
    def create_token(self, data, expires_minutes):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(payload=to_encode, key='SECRET', algorithm='HS256')
    
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, key='SECRET', algorithms=['HS256'])
            return payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token.")