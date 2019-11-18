# Generated by Django 2.0.7 on 2019-11-18 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dlw', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='m9',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_sec', models.CharField(blank=True, max_length=4, null=True)),
                ('date', models.CharField(blank=True, max_length=20, null=True)),
                ('wo_no', models.CharField(blank=True, max_length=7, null=True)),
                ('part_no', models.CharField(blank=True, max_length=8, null=True)),
                ('aff_opn', models.CharField(blank=True, max_length=10, null=True)),
                ('on_off', models.CharField(blank=True, max_length=4, null=True)),
                ('cat', models.CharField(blank=True, max_length=2, null=True)),
                ('mw_no', models.CharField(blank=True, max_length=8, null=True)),
                ('mg9_no', models.CharField(blank=True, max_length=8, null=True)),
                ('empno', models.CharField(max_length=20, null=True)),
                ('sus_jbno', models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True)),
                ('res_jno', models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True)),
                ('idle_time_man_mac', models.CharField(blank=True, max_length=7, null=True)),
                ('empname', models.CharField(max_length=50, null=True)),
                ('prev_empno', models.CharField(max_length=20, null=True)),
                ('remark', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='axlewheelmachining',
            name='bo_qty',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='axlewheelmachining',
            name='dispatch_date',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='axlewheelmachining',
            name='pt_no',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='axlewheelpressing',
            name='bo_qty',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='axlewheelpressing',
            name='dispatch_date',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='axlewheelpressing',
            name='pt_no',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='bogieassembly',
            name='bo_qty',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='bogieassembly',
            name='dispatch_date',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='bogieassembly',
            name='pt_no',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='machiningairbox',
            name='bo_qty',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='machiningairbox',
            name='dispatch_date',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='machiningairbox',
            name='pt_no',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='miscellsection',
            name='bo_qty',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='miscellsection',
            name='dispatch_date',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='miscellsection',
            name='pt_no',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
