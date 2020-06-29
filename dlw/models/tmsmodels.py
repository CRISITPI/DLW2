from django.db import models

class WheelMachining(models.Model):
    sno=models.AutoField(primary_key=True)
    bo_no=models.CharField(max_length=20,null=True)
    bo_date=models.CharField(max_length=20,null=True)
    pt_no=models.CharField(max_length=20,null=True)
    bo_qty=models.CharField(max_length=20,null=True)
    in_qty=models.CharField(max_length=20,null=True)
    out_qty=models.CharField(max_length=20,null=True)
    wheel_no=models.CharField(max_length=20,null=True)
    wheel_make=models.CharField(max_length=20,null=True)
    wheel_heatcaseno=models.CharField(max_length=25,null=True)
    loco_type=models.CharField(max_length=20,null=True)
    date=models.CharField(max_length=20,null=True)
    dispatch_to=models.CharField(max_length=20,null=True)
    ustwhl=models.CharField(max_length=20,null=True)
    ustwhl_date=models.CharField(max_length=20,null=True)
    ustwhl_status=models.CharField(max_length=20,null=True)
    hub_lengthwhl=models.CharField(max_length=20,null=True)
    tread_diawhl=models.CharField(max_length=20,null=True)   
    rim_thicknesswhl=models.CharField(max_length=20,null=True)
    bore_diawhl=models.CharField(max_length=20,null=True)
    inspector_namewhl=models.CharField(max_length=20,null=True)
    datewhl=models.CharField(null=True,max_length=20)      
    dispatch_status=models.BooleanField(default=False)
    wheelfitting_status=models.BooleanField(default=False)
    wheelinspection_status=models.BooleanField(default=False)
    inspection_status=models.NullBooleanField()
    dispatch_date=models.CharField(max_length=20,null=True)
    wheelp_no=models.CharField(max_length=20,null=True)


class AxleMachining(models.Model):
    sno=models.AutoField(primary_key=True)
    bo_no=models.CharField(max_length=20,null=True)
    bo_date=models.CharField(max_length=20,null=True)
    pt_no=models.CharField(max_length=20,null=True)
    bo_qty=models.CharField(max_length=20,null=True)
    in_qty=models.CharField(max_length=20,null=True)
    out_qty=models.CharField(max_length=20,null=True)
    axle_no=models.CharField(max_length=20,null=True)
    axle_make=models.CharField(max_length=20,null=True)
    axle_heatcaseno=models.CharField(max_length=25,null=True)
    loco_type=models.CharField(max_length=20,null=True)
    date=models.CharField(max_length=20,null=True)
    dispatch_to=models.CharField(max_length=20,null=True)
    ustaxle=models.CharField(max_length=20,blank=True)
    ustaxle_date=models.CharField(max_length=20,null=True)
    ustaxle_status=models.CharField(max_length=20,null=True)
    axlelength=models.CharField(max_length=20,blank=True)
    journalaxle=models.CharField(max_length=20,blank=True)
    throweraxle=models.CharField(max_length=20,blank=True)   
    wheelseataxle=models.CharField(max_length=20,blank=True)
    gearseataxle=models.CharField(max_length=20,blank=True)
    collaraxle=models.CharField(max_length=20,blank=True)
    dateaxle=models.CharField(null=True,max_length=20)
    bearingaxle=models.CharField(max_length=20,blank=True)
    abutmentaxle=models.CharField(max_length=20,blank=True)
    inspector_nameaxle=models.CharField(max_length=20,blank=True)
    journal_surfacefinishGE=models.CharField(max_length=20,blank=True)
    wheelseat_surfacefinishGE=models.CharField(max_length=20,blank=True)
    gearseat_surfacefinishGE=models.CharField(max_length=20,blank=True)
    journal_surfacefinishFE=models.CharField(max_length=20,blank=True)
    wheelseat_surfacefinishFE=models.CharField(max_length=20,blank=True)
    gearseat_surfacefinishFE=models.CharField(max_length=20,blank=True)
    dispatch_status=models.BooleanField(default=False)
    axlefitting_status=models.BooleanField(default=False)
    axleinspection_status=models.BooleanField(default=False) 
    inspection_status=models.NullBooleanField()
    dispatch_date=models.CharField(max_length=20,null=True)
    axlep_no=models.CharField(max_length=20,null=True)
    journalaxlende=models.CharField(max_length=20,blank=True)
    throweraxlende=models.CharField(max_length=20,blank=True)
    wheelseataxlende=models.CharField(max_length=20,blank=True)
    collaraxlende=models.CharField(max_length=20,blank=True)



