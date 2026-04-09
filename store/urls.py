from django.urls import path
from . import views


# URLConf

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetails.as_view()),
    path('collectins/<int:pk>/', views.CollectionDetails.as_view(),name = 'collection_detail')
]
