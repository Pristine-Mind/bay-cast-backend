from rest_framework import serializers

from django.utils import timezone

from .models import Product, Process, Station, CastingSnapshot, RammingFloor, MoldingFloor, ProcessingImages
from .utils import generate_qr


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    This serializer automatically generates a QR image for the product
    based on its ID and name before creating it.

    Attributes:
        model: The Product model class.
        fields: Specifies that all fields of the model should be included in serialization.

    Methods:
        create: Overrides the default create method to generate a QR image for the product
                before creating it.
    """

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        """
        Create method override to generate a QR image for the product before creating it.

        Args:
            validated_data (dict): Validated data for the product.

        Returns:
            Product: The newly created product instance.
        """

        product_id = validated_data.get('product_id')
        product_name = validated_data.get('product_name')
        validated_data['qr_image'] = generate_qr(product_id, product_name)
        product = super().create(validated_data)

        # create corresponding process as well
        Process.objects.create(
            product=product,
            station_id=1,
            entry_time=timezone.now()
        )
        return product


class ProcessSerializer(serializers.ModelSerializer):
    """
    Serializer for the Process model.

    This serializer serializes all fields of the Process model.

    Attributes:
        model: The Process model class.
        fields: Specifies that all fields of the model should be included in serialization.
    """

    class Meta:
        model = Process
        fields = "__all__"


class StationSerialzier(serializers.ModelSerializer):
    number_of_products = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Station
        fields = '__all__'

    def get_number_of_products(self, obj):
        return Product.objects.filter(
            process__station=obj
        ).count()

    def get_products(self, obj):
        queryset = Process.objects.filter(station=obj).select_related('product')

        return [
            {
                "id": process.product.product_id,
                "product_name": process.product.product_name,
                "entry_time": process.entry_time,
                "exit_time": process.exit_time,
                "qr_image": self.context.get('request').build_absolute_uri(process.product.qr_image.url),
            } for process in queryset
        ]


class ProductProcessSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    product_name = serializers.CharField()
    entry_time = serializers.DateTimeField()
    exit_time = serializers.DateTimeField()


class StationProductProcessSerializer(serializers.Serializer):
    station_name = serializers.CharField()
    products = ProductProcessSerializer(many=True)


class RammingFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RammingFloor
        fields = '__all__'


class MoldingFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoldingFloor
        fields = '__all__'


class ProcessingImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingImages
        fields = ['id', 'image', 'description']


class CastingSnapshotSerializer(serializers.ModelSerializer):
    ramming_floor = RammingFloorSerializer()
    molding_floor = MoldingFloorSerializer()
    pictures = ProcessingImagesSerializer(many=True, read_only=True)
    pictures_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=ProcessingImages.objects.all(), source='pictures'
    )

    class Meta:
        model = CastingSnapshot
        fields = [
            'id', 'process', 'control_no', 'casting_type', 'weight_lbs', 'materials', 'pattern_type',
            'sand_ph_load', 'sand_temperature',
            'ramming_floor', 'molding_floor',
            'mold_close_to_pour_time_days', 'pour_temperature', 'pour_time_seconds',
            'shakeout_time_days', 'surface_quality_grade', 'comments', 'pictures', 'pictures_ids'
        ]

    def create(self, validated_data):
        ramming_floor_data = validated_data.pop('ramming_floor')
        molding_floor_data = validated_data.pop('molding_floor')
        ramming_floor = RammingFloor.objects.create(**ramming_floor_data)
        molding_floor = MoldingFloor.objects.create(**molding_floor_data)
        casting_snapshot = CastingSnapshot.objects.create(
            ramming_floor=ramming_floor, molding_floor=molding_floor, **validated_data
        )
        return casting_snapshot

    def update(self, instance, validated_data):
        ramming_floor_data = validated_data.pop('ramming_floor', None)
        molding_floor_data = validated_data.pop('molding_floor', None)

        if ramming_floor_data:
            for attr, value in ramming_floor_data.items():
                setattr(instance.ramming_floor, attr, value)
            instance.ramming_floor.save()

        if molding_floor_data:
            for attr, value in molding_floor_data.items():
                setattr(instance.molding_floor, attr, value)
            instance.molding_floor.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