class AxleWheelPressing(models.Model):
    sno=models.AutoField(primary_key=True)
    bo_no=models.CharField(max_length=20,null=True)
    bo_date=models.CharField(max_length=20,null=True)
    pt_no=models.CharField(max_length=20,null=True)
    bo_qty=models.CharField(max_length=20,null=True)
    in_qty=models.CharField(max_length=20,null=True)
    out_qty=models.CharField(max_length=20,null=True)
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
    wheel_de_make=models.CharField(max_length=20,null=True)
    wheel_de_pressure=models.CharField(max_length=20,null=True)
    wheel_nde_make=models.CharField(max_length=20,null=True)
    wheel_nde_pressure=models.CharField(max_length=20,null=True)
    axle_make=models.CharField(max_length=20,null=True)
    msu_unit_no=models.CharField(max_length=20,null=True)
    bullgear_pressure=models.CharField(max_length=20,null=True)
    msu_unit_make=models.CharField(max_length=20,null=True)
    axle_box_node=models.CharField(max_length=20,null=True)
    axle_box_makede=models.CharField(max_length=20,null=True)
    axle_box_clearancede=models.CharField(max_length=20,null=True)
    axle_box_nonde=models.CharField(max_length=20,null=True)
    axle_box_makende=models.CharField(max_length=20,null=True)
    axle_box_clearancende=models.CharField(max_length=20,null=True)
    msu_bearing_de_make=models.CharField(max_length=20,null=True)
    msu_bearing_nde_make=models.CharField(max_length=20,null=True)
    cru_bearing_no_de=models.CharField(max_length=20,null=True)
    cru_bearing_make_de=models.CharField(max_length=20,null=True)
    cru_bearing_pressure_de=models.CharField(max_length=20,null=True)
    cru_bearing_no_nde=models.CharField(max_length=20,null=True)
    cru_bearing_make_nde=models.CharField(max_length=20,null=True)
    cru_bearing_pressure_nde=models.CharField(max_length=20,null=True)
    wheel_distance=models.CharField(max_length=20,null=True)
    axialplay_de=models.CharField(max_length=20,null=True)
    axialplay_nde=models.CharField(max_length=20,null=True)
    date=models.CharField(max_length=20,null=True)
    locos=models.CharField(max_length=20,null=True)
    inspector_name=models.CharField(max_length=20,null=True)
    journal_no_de=models.CharField(max_length=20,null=True)
    journal_make_de=models.CharField(max_length=20,null=True)
    journal_no_nde=models.CharField(max_length=20,null=True)
    journal_make_nde=models.CharField(max_length=20,null=True)
    inspectinspection_status=models.NullBooleanField()
    hhpinspection_status=models.NullBooleanField()
    dispatch_date=models.CharField(max_length=20,null=True)
    edit_date=models.CharField(max_length=20,null=True)
    inspect_date=models.CharField(max_length=20,null=True)



class PinionPressing(models.Model):
    sno=models.AutoField(primary_key=True)
    bo_no=models.CharField(max_length=20,null=True)
    bo_date=models.CharField(max_length=20,null=True)
    pt_no=models.CharField(max_length=20,null=True)
    bo_qty=models.CharField(max_length=20,null=True)
    in_qty=models.CharField(max_length=20,null=True)
    out_qty=models.CharField(max_length=20,null=True)
    date=models.CharField(max_length=20,null=True)
    tm_no=models.CharField(max_length=20,null=True)
    tm_make=models.CharField(max_length=20,null=True)
    pinion_no=models.CharField(max_length=20,null=True)
    pinion_make=models.CharField(max_length=20,null=True)
    pinion_travel=models.CharField(max_length=20,null=True)
    pinion_pressure_triangle_glycerin=models.CharField(max_length=20,null=True)
    pinion_pressure_square_ram=models.CharField(max_length=20,null=True)
    pinion_teeth_dist=models.CharField(max_length=20,null=True)
    blue_match=models.CharField(max_length=20,null=True)
    loco_type=models.CharField(max_length=20,null=True)
    dispatch_to=models.CharField(max_length=50,null=True)
    dispatch_status=models.BooleanField(default=False)
    dispatch_date=models.CharField(max_length=20,null=True)
    inspection_status=models.NullBooleanField()
    axle_no=models.CharField(max_length=20,null=True)
    inspect_date=models.CharField(max_length=20,null=True)


