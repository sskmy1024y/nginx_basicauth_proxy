import hashlib
import re
import sqlite3

class Users():

  dbpath = "users.db"
  
  def __init__(self, name, password, pathlist, ishashed=False):
    self.name = name
    self.pass_hash = password if ishashed else hashlib.sha512(password.encode('utf-8')).hexdigest()
    self.pathlist = re.split(',\r*\n*', pathlist)

  def auth(self, password):
    return self.pass_hash == hashlib.sha512(password.encode('utf-8')).hexdigest()

  def getUsername(self):
    return self.name

  def getPathList(self):
    return self.pathlist
    
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
    
      # DB connection
      connection = sqlite3.connect(cls.dbpath)
      cursor = connection.cursor()
      try:
        cursor.execute("INSERT INTO users(name, password, pathlist) VALUES (:name, :password, :pathlist)", {'name': name, 'password': pass_hash, 'pathlist': pathlist})
        u = cursor.fetchone()    
      except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        return False

      connection.commit()
      connection.close()
      return True

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
        data = cls(u['name'], u['password'], u['pathlist'], True)
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
      cursor.execute("SELECT * FROM users WHERE name=?", (name,))
      us = cursor.fetchall()
      for u in us:
        data.append(cls(u['name'], u['password'], u['pathlist'], True))
      
    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])

    connection.close()
    return data
