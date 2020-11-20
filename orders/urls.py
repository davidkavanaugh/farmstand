from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', csrf_exempt(views.OrderListView.as_view())),
    path('<int:order_id>', views.OrderDetailView.as_view()),
]