class BogieAssembly(models.Model):
    sno=models.AutoField(primary_key=True)
    bo_no=models.CharField(max_length=20,null=True)
    bo_date=models.CharField(max_length=20,null=True)
    pt_no=models.CharField(max_length=20,null=True)
    bo_qty=models.CharField(max_length=20,null=True)
    date=models.CharField(max_length=20,null=True)
    loco_type=models.CharField(max_length=20,null=True)
    in_date=models.CharField(max_length=20,null=True)
    out_qty=models.CharField(max_length=20,null=True)
    frameserial_no=models.CharField(max_length=20,null=True)
    frame_make=models.CharField(max_length=20,null=True)
    frame_type=models.CharField(max_length=20,null=True)
    axle_no=models.CharField(max_length=20,null=True)
    axle_location=models.CharField(max_length=20,null=True)
    traction_motor_no=models.CharField(max_length=20,null=True)
    gear_case_no=models.CharField(max_length=20,null=True)
    gear_case_make=models.CharField(max_length=20,null=True)
    msu_unit_no=models.CharField(max_length=20,null=True)
    break_rigging_make=models.CharField(max_length=20,null=True)
    coil_spring_make=models.CharField(max_length=20,null=True)
    secondary_coil_make=models.CharField(max_length=20,null=True)
    sand_box_make=models.CharField(max_length=20,null=True)
    spheri_block_make=models.CharField(max_length=20,null=True)
    thrust_pad_make=models.CharField(max_length=20,null=True)
    break_cylinder_make=models.CharField(max_length=20,null=True)
    elastic_shop_make=models.CharField(max_length=30,null=True)
    lateral_damper=models.CharField(max_length=20,null=True)
    horizontal_damper=models.CharField(max_length=20,null=True)
    dispatch_to=models.CharField(max_length=50,null=True)
    dispatch_status=models.BooleanField(default=False)
    inspection_status=models.NullBooleanField()
    dispatch_date=models.CharField(max_length=20,null=True)
    inspect_date=models.CharField(max_length=20,null=True)
    first_axle=models.CharField(max_length=20,null=True)
    second_axle=models.CharField(max_length=20,null=True)
    third_axle=models.CharField(max_length=20,null=True)
    first_axle_location=models.CharField(max_length=10,null=True)
    second_axle_location=models.CharField(max_length=10,null=True)
    third_axle_location=models.CharField(max_length=10,null=True)
    first_coilspring_make=models.CharField(max_length=20,null=True)
    first_gearcase_no=models.CharField(max_length=20,null=True)
    first_gearcase_make=models.CharField(max_length=20,null=True)
    first_back_lash=models.CharField(max_length=20,null=True)
    first_vertical_r=models.CharField(max_length=20,null=True)
    first_vertical_l=models.CharField(max_length=20,null=True)
    first_horizontal_r=models.CharField(max_length=20,null=True)
    first_horizontal_l=models.CharField(max_length=20,null=True)
    second_coilspring_make=models.CharField(max_length=20,null=True)
    second_gearcase_no=models.CharField(max_length=20,null=True)
    second_gearcase_make=models.CharField(max_length=20,null=True)
    second_back_lash=models.CharField(max_length=20,null=True)
    second_vertical_r=models.CharField(max_length=20,null=True)
    second_vertical_l=models.CharField(max_length=20,null=True)
    second_horizontal_r=models.CharField(max_length=20,null=True)
    second_horizontal_l=models.CharField(max_length=20,null=True)
    third_coilspring_make=models.CharField(max_length=20,null=True)
    third_gearcase_no=models.CharField(max_length=20,null=True)
    third_gearcase_make=models.CharField(max_length=20,null=True)
    third_back_lash=models.CharField(max_length=20,null=True)
    third_vertical_r=models.CharField(max_length=20,null=True)
    third_vertical_l=models.CharField(max_length=20,null=True)
    third_horizontal_r=models.CharField(max_length=20,null=True)
    third_horizontal_l=models.CharField(max_length=20,null=True)
    wheel_set_guide=models.CharField(max_length=20,null=True)
    gear_case_oil=models.CharField(max_length=20,null=True)
    first_secondary_coilspring_make=models.CharField(max_length=20,null=True)
    second_secondary_coilspring_make=models.CharField(max_length=20,null=True)
    third_secondary_coilspring_make=models.CharField(max_length=20,null=True)
    motor_check=models.CharField(max_length=20,null=True)
    motor_date=models.CharField(max_length=20,null=True)
    lowering_check=models.CharField(max_length=20,null=True)
    lowering_date=models.CharField(max_length=20,null=True)
    dispatch_check=models.CharField(max_length=20,null=True)
    dispatch_check_date=models.CharField(max_length=20,null=True)
    loco_paper=models.CharField(max_length=20,null=True)
    locopaper_date=models.CharField(max_length=20,null=True)
    h_plate=models.CharField(max_length=20,null=True)
    torque_support=models.CharField(max_length=20,null=True)