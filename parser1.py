import pandas as pd
import json

def read_csv(file_path):
    “”"Reads a CSV file and returns a DataFrame.“”"
    return pd.read_csv(file_path)

def load_json(file_path):
    “”"Loads a JSON file and returns the parsed JSON object.“”"
    with open(file_path, ‘r’) as file:
        return json.load(file)

def map_data_to_dict(data, mapping):
    “”"
    Maps the DataFrame data to a dictionary based on the given mapping.
    This function works recursively to handle nested mappings and lists.
    “”"
    def map_row(row, mapping):
        “”"Maps a single row to a dictionary based on the given mapping.“”"
        if isinstance(mapping, dict):
            result = {}
            for key, value in mapping.items():
                if isinstance(value, (dict, list)):
                    result[key] = map_row(row, value)
                else:
                    result[key] = row[value]
            return result
        elif isinstance(mapping, list):
            result = []
            for item in mapping:
                result.append(map_row(row, item))
            return result
        else:
            return row[mapping]

    # Apply the mapping to each row in the DataFrame
    mapped_data = [map_row(row, mapping) for _, row in data.iterrows()]

    return mapped_data

def convert_csv_to_dict(csv_file, json_file):
    “”"Converts a CSV file to a dictionary based on the JSON mapping.“”"
    data = read_csv(csv_file)
    mapping = load_json(json_file)
    mapped_data = map_data_to_dict(data, mapping)
    return mapped_data

# Example usage
csv_file_path = ‘test.csv’
json_file_path = ‘te.json’

result_dict = convert_csv_to_dict(csv_file_path, json_file_path)
print(json.dumps(result_dict, indent=4))
