from . import views
from django.urls import path

urlpatterns = [
    path('', views.CartListView.as_view()),
    path('<int:product_id>', views.CartDetailView.as_view()),
    path('checkout', views.checkout),
    path('checkout/success', views.checkout_success)
]
