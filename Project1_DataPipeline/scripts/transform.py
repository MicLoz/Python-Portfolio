import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta  # pip install python-dateutil

logger = logging.getLogger(__name__)

class TransformTypeError(Exception):
    """Raised when a transformation receives an invalid data type."""
    pass

def ensure_type(value, expected_type):
    """
    Ensure that `value` is of type `expected_type` (or tuple of types).
    Returns True if valid, False otherwise.
    """
    return isinstance(value, expected_type)

def multiply(number_for_multiply, value):
    if not ensure_type(number_for_multiply, (int, float)):
        raise TransformTypeError(f"multiply: Expected int or float for 'number_for_multiply', got {type(number_for_multiply)}")
    if not ensure_type(value, (int, float)):
        raise TransformTypeError(f"multiply: Expected int or float for 'value', got {type(value)}")
    return number_for_multiply * value

def add(number_for_addition, value):
    if not ensure_type(number_for_addition, (int, float)):
        raise TransformTypeError(f"add: Expected int or float for 'number_for_addition', got {type(number_for_addition)}")
    if not ensure_type(value, (int, float)):
        raise TransformTypeError(f"add: Expected int or float for 'value', got {type(value)}")
    return number_for_addition + value

def subtract(number_for_subtraction, value):
    if not ensure_type(number_for_subtraction, (int, float)):
        raise TransformTypeError(f"subtract: Expected int or float for 'number_for_subtraction', got {type(number_for_subtraction)}")
    if not ensure_type(value, (int, float)):
        raise TransformTypeError(f"subtract: Expected int or float for 'value', got {type(value)}")
    return number_for_subtraction - value

def divide(number_for_division, value):
    if not ensure_type(number_for_division, (int, float)):
        raise TransformTypeError(f"divide: Expected int or float for 'number_for_division', got {type(number_for_division)}")
    if not ensure_type(value, (int, float)):
        raise TransformTypeError(f"divide: Expected int or float for 'value', got {type(value)}")
    if value == 0:
        return None
    else:
        return number_for_division / value

def modulus(number_for_modulus, value):
    if not ensure_type(number_for_modulus, (int, float)):
        raise TransformTypeError(f"modulus: Expected int or float for 'number_for_modulus', got {type(number_for_modulus)}")
    if not ensure_type(value, (int, float)):
        raise TransformTypeError(f"modulus: Expected int or float for 'value', got {type(value)}")
    return number_for_modulus % value

def filter_numeric_values(values):
    valid = [v for v in values if ensure_type(v, (int, float))]
    return valid

def sum_values(values):
    valid = filter_numeric_values(values)
    return sum(valid) if valid else 0

def count_values(values):
    valid = filter_numeric_values(values)
    return len(valid) if valid else 0

def average_values(values):
    valid = filter_numeric_values(values)
    return sum(valid) / len(valid) if valid else None

def max_value(values):
    valid = filter_numeric_values(values)
    return max(valid) if valid else None

def min_value(values):
    valid = filter_numeric_values(values)
    return min(valid) if valid else None

def percentage_difference(value_one, value_two):
    if not ensure_type(value_one, (int, float)):
        raise TransformTypeError(f"percent_diff: Expected int or float for 'value_one', got {type(value_one)}")
    if not ensure_type(value_two, (int, float)):
        raise TransformTypeError(f"percent_diff: Expected int or float for 'value_two', got {type(value_two)}")
    if value_two == 0:
        return None
    return ((value_one - value_two) / value_two) * 100

def replace_null(value, replacement="N/A"):
    if value is None:
        return replacement
    return value

def deduplicate_rows(data, key_columns):
    seen = set()
    result = []

    for row in data:
        key = tuple(row.get(col) for col in key_columns)
        if key not in seen:
            seen.add(key)
            result.append(row)

    return result

def concatenate_strings(values, sep=" "):
    return sep.join(str(v) for v in values if v is not None)

