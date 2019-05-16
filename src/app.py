# coding: utf-8

from flask import Flask, request, make_response, redirect, abort
from users import Users

Users.initDatabase()

Users.register("hogehoge", "fugafuga", "/private,/hogehoge")

app = Flask(__name__)

@app.route('/auth/users', methods=['GET', 'POST'])
def register():    
    if request.method == 'POST':
        # ユーザ情報を追加
        result = Users.register(request.form['name'], request.form['password'], request.form['pathlist'])
        if result:
            # response = make_response(redirect('/'))
            # return response
            return 'success!', 201
        else:
            return 'Conflict', 409
        
    else:
        return '', 200

@app.route('/auth/is_auth')
def is_auth():
    if request.authorization:
        user = Users.find(request.authorization['username'])
        if user and user.auth(request.authorization['password']):
            origin_url = request.headers.get("X-Original-URI")
            if [l for l in user.getPathList() if origin_url.startswith(l)]:
                return '', 200
            else:
                return '', 403
        else:
            return '', 401
    else:    
        return '', 401

