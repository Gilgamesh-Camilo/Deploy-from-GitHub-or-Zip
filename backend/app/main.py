from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uuid, os
from app.ml.pipeline import train_model, infer_from_model
from app.storage import save_file

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post('/upload-csv')
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    uid = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{uid}.csv")
    await save_file(file, path)
    df = pd.read_csv(path, nrows=100)
    return {"id": uid, "filename": file.filename, "preview": df.head(5).to_dict(orient='records')}

@app.post('/train')
async def train(job_name: str = Form(...), file_id: str = Form(...), target: str = Form(...), model_type: str = Form(...)):
    csv_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV not found")
    metrics, model_path = train_model(csv_path, target, model_type)
    return {"job": job_name, "metrics": metrics, "model_path": model_path}

@app.post('/predict')
async def predict(model_path: str = Form(...), payload: str = Form(...)):
    import json
    payload_rows = json.loads(payload)
    preds = infer_from_model(model_path, payload_rows)
    return {"predictions": preds}
