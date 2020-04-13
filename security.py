
from werkzeug.security import safe_str_cmp
from models.user import UserModel

#users = [User(1,'bob','asdf')]

#username_mapping = {u.username: u for u in users} #crea diccionario bob: 1,'bob','asdf', julio: 2,'julio','oliuj' etc

#userid_mapping ={u.id: u for u in users} #lo mismo pero asi: 1: 1,'bob','asdf', 2: 2, etc


def authenticate(username, password):
    #user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    user_id = payload['identity']
    #return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)