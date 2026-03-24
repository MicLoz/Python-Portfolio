import logging

logger = logging.getLogger(__name__)

def multiply(number_for_multiply, value):
    return number_for_multiply * value

def add(number_for_addition, value):
    return number_for_addition + value

def subtract(number_for_subtraction, value):
    return number_for_subtraction - value

def divide(number_for_division, value):
    if value == 0:
        return None
    else:
        return number_for_division / value






def transform_data(data):
    """Transform data by adding a 'value_squared' field."""
    print("Transform: Squaring the 'value' column...")
    for row in data:
        row['value_squared'] = row['value'] ** 2
    print("Transform: Transformation complete.")
    return data