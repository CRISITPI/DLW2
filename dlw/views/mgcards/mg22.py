from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/MG22view/')
def MG22view(request):
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    rolelist=(g.usermaster).role.split(", ")
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    wo_nop = empmast.objects.none()
    dictemper={}
    totindb=0
    if "Superuser" in rolelist:        
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'lvdate':"dd-mm-yy",
            'usermaster':g.usermaster,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'lvdate':"dd-mm-yy",
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'lvdate':"dd-mm-yy",
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Add':
            rolelist=(g.usermaster).role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            lvdate=request.POST.get('updt_date')
            m2=MG22new.objects.filter(shop_sec=shop_sec,updt_date=lvdate).last()
            mm=0
            if m2 is not None:
                temper = {str(mm):{"name":m2.name,
                                               "ticketno":m2.ticketno,"cause":m2.cause,
                        "acdate":m2.acc_Date,"superv":m2.sec_sup,"mistry":m2.mistry,"chargeman":m2.chargeman,
                                               }}
                           
                totindb=totindb+1

                dictemper.update(copy.deepcopy(temper))

            emp=[]
            staff_name = request.GET.get('empname')
            empname = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname')
            if empname is not None and len(empname):
                for i in range(len(empname)):
                    emp.append(empname[i]['empname'])

            w1=M5SHEMP.objects.filter(shopsec=shop_sec).values('name').distinct()
            wono=[]
            for w in range(len(w1)):
                wono.append(w1[w]['name'])
            alt_date="mm-dd-yy"
            if "Superuser" in rolelist:
                 
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'names':wono,
                    'usermaster':g.usermaster,
                    'dictemper':dictemper,
                    'totindb':totindb,
                    'empname':emp,
                    'alt_date':alt_date,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
                    req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'sub':1,
                    'subnav':g.subnav,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                }
        if submitvalue=='Save':
             
            updt_date = request.POST.get('updt_date')
            shop_sec = request.POST.get('shop_sec')
            name=request.POST.get('name1')
            staff_no = request.POST.get('staff_no')
            ticketno = request.POST.get('ticket')
            acc_Date = request.POST.get('datename')
            cause = request.POST.get('cause')
            reason_neg = request.POST.get('reason_neg')
            reason_y_neg = request.POST.get('reason_y_neg')
            equip_check = request.POST.get('equip_check')
            suggestions = request.POST.get('suggestion')
            bgc = request.POST.get('bgc')
            bgc2 = request.POST.get('bgc2')
            sec_sup = request.POST.get('sec_sup')
            chargeman = request.POST.get('Chargeman')
            mistry = request.POST.get('Mistry')
            c1 = request.POST.get('c1')
            c2 = request.POST.get('c2')
            c3 = request.POST.get('c3')
            c4 = request.POST.get('c4')
            a1 = request.POST.get('a1')
            a2 = request.POST.get('a2')
            a3 = request.POST.get('a3')
            SSFO = request.POST.get('SSFO')
              
            
            MG22new.objects.create(updt_date=str(updt_date), shop_sec = str(shop_sec),name=str(name),staff_no=str(staff_no), ticketno=str(ticketno), acc_Date =str(acc_Date),cause = str(cause), reason_neg = str(reason_neg), reason_y_neg= str(reason_y_neg),equip_check= str(equip_check), suggestions = str(suggestions), bgc= str(bgc), bgc2= str(bgc2), sec_sup= str(sec_sup), chargeman = str(chargeman), mistry= str(mistry),c1 = str(c1), c2 = str(c2), c3 = str(c3), c4 =str(c4), a1= str(a1), a2= str(a2), a3= str(a3), ssfo= str(SSFO) )

            messages.success(request, 'Successfully Saved !!!, Select new values to update')
    return render(request, "MGCARD/MG22CARD/MG22view.html", context)


def mg22getstaffno(request):
    if request.method == "GET" and request.is_ajax():  
        from.models import Batch      
        shop_sec = request.GET.get('shop_sec')
        name=request.GET.get('name')
        w1=M5SHEMP.objects.filter(shopsec=shop_sec,name=name).values('staff_no').distinct()
        wono = w1[0]['staff_no']
        cont ={
            "wono":wono,
        }
        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg22getstaffName(request):
    if request.method == "GET" and request.is_ajax():  
        from .models import Batch     
        shop_sec = request.GET.get('shop_sec')
        staff_no = request.GET.get('staff_no')
        w1=M5SHEMP.objects.filter(staff_no=staff_no).values('staff_no','name').distinct()
        wono = list(w1)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/MG22report/')
def mg22report(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = empmast.objects.none()
    dictemper={}
    totindb=0
    emp=[]
    empname = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname')
    if empname is not None and len(empname):
        for i in range(len(empname)):
            emp.append(empname[i]['empname'])

    w1=M5SHEMP.objects.all().values('name').distinct().exclude(name__isnull=True)
    wono=[]
    for w in range(len(w1)):
        wono.append(w1[w]['name'])
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'names':wono,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'lvdate':"yyyy-mm-dd",
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"yyyy-mm-dd",
            'names':wono,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"yyyy-mm-dd",
            'names':wono,
        }
    if request.method=="POST":
        bvalue=request.POST.get('proceed')
        shop_sec=request.POST.get('shop_sec')
        lvdate=request.POST.get('updt_date')
        empname=request.POST.get('emp_name')
        accdate=request.POST.get('accdate')
        if bvalue=='Proceed':
            m2=MG22new.objects.filter(shop_sec=shop_sec,updt_date=lvdate,name=empname,acc_Date=accdate).first()
            nocertf=0
            mm=0
            if m2 is not None:
                if m2.c1 or m2.c2 or m2.c3 or m2.c4 is not None:
                    nocertf=1
                temper = {str(mm):{"name":m2.name,
                                               "ticketno":m2.ticketno,"cause":m2.cause,"bgc2":m2.bgc2,
                        "acdate":m2.acc_Date,"superv":m2.sec_sup,"mistry":m2.mistry,"chargeman":m2.chargeman,"ssfoname":m2.ssfo,
                        "reasonneg":m2.reason_neg,"epchck":m2.equip_check,"sugg":m2.suggestions,
                        "cert1":m2.c1,"cert2":m2.c2,"cert3":m2.c3,"cert4":m2.c4,"firstacc":m2.bgc,
                        "anex1":m2.a1,"anex2":m2.a2,"anex3":m2.a3,
                                               }}

                totindb=1
                dictemper.update(copy.deepcopy(temper))
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'names':wono,
                    'dictemper':dictemper,
                    'totindb':totindb,
                    'empname':emp,
                    "nocertf":nocertf,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
                    req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'sub':1,
                    'subnav':subnav,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                }

    return render(request,"MGCARD/MG22CARD/mg22report.html",context)





