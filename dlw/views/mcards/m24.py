from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/M24views/')
def M24views(request):
    
    wo_nop = empmast.objects.none()
    staff_no = Shemp.objects.values('staff_no').exclude(staff_no__isnull=True).distinct()
    prtlist=[]
    for i in staff_no:
        prtlist.append(i['staff_no'])
    
    desgn = Shemp.objects.values('desgn').exclude(desgn__isnull=True).distinct()
    prtdesgn=[]
    for i in desgn:
        prtdesgn.append(i['desgn'])

    payrate = empmast.objects.values('payrate').exclude(payrate__isnull=True).distinct()
    prtpay=[]
    for i in payrate:
        prtpay.append(i['payrate'])

    superv = empmast.objects.values('empno').exclude(scalecode__isnull=True).distinct()
    prtemp=[]
    for i in superv:
        prtemp.append(i['empno'])

    
    if "Superuser" in g.rolelist:
        tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
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
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
            'usermaster':g.usermaster,

        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = M24.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist,
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist,
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
        
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
       
        if submitvalue=='Proceed':
            fr_date = request.POST.get('fr_date')
            to_date = request.POST.get('to_date')
            shop_sec = request.POST.get('shop_sec')
            ssfo = request.POST.get('ssfo')
            timekeep = request.POST.get('timekeep')
            workshop = request.POST.get('workshop')
            
            obj1 = M24.objects.filter(shop_sec=shop_sec,staff_no=ssfo).values('sno','fr_date','to_date','timekeep','workshop','staff_no','desgn','payrate','supervise_chrgmn','hrs_wrked','rsn_ovrtym').distinct()
      
            leng=obj1.count()
            
            context = {
                'obj1': obj1,
                'mytry':"rimjhim",
                'lent': leng,
                'leng':leng,
                'shop_sec': shop_sec,
                'to_date': to_date,
                'staff_no':staff_no, 
                'ssfo':ssfo,
                'prtlist':prtlist,
                'prtpay':prtpay,
                'prtdesgn':prtdesgn,
                'prtemp':prtemp,
                'timekeep':timekeep,
                'workshop':workshop,
                'fr_date':fr_date,
                'sub': 1, 
                      
            }
        if submitvalue=='submit':
            leng=request.POST.get('len')
            tot= request.POST.get('total')
            tot = int(tot)+1
            for i in range(1,int(tot)):
                fr_date = request.POST.get('fr_date')
                to_date = request.POST.get('to_date')
                shop_sec= request.POST.get('shop_sec')
                ssfo = request.POST.get('ssfo')    
                timekeep = request.POST.get('timekeep')      
                workshop = request.POST.get('workshop')
                sno = request.POST.get('sno'+str(i))
                staff_no = request.POST.get('staff_no')
                designation = request.POST.get('designation')
                payrate = request.POST.get('payrate')
                supervise = request.POST.get('supervise') 
                             
                hrs_wrkd = request.POST.get('hrs_wrkd'+str(i))
                reason = request.POST.get('reason'+str(i))

                M24.objects.create(shop_sec=str(shop_sec),ssfo=str(ssfo),timekeep=str(timekeep),workshop=str(workshop),sno=str(sno),staff_no=str(staff_no),desgn=str(designation),payrate=str(payrate),supervise_chrgmn=str(supervise),hrs_wrked=str(hrs_wrkd),rsn_ovrtym=str(reason),fr_date=str(fr_date),to_date=str(to_date))

    return render(request,"MCARD/M24CARD/M24views.html",context)                        



@login_required
@role_required(urlpass='/m24report/')
def m24report(request):
    
    staff_no = Shemp.objects.values('staff_no').exclude(staff_no__isnull=True).distinct()
    prtlist=[]
    for i in staff_no:
        prtlist.append(i['staff_no'])

    desgn = Shemp.objects.values('desgn').exclude(desgn__isnull=True).distinct()
    prtdesgn=[]
    for i in desgn:
        prtdesgn.append(i['desgn'])

    payrate = empmast.objects.values('payrate').exclude(payrate__isnull=True).distinct()
    prtpay=[]
    for i in payrate:
        prtpay.append(i['payrate'])

    superv = empmast.objects.values('empno').exclude(scalecode__isnull=True).distinct()
    prtemp=[]
    for i in superv:
        prtemp.append(i['empno'])

    
    if "Superuser" in g.rolelist:
        tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
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
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = M24.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist,
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist,
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
        
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
       
        if submitvalue=='Proceed':
            fr_date = request.POST.get('fr_date')
            to_date = request.POST.get('to_date')
            shop_sec = request.POST.get('shop_sec')
            ssfo = request.POST.get('ssfo')
            obj1=0
            obj2=0
            leng2=0
            obj = M24.objects.filter(shop_sec=shop_sec,ssfo=ssfo).values('timekeep','workshop').distinct()
            obj1 = M24.objects.filter(shop_sec=shop_sec,ssfo=ssfo).values('sno','staff_no','desgn','payrate','supervise_chrgmn','hrs_wrked','rsn_ovrtym').distinct()
            if len(obj1):
                staff=obj1[0]['supervise_chrgmn']
                obj2 = empmast.objects.filter(empno=staff).values('empname').distinct()
                leng2=obj2.count()
            leth=obj.count()
            leng=obj1.count()
            
            
            context = {
                'obj1': obj1,
                'obj': obj,
                'obj2':obj2,
                'leth':leth,
                'len2':leng2,
                'mytry':"rimjhim",
                'lent': leng,
                'leng':leng,
                'shop_sec': shop_sec,
                'to_date': to_date,
                'staff_no':staff_no, 
                'ssfo':ssfo,
                'prtlist':prtlist,
                'prtpay':prtpay,
                'prtdesgn':prtdesgn,
                'prtemp':prtemp,
                'fr_date':fr_date,
                'sub': 1, 
                      
            }
    
    return render(request,"MCARD/M24CARD/m24report.html",context)


def m24getssfo(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        w1=list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())                             
        return JsonResponse(w1, safe = False)
    return JsonResponse({"success":False}, status=400)


def m24getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m24getdesgn(request):
    if request.method == "GET" and request.is_ajax():
        staff_no = request.GET.get('staff_no')
        w2=list(Shemp.objects.filter(staff_no=staff_no).values('designation').distinct())
        return JsonResponse(w2, safe = False)
    return JsonResponse({"success":False}, status=400)


def m24getsuprvsr(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        ss_fo = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(ss_fo, safe = False)
    return JsonResponse({"success":False}, status=400)

