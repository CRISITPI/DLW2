# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Aaa(models.Model):
    code = models.CharField(db_column='CODE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    descripton = models.CharField(db_column='DESCRIPTON', max_length=20, blank=True, null=True)  # Field name made lowercase.
    epcs = models.CharField(db_column='EPCS', max_length=70, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AAA'


class Altdoc(models.Model):
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    expl_dt = models.DateField(db_column='EXPL_DT', blank=True, null=True)  # Field name made lowercase.
    prt_dt = models.DateField(db_column='PRT_DT', blank=True, null=True)  # Field name made lowercase.
    m2_fr = models.DecimalField(db_column='M2_FR', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m2_to = models.DecimalField(db_column='M2_TO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5_fr = models.DecimalField(db_column='M5_FR', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5_to = models.DecimalField(db_column='M5_TO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m14_fr = models.DecimalField(db_column='M14_FR', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m14_to = models.DecimalField(db_column='M14_TO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m4_fr = models.DecimalField(db_column='M4_FR', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m4_to = models.DecimalField(db_column='M4_TO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ALTDOC'


class Batch(models.Model):
    bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ep_type = models.CharField(db_column='EP_TYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    div = models.CharField(db_column='DIV', max_length=1, blank=True, null=True)  # Field name made lowercase.
    loco_fr = models.CharField(db_column='LOCO_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    loco_to = models.CharField(db_column='LOCO_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    batch_qty = models.DecimalField(db_column='BATCH_QTY', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    batch_type = models.CharField(db_column='BATCH_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    uot_wk_f = models.DecimalField(db_column='UOT_WK_F', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    b_expl_dt = models.DateField(db_column='B_EXPL_DT', blank=True, null=True)  # Field name made lowercase.
    b_close_dt = models.DateField(db_column='B_CLOSE_DT', blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    b_updt_dt = models.DateField(db_column='B_UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    org_batch = models.CharField(db_column='ORG_BATCH', max_length=7, blank=True, null=True)  # Field name made lowercase.
    repl_opn = models.CharField(db_column='REPL_OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    rel_date = models.DateField(db_column='REL_DATE', blank=True, null=True)  # Field name made lowercase.
    rel_dt_bc = models.DateField(db_column='REL_DT_BC', blank=True, null=True)  # Field name made lowercase.
    clos_dt_b = models.DateField(db_column='CLOS_DT_B', blank=True, null=True)  # Field name made lowercase.
    clos_dt_c = models.DateField(db_column='CLOS_DT_C', blank=True, null=True)  # Field name made lowercase.
    close_no = models.DecimalField(db_column='CLOSE_NO', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=20, blank=True, null=True)  # Field name made lowercase.
    so_no = models.CharField(db_column='SO_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    bal_qty = models.DecimalField(db_column='BAL_QTY', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    progress = models.CharField(db_column='PROGRESS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    old_status = models.CharField(db_column='OLD_STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    scno = models.DecimalField(db_column='SCNO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    date_of_trn = models.DateField(db_column='DATE_OF_TRN', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BATCH'


class BudCode(models.Model):
    department = models.CharField(db_column='DEPARTMENT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dept_code = models.CharField(db_column='DEPT_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    sub_dept = models.CharField(db_column='SUB_DEPT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    sub_dep_cd = models.CharField(db_column='SUB_DEP_CD', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BUD_CODE'


class Cnote(models.Model):
    chg_ind = models.CharField(db_column='CHG_IND', max_length=3, blank=True, null=True)  # Field name made lowercase.
    reg_no = models.CharField(db_column='REG_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    reg_dt = models.DateField(db_column='REG_DT', blank=True, null=True)  # Field name made lowercase.
    ref_1 = models.CharField(db_column='REF_1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ref_1_dt = models.DateField(db_column='REF_1_DT', blank=True, null=True)  # Field name made lowercase.
    ref_2 = models.CharField(db_column='REF_2', max_length=40, blank=True, null=True)  # Field name made lowercase.
    ref_2_dt = models.DateField(db_column='REF_2_DT', blank=True, null=True)  # Field name made lowercase.
    ppl_cn_no = models.CharField(db_column='PPL_CN_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    cn_reg_dt = models.DateField(db_column='CN_REG_DT', blank=True, null=True)  # Field name made lowercase.
    cn_dt = models.DateField(db_column='CN_DT', blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    date_recd = models.DateField(db_column='DATE_RECD', blank=True, null=True)  # Field name made lowercase.
    file_no = models.CharField(db_column='FILE_NO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    page_no = models.CharField(db_column='PAGE_NO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    lett_matt = models.CharField(db_column='LETT_MATT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    lett_no = models.CharField(db_column='LETT_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    from_name = models.CharField(db_column='FROM_NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    from_desig = models.CharField(db_column='FROM_DESIG', max_length=10, blank=True, null=True)  # Field name made lowercase.
    to_desig = models.CharField(db_column='TO_DESIG', max_length=10, blank=True, null=True)  # Field name made lowercase.
    copyto_1 = models.CharField(db_column='COPYTO_1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    copyto_2 = models.CharField(db_column='COPYTO_2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    copyto_3 = models.CharField(db_column='COPYTO_3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    encl = models.CharField(db_column='ENCL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    assly_desc = models.CharField(db_column='ASSLY_DESC', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CNOTE'


class Cod(models.Model):
    cd_type = models.CharField(db_column='CD_TYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    alpha_1 = models.CharField(db_column='ALPHA_1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    alpha_2 = models.CharField(db_column='ALPHA_2', max_length=70, blank=True, null=True)  # Field name made lowercase.
    num_1 = models.DecimalField(db_column='NUM_1', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_2 = models.DecimalField(db_column='NUM_2', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    num_3 = models.DecimalField(db_column='NUM_3', max_digits=8, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    txt = models.CharField(db_column='TXT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gen_info = models.CharField(db_column='GEN_INFO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lupd_date = models.DateField(db_column='LUPD_DATE', blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gm_ptno = models.CharField(db_column='GM_PTNO', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COD'


class Code(models.Model):
    cd_type = models.CharField(db_column='CD_TYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    alpha_1 = models.CharField(db_column='ALPHA_1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    alpha_2 = models.CharField(db_column='ALPHA_2', max_length=70, blank=True, null=True)  # Field name made lowercase.
    num_1 = models.DecimalField(db_column='NUM_1', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_2 = models.DecimalField(db_column='NUM_2', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    num_3 = models.DecimalField(db_column='NUM_3', max_digits=8, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    txt = models.CharField(db_column='TXT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gen_info = models.CharField(db_column='GEN_INFO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lupd_date = models.DateField(db_column='LUPD_DATE', blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gm_ptno = models.CharField(db_column='GM_PTNO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CODE'


class Concord(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    drgno = models.CharField(db_column='DRGNO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    drp = models.CharField(db_column='DRP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cat_no = models.CharField(db_column='CAT_NO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    stk_ut = models.CharField(db_column='STK_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cd_ind = models.CharField(db_column='CD_IND', max_length=4, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CONCORD'


class Cons(models.Model):
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    consignee = models.CharField(db_column='CONSIGNEE', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CONS'


class Copn(models.Model):
    reg_no = models.CharField(db_column='REG_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    shop_sec = models.CharField(db_column='SHOP_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    pa = models.DecimalField(db_column='PA', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at = models.DecimalField(db_column='AT', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lot = models.DecimalField(db_column='LOT', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    ncp_jbs = models.CharField(db_column='NCP_JBS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    m5_cd = models.CharField(db_column='M5_CD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cn_no = models.CharField(db_column='CN_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cn_date = models.DateField(db_column='CN_DATE', blank=True, null=True)  # Field name made lowercase.
    acd = models.CharField(db_column='ACD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    errmsg = models.CharField(db_column='ERRMSG', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COPN'


class Costsum(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=16, blank=True, null=True)  # Field name made lowercase.
    mat_cost = models.DecimalField(db_column='MAT_COST', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dlab_cost = models.DecimalField(db_column='DLAB_COST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    oh_cost = models.DecimalField(db_column='OH_COST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mfg_cost = models.DecimalField(db_column='MFG_COST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rly_cost = models.DecimalField(db_column='RLY_COST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tot_cost = models.DecimalField(db_column='TOT_COST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    foh = models.DecimalField(db_column='FOH', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    toh = models.DecimalField(db_column='TOH', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    aoh = models.DecimalField(db_column='AOH', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tot_time = models.DecimalField(db_column='TOT_TIME', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    c_date = models.DateField(db_column='C_DATE', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ind_cost = models.DecimalField(db_column='IND_COST', max_digits=9, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dep_chrg = models.DecimalField(db_column='DEP_CHRG', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pro_cost = models.DecimalField(db_column='PRO_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    loco_eff = models.CharField(db_column='LOCO_EFF', max_length=4, blank=True, null=True)  # Field name made lowercase.
    inc_bons = models.DecimalField(db_column='INC_BONS', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'COSTSUM'


class Cpart(models.Model):
    reg_no = models.CharField(db_column='REG_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=10000, blank=True, null=True)  # Field name made lowercase.
    drgno = models.CharField(db_column='DRGNO', max_length=18, blank=True, null=True)  # Field name made lowercase.
    spec = models.CharField(db_column='SPEC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    m14splt_cd = models.CharField(db_column='M14SPLT_CD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allow_perc = models.DecimalField(db_column='ALLOW_PERC', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m14_splt = models.CharField(db_column='M14_SPLT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    ppl_cn_no = models.CharField(db_column='PPL_CN_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    cn_date = models.DateField(db_column='CN_DATE', blank=True, null=True)  # Field name made lowercase.
    acd = models.CharField(db_column='ACD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    errmsg = models.CharField(db_column='ERRMSG', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CPART'


class Cpm(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_old = models.DecimalField(db_column='QTY_OLD', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_alt = models.DecimalField(db_column='QTY_ALT', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CPM'


class Cpm1(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_alt = models.DecimalField(db_column='QTY_ALT', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    cur_time = models.CharField(db_column='CUR_TIME', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CPM1'


class Cpmalt(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CPMALT'


class CpmProcess(models.Model):
    start_dt = models.DateField(db_column='START_DT', blank=True, null=True)  # Field name made lowercase.
    start_time = models.CharField(db_column='START_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    assly_over = models.DecimalField(db_column='ASSLY_OVER', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    end_dt = models.DateField(db_column='END_DT', blank=True, null=True)  # Field name made lowercase.
    end_time = models.CharField(db_column='END_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    updt_cpm = models.CharField(db_column='UPDT_CPM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cpm_start_time = models.CharField(db_column='CPM_START_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cpm_end_time = models.CharField(db_column='CPM_END_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    updt_qpp = models.CharField(db_column='UPDT_QPP', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qpp_start_time = models.CharField(db_column='QPP_START_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    qpp_end_time = models.CharField(db_column='QPP_END_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    qpp_assly_over = models.DecimalField(db_column='QPP_ASSLY_OVER', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CPM_PROCESS'


class Cst(models.Model):
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    stk_rate = models.DecimalField(db_column='STK_RATE', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    stk_ut = models.CharField(db_column='STK_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    po_rate = models.DecimalField(db_column='PO_RATE', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    po_ut = models.CharField(db_column='PO_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    po_no = models.CharField(db_column='PO_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    po_date = models.DateField(db_column='PO_DATE', blank=True, null=True)  # Field name made lowercase.
    mat_cost = models.DecimalField(db_column='MAT_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dlab_cost = models.DecimalField(db_column='DLAB_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tinc_bons = models.DecimalField(db_column='TINC_BONS', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    foh_cost = models.DecimalField(db_column='FOH_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    toh_cost = models.DecimalField(db_column='TOH_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    aoh_cost = models.DecimalField(db_column='AOH_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mfg_cost = models.DecimalField(db_column='MFG_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ind_chrg = models.DecimalField(db_column='IND_CHRG', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dep_chrg = models.DecimalField(db_column='DEP_CHRG', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pro_chrg = models.DecimalField(db_column='PRO_CHRG', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rly_cost = models.DecimalField(db_column='RLY_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tot_time = models.DecimalField(db_column='TOT_TIME', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mkt_pric_c = models.DecimalField(db_column='MKT_PRIC_C', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mkt_pric_p = models.DecimalField(db_column='MKT_PRIC_P', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mkt_price = models.DecimalField(db_column='MKT_PRICE', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    basic_rate = models.DecimalField(db_column='BASIC_RATE', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    diff_perc = models.DecimalField(db_column='DIFF_PERC', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_loco = models.DecimalField(db_column='QTY_LOCO', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rate_basis = models.CharField(db_column='RATE_BASIS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    soh_chrg = models.DecimalField(db_column='SOH_CHRG', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rem = models.CharField(db_column='REM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cur_time = models.CharField(db_column='CUR_TIME', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CST'


class Cstr(models.Model):
    reg_no = models.CharField(db_column='REG_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    pp_part = models.CharField(db_column='PP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cp_part = models.CharField(db_column='CP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    ref_ind = models.CharField(db_column='REF_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ref_no = models.CharField(db_column='REF_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cutdia_no = models.CharField(db_column='CUTDIA_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    chg_ind = models.CharField(db_column='CHG_IND', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cn_no = models.CharField(db_column='CN_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    cn_date = models.DateField(db_column='CN_DATE', blank=True, null=True)  # Field name made lowercase.
    acd = models.CharField(db_column='ACD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    errmsg = models.CharField(db_column='ERRMSG', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CSTR'


class Cstrerr(models.Model):
    reg_no = models.CharField(db_column='REG_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    pp_part = models.CharField(db_column='PP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cp_part = models.CharField(db_column='CP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    ref_ind = models.CharField(db_column='REF_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ref_no = models.CharField(db_column='REF_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cutdia_no = models.CharField(db_column='CUTDIA_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    chg_ind = models.CharField(db_column='CHG_IND', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cn_no = models.CharField(db_column='CN_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    cn_date = models.DateField(db_column='CN_DATE', blank=True, null=True)  # Field name made lowercase.
    acd = models.CharField(db_column='ACD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    errmsg = models.CharField(db_column='ERRMSG', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CSTRERR'


class Cst2018(models.Model):
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    mkt_price = models.DecimalField(db_column='MKT_PRICE', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CST_2018'


class Cst2018Mkt(models.Model):
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    mat_cost = models.DecimalField(db_column='MAT_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mfg_cost = models.DecimalField(db_column='MFG_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rly_cost = models.DecimalField(db_column='RLY_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mkt_price = models.DecimalField(db_column='MKT_PRICE', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CST_2018MKT'


class CstProcess(models.Model):
    start_dt = models.DateField(db_column='START_DT', blank=True, null=True)  # Field name made lowercase.
    start_time = models.CharField(db_column='START_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    assly_process = models.DecimalField(db_column='ASSLY_PROCESS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    progress = models.DecimalField(db_column='PROGRESS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    end_dt = models.DateField(db_column='END_DT', blank=True, null=True)  # Field name made lowercase.
    end_time = models.CharField(db_column='END_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CST_PROCESS'


class Cutdia(models.Model):
    cutdia_no = models.CharField(db_column='CUTDIA_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ep_part = models.CharField(db_column='EP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rm_part = models.CharField(db_column='RM_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_desc = models.CharField(db_column='RM_DESC', max_length=18, blank=True, null=True)  # Field name made lowercase.
    thick_rm = models.DecimalField(db_column='THICK_RM', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rm_width = models.DecimalField(db_column='RM_WIDTH', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rm_len = models.DecimalField(db_column='RM_LEN', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rm_spec = models.CharField(db_column='RM_SPEC', max_length=15, blank=True, null=True)  # Field name made lowercase.
    wt_rm = models.DecimalField(db_column='WT_RM', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    rm_unit = models.CharField(db_column='RM_UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    batch_size = models.DecimalField(db_column='BATCH_SIZE', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wt_rm_ml = models.DecimalField(db_column='WT_RM_ML', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CUTDIA'


class Cutpart(models.Model):
    cut_dia = models.CharField(db_column='CUT_DIA', max_length=8, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty_p_loco = models.DecimalField(db_column='QTY_P_LOCO', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CUTPART'


class CMenu(models.Model):
    usr_cd = models.CharField(db_column='USR_CD', max_length=8, blank=True, null=True)  # Field name made lowercase.
    p_id = models.CharField(db_column='P_ID', max_length=2, blank=True, null=True)  # Field name made lowercase.
    c_id = models.CharField(db_column='C_ID', max_length=2, blank=True, null=True)  # Field name made lowercase.
    prog_title = models.CharField(db_column='PROG_TITLE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prog_url = models.CharField(db_column='PROG_URL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prog_name = models.CharField(db_column='PROG_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'C_MENU'


class DbUpdt(models.Model):
    dt = models.DateField(db_column='DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DB_UPDT'


class Docjbs(models.Model):
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_ord = models.CharField(db_column='QTY_ORD', max_length=9, blank=True, null=True)  # Field name made lowercase.
    shop_sec = models.CharField(db_column='SHOP_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    at = models.DecimalField(db_column='AT', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lot = models.DecimalField(db_column='LOT', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    ncp_jbs = models.CharField(db_column='NCP_JBS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    n_shop = models.CharField(db_column='N_SHOP', max_length=4, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_part = models.CharField(db_column='ALT_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCJBS'


class Doclog(models.Model):
    expl_dt = models.DateField(db_column='EXPL_DT', blank=True, null=True)  # Field name made lowercase.
    doc_type = models.CharField(db_column='DOC_TYPE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    scl_cl = models.CharField(db_column='SCL_CL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    batch_type = models.CharField(db_column='BATCH_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    doc_fr = models.DecimalField(db_column='DOC_FR', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    doc_to = models.DecimalField(db_column='DOC_TO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    sel_yn = models.CharField(db_column='SEL_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prt_ind = models.CharField(db_column='PRT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prt_dt = models.DateField(db_column='PRT_DT', blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    kit_ind = models.CharField(db_column='KIT_IND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    stg = models.CharField(db_column='STG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    kit_no = models.DecimalField(db_column='KIT_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    tr_flag = models.CharField(db_column='TR_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DOCLOG'


class Ei301(models.Model):
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    block_no = models.CharField(db_column='BLOCK_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    comp_type = models.CharField(db_column='COMP_TYPE', max_length=30, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    srl_nol1 = models.CharField(db_column='SRL_NOL1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nol2 = models.CharField(db_column='SRL_NOL2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nol3 = models.CharField(db_column='SRL_NOL3', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nol4 = models.CharField(db_column='SRL_NOL4', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nol5 = models.CharField(db_column='SRL_NOL5', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nol6 = models.CharField(db_column='SRL_NOL6', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nol7 = models.CharField(db_column='SRL_NOL7', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nol8 = models.CharField(db_column='SRL_NOL8', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nor1 = models.CharField(db_column='SRL_NOR1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nor2 = models.CharField(db_column='SRL_NOR2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nor3 = models.CharField(db_column='SRL_NOR3', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nor4 = models.CharField(db_column='SRL_NOR4', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nor5 = models.CharField(db_column='SRL_NOR5', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nor6 = models.CharField(db_column='SRL_NOR6', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nor7 = models.CharField(db_column='SRL_NOR7', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nor8 = models.CharField(db_column='SRL_NOR8', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_no9 = models.CharField(db_column='SRL_NO9', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_norc1 = models.CharField(db_column='SRL_NORC1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_norc2 = models.CharField(db_column='SRL_NORC2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nolc1 = models.CharField(db_column='SRL_NOLC1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    srl_nolc2 = models.CharField(db_column='SRL_NOLC2', max_length=20, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EI30_1'


class Ei303(models.Model):
    form_no = models.CharField(db_column='FORM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    block_no = models.CharField(db_column='BLOCK_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    make = models.CharField(db_column='MAKE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    maker_slno = models.CharField(db_column='MAKER_SLNO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EI30_3'


class Ei304(models.Model):
    form_no = models.CharField(db_column='FORM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    block_no = models.CharField(db_column='BLOCK_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    make = models.CharField(db_column='MAKE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    maker_slno = models.CharField(db_column='MAKER_SLNO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=50, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EI30_4'


class Ei481(models.Model):
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    block_no = models.CharField(db_column='BLOCK_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    param = models.CharField(db_column='PARAM', max_length=30, blank=True, null=True)  # Field name made lowercase.
    val_1 = models.CharField(db_column='VAL_1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_2 = models.CharField(db_column='VAL_2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EI48_1'


class Ei482(models.Model):
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    block_no = models.CharField(db_column='BLOCK_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    param = models.CharField(db_column='PARAM', max_length=30, blank=True, null=True)  # Field name made lowercase.
    val_l1 = models.CharField(db_column='VAL_L1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_l2 = models.CharField(db_column='VAL_L2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_l3 = models.CharField(db_column='VAL_L3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_l4 = models.CharField(db_column='VAL_L4', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_l5 = models.CharField(db_column='VAL_L5', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_l6 = models.CharField(db_column='VAL_L6', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_l7 = models.CharField(db_column='VAL_L7', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_l8 = models.CharField(db_column='VAL_L8', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_r1 = models.CharField(db_column='VAL_R1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_r2 = models.CharField(db_column='VAL_R2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_r3 = models.CharField(db_column='VAL_R3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_r4 = models.CharField(db_column='VAL_R4', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_r5 = models.CharField(db_column='VAL_R5', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_r6 = models.CharField(db_column='VAL_R6', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_r7 = models.CharField(db_column='VAL_R7', max_length=10, blank=True, null=True)  # Field name made lowercase.
    val_r8 = models.CharField(db_column='VAL_R8', max_length=10, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EI48_2'


class Enq(models.Model):
    plant = models.CharField(db_column='PLANT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    enq_no = models.CharField(db_column='ENQ_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    enq_dt = models.DateField(db_column='ENQ_DT', blank=True, null=True)  # Field name made lowercase.
    opn_dt = models.DateField(db_column='OPN_DT', blank=True, null=True)  # Field name made lowercase.
    app_dt = models.DateField(db_column='APP_DT', blank=True, null=True)  # Field name made lowercase.
    enq_regn = models.CharField(db_column='ENQ_REGN', max_length=4, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    regn_dt = models.DateField(db_column='REGN_DT', blank=True, null=True)  # Field name made lowercase.
    quote_no = models.CharField(db_column='QUOTE_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    quote_dt = models.DateField(db_column='QUOTE_DT', blank=True, null=True)  # Field name made lowercase.
    dp_code = models.CharField(db_column='DP_CODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    excl = models.DecimalField(db_column='EXCL', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=35, blank=True, null=True)  # Field name made lowercase.
    enq_ref = models.CharField(db_column='ENQ_REF', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ENQ'


class Enqreg(models.Model):
    plant = models.CharField(db_column='PLANT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    enq_no = models.CharField(db_column='ENQ_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    enq_dt = models.DateField(db_column='ENQ_DT', blank=True, null=True)  # Field name made lowercase.
    opn_dt = models.DateField(db_column='OPN_DT', blank=True, null=True)  # Field name made lowercase.
    app_dt = models.DateField(db_column='APP_DT', blank=True, null=True)  # Field name made lowercase.
    enq_regn = models.CharField(db_column='ENQ_REGN', max_length=4, blank=True, null=True)  # Field name made lowercase.
    regn_dt = models.DateField(db_column='REGN_DT', blank=True, null=True)  # Field name made lowercase.
    quote_no = models.CharField(db_column='QUOTE_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    quote_dt = models.DateField(db_column='QUOTE_DT', blank=True, null=True)  # Field name made lowercase.
    dp_code = models.CharField(db_column='DP_CODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    excl = models.DecimalField(db_column='EXCL', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=35, blank=True, null=True)  # Field name made lowercase.
    enq_ref = models.CharField(db_column='ENQ_REF', max_length=40, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ENQREG'


class EpcCode(models.Model):
    cd_type = models.CharField(db_column='CD_TYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    alpha_1 = models.CharField(db_column='ALPHA_1', max_length=20, blank=True, null=True)  # Field name made lowercase.
    alpha_2 = models.CharField(db_column='ALPHA_2', max_length=70, blank=True, null=True)  # Field name made lowercase.
    num_1 = models.DecimalField(db_column='NUM_1', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    num_2 = models.DecimalField(db_column='NUM_2', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    num_3 = models.DecimalField(db_column='NUM_3', max_digits=8, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    txt = models.CharField(db_column='TXT', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gen_info = models.CharField(db_column='GEN_INFO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lupd_date = models.DateField(db_column='LUPD_DATE', blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gm_ptno = models.CharField(db_column='GM_PTNO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EPC_CODE'


class EpPart(models.Model):
    ep_part = models.CharField(db_column='EP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    start_time = models.CharField(db_column='START_TIME', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EP_PART'


class EpPart2(models.Model):
    ep_part = models.CharField(db_column='EP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    start_time = models.CharField(db_column='START_TIME', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EP_PART2'


class FundAvi(models.Model):
    department = models.CharField(db_column='DEPARTMENT', max_length=15, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    sanc_amt = models.DecimalField(db_column='SANC_AMT', max_digits=9, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    fund_balan = models.DecimalField(db_column='FUND_BALAN', max_digits=9, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FUND_AVI'


class Gi25(models.Model):
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    drg_catno = models.CharField(db_column='DRG_CATNO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    vend_name = models.CharField(db_column='VEND_NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.CharField(db_column='UPDT_DT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GI25'


class Gi45(models.Model):
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    drg_catno = models.CharField(db_column='DRG_CATNO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    qty = models.CharField(db_column='QTY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GI45'


class Gi45Ext(models.Model):
    slno = models.CharField(db_column='SLNO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    other_item = models.CharField(db_column='OTHER_ITEM', max_length=35, blank=True, null=True)  # Field name made lowercase.
    sel_sw = models.CharField(db_column='SEL_SW', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GI45EXT'


class Gm(models.Model):
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    rate_basis = models.CharField(db_column='RATE_BASIS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mkt_price = models.DecimalField(db_column='MKT_PRICE', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GM'


class GmCode(models.Model):
    cd_type = models.CharField(db_column='CD_TYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    alpha_1 = models.CharField(db_column='ALPHA_1', max_length=30, blank=True, null=True)  # Field name made lowercase.
    alpha_2 = models.CharField(db_column='ALPHA_2', max_length=15, blank=True, null=True)  # Field name made lowercase.
    alpha_3 = models.CharField(db_column='ALPHA_3', max_length=40, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GM_CODE'


class Hstr(models.Model):
    pp_part = models.CharField(db_column='PP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cp_part = models.CharField(db_column='CP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    ref_ind = models.CharField(db_column='REF_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ref_no = models.CharField(db_column='REF_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    lead_time = models.DecimalField(db_column='LEAD_TIME', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    reg_no = models.CharField(db_column='REG_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HSTR'


class Hwm14His(models.Model):
    doc_code = models.CharField(db_column='DOC_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    doc_no = models.DecimalField(db_column='DOC_NO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pm_no = models.CharField(db_column='PM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    prtdt = models.DateField(db_column='PRTDT', blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ward_no = models.CharField(db_column='WARD_NO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='REASON', max_length=40, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HWM14HIS'


class Hwm5(models.Model):
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    rm_partno = models.CharField(db_column='RM_PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_desc = models.CharField(db_column='RM_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    rm_ut = models.CharField(db_column='RM_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.DecimalField(db_column='RM_QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    shop_sec = models.CharField(db_column='SHOP_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=4, blank=True, null=True)  # Field name made lowercase.
    opn_desc = models.CharField(db_column='OPN_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    opndesc = models.CharField(db_column='OPNDESC', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    pa = models.DecimalField(db_column='PA', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at = models.DecimalField(db_column='AT', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    no_off = models.DecimalField(db_column='NO_OFF', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qty_ord = models.DecimalField(db_column='QTY_ORD', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    scl_cl = models.CharField(db_column='SCL_CL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    m2sln = models.DecimalField(db_column='M2SLN', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m2_date = models.DateField(db_column='M2_DATE', blank=True, null=True)  # Field name made lowercase.
    m4_no = models.DecimalField(db_column='M4_NO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m4_date = models.DateField(db_column='M4_DATE', blank=True, null=True)  # Field name made lowercase.
    m5glsn = models.DecimalField(db_column='M5GLSN', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5_date = models.DateField(db_column='M5_DATE', blank=True, null=True)  # Field name made lowercase.
    expl_dt = models.DateField(db_column='EXPL_DT', blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pr_shopsec = models.CharField(db_column='PR_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    n_shopsec = models.CharField(db_column='N_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    hw_cd = models.CharField(db_column='HW_CD', max_length=2, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    okcpm = models.CharField(db_column='OKCPM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    okptc = models.CharField(db_column='OKPTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    okmrq = models.CharField(db_column='OKMRQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    okopn = models.CharField(db_column='OKOPN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oksslc = models.CharField(db_column='OKSSLC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    okjbs = models.CharField(db_column='OKJBS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    oksplit = models.CharField(db_column='OKSPLIT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=5, blank=True, null=True)  # Field name made lowercase.
    time_pcpls = models.DecimalField(db_column='TIME_PCPLS', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tot_hrspls = models.DecimalField(db_column='TOT_HRSPLS', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ib_no = models.CharField(db_column='IB_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sel_sw = models.CharField(db_column='SEL_SW', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sel_sw_hod = models.CharField(db_column='SEL_SW_HOD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    usr_cd = models.CharField(db_column='USR_CD', max_length=6, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='REMARKS', max_length=30, blank=True, null=True)  # Field name made lowercase.
    shopsecold = models.CharField(db_column='SHOPSECOLD', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lcnoold = models.CharField(db_column='LCNOOLD', max_length=4, blank=True, null=True)  # Field name made lowercase.
    print_ctrl = models.DecimalField(db_column='PRINT_CTRL', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    m13_no = models.CharField(db_column='M13_NO', max_length=11, blank=True, null=True)  # Field name made lowercase.
    m13_date = models.DateField(db_column='M13_DATE', blank=True, null=True)  # Field name made lowercase.
    org_batch = models.CharField(db_column='ORG_BATCH', max_length=7, blank=True, null=True)  # Field name made lowercase.
    org_brnno = models.DecimalField(db_column='ORG_BRNNO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    plregno = models.CharField(db_column='PLREGNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    m5_cd = models.CharField(db_column='M5_CD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ncp_jbs = models.CharField(db_column='NCP_JBS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HWM5'


class Inspcomp(models.Model):
    form_no = models.CharField(db_column='FORM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    partno_ep = models.CharField(db_column='PARTNO_EP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    desc_ep = models.CharField(db_column='DESC_EP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'INSPCOMP'


class Inspcto(models.Model):
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    form_no = models.CharField(db_column='FORM_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    copy_to = models.CharField(db_column='COPY_TO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'INSPCTO'


class Insploco(models.Model):
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    block_no = models.CharField(db_column='BLOCK_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    partno_ep = models.CharField(db_column='PARTNO_EP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=9, blank=True, null=True)  # Field name made lowercase.
    batchno_e = models.CharField(db_column='BATCHNO_E', max_length=9, blank=True, null=True)  # Field name made lowercase.
    builder_no = models.CharField(db_column='BUILDER_NO', max_length=12, blank=True, null=True)  # Field name made lowercase.
    assly_slno = models.CharField(db_column='ASSLY_SLNO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    eng_slno = models.CharField(db_column='ENG_SLNO', max_length=25, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    type_e = models.CharField(db_column='TYPE_E', max_length=5, blank=True, null=True)  # Field name made lowercase.
    class_field = models.CharField(db_column='CLASS', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    rly_allot = models.CharField(db_column='RLY_ALLOT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    shed = models.CharField(db_column='SHED', max_length=5, blank=True, null=True)  # Field name made lowercase.
    date_despt = models.DateField(db_column='DATE_DESPT', blank=True, null=True)  # Field name made lowercase.
    order_no = models.CharField(db_column='ORDER_NO', max_length=9, blank=True, null=True)  # Field name made lowercase.
    orderno_e = models.CharField(db_column='ORDERNO_E', max_length=9, blank=True, null=True)  # Field name made lowercase.
    name_driv = models.CharField(db_column='NAME_DRIV', max_length=20, blank=True, null=True)  # Field name made lowercase.
    name_assis = models.CharField(db_column='NAME_ASSIS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rly_driv = models.CharField(db_column='RLY_DRIV', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shed_driv = models.CharField(db_column='SHED_DRIV', max_length=5, blank=True, null=True)  # Field name made lowercase.
    count_sign = models.CharField(db_column='COUNT_SIGN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    no_cylind = models.CharField(db_column='NO_CYLIND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    bore = models.CharField(db_column='BORE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    bore1 = models.CharField(db_column='BORE1', max_length=5, blank=True, null=True)  # Field name made lowercase.
    stroke = models.CharField(db_column='STROKE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    displ = models.CharField(db_column='DISPL', max_length=3, blank=True, null=True)  # Field name made lowercase.
    start_dt = models.DateField(db_column='START_DT', blank=True, null=True)  # Field name made lowercase.
    compl_dt = models.DateField(db_column='COMPL_DT', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'INSPLOCO'


class Insppara(models.Model):
    form_no = models.CharField(db_column='FORM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    param = models.CharField(db_column='PARAM', max_length=30, blank=True, null=True)  # Field name made lowercase.
    default_vl = models.CharField(db_column='DEFAULT_VL', max_length=10, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'INSPPARA'


class Itemcostsum(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=16, blank=True, null=True)  # Field name made lowercase.
    mat_cost = models.DecimalField(db_column='MAT_COST', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dlab_cost = models.DecimalField(db_column='DLAB_COST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    oh_cost = models.DecimalField(db_column='OH_COST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mfg_cost = models.DecimalField(db_column='MFG_COST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rly_cost = models.DecimalField(db_column='RLY_COST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tot_cost = models.DecimalField(db_column='TOT_COST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    foh = models.DecimalField(db_column='FOH', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    toh = models.DecimalField(db_column='TOH', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    aoh = models.DecimalField(db_column='AOH', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tot_time = models.DecimalField(db_column='TOT_TIME', max_digits=7, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    c_date = models.DateField(db_column='C_DATE', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ind_cost = models.DecimalField(db_column='IND_COST', max_digits=9, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dep_chrg = models.DecimalField(db_column='DEP_CHRG', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pro_cost = models.DecimalField(db_column='PRO_COST', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    loco_eff = models.CharField(db_column='LOCO_EFF', max_length=4, blank=True, null=True)  # Field name made lowercase.
    inc_bons = models.DecimalField(db_column='INC_BONS', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ITEMCOSTSUM'


class Lc1(models.Model):
    shop_sec = models.CharField(db_column='SHOP_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lcno = models.CharField(db_column='LCNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    no_men = models.DecimalField(db_column='NO_MEN', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    no_mcs1 = models.DecimalField(db_column='NO_MCS1', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    no_mcs2 = models.DecimalField(db_column='NO_MCS2', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    no_mcs3 = models.DecimalField(db_column='NO_MCS3', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LC1'


class Loadbk(models.Model):
    sh_sec = models.CharField(db_column='SH_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    no_mc = models.DecimalField(db_column='NO_MC', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    loco_load_hrs = models.DecimalField(db_column='LOCO_LOAD_HRS', max_digits=9, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cap_mnth_hrs = models.DecimalField(db_column='CAP_MNTH_HRS', max_digits=9, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    prod_cap_mnth = models.DecimalField(db_column='PROD_CAP_MNTH', max_digits=9, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lc_des = models.CharField(db_column='LC_DES', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    ptdes = models.CharField(db_column='PTDES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    m5_cd = models.CharField(db_column='M5_CD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pa = models.DecimalField(db_column='PA', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at_hrs = models.DecimalField(db_column='AT_HRS', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lot = models.DecimalField(db_column='LOT', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    dt_run = models.DateField(db_column='DT_RUN', blank=True, null=True)  # Field name made lowercase.
    cur_time = models.CharField(db_column='CUR_TIME', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LOADBK'


class LoadPrt(models.Model):
    f_name = models.CharField(db_column='F_NAME', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prt_type = models.CharField(db_column='PRT_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nodocs = models.DecimalField(db_column='NODOCS', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    staff_name = models.CharField(db_column='STAFF_NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LOAD_PRT'


class Locodesp(models.Model):
    slno = models.DecimalField(db_column='SLNO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    loco_type = models.CharField(db_column='LOCO_TYPE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    loco_no = models.CharField(db_column='LOCO_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dlw_sn = models.CharField(db_column='DLW_SN', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rly = models.CharField(db_column='RLY', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dt_desp = models.DateField(db_column='DT_DESP', blank=True, null=True)  # Field name made lowercase.
    rsp_ref = models.CharField(db_column='RSP_REF', max_length=40, blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='REMARKS', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LOCODESP'


class Lstr(models.Model):
    pp_part = models.CharField(db_column='PP_PART', max_length=15, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    itemno = models.CharField(db_column='ITEMNO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    cp_part = models.CharField(db_column='CP_PART', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dlw_part = models.CharField(db_column='DLW_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rev = models.CharField(db_column='REV', max_length=5, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mb = models.CharField(db_column='MB', max_length=2, blank=True, null=True)  # Field name made lowercase.
    hj_ind = models.CharField(db_column='HJ_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    kit_ind = models.CharField(db_column='KIT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(db_column='UM', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rem = models.CharField(db_column='REM', max_length=10, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LSTR'


class M13(models.Model):
    usr_cd = models.CharField(db_column='USR_CD', max_length=6, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    m13_sn = models.CharField(db_column='M13_SN', max_length=7, blank=True, null=True)  # Field name made lowercase.
    m13_no = models.CharField(db_column='M13_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m13_date = models.DateField(db_column='M13_DATE', blank=True, null=True)  # Field name made lowercase.
    wo = models.CharField(db_column='WO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty_tot = models.DecimalField(db_column='QTY_TOT', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qty_ins = models.DecimalField(db_column='QTY_INS', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qty_pas = models.DecimalField(db_column='QTY_PAS', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qty_rej = models.DecimalField(db_column='QTY_REJ', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fault_cd = models.CharField(db_column='FAULT_CD', max_length=3, blank=True, null=True)  # Field name made lowercase.
    vendor_cd = models.CharField(db_column='VENDOR_CD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    shop = models.CharField(db_column='SHOP', max_length=4, blank=True, null=True)  # Field name made lowercase.
    wo_rep = models.CharField(db_column='WO_REP', max_length=7, blank=True, null=True)  # Field name made lowercase.
    m15_no = models.CharField(db_column='M15_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m15_date = models.DateField(db_column='M15_DATE', blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    wo_st = models.CharField(db_column='WO_ST', max_length=3, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rej_cat = models.CharField(db_column='REJ_CAT', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sel_sw = models.CharField(db_column='SEL_SW', max_length=1, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_dt = models.DateField(db_column='DEL_DT', blank=True, null=True)  # Field name made lowercase.
    hw_dt = models.DateField(db_column='HW_DT', blank=True, null=True)  # Field name made lowercase.
    m13_no_old = models.CharField(db_column='M13_NO_OLD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m13_prtdt = models.DateField(db_column='M13_PRTDT', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='REASON', max_length=120, blank=True, null=True)  # Field name made lowercase.
    job_no = models.CharField(db_column='JOB_NO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    staff_no = models.CharField(db_column='STAFF_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    costdet_no = models.CharField(db_column='COSTDET_NO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    allocation = models.CharField(db_column='ALLOCATION', max_length=15, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='RATE', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    value = models.DecimalField(db_column='VALUE', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    plno_class = models.CharField(db_column='PLNO_CLASS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m15_prtdt = models.DateField(db_column='M15_PRTDT', blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M13'


class M13Shop(models.Model):
    usr_cd = models.CharField(db_column='USR_CD', max_length=6, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    m13_sn = models.CharField(db_column='M13_SN', max_length=7, blank=True, null=True)  # Field name made lowercase.
    m13_no = models.CharField(db_column='M13_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m13_date = models.DateField(db_column='M13_DATE', blank=True, null=True)  # Field name made lowercase.
    wo = models.CharField(db_column='WO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty_tot = models.DecimalField(db_column='QTY_TOT', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qty_ins = models.DecimalField(db_column='QTY_INS', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qty_pas = models.DecimalField(db_column='QTY_PAS', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qty_rej = models.DecimalField(db_column='QTY_REJ', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fault_cd = models.CharField(db_column='FAULT_CD', max_length=3, blank=True, null=True)  # Field name made lowercase.
    vendor_cd = models.CharField(db_column='VENDOR_CD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shop = models.CharField(db_column='SHOP', max_length=4, blank=True, null=True)  # Field name made lowercase.
    wo_rep = models.CharField(db_column='WO_REP', max_length=7, blank=True, null=True)  # Field name made lowercase.
    m15_no = models.CharField(db_column='M15_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m15_date = models.DateField(db_column='M15_DATE', blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    wo_st = models.CharField(db_column='WO_ST', max_length=3, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rej_cat = models.CharField(db_column='REJ_CAT', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sel_sw = models.CharField(db_column='SEL_SW', max_length=1, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hw_dt = models.DateField(db_column='HW_DT', blank=True, null=True)  # Field name made lowercase.
    m13_no_old = models.CharField(db_column='M13_NO_OLD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m13_prtdt = models.DateField(db_column='M13_PRTDT', blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M13SHOP'


class M13Tmp21(models.Model):
    bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ep_type = models.CharField(db_column='EP_TYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pm_no = models.CharField(db_column='PM_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    org_batch = models.CharField(db_column='ORG_BATCH', max_length=7, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    batch_qty = models.DecimalField(db_column='BATCH_QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    batch_type = models.CharField(db_column='BATCH_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    loco_fr = models.CharField(db_column='LOCO_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    loco_to = models.CharField(db_column='LOCO_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    b_expl_dt = models.DateField(db_column='B_EXPL_DT', blank=True, null=True)  # Field name made lowercase.
    bo_updt_dt = models.DateField(db_column='BO_UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M13TMP21'


class M13X(models.Model):
    usr_cd = models.CharField(db_column='USR_CD', max_length=6, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    m13_sn = models.CharField(db_column='M13_SN', max_length=7, blank=True, null=True)  # Field name made lowercase.
    m13_no = models.CharField(db_column='M13_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m13_date = models.DateField(db_column='M13_DATE', blank=True, null=True)  # Field name made lowercase.
    wo = models.CharField(db_column='WO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty_tot = models.DecimalField(db_column='QTY_TOT', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qty_ins = models.DecimalField(db_column='QTY_INS', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qty_pas = models.DecimalField(db_column='QTY_PAS', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qty_rej = models.DecimalField(db_column='QTY_REJ', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fault_cd = models.CharField(db_column='FAULT_CD', max_length=3, blank=True, null=True)  # Field name made lowercase.
    vendor_cd = models.CharField(db_column='VENDOR_CD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    shop = models.CharField(db_column='SHOP', max_length=4, blank=True, null=True)  # Field name made lowercase.
    wo_rep = models.CharField(db_column='WO_REP', max_length=7, blank=True, null=True)  # Field name made lowercase.
    m15_no = models.CharField(db_column='M15_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m15_date = models.DateField(db_column='M15_DATE', blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    wo_st = models.CharField(db_column='WO_ST', max_length=3, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rej_cat = models.CharField(db_column='REJ_CAT', max_length=3, blank=True, null=True)  # Field name made lowercase.
    sel_sw = models.CharField(db_column='SEL_SW', max_length=1, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hw_dt = models.DateField(db_column='HW_DT', blank=True, null=True)  # Field name made lowercase.
    m13_no_old = models.CharField(db_column='M13_NO_OLD', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m13_prtdt = models.DateField(db_column='M13_PRTDT', blank=True, null=True)  # Field name made lowercase.
    reason = models.CharField(db_column='REASON', max_length=120, blank=True, null=True)  # Field name made lowercase.
    job_no = models.CharField(db_column='JOB_NO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    staff_no = models.CharField(db_column='STAFF_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    costdet_no = models.CharField(db_column='COSTDET_NO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    allocation = models.CharField(db_column='ALLOCATION', max_length=15, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='RATE', max_digits=11, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    value = models.DecimalField(db_column='VALUE', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    plno_class = models.CharField(db_column='PLNO_CLASS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    m15_prtdt = models.DateField(db_column='M15_PRTDT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M13X'


class M14Hw(models.Model):
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pm_no = models.CharField(db_column='PM_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M14HW'


class M14M4(models.Model):
    doc_code = models.CharField(db_column='DOC_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    doc_no = models.DecimalField(db_column='DOC_NO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pm_no = models.CharField(db_column='PM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    due_wk = models.CharField(db_column='DUE_WK', max_length=4, blank=True, null=True)  # Field name made lowercase.
    prtdt = models.DateField(db_column='PRTDT', blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    doc_ind = models.CharField(db_column='DOC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    stage = models.CharField(db_column='STAGE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ward_no = models.CharField(db_column='WARD_NO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    finyear = models.CharField(db_column='FINYEAR', max_length=2, blank=True, null=True)  # Field name made lowercase.
    vr_no = models.CharField(db_column='VR_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    kit_ind = models.CharField(db_column='KIT_IND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='STATION', max_length=3, blank=True, null=True)  # Field name made lowercase.
    stg = models.CharField(db_column='STG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sub_kit = models.CharField(db_column='SUB_KIT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    opn_no = models.CharField(db_column='OPN_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    kit_no = models.DecimalField(db_column='KIT_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sub_docno = models.DecimalField(db_column='SUB_DOCNO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    lieu_part = models.CharField(db_column='LIEU_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    drawn_by = models.CharField(db_column='DRAWN_BY', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    doc_no_old = models.DecimalField(db_column='DOC_NO_OLD', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)
    received_mat = models.CharField(db_column='RECEIVED_MAT', max_length=50, blank=True, null=True)
    issued_qty = models.CharField(db_column='ISSUED_QTY', max_length=50, blank=True, null=True)
    received_qty = models.CharField(db_column='RECEIVED_QTY', max_length=50, blank=True, null=True)
    remarks = models.CharField(db_column='REMARKS', max_length=50, blank=True, null=True)
    line = models.CharField(db_column='LINE', max_length=50, blank=True, null=True)
    closing_bal = models.CharField(db_column='CLOSING_BAL', max_length=50, blank=True, null=True)
    laser_pst = models.CharField(db_column='LASER_PST', max_length=50, blank=True, default=0)
    posted_date = models.CharField(db_column='POSTED_DATE', max_length=50, blank=True, default=0)
    wardkp_date = models.CharField(db_column='WARDKP_DATE', max_length=50, blank=True, default=0)
    shopsup_date = models.CharField(db_column='SHOPSUP_DATE', max_length=50, blank=True, default=0)
    posted1_date = models.CharField(db_column='POSTED1_DATE', max_length=50, blank=True, default=0)
    received_mat14 = models.CharField(db_column='RECEIVED_MAT14', max_length=50, blank=True, null=True)
    issued_qty14 = models.CharField(db_column='ISSUED_QTY14', max_length=50, blank=True, null=True)
    received_qty14 = models.CharField(db_column='RECEIVED_QTY14', max_length=50, blank=True, null=True)
    remarks14 = models.CharField(db_column='REMARKS14', max_length=50, blank=True, null=True)
    line14 = models.CharField(db_column='LINE14', max_length=50, blank=True, null=True)
    closing_bal14 = models.CharField(db_column='CLOSING_BAL14', max_length=50, blank=True, null=True)
    laser_pst14 = models.CharField(db_column='LASER_PST14', max_length=50, blank=True, default=0)
    posted_date14 = models.CharField(db_column='POSTED_DATE14', max_length=50, blank=True, default=0)
    wardkp_date14 = models.CharField(db_column='WARDKP_DATE14', max_length=50, blank=True, default=0)
    shopsup_date14 = models.CharField(db_column='SHOPSUP_DATE14', max_length=50, blank=True, default=0)
    posted1_date14 = models.CharField(db_column='POSTED1_DATE14', max_length=50, blank=True, default=0)

    class Meta:

        db_table = 'M14M4'


class M14M4Cris(models.Model):
    doc_code = models.CharField(db_column='DOC_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    doc_no = models.DecimalField(db_column='DOC_NO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pm_no = models.CharField(db_column='PM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    due_wk = models.CharField(db_column='DUE_WK', max_length=4, blank=True, null=True)  # Field name made lowercase.
    prtdt = models.DateField(db_column='PRTDT', blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    doc_ind = models.CharField(db_column='DOC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    stage = models.CharField(db_column='STAGE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ward_no = models.CharField(db_column='WARD_NO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    finyear = models.CharField(db_column='FINYEAR', max_length=2, blank=True, null=True)  # Field name made lowercase.
    vr_no = models.CharField(db_column='VR_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    kit_ind = models.CharField(db_column='KIT_IND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='STATION', max_length=3, blank=True, null=True)  # Field name made lowercase.
    stg = models.CharField(db_column='STG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sub_kit = models.CharField(db_column='SUB_KIT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    opn_no = models.CharField(db_column='OPN_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    kit_no = models.DecimalField(db_column='KIT_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sub_docno = models.DecimalField(db_column='SUB_DOCNO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    lieu_part = models.CharField(db_column='LIEU_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    drawn_by = models.CharField(db_column='DRAWN_BY', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    doc_no_old = models.DecimalField(db_column='DOC_NO_OLD', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M14M4_CRIS'


class M14M4N(models.Model):
    doc_code = models.CharField(db_column='DOC_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    doc_no = models.DecimalField(db_column='DOC_NO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pm_no = models.CharField(db_column='PM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    due_wk = models.CharField(db_column='DUE_WK', max_length=4, blank=True, null=True)  # Field name made lowercase.
    prtdt = models.DateField(db_column='PRTDT', blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    doc_ind = models.CharField(db_column='DOC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    stage = models.CharField(db_column='STAGE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ward_no = models.CharField(db_column='WARD_NO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    finyear = models.CharField(db_column='FINYEAR', max_length=2, blank=True, null=True)  # Field name made lowercase.
    vr_no = models.CharField(db_column='VR_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    kit_ind = models.CharField(db_column='KIT_IND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='STATION', max_length=3, blank=True, null=True)  # Field name made lowercase.
    stg = models.CharField(db_column='STG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sub_kit = models.CharField(db_column='SUB_KIT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    opn_no = models.CharField(db_column='OPN_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    kit_no = models.DecimalField(db_column='KIT_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sub_docno = models.DecimalField(db_column='SUB_DOCNO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    lieu_part = models.CharField(db_column='LIEU_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    drawn_by = models.CharField(db_column='DRAWN_BY', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    doc_no_old = models.DecimalField(db_column='DOC_NO_OLD', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M14M4_N'


class M20(models.Model):
    progress = models.CharField(db_column='PROGRESS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    yearmonth = models.CharField(db_column='YEARMONTH', max_length=4, blank=True, null=True)  # Field name made lowercase.
    nmbr = models.DecimalField(db_column='NMBR', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m20_dat = models.DateField(db_column='M20_DAT', blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qty_loco = models.DecimalField(db_column='QTY_LOCO', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    dg_loco_no = models.CharField(db_column='DG_LOCO_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    requ_no = models.CharField(db_column='REQU_NO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    indentor = models.CharField(db_column='INDENTOR', max_length=3, blank=True, null=True)  # Field name made lowercase.
    po_no = models.CharField(db_column='PO_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    po_date = models.DateField(db_column='PO_DATE', blank=True, null=True)  # Field name made lowercase.
    po_value = models.DecimalField(db_column='PO_VALUE', max_digits=13, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    alloc_head = models.CharField(db_column='ALLOC_HEAD', max_length=7, blank=True, null=True)  # Field name made lowercase.
    alloc_amt = models.DecimalField(db_column='ALLOC_AMT', max_digits=9, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    usr_cd = models.CharField(db_column='USR_CD', max_length=6, blank=True, null=True)  # Field name made lowercase.
    sel = models.CharField(db_column='SEL', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M20'


class M2Doc(models.Model):
    scl_cl = models.CharField(db_column='SCL_CL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    f_shopsec = models.CharField(db_column='F_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=16, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    rc_st_wk = models.CharField(db_column='RC_ST_WK', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rm_partno = models.CharField(db_column='RM_PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.DecimalField(db_column='RM_QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    rm_ptc = models.CharField(db_column='RM_PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cut_shear = models.CharField(db_column='CUT_SHEAR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    m2sln = models.DecimalField(db_column='M2SLN', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m2prtdt = models.DateField(db_column='M2PRTDT', blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m4_no = models.DecimalField(db_column='M4_NO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M2DOC'


class M5Doc(models.Model):
    scl_cl = models.CharField(db_column='SCL_CL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    m2slno = models.DecimalField(db_column='M2SLNO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rm_partno = models.CharField(db_column='RM_PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_ut = models.CharField(db_column='RM_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cut_shear = models.CharField(db_column='CUT_SHEAR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.DecimalField(db_column='RM_QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    shop_sec = models.CharField(db_column='SHOP_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    opn_desc = models.CharField(db_column='OPN_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pa = models.DecimalField(db_column='PA', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at = models.DecimalField(db_column='AT', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    no_off = models.DecimalField(db_column='NO_OFF', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5_cd = models.CharField(db_column='M5_CD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pr_shopsec = models.CharField(db_column='PR_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    n_shopsec = models.CharField(db_column='N_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    qty_ord = models.DecimalField(db_column='QTY_ORD', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    tot_rm_qty = models.DecimalField(db_column='TOT_RM_QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    m5glsn = models.DecimalField(db_column='M5GLSN', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5prtdt = models.DateField(db_column='M5PRTDT', blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M5DOC'


class M5Doc1(models.Model):
    scl_cl = models.CharField(db_column='SCL_CL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    m2slno = models.CharField(db_column='M2SLNO', max_length=320, blank=True, null=True)  # Field name made lowercase.
    rm_partno = models.CharField(db_column='RM_PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_ut = models.CharField(db_column='RM_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cut_shear = models.CharField(db_column='CUT_SHEAR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.CharField(db_column='RM_QTY', max_length=320, blank=True, null=True)  # Field name made lowercase.
    shop_sec = models.CharField(db_column='SHOP_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    opn_desc = models.CharField(db_column='OPN_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pa = models.CharField(db_column='PA', max_length=320, blank=True, null=True)  # Field name made lowercase.
    at = models.CharField(db_column='AT', max_length=320, blank=True, null=True)  # Field name made lowercase.
    no_off = models.CharField(db_column='NO_OFF', max_length=320, blank=True, null=True)  # Field name made lowercase.
    m5_cd = models.CharField(db_column='M5_CD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pr_shopsec = models.CharField(db_column='PR_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    n_shopsec = models.CharField(db_column='N_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    qty_ord = models.CharField(db_column='QTY_ORD', max_length=320, blank=True, null=True)  # Field name made lowercase.
    tot_rm_qty = models.CharField(db_column='TOT_RM_QTY', max_length=320, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    m5glsn = models.CharField(db_column='M5GLSN', max_length=320, blank=True, null=True)  # Field name made lowercase.
    m5prtdt = models.DateField(db_column='M5PRTDT', blank=True, null=True)  # Field name made lowercase.
    seq = models.CharField(db_column='SEQ', max_length=320, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.CharField(db_column='BRN_NO', max_length=320, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'M5DOC1'


class MfgcostProcess(models.Model):
    start_dt = models.DateField(db_column='START_DT', blank=True, null=True)  # Field name made lowercase.
    start_time = models.CharField(db_column='START_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    assly_process = models.DecimalField(db_column='ASSLY_PROCESS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    progress = models.DecimalField(db_column='PROGRESS', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    end_dt = models.DateField(db_column='END_DT', blank=True, null=True)  # Field name made lowercase.
    end_time = models.CharField(db_column='END_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MFGCOST_PROCESS'


class Misapp(models.Model):
    app_id = models.CharField(db_column='APP_ID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    app_area = models.CharField(db_column='APP_AREA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    pmodule = models.CharField(db_column='PMODULE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    module = models.CharField(db_column='MODULE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    mod_seq = models.CharField(db_column='MOD_SEQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    prgpath = models.CharField(db_column='PRGPATH', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prgfile = models.CharField(db_column='PRGFILE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    prompt = models.CharField(db_column='PROMPT', max_length=40, blank=True, null=True)  # Field name made lowercase.
    opmode = models.CharField(db_column='OPMODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    auth_by = models.CharField(db_column='AUTH_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    auth_date = models.DateField(db_column='AUTH_DATE', blank=True, null=True)  # Field name made lowercase.
    valid_upto = models.DateField(db_column='VALID_UPTO', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MISAPP'


class Misusr1(models.Model):
    usr_cd = models.CharField(db_column='USR_CD', max_length=8, blank=True, null=True)  # Field name made lowercase.
    usr_dsgn = models.CharField(db_column='USR_DSGN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    usr_name = models.CharField(db_column='USR_NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    usr_passwd = models.CharField(db_column='USR_PASSWD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    usr_level = models.CharField(db_column='USR_LEVEL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usr_boss = models.CharField(db_column='USR_BOSS', max_length=6, blank=True, null=True)  # Field name made lowercase.
    usr_group = models.CharField(db_column='USR_GROUP', max_length=6, blank=True, null=True)  # Field name made lowercase.
    usr_email = models.CharField(db_column='USR_EMAIL', max_length=30, blank=True, null=True)  # Field name made lowercase.
    app_id = models.CharField(db_column='APP_ID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    app_area = models.CharField(db_column='APP_AREA', max_length=3, blank=True, null=True)  # Field name made lowercase.
    usr_status = models.CharField(db_column='USR_STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    usr_flag = models.CharField(db_column='USR_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    quest_hint = models.CharField(db_column='QUEST_HINT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ans_hint = models.CharField(db_column='ANS_HINT', max_length=40, blank=True, null=True)  # Field name made lowercase.
    staff_no = models.CharField(db_column='STAFF_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MISUSR_1'


class Misusr2(models.Model):
    usr_cd = models.CharField(db_column='USR_CD', max_length=8, blank=True, null=True)  # Field name made lowercase.
    usr_level = models.CharField(db_column='USR_LEVEL', max_length=2, blank=True, null=True)  # Field name made lowercase.
    usr_sec = models.CharField(db_column='USR_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MISUSR_2'


class Misusr3(models.Model):
    usr_cd = models.CharField(db_column='USR_CD', max_length=8, blank=True, null=True)  # Field name made lowercase.
    app_id = models.CharField(db_column='APP_ID', max_length=4, blank=True, null=True)  # Field name made lowercase.
    module = models.CharField(db_column='MODULE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    mod_seq = models.CharField(db_column='MOD_SEQ', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mode = models.CharField(db_column='MODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MISUSR_3'


class Mktp15(models.Model):
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    desc = models.CharField(db_column='DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    stk_rate = models.DecimalField(db_column='STK_RATE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    stk_ut = models.CharField(db_column='STK_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    po_rate = models.DecimalField(db_column='PO_RATE', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    po_ut = models.CharField(db_column='PO_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    po_no = models.CharField(db_column='PO_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    po_date = models.DateField(db_column='PO_DATE', blank=True, null=True)  # Field name made lowercase.
    mat_cost = models.DecimalField(db_column='MAT_COST', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    dlab_cost = models.DecimalField(db_column='DLAB_COST', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    tinc_bons = models.CharField(db_column='TINC_BONS', max_length=320, blank=True, null=True)  # Field name made lowercase.
    foh_cost = models.DecimalField(db_column='FOH_COST', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    toh_cost = models.DecimalField(db_column='TOH_COST', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    aoh_cost = models.DecimalField(db_column='AOH_COST', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mfg_cost = models.DecimalField(db_column='MFG_COST', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    ind_chrg = models.DecimalField(db_column='IND_CHRG', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    dep_chrg = models.DecimalField(db_column='DEP_CHRG', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pro_chrg = models.DecimalField(db_column='PRO_CHRG', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rly_cost = models.DecimalField(db_column='RLY_COST', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    tot_time = models.DecimalField(db_column='TOT_TIME', max_digits=7, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mkt_pric_c = models.DecimalField(db_column='MKT_PRIC_C', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mkt_pric_p = models.DecimalField(db_column='MKT_PRIC_P', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mkt_price = models.DecimalField(db_column='MKT_PRICE', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    basic_rate = models.DecimalField(db_column='BASIC_RATE', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    diff_perc = models.DecimalField(db_column='DIFF_PERC', max_digits=7, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_loco = models.DecimalField(db_column='QTY_LOCO', max_digits=7, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rate_basis = models.CharField(db_column='RATE_BASIS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    soh_chrg = models.DecimalField(db_column='SOH_CHRG', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rem = models.CharField(db_column='REM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MKTP15'


class MmmProduct(models.Model):
    rly = models.CharField(db_column='RLY', max_length=2, blank=True, null=True)  # Field name made lowercase.
    product_code = models.CharField(db_column='PRODUCT_CODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    product_descr = models.CharField(db_column='PRODUCT_DESCR', max_length=70, blank=True, null=True)  # Field name made lowercase.
    product_type = models.CharField(db_column='PRODUCT_TYPE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    flag1 = models.CharField(db_column='FLAG1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag2 = models.CharField(db_column='FLAG2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cataegory = models.CharField(db_column='CATAEGORY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rb_product_code = models.CharField(db_column='RB_PRODUCT_CODE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    product_alias = models.CharField(db_column='PRODUCT_ALIAS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    conv_factor = models.DecimalField(db_column='CONV_FACTOR', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    active = models.CharField(db_column='ACTIVE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    auth_seq = models.DecimalField(db_column='AUTH_SEQ', max_digits=12, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    product_subtype = models.CharField(db_column='PRODUCT_SUBTYPE', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MMM_PRODUCT'


class Mnp(models.Model):
    mwno = models.CharField(db_column='MWNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    maint_area = models.CharField(db_column='MAINT_AREA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    bay = models.CharField(db_column='BAY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mw_cat = models.CharField(db_column='MW_CAT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    shopsec = models.CharField(db_column='SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    sh_name = models.CharField(db_column='SH_NAME', max_length=5, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    no_shift = models.DecimalField(db_column='NO_SHIFT', max_digits=1, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=15, blank=True, null=True)  # Field name made lowercase.
    dt_of_comm = models.DateField(db_column='DT_OF_COMM', blank=True, null=True)  # Field name made lowercase.
    make = models.CharField(db_column='MAKE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    eqp_type = models.CharField(db_column='EQP_TYPE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    mc_type_gr = models.CharField(db_column='MC_TYPE_GR', max_length=30, blank=True, null=True)  # Field name made lowercase.
    used_for = models.CharField(db_column='USED_FOR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cost = models.DecimalField(db_column='COST', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    available = models.CharField(db_column='AVAILABLE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    condition = models.CharField(db_column='CONDITION', max_length=100, blank=True, null=True)  # Field name made lowercase.
    replace_by = models.DecimalField(db_column='REPLACE_BY', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    date_tr_c = models.DateField(db_column='DATE_TR_C', blank=True, null=True)  # Field name made lowercase.
    capacity = models.CharField(db_column='CAPACITY', max_length=10, blank=True, null=True)  # Field name made lowercase.
    required = models.CharField(db_column='REQUIRED', max_length=9, blank=True, null=True)  # Field name made lowercase.
    yr_scrap = models.DateField(db_column='YR_SCRAP', blank=True, null=True)  # Field name made lowercase.
    load_cente = models.CharField(db_column='LOAD_CENTE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cat_code = models.CharField(db_column='CAT_CODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MNP'


class MnpBd(models.Model):
    mwno = models.CharField(db_column='MWNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    bd_slno = models.DecimalField(db_column='BD_SLNO', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    bd_date = models.DateField(db_column='BD_DATE', blank=True, null=True)  # Field name made lowercase.
    bd_time = models.CharField(db_column='BD_TIME', max_length=8, blank=True, null=True)  # Field name made lowercase.
    maint_area = models.CharField(db_column='MAINT_AREA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=4, blank=True, null=True)  # Field name made lowercase.
    bay = models.CharField(db_column='BAY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mw_cat = models.CharField(db_column='MW_CAT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    priority = models.CharField(db_column='PRIORITY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pdc = models.DateField(db_column='PDC', blank=True, null=True)  # Field name made lowercase.
    ready_date = models.DateField(db_column='READY_DATE', blank=True, null=True)  # Field name made lowercase.
    ready_time = models.CharField(db_column='READY_TIME', max_length=8, blank=True, null=True)  # Field name made lowercase.
    lost_hrs = models.DecimalField(db_column='LOST_HRS', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(db_column='NOTES', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    repo_to = models.CharField(db_column='REPO_TO', max_length=6, blank=True, null=True)  # Field name made lowercase.
    bd_by = models.CharField(db_column='BD_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    ready_by = models.CharField(db_column='READY_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    mnp_staff = models.CharField(db_column='MNP_STAFF', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shop_staff = models.CharField(db_column='SHOP_STAFF', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shopsec = models.CharField(db_column='SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    next_act = models.CharField(db_column='NEXT_ACT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    next_date = models.DateField(db_column='NEXT_DATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MNP_BD'


class Mp(models.Model):
    shop_sec = models.CharField(db_column='SHOP_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lcno = models.CharField(db_column='LCNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mwno = models.CharField(db_column='MWNO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    mc_gr = models.CharField(db_column='MC_GR', max_length=2, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MP'


class Ngr(models.Model):
    mgr = models.CharField(db_column='MGR', max_length=2, blank=True, null=True)  # Field name made lowercase.
    sgr1 = models.CharField(db_column='SGR1', max_length=2, blank=True, null=True)  # Field name made lowercase.
    sgr2 = models.CharField(db_column='SGR2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    gdes = models.CharField(db_column='GDES', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    sln = models.DecimalField(db_column='SLN', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    cnt = models.DecimalField(db_column='CNT', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NGR'


class Nstr(models.Model):
    pp_part = models.CharField(db_column='PP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cp_part = models.CharField(db_column='CP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    ref_ind = models.CharField(db_column='REF_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ref_no = models.CharField(db_column='REF_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    lead_time = models.DecimalField(db_column='LEAD_TIME', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    reg_no = models.CharField(db_column='REG_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NSTR'


class Nstrlog(models.Model):
    pp_part = models.CharField(db_column='PP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cp_part = models.CharField(db_column='CP_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    edp_cn_no = models.CharField(db_column='EDP_CN_NO', max_length=6, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NSTRLOG'


class OpnExt(models.Model):
    asm_no = models.CharField(db_column='ASM_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ref_ind = models.CharField(db_column='REF_IND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    dlw_ref_no = models.CharField(db_column='DLW_REF_NO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ref_desc = models.CharField(db_column='REF_DESC', max_length=40, blank=True, null=True)  # Field name made lowercase.
    dlw_plno = models.CharField(db_column='DLW_PLNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mfg = models.CharField(db_column='MFG', max_length=8, blank=True, null=True)  # Field name made lowercase.
    mfg_ref_no = models.CharField(db_column='MFG_REF_NO', max_length=25, blank=True, null=True)  # Field name made lowercase.
    comb_cd = models.CharField(db_column='COMB_CD', max_length=2, blank=True, null=True)  # Field name made lowercase.
    alt_cd = models.CharField(db_column='ALT_CD', max_length=2, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    ref_desc_m = models.CharField(db_column='REF_DESC_M', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPN_EXT'


class OpnPart(models.Model):
    asm_no = models.CharField(db_column='ASM_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ref_asmno = models.CharField(db_column='REF_ASMNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ref_itno = models.CharField(db_column='REF_ITNO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    mb = models.CharField(db_column='MB', max_length=1, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    kit_ind = models.CharField(db_column='KIT_IND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'OPN_PART'


class Oprn(models.Model):
    shop_sec = models.CharField(db_column='SHOP_SEC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=10, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    pa_hrs = models.DecimalField(db_column='PA_HRS', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at_hrs = models.DecimalField(db_column='AT_HRS', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pa = models.DecimalField(db_column='PA', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at = models.DecimalField(db_column='AT', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lot = models.DecimalField(db_column='LOT', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ncp_jbs = models.CharField(db_column='NCP_JBS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    m5_cd = models.CharField(db_column='M5_CD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=5, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    m_1 = models.DecimalField(db_column='M_1', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    c_1 = models.CharField(db_column='C_1', max_length=5, blank=True, null=True)  # Field name made lowercase.
    m_2 = models.DecimalField(db_column='M_2', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    c_2_field = models.CharField(db_column='C_2_', max_length=5, blank=True, null=True)  # Field name made lowercase. Field renamed because it ended with '_'.
    m_3 = models.DecimalField(db_column='M_3', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    c_3 = models.CharField(db_column='C_3', max_length=5, blank=True, null=True)  # Field name made lowercase.
    m5_cd_old = models.CharField(db_column='M5_CD_OLD', max_length=5, blank=True, null=True)  # Field name made lowercase.
    at_old = models.DecimalField(db_column='AT_OLD', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at310899 = models.DecimalField(db_column='AT310899', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lot310899 = models.DecimalField(db_column='LOT310899', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    at_old1 = models.DecimalField(db_column='AT_OLD1', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at_min = models.DecimalField(db_column='AT_MIN', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    at_min_rou = models.DecimalField(db_column='AT_MIN_ROU', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    at011209 = models.DecimalField(db_column='AT011209', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at_hrs1 = models.DecimalField(db_column='AT_HRS1', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    lot011209 = models.DecimalField(db_column='LOT011209', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    o_at = models.DecimalField(db_column='O_AT', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    o_at_min = models.DecimalField(db_column='O_AT_MIN', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rmin = models.DecimalField(db_column='RMIN', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rb = models.DecimalField(db_column='RB', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rat_hr = models.DecimalField(db_column='RAT_HR', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rat = models.DecimalField(db_column='RAT', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    mat_rej = models.IntegerField(db_column='MAT_REJ', blank=True, null=True)  # Field name made lowercase.
    qtr_accep = models.IntegerField(db_column='QTR_ACCEP', blank=True, null=True)  # Field name made lowercase.
    qty_prod = models.IntegerField(db_column='QTY_PROD', blank=True, null=True)  # Field name made lowercase.
    work_rej = models.IntegerField(db_column='WORK_REJ', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'OPRN'


class Part(models.Model):
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    drgno = models.CharField(db_column='DRGNO', max_length=18, blank=True, null=True)  # Field name made lowercase.
    drg_alt = models.CharField(db_column='DRG_ALT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    spec = models.CharField(db_column='SPEC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    size_m = models.CharField(db_column='SIZE_M', max_length=30, blank=True, null=True)  # Field name made lowercase.
    weight = models.DecimalField(db_column='WEIGHT', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    m14splt_cd = models.CharField(db_column='M14SPLT_CD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    allow_perc = models.DecimalField(db_column='ALLOW_PERC', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rate = models.DecimalField(db_column='RATE', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    rate_date = models.DateField(db_column='RATE_DATE', blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    part_grp = models.CharField(db_column='PART_GRP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    flag_hw = models.CharField(db_column='FLAG_HW', max_length=2, blank=True, null=True)  # Field name made lowercase.
    m14_flag = models.CharField(db_column='M14_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    u_f = models.CharField(db_column='U_F', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PART'


class Partalt(models.Model):
    epc = models.CharField(db_column='EPC', max_length=5, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    drgno = models.CharField(db_column='DRGNO', max_length=18, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    cost_ind = models.CharField(db_column='COST_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PARTALT'


class Partdrg(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    drg_no = models.CharField(db_column='DRG_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    drg_alt = models.CharField(db_column='DRG_ALT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    drg_ind = models.CharField(db_column='DRG_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    drg_dir = models.CharField(db_column='DRG_DIR', max_length=15, blank=True, null=True)  # Field name made lowercase.
    drg_file = models.CharField(db_column='DRG_FILE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    updt_by = models.CharField(db_column='UPDT_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    lupd_dt = models.DateField(db_column='LUPD_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PARTDRG'


class Partgrp(models.Model):
    maj_grp = models.CharField(db_column='MAJ_GRP', max_length=2, blank=True, null=True)  # Field name made lowercase.
    sub_grp = models.CharField(db_column='SUB_GRP', max_length=2, blank=True, null=True)  # Field name made lowercase.
    slno = models.DecimalField(db_column='SLNO', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    maj_descr = models.CharField(db_column='MAJ_DESCR', max_length=30, blank=True, null=True)  # Field name made lowercase.
    sub_descr = models.CharField(db_column='SUB_DESCR', max_length=60, blank=True, null=True)  # Field name made lowercase.
    missing1 = models.DecimalField(db_column='MISSING1', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PARTGRP'


class Partmast(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    drgno = models.CharField(db_column='DRGNO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    drg_alt = models.CharField(db_column='DRG_ALT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    drp = models.CharField(db_column='DRP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cat_no = models.CharField(db_column='CAT_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    spec = models.CharField(db_column='SPEC', max_length=25, blank=True, null=True)  # Field name made lowercase.
    size_m = models.CharField(db_column='SIZE_M', max_length=30, blank=True, null=True)  # Field name made lowercase.
    weight = models.DecimalField(db_column='WEIGHT', max_digits=11, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    enduse = models.CharField(db_column='ENDUSE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    loco_type = models.CharField(db_column='LOCO_TYPE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cd_ind = models.CharField(db_column='CD_IND', max_length=4, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    open_by = models.CharField(db_column='OPEN_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    open_date = models.DateField(db_column='OPEN_DATE', blank=True, null=True)  # Field name made lowercase.
    updt_by = models.CharField(db_column='UPDT_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PARTMAST'


class Partnew(models.Model):
    gm_ptno = models.CharField(db_column='GM_PTNO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    old_rev = models.CharField(db_column='OLD_REV', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rev = models.CharField(db_column='REV', max_length=5, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mb = models.CharField(db_column='MB', max_length=2, blank=True, null=True)  # Field name made lowercase.
    it_cat = models.CharField(db_column='IT_CAT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ind_buy = models.CharField(db_column='IND_BUY', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cls = models.CharField(db_column='CLS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cls_eng = models.CharField(db_column='CLS_ENG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(db_column='UM', max_length=2, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    stk_um = models.CharField(db_column='STK_UM', max_length=2, blank=True, null=True)  # Field name made lowercase.
    stk_um_des = models.CharField(db_column='STK_UM_DES', max_length=8, blank=True, null=True)  # Field name made lowercase.
    um_eng = models.CharField(db_column='UM_ENG', max_length=2, blank=True, null=True)  # Field name made lowercase.
    um_cd_dlw = models.CharField(db_column='UM_CD_DLW', max_length=2, blank=True, null=True)  # Field name made lowercase.
    umdes_dlw = models.CharField(db_column='UMDES_DLW', max_length=10, blank=True, null=True)  # Field name made lowercase.
    conv_fact = models.DecimalField(db_column='CONV_FACT', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    wt_p_pc = models.DecimalField(db_column='WT_P_PC', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    unit_wt = models.CharField(db_column='UNIT_WT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    size_pc = models.CharField(db_column='SIZE_PC', max_length=25, blank=True, null=True)  # Field name made lowercase.
    mat_specn = models.CharField(db_column='MAT_SPECN', max_length=55, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='REMARKS', max_length=200, blank=True, null=True)  # Field name made lowercase.
    old_part = models.CharField(db_column='OLD_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    old_desc = models.CharField(db_column='OLD_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dlw_flag = models.CharField(db_column='DLW_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='STATION', max_length=2, blank=True, null=True)  # Field name made lowercase.
    newfield = models.CharField(db_column='NEWFIELD', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PARTNEW'


class Partnew1(models.Model):
    gm_ptno = models.CharField(db_column='GM_PTNO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    old_rev = models.CharField(db_column='OLD_REV', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rev = models.CharField(db_column='REV', max_length=5, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mb = models.CharField(db_column='MB', max_length=2, blank=True, null=True)  # Field name made lowercase.
    it_cat = models.CharField(db_column='IT_CAT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ind_buy = models.CharField(db_column='IND_BUY', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cls = models.CharField(db_column='CLS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cls_eng = models.CharField(db_column='CLS_ENG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    um = models.CharField(db_column='UM', max_length=2, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    stk_um = models.CharField(db_column='STK_UM', max_length=2, blank=True, null=True)  # Field name made lowercase.
    stk_um_des = models.CharField(db_column='STK_UM_DES', max_length=8, blank=True, null=True)  # Field name made lowercase.
    um_eng = models.CharField(db_column='UM_ENG', max_length=2, blank=True, null=True)  # Field name made lowercase.
    um_cd_dlw = models.CharField(db_column='UM_CD_DLW', max_length=2, blank=True, null=True)  # Field name made lowercase.
    umdes_dlw = models.CharField(db_column='UMDES_DLW', max_length=10, blank=True, null=True)  # Field name made lowercase.
    conv_fact = models.DecimalField(db_column='CONV_FACT', max_digits=9, decimal_places=4, blank=True, null=True)  # Field name made lowercase.
    wt_p_pc = models.DecimalField(db_column='WT_P_PC', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    unit_wt = models.CharField(db_column='UNIT_WT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    size_pc = models.CharField(db_column='SIZE_PC', max_length=25, blank=True, null=True)  # Field name made lowercase.
    mat_specn = models.CharField(db_column='MAT_SPECN', max_length=55, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    remarks = models.CharField(db_column='REMARKS', max_length=100, blank=True, null=True)  # Field name made lowercase.
    old_part = models.CharField(db_column='OLD_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    old_desc = models.CharField(db_column='OLD_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dlw_flag = models.CharField(db_column='DLW_FLAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='STATION', max_length=2, blank=True, null=True)  # Field name made lowercase.
    newfield = models.CharField(db_column='NEWFIELD', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PARTNEW1'


class Plant(models.Model):
    unit = models.CharField(db_column='UNIT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    plant = models.CharField(db_column='PLANT', max_length=5, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    add1 = models.CharField(db_column='ADD1', max_length=40, blank=True, null=True)  # Field name made lowercase.
    add2 = models.CharField(db_column='ADD2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    add3 = models.CharField(db_column='ADD3', max_length=45, blank=True, null=True)  # Field name made lowercase.
    add4 = models.CharField(db_column='ADD4', max_length=45, blank=True, null=True)  # Field name made lowercase.
    add5 = models.CharField(db_column='ADD5', max_length=45, blank=True, null=True)  # Field name made lowercase.
    attn = models.CharField(db_column='ATTN', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PLANT'


class Proddem(models.Model):
    dem_regno = models.CharField(db_column='DEM_REGNO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    dem_date = models.DateField(db_column='DEM_DATE', blank=True, null=True)  # Field name made lowercase.
    dem_senddt = models.DateField(db_column='DEM_SENDDT', blank=True, null=True)  # Field name made lowercase.
    dep = models.CharField(db_column='DEP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    batch_type = models.CharField(db_column='BATCH_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    week_no = models.DecimalField(db_column='WEEK_NO', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m2 = models.CharField(db_column='M2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    m4 = models.CharField(db_column='M4', max_length=1, blank=True, null=True)  # Field name made lowercase.
    m5 = models.CharField(db_column='M5', max_length=1, blank=True, null=True)  # Field name made lowercase.
    m14 = models.CharField(db_column='M14', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dem_others = models.CharField(db_column='DEM_OTHERS', max_length=30, blank=True, null=True)  # Field name made lowercase.
    process_dt = models.DateField(db_column='PROCESS_DT', blank=True, null=True)  # Field name made lowercase.
    loading_dt = models.DateField(db_column='LOADING_DT', blank=True, null=True)  # Field name made lowercase.
    print_dt = models.DateField(db_column='PRINT_DT', blank=True, null=True)  # Field name made lowercase.
    issue_dt = models.DateField(db_column='ISSUE_DT', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=30, blank=True, null=True)  # Field name made lowercase.
    staff_no = models.CharField(db_column='STAFF_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=20, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    ddoc_type = models.CharField(db_column='DDOC_TYPE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    m2_fr = models.DecimalField(db_column='M2_FR', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m2_to = models.DecimalField(db_column='M2_TO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5_fr = models.DecimalField(db_column='M5_FR', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5_to = models.DecimalField(db_column='M5_TO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m4_fr = models.DecimalField(db_column='M4_FR', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m4_to = models.DecimalField(db_column='M4_TO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m14_fr = models.DecimalField(db_column='M14_FR', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m14_to = models.DecimalField(db_column='M14_TO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PRODDEM'


class Prodplan(models.Model):
    rev_no = models.CharField(db_column='REV_NO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    yyyymm = models.CharField(db_column='YYYYMM', max_length=6, blank=True, null=True)  # Field name made lowercase.
    loco = models.CharField(db_column='LOCO', max_length=6, blank=True, null=True)  # Field name made lowercase.
    target = models.DecimalField(db_column='TARGET', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    outturn = models.DecimalField(db_column='OUTTURN', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    loco_no = models.CharField(db_column='LOCO_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PRODPLAN'


class Progpart(models.Model):
    pm_no = models.CharField(db_column='PM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    auth_qty = models.DecimalField(db_column='AUTH_QTY', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    auth_qty1 = models.DecimalField(db_column='AUTH_QTY1', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    old_pm_no = models.CharField(db_column='OLD_PM_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    old_pmno = models.CharField(db_column='OLD_PMNO', max_length=4, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PROGPART'


class Ptld(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    p_desc = models.CharField(db_column='P_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rem = models.CharField(db_column='REM', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PTLD'


class Qppextra(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    qty_eng = models.DecimalField(db_column='QTY_ENG', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bi_ind = models.CharField(db_column='BI_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QPPEXTRA'


class Qppn(models.Model):
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=40, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=8, blank=True, null=True)  # Field name made lowercase.
    spl_ind = models.CharField(db_column='SPL_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bqty = models.DecimalField(db_column='BQTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QPPN'


class Qpptempqpa(models.Model):
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    bqty = models.CharField(db_column='BQTY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    spl_ind = models.CharField(db_column='SPL_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bi_ind = models.CharField(db_column='BI_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QPPTEMPQPA'


class Qpptempsum(models.Model):
    spl_ind = models.CharField(db_column='SPL_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=14, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QPPTEMPSUM'


class Qppx(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qty_eng = models.DecimalField(db_column='QTY_ENG', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qty_db = models.DecimalField(db_column='QTY_DB', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bi_ind = models.CharField(db_column='BI_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    issue_upto = models.CharField(db_column='ISSUE_UPTO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QPPX'


class QppProducts(models.Model):
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=6, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=2, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=6, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QPP_PRODUCTS'


class QppTempalt1(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_link = models.DecimalField(db_column='ALT_LINK', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QPP_TEMPALT1'


class QppTempalt2(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    qty_eng = models.DecimalField(db_column='QTY_ENG', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QPP_TEMPALT2'


class QppTempalt3(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    qty_eng = models.DecimalField(db_column='QTY_ENG', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QPP_TEMPALT3'


class QppTempqpp(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    prod_type = models.CharField(db_column='PROD_TYPE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    qty_eng = models.DecimalField(db_column='QTY_ENG', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    bi_ind = models.CharField(db_column='BI_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_ind = models.CharField(db_column='ALT_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QPP_TEMPQPP'


class QtysumTemp(models.Model):
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ptlf = models.CharField(db_column='PTLF', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ptlt = models.CharField(db_column='PTLT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rm_part = models.CharField(db_column='RM_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_ptc = models.CharField(db_column='RM_PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.DecimalField(db_column='RM_QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rm_ut = models.CharField(db_column='RM_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rmlf = models.CharField(db_column='RMLF', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rmlt = models.CharField(db_column='RMLT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=10, blank=True, null=True)  # Field name made lowercase.
    qty_loco = models.CharField(db_column='QTY_LOCO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dt_run = models.DateField(db_column='DT_RUN', blank=True, null=True)  # Field name made lowercase.
    cur_time = models.CharField(db_column='CUR_TIME', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QTYSUM_TEMP'


class QtysumTemp1(models.Model):
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rm_part = models.CharField(db_column='RM_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_ptc = models.CharField(db_column='RM_PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.DecimalField(db_column='RM_QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rm_ut = models.CharField(db_column='RM_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rm_lf = models.CharField(db_column='RM_LF', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rm_lt = models.CharField(db_column='RM_LT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    dt_run = models.DateField(db_column='DT_RUN', blank=True, null=True)  # Field name made lowercase.
    cur_time = models.CharField(db_column='CUR_TIME', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QTYSUM_TEMP1'


class QtysumTemp2(models.Model):
    partno = models.CharField(db_column='PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    pt_lf = models.CharField(db_column='PT_LF', max_length=4, blank=True, null=True)  # Field name made lowercase.
    pt_lt = models.CharField(db_column='PT_LT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rm_part = models.CharField(db_column='RM_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_ptc = models.CharField(db_column='RM_PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.DecimalField(db_column='RM_QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    rm_ut = models.CharField(db_column='RM_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    rm_lf = models.CharField(db_column='RM_LF', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rm_lt = models.CharField(db_column='RM_LT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    dt_run = models.DateField(db_column='DT_RUN', blank=True, null=True)  # Field name made lowercase.
    cur_time = models.CharField(db_column='CUR_TIME', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'QTYSUM_TEMP2'


class Rate(models.Model):
    aoh_rate = models.DecimalField(db_column='AOH_RATE', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    toh_rate = models.DecimalField(db_column='TOH_RATE', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    soh_rate = models.DecimalField(db_column='SOH_RATE', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    dep_rate = models.DecimalField(db_column='DEP_RATE', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ind_rate = models.DecimalField(db_column='IND_RATE', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pro_rate = models.DecimalField(db_column='PRO_RATE', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    avg_bon = models.DecimalField(db_column='AVG_BON', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RATE'


class Refdoc(models.Model):
    drgno = models.CharField(db_column='DRGNO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    ref_ind = models.CharField(db_column='REF_IND', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ref_no = models.CharField(db_column='REF_NO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    recd_yn = models.CharField(db_column='RECD_YN', max_length=1, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=6, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REFDOC'


class ReqRegi(models.Model):
    cos_caseno = models.CharField(db_column='COS_CASENO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    reg_no = models.CharField(db_column='REG_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    a_c_d = models.CharField(db_column='A_C_D', max_length=1, blank=True, null=True)  # Field name made lowercase.
    req_no = models.CharField(db_column='REQ_NO', max_length=25, blank=True, null=True)  # Field name made lowercase.
    req_date = models.DateField(db_column='REQ_DATE', blank=True, null=True)  # Field name made lowercase.
    req_detail = models.CharField(db_column='REQ_DETAIL', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    fund_requr = models.DecimalField(db_column='FUND_REQUR', max_digits=9, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dept_code = models.CharField(db_column='DEPT_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    sub_dep_cd = models.CharField(db_column='SUB_DEP_CD', max_length=2, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    del_ref = models.CharField(db_column='DEL_REF', max_length=15, blank=True, null=True)  # Field name made lowercase.
    del_date = models.DateField(db_column='DEL_DATE', blank=True, null=True)  # Field name made lowercase.
    change_ref = models.CharField(db_column='CHANGE_REF', max_length=15, blank=True, null=True)  # Field name made lowercase.
    chg_date = models.DateField(db_column='CHG_DATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REQ_REGI'


class Rlyshed(models.Model):
    bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    consignee = models.CharField(db_column='CONSIGNEE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    railway = models.CharField(db_column='RAILWAY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shed = models.CharField(db_column='SHED', max_length=10, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RLYSHED'


class Schdesc(models.Model):
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SCHDESC'


class Setmast(models.Model):
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    set_part = models.CharField(db_column='SET_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    set_qty = models.DecimalField(db_column='SET_QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    valid_from = models.DateField(db_column='VALID_FROM', blank=True, null=True)  # Field name made lowercase.
    valid_upto = models.DateField(db_column='VALID_UPTO', blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc_old = models.CharField(db_column='EPC_OLD', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SETMAST'


class Shemp(models.Model):
    yymm = models.CharField(db_column='YYMM', max_length=4, blank=True, null=True)  # Field name made lowercase.
    shopsec = models.CharField(db_column='SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    staff_no = models.CharField(db_column='STAFF_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desgn = models.CharField(db_column='DESGN', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cat = models.CharField(db_column='CAT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    emp_type = models.CharField(db_column='EMP_TYPE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    updt_by = models.CharField(db_column='UPDT_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    updt_date = models.DateField(db_column='UPDT_DATE', blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SHEMP'


class Shop(models.Model):
    shop = models.CharField(db_column='SHOP', max_length=4, blank=True, null=True)  # Field name made lowercase.
    sh_desc = models.CharField(db_column='SH_DESC', max_length=5, blank=True, null=True)  # Field name made lowercase.
    shop_ldt = models.DecimalField(db_column='SHOP_LDT', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    div = models.CharField(db_column='DIV', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cat_02 = models.DecimalField(db_column='CAT_02', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cat1 = models.CharField(db_column='CAT1', max_length=3, blank=True, null=True)  # Field name made lowercase.
    lr1 = models.DecimalField(db_column='LR1', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cat2 = models.CharField(db_column='CAT2', max_length=3, blank=True, null=True)  # Field name made lowercase.
    lr2 = models.DecimalField(db_column='LR2', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cat3 = models.CharField(db_column='CAT3', max_length=3, blank=True, null=True)  # Field name made lowercase.
    lr3 = models.DecimalField(db_column='LR3', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cat4 = models.CharField(db_column='CAT4', max_length=3, blank=True, null=True)  # Field name made lowercase.
    lr4 = models.DecimalField(db_column='LR4', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    avg_inc_er = models.DecimalField(db_column='AVG_INC_ER', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    cat5 = models.CharField(db_column='CAT5', max_length=3, blank=True, null=True)  # Field name made lowercase.
    lr5 = models.DecimalField(db_column='LR5', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ovhd_perc = models.DecimalField(db_column='OVHD_PERC', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=30, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    old_incer = models.DecimalField(db_column='OLD_INCER', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SHOP'


class Sppart(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dimension = models.CharField(db_column='DIMENSION', max_length=20, blank=True, null=True)  # Field name made lowercase.
    used_mc1 = models.CharField(db_column='USED_MC1', max_length=4, blank=True, null=True)  # Field name made lowercase.
    used_mc2 = models.CharField(db_column='USED_MC2', max_length=4, blank=True, null=True)  # Field name made lowercase.
    used_mc3 = models.CharField(db_column='USED_MC3', max_length=4, blank=True, null=True)  # Field name made lowercase.
    used_mc4 = models.CharField(db_column='USED_MC4', max_length=4, blank=True, null=True)  # Field name made lowercase.
    used_ge_mc = models.CharField(db_column='USED_GE_MC', max_length=5, blank=True, null=True)  # Field name made lowercase.
    reord_qty = models.DecimalField(db_column='REORD_QTY', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    availa_qty = models.DecimalField(db_column='AVAILA_QTY', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    shop_ut = models.CharField(db_column='SHOP_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    open_by = models.CharField(db_column='OPEN_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    open_date = models.DateField(db_column='OPEN_DATE', blank=True, null=True)  # Field name made lowercase.
    updt_by = models.CharField(db_column='UPDT_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    a_qty_updt = models.DateField(db_column='A_QTY_UPDT', blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPPART'


class Spptgrp(models.Model):
    maj_grp = models.CharField(db_column='MAJ_GRP', max_length=2, blank=True, null=True)  # Field name made lowercase.
    slno = models.DecimalField(db_column='SLNO', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    maj_descr = models.CharField(db_column='MAJ_DESCR', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SPPTGRP'


class Tally1(models.Model):
    sl_no = models.CharField(db_column='SL_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    descr = models.CharField(db_column='DESCR', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TALLY_1'


class Tally2(models.Model):
    sl_no = models.CharField(db_column='SL_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    sl_no_old = models.CharField(db_column='SL_NO_OLD', max_length=4, blank=True, null=True)  # Field name made lowercase.
    part_no_ol = models.CharField(db_column='PART_NO_OL', max_length=8, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TALLY_2'


class Tempcstr(models.Model):
    part = models.CharField(db_column='PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    child = models.CharField(db_column='CHILD', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dt_time = models.CharField(db_column='DT_TIME', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEMPCSTR'


class Tempexplsum(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    rm_partno = models.CharField(db_column='RM_PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.DecimalField(db_column='RM_QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    rm_ptc = models.CharField(db_column='RM_PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEMPEXPLSUM'


class Tempm14M4(models.Model):
    doc_code = models.CharField(db_column='DOC_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    doc_no = models.DecimalField(db_column='DOC_NO', max_digits=50, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rm_part = models.CharField(db_column='RM_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    pm_no = models.CharField(db_column='PM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    due_wk = models.CharField(db_column='DUE_WK', max_length=4, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    doc_ind = models.CharField(db_column='DOC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEMPM14_M4'


class Tempsummary1(models.Model):
    cat = models.CharField(db_column='CAT', max_length=3, blank=True, null=True)  # Field name made lowercase.
    dw = models.DecimalField(db_column='DW', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    eiw = models.DecimalField(db_column='EIW', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    ni = models.DecimalField(db_column='NI', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    lr = models.DecimalField(db_column='LR', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    sup = models.DecimalField(db_column='SUP', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEMPSUMMARY1'


class TempExpl(models.Model):
    sln = models.CharField(db_column='SLN', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lvl = models.CharField(db_column='LVL', max_length=20, blank=True, null=True)  # Field name made lowercase.
    pp = models.CharField(db_column='PP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cp = models.CharField(db_column='CP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    lfr = models.CharField(db_column='LFR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lto = models.CharField(db_column='LTO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    wt = models.DecimalField(db_column='WT', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    cut = models.CharField(db_column='CUT', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rem = models.CharField(db_column='REM', max_length=6, blank=True, null=True)  # Field name made lowercase.
    ut = models.CharField(db_column='UT', max_length=8, blank=True, null=True)  # Field name made lowercase.
    stut = models.CharField(db_column='STUT', max_length=4, blank=True, null=True)  # Field name made lowercase.
    allowp = models.DecimalField(db_column='ALLOWP', max_digits=6, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    dttym = models.DateField(db_column='DTTYM', blank=True, null=True)  # Field name made lowercase.
    curtym = models.CharField(db_column='CURTYM', max_length=40, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEMP_EXPL'


class TempJbs(models.Model):
    pp = models.CharField(db_column='PP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    cp = models.CharField(db_column='CP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    a_ind = models.CharField(db_column='A_IND', max_length=8, blank=True, null=True)  # Field name made lowercase.
    a_link = models.DecimalField(db_column='A_LINK', max_digits=8, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    a_part = models.CharField(db_column='A_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    time = models.CharField(db_column='TIME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dttym = models.DateField(db_column='DTTYM', blank=True, null=True)  # Field name made lowercase.
    curtym = models.CharField(db_column='CURTYM', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sl = models.DecimalField(db_column='SL', max_digits=4, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEMP_JBS'


# class TempM14M4(models.Model):
#     doc_code = models.CharField(db_column='DOC_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
#     pm_no = models.CharField(db_column='PM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
#     rm_part = models.CharField(db_column='RM_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
#     part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
#     qty = models.DecimalField(db_column='QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
#     l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
#     l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
#     bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
#     assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
#     seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     due_wk = models.CharField(db_column='DUE_WK', max_length=4, blank=True, null=True)  # Field name made lowercase.
#     brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
#     epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
#     doc_ind = models.CharField(db_column='DOC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'TEMP_M14M4'


class TempM5Doc(models.Model):
    scl_cl = models.CharField(db_column='SCL_CL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    m2slno = models.DecimalField(db_column='M2SLNO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rm_partno = models.CharField(db_column='RM_PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_ut = models.CharField(db_column='RM_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cut_shear = models.CharField(db_column='CUT_SHEAR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.DecimalField(db_column='RM_QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    shop_sec = models.CharField(db_column='SHOP_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    opn_desc = models.CharField(db_column='OPN_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pa = models.DecimalField(db_column='PA', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at = models.DecimalField(db_column='AT', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    no_off = models.DecimalField(db_column='NO_OFF', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5_cd = models.CharField(db_column='M5_CD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pr_shopsec = models.CharField(db_column='PR_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    n_shopsec = models.CharField(db_column='N_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    qty_ord = models.DecimalField(db_column='QTY_ORD', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    tot_rm_qty = models.DecimalField(db_column='TOT_RM_QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    m5glsn = models.DecimalField(db_column='M5GLSN', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5prtdt = models.DateField(db_column='M5PRTDT', blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEMP_M5DOC'


class TempPmd(models.Model):
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty_b = models.DecimalField(db_column='QTY_B', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    dttym = models.DateField(db_column='DTTYM', blank=True, null=True)  # Field name made lowercase.
    curtym = models.CharField(db_column='CURTYM', max_length=55, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TEMP_PMD'


class Tools(models.Model):
    tool_code = models.CharField(db_column='TOOL_CODE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=50, blank=True, null=True)  # Field name made lowercase.
    size_m = models.CharField(db_column='SIZE_M', max_length=50, blank=True, null=True)  # Field name made lowercase.
    drg_no = models.CharField(db_column='DRG_NO', max_length=30, blank=True, null=True)  # Field name made lowercase.
    spec = models.CharField(db_column='SPEC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='PRICE', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=30, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    toolcd_old = models.CharField(db_column='TOOLCD_OLD', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TOOLS'


class Toolstk(models.Model):
    location = models.CharField(db_column='LOCATION', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tool_code = models.CharField(db_column='TOOL_CODE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    stock_tot = models.DecimalField(db_column='STOCK_TOT', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    stock_bal = models.DecimalField(db_column='STOCK_BAL', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    cost = models.DecimalField(db_column='COST', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tr_qty = models.DecimalField(db_column='TR_QTY', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    last_issdt = models.DateField(db_column='LAST_ISSDT', blank=True, null=True)  # Field name made lowercase.
    last_recdt = models.DateField(db_column='LAST_RECDT', blank=True, null=True)  # Field name made lowercase.
    open_date = models.DateField(db_column='OPEN_DATE', blank=True, null=True)  # Field name made lowercase.
    close_date = models.DateField(db_column='CLOSE_DATE', blank=True, null=True)  # Field name made lowercase.
    updt_by = models.CharField(db_column='UPDT_BY', max_length=5, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TOOLSTK'


class Tooltr(models.Model):
    location = models.CharField(db_column='LOCATION', max_length=5, blank=True, null=True)  # Field name made lowercase.
    tool_code = models.CharField(db_column='TOOL_CODE', max_length=8, blank=True, null=True)  # Field name made lowercase.
    issued_to = models.CharField(db_column='ISSUED_TO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    vr_qty = models.DecimalField(db_column='VR_QTY', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    vrno = models.CharField(db_column='VRNO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    vrslno = models.CharField(db_column='VRSLNO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    vrno_pr = models.CharField(db_column='VRNO_PR', max_length=5, blank=True, null=True)  # Field name made lowercase.
    vrslno_pr = models.CharField(db_column='VRSLNO_PR', max_length=2, blank=True, null=True)  # Field name made lowercase.
    qty_issue = models.DecimalField(db_column='QTY_ISSUE', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    date_issue = models.DateField(db_column='DATE_ISSUE', blank=True, null=True)  # Field name made lowercase.
    qty_ret = models.DecimalField(db_column='QTY_RET', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    date_ret = models.DateField(db_column='DATE_RET', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cb_qty = models.DecimalField(db_column='CB_QTY', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    stock_add = models.DecimalField(db_column='STOCK_ADD', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TOOLTR'


class Trial(models.Model):
    loco_type = models.CharField(db_column='LOCO_TYPE', max_length=6, blank=True, null=True)  # Field name made lowercase.
    loco_no = models.CharField(db_column='LOCO_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    item_slno = models.DecimalField(db_column='ITEM_SLNO', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    drg_cat_no = models.CharField(db_column='DRG_CAT_NO', max_length=11, blank=True, null=True)  # Field name made lowercase.
    supplier = models.CharField(db_column='SUPPLIER', max_length=30, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=9, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rly = models.CharField(db_column='RLY', max_length=3, blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRIAL'


class Vi36(models.Model):
    form_no = models.CharField(db_column='FORM_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    make = models.CharField(db_column='MAKE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    maker_slno = models.CharField(db_column='MAKER_SLNO', max_length=32, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VI36'


class Vi36Comp(models.Model):
    div = models.CharField(db_column='DIV', max_length=1, blank=True, null=True)  # Field name made lowercase.
    partno_ep = models.CharField(db_column='PARTNO_EP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    des = models.CharField(db_column='DES', max_length=40, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VI36COMP'


class Vi36Old(models.Model):
    div = models.CharField(db_column='DIV', max_length=1, blank=True, null=True)  # Field name made lowercase.
    partno_ep = models.CharField(db_column='PARTNO_EP', max_length=8, blank=True, null=True)  # Field name made lowercase.
    slno = models.CharField(db_column='SLNO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    road_no = models.CharField(db_column='ROAD_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    make = models.CharField(db_column='MAKE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    maker_slno = models.CharField(db_column='MAKER_SLNO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    assly_slno = models.CharField(db_column='ASSLY_SLNO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    updt_dt = models.DateField(db_column='UPDT_DT', blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VI36OLD'


class Wgrptable(models.Model):
    scl_cl = models.CharField(db_column='SCL_CL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    f_shopsec = models.CharField(db_column='F_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    ptc = models.CharField(db_column='PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=16, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    rc_st_wk = models.CharField(db_column='RC_ST_WK', max_length=4, blank=True, null=True)  # Field name made lowercase.
    rm_partno = models.CharField(db_column='RM_PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.DecimalField(db_column='RM_QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    rm_ptc = models.CharField(db_column='RM_PTC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cut_shear = models.CharField(db_column='CUT_SHEAR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    m2sln = models.DecimalField(db_column='M2SLN', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m2prtdt = models.DateField(db_column='M2PRTDT', blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m4_no = models.DecimalField(db_column='M4_NO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=2, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ep_type = models.CharField(db_column='EP_TYPE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    batch_type = models.CharField(db_column='BATCH_TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    batch_qty = models.DecimalField(db_column='BATCH_QTY', max_digits=16, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    loco_fr = models.CharField(db_column='LOCO_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    loco_to = models.CharField(db_column='LOCO_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    uot_wk_f = models.CharField(db_column='UOT_WK_F', max_length=4, blank=True, null=True)  # Field name made lowercase.
    b_expl_dt = models.DateField(db_column='B_EXPL_DT', blank=True, null=True)  # Field name made lowercase.
    dlogb_ty = models.CharField(db_column='DLOGB_TY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    alt_part = models.CharField(db_column='ALT_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    al_fr = models.CharField(db_column='AL_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    al_to = models.CharField(db_column='AL_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    doc_fr = models.DecimalField(db_column='DOC_FR', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    doc_to = models.DecimalField(db_column='DOC_TO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pa_sw = models.CharField(db_column='PA_SW', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WGRPTABLE'


class Xx(models.Model):
    doc_code = models.CharField(db_column='DOC_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    doc_no = models.DecimalField(db_column='DOC_NO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    pm_no = models.CharField(db_column='PM_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    qty = models.DecimalField(db_column='QTY', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    bo_no = models.CharField(db_column='BO_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    due_wk = models.CharField(db_column='DUE_WK', max_length=4, blank=True, null=True)  # Field name made lowercase.
    prtdt = models.DateField(db_column='PRTDT', blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    doc_ind = models.CharField(db_column='DOC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='UNIT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    epc = models.CharField(db_column='EPC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    stage = models.CharField(db_column='STAGE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ward_no = models.CharField(db_column='WARD_NO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    finyear = models.CharField(db_column='FINYEAR', max_length=2, blank=True, null=True)  # Field name made lowercase.
    vr_no = models.CharField(db_column='VR_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    kit_ind = models.CharField(db_column='KIT_IND', max_length=2, blank=True, null=True)  # Field name made lowercase.
    station = models.CharField(db_column='STATION', max_length=3, blank=True, null=True)  # Field name made lowercase.
    stg = models.CharField(db_column='STG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    opn_no = models.CharField(db_column='OPN_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    kit_no = models.DecimalField(db_column='KIT_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sub_docno = models.DecimalField(db_column='SUB_DOCNO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    lieu_part = models.CharField(db_column='LIEU_PART', max_length=8, blank=True, null=True)  # Field name made lowercase.
    drawn_by = models.CharField(db_column='DRAWN_BY', max_length=4, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'XX'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class navbar(models.Model):
    role = models.CharField(max_length=50, blank=True, null=True)
    navmenu = models.CharField(max_length=50, blank=True, null=True)
    navitem = models.CharField(max_length=50, blank=True, null=True)
    navsubitem = models.CharField(max_length=50, blank=True, null=True)
    link = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dlw_navbar'


class roles(models.Model):
    role = models.CharField(primary_key=True, max_length=50)
    parent = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dlw_roles'


class shift(models.Model):
    emp_id = models.CharField(max_length=15, blank=True, null=True)
    shift_id = models.CharField(max_length=50, blank=True, null=True)
    validity_from = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dlw_shift'


class shift_history(models.Model):
    emp_id = models.CharField(max_length=15, blank=True, null=True)
    shift_id = models.CharField(max_length=50, blank=True, null=True)
    validity_from = models.CharField(max_length=30, blank=True, null=True)
    validity_to = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dlw_shift_history'


class testc(models.Model):
    subject = models.CharField(max_length=20, blank=True, null=True)
    targetone = models.IntegerField(blank=True, null=True)
    targettwo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dlw_testc'


class user_master(models.Model):
    emp_id = models.CharField(primary_key=True, max_length=15)
    role = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=50, blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    contactno = models.CharField(max_length=10, blank=True, null=True)
    parent = models.CharField(max_length=50, blank=True, null=True)
    shop_id = models.CharField(max_length = 30 , null=True)

class shop_section(models.Model):
    section_code = models.CharField(primary_key=True, max_length =10)
    section_id = models.CharField(null = True,max_length =10)
    section_desc = models.CharField(null = True,max_length =150)
    shop_code = models.CharField(null = True,max_length =50)
    shop_id = models.CharField(null = True,max_length =50)


class annual_production(models.Model):
    financial_year=models.CharField(null=True,max_length=20)
    target_quantity=models.CharField(null=True,max_length=20)
    loco_type=models.CharField(max_length=50,null=True)
    buffer_quantity=models.CharField(null=True,max_length=20)
    revisionid=models.IntegerField(null=True,default=99)
    customer=models.CharField(null=True,max_length=20,default='ind-rail')

class jpo(models.Model):
    financial_year=models.CharField(null=True,max_length=20)
    revisionid=models.IntegerField(null=True,default=99)
    jpo=models.CharField(null=True,max_length=20)
    subject=models.TextField(null=True)
    reference=models.TextField(null=True)
    majoralt=models.TextField(null=True)
    remark=models.TextField(null=True)
    date=models.CharField(null=True,max_length=30)
    numyrs=models.CharField(null=True,max_length=20)
    numdgp=models.CharField(null=True,max_length=10)
    formno=models.TextField(null=True)
    headmjr=models.TextField(null=True)
    number=models.TextField(null=True)
    finalval=models.IntegerField(null=True,default=0)

class loconame(models.Model):
    loconame=models.TextField(null=True)

class materialname(models.Model):
    matrname=models.TextField(null=True)

class namedgn(models.Model):
    namep=models.CharField(null=True,max_length=50)
    design=models.CharField(null=True,max_length=30)
    revision=models.IntegerField(null=True,default=99)


class testing_purpose(models.Model):
    first=models.CharField(null=True,max_length=50)
    second=models.CharField(null=True,max_length=50)


class MachiningAirBox(models.Model):
    sno=models.AutoField(primary_key=True)
    bo_no=models.CharField(max_length=20,null=True)
    bo_date=models.DateField(null=True)
    airbox_sno=models.CharField(max_length=20,null=True)
    airbox_make=models.CharField(max_length=20,null=True)
    in_qty=models.IntegerField(null=True)
    out_qty=models.IntegerField(null=True)
    date=models.CharField(null=True,max_length=20)
    loco_type=models.CharField(max_length=20,null=True)
    dispatch_to=models.CharField(max_length=20,null=True)
    dispatch_status = models.BooleanField(default=False)

class barrelfirst(models.Model):
    locotype=models.CharField(max_length=100,null=True)
    code=models.CharField(max_length=50,null=True)

class empmast(models.Model):
    empno=models.CharField(max_length=20,primary_key=True)
    empname=models.CharField(max_length=50,null=True)
    birthdate=models.CharField(max_length=50,null=True)
    sex=models.CharField(max_length=10,null=True)
    marital_status=models.CharField(max_length=10,null=True)
    decode_paycategory=models.CharField(max_length=50,null=True)
    billunit=models.CharField(max_length=50,null=True)
    service_status=models.CharField(max_length=50,null=True)
    emp_status=models.CharField(max_length=50,null=True)
    rectt_category=models.CharField(max_length=50,null=True)
    payband=models.CharField(max_length=10,null=True)
    scalecode=models.CharField(max_length=50,null=True)
    pc7_level=models.CharField(max_length=10,null=True)
    payrate=models.CharField(max_length=50,null=True)
    office=models.CharField(max_length=50,null=True)
    station_des=models.CharField(max_length=50,null=True)
    emptype=models.CharField(max_length=10,null=True)
    medicalcode=models.CharField(max_length=50,null=True)
    tradecode=models.CharField(max_length=50,null=True)
    dept_desc=models.CharField(max_length=50,null=True)
    parentshop=models.CharField(max_length=50,null=True)
    shopno=models.CharField(max_length=50,null=True)
    desig_longdesc=models.CharField(max_length=50,null=True)
    wau=models.CharField(max_length=50,null=True)
    inc_category=models.CharField(max_length=50,null=True)
    emp_inctype=models.CharField(max_length=50,null=True)
    parent = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    contactno = models.CharField(max_length=10, blank=True, null=True)

class MiscellSection(models.Model):
   sno=models.AutoField(primary_key=True)
   bo_no=models.CharField(max_length=20,null=True)
   bo_date=models.CharField(max_length=20,null=True)
   shaft_m=models.CharField(max_length=20,null=True) 
   in_qty=models.IntegerField(null=True)
   out_qty=models.IntegerField(null=True)
   date=models.CharField(max_length=20,null=True) 
   loco_type=models.CharField(max_length=20,null=True)
   dispatch_to=models.CharField(max_length=20,null=True)
   dispatch_status = models.BooleanField(default=False)


class AxleWheelMachining(models.Model):
  sno=models.AutoField(primary_key=True)
  bo_no=models.CharField(max_length=20,null=True)
  bo_date=models.CharField(max_length=20,null=True)
  wheel_no=models.CharField(max_length=20,null=True)
  wheel_make=models.CharField(max_length=20,null=True)
  wheel_heatcaseno=models.CharField(max_length=20,null=True)
  axle_no=models.CharField(max_length=20,null=True)
  axle_make=models.CharField(max_length=20,null=True)
  axle_heatcaseno=models.CharField(max_length=20,null=True)
  loco_type=models.CharField(max_length=20,null=True)
  date=models.CharField(max_length=20,null=True)
  dispatch_to=models.CharField(max_length=20,null=True)
  ustaxle=models.CharField(max_length=20,blank=True)
  axlelength=models.CharField(max_length=20,blank=True)
  journalaxle=models.CharField(max_length=20,blank=True)
  throweraxle=models.CharField(max_length=20,blank=True)   
  wheelseataxle=models.CharField(max_length=20,blank=True)
  gearseataxle=models.CharField(max_length=20,blank=True)
  collaraxle=models.CharField(max_length=20,blank=True)
  dateaxle=models.DateField(null=True)
  bearingaxle=models.CharField(max_length=20,blank=True)
  abutmentaxle=models.CharField(max_length=20,blank=True)
  inspector_nameaxle=models.CharField(max_length=20,blank=True)
  journal_surfacefinishGE=models.CharField(max_length=20,blank=True)
  wheelseat_surfacefinishGE=models.CharField(max_length=20,blank=True)
  gearseat_surfacefinishGE=models.CharField(max_length=20,blank=True)
  journal_surfacefinishFE=models.CharField(max_length=20,blank=True)
  wheelseat_surfacefinishFE=models.CharField(max_length=20,blank=True)
  gearseat_surfacefinishFE=models.CharField(max_length=20,blank=True)
  batch_order_no=models.CharField(max_length=20,null=True)
  ustwhl=models.CharField(max_length=20,null=True)
  hub_lengthwhl=models.CharField(max_length=20,null=True)
  tread_diawhl=models.CharField(max_length=20,null=True)   
  rim_thicknesswhl=models.CharField(max_length=20,null=True)
  bore_diawhl=models.CharField(max_length=20,null=True)
  inspector_namewhl=models.CharField(max_length=20,null=True)
  datewhl=models.DateField(null=True)      
  dispatch_status=models.BooleanField(default=False)
  axlefitting_status=models.BooleanField(default=False) 
  wheelfitting_status=models.BooleanField(default=False) 


class M5SHEMP(models.Model):
    yymm = models.CharField(db_column='YYMM', max_length=4, blank=True, null=True)  # Field name made lowercase.
    shopsec = models.CharField(db_column='SHOPSEC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    staff_no = models.CharField(db_column='STAFF_NO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desgn = models.CharField(db_column='DESGN', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cat = models.CharField(db_column='CAT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    emp_type = models.CharField(db_column='EMP_TYPE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    updt_by = models.CharField(db_column='UPDT_BY', max_length=20, blank=True, null=True)  # Field name made lowercase.
    updt_date = models.DateField(db_column='UPDT_DATE', blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ticket_no = models.IntegerField(db_column='TICKET_NO',  blank=True, null=True, default=0)  # Field name made lowercase.
    month_hrs = models.CharField(db_column='MONTH_HRS', max_length=10, blank=True,null=True,default=0) # Field name made lowercase0.
    total_time_taken = models.IntegerField(db_column='TOTAL_TIME_TAKEN', blank=True,null=True, default=0)
    in1 = models.CharField(db_column='IN1', max_length=10, blank=True,null=True) # Field name made lowercase.
    out = models.CharField(db_column='OUT', max_length=10, blank=True,null=True) # Field name made lowercase.
    date = models.CharField(db_column='DATE', max_length=10, blank=True,null=True) # Field name made lowercase.
    flag = models.CharField(db_column='FLAG', max_length=1, blank=True,null=True, default='A') # Field name made lowercase.
    class Meta:
        db_table = 'M5SHEMP'      

class M5DOCnew(models.Model):   
    scl_cl = models.CharField(db_column='SCL_CL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    batch_no = models.CharField(db_column='BATCH_NO', max_length=7, blank=True, null=True)  # Field name made lowercase.
    assly_no = models.CharField(db_column='ASSLY_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    part_no = models.CharField(db_column='PART_NO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    m2slno = models.DecimalField(db_column='M2SLNO', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rm_partno = models.CharField(db_column='RM_PARTNO', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_ut = models.CharField(db_column='RM_UT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cut_shear = models.CharField(db_column='CUT_SHEAR', max_length=8, blank=True, null=True)  # Field name made lowercase.
    rm_qty = models.DecimalField(db_column='RM_QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    shop_sec = models.CharField(db_column='SHOP_SEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    lc_no = models.CharField(db_column='LC_NO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    opn = models.CharField(db_column='OPN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    opn_desc = models.CharField(db_column='OPN_DESC', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pa = models.DecimalField(db_column='PA', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    at = models.DecimalField(db_column='AT', max_digits=6, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    no_off = models.DecimalField(db_column='NO_OFF', max_digits=2, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5_cd = models.CharField(db_column='M5_CD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    pr_shopsec = models.CharField(db_column='PR_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    n_shopsec = models.CharField(db_column='N_SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    qty_ord = models.DecimalField(db_column='QTY_ORD', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    tot_rm_qty = models.DecimalField(db_column='TOT_RM_QTY', max_digits=8, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    l_fr = models.CharField(db_column='L_FR', max_length=4, blank=True, null=True)  # Field name made lowercase.
    l_to = models.CharField(db_column='L_TO', max_length=4, blank=True, null=True)  # Field name made lowercase.
    m5glsn = models.DecimalField(db_column='M5GLSN', max_digits=6, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    m5prtdt = models.DateField(db_column='M5PRTDT', blank=True, null=True)  # Field name made lowercase.
    seq = models.DecimalField(db_column='SEQ', max_digits=3, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    brn_no = models.DecimalField(db_column='BRN_NO', max_digits=5, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    mark = models.CharField(db_column='MARK', max_length=1, blank=True, null=True)  # Field name made lowercase.
    del_fl = models.CharField(db_column='DEL_FL', max_length=1, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    qty_insp = models.IntegerField(db_column='QTY_INSP', default=0, blank=True, null=True)  # Field name made lowercase.
    inspector = models.IntegerField(db_column='INSPECTOR',  blank=True, null=True, default=0)  # Field name made lowercase.
    date = models.CharField(db_column='DATE', blank='True', max_length=10, null='True')  # Field name made lowercase.
    remarks = models.CharField(db_column='REMARKS',max_length=50, blank='True', null='True')  # Field name made lowercase.
    worker = models.CharField(db_column='WORKER',  max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'M5DOCnew'

class PinionPressing(models.Model):
    sno=models.AutoField(primary_key=True)
    bo_no=models.CharField(max_length=20,null=True)
    bo_date=models.CharField(max_length=20,null=True)
    date=models.CharField(max_length=20,null=True)
    tm_no=models.CharField(max_length=20,null=True)
    tm_make=models.CharField(max_length=20,null=True)
    pinion_no=models.CharField(max_length=20,null=True)
    pinion_make=models.CharField(max_length=20,null=True)
    pinion_travel=models.CharField(max_length=20,null=True)
    pinion_pressure=models.CharField(max_length=20,null=True)
    blue_match=models.CharField(max_length=20,null=True)
    loco_type=models.CharField(max_length=20,null=True)
    dispatch_to=models.CharField(max_length=50,null=True)
    dispatch_status=models.BooleanField(default=False)


class dpo(models.Model):
    procedureno=models.CharField(max_length=50,null=True,default='0')
    locotype=models.CharField(max_length=50,null=True)
    orderno=models.CharField(max_length=10,null=True)
    subject=models.TextField(null=True)
    reference=models.TextField(null=True)
    copyto=models.TextField(null=True)
    summary=models.TextField(null=True)
    date=models.CharField(null=True,max_length=20)

class dpoloco(models.Model):
    procedureno=models.CharField(max_length=50,null=True,default='0')
    loconame=models.CharField(max_length=50,null=True)
    locotype=models.CharField(max_length=50,null=True)
    # endcumno=models.CharField(max_length=10,null=True)
    batchordno=models.CharField(max_length=50,null=True)
    qtybatch=models.CharField(max_length=50,null=True)
    cumino=models.CharField(max_length=50,null=True)
    orderno=models.CharField(max_length=10,null=True)


class subnavbar(models.Model):
    parentmenu=models.CharField(null=True,max_length=50)
    childmenu=models.CharField(null=True,max_length=50)
    link=models.CharField(null=True,max_length=50)

class M7(models.Model):
    shop_sec = models.CharField(max_length=100, blank=True, null=True)
    staff_no = models.CharField(max_length=5, blank=True, null=True)
    wo_no = models.CharField(max_length=100, blank=True, null=True)
    month = models.CharField(max_length=5, blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    part_no = models.CharField(max_length=8, blank=True, null=True)
    cat = models.CharField(max_length=2, blank=True, null=True)
    date = models.CharField(max_length=10, blank=True, null=True)
    in1 = models.CharField(max_length=10, blank=True, null=True)
    out = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'M7'

class M20new(models.Model):
    shop_sec = models.CharField(max_length=10, blank=True, null= True)
    staff_no = models.CharField(max_length=10, blank=True, null = True)
    lv_date = models.DateField(blank= True, null= True)
    name = models.CharField(max_length=50, blank=True, null= True)
    ticketno = models.CharField(max_length=10, blank = True, null= True)
    alt_date = models.DateField(blank = True, null=True)

    class Meta:
        db_table = 'M20new'

class AxleWheelPressing(models.Model):
    sno=models.AutoField(primary_key=True)
    bo_no=models.CharField(max_length=20,null=True)
    bo_date=models.CharField(max_length=20,null=True)
    date=models.CharField(max_length=20,null=True)
    loco_type=models.CharField(max_length=20,null=True)
    axle_no=models.CharField(max_length=20,null=True)
    wheelno_de=models.CharField(max_length=20,null=True)
    wheelno_nde=models.CharField(max_length=20,null=True)
    bullgear_make=models.CharField(max_length=20,null=True)   
    bullgear_no=models.CharField(max_length=20,null=True)
    inspector_name=models.CharField(max_length=20,null=True)
    dispatch_to=models.CharField(max_length=50,null=True)
    dispatch_status=models.BooleanField(default=False)

     
class M11(models.Model):
    yymm = models.CharField(db_column='YYMM', max_length=4, blank=True, null=True)  # Field name made lowercase.
    shopsec = models.CharField(db_column='SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    staff_no = models.CharField(db_column='STAFF_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desgn = models.CharField(db_column='DESGN', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cat = models.CharField(db_column='CAT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    emp_type = models.CharField(db_column='EMP_TYPE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    updt_by = models.CharField(db_column='UPDT_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    updt_date = models.DateField(db_column='UPDT_DATE', blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    in1 = models.CharField(db_column='IN1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    out = models.CharField(db_column='OUT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    month = models.CharField(db_column='MONTH', max_length=15, blank=True, null=True)  # Field name made lowercase.
    total_time = models.CharField(db_column='TOTAL_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    idle_time = models.CharField(db_column='IDLE_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    detail_no=models.CharField(db_column='IT_reasons',null=True,max_length=70)

    class Meta:
        db_table = 'M11'
    
class M12DOC(models.Model):
    yymm = models.CharField(db_column='YYMM', max_length=4, blank=True, null=True)  # Field name made lowercase.
    shopsec = models.CharField(db_column='SHOPSEC', max_length=4, blank=True, null=True)  # Field name made lowercase.
    staff_no = models.CharField(db_column='STAFF_NO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=40, blank=True, null=True)  # Field name made lowercase.
    desgn = models.CharField(db_column='DESGN', max_length=10, blank=True, null=True)  # Field name made lowercase.
    cat = models.CharField(db_column='CAT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    emp_type = models.CharField(db_column='EMP_TYPE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    updt_by = models.CharField(db_column='UPDT_BY', max_length=6, blank=True, null=True)  # Field name made lowercase.
    updt_date = models.DateField(db_column='UPDT_DATE', blank=True, null=True)  # Field name made lowercase.
    rec_ind = models.CharField(db_column='REC_IND', max_length=1, blank=True, null=True)  # Field name made lowercase.
    in1 = models.CharField(db_column='IN1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    out = models.CharField(db_column='OUT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(db_column='DATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    month = models.CharField(db_column='MONTH', max_length=15, blank=True, null=True)  # Field name made lowercase.
    total_time = models.CharField(db_column='TOTAL_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    idle_time = models.CharField(db_column='IDLE_TIME', max_length=10, blank=True, null=True)  # Field name made lowercase.
    reasons_for_idle_time = models.CharField(db_column='REASONS_FOR_IDLE_TIME', max_length=30, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        db_table = 'M12DOC'
