from flask import Flask, render_template, request, redirect, session
import re

app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET"

ADMIN_PASSWORD = "1234"
VIDEO_FILE = "video.txt"

def get_video_id(url):
    match = re.search(r"/d/([^/]+)", url)
    return match.group(1) if match else None

@app.route("/")
def index():
    try:
        with open(VIDEO_FILE, "r") as f:
            video_id = f.read().strip()
    except:
        video_id = None

    return render_template("index.html", video_id=video_id)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if "password" in request.form:
            if request.form["password"] == ADMIN_PASSWORD:
                session["admin"] = True
            else:
                return render_template("admin.html", error="รหัสผ่านไม่ถูกต้อง")

        elif "video_url" in request.form and session.get("admin"):
            video_id = get_video_id(request.form["video_url"])
            if video_id:
                with open(VIDEO_FILE, "w") as f:
                    f.write(video_id)
            return redirect("/")

    if not session.get("admin"):
        return render_template("admin.html")

    return render_template("admin.html", logged_in=True)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
