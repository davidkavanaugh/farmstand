from . import views
from django.urls import path

urlpatterns = [
    path("", views.all),
    path('<int:order_id>', views.get)
]