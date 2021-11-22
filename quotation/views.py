from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import Company, Item
from .forms import AddCompForm, UpdateCompForm, AddItemForm, UpdateItemForm

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
    context = {
        'comp': comp
    }
    return HttpResponse(template.render(context, request))


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
    template = loader.get_template("quotation/item/detail.html")
    context = {
        'item': item,
    }
    return HttpResponse(template.render(context, request))


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


def item_update(request, item_id):
    template = loader.get_template("quotation/item/update.html")
    item = Item.objects.get(id=item_id)
    if request.method == "POST":
        form = UpdateItemForm(request.POST, instance=item)
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
