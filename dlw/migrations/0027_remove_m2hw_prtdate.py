# Generated by Django 2.0.7 on 2019-12-14 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0026_auto_20191214_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='m2hw',
            name='prtDate',
        ),
    ]