from flask import Blueprint, render_template, request, jsonify, redirect, url_for, current_app
from flask_login import login_required, current_user
from openai import OpenAI
import openai
import os
import json
from .models import Flashcard

bp = Blueprint("student", __name__)

client = OpenAI(
    api_key=os.getenv("OPENAI"),
)

history = []

#####################################################
# Upload
#####################################################

def read_file_with_multiple_encodings(filepath, encodings=['utf-8', 'ISO-8859-1', 'cp1252']):
    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return "", ""  # Return empty values if the file doesn't exist

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                text = file.read()

                # Remove references section assuming it starts with 'References' or 'REFERENCES'
                ref_index = text.lower().find('references')
                if ref_index != -1:
                    text = text[:ref_index]
            
                return text.replace('\n', ' '), encoding
            
        except (UnicodeDecodeError, FileNotFoundError) as e:
            print(f"Failed to read file {filepath} with encoding {encoding}: {e}")
            continue  # Try the next encoding
    raise UnicodeDecodeError(
        "utf-8",  # encoding
        b"",  # object (empty because we don't have the byte sequence)
        0,  # start position
        0,  # end position
        f"Failed to decode file {filepath} with available encodings."
    )

#####################################################
# Flashcards
#####################################################

    
@bp.route("/flashcards")
def flashcards():
    # Query the flashcards from the database
    flashcards = Flashcard.query.all()

    # Convert the flashcards to a list of dictionaries
    flashcards_data = [{"Term": fc.term, "Definition": fc.definition} for fc in flashcards]

    # Pass the flashcards data to the template
    return render_template('student/flashcards.html', flashcards=flashcards_data)

@bp.route('/translate', methods=['POST'])
def translate_flashcard():
    data = request.json
    term = data.get('term')
    definition = data.get('definition')

    # Construct the prompt for translation
    prompt = (
        f'Translate the following text to German:\n\n'
        f'Term: {term}\nDefinition: {definition}\n\n'
        'Your response should be in the format:\n{"translated_term": "[Your translation here]", "translated_definition": "[Your translation here]"}'
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    # Extract the translated term and definition from the response
    translated = response.choices[0].message.content
    translated_data = json.loads(translated)

    return jsonify({
        "translated_term": translated_data.get('translated_term'),
        "translated_definition": translated_data.get('translated_definition')
    })

#####################################################
# Login
#####################################################

@bp.route('/student_landing')
@login_required
def landing():
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))
    return render_template("student/landing.html", name=current_user.name)

#####################################################
# Chatbot
#####################################################

@bp.route("/chatbot", methods=['GET', 'POST'])
@login_required
def chatbot():
    answer = ""
    if request.method == 'POST':
        submitted_text = request.form['textbox']
        answer = get_response(submitted_text)
        history.append((submitted_text, answer))
    
    return render_template("student/chatbot.html", message=history)

@bp.route("/app_response", methods=['GET', 'POST'])
def app_response():
    answer = ""
    submitted_text = request.args.get('text')
    
    if request.method == 'POST' or request.method == 'GET':
        answer = get_response(submitted_text)
        history.append((submitted_text, answer))
    
    return jsonify({"history": history})


def get_response(question):
    try:
        # Read the prompt_extension when needed
        file_path = os.path.join(current_app.instance_path, 'texts', 'text.txt')
        prompt_extension, used_encoding = read_file_with_multiple_encodings(file_path)

        # Define the initial messages for the conversation, ensuring they are concise
        initial_messages = [
            {
                "role": "system",
                "content": f"You are a STEM teacher. Answer the question accuarately. Explain concepts behind in a simple way with easy examples. Your students are in the age between 12 and 15. This is the course material: {prompt_extension}"
            },
            {
                "role": "user",
                "content": "How do we calculate a modulo? and what is the modulo?"
            },
            {
                "role": "assistant",
                "content": "Think of modulo as finding the remainder after division. For example, 10 mod 3 is 1 because 10 divided by 3 is 3 with a remainder of 1."
            },
            {
                "role": "user",
                "content": question
            }
        ]

        initial_token_count = sum(len(message['content'].split()) for message in initial_messages)

        # Trim the history to fit within the token limit
        max_total_tokens = 16385
        max_history_tokens = max_total_tokens - initial_token_count - 256  # 256 tokens reserved for response
        trimmed_history = []

        current_token_count = 0
        for q, a in reversed(history):
            q_tokens = len(q.split())
            a_tokens = len(a.split())
            if current_token_count + q_tokens + a_tokens <= max_history_tokens:
                trimmed_history.insert(0, {"role": "user", "content": q})
                trimmed_history.insert(0, {"role": "assistant", "content": a})
                current_token_count += q_tokens + a_tokens
            else:
                break

        # Combine the messages for the conversation
        messages = initial_messages + trimmed_history

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        processed = response.choices[0].message.content.strip()
        return processed
    
    except openai.RateLimitError as e:
        # Handle rate limit error gracefully
        print("Rate limit exceeded. Please wait and try again.")
        return "Rate limit exceeded. Please wait and try again."
    
    except openai.OpenAIError as e:
        # Handle other OpenAI API errors
        print(f"OpenAI API error: {e}")
        return f"OpenAI API error: {e}"

