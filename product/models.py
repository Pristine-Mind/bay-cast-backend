from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    product_id = models.CharField(max_length=50, primary_key=True)
    product_name = models.CharField(max_length=100)
    qr_image = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def __str__(self):
        return f"ID: {self.product_id}, Name: {self.product_name}"


class Process(models.Model):
    """
    Model to track the processes of a manufacturing system.

    Attributes:
        product (ForeignKey): A foreign key to the Product model, representing the product associated with this process.
        process_number (IntegerField): An integer field representing the number of the process.
        stage (CharField): A choice field representing different stages in the process.
        entry_time (DateTimeField): The time when the product enters this process.
        exit_time (DateTimeField): The time when the product exits this process.
        temperature (DecimalField): Represents the temperature during the process.
        humidity (DecimalField): Represents the humidity during the process.
        baume (DecimalField): Represents the baume level during the process.
        pouring_temperature (DecimalField): Represents the pouring temperature during the process.
        weights (FloatField): Represents the weight associated with the process.
        pictures (ManyToManyField): Allows multiple images to be associated with a single process.
    """

    class ProcessStep(models.TextChoices):
        """
        Choices for different stages in the manufacturing process.
        """

        ENGINEERING = 'engineering', _('Engineering')
        PATTERN_SHOP = 'pattern_shop', _('Pattern Shop')
        RAMMING_FLOOR = 'ramming_floor', _('Ramming Floor')
        MOLDING_FLOOR = 'molding_floor', _('Molding Floor')
        CLOSING = 'closing', _('Closing')
        POURING = 'pouring', _('Pouring')
        SHAKEOUT = 'shakeout', _('Shakeout')
        CLEANING = 'cleaning', _('Cleaning')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    process_number = models.IntegerField(default=1)
    stage = models.CharField(max_length=20, choices=ProcessStep.choices)
    entry_time = models.DateTimeField(
        verbose_name=_('Time of product entry in process')
    )
    exit_time = models.DateTimeField(
        verbose_name=_('Time of product exit from process')
    )
    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    humidity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    baume = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    pouring_temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    weights = models.FloatField(
        null=True,
        blank=True,
    )
    pictures = models.ManyToManyField(
        "ProcessingImages",
        blank=True
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

    picture = models.ImageField(
        upload_to='process_pictures/',
        null=True,
        blank=True
    )
