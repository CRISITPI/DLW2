# Generated by Django 2.0.7 on 2020-02-28 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0031_correctiveaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='axlewheelpressing',
            name='edit_date',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='axlewheelpressing',
            name='inspect_date',
            field=models.CharField(max_length=20, null=True),
        ),
    ]