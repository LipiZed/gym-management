from pydantic import BaseModel, EmailStr, SecretStr, ConfigDict

class GymCreate(BaseModel):
    name: str
    location: str
    max_capacity: int
    
class GymResponse(BaseModel):
    id: int
    name: str
    location: str
    max_capacity: int
    model_config = ConfigDict(from_attributes=True)