from . import views
from django.urls import path

app_name = "cart"

urlpatterns = [
    path('', views.index, name='index'),
    path('add/<int:product_id>', views.add_to_cart)
]
