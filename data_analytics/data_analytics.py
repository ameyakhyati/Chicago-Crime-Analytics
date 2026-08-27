import pandas as pd
import numpy as np 
    


def get_crime_yearly_trend(db_connection):
    query = "select * from VW_CRIME_YEARLY order by INCIDENT_YEAR;"

    return pd.read_sql_query(query, db_connection)

    
def get_crime_by_category(db_connection, limit = None):
    query = "select * from VW_CRIME_BY_CATEGORY order by CRIME_COUNT desc"

    if limit is not None:
        query += f" limit {limit}"

    return pd.read_sql_query(query, db_connection)


def get_arrest_count_yearly(db_connection):
    query = "select * from VW_ARREST_YEARLY order by INCIDENT_YEAR;"

    return pd.read_sql_query(query, db_connection)


def get_arrest_rates(crime_data, db_connection):
    
    arrest_rate = crime_data["ARREST"].mean()*100

    query = " select INCIDENT_YEAR, ARREST_COUNT from VW_ARREST_YEARLY order by INCIDENT_YEAR;"

    arrest_years = pd.read_sql_query(query, db_connection)
    total_crimes_yearly = crime_data.groupby("INCIDENT_YEAR").size().reset_index(name = "TOTAL_CRIMES")

    arrest_years = arrest_years.merge(total_crimes_yearly, on = "INCIDENT_YEAR", how = "left")
    arrest_years["ARREST_PERCENTAGE"] = (( arrest_years["ARREST_COUNT"] / arrest_years["TOTAL_CRIMES"] ) * 100 ).round(2)
    

    return arrest_rate, arrest_years


def get_arrest_outcome(crime_data):
    data = crime_data.groupby("ARREST").size().reset_index(name="CRIME_COUNT")

    total_crimes = data["CRIME_COUNT"].sum()
    data["CRIME_PERCENTAGE"] = ((data["CRIME_COUNT"] / total_crimes) * 100 ).round(2)

    data["OUTCOME"] = data["ARREST"].map({True: "ARREST", False: "NO ARREST"})

    return data


def get_crime_month_day_heatmap(crime_data):

    week = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    heatmap_data = pd.crosstab(crime_data["INCIDENT_MONTH"], crime_data["INCIDENT_DAYOFWEEK"])

    heatmap_data = heatmap_data.reindex(columns = week, fill_value = 0)

    heatmap_data = heatmap_data.sort_index()
    return heatmap_data


def get_top_community_crime(crime_data, community_data, limit = None):
    crime_count = crime_data.groupby("COMMUNITY_CODE").size().reset_index(name = "TOTAL_CRIMES")
    community_names = community_data[["COMMUNITY_CODE", "COMMUNITY_NAME"]]

    data = crime_count.merge(community_names, on = "COMMUNITY_CODE", how = "left")
    data = data.sort_values("TOTAL_CRIMES", ascending = False).reset_index(drop = True)

    if limit is not None:
        return data.head(limit)

    return data

def get_crime_hour_intensity(crime_data):

    crime_data["INCIDENT_TIME"] = pd.to_datetime(crime_data["INCIDENT_TIME"], format = "%H:%M:%S", errors = "coerce")

    crime_data["HOUR"] = crime_data["INCIDENT_TIME"].dt.hour
    crime_data["HOUR"] = crime_data["HOUR"].astype(int)

    crime_by_hour = crime_data.groupby("HOUR").size().reset_index(name="TOTAL_CRIMES")
    crime_count = pd.DataFrame({"HOUR": range(24)})

    crime_count = crime_count.merge(crime_by_hour, on = "HOUR", how = "left")
    crime_count["TOTAL_CRIMES"] = crime_count["TOTAL_CRIMES"].fillna(0).astype(int)

    return crime_count


def get_mean_crime_boxplot(crime_data, community_data):
    
    data = get_top_community_crime(crime_data, community_data)

    crime_count = data["TOTAL_CRIMES"].to_numpy()
    crime_mean = np.mean(crime_count)
    crime_median = np.median(crime_count)

    quarter_1 = np.percentile(crime_count, 25)
    quarter_3 = np.percentile(crime_count, 75)

    iqr = quarter_3 - quarter_1

    lower_bound = quarter_1 - (1.5 * iqr)
    upper_bound = quarter_3 + (1.5 * iqr)

    data["IS_OUTLIER"] = ((data["TOTAL_CRIMES"] < lower_bound) | (data["TOTAL_CRIMES"] > upper_bound))

    outliers = data[ data["IS_OUTLIER"]].copy()
    stats = { "mean" : round(float(crime_mean), 2),
              "median" : round(float(crime_median), 2),

              "quarter_1" :  round(float(quarter_1), 2),
              "quarter_3" :  round(float(quarter_3), 2),
              "IQR" :  round(float(iqr), 2),

              "lower_bound" : round(float(lower_bound), 2),
              "upper_bound" : round(float(upper_bound), 2)}

    return data, stats, outliers

def get_crime_correlation(crime_data):
    numeric_cols = ["INCIDENT_MONTH", "INCIDENT_YEAR","ARREST", "DOMESTIC","WARD_NO","BEAT_NUM", "DISTRICT_CODE", "COMMUNITY_CODE"]
    available_cols = []

    for column in numeric_cols:
        if column in crime_data.columns:
            available_cols.append(column)


    data = crime_data[available_cols]
    correlation = data.corr()

    return correlation
