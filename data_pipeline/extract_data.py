import pandas as pd
import os
import json


def read_csv_file(file_path):
    data = pd.read_csv(file_path)

    print("\n\n==============================================")
    print(f"Successfully read CSV file : {file_path}")
    print(f"Number of records read : {len(data)}")
    print("==============================================\n\n")

    return data




def generate_metadata(data, dataset_name):
    
    os.makedirs("metadata", exist_ok = True)

    file_path = f"metadata/metadata_{dataset_name}.txt"
    json_path = f"metadata/metadata_{dataset_name}.json"

    missing_val_count = data.isna().sum()
    missing_val_percent = ((missing_val_count / data.shape[0]) * 100).round(2)
    
    column_info = []

    for index, column in enumerate(data.columns):
        column_info.append({
            "index": index,
            "name": column,
            "non_null": int(data[column].notna().sum()),
            "dtype": str(data[column].dtype)
        })

    metadata = {
        "dataset_name": dataset_name,
        "rows": int(data.shape[0]),
        "columns": int(data.shape[1]),
        "column_info": column_info,
        "records": data.head(10).to_dict(orient="records"),
        "missing_values": missing_val_count.to_dict(),
        "missing_percentages": missing_val_percent.to_dict(),
        "description": data.describe().to_dict()
    }

    with open(file_path, "w") as f:

        f.write("=" * 80)
        f.write(f"\n\tMETADATA REPORT FOR {dataset_name}\n")
        f.write("=" * 80)
        f.write("\n\n\n\n")

        f.write("Please NOTE that the metadata of dataset is generated before transforming it, to get idea as to what the raw dataset looks like.")

        f.write("\n\n\n\n")

        f.write(f"DATASET SHAPE : The dataset contains {data.shape[0]} rows and {data.shape[1]} cols.")

        f.write("\n")

        f.write("DATASET COLUMN-WISE INFO : \n")
        f.write("-" * 50)
        f.write("\n")

        data.info(buf=f)

        f.write("\n")
        f.write("-" * 50)

        f.write("\n\n")

        f.write("DATASET RECORD PEEK - FIRST 10 RECORDS\n")
        f.write("-" * 50)
        f.write("\n")

        f.write(data.head(10).to_string())

        f.write("\n")
        f.write("-" * 50)

        f.write("\n\n")

        f.write("DATASET MISSING VALUES - PER COLUMN\n")
        f.write("-" * 50)
        f.write("\n")

        f.write(missing_val_count.to_string())

        f.write("\n")
        f.write("-" * 50)

        f.write("\n\n")

        f.write("DATASET MISSING VALUES PERCENT - PER COLUMN\n")
        f.write("-" * 50)
        f.write("\n")

        f.write(missing_val_percent.to_string())

        f.write("\n")
        f.write("-" * 50)

        f.write("\n\n")

        f.write("DATASET DESCRIPTION - FOR DETECTING OUTLIERS\n")
        f.write("-" * 50)
        f.write("\n")

        f.write(data.describe().to_string())

        f.write("\n")
        f.write("-" * 50)

        f.write("\n\n\n\n")
        f.write("=" * 80)

    with open(json_path, "w") as f:
        json.dump(
            metadata,
            f,
            indent=4,
            default=str
        )

    print(f"\nMetadata SUCCESSFULLY generated for {dataset_name}")

    return file_path




def extract_data():
    dataset_collection = {
        "city_community_data" : "dataset/raw_dataset/chicago_city_community.csv",
        "ward_office_data" : "dataset/raw_dataset/chicago_ward_offices.csv",
        "police_beat_data" : "dataset/raw_dataset/chicago_police_beat_info.csv",
        "iucr_data" : "dataset/raw_dataset/iucr_codes.csv",
        "district_ps_data" : "dataset/raw_dataset/chicago_district_ps_info.csv",
        "crime_data" : "dataset/raw_dataset/chicago_crime_dataset.csv"
        }

    
    extracted_datasets= {}

    for dataset_name, file_path in dataset_collection.items():
        data = read_csv_file(file_path)

        generate_metadata(data, dataset_name)
        extracted_datasets[dataset_name] = data

    return extracted_datasets

