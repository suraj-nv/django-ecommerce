from rest_framework import serializers
from decimal import Decimal
from .models import Product,Collection, Review

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','product_count']
    product_count = serializers.IntegerField(read_only=True)
        
    
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'price_with_tax',
            'inventory',
            'collection',
        ]
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(max_length=100)
    # unit_price = serializers.DecimalField(max_digits=10, decimal_places=2,source='price')
    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # # collection= serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )
    # inventory = serializers.IntegerField()
    def calculate_tax(self, product: Product):
        return product.price * Decimal('1.1')
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review 
        fields = ['id', 'name', 'description', 'date']
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)        
   