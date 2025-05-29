from flask import Flask, render_template, request, redirect
import json
import os
import uuid
import datetime

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
                if 'completed' not in task:
                    task['completed'] = False
                    updated = True
                if 'completed_date' not in task:
                    task['completed_date'] = None
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
    active_tasks = [task for task in tasks if not task.get('completed', False)]
    return render_template('index.html', tasks=active_tasks)

@app.route('/add', methods=['POST'])
def add():
    task_title = request.form.get('title')
    due_date = request.form.get('due_date')
    if task_title:
        tasks = load_tasks()
        task_id = str(uuid.uuid4())
        tasks.append({
            'id': task_id, 
            'title': task_title, 
            'due_date': due_date,
            'completed': False,
            'completed_date': None
        })
        save_tasks(tasks)
    return redirect('/')

@app.route('/complete/<task_id>', methods=['POST'])
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
            task['completed_date'] = datetime.datetime.now().isoformat()
            break
    save_tasks(tasks)
    return redirect('/')

@app.route('/history')
def history():
    tasks = load_tasks()
    completed_tasks = [task for task in tasks if task.get('completed', False)]
    return render_template('history.html', tasks=completed_tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
