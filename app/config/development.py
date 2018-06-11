
class DevelopementConfig:
    DEBUG = True
    
    @staticmethod
    def DATABASE_URI():
        db_type = 'mysql'
        driver = 'pymysql'
        user = 'root'
        password = 'coderslab'
        host = 'localhost'
        db_name = 'football'

        return '{}+{}://{}:{}@{}/{}'.format(
            db_type, driver,
            user, password,
            host, db_name,
        )

    


