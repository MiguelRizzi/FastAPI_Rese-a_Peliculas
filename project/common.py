import jwt

from datetime import datetime
from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import HTTPException

from .database import User

from dotenv import load_dotenv

import os

load_dotenv()

SECRET_KEY= os.getenv('SECRET_KEY')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth")

def create_access_token(user, days=7):
    data = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(days=days)
    }
    
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')

def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception as err:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    data = decode_access_token(token)

    print(data)

    if data:
        return User.select().where(User.id == data['user_id']).first()
    else:
        raise HTTPException(
            status_code=401, 
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"}
        )