# backend/llm_interface.py

from openai import OpenAI

def get_tailored_resume(resume_text: str, job_description: str, api_key: str, prompt: str = "") -> str:
    client = OpenAI(api_key=api_key)

    system_prompt = "You are an expert resume optimizer. Match user resume to job descriptions and output only the tailored content."

    user_prompt = f"""
    JOB DESCRIPTION:
    {job_description}

    RESUME TEXT:
    {resume_text}

    TASK:
    From the resume, extract and rewrite 3–5 of the most relevant projects/skills for the job.
    Output in plain text. {prompt}
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4,
        max_tokens=1000
    )

    return response.choices[0].message.content
