# -------------------------
# Config Validation
# -------------------------
def validate_transform_config(df, transform_config):
    """
    Check that all columns referenced in the transform config exist in the dataframe.
    Returns a dict of {transform_name: [missing_columns]}.
    """

    missing = {}

    # current columns in dataframe
    df_columns = set(df.columns)

    # helper to collect column references per operation
    def extract_columns(cfg: dict) -> list[str]:
        """
        Recursively extract any column names referenced in a transform config.

        Handles:
        - single string values
        - lists of strings
        - nested dictionaries (e.g., add_to_date, average_values)
        Ignores non-string values.
        """
        cols = set()

        if isinstance(cfg, dict):
            for k, v in cfg.items():
                cols.update(extract_columns(v))
        elif isinstance(cfg, list):
            for item in cfg:
                cols.update(extract_columns(item))
        elif isinstance(cfg, str):
            cols.add(cfg)

        return list(cols)

    # iterate over transforms
    for op_name, op_config in transform_config.items():
        referenced_columns = extract_columns(op_config)
        # ignore target columns since they will be created
        referenced_columns = [c for c in referenced_columns if c not in df_columns]
        if referenced_columns:
            missing[op_name] = referenced_columns

    return missing