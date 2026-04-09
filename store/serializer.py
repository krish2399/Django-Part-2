from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length= 20)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','slug','inventory','unit_price','collection','price_with_tax']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=20)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source = 'unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name = 'collection_detail'
    # )
    

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    

    # def validate(self, data):
    #     if data['password']!= data['confrim_password']:
    #         return serializers.ValidationError('Password donot matach')
    #     else:
    #         return data