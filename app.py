from flask import Flask, render_template, request, redirect
import json
import os
import uuid

app = Flask(__name__)
DATA_FILE = 'data.json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            tasks = json.load(f)
            updated = False
            for task in tasks:
                if 'id' not in task:
                    task['id'] = str(uuid.uuid4())
                    updated = True
            if updated:
                save_tasks(tasks)
            return tasks
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task_title = request.form.get('title')
    if task_title:
        tasks = load_tasks()
        task_id = str(uuid.uuid4())
        tasks.append({'id': task_id, 'title': task_title})
        save_tasks(tasks)
    return redirect('/')

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
