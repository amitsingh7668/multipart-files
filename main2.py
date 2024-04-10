from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import csv
import io
from typing import List
import pandas as pd

app = FastAPI()


def csv_to_json1(csv_file, fields):
    """
    Convert CSV file to JSON format based on specified fields using Pandas.
    """
    # Convert the CSV file data into a DataFrame using Pandas
    df = pd.read_csv(io.BytesIO(csv_file), encoding='utf-8')

    # Check if all fields are present in the CSV file
    missing_fields = [field for field in fields.split(',') if field not in df.columns.tolist()]
    if missing_fields:
        missing_fields_str = ', '.join(missing_fields)
        raise HTTPException(status_code=400, detail=f"Field(s) {missing_fields_str} not found in the CSV file.")

    # Filter the DataFrame based on specified fields
    fields_list = fields.split(',')
    filtered_df = df[fields_list]

    # Convert the filtered DataFrame to JSON format
    json_data = filtered_df.to_dict(orient='records')
    
    return json_data


@app.post("/convert1/")
async def convert_csv_to_json1(fields: str = Form(...), file: UploadFile = File(...)):
    """
    Endpoint to upload a CSV file and convert it to JSON format based on specified fields.
    """
    if not file.filename.endswith('.csv'):
        return {"error": "Uploaded file must be a CSV file."}
    
    content = await file.read()
    json_data = csv_to_json1(content, fields)
    return json_data


def csv_to_json(content):
    """
    Convert CSV file to JSON format.
    """
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    
    # Convert DataFrame to JSON
    json_data = df.to_dict(orient='records')
    
    return json_data


@app.post("/convert/")
async def convert_csv_to_json(file: UploadFile = File(...)):
    """
    Endpoint to upload a CSV file and convert it to JSON format.
    """
    if not file.filename.endswith('.csv'):
        return {"error": "Uploaded file must be a CSV file."}
    
    content = await file.read()
    json_data = csv_to_json(content)
    return json_data


@app.get("/details/")
async def get_details():
    return "This is a CSV to JSON converter. Please upload a CSV file to convert it to JSON format."


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
