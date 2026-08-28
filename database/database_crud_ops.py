import sqlite3


def create_crime(db_connection, crime_data):
    columns = ", ".join(crime_data.keys())
    placeholders = ", ".join(["?"] * len(crime_data))

    query = f"""
                insert into CRIMES ({columns})
                values ({placeholders}) """ 

    try:
        cursor = db_connection.cursor()
        cursor.execute(query, tuple(crime_data.values()) )

        db_connection.commit()

        return { "success": True,
                 "message": "Crime record created successfully.",
                 "case_number": crime_data.get("CASE_NUMBER") }

    except Exception as e:
        db_connection.rollback()

        return { "success": False,
                 "message": f"Could not create crime record: {e}" }



def get_all_crimes(db_connection):
    cursor = db_connection.cursor()

    cursor.execute(""" select * from CRIMES
                       order by INCIDENT_DATE desc """)

    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]

    crimes = []
    for row in rows:
        crimes.append(dict(zip(columns, row)))

    return crimes



def get_crime_by_case_number(db_connection, case_number):
    cursor = db_connection.cursor()

    cursor.execute(""" select * from CRIMES
                       where CASE_NUMBER = ? """, (case_number,))

    row = cursor.fetchone()

    if row is None:
        return None

    columns = []
    for column in cursor.description:
        columns.append(column[0])

    return dict(zip(columns, row))



def update_crime(db_connection, case_number, crime_data):
    if not crime_data:
        return {
            "success": False,
            "message": "No data provided for update."
        }

    update_fields = ", ".join([f"{column} = ?" for column in crime_data.keys()])

    values = list(crime_data.values())
    values.append(case_number)

    query = f""" update CRIMES
                 set {update_fields} where CASE_NUMBER = ? """

    try:
        cursor = db_connection.cursor()
        cursor.execute(query, values)

        if cursor.rowcount == 0:
            db_connection.rollback()

            return { "success": False,
                     "message": "Crime record not found."}

        db_connection.commit()

        return { "success": True,
                 "message": "Crime record updated successfully.",
                 "case_number": case_number }

    except Exception as e:
        db_connection.rollback()

        return { "success": False,
                 "message": f"Could not update crime record: {e}" }


def delete_crime(db_connection, case_number):

    try:
        cursor = db_connection.cursor()

        cursor.execute(""" delete from CRIMES
                          where CASE_NUMBER = ? """, (case_number,))

        if cursor.rowcount == 0:
            db_connection.rollback()

            return { "success": False,
                     "message": "Crime record not found."}

        db_connection.commit()

        return { "success": True,
                 "message": "Crime record deleted successfully.",
                 "case_number": case_number}


    except Exception as e:
        db_connection.rollback()

        return { "success": False,
                 "message": f"Could not update crime record: {e}" }


    
def get_crime_options(db_connection):
    cursor = db_connection.cursor()

    options = {}

    cursor.execute(""" select IUCR_CODE, PRIMARY_TYPE, DESCRIPTION
                       from IUCR
                       order by IUCR_CODE """)
    
    options["iucr"] = [dict(row) for row in cursor.fetchall()]

    cursor.execute(""" select BEAT_NUM
                       from POLICE_BEAT
                       order by BEAT_NUM """)
    
    options["beats"] = [row[0] for row in cursor.fetchall()]

    cursor.execute(""" select DISTRICT_CODE, DISTRICT_NAME
                       from DISTRICT_PS
                       order by DISTRICT_CODE """)

    options["districts"] = [dict(row) for row in cursor.fetchall()]

    cursor.execute(""" select WARD_NO, ALDERMAN
                       from WARD_OFFICES
                       order by WARD_NO """)
    
    options["wards"] = [dict(row) for row in cursor.fetchall()]

    cursor.execute(""" select COMMUNITY_CODE, COMMUNITY_NAME
                       from CITY_COMMUNITY
                       order by COMMUNITY_CODE """)
    
    options["communities"] = [dict(row) for row in cursor.fetchall()]

    return options
