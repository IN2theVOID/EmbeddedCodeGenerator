import base64
import datetime
from encodings.base64_codec import base64_encode
from typing import Literal

USER_CREDS = {
    "user": "123",
    "admin": "12345",
    "superuser": "super"
}

USER_ROLES = {
    "user": "user",
    "admin": "admin",
    "superuser": "admin"
}

auth_tokens = []

class AuthResponseFactory:
    @staticmethod
    def getAuthResponce(isAuth: bool, username: str) -> AuthResponse:
        authResponse = AuthResponse
        authResponse.isAuth = isAuth

        token = "None"
        if isAuth:
            token = "TOKEN_" + username + "_" + str(datetime.datetime.now()) + "_ROLE:"+ USER_ROLES[username]
            auth_tokens.append(token)

        authResponse.cookieString = token
        return authResponse

class AuthResponse:
    isAuth: bool
    cookieString: str

class Auth:
    
    @staticmethod
    def authUser(username: str, password: str) -> AuthResponse:
        try:
            if USER_CREDS[username] == password:
                print("AUTH SUCCESS")
                response = AuthResponseFactory.getAuthResponce(isAuth=True, username=username)
            else:
                print("AUTH FAILED")
                response = AuthResponseFactory.getAuthResponce(isAuth=False, username=username)
        except KeyError:
            print("USER NOT IN LIST")
            response = AuthResponseFactory.getAuthResponce(isAuth=False, username=username)
        return response
    
    @staticmethod
    def checkAuth(token: str) -> tuple[Literal[True], str] | tuple[Literal[False], None]:
        print(token)
        print(auth_tokens)
        role = None
        if token in auth_tokens:
            role = Auth.getRoleFromToken(token=token)
            print(role)
            return True, role
        else:
            return False, role
        
    @staticmethod
    def getRoleFromToken(token: str) -> str:
        return token.split("ROLE:")[-1]