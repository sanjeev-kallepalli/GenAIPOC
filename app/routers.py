from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
import os
from operations.utils import save_to_local, process_message

router = APIRouter()

UPLOAD_FOLDER = "upload_data"  # Define the folder to save uploaded files

class ChatMessage(BaseModel):
    message: str

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"

    # Ensure the data folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    with open(file_location, "wb") as f:
        f.write(await file.read())
    resp = save_to_local(file_location)
    resp["location"] = file_location
    resp["filename"] = file.filename

    return resp

@router.post("/chat")
async def chat(message: ChatMessage):
    user_message = message.message
    llm_response = process_message(user_message)
    return {"response": llm_response}


    

    
