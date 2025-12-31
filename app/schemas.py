from pydantic import BaseModel

# login endpoint schema
class LoginRequest(BaseModel):
    username: str
    password: str

# register endpoint schema
class RegisterRequest(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: str
