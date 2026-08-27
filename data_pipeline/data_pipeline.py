from .extract_data import extract_data
from .transform_data import get_processed_dataset
from database import setup_db

def start_pipeline():

    print("\n")
    print("-" * 50)

    print("\tSTARTING DATA PIPELINING")

    print("-" * 50)

    print("\n\nSTEP 1 - EXTRACT RAW DATA FROM CSVs.")
    extracted_datasets = extract_data()

    print("\n\nSTEP 2 - DATA TRANSFORMATION")
    processed_datasets = get_processed_dataset(extracted_datasets)

    print("\n\nSTEP 3 - DATABASE SETUP")
    setup_db(processed_datasets)

    print("\n\n\n\t DATA PIPELINE COMPLETED SUCCESSFULLY")

    return processed_datasets
    
