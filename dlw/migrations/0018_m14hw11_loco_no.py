# Generated by Django 2.0.7 on 2020-01-04 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0017_m14hw11'),
    ]

    operations = [
        migrations.AddField(
            model_name='m14hw11',
            name='loco_no',
            field=models.CharField(blank=True, db_column='LOCO_NO', max_length=10, null=True),
        ),
    ]