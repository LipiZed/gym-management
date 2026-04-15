from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from app.models.membership import MembershipStatus
from datetime import datetime

class MembershipPlanCreate(BaseModel):
    name: str
    duration: int
    price: Decimal
    
class MembershipPlanResponse(BaseModel):
    id: int
    name: str
    duration: int
    price: Decimal
    model_config = ConfigDict(from_attributes=True)
    
    
class MembershipCreate(BaseModel):
    type_id: int
    start_time: datetime
    
class MembershipResponse(BaseModel):
    id: int
    type_id: int
    client_id: int
    start_time: datetime
    end_time: datetime
    status: MembershipStatus
    model_config = ConfigDict(from_attributes=True)