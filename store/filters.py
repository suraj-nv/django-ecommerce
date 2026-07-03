from django_filters import rest_framework as filters
from .models import Product, Collection

PRICE_CHOICES = (
    ('0-2000', '₹0 - ₹2000'),
    ('2000-5000', '₹2000 - ₹5000'),
    ('5000-10000', '₹5000 - ₹10000'),
    ('10000+', '₹10000+'),
)

class ProductFilter(filters.FilterSet):
    collection = filters.ModelChoiceFilter(
        queryset=Collection.objects.all()
    )
    price = filters.ChoiceFilter(
        choices=PRICE_CHOICES,
        method='filter_by_price'
    )

    class Meta:
        model = Product
        fields = ['price']

    def filter_by_price(self, queryset, name, value):
        if value == '0-2000':
            return queryset.filter(price__gte=0, price__lte=2000)
        elif value == '2000-5000':
            return queryset.filter(price__gt=2000, price__lte=5000)
        elif value == '5000-10000':
            return queryset.filter(price__gt=5000, price__lte=10000)
        elif value == '10000+':
            return queryset.filter(price__gt=10000)

        return queryset