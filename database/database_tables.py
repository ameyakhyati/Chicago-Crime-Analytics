
def create_tables(db_connection):
    db_cursor = db_connection.cursor()

    db_cursor.execute('''
                        create table if not exists

                        WARD_OFFICES(
                            WARD_NO integer primary key,
                            ALDERMAN text,
                            ADDRESS text,
                            CITY text,
                            STATE text,
                            ZIPCODE integer,
                            WARD_PHONE text,
                            WARD_FAX text,
                            EMAIL text,
                            WEBSITE text,
                            LOCATION text,
                            CITY_HALL_ADDRESS text,
                            CITY_HALL_CITY text,
                            CITY_HALL_STATE text,
                            CITY_HALL_ZIPCODE integer,
                            CITY_HALL_PHONE text );                                                               
                        ''')
    
    db_cursor.execute('''
                        create table if not exists

                        IUCR(
                            IUCR_CODE text primary key,
                            PRIMARY_TYPE text,
                            DESCRIPTION text,
                            INDEX_CODE text );
                        ''')

    db_cursor.execute('''
                        create table if not exists

                        POLICE_BEAT(
                            BEAT_NUM integer primary key,
                            DISTRICT integer,
                            SECTOR integer,
                            BEAT integer );
                        ''')

    db_cursor.execute('''
                        create table if not exists

                        CITY_COMMUNITY(
                            COMMUNITY_CODE integer primary key,
                            COMMUNITY_NAME text,
                            POPULATION integer,
                            AREA_SQMILE real,
                            AREA_SQKM real,
                            DENSITY_PER_SQMI real,
                            DENSITY_PER_SQKM real );
                        ''')

    db_cursor.execute('''
                        create table if not exists

                        DISTRICT_PS(
                            DISTRICT_CODE integer primary key,
                            DISTRICT_NAME text,
                            ADDRESS text,
                            CITY text,
                            STATE text,
                            ZIP integer,
                            WEBSITE text,
                            PHONE text,
                            FAX text,
                            TTY text,
                            X_COORDINATE real,
                            Y_COORDINATE real,
                            LATITUDE real,
                            LONGITUDE real,
                            LOCATION text );
                        ''')

    db_cursor.execute('''
                        create table if not exists

                        CRIMES(
                            ID integer,
                            CASE_NUMBER text primary key,
                            INCIDENT_TIME text,
                            INCIDENT_DATE text,
                            INCIDENT_DAYOFWEEK text,
                            INCIDENT_MONTH integer,
                            INCIDENT_YEAR integer,
                            BLOCK text,
                            IUCR_CODE text,
                            PRIMARY_TYPE text,
                            DESCRIPTION text,
                            LOCATION_DESC text,
                            ARREST boolean,
                            DOMESTIC boolean,
                            BEAT_NUM integer,
                            DISTRICT_CODE integer,
                            WARD_NO integer,
                            COMMUNITY_CODE integer,
                            FBI_CODE text,
                            DATE_OF_UPDATE text,
                            X_COORDINATE real,
                            Y_COORDINATE real,
                            LATITUDE real,
                            LONGITUDE real,
                            LOCATION text,

                            foreign key(IUCR_CODE) references IUCR(IUCR_CODE),
                            foreign key(WARD_NO) references WARD_OFFICES(WARD_NO),
                            foreign key(BEAT_NUM) references POLICE_BEAT(BEAT_NUM),
                            foreign key(DISTRICT_CODE) references DISTRICT_PS(DISTRICT_CODE),
                            foreign key(COMMUNITY_CODE) references CITY_COMMUNITY(COMMUNITY_CODE) );
                        ''')

def populate_tables(db_connection, processed_datasets):
    print("\n\nPOPULATING DATABASE TABLES...")
    print("-"*50)

    db_dataset_map = {
        "ward_office_data" : "WARD_OFFICES",
        "city_community_data" : "CITY_COMMUNITY",
        "iucr_data" : "IUCR",
        "district_ps_data": "DISTRICT_PS",
        "police_beat_data" : "POLICE_BEAT",
        "crime_data" : "CRIMES" }

    for dataset_name, table_name in db_dataset_map.items():

        data = processed_datasets[dataset_name]
        print(f"\nPopulating database table {table_name} with {dataset_name}")

        columns = ", ".join(data.columns)
        data_placeholder = ", ".join(["?"]* len(data.columns))

        db_query = f"""
                    insert or ignore into {table_name}
                    ({columns})
                    values ({data_placeholder})
                    """

        data_records = list(data.itertuples(index = False, name = None))
        db_connection.executemany(db_query, data_records)

        print(f"Successfully inserted {len(data)} records into database table {table_name}")
