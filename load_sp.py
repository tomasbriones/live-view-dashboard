"""
script that reads csv with state changes.
the state changes are passed as parameters to the store procedure.
permit id must be passed as an additional parameter   
"""

import csv
from db.connection import Connection
import sys
import os

PERMIT_ID = os.getenv('PERMIT_ID')
FILENAME=os.getenv('SC_CSV')


print("el permiso es: ", PERMIT_ID)
print("el cambio de estado es: ", FILENAME)
print("el servicio es: ", os.getenv("CHA_ID"))


def read_doc():
    with open(FILENAME, newline='') as csvfile:
        state_changes = csv.reader(csvfile, delimiter=',')
        next(state_changes)
        data_state_changes = list(state_changes)
        return data_state_changes

def state_changes_sp(conn, states):
    """
    states are given to SP 'create_permit_status' as parameters
    """
    cur = conn.cursor()
    try:
        for i in range(len(states)):
            cur.execute('SELECT create_permit_status(%s,%s,%s,%s,%s)', (
                states[i][0], 
                states[i][1], 
                states[i][2], 
                states[i][3],
                PERMIT_ID))
            conn.commit()
        cur.close()
    except Exception as e:
        print(e)
        return e
    finally:
        if conn is not None:
            conn.close()

conection = Connection()
conn = conection.connect()
# get state changes
states = read_doc()
# pass conn and state changes as params to function
state_changes_sp(conn, states)
# finish process
conection.disconect(conn)
