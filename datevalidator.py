import re
from datetime import datetime

def validate_date(date_value, date_format, pattern):
    # Step 1: Validate the format using regex
    if not re.match(pattern, date_value):
        return False, f"Date '{date_value}' does not match the expected format {date_format}."
    
    # Step 2: Validate the actual date using datetime
    try:
        datetime.strptime(date_value, date_format)
        return True, None
    except ValueError:
        return False, f"Date '{date_value}' is not a valid calendar date."

# Example usage
config = {
    "column_name": "Action Due Date",
    "date_format": "%d/%m/%Y",
    "description": "Date in the format: DD/MM/YYYY, example: 09/11/2023 or 28/02/2023",
    "pattern": "^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\\d{4}$"
}

# Test cases
test_dates = ["28/02/2023", "31/02/2023", "09/11/2023", "31/04/2023"]
for date in test_dates:
    is_valid, error = validate_date(date, config["date_format"], config["pattern"])
    if is_valid:
        print(f"Date '{date}' is valid.")
    else:
        print(f"Date '{date}' is invalid: {error}")
