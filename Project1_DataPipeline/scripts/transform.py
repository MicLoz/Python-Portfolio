import pandas as pd
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta  # pip install python-dateutil

logger = logging.getLogger(__name__)

class TransformTypeError(Exception):
    """Raised when a transformation receives an invalid data type."""
    pass

# -------------------------
# Preprocessing / Type Inference
# -------------------------

def infer_column_types(df: pd.DataFrame) -> dict:
    inferred = {}

    for col in df.columns:
        series = df[col]

        # Remove obvious empty values
        cleaned = series.dropna()
        cleaned = cleaned[cleaned != ""]

        if cleaned.empty:
            inferred[col] = "string"
            continue

        # --- NUMERIC CHECK ---
        numeric_series = pd.to_numeric(cleaned, errors='coerce')
        numeric_valid = numeric_series.notna().sum()

        if numeric_valid >= len(cleaned) * 0.6:
            inferred[col] = "numeric"
            continue

        # --- DATETIME CHECK ---
        datetime_series = pd.to_datetime(cleaned, errors='coerce')
        datetime_valid = datetime_series.notna().sum()

        if datetime_valid >= len(cleaned) * 0.6:
            inferred[col] = "datetime"
            continue

        # --- FALLBACK ---
        inferred[col] = "string"

    return inferred

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and coerce columns based on inferred types:
    - numeric: convert strings to numbers, NaN for invalids
    - datetime: parse strings to datetime
    - string: fill NaN with empty string
    """
    inferred_types = infer_column_types(df)
    for col, dtype in inferred_types.items():
        try:
            if dtype == 'numeric':
                df[col] = pd.to_numeric(df[col], errors='coerce')
            elif dtype == 'datetime':
                df[col] = df[col].apply(parse_date_safe)
            else:
                df[col] = df[col].fillna('').astype(str)
        except Exception as e:
            logger.warning(f"Failed to coerce column '{col}' to {dtype}: {e}")
    return df

# -------------------------
# Helper Functions
# -------------------------

def safe_numeric(value):
    """Return a numeric value or None if invalid."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def add(x, y):
    x = safe_numeric(x)
    y = safe_numeric(y)
    if x is None or y is None:
        return x
    return x + y

def subtract(x, y):
    x = safe_numeric(x)
    y = safe_numeric(y)
    if x is None or y is None:
        return x
    return x - y

def multiply(x, y):
    x = safe_numeric(x)
    y = safe_numeric(y)
    if x is None or y is None:
        return x
    return x * y

def divide(x, y):
    x = safe_numeric(x)
    y = safe_numeric(y)
    if x is None or y in (None, 0):
        return None
    return x / y

def modulus(x, y):
    x = safe_numeric(x)
    y = safe_numeric(y)
    if x is None or y in (None, 0):
        return None
    return x % y

def replace_null(value, replacement="N/A"):
    return value if value not in (None, '') else replacement

def filter_numeric_values(values):
    return [safe_numeric(v) for v in values if safe_numeric(v) is not None]

def sum_values(values):
    valid = filter_numeric_values(values)
    return sum(valid) if valid else 0

def average_values(values):
    valid = filter_numeric_values(values)
    return sum(valid) / len(valid) if valid else None

def max_value(values):
    valid = filter_numeric_values(values)
    return max(valid) if valid else None

def min_value(values):
    valid = filter_numeric_values(values)
    return min(valid) if valid else None

def count_values(values):
    valid = [v for v in values if v is not None]
    return len(valid)

def percentage_difference(value_one, value_two):
    v1 = safe_numeric(value_one)
    v2 = safe_numeric(value_two)
    if v1 is None or v2 in (None, 0):
        return None
    return ((v1 - v2) / v2) * 100

def concatenate_strings(values, sep=" "):
    return sep.join(str(v) for v in values if v not in (None, ''))

def find_string_in_column(value, search_string):
    if value in (None, ''):
        return False
    return search_string in str(value)

