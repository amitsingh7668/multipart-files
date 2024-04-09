from fastapi import FastAPI, File, UploadFile, Form
from typing import List
import pandas as pd

app = FastAPI()


def csv_to_json(csv_file, fields):
    """
    Convert CSV file to JSON format based on specified fields using Pandas.
    """
    # Convert the CSV file data into a DataFrame using Pandas
    df = pd.read_csv(io.BytesIO(csv_file), encoding='utf-8')

    # Filter the DataFrame based on specified fields
    filtered_df = df[fields]

    # Convert the filtered DataFrame to JSON format
    json_data = filtered_df.to_json(orient='records')
    
    return json_data


@app.post("/convert/")
async def convert_csv_to_json(fields: List[str] = Form(...), file: UploadFile = File(...)):
    """
    Endpoint to upload a CSV file and convert it to JSON format based on specified fields.
    """
    if not file.filename.endswith('.csv'):
        return {"error": "Uploaded file must be a CSV file."}
    
    content = await file.read()
    json_data = csv_to_json(content, fields)
    return json_data
