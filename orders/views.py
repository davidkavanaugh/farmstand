from django.http import HttpResponse
from django.views import View
from .models import Order
import json
from users.models import User
from cart.models import CartItem
from products.models import Product
from django.shortcuts import render, redirect


class OrderListView(View):
    def post(self, request):
        try:
            userId = request.POST['userId']
            order = json.loads(request.POST['order'])
            order_total = 0
            order_document = Order.objects.create(
                user=User.objects.get(_id=userId),
            )
            for item in order['items_ordered']:
                order_total += item['item_total']
                cart_item = CartItem.objects.create(
                    product=Product.objects.get(id=item['product_id']),
                    quantity_ordered=item['quantity_ordered']
                )
                order_document.items.add(cart_item)
            order_document.total = order_total
            order_document.save()
            return HttpResponse(order_document.id)
        except Exception:
            raise Exception
    def get(self, request):
        try:
            print(request.session)
            context = {}
            context['orders'] = Order.objects.filter(user=request.session['user_id'])
            return render(request, "orders.html", context)
        except Exception:
            raise Exception


class OrderDetailView(View):
    def get(self, request, orderId):
        try:
            order = Order.objects.get(id=orderId)
            return order
        except Exception:
            raise Exception