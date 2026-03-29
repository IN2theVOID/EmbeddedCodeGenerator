import sqlite3
from datetime import datetime

from modules.exceptions import NoRoleMappingToUser


class User:
    def __init__(self) -> None:
        self._connection = sqlite3.connect("database.db", check_same_thread=False)
        self._cursor = self._connection.cursor()

    def check_creds(self, username: str, password: str) -> bool:
        self._cursor.execute("SELECT username, password FROM users WHERE username = '" + username + "' AND password = '" + password + "'")
        result = self._cursor.fetchall()
        if len(result) < 1:
            return False
        else:
            return True

    def add_user(self, username: str, password: str, role: str) -> None:
        pass

class Role:
    def __init__(self) -> None:
        self._connection = sqlite3.connect("database.db", check_same_thread=False)
        self._cursor = self._connection.cursor()

    def get_role_by_user(self, username: str) -> str:
        self._cursor.execute("SELECT role FROM roles WHERE username = '" + username + "'")
        result = self._cursor.fetchall()
        if len(result) < 1:
            raise NoRoleMappingToUser
        else:
            return result[0][0]

    def add_role(self, name: str) -> None:
        pass

class Audit:
    def __init__(self) -> None:
        self._connection = sqlite3.connect("database.db", check_same_thread=False)
        self._cursor = self._connection.cursor()

    def add_record(self, username: str, record: str) -> None:
        self._cursor.execute("INSERT INTO audit (date, username, record) VALUES (?, ?, ?)", (datetime.now(), username, record))
        self._connection.commit()

    def get_all_records(self) -> sqlite3.Generator[sqlite3.Any, sqlite3.Any, None]:
        self._cursor.execute("SELECT date, username, record FROM audit LIMIT 30")
        result = self._cursor.fetchall()
        for record in result:
            yield record

class Info:
    def __init__(self) -> None:
        self._connection = sqlite3.connect("database.db", check_same_thread=False)
        self._cursor = self._connection.cursor()

    def get_records(self, table: str, columns: str):
        self._cursor.execute("SELECT " + columns + " FROM " + table)
        result = self._cursor.fetchall()
        for record in result:
            yield record
    
    def getDeviceDataByLabel(self, label: str):
        self._cursor.execute("SELECT * FROM devices WHERE label = '" + label + "'")
        result = self._cursor.fetchall()
        return result
    
    def getGenerationDataByTask(self, task: str):
        self._cursor.execute("SELECT * FROM generations WHERE task = '" + task + "'")
        result = self._cursor.fetchall()
        return result


class Generations:
    def __init__(self) -> None:
        self._connection = sqlite3.connect("database.db", check_same_thread=False)
        self._cursor = self._connection.cursor()

    def add_generation(self, task: str, code: str):
        self._cursor.execute("INSERT INTO generations (task, code) VALUES (?, ?)", (task, code))
        self._connection.commit()