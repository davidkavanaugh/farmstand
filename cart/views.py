from django.shortcuts import render, redirect
from users.models import User
from products.models import Product
from cart.models import Cart, CartItem
from orders.models import Order
import uuid
import stripe
import os
import requests
import json
stripe.api_key = os.getenv("STRIPE_API_KEY")
def GetUserByProductId(productId):
    user = Product.objects.get(id=productId).farmer
    return user
def GetUserByUserId(userId):
    user = User.objects.get(_id=userId)
    return user


def index(request):
    context = {}
    cart = []
    if 'cart' in request.session:
        checkout_total = 0
        for key in request.session['cart']:
            farmer = GetUserByProductId(key)
            product = Product.objects.filter(id=key)
            if len(product) > 0:
                product = product[0]
                if product.quantity > 0:
                    price = str(product.price)
                    if "." in price:
                        if(len(price[price.find(".")+1: len(price)])) < 2:
                            product.price = price + "0"
                    else:
                        product.price = price + ".00"
                    quantArr = []
                    for i in range(0, product.quantity+1):
                        quantArr.append(i)
                    quantity_ordered = int(request.session['cart'][key])
                    if quantity_ordered > product.quantity:
                        quantity_ordered = product.quantity
                    total = round(float(quantity_ordered) * float(product.price), 2)
                    # if "." in total:
                    #     if(len(total[total.find(".")+1: len(total)])) < 2:
                    #         total = round(total + "0", 2)
                    # else:
                    #     total = round(total + ".00", 2)
                    print(total)
                    checkout_total = round(float(checkout_total) + float(total), 2)
                    print(checkout_total)
                    cart.append({
                        "product": {
                            "id": product.id,
                            "name": product.name,
                            "price": product.price,
                            "unit": product.unit,
                            "image": product.image,
                            "quantity": quantArr,
                            "farmer": {
                                "name": product.farmer.farm_name,
                                "address": {
                                    "street_1": product.farmer.address.street_1,
                                    "street_2": product.farmer.address.street_2,
                                    "city": product.farmer.address.city,
                                    "state": product.farmer.address.state,
                                    "zip_code": product.farmer.address.zip_code
                                },
                                "instructions": product.farmer.instructions
                            }
                        },
                        "quantity_ordered": quantity_ordered,
                        "total": total,
                    })
        cart_total = str(checkout_total)
        if "." in cart_total:
            if(len(cart_total[cart_total.find(".")+1: len(cart_total)])) < 2:
                cart_total = cart_total + "0"
        else:
            cart_total = cart_total + ".00"
        context['checkout_total'] = cart_total
    non_user_cart = cart
    context['cart'] = cart
    return render(request, "cart.html", context)

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = {}
    if 'user_id' in request.session:
    # LOGGED IN
        cart = Cart.objects.filter(user=User.objects.get(_id=request.session['user_id']))
        if len(cart) > 0:
            cart = cart[0]
        # logged user has cart
            for item in cart.items.all():
                # logged user has this item in cart
                if item.product.id == product_id:
                    item.quantity_ordered += int(request.POST['quantity'])
                    item.save()
                    return redirect('/products/'+ product.farmer._id)
        else:
        # logged user no cart
            cart = Cart.objects.create(
                user = User.objects.get(_id=request.session['user_id'])
            )
        cart_item = CartItem.objects.create(
            cart=cart,
            product=product,
            quantity_ordered=request.POST['quantity']
        )
        cart.items.add(cart_item)
    # NOT LOGGED IN, 
    else:
        # IF NO CART
        if not 'cart' in request.session:
            request.session['cart'] = {}
        cart = request.session['cart']
        if str(product_id) in cart:
            quantity = request.POST['quantity']
            print('ADDING '+quantity+' MORE ' + product.name)
            current_sum = cart[str(product_id)]
            new_sum = int(current_sum) + int(quantity)
            cart[str(product_id)] = new_sum
        else:
            quantity = request.POST['quantity']
            print('ADDING '+quantity+" "+product.name)
            cart[str(product_id)] = quantity
        request.session['cart'] = cart
    return redirect('/products/'+ product.farmer._id)

def update_cart(request, product_id):
    if int(request.POST['quantity']) == 0:
        delete_item(request, product_id)
    else:
        cart = request.session['cart']
        for key in cart:
            if key == str(product_id):
                cart[key] = int(request.POST['quantity'])
        request.session['cart'] = cart
    return redirect('/cart')

def delete_item(request, product_id):
    if 'user_id' in request.session:
        user = User.objects.get(_id=request.session['user_id'])
        cart = Cart.objects.filter(user=user)
        if len(cart) > 0:
            items = cart[0].items.all()
            for item in items:
                if item.product.id == product_id:
                    cart_item = CartItem.objects.get(id=item.id)
                    cart_item.delete()
    else:
        cart = request.session['cart']
        cart.pop(str(product_id))
        request.session['cart'] = cart
    
    return redirect('/cart')

