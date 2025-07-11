from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import io
import time
from backend.parser import extract_text_from_pdf
from backend.llm_interface import get_tailored_resume

app = FastAPI()
session_cache = {}

@app.get("/")
def home():
    return {"message": "Resume Optimizer is live!"} 

@app.post("/optimize")
async def optimize_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    api_key: str = Form(...),
    custom_prompt: str = Form(...),
    cache_key: str = Form(""),
    use_cache: bool = Form(False)
):
    resume_bytes = await resume.read()
    resume_text = extract_text_from_pdf(io.BytesIO(resume_bytes))

    # Cache API key
    if use_cache and cache_key:
        session_cache[cache_key] = {
            "key": api_key,
            "expires": time.time() + 1800
        }

    # Use cached key if exists
    key_to_use = api_key
    if use_cache and cache_key in session_cache:
        if session_cache[cache_key]["expires"] > time.time():
            key_to_use = session_cache[cache_key]["key"]
        else:
            del session_cache[cache_key]

    tailored = get_tailored_resume(
        resume_text=resume_text,
        job_description=job_description,
        api_key=key_to_use,
        prompt=custom_prompt
    )

    return {"tailored_resume": tailored}
