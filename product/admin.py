from django.contrib import admin

from product.models import (
    Process,
    Product,
    Station,
    CastingSnapshot,
    RammingFloor,
    MoldingFloor,
    ProcessingImages,
)


class ProcessAdminInline(admin.TabularInline):
    model = Process
    fields = (
        'id',
        'product',
        'entry_time',
        'exit_time',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    inlines = [ProcessAdminInline]


@admin.register(RammingFloor)
class RammingFloorAdmin(admin.ModelAdmin):
    """
    Admin interface for the RammingFloor model.
    """
    list_display = (
        'id', 'cope_temperature', 'drag_temperature', 'core_temperature',
        'cope_humidity', 'drag_humidity', 'core_humidity'
    )
    search_fields = ('id',)
    list_filter = ('cope_humidity', 'drag_humidity', 'core_humidity')


@admin.register(MoldingFloor)
class MoldingFloorAdmin(admin.ModelAdmin):
    """
    Admin interface for the MoldingFloor model.
    """
    list_display = (
        'id', 'drag_baume', 'core_baume',
        'cope_temperature', 'drag_temperature', 'core_temperature',
        'cope_no_of_coatings', 'drag_no_of_coatings', 'core_no_of_coatings',
        'cope_heat_applied', 'drag_heat_applied', 'core_heat_applied'
    )
    search_fields = ('id',)
    list_filter = ('cope_heat_applied', 'drag_heat_applied', 'core_heat_applied')


class RammingFloorInline(admin.StackedInline):
    """
    Inline admin interface for RammingFloor.
    """
    model = RammingFloor
    extra = 0


class MoldingFloorInline(admin.StackedInline):
    """
    Inline admin interface for MoldingFloor.
    """
    model = MoldingFloor
    extra = 0


@admin.register(CastingSnapshot)
class CastingSnapshotAdmin(admin.ModelAdmin):
    """
    Admin interface for the CastingSnapshot model.
    """
    list_display = (
        'id', 'process', 'casting_type', 'weight_lbs', 'materials',
        'pattern_type', 'sand_ph_load',
        'mold_close_to_pour_time_days', 'pour_temperature', 'pour_time_seconds',
        'shakeout_time_days', 'surface_quality_grade'
    )
    search_fields = ('process__id', 'materials', 'pattern_type')
    list_filter = ('casting_type', 'surface_quality_grade', 'process')
    filter_horizontal = ('pictures',)


@admin.register(ProcessingImages)
class ProcessingImagesAdmin(admin.ModelAdmin):
    """
    Admin interface for the ProcessingImages model.
    """
    list_display = ('id', 'picture',)
