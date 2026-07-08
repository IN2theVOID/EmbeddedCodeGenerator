from typing import Generator

from src.modules.database import User, Role, Audit, DbRecords, DbDevice, DbGenerations

def test_user():
    user = User(dbFile="src/database.db")
    assert user.check_creds(username="user", password="user1")
    assert not user.check_creds(username="user", password="broken")

def test_role():
    role = Role(dbFile="src/database.db")
    assert role.get_role_by_user(username="user") == "user"

def test_audit():
    audit = Audit(dbFile="src/database.db")
    assert isinstance(audit.get_all_records(), Generator)

def test_Db_query():
    records = DbRecords(dbFile="src/database.db")
    device = DbDevice(dbFile="src/database.db")
    generations = DbGenerations(dbFile="src/database.db")
    
    assert isinstance(records.get_info(table="models", columns="label"), Generator)
    assert isinstance(device.get_info(label="device_type"), list)
    assert isinstance(generations.get_info(task="123"), list)