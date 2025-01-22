# Generated by Django 4.2.13 on 2024-07-16 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0003_station_process_station"),
    ]

    operations = [
        migrations.AlterField(
            model_name="process",
            name="stage",
            field=models.CharField(
                blank=True,
                choices=[
                    ("engineering", "Engineering"),
                    ("pattern_shop", "Pattern Shop"),
                    ("ramming_floor", "Ramming Floor"),
                    ("molding_floor", "Molding Floor"),
                    ("closing", "Closing"),
                    ("pouring", "Pouring"),
                    ("shakeout", "Shakeout"),
                    ("cleaning", "Cleaning"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
