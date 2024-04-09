from fastapi import FastAPI, File, UploadFile
import csv
import io

app = FastAPI()


def csv_to_json(csv_file):
    """
    Convert CSV file to JSON format.
    """
    csv_data = io.StringIO(csv_file.decode('utf-8'))
    reader = csv.DictReader(csv_data)
    json_data = []
    for row in reader:
        json_data.append(row)
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
async def convert_csv_to_json():
    return "This is a CSV to JSON converter. Please upload a CSV file to convert it to JSON format."


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

