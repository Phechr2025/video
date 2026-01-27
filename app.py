from flask import Flask, render_template, request, redirect, session
from config import ADMIN_PASSWORD
import re, os

app = Flask(__name__)
app.secret_key = "change_this_secret"

video_link = None

def drive_to_direct(url):
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return None

@app.route('/')
def home():
    return render_template('player.html', video=video_link)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global video_link
    if not session.get('admin'):
        return redirect('/login')

    if request.method == 'POST':
        url = request.form['drive']
        video_link = drive_to_direct(url)

    return render_template('admin.html', video=video_link)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# 🔥 จุดสำคัญที่สุดสำหรับ Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
