import json
import requests


def getrate(current, date):
    tenday = date.day // 15 + 1
    data = {
        'formBean.crrnCd': current,
        'formBean.year': str(date.year),
        'formBean.mon': str(date.month).zfill(2),
        'formBean.tenDay': str(tenday),
    }
    response = requests.post("https://portal.sw.nat.gov.tw/APGQO/GC331!query", data=data)
    jres = json.loads(response.text)
    jdata = jres["data"]
    jstaus = "OK" if jdata != [] else "Get Data Error"
    res = {
        'status': jstaus,
        'in_rate': jdata[0]['IN_RATE'],
        'ex_rate': jdata[0]['EX_RATE'],
    }
    return res
