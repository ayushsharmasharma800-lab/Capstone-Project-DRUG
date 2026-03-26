from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Home Page"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "123":
            return "Login Success"
        else:
            return "Invalid Login"

    return "Login Page"

if __name__ == "__main__":
    app.run(debug=True)



