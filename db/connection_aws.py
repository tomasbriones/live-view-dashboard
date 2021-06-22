#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import settings
from settings.settings import SSH_HOST, SSH_USER, SSH_PK, SSH_PWD, DB_HOST
# from utils.env import SSH_HOST, SSH_USER, SSH_PK, SSH_PWD, DB_HOST
import sshtunnel


class Aws:

    def __init__(self):
        # Variable que determina si estamos conectados a aws...
        self.connected = 0
        self.error = ""

    def awsConnect(self):
        """
        Funcion para abrir (tunnel.start()) la conexion con aws
        """
        print('entrando a la matrix...')
        self.tunnel = None
        print('espere un momento...')
        try:
            tunnel = sshtunnel.SSHTunnelForwarder(
                (str(SSH_HOST)),
                ssh_username=SSH_USER,
                ssh_pkey=SSH_PK,
                ssh_password=SSH_PWD,
                remote_bind_address=(str(DB_HOST), 5432)
            )
            tunnel.start()
            self.connected = 1
            print("tunel aws iniciado")
            return tunnel
        except Exception as e:
            print("Exception: ", e)
            self.error = e
            raise e

    def postgreSqlClose(self):
        """
        Funcion para cerrar la conexion con postgreSql
        """
        self.connected = 0
        try:
            self.tunnel.close()
        except:
            pass
