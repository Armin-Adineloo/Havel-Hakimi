from flask import Flask, render_template, request
from input_file import readfile
from Havel_Hakimi import havel_hakimi


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["graph"]
    file.save(file.filename)
    degrees = readfile(file.filename)
    degrees_copy = degrees.copy()

    if havel_hakimi(degrees_copy):
        result = "Graphic"
    else:
        result = "Not Graphic"

    return f"""
    <h2>File : {file.filename}</h2>
    <h3>Degree Sequence :</h3>
    <p>{degrees}</p>
    <h3>Result :</h3>
    <p>{result}</p>
    <br>
    <a href="/">Back</a>
    """

if __name__ == "__main__":
    app.run(debug=True)
