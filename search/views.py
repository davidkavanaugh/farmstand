from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from django.contrib import messages
import json
from users.models import User, Address
import os

def get_farms(request, zip_code):
    request.session['zipCode'] = request.POST['zipCode']
    request.session['search_radius'] = request.POST['search-radius']
    context = {
        "zipCode": request.POST['zipCode'],
        "farms": []
    }
    headers = {"apikey": os.getenv("ZIP_KEY")}

    params = (
        ("code", request.POST["zipCode"]),
        ("radius", request.POST["search-radius"]),
        ("country", "us"),
        ("unit", "miles")
    )

    response = requests.get(
        os.getenv("ZIP_DOMAIN"), headers=headers, params=params)
    res = json.loads(response.text)["results"]
    if len(res) == 0:
        messages.error(request, "No Farms Found")
        return redirect("/")
    for location in res:
        addresses = Address.objects.filter(zip_code=location["code"])
        for address in addresses:
            print(address)
            farmer = User.objects.get(_id=address.user._id)
            if len(farmer.products.all()) > 0:
                farmer.id = farmer._id
                context["farms"].append(farmer)
    return render(request, "search-results.html", context)

def index(request):
    if 'user_id' in request.session:
        user = User.objects.get(_id=request.session['user_id'])
        return redirect(f'/users/{user._id}')
    if 'zipCode' in request.session:
        context = {
            "zipCode": request.session['zipCode'],
            "search_radius": request.session['search_radius']
        }
    return render(request, "index.html")