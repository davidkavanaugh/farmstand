from django.shortcuts import render, redirect
from users.models import User
from products.models import Product
from cart.models import Cart, CartItem


def index(request):
    context = {}
    if 'user_id' in request.session:
        user = User.objects.get(_id=request.session['user_id'])
        context['user'] = user
        if cart in user:
            print('has cart')
    else: 
        print('not logged in')
        if 'cart' in request.session:
            context['cart'] = request.session['cart']
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
                    for item in cart.items.all():
                        print(item.product.name, item.quantity_ordered)
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
        for item in cart.items.all():
            print(item.product.name, item.quantity_ordered)
    # NOT LOGGED IN, 
    else:
        print('user not logged in')
        # IF NO CART
        if not 'cart' in request.session:
            request.session['cart'] = {}
        cart = request.session['cart']
        if str(product_id) in cart:
            quantity = request.POST['quantity']
            print('ADDING '+quantity+' MORE ' + product.name)
            current_sum = cart[str(product_id)]
            print('CURRENT SUM: '+product.name, current_sum)
            new_sum = int(current_sum) + int(quantity)
            print('NEW SUM: '+product.name, new_sum)
            cart[str(product_id)] = new_sum
        else:
            quantity = request.POST['quantity']
            print('ADDING '+quantity+" "+product.name)
            cart[str(product_id)] = quantity
        request.session['cart'] = cart
        print("ANON_CART: ",request.session['cart'])
    
    return redirect('/products/'+ product.farmer._id)