def parse_date_safe(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%Y-%m-%d %H:%M:%S.%f"):
            try:
                return datetime.strptime(value, fmt)
            except (ValueError, TypeError):
                continue
    return None

def add_to_date(date_value, days=0, months=0, years=0):
    date_value = parse_date_safe(date_value)
    if not date_value:
        return None
    return date_value + relativedelta(days=days, months=months, years=years)

def date_difference(date1, date2, unit="days", swap_if_first_date_less_than_second=False):
    date1 = parse_date_safe(date1)
    date2 = parse_date_safe(date2)
    if not date1 or not date2:
        return None
    if swap_if_first_date_less_than_second and date1 < date2:
        date1, date2 = date2, date1
    delta = date1 - date2
    if unit == "seconds":
        return delta.total_seconds()
    elif unit == "minutes":
        return delta.total_seconds() / 60
    elif unit == "hours":
        return delta.total_seconds() / 3600
    elif unit == "days":
        return delta.days
    return None

def date_difference_precise(date1, date2, swap_if_first_date_less_than_second=False):
    date1 = parse_date_safe(date1)
    date2 = parse_date_safe(date2)
    if not date1 or not date2:
        return None
    if swap_if_first_date_less_than_second and date1 < date2:
        date1, date2 = date2, date1
    delta = relativedelta(date1, date2)
    return {
        "years": delta.years,
        "months": delta.months,
        "days": delta.days,
        "hours": delta.hours,
        "minutes": delta.minutes,
        "seconds": delta.seconds
    }

def deduplicate_rows(data, key_columns):
    seen = set()
    result = []
    for row in data:
        key = tuple(row.get(c) for c in key_columns)
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result

def filter_by_date(data, column, start=None, end=None):
    start_dt = parse_date_safe(start) if start else None
    end_dt = parse_date_safe(end) if end else None
    result = []
    for row in data:
        val = parse_date_safe(row.get(column))
        if not val:
            continue
        if start_dt and val < start_dt:
            continue
        if end_dt and val > end_dt:
            continue
        result.append(row)
    return result

# -------------------------
# Aggregations
# -------------------------

AGGREGATION_FUNCTIONS = {
    "sum_values": sum_values,
    "average_values": average_values,
    "min_value": min_value,
    "max_value": max_value,
    "count_values": count_values,
}

def group_by_aggregate(data, group_by_columns, aggregations):
    grouped = {}
    for row in data:
        key = tuple(row.get(c) for c in group_by_columns)
        grouped.setdefault(key, []).append(row)
    result = []
    for key, rows in grouped.items():
        new_row = {c: key[i] for i, c in enumerate(group_by_columns)}
        for col, agg_name in aggregations.items():
            values = [r.get(col) for r in rows]
            func = AGGREGATION_FUNCTIONS.get(agg_name)
            new_row[col] = func(values) if func else None
        result.append(new_row)
    return result

# -------------------------
# Transformation Registry
# -------------------------

TRANSFORM_FUNCTIONS = {}

def register_transform(name):
    def decorator(func):
        TRANSFORM_FUNCTIONS[name] = func
        return func
    return decorator

# -------------------------
# Transform Wrappers
# -------------------------

@register_transform("add")
def transform_add(data, params):
    col = params.get("column")
    value = params.get("value", 0)
    for row in data:
        if col in row:
            row[col] = add(row[col], value)
    return data

@register_transform("subtract")
def transform_subtract(data, params):
    col = params.get("column")
    value = params.get("value", 0)
    for row in data:
        if col in row:
            row[col] = subtract(row[col], value)
    return data

@register_transform("multiply")
def transform_multiply(data, params):
    col = params.get("column")
    factor = params.get("factor", 1)
    for row in data:
        if col in row:
            row[col] = multiply(row[col], factor)
    return data

@register_transform("divide")
def transform_divide(data, params):
    col = params.get("column")
    value = params.get("value", 1)
    for row in data:
        if col in row:
            row[col] = divide(row[col], value)
    return data

@register_transform("modulus")
def transform_modulus(data, params):
    col = params.get("column")
    value = params.get("value", 1)
    for row in data:
        if col in row:
            row[col] = modulus(row[col], value)
    return data

@register_transform("replace_null")
def transform_replace_null(data, params):
    col = params.get("column")
    replacement = params.get("replacement", "N/A")
    for row in data:
        if col in row:
            row[col] = replace_null(row[col], replacement)
    return data

@register_transform("deduplicate_rows")
def transform_deduplicate_rows(data, params):
    keys = params.get("key_columns", [])
    return deduplicate_rows(data, keys)

@register_transform("filter_by_date")
def transform_filter_by_date(data, params):
    col = params.get("column")
    start = params.get("start")
    end = params.get("end")
    return filter_by_date(data, col, start=start, end=end)

@register_transform("add_to_date")
def transform_add_to_date(data, params):
    col = params.get("column")
    target = params.get("target_column")
    days = params.get("days", 0)
    months = params.get("months", 0)
    years = params.get("years", 0)
    for row in data:
        if col in row:
            row[target] = add_to_date(row[col], days=days, months=months, years=years)
    return data

@register_transform("percentage_difference")
def transform_percentage_difference(data, params):
    col1 = params.get("column1")
    col2 = params.get("column2")
    target = params.get("target_column")
    for row in data:
        if col1 in row and col2 in row:
            row[target] = percentage_difference(row[col1], row[col2])
    return data

@register_transform("concatenate_strings")
def transform_concatenate_strings(data, params):
    cols = params.get("columns", [])
    target = params.get("target_column")
    sep = params.get("sep", " ")
    for row in data:
        row[target] = concatenate_strings([row.get(c) for c in cols], sep)
    return data

@register_transform("find_string_in_column")
def transform_find_string_in_column(data, params):
    col = params.get("column")
    search = params.get("search_string", "")
    target = params.get("target_column")
    for row in data:
        if col in row:
            row[target] = find_string_in_column(row[col], search)
    return data

@register_transform("sum_values")
def transform_sum_values(data, params):
    cols = params.get("columns", [])
    target = params.get("target_column")
    for row in data:
        row[target] = sum_values([row.get(c) for c in cols])
    return data

@register_transform("average_values")
def transform_average_values(data, params):
    cols = params.get("columns", [])
    target = params.get("target_column")
    for row in data:
        row[target] = average_values([row.get(c) for c in cols])
    return data

@register_transform("min_value")
def transform_min_value(data, params):
    cols = params.get("columns", [])
    target = params.get("target_column")
    for row in data:
        row[target] = min_value([row.get(c) for c in cols])
    return data

@register_transform("max_value")
def transform_max_value(data, params):
    cols = params.get("columns", [])
    target = params.get("target_column")
    for row in data:
        row[target] = max_value([row.get(c) for c in cols])
    return data

@register_transform("count_values")
def transform_count_values(data, params):
    cols = params.get("columns", [])
    target = params.get("target_column")
    for row in data:
        row[target] = count_values([row.get(c) for c in cols])
    return data

@register_transform("group_by_aggregate")
def transform_group_by_aggregate(data, params):
    group_cols = params.get("group_by_columns", [])
    aggregations = params.get("aggregations", {})
    return group_by_aggregate(data, group_cols, aggregations)

@register_transform("date_difference")
def transform_date_difference(data, params):
    col1 = params.get("column1")
    col2 = params.get("column2")
    target = params.get("target_column")
    unit = params.get("unit", "days")
    swap = params.get("swap_if_first_date_less_than_second", False)
    for row in data:
        row[target] = date_difference(row.get(col1), row.get(col2), unit=unit, swap_if_first_date_less_than_second=swap)
    return data

@register_transform("date_difference_precise")
def transform_date_difference_precise(data, params):
    col1 = params.get("column1")
    col2 = params.get("column2")
    target = params.get("target_column")
    swap = params.get("swap_if_first_date_less_than_second", False)
    for row in data:
        row[target] = date_difference_precise(row.get(col1), row.get(col2), swap_if_first_date_less_than_second=swap)
    return data

# -------------------------
# Main Transform Dispatcher
# -------------------------

def transform_data(data, config):
    for op, params in config.items():
        func = TRANSFORM_FUNCTIONS.get(op)
        if not func:
            logger.warning(f"Unknown transformation: {op}")
            continue
        try:
            data = func(data, params)
        except Exception as e:
            logger.exception(f"Error running transformation '{op}': {e}")
    return data