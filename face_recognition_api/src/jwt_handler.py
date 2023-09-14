from fastapi import Depends
from os import path
import sys
sys.path.append(path.abspath('D:\Razvan\proj\licenta\login_service'))
from src.jwt_token.jwt_bearer import JWTBearer, decodeJWT

async def decode_jwt_token(token: str = Depends(JWTBearer())):
    try:
        payload = decodeJWT(token)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
