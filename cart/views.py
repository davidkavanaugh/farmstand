from django.shortcuts import render, redirect
from products.models import Product


def index(request):
    return render(request, "cart.html")

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    # del request.session['cart']
    if 'cart' in request.session:
        cart = request.session['cart']
    else:
        cart = {}

    # LOGGED IN
    if 'user_id' in request.session:
        #  IF NO CART
        print('user logged in')
        if not request.session['user_id'] in cart:
            cart[request.session['user_id']] = {}
        my_cart = cart[request.session['user_id']]

    # NOT LOGGED IN, 
    else:
        print('user not logged in')
        # IF NO CART
        if not 'anon' in cart:
            cart['anon'] = {}
        my_cart = cart['anon']

    if str(product_id) in my_cart:
        quantity = request.POST['quantity']
        print('ADDING '+quantity+' MORE ' + product.name)
        current_sum = my_cart[str(product_id)]
        print('CURRENT SUM: '+product.name, current_sum)
        new_sum = int(current_sum) + int(quantity)
        print('NEW SUM: '+product.name, new_sum)
        my_cart[str(product_id)] = new_sum
    else:
        quantity = request.POST['quantity']
        print('ADDING '+quantity+" "+product.name)
        my_cart[str(product_id)] = quantity
    if 'user_id' in request.session:
        request.session['cart'] = {
            request.session['user_id']: my_cart
        }
    else:
        request.session['cart'] = {
            "anon": my_cart
        }
    print("NEW_CART: ",request.session['cart'])
    
    return redirect('/products/'+ product.farmer._id)