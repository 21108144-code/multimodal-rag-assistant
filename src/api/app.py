from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
import io
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.inference.server import get_pipeline
from src.utils.metrics import REQUEST_COUNT, REQUEST_LATENCY, track_latency
from src.config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.mount("/static", StaticFiles(directory="src/api/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('src/api/static/index.html')

class Message(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    text: str
    history: List[Message] = []

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    REQUEST_COUNT.labels(method="POST", endpoint="/query", status="200").inc()
    try:
        pipeline = get_pipeline()
        result = pipeline.query(request.text, history=request.history)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/image", response_model=QueryResponse)
async def query_image_endpoint(file: UploadFile = File(...)):
    REQUEST_COUNT.labels(method="POST", endpoint="/query/image", status="200").inc()
    pipeline = get_pipeline()
    try:
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        result = pipeline.query(image)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics():
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
