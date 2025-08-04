from jose import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
token = "your_jwt_here"

payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print(payload)
