from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/mg11views/')
def mg11views(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    wo_nop = empmast.objects.none()
    name = empmast.objects.values('empname').exclude(empname__isnull=True).distinct()
    prtname=[]
    for i in name:
        prtname.append(i['empname'])
        
    shop_sec = request.GET.get('shop_sec')
    w1 = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
    prtticket=[] 
    for i in w1:
        ty=i['staff_no']
        pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
        prtticket.append(pop)
    tm=shop_section.objects.filter(shop_id=usermaster.shopno).all()
    tmp=[]
    
    for on in tm:
        tmp.append(on.section_code)
    if "Superuser" in g.rolelist:       
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'usermaster':g.usermaster,
            'prtname':prtname,
            'prtticket':prtticket,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = mg11.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'prtname':prtname,
            'prtticket':prtticket,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'prtname':prtname,
            'prtticket':prtticket,
        }
        
    if request.method == "POST":

        submitvalue = request.POST.get('proceed')

        if submitvalue=='Proceed':
            date = request.POST.get('date')
            shop_sec = request.POST.get('shop_sec')
            month = request.POST.get('month')

            obj1 = mg11.objects.filter(shop_sec=shop_sec,month=month).values('sno','date','ticket_no','name','remarks').distinct()
           
            obj3=mg11.objects.all().count()

            wer=obj3+1

            w1 = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()) 

            prtticket=[]
            for i in w1:
                ty=i['staff_no']
                pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
                for i in pop:
                    prtticket.append(i['ticket_no'])

            ticket = request.POST.get('ticket')

            context = {
            'obj1': obj1,
            'mytry':"rimjhim",
            'shop_sec': shop_sec,
            'month':month,
            'date':date,
            'wer':wer,
            'prtname':prtname,
            'prt':prtticket,
            'prtticket':prtticket,
            'ticket':ticket,            
            'sub': 1, 
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
                    
        }

        if submitvalue=='submit':
            leng=request.POST.get('len')

            shop_sec= request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            name = request.POST.get('name')
            tot= request.POST.get('total')
            tot = int(tot)+1

            for i in range(1,int(tot)):
                date = request.POST.get('date')
                shop_sec = request.POST.get('shop_sec')
                month = request.POST.get('month')
                sno = request.POST.get('sno'+str(i))
                ticket = request.POST.get('ticket'+str(i))
                name = request.POST.get('name'+str(i))
                remark = request.POST.get('remark'+str(i))
                mg11.objects.create(shop_sec=str(shop_sec),month=str(month),date=str(date),sno=str(sno),ticket_no=str(ticket),name=str(name),remarks=str(remark))


    return render(request,"MGCARD/MG11CARD/mg11views.html",context)


@login_required
@role_required(urlpass='/mg11report/')
def mg11report(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    wo_nop = empmast.objects.none()
    name = empmast.objects.values('empname').exclude(empname__isnull=True).distinct()
    prtname=[]
    for i in name:
        prtname.append(i['empname'])
        
    shop_sec = request.GET.get('shop_sec')
    w1 = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
    prtticket=[] 
    for i in w1:
        ty=i['staff_no']
        pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
        prtticket.append(pop)
    tm=shop_section.objects.filter(shop_id=usermaster.shopno).all()
    tmp=[]
    
    for on in tm:
        tmp.append(on.section_code)

    if "Superuser" in g.rolelist:        
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'usermaster':g.usermaster,
            'prtname':prtname,
            'prtticket':prtticket,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = mg11.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'prtname':prtname,
            'prtticket':prtticket,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'prtname':prtname,
            'prtticket':prtticket,
        }
        
    if request.method == "POST":

        submitvalue = request.POST.get('proceed')

        if submitvalue=='Proceed':
            date = request.POST.get('date')
            shop_sec = request.POST.get('shop_sec')
            month = request.POST.get('month')
            ticket = request.POST.get('ticket')

            obj1 = mg11.objects.filter(shop_sec=shop_sec,month=month).values('sno','date','ticket_no','name','remarks').distinct()

            obj3=mg11.objects.all().count()
            wer=obj3+1

            tm=shop_section.objects.filter(section_code=shop_sec).all()
            shop_code=tm[0].shop_code
            w1 = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()) 

            prtticket=[]
            for i in w1:
                ty=i['staff_no']
                pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
                for i in pop:
                    prtticket.append(i['ticket_no'])

            leng=obj1.count() 

            context = {
            'obj1': obj1,
            'mytry':"rimjhim",
            'leng':leng,
            'shop_sec': shop_sec,
            'month':month,
            'date':date,
            'wer':wer,
            'prtname':prtname,
            'prt':prtticket,
            'prtticket':prtticket,
            'nav':g.nav,
            'usermaster':g.usermaster,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'sub': 1, 
            'shop_code': shop_code[0:3], 
                    
        }

    return render(request,"MGCARD/MG11CARD/mg11report.html",context)


def mg11Submitdata(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        ticket = request.GET.get('ticket')
        date = request.GET.get('date')         
        month = request.GET.get('month')                      
        sno = request.GET.get('sno')               
        name = request.GET.get('name')        
        remark = request.GET.get('remark')
        mg11.objects.create(
            shop_sec=str(shop_sec),
            month=str(month),
            date=str(date),
            sno=str(sno),
            ticket_no=str(ticket),
            name=str(name),           
            remarks=str(remark),             
            login_id=str(request.user)                
        )
        obj3=mg11.objects.all().count()
        wer=obj3+1

        obj1 =list(mg11.objects.filter(shop_sec=shop_sec,month=month).values('sno','date','ticket_no','name','remarks').distinct())
        
        context={
            'obj1':obj1,
            'wer':wer,
            
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)
    
def mg11updatedata(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec2')
        ticket = request.GET.get('ticket2')
        date = request.GET.get('date2')         
        month = request.GET.get('month2')                      
        sno = request.GET.get('sno2')               
        name = request.GET.get('name2')        
        remark = request.GET.get('remark2')
        mg11.objects.filter(sno=sno).update(
            shop_sec=str(shop_sec),
            month=str(month),
            date=str(date),
            sno=str(sno),
            ticket_no=str(ticket),
            name=str(name),            
            remarks=str(remark),                     
        ) 
        obj3=mg11.objects.all().count()
        wer=obj3+1
        obj1 =list(mg11.objects.filter(shop_sec=shop_sec,month=month).values('sno','date','ticket_no','name','remarks').distinct())
        
        context={
            'obj1':obj1,
            'wer':wer
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)

    
 
def mg11editdata(request):
    if request.method == "GET" and request.is_ajax():
        sno = request.GET.get('sno')
        obj1=list(mg11.objects.filter(sno=sno).values('month', 'date','sno','date','ticket_no','name','remarks').distinct())
        
        context={
            'obj1':obj1,             
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)
       

def mg11getname(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        ticket = request.GET.get('two')
        wname = empmast.objects.filter(ticket_no=ticket).values('empname').distinct()
        myname = wname[0]['empname']
        context={
            'prt':myname,
        }
        return JsonResponse({'cont':context}, safe = False)
    return JsonResponse({"success":False}, status=400)
