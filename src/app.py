# coding: utf-8

from flask import Flask, request, make_response, redirect, abort
from users import Users
import json

Users.initDatabase()

Users.register('admin', 'root', '/')

app = Flask(__name__)

@app.route('/auth/users', methods=['GET', 'POST'])
def register():
    if is_auth()[1] == 200:
        if request.method == 'POST':
            # ユーザ情報を追加
            params = request.get_json()
            result = Users.register(params['name'], params['password'], params['pathlist'])
            if result:
                return json.dumps(result.toJSON()), 201
            else:
                return json.dumps('409 Conflict'), 409
            
        elif request.method == 'GET':
            return Users.getUserLists(), 200
    else:
        return json.dumps('403 Forbidden'), 403


@app.route('/auth/users/<int:usersid>', methods=['GET', 'PUT', 'DELETE'])
def show_users(usersid):
    if is_auth()[1] == 200:
        if request.method == 'GET':
            user = Users.findById(usersid)
            if user:
                return json.dumps(user.toJSON())
            else:
                return json.dumps('User is not found'), 404

        elif request.method == 'PUT':     
            user = Users.findById(usersid)
            if user:
                params = request.get_json()
                user.setName(params['name']) if "name" in params else None
                user.setPassword(params['password']) if "password" in params else None
                user.setPathList(params['pathlist']) if "pathlist" in params else None

                if user.update():
                    return '', 204
                else:
                    return json.dumps('409 Conflict'), 409
            else:
                return json.dumps('User is not found'), 404
            
        elif request.method == 'DELETE':
            user = Users.findById(usersid)
            if user.delete():
                return '', 204
            else:
                return json.dumps('409 Conflict'), 409

                
    else:
        return json.dumps('403 Forbidden'), 403
    


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

