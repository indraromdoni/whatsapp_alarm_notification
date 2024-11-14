import mysql.connector
import time
import datetime

chk_req_data = "SELECT * FROM trouble_equipment WHERE Status1='Waiting'"
get_eqName = "SELECT ID_Equipment_Display, Equipment FROM equipment WHERE ID_Equipment = '{}'"

cnt_req_before = 0
flag_newReq = 0

while True:
    try:
        cnx = mysql.connector.connect(user='elly', password='P4ssword2024',
                              host='192.168.25.221',
                              database='soluman24_test')
        tm = time.time()
        tm_ = datetime.datetime.fromtimestamp(round(tm, 2))
        cursor = cnx.cursor()
        cursor.execute(chk_req_data)
        res = cursor.fetchall()
        print(tm_, "new request waiting", len(res))

        if len(res) != cnt_req_before:
            cnt_req_before = len(res)
            flag_newReq = 1

        if flag_newReq:
            for data in res:
                mc_id = data[2]
                cursor.execute(get_eqName.format(mc_id))
                mc_name = cursor.fetchall()
                print("Req Num :", data[0], "; Req From :", data[20], "; M/C Name :", mc_name[0][1], "; Trouble :", data[4])
            flag_newReq = 0

        cursor.close()
        cnx.close()
        time.sleep(1)
    except Exception as e:
        print("Terjadi error :", e)
        break