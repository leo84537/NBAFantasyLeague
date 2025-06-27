import webbrowser
from flask import Flask

app = Flask("NBA")

@app.route("/")
def home():
    return "WE ARE IN MOTION!"

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)