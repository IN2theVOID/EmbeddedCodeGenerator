import sqlite3
from modules.database import User, Role
from modules.exceptions import NoRoleMappingToUser

with sqlite3.connect("database.db", check_same_thread=False) as connection:
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS roles")
    cursor.execute("DROP TABLE IF EXISTS languages")
    cursor.execute("DROP TABLE IF EXISTS platforms")
    cursor.execute("DROP TABLE IF EXISTS models")
    cursor.execute("DROP TABLE IF EXISTS generations")
    cursor.execute("DROP TABLE IF EXISTS devices")
    cursor.execute("DROP TABLE IF EXISTS audit")

    
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS roles (username TEXT, role TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS languages (label TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS platforms (label TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS models (label TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS generations (prompt TEXT, code TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS devices (label TEXT, address TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS audit (date DATETIME, record TEXT)")


    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user", "user1"))
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin1"))
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("superuser", "superuser1"))
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("viewer", "viewer1"))
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("auditor", "auditor1"))

    cursor.execute("INSERT INTO roles (username, role) VALUES (?, ?)", ("user", "user"))
    cursor.execute("INSERT INTO roles (username, role) VALUES (?, ?)", ("admin", "admin"))
    cursor.execute("INSERT INTO roles (username, role) VALUES (?, ?)", ("superuser", "admin"))
    cursor.execute("INSERT INTO roles (username, role) VALUES (?, ?)", ("viewer", "viewer"))
    cursor.execute("INSERT INTO roles (username, role) VALUES (?, ?)", ("auditor", "auditor"))
    
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    print("Created sers:")
    for row in rows:
        print(f"Name: {row[0]}, Password: {row[1]}")

    cursor.execute("SELECT * FROM roles")
    rows = cursor.fetchall()

    print("Created roles:")
    for row in rows:
        print(f"Name: {row[0]}, Role: {row[1]}")

    connection.commit()

    user = User()
    print(user.check_creds("user","user1"))
    role = Role()

    try:
        print(role.get_role_by_user("auditor"))
    except NoRoleMappingToUser:
        print("Пользователю не назначена роль")