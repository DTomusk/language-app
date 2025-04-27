from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

# TODO: top level file shouldn't really be referencing a specific bounded context
from backend.user_management.api.dependencies import get_token_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), token_service=Depends(get_token_service)) -> str:
    """Get the current user from the token."""
    try:
        user_id = token_service.verify_token(token)
        if user_id is None:
            raise ValueError("Invalid token.")
        return user_id
    except Exception as e:
        raise ValueError(f"Could not validate credentials: {e}") from e
    