def find_string_in_column(value, search_string):
    if value is None:
        return False
    return search_string in str(value)

def add_to_date(date_value, days=0, months=0, years=0, date_format="%Y-%m-%d"):
    date_value = parse_date_safe(date_value, date_format)
    if date_value is None:
        return None
    return date_value + relativedelta(days=days, months=months, years=years)

def parse_date_safe(value, date_format):
    try:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.strptime(value, date_format)
        return None
    except (ValueError, TypeError) as e:
        logger.debug(f"Failed to parse date '{value}': {e}")
        return None

def date_difference(date1, date2, unit="days", date_format="%Y-%m-%d", swap_if_first_date_less_than_second=False):
    date1 = parse_date_safe(date1, date_format)
    date2 = parse_date_safe(date2, date_format)
    if date1 is None or date2 is None:
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
    else:
        logger.debug(f"Invalid unit '{unit}' passed to date_difference")
        return None

def date_difference_precise(date1, date2, date_format="%Y-%m-%d", swap_if_first_date_less_than_second=False):
    date1 = parse_date_safe(date1, date_format)
    date2 = parse_date_safe(date2, date_format)
    if date1 is None or date2 is None:
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

def filter_by_date(data, column, start=None, end=None, date_format="%Y-%m-%d"):
    result = []

    start_dt = parse_date_safe(start, date_format) if start else None
    end_dt = parse_date_safe(end, date_format) if end else None

    for row in data:
        value = parse_date_safe(row.get(column), date_format)
        if value is None:
            continue
        if start_dt and value < start_dt:
            continue
        if end_dt and value > end_dt:
            continue
        result.append(row)

    return result

AGGREGATION_FUNCTIONS = {
    "sum_values": sum_values,
    "average_values": average_values,
    "min_value": min_value,
    "max_value": max_value,
    "count_values": count_values,
}

def group_by_aggregate(data, group_by_columns, aggregations):
    """
    data: list of dicts
    group_by_columns: list of columns to group by
    aggregations: dict of column -> aggregation type

    Example:
    group_by_columns = ["category"]
    aggregations = {
        "value": "sum_values",
        "price": "average_values"
    }
    """

    grouped = {}

    # Step 1: Group rows
    for row in data:
        key = tuple(row.get(col) for col in group_by_columns)

        if key not in grouped:
            grouped[key] = []
        grouped[key].append(row)

    # Step 2: Aggregate
    result = []

    for key, rows in grouped.items():
        new_row = {}

        # Add group by columns back
        for i, col in enumerate(group_by_columns):
            new_row[col] = key[i]

        # Apply aggregations
        for col, agg_type in aggregations.items():
            values = [r[col] for r in rows if col in r and r[col] is not None]

            func = AGGREGATION_FUNCTIONS.get(agg_type)

            if func:
                new_row[col] = func(values)
            else:
                logger.warning(f"Unknown aggregation '{agg_type}' for column '{col}'")
                new_row[col] = None

        result.append(new_row)

    return result

TRANSFORM_FUNCTIONS = {}

def register_transform(name):
    def decorator(func):
        TRANSFORM_FUNCTIONS[name] = func
        return func
    return decorator

@register_transform("multiply")
def transform_multiply(data, params):
    col = params.get("column")
    if not col:
        logger.warning("Missing 'column' in multiply")
        return data

    factor = params.get("factor", 1)

    for row in data:
        if col in row:
            row[col] = multiply(row[col], factor)

    logger.info(f"Multiplied column '{col}' by {factor}")
    return data

@register_transform("add")
def transform_add(data, params):
    col = params.get("column")
    if not col:
        logger.warning("Missing 'column' in add")
        return data

    value = params.get("value", 0)

    for row in data:
        if col in row:
            row[col] = add(row[col], value)
        else:
            logger.debug(f"Column '{col}' missing in row: {row}")

    logger.info(f"Added {value} to column '{col}'")
    return data

