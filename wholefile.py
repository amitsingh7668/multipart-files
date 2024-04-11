import pandas as pd
import json
import logging

logging.basicConfig(level=logging.INFO)

# Step 1: Read CSV data into a Pandas DataFrame


def read_csv(file_path):
    return pd.read_csv(file_path)

# Step 2: Read JSON mapping sheet into a Python dictionary


def read_mapping(json_file_path):
    with open(json_file_path, 'r') as f:
        return json.load(f)

# Step 3: Create Python classes representing the business objects


class BusinessObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MyBusinessObject(BusinessObject):
    pass  # Add any specific logic or methods if needed

# Step 4: Map CSV columns to business object attributes


def map_data_to_objects(df, mapping):
    objects = []
    # Get column names from the DataFrame
    csv_columns = set(df.columns)

    for obj_name, obj_mapping in mapping.items():
        # Get required columns from the mapping
        required_columns = set(get_all_columns(obj_mapping))

        # Check if all required columns exist in the CSV
        missing_columns = required_columns - csv_columns
        if missing_columns:
            logging.info(
                f"Error: Required columns for '{obj_name}' not found in CSV file: {', '.join(missing_columns)}")
            continue

        for index, row in df.iterrows():
            obj_attrs = {}
            for obj_attr, csv_col in flatten_mapping(obj_mapping):
                obj_attrs[obj_attr] = row[csv_col]
            # Create an instance of the business object
            obj_class = globals().get(obj_name)
            if obj_class:
                obj = obj_class(**obj_attrs)
                objects.append(obj)
            else:
                logging.info(f"Error: Class '{obj_name}' not found.")
    return objects

# Helper function to flatten nested mapping


def flatten_mapping(mapping, prefix=''):
    flat_mapping = []
    for key, value in mapping.items():
        if isinstance(value, dict):
            flat_mapping.extend(flatten_mapping(
                value, prefix + key + '_NEXTOBJECT_'))
        else:
            flat_mapping.append((prefix + key, value))
    return flat_mapping

# Helper function to get all columns from nested mapping


def get_all_columns(mapping):
    columns = []
    for key, value in mapping.items():
        if isinstance(value, dict):
            columns.extend(get_all_columns(value))
        else:
            columns.append(value)
    return columns


# Step 5: Perform the conversion
def convert_csv_to_business_objects(csv_file_path, json_mapping_path):
    df = read_csv(csv_file_path)
    mapping = read_mapping(json_mapping_path)
    business_objects = map_data_to_objects(df, mapping)
    return business_objects


# Example usage
csv_file_path = 'data.csv'
json_mapping_path = 'mapping.json'
business_objects = convert_csv_to_business_objects(
    csv_file_path, json_mapping_path)
for obj in business_objects:
    logging.info(vars(obj))  # logging.info attributes of each business object
