# Generated by Django 2.0.7 on 2019-11-08 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0021_auto_20191108_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='axlewheelpressing',
            old_name='axleinspection_status',
            new_name='hhpinspection_status',
        ),
        migrations.RenameField(
            model_name='axlewheelpressing',
            old_name='wheelinspection_status',
            new_name='inspectinspection_status',
        ),
    ]
