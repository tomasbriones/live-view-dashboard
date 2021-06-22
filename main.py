# -*- coding: utf-8 -*-
import os
import requests
from settings.settings import SSH_HOST
from db.db_functions import select_from_db, set_original_date
from db.sql_statements import SELECT_URL_REQ_RES_LOG, SELECT_PATCHES_LOGS_REQ_URL
from utils.utils import set_api_log_data
import dotenv
from db.connection import Connection
from service.api import send_to_api


def main():    
    conection = Connection()
    conn = conection.connect()
    print("Conectando al host")
    print('Ejecutando statements...')
    data = select_from_db(conn, SELECT_URL_REQ_RES_LOG)
    set_api_log_data(conn, data)
    patches_log_data = select_from_db(conn, SELECT_PATCHES_LOGS_REQ_URL)
    print(len(patches_log_data))
    api_data = send_to_api(conn, patches_log_data)
    set_original_date(conn, api_data)
    conection.disconect(conn)

if __name__ == "__main__":
    main()
