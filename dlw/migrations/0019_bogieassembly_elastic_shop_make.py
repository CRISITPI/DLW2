# Generated by Django 2.0.7 on 2019-11-07 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0018_mg20'),
    ]

    operations = [
        migrations.AddField(
            model_name='bogieassembly',
            name='elastic_shop_make',
            field=models.CharField(max_length=30, null=True),
        ),
    ]