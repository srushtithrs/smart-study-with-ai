import os
import json
import time
# pyrefly: ignore [missing-import]
from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
DATA_PATH = os.path.join(STATIC_DIR, 'data.json')

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    path = os.path.join(STATIC_DIR, filename)
    if os.path.exists(path) and os.path.commonpath([STATIC_DIR, path]) == STATIC_DIR:
        return send_from_directory(STATIC_DIR, filename)
    abort(404)


def load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(load_data())

@app.route('/api/login', methods=['POST'])
def login():
    body = request.json or {}
    username = body.get('username') or body.get('email') or 'Suji'
    # NOTE: This is a placeholder authentication for demo purposes.
    data = load_data()
    data['profileName'] = username
    save_data(data)
    return jsonify({ 'ok': True, 'profileName': username })

# ROUTINE endpoints
@app.route('/api/routine', methods=['GET','POST'])
def routine_list_create():
    data = load_data()
    routines = data.get('routine', [])
    if request.method == 'GET':
        return jsonify(routines)
    body = request.json or {}
    if not body.get('name') or not body.get('time'):
        return abort(400, 'name and time required')
    item = {
        'id': int(time.time()*1000),
        'name': body['name'],
        'time': body['time'],
        'icon': body.get('icon','📌'),
        'color': body.get('color','bg-gray-100')
    }
    routines.append(item)
    data['routine'] = routines
    save_data(data)
    return jsonify(item), 201

@app.route('/api/routine/<int:item_id>', methods=['DELETE'])
def routine_delete(item_id):
    data = load_data()
    routines = data.get('routine', [])
    newr = [r for r in routines if r.get('id') != item_id]
    data['routine'] = newr
    save_data(data)
    return jsonify({'ok': True})

# EXAMS endpoints
@app.route('/api/exams', methods=['GET','POST'])
def exams_list_create():
    data = load_data()
    exams = data.get('exams', [])
    if request.method == 'GET':
        return jsonify(exams)
    body = request.json or {}
    if not body.get('subject') or not body.get('date'):
        return abort(400, 'subject and date required')
    item = {
        'id': int(time.time()*1000),
        'subject': body['subject'],
        'date': body['date'],
        'time': body.get('time',''),
        'hours': int(body.get('hours',0))
    }
    exams.append(item)
    data['exams'] = exams
    save_data(data)
    return jsonify(item), 201

@app.route('/api/exams/<int:item_id>', methods=['DELETE'])
def exams_delete(item_id):
    data = load_data()
    exams = data.get('exams', [])
    data['exams'] = [e for e in exams if e.get('id') != item_id]
    save_data(data)
    return jsonify({'ok': True})

# QUESTIONS endpoints (for test mode)
@app.route('/api/questions', methods=['GET','POST'])
def questions_list_create():
    data = load_data()
    questions = data.get('questions', [])
    if request.method == 'GET':
        return jsonify(questions)
    body = request.json or {}
    if not body.get('question') or not body.get('options'):
        return abort(400, 'question and options required')
    item = {
        'id': int(time.time()*1000),
        'question': body['question'],
        'options': body['options'],
        'answer': body.get('answer')
    }
    questions.append(item)
    data['questions'] = questions
    save_data(data)
    return jsonify(item), 201

@app.route('/api/questions/<int:item_id>', methods=['DELETE'])
def questions_delete(item_id):
    data = load_data()
    questions = data.get('questions', [])
    data['questions'] = [q for q in questions if q.get('id') != item_id]
    save_data(data)
    return jsonify({'ok': True})

@app.route('/api/save', methods=['POST'])
def api_save():
    body = request.json or {}
    if not isinstance(body, dict):
        return abort(400)
    save_data(body)
    return jsonify({'ok': True})

if __name__ == '__main__':
    # run with: python backend/app.py
    app.run(host='0.0.0.0', port=5000, debug=True)
