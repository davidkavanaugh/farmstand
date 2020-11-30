from . import views
from django.urls import path

urlpatterns = [
    path('', views.ProductListView.as_view()),
    path('<int:product_id>', views.ProductDetailView.as_view()),
    path("<int:product_id>/edit", views.edit),
    path("new", views.new),
]
