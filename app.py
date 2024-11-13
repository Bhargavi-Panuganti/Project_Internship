from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('projects.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        project_name TEXT NOT NULL,
                        project_manager TEXT NOT NULL,
                        start_date TEXT NOT NULL,
                        end_date TEXT NOT NULL,
                        revised_end_date TEXT,
                        status TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

# Main route
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_manager = request.form['project_manager']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        revised_end_date = request.form['revised_end_date']
        status = request.form['status']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO projects (project_name, project_manager, start_date, end_date, revised_end_date, status) VALUES (?, ?, ?, ?, ?, ?)', 
                       (project_name, project_manager, start_date, end_date, revised_end_date, status))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()

    return render_template('index.html', projects=projects)

# Route to view a project
@app.route('/view/<int:project_id>')
def view_project(project_id):
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()
    conn.close()
    return render_template('view_project.html', project=project)  # Create a template to show project details

# Route to edit a project
@app.route('/edit/<int:project_id>', methods=('GET', 'POST'))
def edit_project(project_id):
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE id = ?', (project_id,)).fetchone()

    if request.method == 'POST':
        project_name = request.form['project_name']
        project_manager = request.form['project_manager']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        revised_end_date = request.form['revised_end_date']
        status = request.form['status']

        conn.execute('''
            UPDATE projects 
            SET project_name = ?, project_manager = ?, start_date = ?, end_date = ?, revised_end_date = ?, status = ?
            WHERE id = ?
        ''', (project_name, project_manager, start_date, end_date, revised_end_date, status, project_id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_project.html', project=project)  # Create a template to edit project details

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Explicitly call the table creation function
    app.run(debug=True)
