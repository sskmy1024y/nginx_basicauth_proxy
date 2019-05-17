import hashlib
import re
import sqlite3
import json

class Users():

  dbpath = "users.db"
  
  def __init__(self, userid, name, password, pathlist, ishashed=False):
    self.id = userid
    self.name = name
    self.pass_hash = password if ishashed else hashlib.sha512(password.encode('utf-8')).hexdigest()
    self.pathlist = re.split(',\r*\n*', pathlist)

  def auth(self, password):
    return self.pass_hash == hashlib.sha512(password.encode('utf-8')).hexdigest()

  def setName(self, name):
    self.name = name

  def getName(self):
    return self.name

  def setPassword(self, password, ishashed=False):
    self.pass_hash = password if ishashed else hashlib.sha512(password.encode('utf-8')).hexdigest()

  def setPathList(self, pathlist):
    self.pathlist = re.split(',\r*\n*', pathlist)

  def getPathList(self):
    return self.pathlist

  def toJSON(self):
    return {'id': self.id, 'name': self.name, 'pathlist': self.pathlist}

  def update(self):
    # DB connection
    connection = sqlite3.connect(self.dbpath)
    cursor = connection.cursor()

    try:
      cursor.execute("UPDATE users SET name=?, password=?, pathlist=? WHERE id=?", (self.name, self.pass_hash, ','.join(self.pathlist), self.id))
    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])
      return False

    connection.commit()
    connection.close()
    return self

  def delete(self):
    connection = sqlite3.connect(self.dbpath)
    cursor = connection.cursor()
    try:
      cursor.execute("DELETE FROM users WHERE id=?", (self.id,))
    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])
      return False

    connection.commit()
    connection.close()
    return True

  @classmethod
  def initDatabase(cls, path="users.db"):
    cls.dbpath = path
    
    # DB connection
    connection = sqlite3.connect(cls.dbpath)
    cursor = connection.cursor()
    try:
      cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, pathlist TEXT)")
    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])

    connection.commit()
    connection.close()

  @classmethod
  def register(cls, name, password, pathlist):
    if cls.find(name):
      return False
    else:
      pass_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
      data = False
      # DB connection
      connection = sqlite3.connect(cls.dbpath)
      connection.row_factory = sqlite3.Row
      cursor = connection.cursor()
      try:
        cursor.execute("INSERT INTO users(name, password, pathlist) VALUES (:name, :password, :pathlist)", {'name': name, 'password': pass_hash, 'pathlist': pathlist})
        cursor.execute("SELECT * FROM users WHERE name=?", (name,))
        u = cursor.fetchone()
        if u:
          data = cls(u['id'], u['name'], u['password'], u['pathlist'], True)
  
      except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        return False

      connection.commit()
      connection.close()
      return data

  @classmethod
  def find(cls, name):
    data = False
    # DB connection
    connection = sqlite3.connect(cls.dbpath)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
      cursor.execute("SELECT * FROM users WHERE name=?", (name,))
      u = cursor.fetchone()
      if u:
        data = cls(u['id'], u['name'], u['password'], u['pathlist'], True)
    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])

    connection.close()
    return data
  
  @classmethod
  def findById(cls, userid):
    data = False
    # DB connection
    connection = sqlite3.connect(cls.dbpath)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
      cursor.execute("SELECT * FROM users WHERE id=?", (userid,))
      u = cursor.fetchone()
      if u:
        data = cls(u['id'], u['name'], u['password'], u['pathlist'], True)
    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])

    connection.close()
    return data

  @classmethod
  def getUserLists(cls):
    data = []
    # DB connection
    connection = sqlite3.connect(cls.dbpath)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
      cursor.execute("SELECT * FROM users")
      us = cursor.fetchall()
      for u in us:
        data.append(cls(u['id'], u['name'], u['password'], u['pathlist'], True).toJSON())

    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])

    connection.close()
    return json.dumps(data)
