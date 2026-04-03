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
        if operation == "multiply":
            col = params["column"]
            if not col:
                logger.warning(f"Missing 'column' in params for {operation}")
                continue
            factor = params.get("factor", 1)
            for row in data:
                if col in row:
                    row[col] = multiply(row[col], factor)
                else:
                    logger.debug(f"Column '{col}' missing in row: {row}")
            logger.info(f"Multiplied column '{col}' by {factor}")

        elif operation == "add":
            col = params["column"]
            if not col:
                logger.warning(f"Missing 'column' in params for {operation}")
                continue
            value = params.get("value", 0)
            for row in data:
                if col in row:
                    row[col] = add(row[col], value)
                else:
                    logger.debug(f"Column '{col}' missing in row: {row}")
            logger.info(f"Added {value} to column '{col}'")

        elif operation == "subtract":
            col = params["column"]
            if not col:
                logger.warning(f"Missing 'column' in params for {operation}")
                continue
            value = params.get("value", 0)
            for row in data:
                if col in row:
                    row[col] = subtract(row[col], value)
                else:
                    logger.debug(f"Column '{col}' missing in row: {row}")
            logger.info(f"Subtracted {value} from column '{col}'")

        elif operation == "divide":
            col = params["column"]
            if not col:
                logger.warning(f"Missing 'column' in params for {operation}")
                continue
            value = params.get("value", 1)
            for row in data:
                if col in row:
                    row[col] = divide(row[col], value)
                else:
                    logger.debug(f"Column '{col}' missing in row: {row}")
            logger.info(f"Divided column '{col}' by {value}")

        elif operation == "modulus":
            col = params["column"]
            if not col:
                logger.warning(f"Missing 'column' in params for {operation}")
                continue
            value = params.get("value", 1)
            for row in data:
                if col in row:
                    row[col] = modulus(row[col], value)
                else:
                    logger.debug(f"Column '{col}' missing in row: {row}")
            logger.info(f"Applied modulus {value} to column '{col}'")

        elif operation == "replace_null":
            col = params["column"]
            if not col:
                logger.warning(f"Missing 'column' in params for {operation}")
                continue
            replacement = params.get("replacement", "N/A")
            for row in data:
                if col in row:
                    row[col] = replace_null(row[col], replacement)
                else:
                    logger.debug(f"Column '{col}' missing in row: {row}")
            logger.info(f"Replaced nulls in column '{col}' with '{replacement}'")

        elif operation == "deduplicate_rows":
            key_cols = params["key_columns"]
            data = deduplicate_rows(data, key_cols)

        elif operation == "filter_by_date":
            column = params["column"]
            start = params.get("start")
            end = params.get("end")
            data = filter_by_date(data, column, start=start, end=end)

        elif operation == "add_to_date":
            column = params["column"]
            target = params["target_column"]
            days = params.get("days", 0)
            months = params.get("months", 0)
            years = params.get("years", 0)
            for row in data:
                if column in row:
                    row[target] = add_to_date(row[column], days=days, months=months, years=years)

        elif operation == "date_difference":
            col1 = params["column1"]
            col2 = params["column2"]
            target = params["target_column"]
            swap = params.get("swap_if_first_date_less_than_second", False)  # default False
            date_format = params.get("date_format", "%Y-%m-%d")  # default %Y-%m-%d
            unit = params.get("unit", "days")
            for row in data:
                if col1 in row and col2 in row:
                    row[target] = date_difference(
                        row[col1],
                        row[col2],
                        date_format=date_format,
                        swap_if_first_date_less_than_second=swap,
                        unit=unit
                    )

        elif operation == "date_difference_precise":
            col1 = params["column1"]
            col2 = params["column2"]
            target = params["target_column"]
            swap = params.get("swap_if_first_date_less_than_second", False)  # default False
            date_format = params.get("date_format", "%Y-%m-%d") # default %Y-%m-%d
            for row in data:
                if col1 in row and col2 in row:
                    row[target] = date_difference_precise(
                        row[col1],
                        row[col2],
                        date_format=date_format,
                        swap_if_first_date_less_than_second=swap
                    )


        elif operation == "percentage_difference":
            col1 = params["column1"]
            col2 = params["column2"]
            target = params["target_column"]
            for row in data:
                if col1 in row and col2 in row:
                    row[target] = percentage_difference(row[col1], row[col2])

        elif operation == "sum_values":
            columns = params["columns"]
            target = params["target_column"]
            for row in data:
                row[target] = sum_values([row[c] for c in columns if c in row])

        elif operation == "count_values":
            columns = params["columns"]
            target = params["target_column"]
            for row in data:
                row[target] = count_values([row[c] for c in columns if c in row])

        elif operation == "average_values":
            columns = params["columns"]
            target = params["target_column"]
            for row in data:
                row[target] = average_values([row[c] for c in columns if c in row])

        elif operation == "max_value":
            columns = params["columns"]
            target = params["target_column"]
            for row in data:
                row[target] = max_value([row[c] for c in columns if c in row])

        elif operation == "min_value":
            columns = params["columns"]
            target = params["target_column"]
            for row in data:
                row[target] = min_value([row[c] for c in columns if c in row])

        elif operation == "group_by_aggregate":
            group_cols = params["group_by_columns"]
            aggregations = params["aggregations"]
            data = group_by_aggregate(data, group_cols, aggregations)

        elif operation == "concatenate_strings":
            columns = params["columns"]
            target = params["target_column"]
            sep = params.get("sep", " ")
            for row in data:
                row[target] = concatenate_strings([row[c] for c in columns if c in row], sep)

        elif operation == "find_string_in_column":
            column = params["column"]
            search_string = params["search_string"]
            target = params["target_column"]
            for row in data:
                if column in row:
                    row[target] = find_string_in_column(row[column], search_string)

        else:
            logger.warning(f"Unknown transformation: {operation}")

    return data