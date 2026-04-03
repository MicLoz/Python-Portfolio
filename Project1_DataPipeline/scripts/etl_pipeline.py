import pandas as pd
import logging
from transform import transform_data, infer_column_types, preprocess_data
from test_data import generate_test_data
from configs import (
    basic_config, type_chaos_config, date_chaos_config, aggregation_config,
    cleaning_config, full_stress_config, nightmare_config
)

# -------------------------
# Logging setup
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# -------------------------
# Extract
# -------------------------
def extract() -> pd.DataFrame:
    """Extract dataset from source (currently test generator)."""
    df = generate_test_data()
    logger.info(f"Extracted {len(df)} rows with columns: {list(df.columns)}")
    return df


# -------------------------
# Preprocess
# -------------------------
def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and coerce columns based on inferred types.
    Handles numeric, datetime, and string conversions safely.
    """
    logger.info("Preprocessing and coercing column types...")
    df = preprocess_data(df)
    logger.info("Preprocessing complete. Sample data:")
    logger.info("\n%s", df.head(5))
    return df


# -------------------------
# Transform
# -------------------------
def transform(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Apply transformations defined in config.
    Converts DataFrame to list-of-dicts for transform_data.
    """
    data = df.to_dict(orient="records")
    try:
        transformed_data = transform_data(data, config)
    except Exception as e:
        logger.exception(f"Error applying transformations: {e}")
        transformed_data = data  # fallback to original data

    df_transformed = pd.DataFrame(transformed_data)
    return df_transformed


# -------------------------
# Load
# -------------------------
def load(df: pd.DataFrame):
    """Display transformed data with shape and dtypes."""
    print("\n=== Transformed Data (first 10 rows) ===")
    print(df.head(10))
    print("\nShape:", df.shape)
    print("\nDtypes:\n", df.dtypes)


# -------------------------
# Pipeline Runner
# -------------------------
def run_pipeline(config: dict):
    logger.info("=== Starting ETL Pipeline ===")

    df = extract()
    df = preprocess(df)
    df = transform(df, config)
    load(df)

    logger.info("=== Pipeline Finished ===")


# -------------------------
# Main Entry
# -------------------------
if __name__ == "__main__":
    # Change this to run with any config
    selected_config = nightmare_config
    run_pipeline(selected_config)