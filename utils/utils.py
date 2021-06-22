import json

from db.db_functions import (increment_counter, insert_patches_logs,
                             update_patches_logs_status, validate_if_exists)


def set_api_log_data(conn, data):
    try:
        for i in range(len(data)):
            existe = validate_if_exists(conn, data[i][6])
            if (existe != True):
                insert_patches_logs(
                    conn,
                    data[i][5],
                    data[i][2],
                    data[i][0],
                    data[i][3],
                    data[i][6]
                )
    except Exception as e:
        return e


def validate_response(conn, response, id_row):
    message = json.loads(response.text)
    try:
        OK = 'OK'
        if response.status_code == 200 and message['status'] == OK:
            print('[validate_response] Ok id: ', id_row)
            update_patches_logs_status(conn, id_row, OK)
            increment_counter(conn, id_row)
            return True
        else:
            update_patches_logs_status(conn, id_row, 'ERROR')
            print('[validate_response] error en ID: ', id_row)
            return False
    except Exception as e:
        print('[validate_response] Exception: \n', e)
        return e
