from datetime import datetime
from django.utils.dateparse import parse_date
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render,redirect
from db.models import Question, Product,Contract
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
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST["Name"]
            count = request.POST["Count"]
            exireDate = parse_date(request.POST["ExireDate"])
            ownerId=request.user.id
            pubDate = datetime.now().date()
            product = Product(name=name , count=count,expire_date=exireDate,ownerID=ownerId,pub_date=pubDate)
            product.save()
            return redirect("/products")
        else:
            return render(request, 'db/addProduct.html')
        # return HttpResponse("Add Question")
    else:
        return redirect("/admin")

class ContractModel:
    def __init__(self, Id, seller,buyer, info, date,prehash, currentHash):
        self.Id = Id
        self.seller = seller
        self.buyer = buyer
        self.info = info
        self.date = date
        self.prehash = prehash
        self.currentHash = currentHash
def productDetails(request,productd_id):
    product = get_object_or_404(Product, id=productd_id)
    contracts = Contract.objects.filter(product_id = productd_id)
    cons = []
    for con in contracts:
        seller = User.objects.filter(id = con.sellerID).first()
        buyer = User.objects.filter(id = con.buyerID).first()
        cons.append(ContractModel(con.id,seller,buyer,con.info,con.date,'',''))
    ownerId = request.user.id
    Sellable = 'False'
    if product.ownerID == ownerId:
        Sellable = 'True'
    return render(request, 'db/product.html', {'product': product , "contracts":cons,"sellable":Sellable})

def sell(request,productd_id):
    if request.user.is_authenticated:
            users = User.objects.all()
            product = get_object_or_404(Product, id=productd_id)
            ownerId = request.user.id
            if(product.ownerID != ownerId):
                return redirect("/products")
            return render(request, 'db/sell.html', {'product': product ,"users":users })
    else:
        return redirect("/admin")

def postSell(request):
    if  request.method == "POST":
        if request.user.is_authenticated:
            ownerId = request.user.id
            newOnwer = request.POST["buyer"]
            productID = request.POST["productID"]
            product = get_object_or_404(Product, id=productID)
            des = request.POST["des"]
            data =str(ownerId) + str(newOnwer) + str(productID) +des
            hash_object = hashlib.md5(bytes(data, encoding='utf-8'))
            hash =hash_object.hexdigest()
            prehash ='',
            product.ownerID = newOnwer
            if Contract.objects.count()>0:
                prehash = Contract.objects.reverse()[Contract.objects.count()-1].strHash
            contract = Contract(info = des,strHash = hash ,sellerID=ownerId,buyerID=newOnwer,date= datetime.now().date()
                                , product_id=productID, prevHash=prehash)
            product.save()
            contract.save()
            return redirect("/products/")
        else:
            return redirect("/admin")

def index(request):
    return render(request, 'db/index.html')

