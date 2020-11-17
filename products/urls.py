from . import views
from django.urls import path

urlpatterns = [
    path("<uuid:user_id>/", views.get_products),
    path('<int:product_id>/', views.get_product),
    path("<int:product_id>/edit", views.edit_product),
    path("<int:product_id>/update", views.update_product),
    path("new", views.new_product),
    path("new/cancel", views.cancel_new_product),
    path("create", views.create_product),
]
