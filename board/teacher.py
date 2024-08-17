from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import PyPDF2
from openai import OpenAI
import json
from .models import Flashcard
from . import db

bp = Blueprint("teacher", __name__)

client = OpenAI(
    api_key=os.getenv("OPENAI"),
)

def clear_text(text):
    text_lines = text.split('\n')
    text_lines = text_lines[10:-10]
    text = '\n'.join(text_lines)

    ref_index = text.lower().find('references')
    if ref_index != -1:
        text = text[:ref_index]

    return text

def summarize(material):
    summary_prompt = f"Point out the core concepts of following course material in a way that fits within 600 tokens:\n\n{material}."
    summary_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": summary_prompt},
        ],
        max_tokens=600
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

def get_flashcards(text):
    chunks = text.split('\n\n') 
    flashcard_limit = 10

    prompt = (
        f'You are a STEM teacher. Create exactly {flashcard_limit} flashcards from the following content:\n\n{chunks}\n\n'
        '''
        Your response should have this format:\n
        [{"Term": "[Your term here]", "Definition": "[Your definition here]"}, {"Term": "[Your term here]", "Definition": "[Your definition here]"}, {"Term": "[Your term here]", "Definition": "[Your definition here]"}, ... ]
        Please do not include any numbers, labels, or extra text. Just give me the content as stated.
        '''
    )

        
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    card_content = response.choices[0].message.content.strip()
    return card_content

def make_database():
    traffic = json.load(open('instance/flashcards/flashcards.json'))
    columns = ['Term', 'Definition']

    for row in traffic:
        keys= tuple(row[c] for c in columns)
        flashcard = Flashcard.query.filter_by(term=keys[0]).first()
        # Check if flashcard exists
        if not flashcard:
            new_flashcard = Flashcard(term=keys[0], definition=keys[1] )
            db.session.add(new_flashcard)
            db.session.commit() 


@bp.route('/generate_flashcards', methods=['POST'])
def generate_flashcards():
    flashcards_folder = os.path.join(current_app.instance_path, 'flashcards')
    os.makedirs(flashcards_folder, exist_ok=True)
    file_path = os.path.join(current_app.instance_path, 'texts', 'text.txt')
    

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    flashcards = get_flashcards(text) or []

    upload_path = os.path.join(flashcards_folder, 'flashcards.json')
    flashcard_dict = json.loads(flashcards.replace('\n', ''))
    with open(upload_path, 'w', encoding='utf-8') as f:
        json.dump(flashcard_dict, f, indent=4)
    make_database()
    return render_template("teacher/upload.html", flashcards=flashcard_dict)


@bp.route('/upload_file', methods=['POST'])
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
        
        with open(upload_path, 'rb') as file:
            pdfreader = PyPDF2.PdfFileReader(file)
            num_pages = pdfreader.numPages
            
            text = ""
            for page_num in range(num_pages):
                pageobj = pdfreader.getPage(page_num)
                extraction = clear_text(pageobj.extractText())
                text += extraction
            
            text_summa = summarize(text)
            
            text_path = os.path.join(text_folder, 'text.txt')
            with open(text_path, 'a', encoding='utf-8') as file1:
                file1.write(text_summa)
        
        return redirect(url_for('teacher.upload'))
    return render_template('teacher/upload.html')

@bp.route('/teacher_profile')
@login_required
def profile():
    return render_template('teacher/profile.html', name=current_user.name, email=current_user.email, school=current_user.school, surname=current_user.surname)