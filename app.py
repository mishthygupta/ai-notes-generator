from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os
import PyPDF2

app = Flask(__name__)

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content

    return text

def generate_summary(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Notes App"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    print("API RESPONSE:", result)

    if "choices" in result:
        return result['choices'][0]['message']['content']
    else:
        return str(result)

@app.route("/", methods=["GET", "POST"])
def index():
    print("Route hit")

    summary = ""

    if request.method == "POST":
        print("POST received")

        text = request.form.get("text")

        if "pdf" in request.files:
            pdf = request.files["pdf"]

            if pdf and pdf.filename != "":
                text = extract_text_from_pdf(pdf)

        if text:
            summary = generate_summary(text)

    return render_template("index.html", summary=summary)


if __name__ == "__main__":
    app.run(debug=True)



