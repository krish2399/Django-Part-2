from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from .models import Product, Collection,OrderItem,Review
from .serializer import ProductSerializer, CollectionSerializer,ReviewSerializer


   
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()  
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id =kwargs['pk']).count() > 0 :
                return Response(
                    {'error': 'Product cannot be deleted because it is associated with an order item.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return super().destroy(request, *args, **kwargs)



class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('product')).all()
    serializer_class = CollectionSerializer   


    def delete(self, request,pk):
        collection = self.get_object()

        if collection.product_set.count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted because it includes one or more products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        return self.response(status = status.HTTP_204_NO_CONTENT)
    
class ReviewViewSet(ModelViewSet):
     queryset = Review.objects.all()
     serializer_class = ReviewSerializer


   
    





    

       
    