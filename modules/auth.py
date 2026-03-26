import base64
import datetime
from encodings.base64_codec import base64_encode
from typing import Literal

from modules.database import User, Role

auth_tokens = []

class AuthResponseFactory:
    def __init__(self):
        self.role = Role()

    def getAuthResponce(self, isAuth: bool, username: str) -> AuthResponse:
        authResponse = AuthResponse
        authResponse.isAuth = isAuth

        token = "None"
        if isAuth:
            token = "TOKEN_" + username + "_" + str(datetime.datetime.now()) + "_ROLE:"+ self.role.get_role_by_user(username)
            auth_tokens.append(token)

        authResponse.cookieString = token
        return authResponse

class AuthResponse:
    isAuth: bool
    cookieString: str

class Auth:
    def __init__(self) -> None:
        self.user = User()
        self.factory = AuthResponseFactory()

    def authUser(self, username: str, password: str) -> AuthResponse:
        try:
            if self.user.check_creds(username, password):
                print("AUTH SUCCESS")
                response = self.factory.getAuthResponce(isAuth=True, username=username)
            else:
                print("AUTH FAILED")
                response = self.factory.getAuthResponce(isAuth=False, username=username)
        except KeyError:
            print("USER NOT IN LIST")
            response = self.factory.getAuthResponce(isAuth=False, username=username)
        return response
    
    def checkAuth(self, token: str) -> tuple[Literal[True], str] | tuple[Literal[False], None]:
        print(token)
        print(auth_tokens)
        role = None
        if token in auth_tokens:
            role = self.getRoleFromToken(token=token)
            print(role)
            return True, role
        else:
            return False, role
        
    def getRoleFromToken(self, token: str) -> str:
        return token.split("ROLE:")[-1]