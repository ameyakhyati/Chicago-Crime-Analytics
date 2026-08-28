from flask import Flask, render_template
from api.routes.crimes_route import crime_bp
import json


app = Flask(__name__)
app.register_blueprint(crime_bp)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/usecase1")
def usecase1():
    metadata_path = "metadata/metadata_crime_data.json"

    with open(metadata_path, "r") as file:
        metadata = json.load(file)

    return render_template("usecase1.html", metadata=metadata)


@app.route("/usecase2")
def usecase2():
    return render_template("usecase2.html")


@app.route("/usecase3")
def usecase3():
    return render_template("usecase3.html")


@app.route("/usecase4")
def usecase4():
    with open("static/analytics/usecase4.json", "r") as file:
        analytics = json.load(file)

    return render_template("usecase4.html", analytics=analytics)


if __name__ == "__main__":
    app.run(debug=True)
