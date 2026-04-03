import pandas as pd
import numpy as np

def generate_test_data():
    data = [
        # 1. Clean row (baseline)
        {"id": 1, "age": 25, "price": 10.5, "quantity": 2, "date": "2024-01-15",
         "category": "A", "text": "I am a clean baseline row"},

        # 2. Nulls everywhere
        {"id": 2, "age": None, "price": None, "quantity": None, "date": None,
         "category": None, "text": None},

        # 3. Empty strings vs None
        {"id": 3, "age": "", "price": "", "quantity": "", "date": "",
         "category": "", "text": ""},

        # 4. Mixed numeric types (string numbers)
        {"id": 4, "age": "30", "price": "99.99", "quantity": "5",
         "date": "2024-02-01", "category": "B", "text": "string numbers"},

        # 5. Invalid numbers and invalid date
        {"id": 5, "age": "abc", "price": "??", "quantity": -10,
         "date": "2024-02-30", "category": "C", "text": "bad numbers"},

        # 6. Different date formats
        {"id": 6, "age": 40, "price": 50.0, "quantity": 3,
         "date": "15/03/2024", "category": "A", "text": "different date format"},
        {"id": 10, "age": 63, "price": 34.7, "quantity": 90,
         "date": "2021-12-29 11:34:59.996", "category": "A", "text": "different date format"},
        {"id": 11, "age": 50, "price": 20.0, "quantity": 5,
         "date": "2023/12/31", "category": "B", "text": "US/ISO date formats"},
        {"id": 12, "age": 45, "price": 15.0, "quantity": 10,
         "date": "12-25-2023", "category": "B", "text": "MM-DD-YYYY format"},

        # 7. Extreme numeric values
        {"id": 7, "age": 999999999, "price": 1e308, "quantity": 0,
         "date": "1900-01-01", "category": "Z", "text": "extreme values"},
        {"id": 13, "age": -999, "price": -1e308, "quantity": -5,
         "date": "2025-12-31", "category": "X", "text": "negative extreme values"},
        {"id": 14, "age": np.inf, "price": -np.inf, "quantity": np.nan,
         "date": "2025-06-30", "category": "Y", "text": "inf, -inf, NaN"},

        # 8. Duplicate rows
        {"id": 1, "age": 25, "price": 10.5, "quantity": 2,
         "date": "2024-01-15", "category": "A", "text": "duplicate with baseline"},

        # 9. Missing keys entirely
        {"id": 8},

        # 10. Weird strings
        {"id": 9, "age": 20, "price": 15.5, "quantity": 1, "date": "2024-01-01",
         "category": "A", "text": "🔥 unicode \n newlines \t tabs !!!"},

        # 11. Very long strings
        {"id": 15, "age": 35, "price": 100.0, "quantity": 5,
         "date": "2024-03-15", "category": "C", "text": "x"*1000},

        # 12. Out-of-order dates (for date difference testing)
        {"id": 16, "age": 30, "price": 50.0, "quantity": 2,
         "date": "2025-01-01", "category": "D", "text": "future date"},
        {"id": 17, "age": 28, "price": 60.0, "quantity": 3,
         "date": "2023-01-01", "category": "D", "text": "past date"},

        # 13. Strings with separators (for concatenation testing)
        {"id": 18, "age": 40, "price": 75.0, "quantity": 4,
         "date": "2024-07-07", "category": "E", "text": "hello|world|test"},
    ]

    return pd.DataFrame(data)