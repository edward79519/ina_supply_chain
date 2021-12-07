from django.http import JsonResponse
from quotation.custom.warehousedb import get_itemdetail


def getdetail(request):
    sn = request.GET.get('sn')
    print(sn)
    detail = get_itemdetail(sn)
    return JsonResponse(detail)
