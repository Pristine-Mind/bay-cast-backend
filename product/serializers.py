from rest_framework import serializers

from django.db import models
from django.utils import timezone

from .models import Product, Process, Station
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
