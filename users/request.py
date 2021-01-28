import sqlite3
import json
from models.users import User
from datetime import datetime

def register_user(user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        #Set values passed in from form
        db_cursor.execute("""
        INSERT INTO Users
            ( first_name, last_name, email, password, username, created_on)
        VALUES
            ( ?, ?, ?, ?, ?, ? );
        """, (user['first_name'], user['last_name'], user['email'], user['password'], user['username'], datetime.now()))

        #Set id to id of last row, set created on to now, and account type to 1 for all (for now)
        id = db_cursor.lastrowid
        account_type_id = 1

        #Add the created things to the user being created
        user['id'] = id
        user['account_type_id'] = account_type_id
        user['valid'] = True


        return json.dumps(user)




