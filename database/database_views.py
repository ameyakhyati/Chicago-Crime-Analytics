def create_views(db_connection):
    db_cursor = db_connection.cursor()

    db_cursor.execute('''
                        create view if not exists
                        VW_CRIME_YEARLY as
                        
                            select INCIDENT_YEAR, count(*) as TOTAL_CRIMES
                            from CRIMES

                            group by INCIDENT_YEAR
                            order by INCIDENT_YEAR;                            
                        ''')

    db_cursor.execute('''
                        create view if not exists
                        VW_CRIME_BY_CATEGORY as

                            select PRIMARY_TYPE,
                            count(*) as CRIME_COUNT,

                            round( count(*) * 100.0 / (select count(*) from CRIMES), 2) as CRIME_PERCENTAGE
                            from CRIMES

                            group by PRIMARY_TYPE
                            order by CRIME_COUNT desc;   
                        ''')

    db_cursor.execute('''
                        create view if not exists
                        VW_ARREST_YEARLY as

                            select INCIDENT_YEAR,
                            count(*) as ARREST_COUNT,

                            round(count(*) * 100.0 / ( select count(*) from CRIMES c2
                                                      where c2.INCIDENT_YEAR = CRIMES.INCIDENT_YEAR), 2 ) as ARREST_PERCENTAGE

                            from CRIMES
                            where ARREST = 1

                            group by INCIDENT_YEAR
                            order by INCIDENT_YEAR desc;

                        ''')

    return db_cursor.fetchall()
