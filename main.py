from flask import Flask, request, Response
users = {
    "admin": 123,
    "guest": 456
}
app = Flask(__name__)

def authenticate():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return False
    user = users.get(auth.username)
    if not user or user != auth.password:
        return False
    return auth.username, auth.password

@app.route("/register")
def register():
    return '''
    <h1>Enter your username and password</h1>
    <form action="/submit_registration" method="post">
    <input type="text" name="username" id="username">
    <input type="password" name="password" id="password">
    <input type="submit" value="Submit">
    </form>
    '''

@app.route("/submit_registration", methods=['POST'])
def submit_registration():
    username = request.form['username']
    password = request.form['password']
    if password and username:
        users[username] = password
        return Response("User registered",200)
    else:
        return Response("Registration failed", 401)

def requires_auth(f):
    """Decorator to enforce HTTP basic auth."""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not authenticate():
            return authenticate_response()
        return f(*args, **kwargs)
    return decorated

def authenticate_response():
    return Response(
        'Could not verify your access!', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

@app.route("/create")
@requires_auth
def create():
    return "<p>Create!</p>"

@app.route("/update")
@requires_auth
def update():
    return "<p>Update!</p>"

@app.route("/read")
def read():
    return "<p>READ!</p>"

@app.route("/delete")
@requires_auth
def delete():
    return "<p>Delete!</p>"

