# backend/main.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Optional: allow frontend to connect if you're using Streamlit or React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Smart Resume Optimizer API is running."}

@app.post("/optimize")
async def optimize_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Placeholder logic
    resume_text = await resume.read()
    return JSONResponse(content={
        "received_file_name": resume.filename,
        "job_description_snippet": job_description[:100],
        "status": "Success. Ready for processing!"
    })
