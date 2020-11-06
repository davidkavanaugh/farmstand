from django.shortcuts import render, redirect


def index(request):
    return render(request, "products.html")


def new_product(request):
    return render(request, "new-product.html")


def create_product(request):
    pass
