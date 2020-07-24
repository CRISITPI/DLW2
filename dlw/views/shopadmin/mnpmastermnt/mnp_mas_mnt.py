from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/mnp_entr/')
def mnp_entr(request):
    
    wo_nop = empmast.objects.none()
     
    tm=shop_section.objects.all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'usermaster':g.usermaster,
    }
     
    return render(request,'SHOPADMIN/MNPMASTERMNT/mnp_entr.html',context)
def mwnochanged(request):
    if request.method == 'GET' and request.is_ajax():
        txtmwno = request.GET.get('Txt_mw')    
        if not txtmwno == "":
            data_list=list(Mnp.objects.filter(mwno=txtmwno).values('mwno','descr','maint_area','location','bay','mw_cat','shopsec','sh_name','lc_no','no_shift','category','dt_of_comm','make','eqp_type','mc_type_gr','used_for','unit','cost','available','condition','replace_by','date_tr_c','capacity','required','yr_scrap','load_cente','status','cat_code','updt_dt'))
            if(len(data_list)>0):
                return JsonResponse(data_list,safe = False)
        
    return JsonResponse({"success":False}, status = 400)

def mwsave(request):
    if request.method == 'GET' and request.is_ajax():
         txtMwNo=request.GET.get('txtMwNo')
         txtDescr=request.GET.get('txtDescr')
         txtShopSec=request.GET.get('txtShopSec')
         txtSh_name=request.GET.get('txtSh_name')
         txtLc_no=request.GET.get('txtLc_no')
         txtBay=request.GET.get('txtBay')
         ddMaintArea=request.GET.get('ddMaintArea')
         txtNo_shift=request.GET.get('txtNo_shift')
         if(txtNo_shift==""):
             txtNo_shift=None
         ddCategory=request.GET.get('ddCategory')
         txtDt_of_comm=request.GET.get('txtDt_of_comm')
         if txtDt_of_comm != "":
            ts=txtDt_of_comm.split('-')
            txtDt_of_comm=ts[2]+"-"+ts[1]+"-"+ts[0]
         txtLocation=request.GET.get('txtLocation')
         txtEqp_type=request.GET.get('txtEqp_type')
         txtMC_Type_GR=request.GET.get('txtMC_Type_GR')
         txtCost=request.GET.get('txtCost')
         if(txtCost==""):
             txtCost=None
         txtUnit=request.GET.get('txtUnit')
         txtAvailable=request.GET.get('txtAvailable')
         txtReplace_by=request.GET.get('txtReplace_by')
         if(txtReplace_by==""):
             txtReplace_by=None
         txtDate_TR_C=request.GET.get('txtDate_TR_C')
         if txtDate_TR_C != "":
             ps=txtDate_TR_C.split('-')
             txtDate_TR_C=ps[2]+"-"+ps[1]+"-"+ps[0]
         txtCapacity=request.GET.get('txtCapacity')
         txtReq=request.GET.get('txtReq')
         txtYR_Scrap=request.GET.get('txtYR_Scrap')
         if txtYR_Scrap != "":
             ls=txtYR_Scrap.split('-')
             txtYR_Scrap=ls[2]+"-"+ls[1]+"-"+ls[0]
         txtCondition=request.GET.get('txtCondition')
         txtMake=request.GET.get('txtMake')
         txtUsed_for=request.GET.get('txtUsed_for')
         data_list1=list(Mnp.objects.filter(mwno=txtMwNo).values('mwno','descr','maint_area','location','bay','mw_cat','shopsec','sh_name','lc_no','no_shift','category','dt_of_comm','make','eqp_type','mc_type_gr','used_for','unit','cost','available','condition','replace_by','date_tr_c','capacity','required','yr_scrap','load_cente','status','cat_code','updt_dt'))
         dt=datetime.date.today()
         if len(data_list1) == 0  :
            
            if txtDescr == "" :
                
                return JsonResponse({"success":False}, status = 400)  
            if txtLocation == "" :
                
                return JsonResponse({"success":False}, status = 400)
            if ddCategory == "" :
                
                return JsonResponse({"success":False}, status = 400)
            if ddMaintArea == "":
                
                return JsonResponse({"success":False}, status = 400)
             
            if txtDt_of_comm =="" and txtDate_TR_C == "" and txtYR_Scrap == "":
                
                Mnp.objects.create(mwno=str(txtMwNo),descr=str(txtDescr),location=str(txtLocation),category=str(ddCategory),
                maint_area=str(ddMaintArea),bay=str(txtBay),shopsec=str(txtShopSec),sh_name=str(txtSh_name),lc_no=str(txtLc_no),
                no_shift=txtNo_shift,eqp_type=str(txtEqp_type),mc_type_gr=str(txtMC_Type_GR),cost=txtCost,unit=str(txtUnit),
                available=str(txtAvailable),replace_by=txtReplace_by,capacity=str(txtCapacity),required=str(txtReq),
                condition=str(txtCondition),make=str(txtMake),used_for=str(txtUsed_for),updt_dt=dt)
            elif txtDt_of_comm =="" and txtDate_TR_C != "" and txtYR_Scrap != "":
                
                Mnp.objects.create(mwno=str(txtMwNo),descr=str(txtDescr),location=str(txtLocation),category=str(ddCategory),
                maint_area=str(ddMaintArea),bay=str(txtBay),shopsec=str(txtShopSec),sh_name=str(txtSh_name),lc_no=str(txtLc_no),
                no_shift=txtNo_shift,eqp_type=str(txtEqp_type),date_tr_c=txtDate_TR_C,yr_scrap=txtYR_Scrap,
                mc_type_gr=str(txtMC_Type_GR),cost=txtCost,unit=str(txtUnit),available=str(txtAvailable),replace_by=txtReplace_by,
                capacity=str(txtCapacity),required=str(txtReq),condition=str(txtCondition),make=str(txtMake),used_for=str(txtUsed_for),updt_dt=dt)
            elif txtDate_TR_C == "" and txtDt_of_comm !="" and txtYR_Scrap != "":
                
                Mnp.objects.create(mwno=str(txtMwNo),descr=str(txtDescr),location=str(txtLocation),category=str(ddCategory),
                maint_area=str(ddMaintArea),bay=str(txtBay),shopsec=str(txtShopSec),sh_name=str(txtSh_name),lc_no=str(txtLc_no),
                no_shift=txtNo_shift,eqp_type=str(txtEqp_type),dt_of_comm=txtDt_of_comm,yr_scrap=txtYR_Scrap,
                mc_type_gr=str(txtMC_Type_GR),cost=txtCost,unit=str(txtUnit),available=str(txtAvailable),replace_by=txtReplace_by,
                capacity=str(txtCapacity),required=str(txtReq),condition=str(txtCondition),make=str(txtMake),used_for=str(txtUsed_for),updt_dt=dt)
            elif txtYR_Scrap == "" and txtDt_of_comm !="" and txtDate_TR_C != "":
                
                Mnp.objects.create(mwno=str(txtMwNo),descr=str(txtDescr),location=str(txtLocation),category=str(ddCategory),
                maint_area=str(ddMaintArea),bay=str(txtBay),shopsec=str(txtShopSec),sh_name=str(txtSh_name),lc_no=str(txtLc_no),
                no_shift=txtNo_shift,eqp_type=str(txtEqp_type),dt_of_comm=txtDt_of_comm,date_tr_c=txtDate_TR_C,
                mc_type_gr=str(txtMC_Type_GR),cost=txtCost,unit=str(txtUnit),available=str(txtAvailable),replace_by=txtReplace_by,
                capacity=str(txtCapacity),required=str(txtReq),condition=str(txtCondition),make=str(txtMake),used_for=str(txtUsed_for),updt_dt=dt)
            elif txtDt_of_comm =="" and txtDate_TR_C == "" and txtYR_Scrap != "":
                
                Mnp.objects.create(mwno=str(txtMwNo),descr=str(txtDescr),location=str(txtLocation),category=str(ddCategory),
                maint_area=str(ddMaintArea),bay=str(txtBay),shopsec=str(txtShopSec),sh_name=str(txtSh_name),lc_no=str(txtLc_no),
                no_shift=txtNo_shift,eqp_type=str(txtEqp_type),yr_scrap=txtYR_Scrap,
                mc_type_gr=str(txtMC_Type_GR),cost=txtCost,unit=str(txtUnit),available=str(txtAvailable),replace_by=txtReplace_by,
                capacity=str(txtCapacity),required=str(txtReq),condition=str(txtCondition),make=str(txtMake),used_for=str(txtUsed_for),updt_dt=dt)
            
            elif txtDt_of_comm =="" and txtDate_TR_C != "" and txtYR_Scrap == "":
                
                Mnp.objects.create(mwno=str(txtMwNo),descr=str(txtDescr),location=str(txtLocation),category=str(ddCategory),
                maint_area=str(ddMaintArea),bay=str(txtBay),shopsec=str(txtShopSec),sh_name=str(txtSh_name),lc_no=str(txtLc_no),
                no_shift=txtNo_shift,eqp_type=str(txtEqp_type),date_tr_c=txtDate_TR_C,
                mc_type_gr=str(txtMC_Type_GR),cost=txtCost,unit=str(txtUnit),available=str(txtAvailable),replace_by=txtReplace_by,
                capacity=str(txtCapacity),required=str(txtReq),condition=str(txtCondition),make=str(txtMake),used_for=str(txtUsed_for),updt_dt=dt)
             
            elif txtDt_of_comm !="" and txtDate_TR_C == "" and txtYR_Scrap == "":
                
                Mnp.objects.create(mwno=str(txtMwNo),descr=str(txtDescr),location=str(txtLocation),category=str(ddCategory),
                maint_area=str(ddMaintArea),bay=str(txtBay),shopsec=str(txtShopSec),sh_name=str(txtSh_name),lc_no=str(txtLc_no),
                no_shift=txtNo_shift,eqp_type=str(txtEqp_type),dt_of_comm=txtDt_of_comm,
                mc_type_gr=str(txtMC_Type_GR),cost=txtCost,unit=str(txtUnit),available=str(txtAvailable),replace_by=txtReplace_by,
                capacity=str(txtCapacity),required=str(txtReq),condition=str(txtCondition),make=str(txtMake),used_for=str(txtUsed_for),updt_dt=dt)
            
            else:
                
                Mnp.objects.create(mwno=str(txtMwNo),descr=str(txtDescr),location=str(txtLocation),category=str(ddCategory),
                maint_area=str(ddMaintArea),bay=str(txtBay),shopsec=str(txtShopSec),sh_name=str(txtSh_name),lc_no=str(txtLc_no),
                no_shift=txtNo_shift,eqp_type=str(txtEqp_type),dt_of_comm=txtDt_of_comm,date_tr_c=txtDate_TR_C,yr_scrap=txtYR_Scrap,
                mc_type_gr=str(txtMC_Type_GR),cost=txtCost,unit=str(txtUnit),available=str(txtAvailable),replace_by=txtReplace_by,
                capacity=str(txtCapacity),required=str(txtReq),condition=str(txtCondition),make=str(txtMake),used_for=str(txtUsed_for),updt_dt=dt)
            
            
            obj=[]
            return JsonResponse(obj,safe = False)
         else:
            
            Mnp.objects.filter(mwno=txtMwNo).update(descr=str(txtDescr),location=str(txtLocation),category=str(ddCategory),
                maint_area=str(ddMaintArea),bay=str(txtBay),shopsec=str(txtShopSec),sh_name=str(txtSh_name),lc_no=str(txtLc_no),
                no_shift=txtNo_shift,eqp_type=str(txtEqp_type),dt_of_comm=txtDt_of_comm,date_tr_c=txtDate_TR_C,yr_scrap=txtYR_Scrap,
                mc_type_gr=str(txtMC_Type_GR),cost=txtCost,unit=str(txtUnit),available=str(txtAvailable),replace_by=txtReplace_by,
                capacity=str(txtCapacity),required=str(txtReq),condition=str(txtCondition),make=str(txtMake),used_for=str(txtUsed_for),
                load_cente=str(txtLc_no),updt_dt=dt)
            
            obj=[]
            return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status = 400)
