from . import views
from django.urls import path

app_name = "search"

urlpatterns = [
    path('', views.index, name='index'),
    path('get-farms', views.get_farms),
]
