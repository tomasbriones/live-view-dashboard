import requests
import json
import os
from utils.utils import validate_response
from settings.settings import API_PORT, API_URL
# from utils.env import API_PORT, API_URL
from db.db_functions import update_patches_logs_status


def send_to_api(endpoint, payload):
    try:
        URL = 'http://'+API_URL+':'+API_PORT+'/'+endpoint
        headers = headers = {
            'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post(URL, data=json.dumps(payload), headers=headers)
        print(res.text)
    except Exception as e:
        print('[send_to_api] Exception: ', e)
        return e


def get_token():
    URL = os.getenv('ENDPOINT')+'/api/v1/api-token-auth/'
    body = {
        'api_key': os.getenv('API_KEY'),
        'chile_atiende_id': os.getenv('CHA_ID')
    }

    try:
        res = requests.post(URL, data=body)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            print('[get_token] Error en obtencion de token: ', res.text)
            return False
    except Exception as e:
        print('[get_token] Exception: ', e)
        return e


def validate_token(token):
    headers = {'Authorization': 'token ' + token}
    URL = os.getenv('ENDPOINT')+'/api/v1/companies/82438821-0/'
    res = requests.get(URL, headers=headers)
    if res.status_code == 200:
        print(res.text)
        return True
    return False


def create_permit(token, url, payload):
    URL = os.getenv('ENDPOINT')
    NEW_URL = URL+url
    # print(NEW_URL)
    headers = {'Authorization': 'token ' + token}
    res = requests.post(NEW_URL, headers=headers, data=payload)
    if res.status_code == 200:
        return res
    else:
        print('[create_permit] resultado no es 200: ', res)
    return False


def token_process(data, i):
    token = get_token()
    if token != False:
        token_valid = validate_token(token['token'])
        if token_valid == True:
            return True, token["token"]
        else:
            print('[send_to_api] Token invalido, pasando al siguiente')
            return False, ""
    else:
        print("No se pudo obtener token")


def send_to_api(conn, data):
    try:
        for i in range(len(data)):
            is_valid, token = token_process(data, i)
            if is_valid == False:
                update_patches_logs_status(conn, data[i][0], 'ERROR')
            else:
                res = create_permit(token, data[i][2], data[i][1])
                if type(res) == bool or res == False:
                    update_patches_logs_status(conn, data[i][0], 'ERROR')
                else:
                    if res.status_code == 200:
                        validate_response(conn, res, data[i][0])
                    else:
                        print("res no es 200...", res.text)
        return data
    except Exception as e:
        print('[send_to_api] Exception: \n', e)
        return e
