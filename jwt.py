from fastapi import FastAPI, HTTPException, Depends 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
import jwt 
from datetime import datetime, timedelta 
 
app = FastAPI() 
 
SECRET_KEY = "MYSECRET123"   # your JWT signature key 
ALGORITHM = "HS256" 
 
# very simple username/password 
FAKE_USER = { 
    "username": "admin", 
    "password": "1234" 
} 
 
security = HTTPBearer() 
 
def create_jwt_token(username: str): 
    payload = { 
        "sub": username, 
        "exp": datetime.utcnow() + timedelta(minutes=30)   # token expires in 30 min 
    } 
    return jwt.encode(payload, SECRET_KEY, 
algorithm=ALGORITHM) 
 
def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)): 
    token = credentials.credentials 
    try: 
        payload = jwt.decode(token, SECRET_KEY, 
algorithms=[ALGORITHM]) 
        return payload["sub"] 
    except jwt.ExpiredSignatureError: 
     raise HTTPException(status_code=401, detail="Token expired") 
    except jwt.InvalidTokenError: 
     raise HTTPException(status_code=401, detail="Invalid token") 
@app.post("/login") 
def login(username: str, password: str): 
    if username == FAKE_USER["username"] and password == FAKE_USER["password"]: token = create_jwt_token(username) 
    return {"access_token": token} 
    raise HTTPException(status_code=401, detail="Invalid username or password") 
@app.get("/protected") 
def protected_route(current_user: str = 
Depends(verify_jwt_token)): 
    return {"message": "This is a protected route!", "user":current_user}