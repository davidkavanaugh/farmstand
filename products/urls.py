from . import views
from django.urls import path

urlpatterns = [
    path("new", views.new_product),
    path("new/cancel", views.cancel_new_product),
    path("create", views.create_product),
    path("<uuid:user_id>", views.my_products)
]
