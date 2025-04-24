import fitz  # PyMuPDF

def parse_blood_report(pdf_bytes):
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    # Dummy structured output for example
    return {
        "WBC": 8000,
        "RBC": 4.5,
        "Hemoglobin": 13.5
    }