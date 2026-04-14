"""
configs.py

Predefined transformation configurations for the ETL pipeline.
These configs are designed for testing different scenarios, 
from basic operations to full stress tests and nightmare cases.
"""
# -----------------------------------
# Prototyping full (combined) config
# -----------------------------------
basic_pipeline_internal = {
    "extract": {
        "mode": "internal"
    },
    "transform": {
        "steps": [
            {"op": "add", "column": "age", "value": 10},
            {"op": "replace_null", "column": "category", "replacement": "UNKNOWN"}
        ]
    },
    "load": {
        "mode": "console"
    }
}

basic_pipeline_json = {
    "extract": {
        "mode": "json",
        "path": "data/testdata.json"
    },
    "transform": {
        "steps": [
            {"op": "add", "column": "age", "value": 10},
            {"op": "replace_null", "column": "category", "replacement": "UNKNOWN"}
        ]
    },
    "load": {
        "mode": "console"
    }
}


# --------------------------------
# Basic / typical transformations
# --------------------------------
basic_config = {
    "add": {"column": "age", "value": 10},
    "replace_null": {"column": "category", "replacement": "UNKNOWN"}
}

# ---------------------------------------
# Type chaos (intentionally wrong types)
# ---------------------------------------
type_chaos_config = {
    "add": {"column": "age", "value": 5},          # may break on string values
    "divide": {"column": "price", "value": 0},     # division by zero
}

# ------------------------------------------
# Date chaos (various date transformations)
# ------------------------------------------
date_chaos_config = {
    "add_to_date": {
        "column": "date",
        "target_column": "date_plus_5",
        "days": 5
    },
    "date_difference": {
        "column1": "date",
        "column2": "date",
        "target_column": "date_diff",
        "unit": "days"
    }
}

# ------------------------------------
# Aggregation-specific configurations
# ------------------------------------
aggregation_config = {
    "sum_values": {
        "columns": ["age", "price", "quantity"],
        "target_column": "total"
    },
    "average_values": {
        "columns": ["age", "price"],
        "target_column": "avg"
    }
}

# -------------------------------------
# Cleaning / deduplication / filtering
# -------------------------------------
cleaning_config = {
    "replace_null": {"column": "text", "replacement": "EMPTY"},
    "deduplicate_rows": {"key_columns": ["id"]},
    "filter_by_date": {
        "column": "date",
        "start": "2024-01-01",
        "end": "2024-12-31"
    }
}

# -------------------------------
# Full stress test configuration
# -------------------------------
full_stress_config = {
    "replace_null": {"column": "category", "replacement": "UNKNOWN"},
    "add": {"column": "age", "value": 10},
    "divide": {"column": "price", "value": 2},
    "add_to_date": {
        "column": "date",
        "target_column": "new_date",
        "days": 10
    },
    "percentage_difference": {
        "column1": "price",
        "column2": "quantity",
        "target_column": "pct_diff"
    },
    "concatenate_strings": {
        "columns": ["category", "text"],
        "target_column": "combined"
    },
    "group_by_aggregate": {
        "group_by_columns": ["category"],
        "aggregations": {
            "price": "average_values",
            "quantity": "sum_values"
        }
    }
}

# --------------------------------------
# Nightmare / comprehensive stress test
# --------------------------------------
nightmare_config = {
    "replace_null": {"column": "category", "replacement": "UNKNOWN"},
    "add": {"column": "age", "value": 10},
    "subtract": {"column": "quantity", "value": 5},
    "divide": {"column": "price", "value": 0},  # test division by zero
    "modulus": {"column": "quantity", "value": 3},
    "add_to_date": {
        "column": "date",
        "target_column": "new_date",
        "days": 10,
        "months": 1,
        "years": 0
    },
    "date_difference": {
        "column1": "start_date",
        "column2": "end_date",
        "target_column": "date_diff_days",
        "unit": "days",
        "swap_if_first_date_less_than_second": True
    },
    "date_difference_precise": {
        "column1": "start_date",
        "column2": "end_date",
        "target_column": "date_diff_precise"
    },
    "percentage_difference": {
        "column1": "price",
        "column2": "quantity",
        "target_column": "pct_diff"
    },
    "concatenate_strings": {
        "columns": ["category", "text"],
        "target_column": "combined",
        "sep": " | "
    },
    "sum_values": {"columns": ["price", "quantity"], "target_column": "sum_total"},
    "average_values": {"columns": ["price", "quantity"], "target_column": "avg_total"},
    "min_value": {"columns": ["price", "quantity"], "target_column": "min_total"},
    "max_value": {"columns": ["price", "quantity"], "target_column": "max_total"},
    "count_values": {"columns": ["price", "quantity"], "target_column": "count_total"},
    "deduplicate_rows": {"key_columns": ["id"]},
    "filter_by_date": {
        "column": "date",
        "start": "2023-01-01",
        "end": "2025-12-31"
    },
    "find_string_in_column": {
        "column": "text",
        "search_string": "urgent",
        "target_column": "found_urgent"
    }
}