@register_transform("subtract")
def transform_subtract(data, params):
    col = params.get("column")
    if not col:
        logger.warning("Missing 'column' in subtract")
        return data

    value = params.get("value", 0)

    for row in data:
        if col in row:
            row[col] = subtract(row[col], value)
        else:
            logger.debug(f"Column '{col}' missing in row: {row}")
    logger.info(f"Subtracted {value} from column '{col}'")
    return data

@register_transform("divide")
def transform_divide(data, params):
    col = params.get("column")
    if not col:
        logger.warning("Missing 'column' in divide")
        return data

    value = params.get("value", 1)

    for row in data:
        if col in row:
            row[col] = divide(row[col], value)
        else:
            logger.debug(f"Column '{col}' missing in row: {row}")
    logger.info(f"Divided column '{col}' by {value}")
    return data

@register_transform("modulus")
def transform_modulus(data, params):
    col = params.get("column")
    if not col:
        logger.warning("Missing 'column' in modulus")
        return data

    value = params.get("value", 1)

    for row in data:
        if col in row:
            row[col] = modulus(row[col], value)
        else:
            logger.debug(f"Column '{col}' missing in row: {row}")
    logger.info(f"Applied modulus {value} to column '{col}'")
    return data

@register_transform("replace_null")
def transform_replace_null(data, params):
    col = params.get("column")
    if not col:
        logger.warning("Missing 'column' in replace_null")
        return data

    replacement = params.get("replacement", "N/A")

    for row in data:
        if col in row:
            row[col] = replace_null(row[col], replacement)
        else:
            logger.debug(f"Column '{col}' missing in row: {row}")
    logger.info(f"Replaced nulls in column '{col}' with '{replacement}'")
    return data

@register_transform("deduplicate_rows")
def transform_deduplicate_rows(data, params):
    key_cols = params.get("key_columns")
    if not key_cols:
        logger.warning("Missing 'key_columns' in deduplicate_rows")
        return data

    return deduplicate_rows(data, key_cols)

@register_transform("filter_by_date")
def transform_filter_by_date(data, params):
    column = params.get("column")
    if not column:
        logger.warning("Missing 'column' in filter_by_date")
        return data

    start = params.get("start")
    end = params.get("end")

    return filter_by_date(data, column, start=start, end=end)

@register_transform("add_to_date")
def transform_add_to_date(data, params):
    column = params.get("column")
    target = params.get("target_column")

    if not column or not target:
        logger.warning("Missing 'column' or 'target_column' in add_to_date")
        return data

    days = params.get("days", 0)
    months = params.get("months", 0)
    years = params.get("years", 0)

    for row in data:
        if column in row:
            row[target] = add_to_date(
                row[column],
                days=days,
                months=months,
                years=years
            )

    return data

@register_transform("date_difference")
def transform_date_difference(data, params):
    col1 = params.get("column1")
    col2 = params.get("column2")
    target = params.get("target_column")

    if not col1 or not col2 or not target:
        logger.warning("Missing required params in date_difference")
        return data

    swap = params.get("swap_if_first_date_less_than_second", False)
    date_format = params.get("date_format", "%Y-%m-%d")
    unit = params.get("unit", "days")

    for row in data:
        if col1 in row and col2 in row:
            row[target] = date_difference(
                row[col1],
                row[col2],
                unit=unit,
                date_format=date_format,
                swap_if_first_date_less_than_second=swap
            )

    return data


@register_transform("date_difference_precise")
def transform_date_difference_precise(data, params):
    col1 = params.get("column1")
    col2 = params.get("column2")
    target = params.get("target_column")

    if not col1 or not col2 or not target:
        logger.warning("Missing required params in date_difference_precise")
        return data

    swap = params.get("swap_if_first_date_less_than_second", False)
    date_format = params.get("date_format", "%Y-%m-%d")

    for row in data:
        if col1 in row and col2 in row:
            row[target] = date_difference_precise(
                row[col1],
                row[col2],
                date_format=date_format,
                swap_if_first_date_less_than_second=swap
            )

    return data


