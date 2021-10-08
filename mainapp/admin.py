from django.contrib import admin
from mainapp.models import ProductCategory, Product

# Register your models here.
admin.site.register(ProductCategory)
# admin.site.register(Product)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'description', ('price', 'quantity', 'category'))
    readonly_fields = ('description',)
    ordering = ('name', 'price',)
    search_fields = ('name', )




