from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/spptalot/')
def spptalot(request):
    
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
        'usermaster':g.usermaster
    }     
    return render(request,'SHOPADMIN/SPPTALOT/spptalot.html',context)


Viewstate_slno=0
def txtPart_No_TextChanged(request):
    if request.method == "GET" and request.is_ajax():
        txtpart_no = request.GET.get('txtPart_No')
        if txtpart_no == "":
            l1=[0]
            return JsonResponse(l1,safe = False)
        else:
            part = list(Sppart.objects.filter(part_no=txtpart_no).values('part_no','name','descr','dimension','used_mc1','used_mc2','used_mc3','used_mc4','used_ge_mc','reord_qty','shop_ut'))
            if len(part) > 0:
                return JsonResponse(part,safe = False)
            else:
                l1=[1]
                return JsonResponse(l1,safe = False)
    return JsonResponse({"success":False}, status = 400)  

def txtShop_ut_TextChanged(request):
    if request.method == "GET" and request.is_ajax():
        txtShop_ut = request.GET.get('txtShop_ut')
        code = list(Code.objects.filter(cd_type='51',code=txtShop_ut).values('cd_type','code','alpha_1','alpha_2','num_1','num_2','num_3','txt','flag','gen_info','lupd_date','rec_ind','gm_ptno','epc_old'))
        if len(code) == 0:
            l1=[0]
            return JsonResponse(l1,safe = False)
        obj=[]
        return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status = 400)  

def groupvalues(request):
    if request.method == "GET" and request.is_ajax():
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT "MAJ_GRP","MAJ_DESCR" FROM public."SPPTGRP" ORDER BY %s',[1])
        row = cursor.fetchall()
        dt=list(row)
        return JsonResponse(dt,safe = False)
    return JsonResponse({"success":False}, status = 400)  

def usedmachine(request):
    if request.method == "GET" and request.is_ajax():
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT "MWNO","DES" FROM public."MP" WHERE "MWNO" IS NOT NULL ORDER BY %s',[1])
        row = cursor.fetchall()
        dt=list(row)
        return JsonResponse(dt,safe = False)
    return JsonResponse({"success":False}, status = 400)  

def txtMaj_grp_TextChanged(request):
    if request.method == "GET" and request.is_ajax():
        groupval = request.GET.get('group')
        grp = list(Spptgrp.objects.filter(maj_grp=groupval).values('slno'))
        return JsonResponse(grp,safe = False)
    return JsonResponse({"success":False}, status = 400)  

def Unit_List(request):
    if request.method == "GET" and request.is_ajax():
        codes=list(Code.objects.filter(cd_type='51').values('code','alpha_1'))
        if len(codes) > 0 :
            print("codes are",codes)
            return JsonResponse(codes,safe = False)
    return JsonResponse({"success":False}, status = 400)  

def BtnSave_Click(request):
    if request.method == "GET" and request.is_ajax():
        txtPart_No = request.GET.get('txtPart_No')
        txtName = request.GET.get('txtName')
        txtMaj_grp = request.GET.get('txtMaj_grp')
        txtSlNo = request.GET.get('txtSlNo')
        txtDescr = request.GET.get('txtDescr')
        txtDimension = request.GET.get('txtDimension')
        txtShop_ut = request.GET.get('txtShop_ut')
        txtUsed_mc1 = request.GET.get('txtUsed_mc1')
        txtUsed_mc2 = request.GET.get('txtUsed_mc2')
        txtUsed_mc3 = request.GET.get('txtUsed_mc3')
        txtUsed_mc4 = request.GET.get('txtUsed_mc4')
        txtUsed_ge_mc = request.GET.get('txtUsed_ge_mc')
        txtReOrd_qty = request.GET.get('txtReOrd_qty')
        print("values received are",txtPart_No,txtName,txtMaj_grp,txtSlNo,txtDescr,txtDimension,txtShop_ut,txtUsed_mc1,txtUsed_mc2,txtUsed_mc3,txtUsed_mc4,txtUsed_ge_mc,txtReOrd_qty)
        global Viewstate_slno
        Viewstate_slno=txtSlNo
        dte=datetime.datetime.today().strftime("%Y-%m-%d")
        if txtName == "":
            a=[0]
            return JsonResponse(a,safe = False)
        if txtDescr == "":
            print("desc")
            a=[1]
            return JsonResponse(a,safe = False)
        if txtMaj_grp == "":
            a=[2]
            return JsonResponse(a,safe = False)
        if txtMaj_grp != "":
            grp = list(Spptgrp.objects.filter(maj_grp=txtMaj_grp).values('slno'))
            if len(grp) > 0:
                slno=grp[0]['slno']+1
                if Decimal(txtSlNo) > slno:
                    txtSlNo=slno
                    Viewstate_slno=txtSlNo
            else:
                a=[3,txtMaj_grp]
                return JsonResponse(a,safe = False)
        if txtPart_No != "":
            part = list(Sppart.objects.filter(part_no=txtPart_No).values('part_no','name','descr','dimension'))
            if len(part) ==0:
                a=[4]
                return JsonResponse(a,safe = False)
            else:
                a=[5]
                print("update statement")
                dt2=Sppart.objects.filter(part_no=txtPart_No).update(name=txtName,descr=txtDescr,dimension=txtDimension,used_mc1=txtUsed_mc1,used_mc2=txtUsed_mc2,used_mc3=txtUsed_mc3,used_mc4=txtUsed_mc4,used_ge_mc=txtUsed_ge_mc,reord_qty=txtReOrd_qty,shop_ut=txtShop_ut,open_date=dte,updt_dt=dte)
                if dt2 != 0:
                    print("data updated")
                return JsonResponse(a,safe = False)
        else:
            print("insert here")
            if Viewstate_slno == 0:
                grp1 = list(Spptgrp.objects.filter(maj_grp=txtMaj_grp).values('slno'))
                if len(grp1) > 0 and Decimal(txtSlNo) > slno:
                    txtSlNo=slno
                    Viewstate_slno=txtSlNo
            n=Viewstate_slno.zfill(3)
            print("padded value is",n)
            Viewstate_partno="S"+txtMaj_grp+n+"0"
            if txtReOrd_qty != "":
                dt1=Sppart.objects.create(part_no=Viewstate_partno,name=txtName,descr=txtDescr,dimension=txtDimension,used_mc1=txtUsed_mc1,used_mc2=txtUsed_mc2,used_mc3=txtUsed_mc3,used_mc4=txtUsed_mc4,used_ge_mc=txtUsed_ge_mc,reord_qty=txtReOrd_qty,shop_ut=txtShop_ut,open_date=dte,updt_dt=dte)
                if dt1 != 0:
                    print("insertion successfull")
                    obj=[6,n]
                    return JsonResponse(obj,safe = False)
            else:
                dt1=Sppart.objects.create(part_no=Viewstate_partno,name=txtName,descr=txtDescr,dimension=txtDimension,used_mc1=txtUsed_mc1,used_mc2=txtUsed_mc2,used_mc3=txtUsed_mc3,used_mc4=txtUsed_mc4,used_ge_mc=txtUsed_ge_mc,shop_ut=txtShop_ut,open_date=dte,updt_dt=dte)
                if dt1 != 0:
                    print("insertion successfull")
                    obj=[6,n]
                    return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status = 400)  
