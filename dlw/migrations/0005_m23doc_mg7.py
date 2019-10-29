# Generated by Django 2.0.7 on 2019-10-26 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0004_auto_20191026_0721'),
    ]

    operations = [
        migrations.CreateModel(
            name='m23doc',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.CharField(db_column=' DATE', max_length=50)),
                ('shop_no', models.CharField(db_column=' SHOP_NO', max_length=15)),
                ('emp_no', models.CharField(db_column=' EMP_NO', max_length=15)),
                ('emp_name', models.CharField(db_column=' EMP_NAME', max_length=25)),
                ('ga_time', models.CharField(db_column='GA_TIME', max_length=50)),
                ('purpose', models.CharField(db_column=' PURPOSE', max_length=80)),
                ('from_time', models.CharField(db_column='FROM_TIME', max_length=20)),
                ('to_time', models.CharField(db_column='TO_TIME', max_length=20)),
            ],
            options={
                'db_table': 'M23new',
            },
        ),
        migrations.CreateModel(
            name='MG7',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fromshop', models.CharField(blank=True, db_column='FROMSHOP', max_length=4, null=True)),
                ('toshop', models.CharField(blank=True, db_column='TOSHOP', max_length=4, null=True)),
                ('date', models.CharField(blank=True, db_column='DATE', default=0, max_length=10, null=True)),
                ('wo_no', models.CharField(blank=True, db_column='WORK_DRDER', max_length=9, null=True)),
                ('part_no', models.CharField(blank=True, db_column='PART_NO', max_length=10, null=True)),
                ('des', models.CharField(blank=True, db_column='PART_DESCRIPTION', max_length=30, null=True)),
                ('qty_ord', models.CharField(blank=True, db_column='QTY_ORDERED', max_length=8, null=True)),
                ('qty_req', models.CharField(blank=True, db_column='QTY_REQUESTED', max_length=8, null=True)),
                ('qty_rej', models.CharField(blank=True, db_column='QTY_REJECTED', max_length=8, null=True)),
                ('m13_no', models.CharField(blank=True, db_column='M13_NO', max_length=10, null=True)),
                ('m5glsn', models.CharField(blank=True, db_column='M5GLSN', max_length=10, null=True)),
                ('reason', models.CharField(blank=True, db_column='QTY_REASON', max_length=25, null=True)),
            ],
            options={
                'db_table': 'MG7',
            },
        ),
    ]
