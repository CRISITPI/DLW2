from dlw.views import *
import dlw.views.globals as g

def m13viewgetwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = list(M13.objects.filter(shop = shop_sec).values('wo').distinct())
        return JsonResponse(wo_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m13viewgetpano(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        part_no = list(M13.objects.filter(shop = shop_sec,wo=wo_no).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m13getno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        part_no = request.GET.get('part_nop')
        pp = list(M13.objects.filter(shop=shop_sec,part_no=part_no,wo=wo_no).values('m13_no').distinct())
        return JsonResponse(pp, safe = False)
    return JsonResponse({"success":False}, status=400)

def m13getslno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        part_no = request.GET.get('part_nop')
        m13_no = request.GET.get('m13_no')
        sl = list(M13.objects.filter(shop=shop_sec,part_no=part_no,wo=wo_no,m13_no=m13_no).values('slno').distinct())
        return JsonResponse(sl, safe = False)
    return JsonResponse({"success":False}, status=400)

def m13getdata(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        part_no = request.GET.get('part_nop')
        m13_no = request.GET.get('m13_no')
        slno = request.GET.get('slno')
        obj = list(M13.objects.filter(shop=str(shop_sec),part_no=str(part_no),wo=str(wo_no),m13_no=str(m13_no),slno=str(slno)).values('m13_no','m13_date','qty_tot','qty_ins','qty_pas','qty_rej','opn','vendor_cd','fault_cd','staff_no','reason','slno','m13_sn','wo_rep','m15_no','epc','rej_cat','job_no').distinct())
        obj1 = list(Part.objects.filter(partno=part_no).values('des','drgno').distinct())
        obj.append(obj1)
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/m13view/')
def m13view(request):    
    wo_nop = empmast.objects.none()    
    tmp=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'usermaster':g.usermaster,

    }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = M13.objects.all().filter(shop=g.rolelist[i]).values('wo').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'subnav':g.subnav,
        }
        
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'subnav':subnav,
        }
    if request.method == "POST":        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':            
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            part_no = request.POST.get('part_nop')
            m13_no=request.POST.get('m13_no')
            slno=request.POST.get('slno')
            obj = list(M13.objects.filter(shop=shop_sec,part_no=part_no,wo=wo_no,m13_no=m13_no,slno=slno).values('m13_no','m13_date','qty_tot','qty_ins','qty_pas','qty_rej','opn','vendor_cd','fault_cd','staff_no','reason','slno','m13_sn','wo_rep','m15_no','epc','rej_cat','job_no').distinct())
            obj1 = Part.objects.filter(partno=part_no).values('des','drgno').distinct()            
            leng = len(obj)
            leng1 = len(obj1) 
            
            context={
                'sub':1,
                'lenm' :2,
                'nav':g.nav,
                'subnav':g.subnav,
                'ip':get_client_ip(request),
                'roles':tmp,
                'obj': obj,
                'obj1': obj1,
                'len': leng,
                'len1':leng1,
                'shop_sec': shop_sec,
                'wo_no': wo_no,
                'part_no': part_no,
                'slno' : slno,
                'usermaster':g.usermaster,

            }
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    req = M13.objects.all().filter(shop=g.rolelist[i]).values('wo').distinct()
                    wo_nop =wo_nop | req
                context = {
                    'sub':1,
                    'lenm' :len(g.rolelist),
                    'wo_nop':wo_nop,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    'subnav':g.subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1':leng1,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                }
                
            elif(len(g.rolelist)>1):
                context = {
                    'sub': 1,
                    'lenm' :len(g.rolelist),
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    'subnav':g.subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1':leng1,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                }

        if submitvalue=='Save':
                slno= request.POST.get('slno')
                m13_sn = request.POST.get('m13_sn')
                epc = request.POST.get('epc')
                qty_tot = request.POST.get('qty_tot')
                qty_ins = request.POST.get('qty_ins')
                qty_pas = request.POST.get('qty_pas')
                qty_rej = request.POST.get('qty_rej')
                vendor_cd = request.POST.get('vendor_cd')
                opn = request.POST.get('opn')
                job_no = request.POST.get('job_no')
                fault_cd = request.POST.get('fault_cd')
                emp_id = request.POST.get('emp_id')
                wo_rep = request.POST.get('wo_rep')
                m13no = request.POST.get('m13no')
                m15_no = request.POST.get('m15_no')
                rej_cat = request.POST.get('rej_cat')
                reason = request.POST.get('reason')
                if m13_sn and qty_tot and qty_ins and qty_pas and qty_rej and vendor_cd and opn and job_no and fault_cd and wo_rep and m15_no and rej_cat and reason and m13no and slno and epc:
                    M13.objects.filter(m13_no=m13no).update(slno=slno,staff_no=emp_id,m13_sn=m13_sn,epc=epc,qty_tot=qty_tot,qty_ins=qty_ins,qty_pas=qty_pas,qty_rej=qty_rej,vendor_cd=vendor_cd,opn=opn,job_no=job_no,fault_cd=fault_cd,wo_rep=wo_rep,m13_no=m13no,m15_no=m15_no,rej_cat=rej_cat,reason=reason)
                    messages.success(request,'Successfully Updated')
                else:
                    messages.success(request,'Please enter all fields!')
    return render(request,"MCARD/M13CARD/m13view.html",context)


@login_required
@role_required(urlpass='/m13insert/')
def m13insert(request):
    from dlw.models import M13     
    wo_nop = empmast.objects.none()     
    tmp=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()     
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'usermaster':g.usermaster,
    }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = M13.objects.all().filter(shop=g.rolelist[i]).values('wo').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'subnav':g.subnav,
        }
        
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'subnav':g.subnav,
        }
    if request.method == "POST":
        global shop_sec
        global wo_no
        global part_no
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Save':
                user=request.user
                shop_sec = request.POST.get('shop_sec')
                wo_no = request.POST.get('wo_no')
                part_no = request.POST.get('part_nop')
                from decimal import Decimal
                m13_no=request.POST.get('m13no')  
                slno= request.POST.get('slno')
                m13_sn = request.POST.get('m13_sn')
                epc = request.POST.get('epc')
                ab=request.POST.get('qty_tot')
                qt=ab
                if len(ab):
                    qty_tot = Decimal(ab)
                else:
                    qty_tot=0
                ab=request.POST.get('qty_ins')
                qi=ab
                if len(ab):
                    qty_ins = Decimal(ab)
                else:
                    qty_ins=0
                ab=request.POST.get('qty_pas')
                qp=ab
                if len(ab):
                    qty_pas = Decimal(ab)
                else:
                    qty_pas=0
                ab=request.POST.get('qty_rej')
                qr=ab
                if len(ab):
                    qty_rej = Decimal(ab)
                else:
                    qty_rej=0
                vendor_cd = request.POST.get('vendor_cd')
                opn = request.POST.get('opn')
                job_no = request.POST.get('job_no')
                fault_cd = request.POST.get('fault_cd')
                wo_rep = request.POST.get('wo_rep')
                m13no = request.POST.get('m13no')
                m15_no = request.POST.get('m15_no')
                rej_cat = request.POST.get('rej_cat')
                reason = request.POST.get('reason')
                emp_id = request.POST.get('emp_id')
                m13date = request.POST.get('date')
                M13.objects.create(usr_cd=str(user), shop=str(shop_sec), staff_no=str(emp_id), wo=str(wo_no), part_no=str(part_no), m13_sn=str(m13_sn), qty_tot=int(qty_tot), qty_ins=int(qty_ins), qty_pas=int(qty_pas), qty_rej=int(qty_rej), vendor_cd=str(vendor_cd), opn=str(opn), job_no=str(job_no), fault_cd=str(fault_cd),m15_no=str(m15_no), wo_rep=str(wo_rep), rej_cat=str(rej_cat), reason=str(reason), m13_no=str(m13_no), slno=str(slno), epc=str(epc), m13_date=str(m13date))
                smsM13("8130731698","Inspection card for M13 No:-"+m13_no+" dated:- "+m13date+" of Part No:-"+part_no+" for work order no:- "+wo_no+" has been generated. Qty inspected:- "+qi+", Qty Passed:- "+qp+", Qty Rejected:- "+qr+" under "+fault_cd+" head")
                messages.success(request,'Successfully Edited!')
    return render(request,"MCARD/M13CARD/m13insert.html",context)

