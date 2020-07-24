from django.db import models

class MG47_table1(models.Model):
    num=models.CharField(db_column='Sr.No.',max_length=50,primary_key=True)
    shop=models.CharField(db_column='Shop',max_length=50, null=True) 
    to_sse=models.CharField(db_column='ToSSE', max_length=50, null=True)  # Field name made lowercase.
    date=models.CharField(db_column='Date',max_length=50,null=True)
    allocable_to=models.CharField(db_column='allocable_to', max_length=50, null=True) 
    issued_on=models.CharField(db_column='Issued_on',max_length=20,null=True)
    empno=models.CharField(db_column='EmployeeID', max_length=50, null=True)  # Field name made lowercase.
    from_sse=models.CharField(db_column='FromSSE', max_length=50, null=True)  # Field name made lowercase.
    empname=models.CharField(db_column='Empname',max_length=100,null=True)

    class Meta:
        db_table = 'MG47_table1'

class MG47_table2(models.Model):
    desc=models.CharField(db_column='description',max_length=50,null=True)
    demand=models.CharField(db_column='QTY_demand',max_length=50,null=True)
    issued=models.CharField(db_column='QTY_issued',max_length=50,null=True)
    num=models.ForeignKey(MG47_table1,on_delete=models.CASCADE)

    class Meta:
        db_table = 'MG47_table2'