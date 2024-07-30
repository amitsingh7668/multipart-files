import pandas as pd
import json

def read_csv(file_path):
    """Reads a CSV file and returns a DataFrame."""
    return pd.read_csv(file_path)

def load_json(file_path):
    """Loads a JSON file and returns the parsed JSON object."""
    with open(file_path, 'r') as file:
        return json.load(file)

def apply_conversion_rule(value, rule):
    """
    Applies a conversion rule to a given value.
    The rule is expected to be a dictionary with 'replace' and optional 'default' keys.
    The 'replace' key specifies the replacement logic in the form {old_value: new_value}.
    The 'default' key specifies the default value if the original value is not found in 'replace'.
    """
    if 'replace' in rule:
        value_str = str(value)
        rule_dict = {str(k): v for k, v in rule['replace'].items()}
        return rule_dict.get(value_str, rule.get('default', value))
    return value

def map_data_to_dict(data, mapping):
    """
    Maps the DataFrame data to a dictionary based on the given mapping.
    This function works recursively to handle nested mappings and lists.
    """
    def map_row(row, mapping):
        """Maps a single row to a dictionary based on the given mapping."""
        if isinstance(mapping, dict):
            result = {}
            for key, value in mapping.items():
                if isinstance(value, dict):
                    if 'column' in value and 'rule' in value:
                        result[key] = apply_conversion_rule(row[value['column']], value['rule'])
                    else:
                        result[key] = map_row(row, value)
                elif isinstance(value, list):
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
    """Converts a CSV file to a dictionary based on the JSON mapping."""
    data = read_csv(csv_file)
    mapping = load_json(json_file)
    mapped_data = map_data_to_dict(data, mapping)
    return mapped_data
# Example usage
csv_file_path = 'test.csv'
json_file_path = 'te.json'

result_dict = convert_csv_to_dict(csv_file_path, json_file_path)
print(json.dumps(result_dict, indent=4))
