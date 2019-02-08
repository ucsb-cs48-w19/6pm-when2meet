from flask import Flask
app = Flask(__name__)

@app.route('/')
def userSelection():
    return "selected"

if __name__ == "__main__":
    app.run();
