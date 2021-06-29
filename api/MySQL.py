from config import key
import pymysql

class DB:
    def __init__(self):
        self.db = pymysql.connect(
            user = 'root',
            passwd = key.MYSQL_PASSWORD,
            host = key.MYSQL_IP,
            port = key.MYSQL_PORT,
            db = 'STOCK',
            charset = 'utf8'
        )

        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
    
    def commit(self):
        self.db.commit()
        
    def printLog(self):
        for log in self.cursor:
            print(log)

    def createDatabase(self):
        createDBQuery = "CREATE DATABASE STOCK"
        self.cursor.execute(createDBQuery)

    def createTable(self,model):
        create_movies_table_query = "CREATE TABLE " + model
        self.cursor.execute(create_movies_table_query)
    
