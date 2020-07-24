from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/m11report/')
def m11report(request): 
    tmp=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'user':g.usermaster,
        'roles':tmp
    }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
            wo_no =  req
        context = {
            'sub':0,
            'len' :len(g.rolelist),
            'wo_no':wo_no,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'user':g.usermaster,
            'lent':0,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'len' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'user':g.usermaster,
            'lent':0,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            from decimal import Decimal
            month = request.POST.get('monthdrop')
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            staff_no = request.POST.get('staff_no')
            part_no = request.POST.get('part_no')
            tempcat=Shemp.objects.filter(staff_no=staff_no).values('cat','name').distinct()
            empname=tempcat[0]['name']
            tcat=tempcat[0]['cat']
            obj1 = M11.objects.filter(staff_no=staff_no,shopsec=shop_sec,month=month).values('id','month','cat','in1','out','in_date','out_date','shift','total_time','detail_no','idle_time').distinct()
            obj2='None'
            obj3='None'
            leng=0
            leng1=0
            rr='None'
            amt=0
            patotal=0
            a=0 
            b=0
            t=0
            if len(obj1):
                if obj1[0]['cat'] is not None:
                    t=obj1[0]['cat']
                else:
                    t=tempcat[0]['cat']
            else:
                t=tempcat[0]['cat']
            if t != 'None':
                obj2 = Rates.objects.filter(staff_no=staff_no).values('avg_rate').distinct()
                obj3 = M11.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('month','cat')[0]


            for op in range(len(obj1)):
                patotal=obj1[op]['total_time']
                if patotal is not None and len(str(patotal)):
                    p=patotal.split(':')
                    a=a+Decimal(p[0])
                    b=b+Decimal(p[1])
                    if (b>=60):
                        a=a+1
                        b=b%60

                rr=str(a)+':'+str(b)    
            
        
            tmhr=rr
            if len(obj2):    
                avgrt=obj2[0]['avg_rate']
                if tmhr == 'None': 
                    tmhr=0
                    avgrt=0
                else:
                    tmhr1=tmhr.split(':')
                    tmhr=Decimal(tmhr1[0])+(Decimal(tmhr1[1])/60)
                    
            
                amt=tmhr*avgrt
            leng = obj1.count()
            leng1 = obj2.count()
            leng=obj1.count()
            amt=round(amt,2)
             
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                    wo_no = req
                context = {
                    'sub':1,
                    'len' :len(g.rolelist),
                    'wo_no':wo_no,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles' :tmp,
                    'user':g.usermaster,
                    'lent':0,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,'tcat':tcat,'empname':empname,
                }
            elif(len(g.rolelist)>1):
                context = {
                    'sub':1,
                    'len' :len(g.rolelist),
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles' :tmp,
                    'user':g.usermaster,
                    'lent':0,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,'tcat':tcat,'empname':empname,
                }
        if submitvalue=='PrintPDF':
            from decimal import Decimal
            obj2='None'
            leng=0
            leng1=0
            rr='None'
            amt=0
            patotal=0
            a=0 
            b=0
            t=0
            month = request.POST.get('month')
            shop_sec = request.POST.get('shopsec')
            wo_no = request.POST.get('wo_no')
            staff_no = request.POST.get('staff_no')
            part_no = request.POST.get('part_no')
            tempcat=Shemp.objects.filter(staff_no=staff_no).values('cat','name').distinct()
            empname=tempcat[0]['name']
            tcat=tempcat[0]['cat']
            obj1 = M11.objects.filter(staff_no=staff_no,shopsec=shop_sec,month=month).values('id','month','cat','in1','out','in_date','out_date','shift','total_time','detail_no','idle_time').distinct()   
            obj2 = Rates.objects.filter(staff_no=staff_no).values('avg_rate').distinct()


            for op in range(len(obj1)):
                patotal=obj1[op]['total_time']
                if patotal is not None and len(str(patotal)):
                    p=patotal.split(':')
                    a=a+Decimal(p[0])
                    b=b+Decimal(p[1])
                    if (b>=60):
                        a=a+1
                        b=b%60

                rr=str(a)+':'+str(b)    

            tmhr=rr
            if len(obj2):    
                avgrt=obj2[0]['avg_rate']
                if tmhr == 'None': 
                    tmhr=0
                    avgrt=0
                else:
                    tmhr1=tmhr.split(':')
                    tmhr=Decimal(tmhr1[0])+(Decimal(tmhr1[1])/60)
                    
            
                amt=tmhr*avgrt
            leng = obj1.count()
            leng1 = obj2.count()
            leng=obj1.count()
            amt=round(amt,2)
            context = {
                    
                    'obj1': obj1,
                    'shop_sec': shop_sec,
                    'staff_no':staff_no,
                    'wo_no': wo_no,
                    'r1':rr,
                    'amt1': amt,
                    'month': month,'tcat':tcat,'empname':empname,
            }  
                
            pdf = render_to_pdf('MCARD/M11CARD/M11pdfc.html',context)
            return HttpResponse(pdf, content_type='application/pdf')

    return render(request,"MCARD/M11CARD/m11report.html",context) 
	
	

@login_required
@role_required(urlpass='/m11view/')
def m11view(request):  
    tmp=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
      
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'user':g.usermaster,
    }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(status='R').values('bo_no').exclude(bo_no__isnull=True).distinct()
            wo_no = req
        context = {
            'sub':0,
            'len' :len(g.rolelist),
            'wo_no':wo_no,
            'user':g.usermaster,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'lent':0,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'len' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'lent':0,
            'user':g.usermaster,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            from decimal import Decimal
            month = request.POST.get('monthdrop')
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            staff_no = request.POST.get('staff_no')
            part_no = request.POST.get('part_no')
            tempcat=Shemp.objects.filter(staff_no=staff_no).values('cat','name').distinct()
            empname=tempcat[0]['name']
            tcat=tempcat[0]['cat']
            obj1 = M11.objects.filter(staff_no=staff_no,shopsec=shop_sec,month=month).values('id','month','cat','in1','out','in_date','out_date','shift','total_time','detail_no','idle_time').distinct()
            obj2='None'
            obj3='None'
            leng=0
            leng1=0
            rr='None'
            amt=0
            patotal=0
            a=0 
            b=0
            t=0
            if len(obj1):
                if obj1[0]['cat'] is not None:
                    t=obj1[0]['cat']
                else:
                    t=tempcat[0]['cat']
            else:
                t=tempcat[0]['cat']
            if t != 'None':
                obj2 = Rates.objects.filter(staff_no=staff_no).values('avg_rate').distinct()
                obj3 = M11.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('month','cat').distinct()
                if len(obj3):
                    obj3 = M11.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('month','cat')[0]

            for op in range(len(obj1)):
                patotal=obj1[op]['total_time']
                if patotal is not None and len(str(patotal)):
                    p=patotal.split(':')
                    a=a+Decimal(p[0])
                    b=b+Decimal(p[1])
                    if (b>=60):
                        a=a+1
                        b=b%60
                rr=str(a)+':'+str(b)    
            
            tmhr=rr
            if len(obj2):    
                avgrt=obj2[0]['avg_rate']
                if tmhr == 'None': 
                    tmhr=0
                    avgrt=0
                else:
                    tmhr1=tmhr.split(':')
                    tmhr=Decimal(tmhr1[0])+(Decimal(tmhr1[1])/60)                    
                amt=tmhr*avgrt
            leng = obj1.count()
            leng1 = obj2.count()
            leng=obj1.count()
            amt=round(amt,2)
            if "Superuser" in g.rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'user':g.usermaster,
                    'month': month,'tcat':tcat,'empname':empname,
                }
            elif(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(status='R').values('bo_no').exclude(bo_no__isnull=True).distinct()
                    wo_no =wo_no | req
                context = {
                    'sub':1,
                    'len' :len(g.rolelist),
                    'wo_no':wo_no,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles' :g.rolelist,
                    'lent':0,
                    'user':g.usermaster,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,'tcat':tcat,'empname':empname,
                }
            elif(len(g.rolelist)>1):
                context = {
                    'sub':1,
                    'len' :len(g.rolelist),
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles' :g.rolelist,
                    'lent':0,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'user':g.usermaster,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,'tcat':tcat,'empname':empname,
                }   
        submitvalue = request.POST.get('PrintPDF')
        if submitvalue=='PrintPDF':
            from decimal import Decimal
            obj2='None'
            leng=0
            leng1=0
            rr='None'
            amt=0
            patotal=0
            a=0 
            b=0
            t=0
            month = request.POST.get('month')
            shop_sec = request.POST.get('shopsec')
            wo_no = request.POST.get('wo_no')
            staff_no = request.POST.get('staff_no')
            part_no = request.POST.get('part_no')
            tempcat=Shemp.objects.filter(staff_no=staff_no).values('cat','name').distinct()
            empname=tempcat[0]['name']
            tcat=tempcat[0]['cat']
            obj1 = M11.objects.filter(staff_no=staff_no,shopsec=shop_sec,month=month).values('id','month','cat','in1','out','in_date','out_date','shift','total_time','detail_no','idle_time').distinct()   
            obj2 = Rates.objects.filter(staff_no=staff_no).values('avg_rate').distinct()


            for op in range(len(obj1)):
                patotal=obj1[op]['total_time']
                if patotal is not None and len(str(patotal)):
                    p=patotal.split(':')
                    a=a+Decimal(p[0])
                    b=b+Decimal(p[1])
                    if (b>=60):
                        a=a+1
                        b=b%60

                rr=str(a)+':'+str(b)   
            tmhr=rr
            if len(obj2):    
                avgrt=obj2[0]['avg_rate']
                if tmhr == 'None': 
                    tmhr=0
                    avgrt=0
                else:
                    tmhr1=tmhr.split(':')
                    tmhr=Decimal(tmhr1[0])+(Decimal(tmhr1[1])/60)
                amt=tmhr*avgrt
            leng = obj1.count()
            leng1 = obj2.count()
            leng=obj1.count()
            amt=round(amt,2)
            context = {
                    
                    'obj1': obj1,
                    'shop_sec': shop_sec,
                    'staff_no':staff_no,
                    'wo_no': wo_no,
                    'r1':rr,
                    'amt1': amt,
                    'month': month,'tcat':tcat,'empname':empname,
            }  
                
            pdf = render_to_pdf('MCARD/M11CARD/M11pdfc.html',context)
            return HttpResponse(pdf, content_type='application/pdf')
            
        if submitvalue=='Submit':
            leng=request.POST.get('len')
            shopsec= request.POST.get('shopsec')
            staff_no = request.POST.get('staff_no')
            inoutnum = request.POST.get("inoutnum")
            ename= request.POST.get('empname')
            scat=request.POST.get('tcat')
            
            for i in range(1, int(leng)+1):
                in_date = request.POST.get('in_date'+str(i))
                out_date = request.POST.get('out_date'+str(i))
                shift = request.POST.get('shift'+str(i))
                month = request.POST.get('month')
                in1 = request.POST.get('in1'+str(i))
                out = request.POST.get('out'+str(i))
                total_time = request.POST.get('total_time'+str(i))
                idle_time = request.POST.get('idle_time'+str(i))
                detail_no = request.POST.get('detail_no'+str(i))
                amt = request.POST.get('amt1'+str(i))

               
                sender_email_id = 'crisdlwproject@gmail.com'
                sender_email_id_password = 'cris@1234'

                if  month and in1 and out and idle_time and detail_no and total_time:
                    M11.objects.create(shopsec=shopsec,staff_no=staff_no,in1=str(in1),out=str(out),name=str(ename),cat=scat,month=str(month),total_time=str(total_time),in_date=str(in_date),out_date=str(out_date),shift=str(shift),idle_time=str(idle_time),detail_no=str(detail_no))
                   
                    messages.success(request, 'Data Saved Successfully!!')
                else:
                    messages.success(r598+equest, 'Please enter all values!!')
                    wo_no=Batch.objects.all().values('bo_no').distinct()
                    

    return render(request,"MCARD/M11CARD/m11views.html",context)


def m11save(request):
    if request.method == 'GET' and request.is_ajax():
        shopsec= request.GET.get('shopsec')
        staff_no = request.GET.get('staff_no')
        ename= request.GET.get('ename')   
        scat=request.GET.get('tcat')
        
        in_date = request.GET.get('in_date')   
        out_date = request.GET.get('out_date')
        shift = request.GET.get('shift')
        month = request.GET.get('month')
        in1 = request.GET.get('in1')
        out = request.GET.get('out')
        total_time = request.GET.get('total_time')
        idle_time = request.GET.get('idle_time')
        detail_no = request.GET.get('detail_no')
        amt = request.GET.get('amt1')
        sender_email_id = 'crisdlwproject@gmail.com'
        sender_email_id_password = 'cris@1234'

        if  month and in1 and out and idle_time and detail_no and total_time:
            M11.objects.create(shopsec=shopsec,staff_no=staff_no,in1=str(in1),out=str(out),name=str(ename),cat=scat,month=str(month),total_time=str(total_time),in_date=str(in_date),out_date=str(out_date),shift=str(shift),idle_time=str(idle_time),detail_no=str(detail_no))
        
            emp_det=list(emp_details.objects.filter(shopsec=str(shopsec),card_details='M11').values('mobileno','email_id'))
            for x in range(len(emp_det)):

                sms(emp_det[x]['mobileno'],"Man idle card for Emp number "+ staff_no +" Name "+ ename +" Soap "+ shopsec +" has been generated for the Date "+ in_date +" Total idle time "+idle_time+" ")

                email1(sender_email_id,sender_email_id_password,emp_det[x]['email_id'],'Subject: MAN IDLE TIME CARD \n\n   Dear Sir,   Man idle card for Emp number '+ staff_no +' Name '+ ename +' Soap '+ shopsec +' has been generated for the Date '+ in_date +' Total idle time '+idle_time+' ')
            obj1=list(M11.objects.filter(staff_no=staff_no,shopsec=shopsec,month=month).values('id','month','in1','out','in_date','out_date','shift','total_time','detail_no','idle_time').order_by('in_date'))

            context={
            'obj1':obj1,
                }   
            return JsonResponse({'data':context}, safe = False)
        
    return JsonResponse({"success":False}, status = 400)


def m11getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2=Batch.objects.filter(status='R').values('bo_no').exclude(bo_no__isnull=True).distinct()
        wo_no = list(w2)                                             
        return JsonResponse(wo_no, safe = False)                    
    return JsonResponse({"success":False}, status=400)

def m11getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no=list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m11getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        
        wo_no = request.GET.get('wo_no')
        
        part_no = list(Batch.objects.filter(bo_no=wo_no).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m11indateLink(request):
    if request.method == 'GET' and request.is_ajax():  
        in_date= request.GET.get('in_date')
        staff_no= request.GET.get('staff_no')
        shop_sec= request.GET.get('shop_sec')
        data_list =list(M21DOCNEW1.objects.filter(shop_sec=shop_sec,staff_no=staff_no,date=in_date).values('in1','date','out','outdate','total_time').distinct())
        if(len(data_list)>0):
            return JsonResponse(data_list,safe = False)                         
    return JsonResponse({"success":False},status=400)

def m11indateCheck(request):
    if request.method == 'GET' and request.is_ajax():  
        in_date= request.GET.get('in_date')
        staff_no= request.GET.get('staff_no')
        shop_sec= request.GET.get('shop_sec')
     
        data_list =list(M11.objects.filter(shopsec=shop_sec,staff_no=staff_no,in_date=in_date).values('in1','in_date','out','out_date','total_time').distinct())
        if(len(data_list)>0):
            return JsonResponse(data_list,safe = False)                         
    return JsonResponse({"success":False},status=400)

def indateqry1(request):
    if request.method == 'GET' and request.is_ajax():  
        date= request.GET.get('in_date')
        staff_no= request.GET.get('staff_no')
        shop_sec= request.GET.get('shop_sec')
        data_list =list(M21DOCNEW1.objects.filter(shop_sec=shop_sec,staff_no=staff_no,date=date).values('in1','date','out','outdate','total_time').distinct())
        if(len(data_list)>0):
            return JsonResponse(data_list,safe = False)                         
    return JsonResponse({"success":False},status=400)

def indateCheck(request):
    if request.method == 'GET' and request.is_ajax():  
        in_date= request.GET.get('in_date')
        staff_no= request.GET.get('staff_no')
        shop_sec= request.GET.get('shop_sec')
        data_list =list(M11.objects.filter(shopsec=shop_sec,staff_no=staff_no,in_date=in_date).values('in1','in_date','out','out_date','total_time').distinct())
        if(len(data_list)>0):
            return JsonResponse(data_list,safe = False)                         
    return JsonResponse({"success":False},status=400)

def m11repor(request):
    if request.method=="GET" and request.is_ajax():
        month = request.GET.get('month')
        staff = request.GET.get('staff')
        shop = request.GET.get('shop')
        myval=list(M11.objects.filter(staff_no=staff,shopsec=shop,month=month).values('month','in1','out','in_date','out_date','shift','total_time','detail_no','idle_time').order_by('in_date'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)
def m11editdata(request):
    if request.method == "GET" and request.is_ajax():
        sno = request.GET.get('id')
        obj1=list(M11.objects.filter(id=sno).values('id','month','in1','out','in_date','out_date','shift','total_time','detail_no','idle_time').distinct())
        
        context={
            'obj1':obj1,             
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)

def m11updatedata(request):
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get('id') 
        shopsec = request.GET.get('shopsec')
        scat=request.GET.get('scat')
        ename= request.GET.get('empname')
        staff_no = request.GET.get('staff_no')
        month = request.GET.get('month')
        shift = request.GET.get('shift')
        in_date = request.GET.get('in_date')         
        in1 = request.GET.get('in1')                      
        out_date = request.GET.get('out_date')               
        out = request.GET.get('out')
        total_time = request.GET.get('total_time')
        detail_no = request.GET.get('detail_no') 
        idle_time = request.GET.get('idle_time')
        M11.objects.filter(id=id).update(shopsec=shopsec,staff_no=staff_no,in1=str(in1),out=str(out),name=str(ename),cat=scat,month=str(month),total_time=str(total_time),in_date=str(in_date),out_date=str(out_date),shift=str(shift),detail_no=str(detail_no),idle_time=str(idle_time))
         
        obj1=list(M11.objects.filter(staff_no=staff_no,shopsec=shopsec,month=month).values('id','month','in1','out','in_date','out_date','shift','total_time','detail_no','idle_time').order_by('in_date'))

              
        context={
            'obj1':obj1,
            
        }       
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)
