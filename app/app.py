from flask import Flask
from flask import make_response
app = Flask(__name__)


@app.route('/')
def main():
    return make_response(open('templates/index.html').read())


if __name__ == '__main__':
    app.run(debug=True)
