import pandas as pd
import logging

logger = logging.getLogger(__name__)

def extract_data(source=None):
    """Extract data. If no source provided, create fake data."""
    if source is None:
        logger.info("Extracting Data - No source specified: Generating fake data...")
        data = pd.DataFrame({
            "name": ["Homer", "Marge", "Bart", "Lisa", "Maggie"],
            "age": [45, 47, 11, 12, 4]
        })
    else:
        logger.info(f"Extracting Data - Using provided data source: {source}")
        data = source #Use actual source data
    logging.info(f"Extracted {len(data)} rows.")
    return data