from pydantic import BaseModel

# login endpoint schema
class LoginRequest(BaseModel):
    username: str
    password: str
