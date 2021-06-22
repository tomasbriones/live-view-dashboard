# -*- coding: utf-8 -*-
from db.sql_statements import GET_PERMIT_ORIGINAL_DATE, SELECT_PATCHES_LOGS_ID, INSERT_DATA_IN_PATCHES_LOGS, UPDATE_PATCHES_LOGS_STATUS, UPDATE_PATCHES_LOGS_COUNTER, UPDATE_CHANGE_STATE_DATE_NOTIFICATION, GET_CHANGE_STATE_DATE_NOTIFICATION, SELECT_ORIGINAL_API_LOGS_ID
# from utils.utils import get_permit_id
import json
import pytz
import datetime


scl_tz = pytz.timezone('America/Santiago')


def validate_if_exists(conn, origin_log_id):
    try:
        cur = conn.cursor()
        query = SELECT_ORIGINAL_API_LOGS_ID % (origin_log_id)
        cur.execute(query)
        res = cur.fetchall()
        conn.commit()
        cur.close()
        return res[0][0]
    except Exception as e:
        return e


def select_from_db(conn, query):
    print(conn)
    try:
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        conn.commit()
        return res
    except Exception as e:
        return e


def insert_patches_logs(conn, req, url, log, ms_app_id, original_log_id):
    cur = conn.cursor()
    req_dump = json.dumps(req, ensure_ascii=False).encode('utf-8')
    query = INSERT_DATA_IN_PATCHES_LOGS % (
        req_dump.decode(), url, log, ms_app_id, original_log_id)
    cur.execute(query)
    conn.commit()
    cur.close()


def update_patches_logs_status(conn, id_row, status):
    cur = conn.cursor()
    query = UPDATE_PATCHES_LOGS_STATUS % (status, id_row)
    cur.execute(query)
    conn.commit()
    cur.close()


def increment_counter(conn, id_row):
    query = SELECT_PATCHES_LOGS_ID % (id_row)
    counter_value = select_from_db(conn, query)
    query = UPDATE_PATCHES_LOGS_COUNTER % (counter_value[0][0]+1, id_row)
    insert_on_db(conn, query)


def insert_on_db(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()


def get_last_notification(conn, data):
    cur = conn.cursor()
    query = GET_CHANGE_STATE_DATE_NOTIFICATION % (data)
    cur.execute(query)
    res = cur.fetchone()
    conn.commit()
    return res


def update_last_notification(conn, original_date, created_new, permit_id):
    cur = conn.cursor()
    # print("UPDATE LAST NOTIFICATION")
    # print("--------------------------")
    # print("ORIGINAL DATE TO SCL: \n", original_date.astimezone(scl_tz))
    # print("CREATED NEW SCL: \n", created_new.astimezone(scl_tz))
    # print("PERMIT ID: \n", permit_id)
    # print("--------------------------")
    query = UPDATE_CHANGE_STATE_DATE_NOTIFICATION % (
        original_date.astimezone(scl_tz),
        original_date.astimezone(scl_tz),
        created_new.astimezone(scl_tz),
        permit_id)
    print(query)
    res = cur.execute(query)
    conn.commit()
    return res


def get_permit_id(data, i):
    ms = data[i][2].split('/')
    return ms[4]


def set_original_date(conn, data):
    try:
        for i in range(len(data)):
            permit_id = get_permit_id(data, i)
            last_notification = get_last_notification(conn, permit_id)
            query = GET_PERMIT_ORIGINAL_DATE % (
                data[i][3].astimezone(scl_tz), permit_id)
            original_date = select_from_db(conn, query)
            if len(original_date) == 1:
                update_last_notification(
                    conn, original_date[0][0], last_notification[1], permit_id)
            else:
                print('[set_original_date] No hay resultados para query: \n', query)
    except Exception as e:
        print('[set_original_date] Exception: ', e)
