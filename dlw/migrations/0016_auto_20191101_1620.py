# Generated by Django 2.0.7 on 2019-11-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0015_auto_20191101_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='axlewheelmachining',
            name='inspection_status',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='axlewheelpressing',
            name='inspection_status',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='bogieassembly',
            name='inspection_status',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='pinionpressing',
            name='inspection_status',
            field=models.NullBooleanField(),
        ),
    ]