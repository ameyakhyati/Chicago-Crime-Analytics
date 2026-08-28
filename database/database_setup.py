from .database_tables import create_tables, populate_tables
from .database_views import create_views
import sqlite3

db_path = "database/CHICAGO_CRIMES.DB"

def connect_db():
    print("Initiating Database Coneection")
    
    db_connection = sqlite3.connect(db_path)
    db_connection.execute("PRAGMA foreign_keys = ON")

    return db_connection
    

def setup_db(processed_datasets):
    db_connection = connect_db()

    try:
        print("\nDatabase Setup In Process : Creating Tables, Inserting Values, Creating Views")
        create_tables(db_connection)
        populate_tables(db_connection, processed_datasets)
        create_views(db_connection)

        db_connection.commit()

    except Exception as e:
        db_connection.rollback()
        print(f"\nError occured during database setup : \n{e}")
        raise

    finally:
        print("\nClosing Database Connection")
        db_connection.close()
