from . import views
from django.urls import path

app_name = "cart"

urlpatterns = [
    path('', views.index, name='index'),
]
