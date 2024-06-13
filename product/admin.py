from django.contrib import admin

from product.models import Process, Product


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
