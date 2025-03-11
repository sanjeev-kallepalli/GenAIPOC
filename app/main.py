from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routers import router
import os
from dotenv import load_dotenv
import openai


# Load environment variables from config.env
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix='/api')

@app.on_event("startup")
def check_openai_api_key():
    api_key = os.environ.get('OPENAI_API_KEY')

    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return HTTPException(status_code=500, detail="could not validate token")
    else:
        return True

