from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/create")
def create():
    return "<p>Create!</p>"

@app.route("/update")
def update():
    return "<p>Update!</p>"

@app.route("/read")
def read():
    return "<p>READ!</p>"

@app.route("/delete")
def delete():
    return "<p>Delete!</p>"