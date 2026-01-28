from flask import Flask, render_template, send_file, request, abort
import os

app = Flask(__name__)

VIDEO_PATH = "videos/long.mp4"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video")
def video():
    if not os.path.exists(VIDEO_PATH):
        abort(404)

    # ✅ สำคัญมาก: conditional=True สำหรับคลิปยาว
    return send_file(
        VIDEO_PATH,
        mimetype="video/mp4",
        conditional=True
    )


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "1234":
            return render_template("admin.html", success=True)
        return render_template("admin.html", error=True)

    return render_template("admin.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
