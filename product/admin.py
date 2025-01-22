from django.contrib import admin

from product.models import (
    Process,
    Product,
    Station,
    ProcessingImages,
)


class ProcessAdminInline(admin.TabularInline):
    model = Process
    fields = (
        "id",
        "product",
        "entry_time",
        "exit_time",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    inlines = [ProcessAdminInline]
