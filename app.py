from flask import Flask, request, jsonify
import json
import random
import os

app = Flask(__name__)

# Data file
DATA_FILE = 'flashcards.json'

# Initialize data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# Rule-based subject detection
def detect_subject(question):
    keywords = {
        "Physics": ["force", "acceleration", "velocity", "gravity", "newton"],
        "Biology": ["photosynthesis", "cell", "plant", "organism", "enzyme"],
        "Chemistry": ["atom", "molecule", "reaction", "acid", "base"],
        "Math": ["algebra", "equation", "geometry", "calculus", "matrix"]
    }
    for subject, words in keywords.items():
        if any(word.lower() in question.lower() for word in words):
            return subject
    return "General"

# Root route
@app.route('/')
def home():
    return "Flashcard Backend API is running!"

# Add flashcard endpoint
@app.route('/flashcard', methods=['POST'])
def add_flashcard():
    data = request.json
    subject = detect_subject(data['question'])

    # Read existing data
    with open(DATA_FILE, 'r') as f:
        flashcards = json.load(f)

    flashcards.append({
        "student_id": data['student_id'],
        "question": data['question'],
        "answer": data['answer'],
        "subject": subject
    })

    # Save updated data
    with open(DATA_FILE, 'w') as f:
        json.dump(flashcards, f, indent=4)

    return jsonify({"message": "Flashcard added successfully", "subject": subject})

# Get flashcards endpoint
@app.route('/get-subject', methods=['GET'])
def get_flashcards():
    student_id = request.args.get('student_id')
    limit = int(request.args.get('limit', 5))

    # Read data
    with open(DATA_FILE, 'r') as f:
        flashcards = json.load(f)

    student_flashcards = [fc for fc in flashcards if fc['student_id'] == student_id]
    random.shuffle(student_flashcards)
    return jsonify(student_flashcards[:limit])

if __name__ == '__main__':
    app.run(debug=True)
