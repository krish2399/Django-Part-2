from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from .models import Product, Collection,OrderItem,Review
from .serializer import ProductSerializer, CollectionSerializer,ReviewSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination


   
class ProductViewSet(ModelViewSet):     
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price','last_update']


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
    serializer_class = ReviewSerializer

    def get_queryset(self):
        #  return Review.objects.filter(product_id = self.kwargs['product_pk'])
        
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset =  queryset.filter(collection_id=collection_id)
        return Product.objects.filter(collection_id = self.request.query_params['collection_id'])

    def get_serializer_context(self):
         return {'product_id': self.kwargs['product_pk']}







    

       
    