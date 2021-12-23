import requests
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Company, Item, Inquiry, ItemQuota, Current, Category, Manufacturer
from .forms import AddCompForm, UpdateCompForm, AddItemForm, UpdateItemForm, AddInquiryForm, UpdateQuotaForm
from django.utils import timezone
from datetime import datetime
from .custom.exchange import getrate
from django.contrib.auth.decorators import login_required
from .custom import export
from pathlib import Path, PurePath

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


# 歷史報價匯出
def item_hstr_export(request, item_id):
    item = Item.objects.get(id=item_id)
    quotas = ItemQuota.objects.filter(itemsn_id=item_id).order_by("-qdate")
    quotas_data = {
        'item_sn': item.sn,
        'item_name': item.name,
        'data': [],
    }
    # 製作資料
    if quotas.count() != 0:
        for quota in quotas:
            if quota.price:
                quotas_data['data'].append({
                    'item_sn': item.sn,
                    'item_name': item.name,
                    'item_cate': item.cate.name,
                    'item_mfg': item.mfg.name,
                    'item_spec': item.specmain,
                    'cnt': quota.count,
                    'price': quota.price,
                    'crnt': quota.crnt.code,
                    'xchgrt': quota.xchgrt,
                    'TWD_price': quota.ntd_price(),
                    'qdate': quota.qdate,
                })
    file_name = export.item_to_excel(quotas_data)
    file_date = file_name.split("_")[2][0:6]
    [fyear, fmon] = [file_date[0:4], file_date[4:6]]
    print(fyear, fmon)
    return HttpResponseRedirect("/static/files/itemhistory/output/{}/{}/{}".format(fyear, fmon, file_name))


# 取得物品序號
def get_itemsn(cate_id, mfg_id, spec):
    cate = Category.objects.get(id=cate_id).sn
    mfg = Manufacturer.objects.get(id=mfg_id).sn
    return '{}{}{}'.format(cate, mfg, spec.zfill(8))


@login_required
def item_add(request):
    template = loader.get_template("quotation/item/add.html")
    if request.method == "POST":
        sn = get_itemsn(cate_id=request.POST['cate'], mfg_id=request.POST['mfg'], spec=request.POST['specmain'])
        new_reqst = request.POST.copy()
        new_reqst['sn'] = sn
        form = AddItemForm(new_reqst)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("../")
        else:
            context = {
                'form': form,
            }
            return HttpResponse(template.render(context, request))
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
    else:
        form = AddInquiryForm()
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
def inquiry_export(request, inqry_id):
    inquiry = Inquiry.objects.get(id=inqry_id)
    quotas_old = ItemQuota.objects.filter(inquirysn_id=inqry_id, is_new=False)
    data = {
        'inquiryid': inquiry.sn,
        'date': inquiry.startdate,
        'author': inquiry.author.last_name+inquiry.author.first_name,
        'author_tel': '02-2796-1122',
        'company': inquiry.company.fullname,
        'comp_contact': inquiry.company.spnsr,
        'contact_tel': '{} ext:{}'.format(inquiry.company.tel, inquiry.company.tel_ext),
        'category': inquiry.cate.name,
        'quotas': [],
    }

    if quotas_old.count() != 0:
        for quota in quotas_old:
            data['quotas'].append({
                'item_sn': quota.itemsn.sn,
                'item_name': quota.itemsn.name,
                'item_mfg': quota.itemsn.mfg.name,
                'item_spec': quota.itemsn.specmain,
            })
    file_name = export.to_excel(data)
    file_date = file_name.split("_")[3][0:6]
    [fyear, fmon] = [file_date[0:4], file_date[4:6]]
    print(fyear, fmon)
    return HttpResponseRedirect("/static/files/inquiry/output/{}/{}/{}".format(fyear, fmon, file_name))

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
            return redirect('./')
    else:
        if quota.crnt is None:
            form = UpdateQuotaForm(initial={})
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
        sn = get_itemsn(cate_id=request.POST['cate'], mfg_id=request.POST['mfg'], spec=request.POST['specmain'])
        newre = request.POST.copy()
        newre['sn'] = sn
        form = AddItemForm(newre)

        # add item method
        if form.is_valid():
            newitem = form.save()

            # create new itemquota and inqry link
            quota = ItemQuota(
                itemsn_id=newitem.id,
                inquirysn_id=inqry_id,
                is_new=True,
            )
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
            context = {
                'form': form,
                'qryform': UpdateQuotaForm(request.POST),
            }
            return HttpResponse(template.render(context, request))
    else:
        form = AddItemForm()
        form.fields['cate'].queryset = Category.objects.filter(id=inqry.cate.id)
        form.fields['cate'].initial = inqry.cate.id
        qryform = UpdateQuotaForm(
            initial={
                'crnt': 1,
                # 'qdate': timezone.now().strftime("%Y-%m-%d"),
            })
    context = {
        'form': form,
        'qryform': qryform,
    }
    return HttpResponse(template.render(context, request))
