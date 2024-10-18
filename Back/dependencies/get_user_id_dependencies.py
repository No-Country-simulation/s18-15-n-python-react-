from fastapi import Depends
from auth.oauth_verify import verify_token  

async def get_user_id(token_data: dict = Depends(verify_token)):
    """Extrae el user_id del token JWT."""
    return token_data['sub']
