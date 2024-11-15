import requests
import mysql.connector
from mysql.connector import pooling
import time
import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sendWA(number: str, text: str):
    data = {"number": number, "message": text}
    response = requests.post("http://192.168.25.208:3999/sendwa", json=data, timeout=5)
    return response

# Pooling koneksi untuk lebih efisien
dbconfig = {
    "user": "elly",
    "password": "P4ssword2024",
    "host": "192.168.25.221",
    "database": "soluman24_test"
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)

chk_req_data = "SELECT * FROM trouble_equipment WHERE Status1 = %s"
get_eqName = "SELECT ID_Equipment_Display, Equipment FROM equipment WHERE ID_Equipment = %s"

cnt_req_before = 0
flag_newReq = 0

while True:
    try:
        cnx = connection_pool.get_connection()
        tm = time.time()
        tm_ = datetime.datetime.fromtimestamp(round(tm, 2))
        cursor = cnx.cursor()
        
        cursor.execute(chk_req_data, ("Waiting",))
        res = cursor.fetchall()
        #print(tm_, "new request waiting", len(res))

        if len(res) > cnt_req_before:
            cnt_req_before = len(res)
            flag_newReq = 1

        if flag_newReq:
            txt = []
            latest_trouble = res[-1]
            cursor.execute(get_eqName, (latest_trouble[2],))
            mc_name = cursor.fetchall()[0][1]
            txt.append("SOLUMAN Information\n\nNew request occurs :\n")
            txt.append(f"Req Num : {latest_trouble[0]}; Req From : {latest_trouble[20]}; M/C Name : {mc_name}; Trouble : {latest_trouble[4]}\n")
            txt.append("\nWaiting for approval :\n")
            for i, data in enumerate(res):
                mc_id = data[2]
                cursor.execute(get_eqName, (mc_id,))
                mc_name = cursor.fetchall()[0][1]
                txt.append(f"{i+1}. Req Num : {data[0]}; Req From : {data[20]}; M/C Name : {mc_name}; Trouble : {data[4]}\n")
            print("".join(txt))
            res = sendWA("6285794607446@c.us", "".join(txt))
            flag_newReq = 0

        cursor.close()
        cnx.close()
        time.sleep(1)
    except mysql.connector.Error as e:
        print("Database error:", e)
        break
    except Exception as e:
        print("Terjadi error :", e)
        break
