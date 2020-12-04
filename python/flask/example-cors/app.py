from flask import Flask, request
from flask_cors import CORS, cross_origin

# 浏览器才会有跨域问题
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:80"}})


@app.route('/foo', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def foo():
    return request.json['inputVar']


if __name__ == '__main__':
    app.run()
