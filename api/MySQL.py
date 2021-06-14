from config import key
import pymysql

db = pymysql.connect(
    user = 'root',
    passwd = key.MYSQL_PASSWORD,
    host = key.MYSQL_IP,
    port = key.MYSQL_PORT,
    db = 'sys',
    charset = 'utf8'
)

cursor = db.cursor(pymysql.cursors.DictCursor)
