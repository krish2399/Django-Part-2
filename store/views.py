from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Product, Collection
from .serializer import ProductSerializer, CollectionSerializer

class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}

   


class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()  
    serializer_class = ProductSerializer

   
    
    def delete(self,request,pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.exists():
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CollectionDetails(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('product')
    )
    serializer_class = CollectionSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        collection = self.get_object()

        if collection.product_set.count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted because it includes one or more products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        return self.response(status = status.HTTP_204_NO_CONTENT)
         

    

       
    