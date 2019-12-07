# Generated by Django 2.0.7 on 2019-12-06 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0018_rates_staff_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='logbook_record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_w_no', models.CharField(blank=True, max_length=10, null=True)),
                ('job_booked', models.CharField(blank=True, max_length=10, null=True)),
                ('staff_no', models.CharField(blank=True, max_length=10, null=True)),
                ('attandance', models.CharField(blank=True, max_length=10, null=True)),
                ('out_turn', models.CharField(blank=True, max_length=10, null=True)),
                ('remarks', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]
