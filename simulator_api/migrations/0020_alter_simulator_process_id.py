# Generated by Django 4.2.5 on 2023-09-10 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0019_remove_configuration_seasonality_components_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulator',
            name='process_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
