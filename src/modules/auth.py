import base64
import datetime
from encodings.base64_codec import base64_encode
from typing import Literal
from urllib import response

from modules.database import User, Role, Audit
from modules.exceptions import NoRoleMappingToUser
from modules.logger import log, LoggerDecorator

auth_tokens = []

class AuthResponseFactory:
    def __init__(self):
        self._role = Role()

    @LoggerDecorator()
    def getAuthResponce(self, isAuth: bool, username: str) -> AuthResponse:
        authResponse = AuthResponse
        authResponse.isAuth = isAuth

        token = "None"
        if isAuth: 
            try:
                token = "TOKEN;" + username + ";" + str(datetime.datetime.now()) + ";"+ self._role.get_role_by_user(username)
                auth_tokens.append(token)
            except NoRoleMappingToUser as e:
                raise NoRoleMappingToUser from e
        authResponse.cookieString = token
        return authResponse

class AuthResponse:
    isAuth: bool
    cookieString: str

class Auth:
    def __init__(self) -> None:
        self._user = User()
        self._factory = AuthResponseFactory()
        self._audit = Audit()

    @LoggerDecorator()
    def authUser(self, username: str, password: str) -> AuthResponse:
        try:
            if self._user.check_creds(username, password):
                log.info("AUTH SUCCESS")
                self._audit.add_record(username=username, record="Auth user")
                response = self._factory.getAuthResponce(isAuth=True, username=username)
            else:
                log.info("AUTH FAILED")
                self._audit.add_record(username=username, record="Auth failed")
                response = self._factory.getAuthResponce(isAuth=False, username=username)
        except KeyError:
            log.error("USER NOT IN LIST")
            self._audit.add_record(username=username, record="Auth failed")
            response = self._factory.getAuthResponce(isAuth=False, username=username)
        return response
    
    @LoggerDecorator()
    def checkAuth(self, token: str) -> tuple[Literal[True], str] | tuple[Literal[False], None]:
        log.info(token)
        role = None
        if token in auth_tokens:
            role = self.getRoleFromToken(token=token)
            username = self.getUsernameFromToken(token=token)
            log.info(role)
            return True, role, username
        else:
            username = self.getUsernameFromToken(token=token)
            return False, role, username
    
    @LoggerDecorator()
    def getRoleFromToken(self, token: str) -> str:
        return token.split(";")[3]
    
    @LoggerDecorator()
    def getUsernameFromToken(self, token: str) -> str:
        return token.split(";")[1]