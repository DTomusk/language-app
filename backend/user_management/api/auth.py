# TODO: this is an application wide dependency, so it needs to be moved up 

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from backend.user_management.api.dependencies import get_token_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), token_service=Depends(get_token_service)):
    """Get the current user from the token."""
    try:
        print(token)
        if not token:
            print("No token provided.")
        user_id = token_service.verify_token(token)
        if user_id is None:
            raise ValueError("Invalid token.")
        return user_id
    except Exception as e:
        raise ValueError(f"Could not validate credentials: {e}") from e
    