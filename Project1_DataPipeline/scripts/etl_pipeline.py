import pandas as pd
import logging
from transform import transform_data, preprocess_data
from config_validation import validate_pipeline_config_structure
from data_validation import validate_data
from test_data import generate_test_data
from configs import (
    basic_config, type_chaos_config, date_chaos_config, aggregation_config,
    cleaning_config, full_stress_config, nightmare_config, basic_pipeline_internal, basic_pipeline_json
)
from filesystem import parent_path
from extract_from_json import json_to_df

# Toggle config validation behaviour here
STRICT_MODE = False

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
def extract(config: dict) -> pd.DataFrame:
    """Extract dataset from source (defined in config)."""
    if config["mode"] == "internal":
        df = generate_test_data()

    elif config["mode"] == "json":
        relative_data_path = config["path"]
        full_data_path = parent_path / relative_data_path
        df = json_to_df(full_data_path)

    else:
        raise ValueError(f"Unknown mode {config['mode']}")

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

    steps = config.get("steps", [])

    try:
        transformed_data = transform_data(data, steps)
    except Exception as e:
        logger.exception(f"Error applying transformations: {e}")
        transformed_data = data

    return pd.DataFrame(transformed_data)


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

    # -------------------------
    # 1. CONFIG VALIDATION
    # -------------------------
    logger.info("Validating pipeline config structure...")

    errors = validate_pipeline_config_structure(config)

    if errors:
        logger.error("=== CONFIG VALIDATION FAILED ===")
        for err in errors:
            logger.error(err)
        raise ValueError("Invalid pipeline config")

    logger.info("=== CONFIG VALIDATION PASSED ===")

    # -------------------------
    # 2. EXTRACT
    # -------------------------
    logger.info("Extracting data...")

    df = extract(config["extract"])

    # -------------------------
    # 3. DATA VALIDATION
    # -------------------------
    logger.info("Validating data against transform config...")

    data_errors = validate_data(df, config["transform"])

    if data_errors["missing_columns"] or data_errors["missing_params"]:
        logger.warning("Data validation issues detected:")

        if data_errors["missing_columns"]:
            logger.warning(f"Missing columns: {data_errors['missing_columns']}")

        if data_errors["missing_params"]:
            logger.warning(f"Missing params: {data_errors['missing_params']}")

        if STRICT_MODE:
            raise ValueError("Data validation failed")

    # -------------------------
    # 4. PREPROCESS
    # -------------------------
    logger.info("Preprocessing data...")
    df = preprocess(df)

    # -------------------------
    # 5. TRANSFORM
    # -------------------------
    logger.info("Transforming data...")
    df = transform(df, config["transform"])

    # -------------------------
    # 6. LOAD
    # -------------------------
    logger.info("Loading data...")
    load(df)

    logger.info("=== Pipeline Finished ===")

# -------------------------
# Main Entry
# -------------------------
if __name__ == "__main__":
    # Changing this to run with any config
    selected_pipeline = basic_pipeline_internal
    run_pipeline(selected_pipeline)