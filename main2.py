from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import csv
import io
from typing import List
import pandas as pd

app = FastAPI()

def csv_to_json(csv_file, fields):
    """
    Convert CSV file to JSON format.
    """
    csv_data = io.StringIO(csv_file.decode('utf-8'))
    reader = csv.DictReader(csv_data)
    
    # Check if all required fields are present in the CSV header
    csv_header = next(reader)
    for field in fields:
        if field not in csv_header:
            raise HTTPException(status_code=400, detail=f"Field '{field}' is required but missing in the CSV file header.")
    
    json_data = []
    for row in reader:
        json_data.append(row)
    
    return json_data

@app.post("/convert/")
async def convert_csv_to_json(fields: List[str] = Form(...), file: UploadFile = File(...)):
    """
    Endpoint to upload a CSV file and convert it to JSON format.
    """
    if not file.filename.endswith('.csv'):
        return {"error": "Uploaded file must be a CSV file."}
    
    content = await file.read()
    json_data = csv_to_json(content, fields)
    return json_data

@app.get("/details/")
async def get_details():
    return "This is a CSV to JSON converter. Please upload a CSV file to convert it to JSON format."
