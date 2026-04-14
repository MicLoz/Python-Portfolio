from transform import TRANSFORM_METADATA


# -----------------------------
# COLUMN EXTRACTION
# -----------------------------

def extract_columns(op_name: str, op_params: dict) -> list:
    metadata = TRANSFORM_METADATA.get(op_name, {})
    column_params = metadata.get("column_params", [])

    cols = []

    for param in column_params:
        value = op_params.get(param)

        if isinstance(value, list):
            cols.extend(value)
        elif isinstance(value, str):
            cols.append(value)

    return cols


# -----------------------------
# COLUMN VALIDATION
# -----------------------------

def validate_columns_exist(df, transform_steps):
    """
    Validate columns exist AFTER extract.
    """

    df_columns = set(df.columns)
    missing = {}

    for step in transform_steps:
        op_name = step.get("op")
        op_params = {k: v for k, v in step.items() if k != "op"}

        cols = extract_columns(op_name, op_params)
        missing_cols = [c for c in cols if c not in df_columns]

        if missing_cols:
            missing[op_name] = missing_cols

    return missing


# -----------------------------
# REQUIRED PARAM VALIDATION
# -----------------------------

def validate_required_params(transform_steps):
    """
    Ensure required transform params exist (data-level check).
    """

    from transform import TRANSFORM_METADATA

    missing = {}

    for step in transform_steps:
        op_name = step.get("op")
        op_params = {k: v for k, v in step.items() if k != "op"}

        metadata = TRANSFORM_METADATA.get(op_name, {})
        required = metadata.get("required_params", [])

        missing_params = [p for p in required if p not in op_params]

        if missing_params:
            missing[op_name] = missing_params

    return missing


# -----------------------------
# DATA VALIDATION ENTRY POINT
# -----------------------------

def validate_data(df, transform_config):
    steps = transform_config.get("steps", [])

    return {
        "missing_columns": validate_columns_exist(df, steps),
        "missing_params": validate_required_params(steps)
    }