def m13get1(request):
    if request.method == "GET" and request.is_ajax():
        user=request.user
        part_no = request.GET.get('part_no')
        wo_no = request.GET.get('wo_no')
        obj = list(Part.objects.filter(partno=part_no).values('des','drgno').distinct())
        m=''
        obj1 = list(M2Doc.objects.filter(part_no=part_no,batch_no=wo_no).values('qty').distinct())
        
        for k in M13.objects.raw('SELECT id, "SLNO"::int as s FROM public."M13" WHERE "USR_CD"=%s order by "SLNO"::int desc',[str(user)]):
            m=k.s
            break
        ep=list(Batch.objects.filter(bo_no=wo_no).values('ep_type'))
        obj.append(obj1)
        obj.append(m)
        obj.append(ep)
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)

def m13getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = list(Batch.objects.filter(status='R').values('bo_no').distinct())
        return JsonResponse(wo_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m13getpano(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        p1=M14M4.objects.filter(bo_no__in=[Batch.objects.filter(status='R',bo_no=wo_no).values('bo_no').distinct()]).values('part_no').distinct()
        p2=M2Doc.objects.filter(batch_no__in=[Batch.objects.filter(status='R',bo_no=wo_no).values('bo_no').distinct()]).values('part_no').distinct()
        p=p1.union(p2)
        part_no=list(Oprn.objects.filter(part_no__in=[p],shop_sec=shop_sec).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)


