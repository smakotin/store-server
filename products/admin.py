from django.contrib import admin

from products.models import Cart, Product, ProductCategory

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category')
    fields = ('image', 'name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category')
    readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('-name',)
    list_editable = ('price', 'quantity', 'category')
    list_display_links = ('id', 'name')


class CartAdmin(admin.TabularInline):
    model = Cart
    extra = 0
