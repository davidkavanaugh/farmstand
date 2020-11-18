from . import views
from django.urls import path

app_name = "cart"

urlpatterns = [
    path('', views.index, name='index'),
    path('add/<int:product_id>', views.add_to_cart),
    path('update/<int:product_id>', views.update_cart),
    path('delete/<int:product_id>', views.delete_item),
    path('checkout', views.checkout)
]
