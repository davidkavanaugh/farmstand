from django.shortcuts import render, redirect
from users.models import User
from .models import Product


def new_product(request):
    return render(request, "new-product.html")


def create_product(request):
    # CONVERT PRICE
    price = request.POST['product_price']
    if "." in price:
        if(len(price[price.find(".")+1: len(price)])) < 2:
            price = price + "0"
    else:
        price = float(price + ".00")

    # CREATE PRODUCT DOCUMENT
    Product.objects.create(
        name=request.POST["product_name"],
        description=request.POST["product_description"],
        price=price,
        unit=request.POST["product_unit"],
        quantity=request.POST["product_quantity"],
        image=request.FILES['image'],
        farmer=User.objects.get(_id=request.session["user_id"])
    )
    return redirect('/users')


def cancel_new_product(request):
    return redirect("/users")
