#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from utils.env import *
from settings.settings import DB_USER, DB_HOST, DB_PWD, LOCALHOST, DB_NAME
import psycopg2


class PostgreSql:

    def __init__(self, tunnel = False):
        # Variable que determina si estamos conectados a postgreSql...
        self.connected = 0
        self.error = ""
        self.tunnel = tunnel
        self.user = DB_USER
        self.pw = DB_PWD        
        self.database = DB_NAME
        self.host = DB_HOST        
        self.port = 5432
        if tunnel != False:
            self.port = tunnel.local_bind_port
            self.host = LOCALHOST


    def postgreSqlConnect(self):
        """
        Realiza la conexion con la base de datos
        Tiene que recibir:
            - host
            - user
            - pw => password
            - database => database name
        Puede recibir:
            - port
        Devuelve True o False
        """
        print('Connecting to the PostgreSQL database...')        

        try:
            self.db_conn = psycopg2.connect(user=self.user, password=self.pw, host=self.host, database=self.database,

                                            port=self.port)

            # self.cursor = self.db.cursor()
            self.connected = 1
            print('Connected to PostgreSQL database...')
            return self.db_conn
            # return self.cursor
        except Exception as e:
            self.error = "Error: %s" % (e)
            print(self.error)
        except:
            self.error = "Error desconocido"
            print(self.error)
        return False

    def prepare(self, query, params=None, execute=True):
        """
        Funcion que ejecuta una instruccion mysql
        Tiene que recibir:
            - query
        Puede recibir:
            - params => tupla con las variables
            - execute => devuelve los registros
        Devuelve False en caso de error
        """
        if self.connected:
            self.error = ""
            try:
                self.cursor.execute(query, params)
                self.db.commit()
                if execute:
                    # convert de result to dictionary
                    result = []
                    columns = tuple([d[0].decode('utf8')
                                    for d in self.cursor.description])
                    for row in self.cursor:
                        result.append(dict(zip(columns, row)))
                    return result
                return True
            except Exception as e:
                self.error = "Error: %s" % (e)
        return False

    def lastId(self):
        """
        Funcion que devuelve el ultimo id añadido
        """
        return self.cursor.lastrowid

    def affectedRows(self):
        return self.cursor.rowcount

    def postgreSqlClose(self):
        """
        Funcion para cerrar la conexion con la base de datos
        """
        self.connected = 0
        try:
            self.cursor.close()
        except:
            pass
        try:
            self.db_conn.close()
        except:
            pass

    def fetchOneAssoc(self, cursor):
        data = cursor.fetchone()
        if data == None:
            return None
        desc = cursor.description

        dict = {}

        for (name, value) in zip(desc, data):
            dict[name[0]] = value

        return dict


if __name__ == "__main__":
    obj = postgreSql()
    result = obj.postgreSqlConnect(
        LOCALHOST, DB_USER, DB_PWD, DB_NAME)
    if result:

        # ejeplo 1 - INSERT
        # print obj.prepare("INSERT INTO tabla VALUES (null, now(), 'http')", None, False)
        # print obj.lastId

        # ejemplo 2 - UPDATE
        # query = "UPDATE tabla SET Texto=%s WHERE id=%s"
        # params = ("XX", 20)
        # obj.prepare(query, params, False)
        # if result:
        #     print result
        # else:
        #     print obj.error
        # print obj.affectedRows()

        # ejemplo 3 - SELECT
        # result = obj.prepare("SELECT * FROM tabla WHERE id=%s", (20,))
        result = obj.prepare("SELECT * FROM api_patches_logs")
        if result:
            print(result)
        else:
            print(obj.error)

        obj.mysqlClose()
    else:
        print(obj.error)
