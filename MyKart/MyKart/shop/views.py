import json

from django.shortcuts import render
from django.http import HttpResponse
from math import ceil
from .models import Product, Contact, Orders, OrderUpdate


def index(request):
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allprods.append([prod, range(1, nSlides), nSlides])
    params = {'allprods': allprods}
    return render(request, "shop/index.html", params)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()

    return render(request, 'shop/contact.html')


def about(request):
    return render(request, 'shop/about.html')


def pview(request, myid):
    product = Product.objects.filter(id=myid)
    return render(request, "shop/prod-view.html", {'product': product[0]})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    return HttpResponse("We are at search")


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')

        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                       zip_code=zip_code, phone=phone)
        order.save()
        thank = True
        pid = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': pid})
    return render(request, 'shop/checkout.html')
