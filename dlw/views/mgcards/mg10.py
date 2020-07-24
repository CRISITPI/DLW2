from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/mg10views/')
def mg10views(request):
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

    payrate = empmast.objects.values('payrate').exclude(payrate__isnull=True).distinct()
    prtpay=[]
    for i in payrate:
        prtpay.append(i['payrate'])
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
            'prtname':prtname,
            'prtpay':prtpay,
            'prtticket':prtticket,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):

            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = mg10.objects.filter(part_no__in=w1).values('batch_no').distinct()
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
            'prtname':prtname,
            'prtpay':prtpay,
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
            'prtpay':prtpay,
            'prtticket':prtticket,
        }
        
    if request.method == "POST":

        submitvalue = request.POST.get('proceed')

        if submitvalue=='Proceed':
            date = request.POST.get('date')
            shop_sec = request.POST.get('shop_sec')
            month = request.POST.get('month')
            ticket = request.POST.get('ticket')
            obj1 = mg10.objects.filter(shop_sec=shop_sec,month=month).values('sno','date','ticket_no','name','payrate','cat','eiwdate','remarks').distinct()
     
            obj3=mg10.objects.all().count()
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
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'shop_sec': shop_sec,
            'month':month,
            'date':date,
            'wer':wer,
            'prtname':prtname,
            'prtpay':prtpay,
            'prt':prtticket,
            'prtticket':prtticket,
            'ticket':ticket,
            'sub': 1, 
            'usermaster':g.usermaster,
            'roles' :tmp,
            }
        if submitvalue=='submit':
            leng=request.POST.get('len')

            tot= request.POST.get('total')            
            tot = int(tot)+1
            for i in range(1,int(tot)):
                date = request.POST.get('date')
                shop_sec = request.POST.get('shop_sec')
                month = request.POST.get('month')
                ticket = request.POST.get('ticket'+str(i))                
                sno = request.POST.get('sno'+str(i))               
                name = request.POST.get('name'+str(i))
                payrate = request.POST.get('payrate'+str(i))
                category = request.POST.get('category'+str(i)) 
                eiwdate = request.POST.get('eiwdate'+str(i))
                remark = request.POST.get('remark'+str(i))
               
                mg10.objects.create(
                    shop_sec=str(shop_sec),
                    month=str(month),
                    date=str(date),
                    sno=str(sno),
                    ticket_no=str(ticket),
                    name=str(name),
                    payrate=str(payrate),
                    cat=str(category),
                    eiwdate=str(eiwdate),
                    remarks=str(remark),                     
                    )

            messages.success(request, 'Successfully Done!, Select new values to proceed')
    return render(request,"MGCARD/MG10CARD/mg10views.html",context)


@login_required
@role_required(urlpass='/mg10report/')
def mg10report(request):
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

    payrate = empmast.objects.values('payrate').exclude(payrate__isnull=True).distinct()
    prtpay=[]
    for i in payrate:
        prtpay.append(i['payrate'])
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
            'prtname':prtname,
            'usermaster':g.usermaster,
            'prtpay':prtpay,
            'prtticket':prtticket,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):

            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = mg10.objects.filter(part_no__in=w1).values('batch_no').distinct()
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
            'prtpay':prtpay,
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
            'usermaster':g.usermaster,
            'prtname':prtname,
            'prtpay':prtpay,
            'prtticket':prtticket,
        }
        
    if request.method == "POST":

        submitvalue = request.POST.get('proceed')

        if submitvalue=='Proceed':
            date = request.POST.get('date')
            shop_sec = request.POST.get('shop_sec')
            month = request.POST.get('month')
            ticket = request.POST.get('ticket')

            obj1 = mg10.objects.filter(shop_sec=shop_sec,month=month).values('sno','date','ticket_no','name','payrate','cat','eiwdate','remarks').distinct()
        
            tms=shop_section.objects.all()
            tmp=[]        
            for on in tms:
                tmp.append(on.section_code)
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
            ticket = request.POST.get('ticket')

            context = {
            'obj1': obj1,
            'mytry':"rimjhim",
            'leng':leng,
            'shop_sec': shop_sec,
            'month':month,
            'date':date,
            'prtname':prtname,
            'prtpay':prtpay,
            'prt':prtticket,
            'prtticket':prtticket,
            'ticket':ticket,
            'roles':tmp,
            'sub': 1, 
            'nav':g.nav,
            'usermaster':g.usermaster,
            'subnav':g.subnav,
            'shop_code': shop_code[0:3], 
                    
        }

    return render(request,"MGCARD/MG10CARD/mg10report.html",context)



