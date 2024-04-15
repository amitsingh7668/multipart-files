import pandas as pd

# Sample CSV data
csv_data = """name,age,salary
Amit,30,qq
John,35,5000
Alice,25,45000"""

# Save the sample CSV data to a file
with open('sample.csv', 'w') as file:
    file.write(csv_data)

# Transformation list for updating column names and values
transformations = [
    {
        "column": "salary",
        "new_name": "new_salary",
        "value_mappings": [{"5000": "500002"},{"qq": "50000PSD"}]
    },
    {
        "column": "salary1",
        "new_name": "new_salary1",
        "value_mappings": [{"qq": "50000PSD"}]
    }
]

# Read the CSV file using pandas
df = pd.read_csv('sample.csv')

# Update column names and values
for transformation in transformations:
    old_name = transformation["column"]
    new_name = transformation["new_name"]
    value_mappings = transformation["value_mappings"]

    if old_name in df.columns:
        print(f"Updating column '{old_name}' to '{new_name}'")
        df.rename(columns={old_name: new_name}, inplace=True)

        print(f"Updating values in column '{new_name}'")
        for value_mapping in value_mappings:
            for old_value, new_value in value_mapping.items():
                df[new_name] = df[new_name].replace(old_value, new_value)

# Display the updated DataFrame
print(df)
