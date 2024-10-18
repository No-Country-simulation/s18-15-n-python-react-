from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import SECRET_KEY
from datetime import datetime, timezone
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class TokenData(BaseModel):
    sub: str = None

def verify_token(token: str = Depends(oauth2_scheme)):
    """Verifica el token JWT y extrae la información del usuario."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")  # Extraer el campo 'sub' (ID del usuario)
        
        print(f"Payload decodificado: {payload}")  # Log del payload

        if user_id is None:
            raise credentials_exception

        # Imprimir el tiempo de expiración del token
        expiration_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        current_time = datetime.now(timezone.utc)

        # Verificar que el token no haya expirado
        if expiration_time < current_time:
            raise HTTPException(
                status_code=401,
                detail="El token ha expirado.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Retornar los datos del token (en este caso el ID del usuario)
        return {"sub": user_id}
    
    except JWTError as e:
        print(f"Error decodificando el token: {e}")  # Log del error
        raise credentials_exception