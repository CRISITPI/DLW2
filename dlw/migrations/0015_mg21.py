# Generated by Django 2.0.7 on 2019-11-27 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0014_m3a_mgr_mgrreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='MG21',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_sec', models.CharField(blank=True, db_column='SHOP_SEC', max_length=4, null=True)),
                ('staff_no', models.CharField(blank=True, db_column='STAFF_NO', max_length=8, null=True)),
                ('date', models.CharField(db_column=' DATE', max_length=50)),
                ('name', models.CharField(blank=True, db_column='NAME', max_length=25, null=True)),
                ('to_the', models.CharField(db_column=' TO_THE', max_length=25)),
                ('rep_no', models.CharField(db_column='REP_NO', max_length=15)),
                ('acc_date', models.CharField(blank=True, db_column='ACCCIDENT_DATE', default='0', max_length=10, null=True)),
                ('super_in', models.CharField(blank=True, db_column='SUPER_INTENDENT', max_length=35)),
                ('last_modified', models.CharField(db_column='LAST_MODIFIED', max_length=15)),
                ('login_id', models.CharField(db_column='LOGIN_ID', max_length=15)),
            ],
            options={
                'db_table': 'MG21',
            },
        ),
    ]