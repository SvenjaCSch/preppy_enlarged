from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import PyPDF2
from openai import OpenAI


bp = Blueprint("teacher", __name__)

client = OpenAI(
    api_key=os.getenv("OPENAI"),
)

def clear_text(text):
    # Remove headers and footers if they are in the first and last 1000 characters
    text_lines = text.split('\n')
    text_lines = text_lines[10:-10]
    text = '\n'.join(text_lines)

    ref_index = text.lower().find('references')
    if ref_index != -1:
        text = text[:ref_index]

    return text


def summarize(material):
            # Summarize the course material to fit within a smaller token limit
        summary_prompt = f"Point out the core concepts of following course material in a way that fits within 500 tokens:\n\n{material}."
        summary_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a assistant. Do not engage with the user."},
                {"role": "user", "content": summary_prompt}
            ],
            max_tokens=300
        )
        
        summarized_material = summary_response.choices[0].message.content.strip()
        return summarized_material

@bp.route('/teacher_landing')
@login_required
def landing():
    if current_user.role != 'teacher':
        return redirect(url_for('auth.login'))
    return render_template("teacher/landing.html", name=current_user.name)

@bp.route('/upload')
@login_required
def upload():
    return render_template('teacher/upload.html')

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        pdf_folder = os.path.join(current_app.instance_path, 'pdfs')
        text_folder = os.path.join(current_app.instance_path, 'texts')

        # Create directories if they don't exist
        os.makedirs(pdf_folder, exist_ok=True)
        os.makedirs(text_folder, exist_ok=True)

        upload_path = os.path.join(pdf_folder, secure_filename(f.filename))
        f.save(upload_path)
        
        # Open the saved file for reading
        with open(upload_path, 'rb') as file:
            pdfreader = PyPDF2.PdfFileReader(file)
            num_pages = pdfreader.numPages
            
            # Iterate through all pages and extract text
            text = ""
            for page_num in range(num_pages):
                pageobj = pdfreader.getPage(page_num)
                extraction = clear_text(pageobj.extractText())
                text += extraction
            
            text_summa = summarize(text)
            
            # Write the extracted text to a file
            text_path = os.path.join(text_folder, 'text.txt')
            with open(text_path, 'a', encoding='utf-8') as file1:
                file1.write(text_summa)
        
        return render_template('teacher/upload.html')