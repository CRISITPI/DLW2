from django.db import models
class M14HW11(models.Model): 
    doc_code = models.CharField(db_column='DOC_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    m14_no = models.CharField(db_column='M14_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m14_date = models.CharField(db_column='M14_DT',max_length=15, blank=True, null=True)  # Field name made lowercase   
    m13_no = models.CharField(db_column='M13_REF', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m13_date = models.CharField(db_column='M13_DT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    char_wo = models.CharField(db_column='C_WORKORDER', max_length=8, blank=True, null=True)  # Field name made lowercase.
    sl_no = models.DecimalField(db_column='M13_SLNO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.    
    pm_no = models.CharField(db_column='PM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    part_desc = models.CharField(db_column='PART_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='REASON', max_length=100, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    assly_desc = models.CharField(db_column='ASSLY_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    unit = models.DecimalField(db_column='UNIT', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    loco_no = models.CharField(db_column='LOCO_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
