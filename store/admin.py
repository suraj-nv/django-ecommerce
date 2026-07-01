from django.contrib import admin,messages

from django.contrib.contenttypes.admin import GenericTabularInline

from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from tags.models import TaggedItem

from . import models

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'Inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('<50', 'Medium'),
            ('>=50', 'High'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '<50':
            return queryset.filter(inventory__lt=50)
        if self.value() == '>=50':
            return queryset.filter(inventory__gte=50)

# =====================================
# Product Admin
# =====================================
class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']
    extra=0
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    inlines = [TagInline]
    prepopulated_fields = {'slug': ('title',)}
    list_display = [
        'title',
        'price',
        'inventory',
        'inventory_status',
        'collection_title',
    ]

    list_editable = ['price', 'inventory']
    list_filter = [InventoryFilter, 'collection', 'last_update']
    list_select_related = ['collection']
    search_fields = ['title']
    list_per_page = 20
    
    actions = ['clear_inventory']
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',messages.ERROR
        )
    @admin.display(ordering='inventory', description='Inventory Status')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        elif product.inventory < 50:
            return 'Medium'
        return 'OK'

    @admin.display(ordering='collection__title', description='Collection')
    def collection_title(self, product):
        return product.collection.title


# =====================================
# Collection Admin
# =====================================

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    search_fields = ['title']
    list_per_page = 20

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(product_count=Count('product'))
        )

    @admin.display(ordering='product_count', description='Products')
    def product_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + f'?collection__id__exact={collection.id}'
        )
        return format_html(
            '<a href="{}">{}</a>',
            url,
            collection.product_count
        )


# =====================================
# Customer Admin
# =====================================

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'email',
        'membership',
    ]

    search_fields = [
        'first_name',
        'last_name',
        'email',
    ]

    ordering = [
        'first_name',
        'last_name',
    ]

    list_editable = ['membership']
    list_per_page = 10


# =====================================
# Order Admin
# =====================================
class OrderItemInline(admin.StackedInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra=0
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = [
        'id',
        'placed_at',
        'customer',
    ]

    list_select_related = ['customer']
    inlines = [OrderItemInline]
    list_per_page = 10