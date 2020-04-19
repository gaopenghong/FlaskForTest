# -*- coding:utf-8 -*-

# ssh_conf.py 数据库配置信息
import pymysql
import socket
from sshtunnel import SSHTunnelForwarder

dbconfig = {
    't1': 30110,
    't2': 30120,
    't3': 30130,
    't4': 30140,
    't5': 30150,
    't6': 30160,
    't7': 30170,
    't8': 30180,
    't9': 30190,
    't10': 30200,
    'r1': 30112,
    'r2': 30122,
    'd1': 30111,
    'd2': 30121,
    'd3': 30131,
    'd4': 30141,
    'd5': 30151,

}


def remote_database(environment, database, sql):
    port = dbconfig[environment]
    hostname = socket.getfqdn(socket.gethostname())
    try:
        myaddr = socket.gethostbyname(hostname)
    except:
        myaddr = socket.gethostbyname("")
    sql_function = str.lower(sql[:3])
    if myaddr != "192.168.2.68":
        try:
            with SSHTunnelForwarder(('39.106.179.67', 10068), ssh_password='2679a2QWS#',
                                    ssh_username='fyadmin',
                                    remote_bind_address=('192.168.1.30', port), ) as server:
                db = pymysql.connect(host='127.0.0.1', port=server.local_bind_port, user='fykctest',
                                     password='fykctest_88',
                                     db=database, charset='utf8')
                cursor = db.cursor()
                cursor.execute(sql)
                if sql_function == 'sel':
                    data = cursor.fetchall()
                    cursor.close()
                    db.close()
                    data_1 = []
                    for i in data:
                        j = list(i)
                        data_1.append(j)
                    return data_1
                else:
                    db.commit()
                db.close()
        except:
            print("连接数据库失败")
            return "连接数据库失败"
    else:
        try:
            db = pymysql.connect(host='192.168.1.29', port=port, user='fykctest', password='fykctest_88',
                                 db=database, charset='utf8')
            cursor = db.cursor()
            cursor.execute(sql)
            if sql_function == 'sel':
                data = cursor.fetchall()
                cursor.close()
                db.close()
                data_1 = []
                for i in data:
                    j = list(i)
                    data_1.append(j)
                return data_1
            else:
                db.commit()
            db.close()
        except:
            return "连接数据库失败"


if __name__ == '__main__':
    # myname = socket.getfqdn(socket.gethostname())
    # myaddr = socket.gethostbyname(myname)
    # print(myaddr)
    # mobile = '16022222222'
    # r = remote_database(dbconfig[4][-1], "fykc_xdriver_service", "select id from fykc_xdriver_service.driver_info where id<%s;" % mobile)
    # r = remote_database(dbconfig[4][-1], "fykc_xdriver_service", "select id from fykc_xdriver_service.driver_info where mobile=%s;" % mobile)
    # print(r)
    # print(r[0][0])
    order_sn = '129102597044'
    # sql_update_time = 'update base_info set planTransTime=60 where orderSn="' + order_sn + '"'
    sql_update_time = 'select * from base_info limit 1'
    l = remote_database(30112, 'fykc_order_center', sql_update_time)
    print(l)