def mg10Submitdata(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        ticket = request.GET.get('ticket1')
        date = request.GET.get('date')         
        month = request.GET.get('month')                      
        sno = request.GET.get('sno1')               
        name = request.GET.get('name1')
        payrate = request.GET.get('payrate1')
        category = request.GET.get('category1') 
        eiwdate = request.GET.get('eiwdate1')
        remark = request.GET.get('remark1')
        mg10.objects.create(
            shop_sec=str(shop_sec),
            month=str(month),
            date=str(date),
            sno=str(sno),
            ticket_no=str(ticket),
            name=str(name),
            payrate=str(payrate),
            cat=str(category),
            eiwdate=str(eiwdate),
            remarks=str(remark),             
            login_id=str(request.user)                
        )
        obj3=mg10.objects.all().count()
        wer=obj3+1

        obj1 =list(mg10.objects.filter(shop_sec=shop_sec,month=month).values('sno','date','ticket_no','name','payrate','cat','eiwdate','remarks').distinct())
        
    
        context={
            'obj1':obj1,
            'wer':wer
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg10updatedata(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec2')
        ticket = request.GET.get('ticket2')
        date = request.GET.get('date2')         
        month = request.GET.get('month2')                      
        sno = request.GET.get('sno2')               
        name = request.GET.get('name2')
        payrate = request.GET.get('payrate2')
        category = request.GET.get('category2') 
        eiwdate = request.GET.get('eiwdate2')
        remark = request.GET.get('remark2')
        mg10.objects.filter(sno=sno).update(
            shop_sec=str(shop_sec),
            month=str(month),
            date=str(date),
            sno=str(sno),
            ticket_no=str(ticket),
            name=str(name),
            payrate=str(payrate),
            cat=str(category),
            eiwdate=str(eiwdate),
            remarks=str(remark),                     
        ) 
        obj3=mg10.objects.all().count()
        wer=obj3+1
        obj1 =list(mg10.objects.filter(shop_sec=shop_sec,month=month).values('sno','date','ticket_no','name','payrate','cat','eiwdate','remarks').distinct())
        
        context={
            'obj1':obj1,
            'wer':wer
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg10editdata(request):
    if request.method == "GET" and request.is_ajax():
        sno = request.GET.get('sno')
        obj1=list(mg10.objects.filter(sno=sno).values('month', 'date','sno','date','ticket_no','name','payrate','cat','eiwdate','remarks').distinct())
        
        context={
            'obj1':obj1,             
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg10checkdate(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        ticket = request.GET.get('ticket')
        d1 = M21.objects.filter(shop_sec=shop_sec).values('date').distinct()
        date_values = []
        return JsonResponse(d1, safe = False)
    return JsonResponse({"success":False}, status=400)
    
           
    

    

def mg10getpayrate(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        ticket = request.GET.get('ticket')
        ticket = list(empmast.objects.filter(ticket_no=ticket).values('payrate').distinct())
        return JsonResponse(ticket, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg10getname(request):
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


def mg10getcat(request):
    if request.method == "GET" and request.is_ajax():
        ticket = request.GET.get('two')
        w1 = list(empmast.objects.filter(ticket_no=ticket).values('empno','payrate').exclude(empno__isnull=True).distinct())
        t=w1[0]['empno']
        payrate=w1[0]['payrate']
        w2=str(t)
        w4=w2[6:11]
        w3= list(Shemp.objects.filter(staff_no=w4).values('cat').exclude(cat__isnull=True).distinct())[0]
        context={
            'prt':w3['cat'],
            'payrate':payrate,
        }
        return JsonResponse({'cont':context}, safe = False)
    return JsonResponse({"success":False}, status=400)
