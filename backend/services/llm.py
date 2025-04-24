import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_diagnosis(blood_data, xray_data):
    prompt = f"""
    Blood test results: {blood_data}
    X-ray findings: {xray_data}

    Based on this, what potential issues could be affecting specific organs?
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
