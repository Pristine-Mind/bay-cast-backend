from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    product_id = models.CharField(max_length=50, primary_key=True)
    product_name = models.CharField(max_length=100)
    qr_image = models.ImageField(upload_to="qr_codes/", null=True, blank=True)

    def __str__(self):
        return f"ID: {self.product_id}, Name: {self.product_name}"


class Station(models.Model):
    name = models.CharField(verbose_name=_("Name of station"))

    def __str__(self):
        return self.name


class Process(models.Model):
    """
    Model to track the processes of a manufacturing system.

    Attributes:
        product (ForeignKey): A foreign key to the Product model, representing the product associated with this process.
        process_number (IntegerField): An integer field representing the number of the process.
        stage (CharField): A choice field representing different stages in the process.
        entry_time (DateTimeField): The time when the product enters this process.
        exit_time (DateTimeField): The time when the product exits this process.
    """

    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    process_number = models.IntegerField(default=1)
    entry_time = models.DateTimeField(
        verbose_name=_("Time of product entry in process"),
        null=True,
        blank=True,
    )
    exit_time = models.DateTimeField(
        verbose_name=_("Time of product exit from process"),
        null=True,
        blank=True,
    )

    def __str__(self):
        """
        String representation of the Process model.
        """
        return f"Process {self.process_number} for {self.product}"


class ProcessingImages(models.Model):
    """
    Model to store images associated with manufacturing processes.

    Attributes:
        picture (ImageField): Represents an image associated with the process.
    """

    picture = models.ImageField(upload_to="process_pictures/", null=True, blank=True)


class RammingFloor(models.Model):
    """

    Ramming floor values for cope, drag, and core.

    """

    cope_temperature = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Cope Temperature (°F)",
        help_text="Temperature for cope.",
    )

    drag_temperature = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Drag Temperature (°F)",
        help_text="Temperature for drag.",
    )

    core_temperature = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Core Temperature (°F)",
        help_text="Temperature for core.",
    )

    cope_humidity = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Cope Humidity (%)",
        help_text="Humidity for cope.",
    )

    drag_humidity = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Drag Humidity (%)",
        help_text="Humidity for drag.",
    )

    core_humidity = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Core Humidity (%)",
        help_text="Humidity for core.",
    )

    sand_ph_load = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Sand PH (Load)",
        help_text="PH level of the sand used.",
    )

    sand_temperature_core = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Sand Temperature Core(°F)",
        help_text="Temperature of the sand used core.",
    )

    sand_temperature_cope = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Sand Temperature Cope(°F)",
        help_text="Temperature of the sand used cope.",
    )

    sand_temperature_drag = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Sand Temperature Drag(°F)",
        help_text="Temperature of the sand used drag.",
    )

    def __str__(self):

        return f"Ramming Floor - Cope: {self.cope_temperature}, Drag: {self.drag_temperature}, Core: {self.core_temperature}"


class MoldingFloor(models.Model):
    """

    Molding floor values for cope, drag, and core.

    """

    cope_baume = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Cope Baume",
        help_text="Baume value for cope.",
    )

    drag_baume = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Drag Baume",
        help_text="Baume value for drag.",
    )

    core_baume = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Core Baume",
        help_text="Baume value for core.",
    )

    cope_temperature = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Cope Temperature (°F)",
        help_text="Temperature for cope.",
    )

    drag_temperature = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Drag Temperature (°F)",
        help_text="Temperature for drag.",
    )

    core_temperature = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Core Temperature (°F)",
        help_text="Temperature for core.",
    )

    cope_no_of_coatings = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Cope Number of Coatings",
        help_text="Number of coatings for cope.",
    )

    drag_no_of_coatings = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Drag Number of Coatings",
        help_text="Number of coatings for drag.",
    )

    core_no_of_coatings = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Core Number of Coatings",
        help_text="Number of coatings for core.",
    )

    cope_heat_applied = models.BooleanField(
        null=True, blank=True,
        verbose_name="Cope Heat Applied",
        help_text="Indicates if heat was applied for cope.",
    )

    drag_heat_applied = models.BooleanField(
        null=True, blank=True,
        verbose_name="Drag Heat Applied",
        help_text="Indicates if heat was applied for drag.",
    )

    core_heat_applied = models.BooleanField(
        null=True, blank=True,
        verbose_name="Core Heat Applied",
        help_text="Indicates if heat was applied for core.",
    )

    def __str__(self):

        return f"Molding Floor - Cope: {self.cope_baume}, Drag: {self.drag_baume}, Core: {self.core_baume}"


class StationOne(models.Model):

    casting_type = models.CharField(
        max_length=100,
        verbose_name="Casting Type",
        help_text="Type of casting used in the process.",
        null=True,
        blank=True,
    )

    weight_lbs = models.FloatField(
        verbose_name="Weight (lbs)", help_text="The weight of the casting in pounds."
    )

    materials = models.CharField(
        max_length=200,
        verbose_name="Materials",
        help_text="Materials used in the casting process.",
    )

    pattern_type = models.CharField(
        max_length=100,
        verbose_name="Pattern Type",
        help_text="Type of pattern used in the process.",
    )


class Pour(models.Model):

    mold_close_to_pour_time_days = models.FloatField(null=True, blank=True)

    pour_temperature = models.FloatField(null=True, blank=True)

    pour_time_seconds = models.FloatField(null=True, blank=True)

    def __str__(self):

        return f"Pour - Temp: {self.pour_temperature}, Time: {self.pour_time_seconds}"


class Shakeout(models.Model):

    shakeout_time_days = models.FloatField(null=True, blank=True)

    def __str__(self):

        return f"Shakeout - Time (Days): {self.shakeout_time_days}"


class Quality(models.Model):

    surface_quality_grade = models.IntegerField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)


class CastingSnapshot(models.Model):
    """

    A snapshot of the casting process that stores detailed measurements and quality assessments

    for a specific casting instance.

    """

    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        verbose_name="Related Product",
        help_text="The product this snapshot is associated with.",
    )

    station = models.ForeignKey(
        "Station", on_delete=models.CASCADE, verbose_name="Related Station"
    )

    station_one = models.OneToOneField(
        StationOne,
        on_delete=models.CASCADE,
        verbose_name="StationOne",
        help_text="Station One.",
        null=True,
        blank=True,
    )

    ramming_floor = models.OneToOneField(
        RammingFloor,
        on_delete=models.CASCADE,
        verbose_name="Ramming Floor",
        help_text="Ramming floor details for cope, drag, and core.",
        null=True,
        blank=True,
    )

    molding_floor = models.OneToOneField(
        MoldingFloor,
        on_delete=models.CASCADE,
        verbose_name="Molding Floor",
        help_text="Molding floor details for cope, drag, and core.",
        null=True,
        blank=True,
    )

    pour = models.OneToOneField(Pour, on_delete=models.CASCADE, null=True, blank=True)

    shakeout = models.OneToOneField(
        Shakeout, on_delete=models.CASCADE, null=True, blank=True
    )

    quality = models.OneToOneField(
        Quality, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):

        return f"Casting Snapshot {self.control_no}"

    class Meta:

        verbose_name = "Casting Snapshot"

        verbose_name_plural = "Casting Snapshots"
