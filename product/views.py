from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from django.db.models import Q
from api_MercadoLivre.getContent import getInfoFromProduct, get_access_token
from decouple import config
from django.contrib.auth.decorators import login_required
from .models import TrackingProduct, Product


@login_required
def index(request):
    if request.method == "GET":
        app_id = config('APP_ID')
        client_secret = config('CLIENT_SECRET')
        refresh_token = config('REFRESH_TOKEN')
        
        access_token = get_access_token(app_id, client_secret, refresh_token)
        access_token = access_token["access_token"]   
        # key_word = request.GET.get("keyWord")
        product_id = request.GET.get("product_id")
        # products = Product.objects.filter(Q(id=product_id) & Q(user=request.user)).all()
        if product_id:
            product_info = getInfoFromProduct(access_token, product_id)
            if product_info:
       
                return render(request, "product/index.html", {'product' : product_info})

        return render(request, "product/index.html")

    elif request.method == "POST":
        return render(request, "product/index.html")

    

