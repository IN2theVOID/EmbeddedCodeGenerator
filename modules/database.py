import sqlite3
from modules.exceptions import NoRoleMappingToUser


class User:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("database.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def check_creds(self, username: str, password: str) -> bool:
        self.cursor.execute("SELECT username, password FROM users WHERE username = '" + username + "' AND password = '" + password + "'")
        result = self.cursor.fetchall()
        if len(result) < 1:
            return False
        else:
            return True

    def add_user(self, username: str, password: str, role: str) -> None:
        pass

class Role:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("database.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_role_by_user(self, username: str) -> str:
        self.cursor.execute("SELECT role FROM roles WHERE username = '" + username + "'")
        result = self.cursor.fetchall()
        if len(result) < 1:
            raise NoRoleMappingToUser
        else:
            return result[0][0]

    def add_role(self, name: str) -> None:
        pass