# -*- coding: utf-8 -*-

#set PYTHONPATH=Z:\Temp

import json
from flask import Flask, request, jsonify, make_response
import uhaha
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST','OPTIONS'])
def home():
    if request.method=='OPTIONS':
        res = make_response('')
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Method'] = '*'
        res.headers['Access-Control-Allow-Headers'] = '*'
        return res
    params = request.json if request.method == "POST" else request.args
    #res = make_response(jsonify({'code': 0,'data': {'username': 123, 'nickname': 'DSB'}}))
    #res = make_response(jsonify(params))
    res = uhaha.handle(params)
    res = make_response(json.dumps(res,ensure_ascii=False,separators=(',',':')))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Method'] = '*'
    res.headers['Access-Control-Allow-Headers'] = '*'
    return res

@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action="/signin" method="post">
<p><input name="username"></p>
<p><input name="password" type="password"></p>
<p><button type="submit">Sign In</button></p>
</form>'''

@app.route('/signin', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run(debug=True,host='10.0.16.6',port=5003)