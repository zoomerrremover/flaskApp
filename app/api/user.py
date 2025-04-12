@app.route("/create",methods=['POST'])
@requires_auth
def create():
    return "<p>Create!</p>"

@app.route("/update",methods=['PUT'])
@requires_auth
def update():
    return "<p>Update!</p>"

@app.route("/read",methods=['GET'])
def read():
    return "<p>READ!</p>"

@app.route("/delete",methods=['DELETE'])
@requires_auth
def delete():
    return "<p>Delete!</p>"