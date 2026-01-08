from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def to_uppercase():
    user_name = request.args.get('name')

    if user_name:
        return f"<h1>{user_name.upper()}</h1>"
    else:
        return "<h1>Please provide a name in the URL.</h1>"

if __name__ == '__main__':
    app.run(debug=True)