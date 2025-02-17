# Generated by Django 4.2.14 on 2025-01-06 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0008_delete_castingsnapshot_delete_moldingfloor_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="MoldingFloor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cope_baume",
                    models.FloatField(
                        blank=True,
                        help_text="Baume value for cope.",
                        null=True,
                        verbose_name="Cope Baume",
                    ),
                ),
                (
                    "drag_baume",
                    models.FloatField(
                        blank=True,
                        help_text="Baume value for drag.",
                        null=True,
                        verbose_name="Drag Baume",
                    ),
                ),
                (
                    "core_baume",
                    models.FloatField(
                        blank=True,
                        help_text="Baume value for core.",
                        null=True,
                        verbose_name="Core Baume",
                    ),
                ),
                (
                    "cope_temperature",
                    models.FloatField(
                        blank=True,
                        help_text="Temperature for cope.",
                        null=True,
                        verbose_name="Cope Temperature (°F)",
                    ),
                ),
                (
                    "drag_temperature",
                    models.FloatField(
                        blank=True,
                        help_text="Temperature for drag.",
                        null=True,
                        verbose_name="Drag Temperature (°F)",
                    ),
                ),
                (
                    "core_temperature",
                    models.FloatField(
                        blank=True,
                        help_text="Temperature for core.",
                        null=True,
                        verbose_name="Core Temperature (°F)",
                    ),
                ),
                (
                    "cope_no_of_coatings",
                    models.FloatField(
                        blank=True,
                        help_text="Number of coatings for cope.",
                        null=True,
                        verbose_name="Cope Number of Coatings",
                    ),
                ),
                (
                    "drag_no_of_coatings",
                    models.FloatField(
                        blank=True,
                        help_text="Number of coatings for drag.",
                        null=True,
                        verbose_name="Drag Number of Coatings",
                    ),
                ),
                (
                    "core_no_of_coatings",
                    models.FloatField(
                        blank=True,
                        help_text="Number of coatings for core.",
                        null=True,
                        verbose_name="Core Number of Coatings",
                    ),
                ),
                (
                    "cope_heat_applied",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates if heat was applied for cope.",
                        verbose_name="Cope Heat Applied",
                    ),
                ),
                (
                    "drag_heat_applied",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates if heat was applied for drag.",
                        verbose_name="Drag Heat Applied",
                    ),
                ),
                (
                    "core_heat_applied",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates if heat was applied for core.",
                        verbose_name="Core Heat Applied",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pour",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "mold_close_to_pour_time_days",
                    models.FloatField(blank=True, null=True),
                ),
                ("pour_temperature", models.FloatField(blank=True, null=True)),
                ("pour_time_seconds", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Quality",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("surface_quality_grade", models.IntegerField(blank=True, null=True)),
                ("comments", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="RammingFloor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cope_temperature",
                    models.FloatField(
                        blank=True,
                        help_text="Temperature for cope.",
                        null=True,
                        verbose_name="Cope Temperature (°F)",
                    ),
                ),
                (
                    "drag_temperature",
                    models.FloatField(
                        blank=True,
                        help_text="Temperature for drag.",
                        null=True,
                        verbose_name="Drag Temperature (°F)",
                    ),
                ),
                (
                    "core_temperature",
                    models.FloatField(
                        blank=True,
                        help_text="Temperature for core.",
                        null=True,
                        verbose_name="Core Temperature (°F)",
                    ),
                ),
                (
                    "cope_humidity",
                    models.FloatField(
                        blank=True,
                        help_text="Humidity for cope.",
                        null=True,
                        verbose_name="Cope Humidity (%)",
                    ),
                ),
                (
                    "drag_humidity",
                    models.FloatField(
                        blank=True,
                        help_text="Humidity for drag.",
                        null=True,
                        verbose_name="Drag Humidity (%)",
                    ),
                ),
                (
                    "core_humidity",
                    models.FloatField(
                        blank=True,
                        help_text="Humidity for core.",
                        null=True,
                        verbose_name="Core Humidity (%)",
                    ),
                ),
                (
                    "sand_ph_load",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        help_text="PH level of the sand used.",
                        max_digits=5,
                        null=True,
                        verbose_name="Sand PH (Load)",
                    ),
                ),
                (
                    "sand_temperature_core",
                    models.FloatField(
                        blank=True,
                        help_text="Temperature of the sand used core.",
                        null=True,
                        verbose_name="Sand Temperature Core(°F)",
                    ),
                ),
                (
                    "sand_temperature_cope",
                    models.FloatField(
                        blank=True,
                        help_text="Temperature of the sand used cope.",
                        null=True,
                        verbose_name="Sand Temperature Cope(°F)",
                    ),
                ),
                (
                    "sand_temperature_drag",
                    models.FloatField(
                        blank=True,
                        help_text="Temperature of the sand used drag.",
                        null=True,
                        verbose_name="Sand Temperature Drag(°F)",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Shakeout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("shakeout_time_days", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="StationOne",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "casting_type",
                    models.CharField(
                        blank=True,
                        help_text="Type of casting used in the process.",
                        max_length=100,
                        null=True,
                        verbose_name="Casting Type",
                    ),
                ),
                (
                    "weight_lbs",
                    models.FloatField(
                        help_text="The weight of the casting in pounds.",
                        verbose_name="Weight (lbs)",
                    ),
                ),
                (
                    "materials",
                    models.CharField(
                        help_text="Materials used in the casting process.",
                        max_length=200,
                        verbose_name="Materials",
                    ),
                ),
                (
                    "pattern_type",
                    models.CharField(
                        help_text="Type of pattern used in the process.",
                        max_length=100,
                        verbose_name="Pattern Type",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CastingSnapshot",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "molding_floor",
                    models.OneToOneField(
                        help_text="Molding floor details for cope, drag, and core.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.moldingfloor",
                        verbose_name="Molding Floor",
                    ),
                ),
                (
                    "pour",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.pour",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        help_text="The product this snapshot is associated with.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                        verbose_name="Related Product",
                    ),
                ),
                (
                    "quality",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.quality",
                    ),
                ),
                (
                    "ramming_floor",
                    models.OneToOneField(
                        help_text="Ramming floor details for cope, drag, and core.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.rammingfloor",
                        verbose_name="Ramming Floor",
                    ),
                ),
                (
                    "shakeout",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.shakeout",
                    ),
                ),
                (
                    "station",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.station",
                        verbose_name="Related Station",
                    ),
                ),
                (
                    "station_one",
                    models.OneToOneField(
                        help_text="Station One.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.stationone",
                        verbose_name="StationOne",
                    ),
                ),
            ],
            options={
                "verbose_name": "Casting Snapshot",
                "verbose_name_plural": "Casting Snapshots",
            },
        ),
    ]