@register_transform("percentage_difference")
def transform_percentage_difference(data, params):
    col1 = params.get("column1")
    col2 = params.get("column2")
    target = params.get("target_column")

    if not col1 or not col2 or not target:
        logger.warning("Missing required params in percentage_difference")
        return data

    for row in data:
        if col1 in row and col2 in row:
            row[target] = percentage_difference(row[col1], row[col2])

    return data


@register_transform("sum_values")
def transform_sum_values(data, params):
    columns = params.get("columns")
    target = params.get("target_column")

    if not columns or not target:
        logger.warning("Missing 'columns' or 'target_column' in sum_values")
        return data

    for row in data:
        row[target] = sum_values([row[c] for c in columns if c in row])

    return data


@register_transform("count_values")
def transform_count_values(data, params):
    columns = params.get("columns")
    target = params.get("target_column")

    if not columns or not target:
        logger.warning("Missing 'columns' or 'target_column' in count_values")
        return data

    for row in data:
        row[target] = count_values([row[c] for c in columns if c in row])

    return data


@register_transform("average_values")
def transform_average_values(data, params):
    columns = params.get("columns")
    target = params.get("target_column")

    if not columns or not target:
        logger.warning("Missing 'columns' or 'target_column' in average_values")
        return data

    for row in data:
        row[target] = average_values([row[c] for c in columns if c in row])

    return data


@register_transform("max_value")
def transform_max_value(data, params):
    columns = params.get("columns")
    target = params.get("target_column")

    if not columns or not target:
        logger.warning("Missing 'columns' or 'target_column' in max_value")
        return data

    for row in data:
        row[target] = max_value([row[c] for c in columns if c in row])

    return data


@register_transform("min_value")
def transform_min_value(data, params):
    columns = params.get("columns")
    target = params.get("target_column")

    if not columns or not target:
        logger.warning("Missing 'columns' or 'target_column' in min_value")
        return data

    for row in data:
        row[target] = min_value([row[c] for c in columns if c in row])

    return data


@register_transform("group_by_aggregate")
def transform_group_by_aggregate(data, params):
    group_cols = params.get("group_by_columns")
    aggregations = params.get("aggregations")

    if not group_cols or not aggregations:
        logger.warning("Missing params in group_by_aggregate")
        return data

    return group_by_aggregate(data, group_cols, aggregations)


@register_transform("concatenate_strings")
def transform_concatenate_strings(data, params):
    columns = params.get("columns")
    target = params.get("target_column")

    if not columns or not target:
        logger.warning("Missing 'columns' or 'target_column' in concatenate_strings")
        return data

    sep = params.get("sep", " ")

    for row in data:
        row[target] = concatenate_strings(
            [row[c] for c in columns if c in row],
            sep
        )

    return data


@register_transform("find_string_in_column")
def transform_find_string_in_column(data, params):
    column = params.get("column")
    search_string = params.get("search_string")
    target = params.get("target_column")

    if not column or not target:
        logger.warning("Missing params in find_string_in_column")
        return data

    for row in data:
        if column in row:
            row[target] = find_string_in_column(row[column], search_string)

    return data


def transform_data(data, config):
    """
    Apply transformations based on config.
    config example:
    {
        "multiply": {"column": "value", "factor": 10},
        "replace_null": {"column": "name", "replacement": "N/A"},
        "deduplicate": {"key_columns": ["id"]}
    }

    NOTE: This function mutates input data in-place.
    """
    for operation, params in config.items():
        func = TRANSFORM_FUNCTIONS.get(operation)

        if not func:
            logger.warning(f"Unknown transformation: {operation}")
            continue

        try:
            data = func(data, params)
        except Exception as e:
            logger.exception(f"Error running transformation '{operation}': {e}")

    return data