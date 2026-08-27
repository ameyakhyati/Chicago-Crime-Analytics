import pandas as pd
import numpy as np
import os



def handle_missing_values(data):
    protected_cols = ["PRIMARY_TYPE", "WARD_NO", "IUCR_CODE", "BEAT_NUM", "DISTRICT_CODE", "COMMUNITY_CODE"]

    dropped_cols = {}
    missing_percent_cols = {}
    dropping_percent_thresh = 50

    for column in data.columns:
        missing_val_percent = ((data[column].isna().sum() / len(data)) * 100).round(2)
        missing_percent_cols[column] = missing_val_percent

        if missing_val_percent >= dropping_percent_thresh and column not in protected_cols:
            dropped_cols[column] = missing_val_percent

    print("Columns and their missing value percentages are: \n")
    print("\nCOLUMN NAME : MISSING VALUE PERCENTAGE")
    print("-" * 50)

    for col_name, missing_percent in missing_percent_cols.items():
        print(f"{col_name} : {missing_percent} %")

    print("-" * 50)
    print("\n\n\n")

    
    if dropped_cols:
        print("Columns that are to be dropped from the dataset, due to missing value percentage being 50% or greater are: \n")
        print("\nCOLUMN NAME : MISSING VALUE PERCENTAGE")
        print("-" * 50)

        for col_name, missing_percent in dropped_cols.items():
            print(f"{col_name} : {missing_percent} %")

        print("-" * 50)

        data.drop(columns = dropped_cols.keys(), inplace = True)

    else:
        print("No columns will be dropped as none have reached the missing value percentage beinf  50% or greater")


    categorical_cols = ["LOCATION_DESC", "WARD_NO", "ARREST", "DOMESTIC", "PRIMARY_TYPE", "IUCR_CODE", "BEAT_NUM", "DISTRICT_CODE", "COMMUNITY_CODE"]
    datetime_cols = ["INCIDENT_DATE", "INCIDENT_TIME", "DATE_OF_UPDATE"]
                        
    numerical_cols = ["POPULATION", "AREA_SQMILE", "AREA_SQKM", "DENSITY_PER_SQMI", "DENSITY_PER_SQKM"]
    location_cols = ["X_COORDINATE", "Y_COORDINATE", "LATITUDE", "LONGITUDE"]

    
    for column in data.columns:
        if column in categorical_cols or column in datetime_cols:
            mode_val = data[column].mode()[0]
            data[column] = data[column].fillna(mode_val)

        elif column in numerical_cols or column in location_cols:
            median_val = data[column].median()
            data[column] = data[column].fillna(median_val)


    if "INCIDENT_DATE" in data.columns:
        missing_month = data["INCIDENT_MONTH"].isna()
        data.loc[missing_month, "INCIDENT_MONTH"] = pd.to_datetime( data.loc[missing_month, "INCIDENT_DATE"]).dt.month

        missing_year = data["INCIDENT_YEAR"].isna()
        data.loc[missing_year, "INCIDENT_YEAR"] = pd.to_datetime( data.loc[missing_year, "INCIDENT_DATE"]).dt.year

        missing_weekday = data["INCIDENT_DAYOFWEEK"].isna()
        data.loc[missing_weekday, "INCIDENT_DAYOFWEEK"] = pd.to_datetime( data.loc[missing_weekday, "INCIDENT_DATE"]).dt.day_name().str.strip().str.upper()
    
            
    return data   
            



def transform_text_cols(data):
    text_cols = ["LOCATION_DESC", "PRIMARY_TYPE", "IUCR_CODE", "DESCRIPTION", "BLOCK", "LOCATION"]

    for column in text_cols:
        if column in data.columns:
            data[column] = (data[column].astype("string").str.strip().str.upper())

    return data




def transform_num_cols(data):
    numeric_cols = ["WARD_NO", "BEAT_NUM", "DISTRICT_CODE", "COMMUNITY_CODE", "POPULATION", "AREA_SQMILE", "AREA_SQKM", "DENSITY_PER_SQMI", "DENSITY_PER_SQKM", "X_COORDINATE", "Y_COORDINATE", "LATITUDE", "LONGITUDE"]

    for column in numeric_cols:
        if column in data.columns:
            data[column] =  pd.to_numeric(data[column], errors = "coerce")

    return data




def transform_date_cols(data):
    
    if "DATE" in data.columns:
        data["DATE"] = pd.to_datetime(data["DATE"], errors = "coerce")

        data["INCIDENT_DAYOFWEEK"] = data["DATE"].dt.day_name().str.strip().str.upper()
        data["INCIDENT_DATE"] = data["DATE"].dt.date
        data["INCIDENT_TIME"] = data["DATE"].dt.strftime("%H:%M:%S")
        data["INCIDENT_MONTH"] = data["DATE"].dt.month

        data.drop(columns = ["DATE"], inplace = True)

        
    if "YEAR" in data.columns:
        data.rename(columns = {"YEAR": "INCIDENT_YEAR"}, inplace = True)

    if "DATE_OF_UPDATE" in data.columns:
        data["DATE_OF_UPDATE"] = pd.to_datetime(data["DATE_OF_UPDATE"], errors = "coerce").dt.strftime("%Y-%m-%d %H:%M:%S")

    return data




def transform_bool_cols(data):
    boolean_cols = ["ARREST", "DOMESTIC"]
    
    for column in boolean_cols:
        if column in data.columns:
            data[column] = data[column].astype("string").str.strip().str.upper().map({"TRUE" : True, "FALSE" : False})

    return data




def transform_data(data, dataset_name):
    print("\n\n="*80)
    print(f"Processing & Cleaning {dataset_name}")
    print("="*80)

    data.columns = data.columns.str.strip().str.upper()

    data = transform_text_cols(data)
    data = transform_num_cols(data)
    data = transform_date_cols(data)
    data = transform_bool_cols(data)

    data = handle_missing_values(data)
    data = data.astype(object).where(pd.notna(data), None)

    
    os.makedirs(f"dataset/processed_dataset", exist_ok = True)
    filepath = (f"dataset/processed_dataset/cleaned_{dataset_name}.csv")

    data.to_csv(filepath, index = False)

    return data




def get_processed_dataset(extracted_datasets):
    processed_datasets = {}

    for dataset_name, data in extracted_datasets.items():
        processed_datasets[dataset_name] = transform_data(data, dataset_name)

    return processed_datasets
