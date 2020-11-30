from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('<str:zip_code>', views.get_farms)
]
