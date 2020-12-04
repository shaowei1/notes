import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/index")
def index_test():
    print("index test,sleep for 15 second")
    time.sleep(15)
    return "index test for non-block"

if __name__ == '__main__':
    print(__name__)
    app.run(host="0.0.0.0", port=8088, debug=True)

"""
1. 访问 http://127.0.0.1:8088/index
2. 15s内新tab访问 http://127.0.0.1:8088/
==> 没有被阻塞
"""