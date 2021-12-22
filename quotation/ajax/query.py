from django.http import JsonResponse
from quotation.models import Manufacturer
import re


def get_mfg(request):
    cate_id = request.GET.get('cate_id')
    pattern = r'\d+'
    if re.match(pattern, cate_id) is not None:
        mfgs = Manufacturer.objects.filter(cate_id=cate_id)
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


