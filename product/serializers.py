from rest_framework import serializers

from django.utils import timezone

from .models import (
    Product,
    Process,
    Station,
    ProcessingImages,
    MoldingFloor,
    StationOne,
    Pour,
    Shakeout,
    Quality,
    CastingSnapshot,
    RammingFloor,
)
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

        product_id = validated_data.get("product_id")
        product_name = validated_data.get("product_name")
        validated_data["qr_image"] = generate_qr(product_id, product_name)
        product = super().create(validated_data)

        # create corresponding process as well
        Process.objects.create(product=product, station_id=1, entry_time=timezone.now())
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
        fields = "__all__"

    def get_number_of_products(self, obj):
        return Product.objects.filter(process__station=obj).count()

    def get_products(self, obj):
        queryset = Process.objects.filter(station=obj, is_active=True).select_related(
            "product"
        )

        return [
            {
                "id": process.product.product_id,
                "product_name": process.product.product_name,
                "entry_time": process.entry_time,
                "exit_time": process.exit_time,
                "qr_image": self.context.get("request").build_absolute_uri(
                    process.product.qr_image.url
                ),
            }
            for process in queryset
        ]


class ProductProcessSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    product_name = serializers.CharField()
    entry_time = serializers.DateTimeField()
    exit_time = serializers.DateTimeField()


class StationProductProcessSerializer(serializers.Serializer):
    station_name = serializers.CharField()
    products = ProductProcessSerializer(many=True)


class MoldingFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoldingFloor
        fields = "__all__"


class StationOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationOne
        fields = "__all__"


class PourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pour
        fields = "__all__"


class ShakeoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shakeout
        fields = "__all__"


class QualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quality
        fields = "__all__"


class RammingFloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RammingFloor
        fields = "__all__"


class CastingSnapshotSerializer(serializers.ModelSerializer):
    """
    Serializer for the CastingSnapshot model, with nested station-specific serializers.
    """

    station_one = StationOneSerializer(required=False, allow_null=True)
    ramming_floor = RammingFloorSerializer(required=False, allow_null=True)
    molding_floor = MoldingFloorSerializer(required=False, allow_null=True)
    pour = PourSerializer(required=False, allow_null=True)
    shakeout = ShakeoutSerializer(required=False, allow_null=True)
    quality = QualitySerializer(required=False, allow_null=True)

    class Meta:
        model = CastingSnapshot
        fields = [
            "id",
            "product",
            "station",
            "station_one",
            "ramming_floor",
            "molding_floor",
            "pour",
            "shakeout",
            "quality",
        ]

    def has_significant_value(self, data):
        """
        Returns True if at least one field in the data dict
        is non-empty, non-None, or otherwise 'significant'.
        You can customize this check based on your business rules.
        """
        if not data:
            return False

        for value in data.values():
            if value is None:
                continue

            if isinstance(value, str) and value.strip() == "":
                continue

            return True

        return False

    def create(self, validated_data):
        """
        Custom create method to handle nested writes for station-specific data.
        """
        station_one_data = validated_data.pop("station_one", None)
        molding_floor_data = validated_data.pop("molding_floor", None)
        pour_data = validated_data.pop("pour", None)
        shakeout_data = validated_data.pop("shakeout", None)
        quality_data = validated_data.pop("quality", None)
        ramming_floor_data = validated_data.pop("ramming_floor", None)

        # Create the CastingSnapshot first
        snapshot = CastingSnapshot.objects.create(**validated_data)

        # If station_one data was provided, create a StationOne record and link it
        if self.has_significant_value(station_one_data):
            station_one_obj = StationOne.objects.create(**station_one_data)
            snapshot.station_one = station_one_obj
            snapshot.save()

        # If molding_floor data was provided, create a MoldingFloor record and link it
        if self.has_significant_value(molding_floor_data):
            molding_floor_obj = MoldingFloor.objects.create(**molding_floor_data)
            snapshot.molding_floor = molding_floor_obj
            snapshot.save()

        if self.has_significant_value(ramming_floor_data):
            ramming_floor_obj = RammingFloor.objects.create(**ramming_floor_data)
            snapshot.ramming_floor = ramming_floor_obj
            snapshot.save()

        # If pour data was provided
        if self.has_significant_value(pour_data):
            pour_obj = Pour.objects.create(**pour_data)
            snapshot.pour = pour_obj
            snapshot.save()

        # If shakeout data was provided
        if self.has_significant_value(shakeout_data):
            shakeout_obj = Shakeout.objects.create(**shakeout_data)
            snapshot.shakeout = shakeout_obj
            snapshot.save()

        # If quality data was provided
        if self.has_significant_value(quality_data):
            quality_obj = Quality.objects.create(**quality_data)
            snapshot.quality = quality_obj
            snapshot.save()

        return snapshot

    def update(self, instance, validated_data):
        """
        Custom update method for nested writes.
        """
        station_one_data = validated_data.pop("station_one", None)
        molding_floor_data = validated_data.pop("molding_floor", None)
        pour_data = validated_data.pop("pour", None)
        shakeout_data = validated_data.pop("shakeout", None)
        quality_data = validated_data.pop("quality", None)
        ramming_floor_data = validated_data.pop("ramming_floor", None)

        # Update the CastingSnapshot's own fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create StationOne
        if station_one_data is not None:
            if instance.station_one:
                # Update existing StationOne
                for attr, value in station_one_data.items():
                    setattr(instance.station_one, attr, value)
                instance.station_one.save()
            else:
                station_one_obj = StationOne.objects.create(**station_one_data)
                instance.station_one = station_one_obj
                instance.save()

        # Update or create MoldingFloor
        if molding_floor_data is not None:
            if instance.molding_floor:
                for attr, value in molding_floor_data.items():
                    setattr(instance.molding_floor, attr, value)
                instance.molding_floor.save()
            else:
                molding_floor_obj = MoldingFloor.objects.create(**molding_floor_data)
                instance.molding_floor = molding_floor_obj
                instance.save()

        # Update or create MoldingFloor
        if ramming_floor_data is not None:
            if instance.ramming_floor:
                for attr, value in ramming_floor_data.items():
                    setattr(instance.ramming_floor, attr, value)
                instance.ramming_floor.save()
            else:
                ramming_floor_obj = RammingFloor.objects.create(**ramming_floor_data)
                instance.ramming_floor = ramming_floor_obj
                instance.save()

        # Update or create Pour
        if pour_data is not None:
            if instance.pour:
                for attr, value in pour_data.items():
                    setattr(instance.pour, attr, value)
                instance.pour.save()
            else:
                pour_obj = Pour.objects.create(**pour_data)
                instance.pour = pour_obj
                instance.save()

        # Update or create Shakeout
        if shakeout_data is not None:
            if instance.shakeout:
                for attr, value in shakeout_data.items():
                    setattr(instance.shakeout, attr, value)
                instance.shakeout.save()
            else:
                shakeout_obj = Shakeout.objects.create(**shakeout_data)
                instance.shakeout = shakeout_obj
                instance.save()

        # Update or create Quality
        if quality_data is not None:
            if instance.quality:
                for attr, value in quality_data.items():
                    setattr(instance.quality, attr, value)
                instance.quality.save()
            else:
                quality_obj = Quality.objects.create(**quality_data)
                instance.quality = quality_obj
                instance.save()

        return instance
