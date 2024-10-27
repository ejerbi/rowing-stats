from flask import Flask, render_template, redirect
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    subprocess.Popen(["streamlit", "run", "dashboard.py", "--server.headless", "true"])
    return redirect("http://localhost:8501")
if __name__ == '__main__':
    app.run(debug=True)
