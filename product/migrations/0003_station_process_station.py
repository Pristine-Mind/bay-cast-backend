# Generated by Django 4.2.13 on 2024-07-11 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_processingimages_process"),
    ]

    operations = [
        migrations.CreateModel(
            name="Station",
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
                ("name", models.CharField(verbose_name="Name of station")),
            ],
        ),
        migrations.AddField(
            model_name="process",
            name="station",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="product.station",
            ),
            preserve_default=False,
        ),
    ]
