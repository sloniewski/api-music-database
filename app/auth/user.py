from werkzeug.security import generate_password_hash, check_password_hash

class User:
    username = None
    __hashed_password = None
    __is_authenticated = False

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.__id = None

    @property
    def user_id(self):
        return self.__id

    @property
    def password(self):
        return self.__hashed_password

    def set_password(self, password):
        self.__hashed_password = password


    @property
    def is_authenticated(self):
        self.login()
        return self.__is_authenticated
    
    def login(self):
        if self.__is_authenticated is True:
            return True
        
        if self.username is None or self.password is None:
            raise AttributeError('User login or password is missing')
        
        self.__is_authenticated = True # :TODO implement login
        self.id = 5 # TODO
        
        return True



