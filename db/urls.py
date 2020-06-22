from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products),
    path('products/addProduct', views.addProduct),
    path('products/<int:productd_id>/', views.productDetails),
    path('sell/<int:productd_id>/', views.sell),
    path('postSell/', views.postSell),

]

