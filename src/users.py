import hashlib
import JsonAdapter

class Users(JsonAdapter.JsonAdapter):

  userslist = []
  
  def __init__(self, name, password, pathlist):
    self.name = name
    self.pass_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
    self.pathlist = pathlist
    global userslist
    userslist.append(self)

  def auth(self, password):
    return self.pass_hash == hashlib.sha512(password.encode('utf-8')).hexdigest()

  def greet(self):
    return "my name is %s " % self.name

  def getPathList(self):
    return self.pathlist

  @classmethod
  def getUsersList(cls):
    return cls.userslist
