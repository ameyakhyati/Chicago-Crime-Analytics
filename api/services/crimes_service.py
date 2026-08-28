from database import *


def add_crime(db_connection, crime_data):
    return create_crime( db_connection, crime_data)



def get_crimes(db_connection):
    return get_all_crimes( db_connection)


def get_crime(db_connection, case_number):
    return get_crime_by_case_number( db_connection, case_number)


def edit_crime(db_connection, case_number, crime_data):
    return update_crime( db_connection, case_number, crime_data)


def remove_crime(db_connection, case_number):
    return delete_crime( db_connection, case_number)

def get_options(db_connection):
    return get_crime_options(db_connection)
