# Generated by Django 2.0.7 on 2019-11-20 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0002_auto_20191120_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='ms_tools_calibration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calibration_code', models.CharField(blank=True, max_length=10)),
                ('maintenance_group', models.CharField(blank=True, max_length=10)),
                ('shop_code', models.CharField(blank=True, max_length=10)),
                ('instrument_number', models.CharField(blank=True, max_length=20)),
                ('calibration_date', models.CharField(blank=True, max_length=10)),
                ('accuracy_calibrated', models.CharField(blank=True, max_length=50, null=True)),
                ('calibrating_person', models.CharField(blank=True, max_length=50, null=True)),
                ('verified_by', models.CharField(blank=True, max_length=50, null=True)),
                ('remarks', models.CharField(blank=True, max_length=200, null=True)),
                ('ambient_temp', models.CharField(blank=True, max_length=10, null=True)),
                ('plus_error', models.FloatField(blank=True, max_length=10, null=True)),
                ('minus_error', models.FloatField(blank=True, max_length=10, null=True)),
                ('standrad_reading', models.CharField(blank=True, max_length=50, null=True)),
                ('receipt_code', models.FloatField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ms_tools_Frequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Frequency', models.CharField(blank=True, max_length=50)),
                ('FrequencyCode', models.CharField(blank=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ms_tools_group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(blank=True, max_length=50)),
                ('maintenance_group', models.CharField(blank=True, max_length=20, null=True)),
                ('range', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_of_measure', models.CharField(blank=True, max_length=50, null=True)),
                ('accuracy_criteria', models.CharField(blank=True, max_length=50, null=True)),
                ('calibration_frequency', models.CharField(blank=True, max_length=50, null=True)),
                ('calibration_link', models.CharField(blank=True, max_length=50, null=True)),
                ('process_tolerance', models.CharField(blank=True, max_length=50, null=True)),
                ('work_instruction_number', models.CharField(blank=True, max_length=50, null=True)),
                ('plus_error', models.CharField(blank=True, max_length=50, null=True)),
                ('minus_error', models.CharField(blank=True, max_length=50, null=True)),
                ('calibration_prodedure', models.CharField(blank=True, max_length=100, null=True)),
                ('type_ins', models.CharField(blank=True, max_length=50, null=True)),
                ('change_date', models.CharField(blank=True, max_length=50, null=True)),
                ('user_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ms_tools_issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance_group', models.CharField(blank=True, max_length=20)),
                ('instrument_number', models.CharField(blank=True, max_length=50)),
                ('shop_code', models.CharField(blank=True, max_length=50)),
                ('issued_date', models.CharField(blank=True, max_length=50, null=True)),
                ('issued_to', models.CharField(blank=True, max_length=50, null=True)),
                ('issued_by', models.CharField(blank=True, max_length=50, null=True)),
                ('receipt_code', models.CharField(blank=True, max_length=50, null=True)),
                ('issue_code', models.CharField(blank=True, max_length=50)),
                ('CalibrationDueDate', models.CharField(blank=True, max_length=50, null=True)),
                ('user_id', models.CharField(blank=True, max_length=50, null=True)),
                ('CalibrationFrequency', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ms_tools_master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history_card_number', models.CharField(blank=True, max_length=50)),
                ('shop_code', models.CharField(blank=True, max_length=50)),
                ('maintenance_group', models.CharField(blank=True, max_length=50)),
                ('instrument_number', models.CharField(blank=True, max_length=50, null=True)),
                ('make', models.CharField(blank=True, max_length=50, null=True)),
                ('model', models.CharField(blank=True, max_length=50, null=True)),
                ('standard', models.CharField(blank=True, max_length=50, null=True)),
                ('tool_code', models.CharField(blank=True, max_length=50, null=True)),
                ('group_name', models.CharField(blank=True, max_length=50, null=True)),
                ('range', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_of_measure', models.CharField(blank=True, max_length=50, null=True)),
                ('accuracy_criteria', models.CharField(blank=True, max_length=50, null=True)),
                ('calibration_frequency', models.CharField(blank=True, max_length=50, null=True)),
                ('calibration_link', models.CharField(blank=True, max_length=50, null=True)),
                ('process_tolerance', models.CharField(blank=True, max_length=50, null=True)),
                ('work_instruction_number', models.CharField(blank=True, max_length=50, null=True)),
                ('plus_error', models.FloatField(blank=True, max_length=50, null=True)),
                ('minus_error', models.FloatField(blank=True, max_length=50, null=True)),
                ('calibration_due_date', models.CharField(blank=True, max_length=50, null=True)),
                ('calibration_prodedure', models.CharField(blank=True, max_length=1000, null=True)),
                ('introduced_date', models.CharField(blank=True, max_length=50, null=True)),
                ('user_id', models.CharField(blank=True, max_length=50, null=True)),
                ('employee', models.CharField(blank=True, max_length=50, null=True)),
                ('remarks', models.CharField(blank=True, max_length=50, null=True)),
                ('last_iss_date', models.CharField(blank=True, max_length=50, null=True)),
                ('last_cal_date', models.CharField(blank=True, max_length=50, null=True)),
                ('last_rec_date', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ms_tools_receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_code', models.CharField(blank=True, max_length=50)),
                ('instrument_number', models.CharField(blank=True, max_length=50)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('maintenance_group', models.CharField(blank=True, max_length=20)),
                ('shop_code', models.CharField(blank=True, max_length=50)),
                ('receipt_date', models.CharField(blank=True, max_length=50, null=True)),
                ('recived_by', models.CharField(blank=True, max_length=50, null=True)),
                ('plus_error', models.FloatField(blank=True, max_length=10)),
                ('minus_error', models.FloatField(blank=True, max_length=10)),
                ('accuracy_received', models.FloatField(blank=True, max_length=10, null=True)),
                ('accuracy_calibrated', models.FloatField(blank=True, max_length=10, null=True)),
                ('calibration_date', models.CharField(blank=True, max_length=50, null=True)),
                ('remarks', models.CharField(blank=True, max_length=50, null=True)),
                ('discripency', models.CharField(blank=True, max_length=50, null=True)),
                ('change_date', models.CharField(blank=True, max_length=50, null=True)),
                ('user_id', models.CharField(blank=True, max_length=50, null=True)),
                ('supervisor', models.CharField(blank=True, max_length=50, null=True)),
                ('rec_chd_by', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ms_tools_shopchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=6, null=True)),
                ('instrument_number', models.CharField(blank=True, max_length=20, null=True)),
                ('shop_code', models.CharField(blank=True, max_length=2, null=True)),
                ('surrendered_date', models.CharField(blank=True, max_length=10, null=True)),
                ('sl_no', models.CharField(blank=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ms_tools_shops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(blank=True, max_length=50)),
                ('shop_code', models.CharField(blank=True, max_length=10)),
            ],
        ),
    ]
