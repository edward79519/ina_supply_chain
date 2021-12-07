from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Company, Item, Inquiry, ItemQuota, Current
from .forms import AddCompForm, UpdateCompForm, AddItemForm, UpdateItemForm, AddInquiryForm, UpdateQuotaForm
from django.utils import timezone
from datetime import datetime
from .custom.exchange import getrate
from django.contrib.auth.decorators import login_required


# Create your views here.


def comp_list(request):
    comp_list = Company.objects.all()
    template = loader.get_template('quotation/company/list.html')
    context = {
        'comp_list': comp_list,
    }
    return HttpResponse(template.render(context, request))


def comp_detail(request, comp_id):
    comp = Company.objects.get(id=comp_id)
    template = loader.get_template('quotation/company/detail.html')
    inquirys = comp.inquirys.filter(is_open=True)
    itemquotas = ItemQuota.objects.filter(inquirysn__company_id=comp_id)
    context = {
        'comp': comp,
        'inquirys': inquirys,
        'itemquotas': itemquotas,
    }
    return HttpResponse(template.render(context, request))


@login_required
def comp_add(request):
    template = loader.get_template('quotation/company/add.html')
    if request.method == "POST":
        form = AddCompForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("../")
        else:
            print("error")
    else:
        form = AddCompForm()
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def comp_update(request, comp_id):
    template = loader.get_template('quotation/company/update.html')
    comp = Company.objects.get(id=comp_id)
    if request.method == "POST":
        form = UpdateCompForm(request.POST, instance=comp)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("../")
        else:
            print("error")
    else:
        form = UpdateCompForm(instance=comp)
    context = {
        'comp': comp,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


def item_list(request):
    items = Item.objects.all()
    template = loader.get_template("quotation/item/list.html")
    context = {
        'items': items,
    }
    return HttpResponse(template.render(context, request))


def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    quotas = ItemQuota.objects.filter(itemsn_id=item_id).order_by("-qdate")
    time_arr = []
    price_arr = []
    for q in quotas:
        if q.qdate and q.ntd_price():
            time_arr.append(q.qdate.strftime("%Y-%m-%d"))
            price_arr.append(float(q.ntd_price()))
    quota_data = {
        "time": time_arr,
        "price": price_arr,
    }
    template = loader.get_template("quotation/item/detail.html")
    context = {
        'item': item,
        'quotas': quotas,
        'quota_data': quota_data,
    }
    return HttpResponse(template.render(context, request))


@login_required
def item_add(request):
    template = loader.get_template("quotation/item/add.html")
    if request.method == "POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("../")
        else:
            print('error')
            return HttpResponseRedirect("./")
    else:
        form = AddItemForm()
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def item_update(request, item_id):
    template = loader.get_template("quotation/item/update.html")
    item = Item.objects.get(id=item_id)
    if request.method == "POST":
        form = UpdateItemForm(request.POST, instance=item)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("../")
        else:
            print('error')
            return HttpResponseRedirect("./")
    else:
        form = UpdateItemForm(instance=item)
    context = {
        'form': form,
        'item': item,
    }
    return HttpResponse(template.render(context, request))


def inquiry_list(request):
    inquirys = Inquiry.objects.all().order_by("-addtime")
    template = loader.get_template("quotation/inquiry/list.html")
    context = {
        'inquirys': inquirys,
    }
    return HttpResponse(template.render(context, request))


def inquiry_detail(request, inqry_id):
    inquiry = Inquiry.objects.get(id=inqry_id)
    quotas_old = ItemQuota.objects.filter(inquirysn_id=inqry_id, is_new=False)
    quotas_new = ItemQuota.objects.filter(inquirysn_id=inqry_id, is_new=True)
    template = loader.get_template("quotation/inquiry/detail.html")
    context = {
        'inquiry': inquiry,
        'quotas_old': quotas_old,
        'quotas_new': quotas_new,
    }
    return HttpResponse(template.render(context, request))


@login_required
def inquiry_add(request):
    template = loader.get_template("quotation/inquiry/add.html")
    if request.method == "POST":
        count = Inquiry.objects.filter(addtime__date=timezone.now().date()).count() + 1
        sn = "{}{}".format(timezone.now().date().strftime("%Y%m%d"), str(count).zfill(3))
        query = request.POST.copy()
        query['sn'] = sn
        form = AddInquiryForm(query, initial={'author': request.user})
        if form.is_valid():
            inqform = form.save()
            cate_id = query['cate']
            item_ids = Item.objects.filter(cate_id=cate_id).values_list('id')
            quotas = [ItemQuota(itemsn_id=item_id[0], inquirysn_id=inqform.pk) for item_id in item_ids]
            ItemQuota.objects.bulk_create(quotas)
            return HttpResponseRedirect("../")
        else:
            print("error")
            return HttpResponseRedirect("./")
    else:
        form = AddInquiryForm(initial={'author': request.user})
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def inquiry_close(request, inqry_id):
    inqry = Inquiry.objects.get(id=inqry_id)
    inqry.status = Inquiry.Status.END
    inqry.save()
    return HttpResponseRedirect("../")


@login_required
def quota_inpageupdate(request, quota_id):
    template = loader.get_template("quotation/inquiry/quota/inpgupdate.html")
    quota = ItemQuota.objects.get(id=quota_id)
    if request.method == "POST":
        crnt = Current.objects.get(id=request.POST['crnt']).code
        qdate = datetime.strptime(request.POST['qdate'], "%Y-%m-%d")
        rate_data = getrate(crnt, qdate)
        quota_data = request.POST.copy()
        quota_data["xchgrt"] = rate_data['in_rate']
        form = UpdateQuotaForm(quota_data, instance=quota)
        if form.is_valid():
            form.save()
            return HttpResponse(
                '<script type="text/javascript">window.close();window.opener.location.reload();</script>'
            )
    else:
        form = UpdateQuotaForm(instance=quota)
    context = {
        'quota': quota,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def quota_newadd(request, inqry_id):
    template = loader.get_template("quotation/inquiry/quota/newadd.html")
    inqry = Inquiry.objects.get(id=inqry_id)
    if request.method == "POST":

        #  add new item
        newitmcnt = Item.objects.filter(sn__startswith="TMP").count()
        sn = "TMP{}{}".format(timezone.now().date().strftime("%Y%m%d"), str(newitmcnt+1).zfill(3))
        newre = request.POST.copy()
        newre['sn'] = sn
        form = AddItemForm(newre, initial={'cate': inqry.cate.id})

        pass  # add item method
        newitem = form.save()

        pass  # create new itemquota and inqry link
        quota = ItemQuota(itemsn_id=newitem.id, inquirysn_id=inqry_id, is_new=True)
        quota.save()

        # update itemquota
        crnt = Current.objects.get(id=request.POST['crnt']).code
        qdate = datetime.strptime(request.POST['qdate'], "%Y-%m-%d")
        rate_data = getrate(crnt, qdate)
        newre["xchgrt"] = rate_data['in_rate']
        qryform = UpdateQuotaForm(newre, instance=quota)
        qryform.save()
        return HttpResponse(
            '<script type="text/javascript">window.close();window.opener.location.reload();</script>'
        )
    else:
        form = AddItemForm(initial={'cate': inqry.cate.id})
        qryform = UpdateQuotaForm(initial={'crnt': 1})
    context = {
        'form': form,
        'qryform': qryform,
    }
    return HttpResponse(template.render(context, request))
