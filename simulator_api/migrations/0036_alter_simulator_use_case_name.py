# Generated by Django 4.2.5 on 2023-09-13 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0035_alter_simulator_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulator',
            name='use_case_name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]