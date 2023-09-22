# Generated by Django 4.2.5 on 2023-09-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0036_alter_simulator_use_case_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='missing_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='outlier_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='trend_coefficients',
            field=models.JSONField(default=0),
        ),
    ]