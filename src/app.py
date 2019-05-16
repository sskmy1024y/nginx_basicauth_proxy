# coding: utf-8

from flask import Flask, request, make_response, redirect, abort
import json
import re

# 外部ファイルからユーザ情報を取得
f = open('users.json' , 'r')
users_list = json.load(f)

app = Flask(__name__)

@app.route('/auth/register', methods=['GET', 'POST'])
def register():    
    if request.method == 'POST':
        # PathListを配列に整形
        pathlist = re.split(',\r*\n*', request.form['pathlist'])
        # 配列にユーザ情報を追加
        users_list.append({'name': request.form['name'], 'password': request.form['password'], 'pathlist': pathlist})
        
        with open("users.json", "w") as f:
            json.dump(users_list, f)

        response = make_response(redirect('/'))
        return response
    else:
        return '', 200

@app.route('/auth/is_auth')
def is_auth():
    if request.authorization:
        user = [s for s in users_list if request.authorization['username'] == s['name'] and request.authorization['password'] == s['password']][0]
        if user:
            origin_url = request.headers.get("X-Original-URI")
            app.logger.debug(str(user['pathlist']))
            if [l for l in user['pathlist'] if origin_url.startswith(l)]:
                return '', 200
            else:
                return '', 403
        else:
            return '', 401
    else:    
        return '', 401

