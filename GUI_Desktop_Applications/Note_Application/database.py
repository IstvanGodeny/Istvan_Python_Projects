"""
Application: Note Application
Author: Istvan Godeny
Date: 14/07/2025
License: MIT License
"""

import os

from PySide6.QtSql import QSqlDatabase, QSqlQuery

# Database path
DB_PATH = "notes.sqlite"

# Initial the database
def init_database():
    if not os.path.exists(DB_PATH):
        # Create the database if it doesn't exist
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(DB_PATH)
        if not db.open():
            print("Could not open the database")
            return False

        query = QSqlQuery()
        query.exec("""
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT
            )
        """)

        db.close()


    return True
