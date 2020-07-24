from django.db import models
class m23doc(models.Model):
     id = models.AutoField(primary_key=True)
     date=models.CharField(db_column=' DATE', max_length=50)
     shop_no=models.CharField(db_column=' SHOP_NO', max_length=15)
     emp_no=models.CharField( db_column=' EMP_NO', max_length=15)
     emp_name=models.CharField( db_column=' EMP_NAME', max_length=25)
     ga_time=models.CharField(db_column='GA_TIME', max_length=50)
     purpose=models.CharField(db_column=' PURPOSE', max_length=80 ) 
     from_time=models.CharField(db_column='FROM_TIME', max_length=20)
     to_time=models.CharField(db_column='TO_TIME', max_length=20)
     todate=models.CharField(db_column='TO_DATE', max_length=20,blank=True, null=True)
     sno=models.CharField(db_column='SNo', max_length=20,blank=True, null=True)
     class Meta:
        db_table = 'M23new'