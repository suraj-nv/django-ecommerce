from django.urls import include, path
from . import views

from rest_framework_nested import routers
# from pprint import pprint
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet, basename='collection')
products_router = routers.NestedDefaultRouter(
    router,
    r'products',
    lookup='product'
)

products_router.register(
    r'reviews',
    views.ReviewViewSet,
    basename='product-reviews'
)
urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
]
# pprint(router.urls)
# urlpatterns = router.urls + review_router.urls
# urlpatterns = [
#     # path('products/', views.ProductList.as_view(), name='product_list'),
#     # path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
#     # path('collections/', views.CollectionList.as_view(), name='collection_list'),
#     # path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
# ]