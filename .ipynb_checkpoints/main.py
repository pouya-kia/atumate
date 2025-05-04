# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import pipeline_router

app = FastAPI()

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include pipeline routes
app.include_router(pipeline_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Pipeline API is running"}
