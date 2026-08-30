from pydantic import BaseModel

# auth
class AuthRequest(BaseModel):
    username: str
    password: str
