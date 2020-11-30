from django.shortcuts import render, redirect
from users.models import User
from .models import Product
from django.contrib import messages
import os
import stripe
stripe.api_key = os.getenv("STRIPE_API_KEY")
from users.repository import RefreshStripeUser
from users.repository import StripeReady
from django.views import View


class ProductListView(View):
    def post(self, request):
        request.session['postData'] = request.POST
        context = {}
        errors = Product.objects.product_validator(request.POST, request.FILES)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/products/new')
        # CREATE PRODUCT DOCUMENT
        Product.objects.create(
            name=request.POST["product_name"],
            description=request.POST["product_description"],
            price=request.POST['product_price'],
            unit=request.POST["product_unit"],
            quantity=request.POST["product_quantity"],
            image=request.FILES['image'],
            farmer=User.objects.get(_id=request.session["user_id"])
        )
        messages.success(request, "Product Added!")
        del request.session['postData']
        return redirect('/users/'+request.session['user_id']+'/products')

    def get(self, request, user_id):
        user = User.objects.get(_id=user_id)
        products = user.products.all()
        # CONVERT PRICE
        for product in products:
            price = str(product.price)
            if "." in price:
                if(len(price[price.find(".")+1: len(price)])) < 2:
                    product.price = price + "0"
            else:
                product.price = price + ".00"
        context = {"farmer": user, "products": products}
        return render(request, "products.list.html", context)        

class ProductDetailView(View):
    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'patch':
            return self.patch(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(ProductDetailView, self).dispatch(*args, **kwargs)
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        farmer = product.farmer
        farmer.id = product.farmer._id
        quantity = []
        for i in range(1, product.quantity+1):
            quantity.append(i)
        context = {
            "product": product,
            "farmer": farmer,
            "quantity": quantity
        }
        return render(request, "products.detail.html", context)
    def patch(self, request, product_id):
        request.session['postData'] = request.POST
        errors = Product.objects.product_update_validator(request.POST, request.FILES)
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
            product = Product.objects.get(id=product_id)
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.name=request.POST["product_name"]
            product.description=request.POST["product_description"]
            product.price=price
            product.unit=request.POST["product_unit"]
            product.quantity=request.POST["product_quantity"]
            product.save()
            messages.success(request, "Product Updated!")
            del request.session['postData']
            return redirect(f'/products/{product_id}')
    def delete(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product.delete()
        messages.success(request, f"{product.name} deleted!")
        return redirect('/users/'+request.session['user_id']+'/products')

def new(request):
    context = {}
    print("getting user:", request.session['user_id'])
    user = User.objects.get(_id=request.session['user_id'])
    user.id = user._id
    context['user'] = user
    print("getting stripe user:", user.stripeId)
    stripe_user = stripe.Account.retrieve(user.stripeId)

    if StripeReady(stripe_user) == True:
        print('user stripe account ready')
        if 'postData' in request.session:
            context['product'] = request.session['postData']
        return render(request, "products.new.html", context)
    else:
        print('user needs to finish stripe onboarding')
        return RefreshStripeUser(user.stripeId)

def edit(request, product_id):
    product = Product.objects.get(id=product_id)
    price = str(product.price)
    if "." in price:
        if(len(price[price.find(".")+1: len(price)])) < 2:
            price = price + "0"
    else:
        price = float(price + ".00")
    product.price = price
    context = {
        "product": product
    }
    return render(request, "products.edit.html", context)