from django.http import JsonResponse
from quotation.models import Manufacturer
import re


def get_mfg(request):
    cate_id = request.GET.get('cate_id')
    pattern = r'\d+'
    if re.match(pattern, cate_id) is not None:
        mfgs = Manufacturer.objects.filter(cate_id=cate_id, is_open=True)
    else:
        mfgs = Manufacturer.objects.all()
    mfg_list = []
    for idx, mfg in enumerate(mfgs):
        mfg_list.append({
            'id': mfg.id,
            'id_name': '{}_{}'.format(mfg.sn, mfg.name),
        })
    data = {
        'mfgs': mfg_list,
    }
    return JsonResponse(data)


def get_mfgcode(request):
    mfg_name = request.GET.get('mfg_name')
    mfg = Manufacturer.objects.filter(name__exact=mfg_name)
    data = {}
    if mfg.count() == 0:
        data['status'] = "Error"
        data['message'] = "查無資料。"
    elif mfg.count() == 1:
        data['status'] = "OK"
        data['mfg_code'] = mfg[0].sn
    else:
        data['status'] = "Error"
        data['message'] = "查詢超過一筆資料。"
    rdata = {
        'data': data,
    }
    print(rdata)
    return JsonResponse(rdata)
