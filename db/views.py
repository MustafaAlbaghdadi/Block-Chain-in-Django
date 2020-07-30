from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from db.models import Question, Product, Contract
from django.contrib.auth.models import User
import hashlib


def products(request):
    if request.user.is_authenticated:
        ownerId = request.user.id
        productList = Product.objects.filter(ownerID=ownerId)
        context = {'productList': productList}
        return render(request, 'db/products.html', context)
    else:
        return redirect("/admin")


def AllProduct(request):
    if request.user.is_authenticated:
        productList = Product.objects.all()
        context = {'productList': productList}
        return render(request, 'db/AllProduct.html', context)
    else:
        return redirect("/admin")


def contracts(request):
    if request.user.is_authenticated:
        contracts = Contract.objects.all()
        cons = []
        for con in contracts:
            seller = User.objects.filter(id=con.sellerID).first()
            buyer = User.objects.filter(id=con.buyerID).first()
            cons.append(ContractModel(con.id, seller, buyer, con.info, con.date, con.prevHash, con.strHash))
        context = {'contracts': cons}
        return render(request, 'db/contracts.html', context)
    else:
        return redirect("/admin")


def addProduct(request):
    if request.user.is_authenticated and str(request.user.groups.all().first()) == 'Farmer':
        if request.method == "POST":

            product = Product(name=request.POST["Name"],
                              count=request.POST["Count"],
                              ownerID=request.user.id,
                              pub_date=datetime.now().date(),
                              farmerID=request.user.id,
                              farm_temp=request.POST["farm_temp"],
                              farm_humidity=request.POST["farm_humidity"],
                              compost_type=request.POST["compost_type"],
                              seed_type=request.POST["seed_type"],
                              unite_type=request.POST["unite_type"],
                              date_of_harvest=request.POST["date_of_harvest"],
                              farm_location=request.POST["farm_location"],
                              )
            product.save()
            return redirect("/products")
        else:
            return render(request, 'db/addProduct.html')
        # return HttpResponse("Add Question")
    else:
        return redirect("/admin")


class ContractModel:
    def __init__(self, Id, seller, buyer, info, date, prehash, currentHash):
        self.Id = Id
        self.seller = seller
        self.buyer = buyer
        self.info = info
        self.date = date
        self.prehash = prehash
        self.currentHash = currentHash


def productDetails(request, productd_id):
    product = get_object_or_404(Product, id=productd_id)
    contracts = Contract.objects.filter(product_id=productd_id)
    cons = []
    for con in contracts:
        seller = User.objects.filter(id=con.sellerID).first()
        buyer = User.objects.filter(id=con.buyerID).first()
        cons.append(ContractModel(con.id, seller, buyer, con.info, con.date, '', ''))
    ownerId = request.user.id
    Sellable = 'False'
    if product.ownerID == ownerId:
        Sellable = 'True'
    return render(request, 'db/product.html', {'product': product, "contracts": cons, "sellable": Sellable,
                                               "farmer": User.objects.filter(id=product.farmerID).first(),
                                               "factory": User.objects.filter(id=product.factoryID).first(),
                                               "distrabuter": User.objects.filter(id=product.distrabuterID).first(),
                                               "markting": User.objects.filter(id=product.marktingID).first(),
                                               })


def sell(request, productd_id):
    if request.user.is_authenticated:
        users = User.objects.all()
        product = get_object_or_404(Product, id=productd_id)
        state = 0
        if product.factoryID == 0:
            users = User.objects.filter(groups__name__in=['Factory']).all()
            state = 1
        if product.distrabuterID == 0:
            users = User.objects.filter(groups__name__in=['Distrabuter']).all()
            state = 2
        if product.marktingID == 0:
            users = User.objects.filter(groups__name__in=['marketer']).all()
            state = 3
        ownerId = request.user.id
        if (product.ownerID != ownerId):
            return redirect("/products")
        return render(request, 'db/sell.html', {'product': product, "users": users, "state": state})
    else:
        return redirect("/admin")


def postSell(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            ownerId = request.user.id
            newOnwer = request.POST["buyer"]
            productID = request.POST["productID"]
            product = get_object_or_404(Product, id=productID)
            des = request.POST["des"]
            data = str(ownerId) + str(newOnwer) + str(productID) + des
            hash_object = hashlib.md5(bytes(data, encoding='utf-8'))
            hash = hash_object.hexdigest()
            prehash = '',
            if Contract.objects.count() > 0:
                prehash = Contract.objects.reverse()[Contract.objects.count() - 1].strHash
            contract = Contract(info=des, strHash=hash, sellerID=ownerId, buyerID=newOnwer, date=datetime.now().date()
                                , product_id=productID, prevHash=prehash)

            if request.POST["state"] == '1':
                product.ownerID = newOnwer
                product.canning_date = request.POST["canning_date"]
                product.processing_date = request.POST["processing_date"]
                product.expire_date = request.POST["expire_date"]
                product.factory_temp = request.POST["factory_temp"]
                product.factory_humidity = request.POST["factory_humidity"]
                product.factoryID = newOnwer
            if request.POST["state"] == '2':
                product.ownerID = newOnwer
                product.distrabuterID = newOnwer
                product.destrbutor_temp = request.POST["destrbutor_temp"]
                product.destrbutor_humidity = request.POST["destrbutor_humidity"]
                product.entry_store_date = request.POST["entry_store_date"]
                product.unite_type = request.POST["unite_type"]
                product.count = request.POST["Count"]
            if request.POST["state"] == '3':
                if int(request.POST["Count"]) < product.count:
                    p = Product(
                        name=product.name,
                        pub_date=product.pub_date,
                        ownerID=newOnwer,
                        farmerID=product.farmerID,
                        farm_temp=product.farm_temp,
                        farm_humidity=product.farm_humidity,
                        compost_type=product.compost_type,
                        seed_type=product.seed_type,
                        date_of_harvest=product.date_of_harvest,
                        farm_location=product.farm_location,
                        factoryID=product.factoryID,
                        canning_date=product.canning_date,
                        processing_date=product.processing_date,
                        expire_date=product.expire_date,
                        factory_temp=product.factory_temp,
                        factory_humidity=product.factory_humidity,
                        distrabuterID=product.distrabuterID,
                        entry_store_date=product.entry_store_date,
                        destrbutor_temp=product.destrbutor_temp,
                        destrbutor_humidity=product.destrbutor_humidity,
                        market_temp=request.POST["market_temp"],
                        market_humidity=request.POST["market_humidity"],
                        unite_type=request.POST["unite_type"],
                        entry_market_date=request.POST["entry_market_date"],
                        count=request.POST["Count"]

                    )
                    product.count = int(product.count) - int(p.count)
                    p.save()
                else:
                    product.ownerID = newOnwer
                    product.marktingID = newOnwer
                    product.market_temp = request.POST["market_temp"]
                    product.market_humidity = request.POST["market_humidity"]
                    product.entry_market_date = request.POST["entry_market_date"]
                    product.unite_type = request.POST["unite_type"]
                    product.count = request.POST["Count"]

            product.save()
            contract.save()
            return redirect("/products/")
        else:
            return redirect("/admin")


def index(request):
    group = request.user.groups.all().first()
    return render(request, 'db/index.html', {'mygroup': group})
