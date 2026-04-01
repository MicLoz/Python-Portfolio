import logging
from datetime import datetime, timedelta
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
    return number_for_division / value

def modulus(number_for_modulus, value):
    if not ensure_type(number_for_modulus, (int, float)):
        raise TransformTypeError(f"divide: Expected int or float for 'number_for_modulus', got {type(number_for_modulus)}")
    if not ensure_type(value, (int, float)):
        raise TransformTypeError(f"divide: Expected int or float for 'value', got {type(value)}")
    return number_for_modulus % value

def sum_values(values):
    if not values:
        return 0
    return sum(values)

def count_values(values):
    if not values:
        return 0
    return len(values)

def average_values(values):
    if not values:
        return None
    return sum(values) / len(values)

def max_value(values):
    if not values:
        return None
    return max(values)

def min_value(values):
    if not values:
        return None
    return min(values)

def percentage_difference(value_one, value_two):
    if value_one is None or value_two is None:
        return None
    if value_two == 0:
        return None  # avoid division by zero
    return ((value_one - value_two) / value_two) * 100

def replace_null(value, replacement="N/A"):
    if value is None:
        return replacement
    return value

def deduplicate_rows(data, key_columns):
    seen = set()
    result = []

    for row in data:
        key = tuple(row[col] for col in key_columns)
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
    if isinstance(date_value, str):
        date_value = datetime.strptime(date_value, date_format)
    return date_value + relativedelta(days=days, months=months, years=years)

def date_difference(date1, date2, unit="days", date_format="%Y-%m-%d"):
    if isinstance(date1, str):
        date1 = datetime.strptime(date1, date_format)
    if isinstance(date2, str):
        date2 = datetime.strptime(date2, date_format)

    delta = date1 - date2

    if unit == "days":
        return delta.days
    elif unit == "seconds":
        return delta.total_seconds()
    elif unit == "minutes":
        return delta.total_seconds() / 60
    elif unit == "hours":
        return delta.total_seconds() / 3600
    else:
        return None

def date_difference_precise(date1, date2, date_format="%Y-%m-%d"):
    if isinstance(date1, str):
        date1 = datetime.strptime(date1, date_format)
    if isinstance(date2, str):
        date2 = datetime.strptime(date2, date_format)

    if date1 < date2:
        date1, date2 = date2, date1  # ensure positive difference

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

    for row in data:
        value = row.get(column)

        if isinstance(value, str):
            value = datetime.strptime(value, date_format)

        if start:
            start_dt = datetime.strptime(start, date_format)
            if value < start_dt:
                continue

        if end:
            end_dt = datetime.strptime(end, date_format)
            if value > end_dt:
                continue
        result.append(row)

    return result


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
        key = tuple(row[col] for col in group_by_columns)

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
            values = [r[col] for r in rows if r[col] is not None]

            if agg_type == "sum_values":
                new_row[col] = sum_values(values)

            elif agg_type == "average_values":
                new_row[col] = average_values(values)

            elif agg_type == "min_value":
                new_row[col] = min_value(values)

            elif agg_type == "max_value":
                new_row[col] = max_value(values)

            elif agg_type == "count_values":
                new_row[col] = count_values(values)

            else:
                new_row[col] = None  # unknown aggregation

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
    """
    for operation, params in config.items():
        if operation == "multiply":
            col = params["column"]
            factor = params.get("factor", 1)
            for row in data:
                row[col] = multiply(row[col], factor)
            logger.info(f"Multiplied column '{col}' by {factor}")

        elif operation == "add":
            col = params["column"]
            value = params.get("value", 0)
            for row in data:
                row[col] = add(row[col], value)
            logger.info(f"Added {value} to column '{col}'")

        elif operation == "subtract":
            col = params["column"]
            value = params.get("value", 0)
            for row in data:
                row[col] = subtract(row[col], value)
            logger.info(f"Subtracted {value} from column '{col}'")

        elif operation == "divide":
            col = params["column"]
            value = params.get("value", 1)
            for row in data:
                row[col] = divide(row[col], value)
            logger.info(f"Divided column '{col}' by {value}")

        elif operation == "modulus":
            col = params["column"]
            value = params.get("value", 1)
            for row in data:
                row[col] = modulus(row[col], value)
            logger.info(f"Applied modulus {value} to column '{col}'")

        elif operation == "replace_null":
            col = params["column"]
            replacement = params.get("replacement", "N/A")
            for row in data:
                row[col] = replace_null(row[col], replacement)
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
                row[target] = add_to_date(row[column], days=days, months=months, years=years)

        elif operation == "date_difference":
            col1 = params["column1"]
            col2 = params["column2"]
            target = params["target_column"]
            unit = params.get("unit", "days")
            for row in data:
                row[target] = date_difference(row[col1], row[col2], unit=unit)

        elif operation == "percentage_difference":
            col1 = params["column1"]
            col2 = params["column2"]
            target = params["target_column"]
            for row in data:
                row[target] = percentage_difference(row[col1], row[col2])

        elif operation == "sum_values":
            columns = params["columns"]
            target = params["target_column"]
            for row in data:
                row[target] = sum_values([row[c] for c in columns])

        elif operation == "count_values":
            columns = params["columns"]
            target = params["target_column"]
            for row in data:
                row[target] = count_values([row[c] for c in columns])

        elif operation == "average_values":
            columns = params["columns"]
            target = params["target_column"]
            for row in data:
                row[target] = average_values([row[c] for c in columns])

        elif operation == "max_value":
            columns = params["columns"]
            target = params["target_column"]
            for row in data:
                row[target] = max_value([row[c] for c in columns])

        elif operation == "min_value":
            columns = params["columns"]
            target = params["target_column"]
            for row in data:
                row[target] = min_value([row[c] for c in columns])

        elif operation == "group_by_aggregate":
            group_cols = params["group_by_columns"]
            aggregations = params["aggregations"]
            data = group_by_aggregate(data, group_cols, aggregations)

        elif operation == "concatenate_strings":
            columns = params["columns"]
            target = params["target_column"]
            sep = params.get("sep", " ")
            for row in data:
                row[target] = concatenate_strings([row[c] for c in columns], sep)

        elif operation == "find_string_in_column":
            column = params["column"]
            search_string = params["search_string"]
            target = params["target_column"]
            for row in data:
                row[target] = find_string_in_column(row[column], search_string)

        else:
            logger.warning(f"Unknown transformation: {operation}")

    return data