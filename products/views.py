from django.shortcuts import render, redirect
from users.models import User
from .models import Product
from django.contrib import messages


def get_product(request, product_id):
    product = Product.objects.get(id=product_id)
    farmer = product.farmer
    farmer.id = farmer._id
    quantity = []
    for i in range(1, product.quantity+1):
        quantity.append(i)
    context = {"farmer": farmer, "product": product, "quantity": quantity}
    if 'user_id' in request.session:
        if str(request.session['user_id']) == str(product.farmer._id):
            return render(request, "my_product.html", context)
    return render(request, "get_product.html", context)    

def get_products(request, user_id):
    user = User.objects.get(_id=user_id)
    context = {"farmer": user, "products": user.products.all()}
    if 'user_id' in request.session:
        if str(user_id) == str(request.session['user_id']):
            return render(request, "my_products.html", context)
    return render(request, "all_products.html", context)

def new_product(request):
    if 'postData' in request.session:
        context = {
            "product": request.session['postData']
        }
    return render(request, "create_product.html")


def create_product(request):
    context = {}
    errors = Product.objects.product_validator(request.POST, request.FILES)
    if len(errors) > 0:
        request.session['postData'] = request.POST
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/products/new')
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
    messages.success(request, "Product Added!")
    return redirect('/products/'+ request.session['user_id'])

def cancel_new_product(request):
    return redirect("/users")


def edit_product(request, product_id):
    context = {
        "product": Product.objects.get(id=product_id)
    }
    return render(request, "update_product.html", context)

def update_product(request, product_id):
    errors = Product.objects.product_validator(request.POST, request.FILES)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(f'/products/{product_id}/edit')
    else:
    # CONVERT PRICE
        price = request.POST['product_price']
        if "." in price:
            if(len(price[price.find(".")+1: len(price)])) < 2:
                price = price + "0"
        else:
            price = float(price + ".00")
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product = Product.objects.get(id=product_id)
        product.name=request.POST["product_name"]
        product.description=request.POST["product_description"]
        product.price=price
        product.unit=request.POST["product_unit"]
        product.quantity=request.POST["product_quantity"]
        product.save()
        messages.success(request, "Product Updated!")
        return redirect(f'/products/{product_id}')