import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def transform(data):
    # Add a new column
    data['age_in_10_years'] = data['age'] + 10
    return data

def load(data):
    # Print to console (for portfolio demo)
    print("Transformed Data:")
    print(data)

def run_pipeline():
    df = extract()
    df = transform(df)
    load(df)

if __name__ == "__main__":
    run_pipeline()