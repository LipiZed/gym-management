from pydantic import BaseModel, EmailStr, SecretStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: SecretStr
    full_name: str
    phone: str
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    phone: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)



class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    