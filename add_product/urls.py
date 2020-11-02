from . import views
from django.urls import path

app_name = "add_product"

urlpatterns = [
    path('', views.index, name='index'),
]
