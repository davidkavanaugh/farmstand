from django.shortcuts import render, redirect
from users.models import User
from .models import Product
from django.contrib import messages


def get_products(request, user_id):
    user = User.objects.get(_id=user_id)
    context = {"farmer": user}
    if 'user_id' in request.session:
        if str(user_id) == str(user._id):
            return render(request, "my_products.html", context)
    return render(request, "all_products.html", context)

def new_product(request):
    return render(request, "create_product.html")


def create_product(request):
    errors = Product.objects.product_validation(request.POST, request.FILES)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        request.session['postData'] = request.POST
        return redirect('/products/create')
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


