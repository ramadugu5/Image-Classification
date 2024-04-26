import sqlite3

from flask import Flask, render_template, request, url_for, flash, redirect, session



app = Flask(__name__)
app.secret_key = 'your_secret_key'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    db = getattr(app, '_database', None)
    if db is None:
        db = sqlite3.connect("database.db")
        app._database = db
    return db
  
# def create_table():
#     conn = get_db()
#     cursor = conn.cursor()

#     cursor.execute('''CREATE TABLE IF NOT EXISTS recordings
#                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                       camera_data BLOB,
#                       audio_data BLOB)''')
#     conn.commit()  


# class Recording(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     camera_data = db.Column(db.LargeBinary)
#     audio_data = db.Column(db.LargeBinary)





@app.route('/home2')
def home2():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('login.html', posts=posts)


@app.route('/home3')
def home3():
    return render_template('home2.html')


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate the username and password (e.g., check against a da  tabase)
        # Replace this with your own validation logic

        if username == 'admin' and password == 'password':
            # Set the user as authenticated in the session
            session['authenticated'] = True
            return redirect(url_for('home3'))
        else:
            # Redirect to the login page with an error message
            return redirect(url_for('login'))

    return render_template('login.html')





@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route("/home")
def home():
    return render_template('dashboard.html')

@app.route('/record', methods=['POST'])
def record():
    camera_data = request.files['camera'].read()
    audio_data = request.files['audio'].read()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO recordings (camera_data, audio_data)
                      VALUES (?, ?)''', (camera_data, audio_data))
    conn.commit()

    return 'Data saved successfully'




if __name__ == '__main__':
    #create_table()
    app.run(debug=True, port=2024)