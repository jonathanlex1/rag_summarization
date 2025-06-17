from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os 
from module import stuff_document_summarization, map_reduce_summarization

class Response(BaseModel) : 
    response : str 

app = FastAPI()

@app.get('/') 
def home() : 
    return {'message' : 'hello'}


@app.post('/url_summary', response_model=Response) 
def summarize(path) : 
    summary = stuff_document_summarization(path)
    return Response(response=summary)

@app.post('/document_summary', response_model=Response)
async def documment_summarize(path:UploadFile=File(...)) : 
    file_dir = 'data/'
    if not os.path.exists(file_dir) : 
        os.makedirs(file_dir, exist_ok=True)

    filename = path.filename
    file_path = os.path.join(file_dir, filename)

    with open(file_path, 'wb') as f : 
        f.write(await path.read())

    summary = stuff_document_summarization(file_path) 
    return Response(response=summary)