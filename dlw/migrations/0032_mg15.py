# Generated by Django 2.0.7 on 2019-11-15 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0031_m14m4new1_m2docnew1_m5docnew1'),
    ]

    operations = [
        migrations.CreateModel(
            name='MG15',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_sec', models.CharField(blank=True, db_column='SHOP_SEC', max_length=4, null=True)),
                ('staff_no', models.CharField(blank=True, db_column='STAFF_NO', max_length=8, null=True)),
                ('name', models.CharField(blank=True, db_column='NAME', max_length=25, null=True)),
                ('desgn', models.CharField(blank=True, db_column='DESIGNATION', max_length=20, null=True)),
                ('cat', models.CharField(blank=True, db_column='CATEGORY', max_length=10, null=True)),
                ('emp_type', models.CharField(blank=True, db_column='EMPLOYEE_TYPE', max_length=15, null=True)),
                ('remarks', models.CharField(blank=True, db_column='REMARKS', max_length=50, null=True)),
                ('h1a', models.CharField(blank=True, db_column='FIRST HALF ABSENT', max_length=15, null=True)),
                ('h2a', models.CharField(blank=True, db_column='SECOND HALF ABSENT', max_length=15, null=True)),
                ('causeofab', models.CharField(blank=True, db_column='CAUSE OF ABSENT', max_length=50, null=True)),
                ('ticket_no', models.CharField(blank=True, db_column='TICKET_NUMBER', max_length=20, null=True)),
                ('date', models.CharField(blank=True, db_column='DATE', default='0', max_length=10, null=True)),
            ],
            options={
                'db_table': 'MG15',
            },
        ),
    ]