def checkout(request):
    context = {}
    order_object = {}
    order_total = 0
    if 'user_id' in request.session:
        cart = Cart.objects.get(user=User.objects.get(_id=request.session['user_id']))
        for item in cart.items.all():
            if not item.product.farmer._id in order_object:
                order_object[item.product.farmer._id] = {
                    "seller_name": item.product.farmer.farm_name,
                    "seller_email": item.product.farmer.email,
                    "seller_address": {
                        "street_1": item.product.farmer.address.street_1,
                        "street_2": item.product.farmer.address.street_2,
                        "city": item.product.farmer.address.city,
                        "state": item.product.farmer.address.state,
                        "zip_code": item.product.farmer.address.zip_code,
                    },
                    "seller_instructions": item.product.farmer.instructions,
                    "items_ordered": []
                }
            order_object[item.product.farmer._id]['items_ordered'].append({
                "product_id": item.product.id,
                "product_name": item.product.name,
                "product_price": item.product.price,
                "product_unit": item.product.unit,
                "quantity_ordered": item.quantity_ordered,
                "item_total": item.quantity_ordered * item.product.price
            })
            order_total += item.quantity_ordered * item.product.price
    else:
        cart = request.session['cart']
        for item in cart:
            product = Product.objects.filter(id=item)
            if len(product) > 0:
                product = product[0]
            else: 
                continue
            if not product.farmer._id in order_object:
                order_object[product.farmer._id] = {
                    "seller_name": product.farmer.farm_name,
                    "seller_email": product.farmer.email,
                    "seller_address": {
                        "street_1": product.farmer.address.street_1,
                        "street_2": product.farmer.address.street_2,
                        "city": product.farmer.address.city,
                        "state": product.farmer.address.state,
                        "zip_code": product.farmer.address.zip_code,
                    },
                    "seller_instructions": product.farmer.instructions,
                    "items_ordered": []
                }
            order_object[product.farmer._id]['items_ordered'].append({
                "product_id": product.id,
                "product_name": product.name,
                "product_price": product.price,
                "product_unit": product.unit,
                "quantity_ordered": cart[item],
                "item_total": float(cart[item]) * product.price
            })
            order_total += float(cart[item]) * product.price
    order_total = int(order_total * 100)
    order_object['order_total'] = order_total
    print('order total:', order_total)
    transfer_group = uuid.uuid4().hex
    # Create a PaymentIntent:
    payment_intent = stripe.PaymentIntent.create(
        amount=order_total,
        currency='usd',
        payment_method_types=['card'],
        transfer_group=transfer_group,
    )
    for userId in order_object:
        if userId == 'order_total':
            continue
        user = User.objects.get(_id=userId)
        transfer_total = 0
        items_ordered = order_object[userId]['items_ordered']
        for item in items_ordered:
            transfer_total += item['item_total']
        transfer_total = int(transfer_total * 90)
        transfer = stripe.Transfer.create(
            amount=transfer_total,
            currency="usd",
            destination=user.stripeId,
            transfer_group=transfer_group,
        )
        print('transfer: ', transfer.id, transfer.amount)
    context['payment_intent'] = payment_intent
    context['stripe_key'] = os.getenv("STRIPE_PUBLISH_KEY")
    request.session['order'] = order_object
    return render(request, "stripe_payment.html", context)

def checkout_success(request):
    if not 'order' in request.session:
        return redirect('/cart')
    receipt = {
        'sale_total': float(request.session['order']['order_total'] / 100),
        'orders': []
    }
    for key in request.session['order']:
        if key != 'order_total':
            payload = {"userId": key, "order": json.dumps(request.session['order'][key])}
            order_document = requests.post("http://localhost:8000/orders/", data=payload)
            receipt['orders'].append(
                Order.objects.get(id=order_document.text)
            )
    del request.session['cart']
    del request.session['order']
    return render(request, "checkout_success.html", receipt)
    cart = []
    request.session['order'] = {}
    if 'cart' in request.session:
        checkout_total = 0
        # key is product id
        for key in request.session['cart']:
            product = Product.objects.filter(id=key)
            if len(product) > 0:
                product = product[0]
                price = str(product.price)
                if "." in price:
                    if(len(price[price.find(".")+1: len(price)])) < 2:
                        product.price = price + "0"
                else:
                    product.price = price + ".00"
                quantity_ordered = int(request.session['cart'][key])
                total = str(float(quantity_ordered) * float(product.price))
                if "." in total:
                    if(len(total[total.find(".")+1: len(total)])) < 2:
                        total = total + "0"
                else:
                    total = total + ".00"
                checkout_total = float(checkout_total) + float(total)
                cart.append({
                    "product": {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "unit": product.unit,
                        "image": product.image,
                        "quantity": quantity_ordered, 
                        
                    },
                    "quantity_ordered": quantity_ordered,
                    "total": total,
                })
        cart_total = str(checkout_total)
        if "." in cart_total:
            if(len(cart_total[cart_total.find(".")+1: len(cart_total)])) < 2:
                cart_total = cart_total + "0"
        else:
            cart_total = cart_total + ".00"
        context['checkout_total'] = cart_total
        non_user_cart = cart
        context['cart'] = cart
    del request.session['order']
    del request.session['cart']
    return render(request, "checkout_success.html", context)  