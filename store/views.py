from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

import rest_framework
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework import status
from .Serializers import AddCartItemSerializer, CartItemSerializer, ProductSerializer,UpdateCartItemSerializer,CollectionSerializer,ReviewSerializer,CartSerializer
from .models import Cart, OrderItem, Product,Collection, Review, CartItem
from .filters import ProductFilter

class ReviewViewSet(ModelViewSet):
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    serializer_class = ReviewSerializer
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
    
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'last_update']
    # pagination_class = PageNumberPagination
    # def get_queryset(self):
    #       queryset = Product.objects.all()
    #       collection_id = self.request.query_params.get('collection_id')
    #       if collection_id is not None:
    #             queryset = queryset.filter(collection_id=collection_id)
    #       return queryset      
    serializer_class = ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated with an order item.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)
    
# class ProductList(ProductViewSet):
    
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    # # def get_queryset(self):
    #     # return Product.objects.select_related('collection').all()
    
    # # def get_serializer_class(self):
    #     # return ProductSerializer
    
    # def get_serializer_context(self):
    #     return {'request': self.request}

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'id'
    
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitem_set.count() > 0:
#             return Response(
#                 {'error': 'Product cannot be deleted because it is associated with an order item.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def product_list(request):
    # if request.method == 'GET':
    #     query_set = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(query_set, many=True, context={'request': request})
    #     return Response(serializer.data)
    
    # elif request.method == 'POST':
    #     serializer = ProductSerializer(data=request.data)

    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
    # product = get_object_or_404(Product, pk=id)
    # if request.method == 'GET':
       
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # elif request.method == 'PUT':
    #     serializer = ProductSerializer(product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    # elif request.method == 'DELETE':
    #     if product.orderitem_set.count() > 0:
    #         return Response(
    #             {'error': 'Product cannot be deleted because it is associated with an order item.'},
    #             status=status.HTTP_405_METHOD_NOT_ALLOWED
    #         )
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        product_count=Count('product')
    )
    serializer_class = CollectionSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted because it contains products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)
# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         product_count=Count('product')
#     )
#     serializer_class = CollectionSerializer
#     # def get_queryset(self):
#     #     return Collection.objects.annotate(
#     #         product_count=Count('product')
#     #     )

#     # def get_serializer_class(self):
#     #     return CollectionSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}
        
    
    
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         product_count=Count('product')
#     )
#     serializer_class = CollectionSerializer
#     # lookup_field = 'id'
       
   
#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(
#             product_count=Count('product')
#         ), pk=pk)
#         if collection.product_set.count() > 0:
#             return Response(
#                 {'error': 'Collection cannot be deleted because it contains products.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# # @api_view(['GET', 'POST'])
# # def collection_list(request):
#     # if request.method == 'GET':
#     #     query_set = Collection.objects.annotate(
#     #         product_count=Count('product')
#     #     )
#     #     serializer = CollectionSerializer(query_set, many=True, context={'request': request})
#     #     return Response(serializer.data)
    
#     # elif request.method == 'POST':
#     #     serializer = CollectionSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# # @api_view(['GET', 'PUT', 'DELETE'])
#  def collection_detail(request, id):
    # collection = get_object_or_404(Collection.objects.annotate(
    #         product_count=Count('product')
    #     ), pk=id)
    # if request.method == 'GET':
       
    #     serializer = CollectionSerializer(collection)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # elif request.method == 'PUT':
    #     serializer = CollectionSerializer(collection, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data,status=status.HTTP_200_OK)
    # elif request.method == 'DELETE':
    #     if collection.product_set.count() > 0:
    #         return Response(
    #             {'error': 'Collection cannot be deleted because it contains products.'},
    #             status=status.HTTP_405_METHOD_NOT_ALLOWED
    #         )
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)    

    
class CartViewSet(CreateModelMixin,GenericViewSet,RetrieveModelMixin,DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    # queryset = CartItem.objects.all()
