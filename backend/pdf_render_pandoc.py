import subprocess
import tempfile
import os

def render_pandoc_resume(markdown_text: str) -> bytes:
    with tempfile.TemporaryDirectory() as tmpdir:
        md_path = os.path.join(tmpdir, "resume.md")
        pdf_path = os.path.join(tmpdir, "resume.pdf")

        # Save markdown content
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        # Generate PDF with custom formatting
        subprocess.run([
            "pandoc", md_path,
            "-o", pdf_path,
            "--variable", "fontsize=9pt",              
            "-V", "geometry:margin=0.6in"               
        ], check=True)

        # Read PDF bytes
        with open(pdf_path, "rb") as f:
            return f.read()
