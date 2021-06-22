# from utils.env import * as env
from db.db_functions import *
from db.sql_statements import *
from db.connection_aws import Aws
from db.connection_postgresql import PostgreSql
import os

class Connection:

    def connect(self):
        # Funcion para conectar a aws y obtener un cursor a la bd postgresql
        if os.getenv('ENVIRONMENT') != 'AWS':
            aws = Aws()
            self.tunnel = aws.awsConnect()
            postgre_sql = PostgreSql(self.tunnel)
            self.db_conn = postgre_sql.postgreSqlConnect()
        else:
            # self.tunnel = aws.awsConnect()
            postgre_sql = PostgreSql()
            self.db_conn = postgre_sql.postgreSqlConnect()
        return self.db_conn
            

    def disconect(self, conn):
        if os.getenv('ENVIRONMENT') != 'AWS':
            conn.close()
            self.db_conn.close()
            print('Desconectando de postgresql')
            self.tunnel.close()
            print('Desconectando de aws')
        else: 
            conn.close()
            self.db_conn.close()
            print('Cerrando conexión')

# def db_version():
#     print('PostgreSQL database version:')
#     cur = db_conn.cursor()
#     cur.execute('SELECT version()')
#     db_version = cur.fetchone()
#     print(db_version)
