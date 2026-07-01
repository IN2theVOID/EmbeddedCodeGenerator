
from src.modules.auth import Auth, AuthResponse

def test_auth():
    auth = Auth()
    assert auth.getRoleFromToken("TOKEN\073user\0732026-07-01 22:31:00.342046\073user") == "user"
    assert auth.getUsernameFromToken("TOKEN\073user\0732026-07-01 22:31:00.342046\073user") == "user"
