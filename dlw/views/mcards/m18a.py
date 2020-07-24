from dlw.views import *
import dlw.views.globals as g


@login_required
@role_required(urlpass='/m18aview/')
def m18aview(request):
     
    tmp=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
     
    wo_nop = user_master.objects.none()
     
        
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,

            'ip':get_client_ip(request),
            'roles':tmp,
            'usermaster':g.usermaster,
            'subnav':g.subnav,
        }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=g.rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req

        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,

            'ip':get_client_ip(request),
            'roles' :tmp,
            'usermaster':g.usermaster,
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            from decimal import Decimal
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            br_no= request.POST.get('br_no')
            part_no = request.POST.get('part_nop')
            month = request.POST.get('month')
            staff_no = request.POST.get('sse')
            ticket_no = request.POST.get('ticket_no')
            oprn_no = request.POST.get('oprn_no')

            ty=str(staff_no)
            staff=ty[6:11]
            staff=Shemp.objects.filter(shopsec=shop_sec,staff_no=staff).values('cat').exclude(staff_no__isnull=True)[0]
           
            obj3=0
            obj2=0
            p=None
            obj1=M18DOC.objects.filter(shopsec=shop_sec,month=month,staff_no=staff_no).all()
            if len(obj1):
              obj3=M18DOC.objects.filter(shopsec=shop_sec,month=month,staff_no=staff_no).values('req_no')[0]
            obj4=0
            obj2=Oprn.objects.filter(shop_sec=shop_sec,part_no=part_no).values('opn').distinct()

            emp=empmast.objects.filter(empno=staff_no).values('empno').distinct()
            empno=[]
            for i in emp:
                empno.append(i['empno'])

            leng=obj1.count()
            leng2=obj2.count()
                 
            context={
                    'len' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'usermaster':g.usermaster,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'obj4':obj4,
                    'len2':leng2,
                    'p':p,
                    'lent': leng,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no':part_no,
                    'staff':staff,
                    'ticket_no':ticket_no,
                    'month': month,
                    'empno':empno,
                    'oprn_no':oprn_no,
                    'sub':1,
                }
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                    wo_no =wo_no | req
                context = {
                    'len' :len(rolelist),
                    'wo_no':wo_no,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles' :tmp,
                    'usermaster':g.usermaster,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'obj4':obj4,
                    'lent': leng,
                    'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff':staff,
                    'oprn_no':oprn_no,
                    'empno':empno,
                    'part_no':part_no,
                    'p':p,
                    'ticket_no':ticket_no,
                    'month': month,
                    'sub':1,
                }
            if(len(g.rolelist)>1):
                context = {
                    'len' :len(g.rolelist),
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles' :tmp,
                    'usermaster':g.usermaster,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'obj4':obj4,
                    'len2':leng2,
                    'lent': leng,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'staff':staff,
                    'p':p,
                    'oprn_no':oprn_no,
                    'ticket_no':ticket_no,
                    'part_no':part_no,
                    'month': month,
                    'empno':empno,
                    'sub':1,
                }

        if submitvalue=='submit':
            leng=request.POST.get('len')
            shopsec = request.POST.get('shopsec')
            month1= request.POST.get('month')
            req_no=request.POST.get('req_no')
            inoutnum=request.POST.get("inoutnum")
           

            for i in range(1, int(inoutnum)+1):
                in1 = request.POST.get('in1add'+str(i))
                
                out = request.POST.get('outadd'+str(i))
                month = request.POST.get('month_add'+str(i))
                total_time = request.POST.get('total_time_add'+str(i))
                in_date = request.POST.get('in_dateadd'+str(i))
                out_date = request.POST.get('out_dateadd'+str(i))
                cat = request.POST.get('catadd'+str(i))
                total_time = request.POST.get('total_time_takenadd'+str(i))
                shift=request.POST.get('shiftadd'+str(i))
                staff_no=request.POST.get('staff_noadd'+str(i))
                staff_name=request.POST.get('staff_nameadd'+str(i))
                ticket_no=request.POST.get('ticket_noadd'+str(i))
                req_no = request.POST.get('req_no')
                
                M18DOC.objects.create(shift_typename=str(shift),shopsec=str(shopsec),name=str(staff_name),staff_no=str(staff_no),in1=str(in1),out=str(out),month=str(month1),in_date=str(in_date),cat=str(cat),total_time_taken=str(total_time),out_date=str(out_date),ticket_no=str(ticket_no),req_no=str(req_no))

    return render(request,"MCARD/M18ACARD/m18aview.html",context)

def m18getempname(request):
    if request.method == "GET" and request.is_ajax():  
        examcode= request.GET.get('two')
        ex= empmast.objects.filter(empno=examcode).all()
      
        exam ={
            "exam_type":ex[0].empname,
        }    
       
        return JsonResponse({"exam":exam}, safe = False)
    return JsonResponse({"success":False}, status=400)   

def m18getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').exclude(batch_no__isnull=True).distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m18getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        part_no = list(M5DOCnew.objects.filter(batch_no =wo_no,shop_sec=shop_sec).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m18getoprn_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        part_no = request.GET.get('part_nop')
        oprn_no = list(Oprn.objects.filter(part_no=part_no).values('opn').exclude(opn__isnull=True).distinct())
        return JsonResponse(oprn_no, safe = False)
    return JsonResponse({"success":False}, status=400)  


def m18getticket_no(request):
    if request.method == "GET" and request.is_ajax():
        sse=request.GET.get('sse')
        ticket_no = list(empmast.objects.filter(empno=sse).values('ticket_no').exclude(ticket_no__isnull=True).distinct())
        return JsonResponse(ticket_no, safe = False)
    return JsonResponse({"success":False}, status=400)  


def m18getsse(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff=Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
        prtstaff=[]
        for i in staff:
           ty=i['staff_no']
           pop=empmast.objects.filter(empno__contains=ty).values('empno')
           for i in pop:
            prtstaff.append(i['empno'])

        context={
            'prt':prtstaff,
        }
        return JsonResponse({'context':context}, safe = False)
    return JsonResponse({"success":False}, status=400)


