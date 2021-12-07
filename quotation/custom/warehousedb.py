import pymssql
import configparser
import os
from quotation.models import Item


def get_itemdetail(sn):
    filename = "secret.cfg"
    figpwd = os.path.join(os.path.dirname(__file__), filename)
    config = configparser.ConfigParser()
    config.read(figpwd)
    dbusr = config['WarehouseDB']
    data = {}
    try:
        conn = pymssql.connect(server='192.168.168.121', user=dbusr["user"], password=dbusr["password"],
                               database='Warehouse')
        cursor = conn.cursor()
        sql_str = """
            SELECT stock.[item_sn], stock.[item_name], stock.[item_specmain],
                stock.[item_specsub], stock.[item_isvalid], cate.cate_en, cate.cate_name
            FROM [Warehouse].[dbo].[stock_item] AS stock
            INNER JOIN [Warehouse].[dbo].[stock_category] AS cate
            ON (stock.item_cate_id = cate.id)
            WHERE stock.[item_sn] = '{}'
        """.format(sn)
        cursor.execute(sql_str)
        row = cursor.fetchone()
        if row:  # 有查到資料的話
            data['status'] = True
            data['result'] = {}
            for i in range(len(cursor.description)):
                data['result'][cursor.description[i][0]] = row[i]
            item_cnt = Item.objects.filter(sn=data['result']['item_sn']).count()
            if item_cnt != 0:
                data['status'] = False
                data['result'] = "已有相同品項，請再查詢！"
        else:
            data['status'] = False
            data['result'] = "查無資料！"
        conn.close()
    except:
        print("error")
        data['status'] = False
        data['result'] = "查詢資料錯誤!請聯絡管理員。"
    print(data)
    return data
