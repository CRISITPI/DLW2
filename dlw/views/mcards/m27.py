from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/m27view/')
def m27view(request):
    pa_no = empmast.objects.none()
    
    mon="dd-mm-yyyy"
    stfrate="staff rate"
    stfname="staff name"
    stfdesg="staff designation"
    if "Superuser" in g.rolelist: 
        shop_sec_temp = request.POST.get('shop_sec')
        stfno_temp = request.POST.get('staffNo')
        getDateList = list(M21DOCNEW1.objects.filter(shop_sec=shop_sec_temp,staff_no=stfno_temp).values('date').exclude(date__isnull=True)) 
        tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'stfname': stfname,
            'usermaster':g.usermaster,
            'stfdesg': stfdesg,
            'stfrate': stfrate,
            'getDateList':getDateList,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = Oprn.objects.all().filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            pa_no =pa_no | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'pa_no':pa_no,
            'roles' :tmp,
            'usermaster':g.usermaster,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'getDateList':getDateList,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'ip':get_client_ip(request),
            'roles' :tmp,
            'usermaster':g.usermaster,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'getDateList':getDateList,
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            mon=request.POST.get('date1')
            shop_sec = request.POST.get('shop_sec')
            stfno = request.POST.get('staffNo')
            stfname = request.POST.get('staffName')
            stfdesg = request.POST.get('staffDesg')
            stfrate = request.POST.get('staffRate')
            wono=[]
            ex=list(Batch.objects.all().values('bo_no').exclude(bo_no__isnull=True).distinct())
            for i in ex:
                wono.append(i['bo_no'])
            if "Superuser" in g.rolelist:
                   
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'sub': 1,
                        'mon':mon,
                        'stfno':stfno,
                        'shopsec': shop_sec,
                        'stfname': stfname,
                        'stfdesg': stfdesg,
                        'stfrate': stfrate,
                        'usermaster':g.usermaster,
                        'subnav':g.subnav,
                        'totindb':0,
                        'batch_no':wono,
                        'getDateList':getDateList,
                  }
            elif(len(g.rolelist)==1):
                  for i in range(0,len(g.rolelist)):

                        w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                        req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                        wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :tmp,
                        'usermaster':g.usermaster,
                        'lenm' :len(g.rolelist),
                        'nav': g.nav,
                        'ip': get_client_ip(request),
                        'sub': 1,
                        'mon':mon,
                        'stfno':stfno,
                        'shopsec': shop_sec,
                        'stfname': stfname,
                        'stfdesg': stfdesg,
                        'subnav':g.subnav,
                        'getDateList':getDateList,
                  }
            elif(len(g.rolelist)>1):
                  context = {
                        'lenm' :len(g.rolelist),
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'usermaster':g.usermaster,
                        'roles' :tmp,
                        'sub': 1,
                        'mon':mon,
                        'stfno':stfno,
                        'shopsec': shop_sec,
                        'stfname': stfname,
                        'stfdesg': stfdesg,
                        'subnav':g.subnav,
                        'getDateList':getDateList,
                  }

        if submitvalue=='Save':
            date1=request.POST.get('date1')
            shop_sec=request.POST.get('shopsec')
            staffNo=request.POST.get('stfno')
            staffName=request.POST.get('stfname')
            staffDesg =request.POST.get('stfdesg')
            staffRate=request.POST.get('staffRate')
            tot = request.POST.get('total')
            tot=int(tot)+1
            for i in range(1,int(tot)):    
                wono = request.POST.get("wono"+str(i))
                wodate = request.POST.get("wodate"+str(i))
                ofcdate = request.POST.get("ofcdate"+str(i))
                tothrs = request.POST.get("tothrs"+str(i))
                M27TimeSheet.objects.create(shop_sec=shop_sec, staff_no=staffNo, rate=staffRate, month=date1, tot_hrs=tothrs, ofc_date=ofcdate, wo_date=wodate, wo_no=wono, desg=staffDesg, name=staffName)

            emp_detail= emp_details.objects.filter(card_details='M27').values('email_id','mobileno')   
            mob_temp=[]            
            for i in emp_detail: 
                mob_temp.append(i['mobileno'])
            for j in range(len(mob_temp)):
                smsM18(mob_temp[j],"Dear Employee TimeSheet of indirect labour(M27) card has been generated.")          
            messages.success(request, 'Successfully Saved !')     
    return render(request,'MCARD/M27CARD/m27view1.html',context) 



def m27getStaffNo(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        date = request.GET.get('date')
        staff_no = list(M5SHEMP.objects.filter(shopsec = shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m27getDetails(request):
    if request.method == "GET" and request.is_ajax():
        staffNo = request.GET.get('staffNo')        
        getdetail = list(M5SHEMP.objects.filter(staff_no = staffNo).values('name','desgn').exclude(name__isnull=True).distinct())
        return JsonResponse(getdetail, safe = False)
    return JsonResponse({"success":False}, status=400)


def m27getDesignation(request): 
    if request.method == "GET" and request.is_ajax():
        staffNo = request.GET.get('staffNo')    
        staffName = request.GET.get('staffName')      
        getdetaildesgn = list(M5SHEMP.objects.filter(staff_no = staffNo, name = staffName).values('desgn').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(getdetaildesgn, safe = False)
    return JsonResponse({"success":False}, status=400)

def m27getWorkOrder(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m27getWorkOrderDate(request):
    if request.method == "GET" and request.is_ajax():
        wono = request.GET.get('wo')
        wono1 = list(Batch.objects.filter(bo_no = wono).values('b_expl_dt').exclude(bo_no__isnull=True).exclude(b_expl_dt__isnull=True).distinct())
        return JsonResponse(wono1, safe = False)
    return JsonResponse({"success":False}, status=400)

def m27getBatchNo(request):
    if request.method == "GET" and request.is_ajax():
        mAsslyno = request.GET.get('mAsslyno')
        bo_no=Batch.objects.filter(part_no=mAsslyno).values('bo_no').distinct()
        bo_no_temp = list(bo_no)
        return JsonResponse(bo_no_temp, safe = False)
    return JsonResponse({"success": False}, status=400)


def m27getWorkOrder(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)



