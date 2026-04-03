import pandas as pd
import logging
from transform import transform_data
from test_data import generate_test_data
from configs import (basic_config, type_chaos_config, date_chaos_config, aggregation_config,
                     cleaning_config, full_stress_config, nightmare_config)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract():
    return generate_test_data()

def transform(df, config):
    data = df.to_dict(orient="records")
    data = transform_data(data, config)
    return pd.DataFrame(data)

def load(data):
    print("\n=== Transformed Data ===")
    print(data.head(10))
    print("\nShape:", data.shape)
    print("\nDtypes:\n", data.dtypes)

def run_pipeline(config=basic_config):
    logger.info("Starting pipeline")

    df = extract()
    logger.info(f"Extracted {len(df)} rows")

    config = {
        "add": {"column": "age", "value": 10}
    }

    df = transform(df, config)
    logger.info("Transformation complete")

    load(df)

    logger.info("Pipeline finished")

if __name__ == "__main__":
    selected_config = nightmare_config
    run_pipeline(selected_config)