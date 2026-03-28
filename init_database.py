import sqlite3
from modules.database import User, Role
from modules.exceptions import NoRoleMappingToUser

with sqlite3.connect("database.db", check_same_thread=False) as connection:
    cursor = connection.cursor()
    
    # DROP
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS roles")
    cursor.execute("DROP TABLE IF EXISTS languages")
    cursor.execute("DROP TABLE IF EXISTS platforms")
    cursor.execute("DROP TABLE IF EXISTS models")
    # cursor.execute("DROP TABLE IF EXISTS generations")
    cursor.execute("DROP TABLE IF EXISTS devices")
    # cursor.execute("DROP TABLE IF EXISTS audit")

    # CREATE
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS roles (username TEXT, role TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS languages (label TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS platforms (label TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS models (label TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS generations (prompt TEXT, code TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS devices (label TEXT, address TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS audit (date DATETIME, username TEXT, record TEXT)")

    # INSERT USERS
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user", "user1"))
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin1"))
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("superuser", "superuser1"))
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("viewer", "viewer1"))
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("auditor", "auditor1"))

    # INSERT ROLES
    cursor.execute("INSERT INTO roles (username, role) VALUES (?, ?)", ("user", "user"))
    cursor.execute("INSERT INTO roles (username, role) VALUES (?, ?)", ("admin", "admin"))
    cursor.execute("INSERT INTO roles (username, role) VALUES (?, ?)", ("superuser", "admin"))
    cursor.execute("INSERT INTO roles (username, role) VALUES (?, ?)", ("viewer", "viewer"))
    cursor.execute("INSERT INTO roles (username, role) VALUES (?, ?)", ("auditor", "auditor"))
    
    # INSERT LANGUAGES
    cursor.execute("INSERT INTO languages (label) VALUES (?)", ("c++",))
    cursor.execute("INSERT INTO languages (label) VALUES (?)", ("c",))
    cursor.execute("INSERT INTO languages (label) VALUES (?)", ("python",))
    cursor.execute("INSERT INTO languages (label) VALUES (?)", ("rust",))
    cursor.execute("INSERT INTO languages (label) VALUES (?)", ("assembly",))
    cursor.execute("INSERT INTO languages (label) VALUES (?)", ("lua",))

    # INSERT PLATFORMS
    cursor.execute("INSERT INTO platforms (label) VALUES (?)", ("arm",))
    cursor.execute("INSERT INTO platforms (label) VALUES (?)", ("x86",))
    cursor.execute("INSERT INTO platforms (label) VALUES (?)", ("x86_64",))
    cursor.execute("INSERT INTO platforms (label) VALUES (?)", ("riscv",))
    cursor.execute("INSERT INTO platforms (label) VALUES (?)", ("avr",))
    cursor.execute("INSERT INTO platforms (label) VALUES (?)", ("esp32",))
    cursor.execute("INSERT INTO platforms (label) VALUES (?)", ("nodemcu",))

    # INSERT MODELS
    cursor.execute("INSERT INTO models (label) VALUES (?)", ("llama3",))
    cursor.execute("INSERT INTO models (label) VALUES (?)", ("llama3.2",))
    cursor.execute("INSERT INTO models (label) VALUES (?)", ("qwen3.5",))

    # INSERT DEVICES
    cursor.execute("INSERT INTO devices (label, address) VALUES (?, ?)", ("Termosensor1 (1st floor)","10.0.0.153"))
    cursor.execute("INSERT INTO devices (label, address) VALUES (?, ?)", ("Termosensor2 (1st floor)","10.0.0.154"))
    cursor.execute("INSERT INTO devices (label, address) VALUES (?, ?)", ("Termosensor3 (1st floor)","10.0.0.155"))
    cursor.execute("INSERT INTO devices (label, address) VALUES (?, ?)", ("Termosensor4 (3st floor)","10.0.0.156"))
    cursor.execute("INSERT INTO devices (label, address) VALUES (?, ?)", ("Termosensor5 (3st floor)","10.0.0.157"))
    cursor.execute("INSERT INTO devices (label, address) VALUES (?, ?)", ("Termosensor6 (4st floor)","10.0.0.158"))
    cursor.execute("INSERT INTO devices (label, address) VALUES (?, ?)", ("Termosensor7 (5st floor)","10.0.0.159"))
    cursor.execute("INSERT INTO devices (label, address) VALUES (?, ?)", ("Termosensor8 (7st floor)","10.0.0.160"))

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    print("Created users:")
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