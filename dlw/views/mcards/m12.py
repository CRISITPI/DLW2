from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m12view/')
def m12view(request):
     
    
    tmp=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    
    context={
        'sub':0,
        'len' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'user':g.usermaster,
    }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
            wo_no = req
        context = {
            'sub':0,
            'len' :len(g.rolelist),
            'wo_no':wo_no,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
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
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            month = request.POST.get('month')
            wo_no = request.POST.get('wo_no')
            tempcat=Shemp.objects.filter(staff_no=staff_no).values('cat','name').distinct()
            empname=tempcat[0]['name']
            tcat=tempcat[0]['cat']
            obj1 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('id','cat','time_hrs','in_date','out_date','shift','in1','out','reasons_for_idle_time','total_time','idle_time','month').distinct() 
            obj2='None'
            obj3='None'
            leng=0
            leng1=0
            rr='None'
            amt=0
            patotal=0
            a=0
            b=0
            if len(obj1):
                t=obj1[0]['cat']
                if t != 'None':
                    obj2 = Rates.objects.filter(cat=t).values('avg_rate').distinct()
                    obj3 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('month','cat')[0]
                   
           
                for op in range(len(obj1)):
                    patotal=obj1[op]['total_time']
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
                    amt=Decimal(amt).quantize(Decimal('1.00'))
                leng = obj1.count()
                leng1 = obj2.count()
 
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                    wo_no = req
                context = {
                    'len' :len(g.rolelist),
                    'wo_no':wo_no,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles' :tmp,
                    'user':g.usermaster,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,
                    'sub':1,
                    'tcat':tcat,'empname':empname,
                }
            elif(len(g.rolelist)>1):
                context = {
                    'len' :len(g.rolelist),
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles' :tmp,
                    'user':g.usermaster,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,
                    'sub':1,
                    'tcat':tcat,'empname':empname,
                }
        submitvalue = request.POST.get('PrintPDF')
        if submitvalue=='PrintPDF':
            from decimal import Decimal
            shop_sec = request.POST.get('shopsec')
            staff_no = request.POST.get('staff_no')
            month = request.POST.get('month')
            wo_no = request.POST.get('wo_no')
            tempcat=Shemp.objects.filter(staff_no=staff_no).values('cat','name').distinct()
            empname=tempcat[0]['name']
            tcat=tempcat[0]['cat']
            
            obj1 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('id','cat','time_hrs','in_date','out_date','shift','in1','out','reasons_for_idle_time','total_time','idle_time','month').distinct() 
            
            rr='None'
            amt=0
            patotal=0
            a=0
            b=0
            if len(obj1):
                t=obj1[0]['cat']
                if t != 'None':
                    obj2 = Rates.objects.filter(cat=t).values('avg_rate').distinct()
                    obj3 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('month','cat')[0]
                   
           
                for op in range(len(obj1)):
                    patotal=obj1[op]['total_time']
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
                
            pdf = render_to_pdf('MCARD/M12CARD/M12pdfc.html',context)
            return HttpResponse(pdf, content_type='application/pdf')

        if submitvalue=='submit':
            leng=request.POST.get('len')
            shopsec= request.POST.get('shopsec')
            staff_no = request.POST.get('staff_no')
            month = request.POST.get('month')
            inoutnum=request.POST.get("inoutnum")
            amt = request.POST.get('amt')
            for i in range(1, int(leng)+1):
                in1 = request.POST.get('in1'+str(i))
                out = request.POST.get('out'+str(i))
                date = request.POST.get('date'+str(i))
                month = request.POST.get('month'+str(i))
               
                total_time = request.POST.get('total_time'+str(i))
                time_hrs = request.POST.get('total_time'+str(i))
                idle_time = request.POST.get('idle_time'+str(i))
                reasons_for_idle_time = request.POST.get('reasons_for_idle_time'+str(i))
                M12DOC.objects.filter(shopsec=shopsec,staff_no=staff_no,date=date,month=month).update(date=str(date),in1=str(in1),out=str(out),month=str(month),total_time=str(total_time),idle_time=str(idle_time),reasons_for_idle_time=str(reasons_for_idle_time),time_hrs=str(time_hrs),amt=str(amt))
               

            for i in range(1, int(inoutnum)+1):
                in1 = request.POST.get('in1add'+str(i))
                out = request.POST.get('outadd'+str(i))
                month = request.POST.get('month_add'+str(i))
                total_time = request.POST.get('total_time_add'+str(i))
                date = request.POST.get('dateadd'+str(i))
                cat = request.POST.get('catadd'+str(i))
                time_hrs = request.POST.get('total_time_add'+str(i))
                idle_time = request.POST.get('idle_time_add'+str(i))
                reasons_for_idle_time = request.POST.get('reasons_for_idle_timeadd'+str(i))
            
                M12DOC.objects.create(shopsec=shopsec,staff_no=staff_no,in1=str(in1),out=str(out),month=str(month),total_time=str(total_time),date=str(date),idle_time=str(idle_time),reasons_for_idle_time=str(reasons_for_idle_time),cat=str(cat),time_hrs=str(time_hrs))
              
                wo_no=Batch.objects.all().values('bo_no').distinct()
    return render(request,"MCARD/M12CARD/m12view.html",context)
    
@login_required
@role_required(urlpass='/m12report/')
def m12report(request):
     
    wo_no = empmast.objects.none()
    
    tmp=shop_section.objects.all()
     
    context={
        'sub':0,
        'len' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'user':g.usermaster,
    }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
            wo_no = req
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
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            month = request.POST.get('month')
            wo_no = request.POST.get('wo_no')
            tempcat=Shemp.objects.filter(staff_no=staff_no).values('cat','name').distinct()
            empname=tempcat[0]['name']
            tcat=tempcat[0]['cat']
            obj1 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('id','cat','time_hrs','in_date','out_date','shift','in1','out','reasons_for_idle_time','total_time','idle_time','month').distinct() 
            obj2='None'
            obj3='None'
            leng=0
            leng1=0
            rr='None'
            amt=0
            patotal=0
            a=0
            b=0
            if len(obj1):
                t=obj1[0]['cat']
                if t != 'None':
                    obj2 = Rates.objects.filter(cat=t).values('avg_rate').distinct()
                    obj3 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('month','cat')[0]
                   
           
                for op in range(len(obj1)):
                    patotal=obj1[op]['total_time']
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
                    amt=Decimal(amt).quantize(Decimal('1.00'))
                leng = obj1.count()
                leng1 = obj2.count()
             
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                    wo_no =  req
                context = {
                    'len' :len(g.rolelist),
                    'wo_no':wo_no,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles' :tmp,
                    'user':g.usermaster,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,
                    'sub':1,
                    'tcat':tcat,'empname':empname,
                }
            elif(len(g.rolelist)>1):
                context = {
                    'len' :len(g.rolelist),
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles' :tmp,
                    'user':g.usermaster,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,
                    'sub':1,
                    'tcat':tcat,'empname':empname,
                }

        if submitvalue=='submit':
            leng=request.POST.get('len')
            shopsec= request.POST.get('shopsec')
            staff_no = request.POST.get('staff_no')
            month = request.POST.get('month')
            inoutnum=request.POST.get("inoutnum")
            amt = request.POST.get('amt')
            for i in range(1, int(leng)+1):
                in1 = request.POST.get('in1'+str(i))
                out = request.POST.get('out'+str(i))
                date = request.POST.get('date'+str(i))
                month = request.POST.get('month'+str(i))
               
                total_time = request.POST.get('total_time'+str(i))
                time_hrs = request.POST.get('total_time'+str(i))
                idle_time = request.POST.get('idle_time'+str(i))
                reasons_for_idle_time = request.POST.get('reasons_for_idle_time'+str(i))
                M12DOC.objects.filter(shopsec=shopsec,staff_no=staff_no,date=date,month=month).update(date=str(date),in1=str(in1),out=str(out),month=str(month),total_time=str(total_time),idle_time=str(idle_time),reasons_for_idle_time=str(reasons_for_idle_time),time_hrs=str(time_hrs),amt=str(amt))
               

            for i in range(1, int(inoutnum)+1):
                in1 = request.POST.get('in1add'+str(i))
                out = request.POST.get('outadd'+str(i))
                month = request.POST.get('month_add'+str(i))
                total_time = request.POST.get('total_time_add'+str(i))
                date = request.POST.get('dateadd'+str(i))
                cat = request.POST.get('catadd'+str(i))
                time_hrs = request.POST.get('total_time_add'+str(i))
                idle_time = request.POST.get('idle_time_add'+str(i))
                reasons_for_idle_time = request.POST.get('reasons_for_idle_timeadd'+str(i))
               
              
                M12DOC.objects.create(shopsec=shopsec,staff_no=staff_no,in1=str(in1),out=str(out),month=str(month),total_time=str(total_time),date=str(date),idle_time=str(idle_time),reasons_for_idle_time=str(reasons_for_idle_time),cat=str(cat),time_hrs=str(time_hrs))
             
                
                

                wo_no=Batch.objects.all().values('bo_no').distinct()

        if submitvalue=='PrintPDF':
            from decimal import Decimal
            shop_sec = request.POST.get('shopsec')
            staff_no = request.POST.get('staff_no')
            month = request.POST.get('month')
            wo_no = request.POST.get('wo_no')
            tempcat=Shemp.objects.filter(staff_no=staff_no).values('cat','name').distinct()
            empname=tempcat[0]['name']
            tcat=tempcat[0]['cat']
            obj1 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('id','cat','time_hrs','in_date','out_date','shift','in1','out','reasons_for_idle_time','total_time','idle_time','month').distinct() 
            rr='None'
            amt=0
            patotal=0
            a=0
            b=0
            if len(obj1):
                t=obj1[0]['cat']
                if t != 'None':
                    obj2 = Rates.objects.filter(cat=t).values('avg_rate').distinct()
                    obj3 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('month','cat')[0]
                   
           
                for op in range(len(obj1)):
                    patotal=obj1[op]['total_time']
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
                
            pdf = render_to_pdf('MCARD/M12CARD/M12pdfc.html',context)
            return HttpResponse(pdf, content_type='application/pdf')

    return render(request,"MCARD/M12CARD/m12report.html",context)

def m12save(request):
    if request.method == 'GET' and request.is_ajax():
        shopsec= request.GET.get('shopsec')
        staff_no = request.GET.get('staff_no')
        ename= request.GET.get('ename')
        scat=request.GET.get('scat')
        in_date = request.GET.get('in_date')   
        out_date = request.GET.get('out_date')
        shift = request.GET.get('shift')
        month = request.GET.get('month')
        in1 = request.GET.get('in1')
        out = request.GET.get('out')
        total_time = request.GET.get('total_time')
        idle_time = request.GET.get('idle_time')
        detail_no = request.GET.get('detail_no')
        amt = request.GET.get('amt')
        sender_email_id = 'crisdlwproject@gmail.com'
        sender_email_id_password = 'cris@1234'

        if  month and in1 and out and idle_time and detail_no and total_time:
            M12DOC.objects.create(shopsec=shopsec,staff_no=staff_no,name=str(ename),in1=str(in1),out=str(out),month=str(month),total_time=str(total_time),in_date=str(in_date),out_date=str(out_date),idle_time=str(idle_time),reasons_for_idle_time=str(detail_no),cat=str(scat),amt=str(amt),shift=str(shift))
            
            emp_det=list(emp_details.objects.filter(shopsec=str(shopsec),card_details='M12').values('mobileno','email_id'))
            for x in range(len(emp_det)):

                sms(emp_det[x]['mobileno'],"Machine idle card for Emp number "+ staff_no +" Name "+ ename +" Soap "+ shopsec +" has been generated for the Date "+ in_date +" Total idle time "+idle_time+" ")

                email1(sender_email_id,sender_email_id_password,emp_det[x]['email_id'],'Subject: MACHINE IDLE TIME CARD \n\n   Dear Sir,   Machine idle card for Emp number '+ staff_no +' Name '+ ename +' Soap '+ shopsec +' has been generated for the Date '+ in_date +' Total idle time '+idle_time+' ')
            obj1=list(M12DOC.objects.filter(staff_no=staff_no,shopsec=shopsec,month=month).values('id','month','in1','out','in_date','out_date','shift','total_time','reasons_for_idle_time','idle_time').order_by('in_date'))

            context={
            'obj1':obj1,
                }   
            return JsonResponse({'data':context}, safe = False)
        
    return JsonResponse({"success":False}, status = 400)
def m12indateCheck(request):
    if request.method == 'GET' and request.is_ajax():  
        in_date= request.GET.get('in_date')
        staff_no= request.GET.get('staff_no')
        shop_sec= request.GET.get('shop_sec')
        data_list =list(M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,in_date=in_date).values('in1','in_date','out','out_date','total_time').distinct())
        if(len(data_list)>0):
            return JsonResponse(data_list,safe = False)                         
    return JsonResponse({"success":False},status=400)

def m12editdata(request):
    if request.method == "GET" and request.is_ajax():
        sno = request.GET.get('id')
        obj1=list(M12DOC.objects.filter(id=sno).values('id','month','in1','out','in_date','out_date','shift','total_time','reasons_for_idle_time','idle_time').distinct())
        
        context={
            'obj1':obj1,             
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)

def m12updatedata(request):
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get('id') 
        shopsec = request.GET.get('shopsec')
        scat=request.GET.get('scat')
        ename= request.GET.get('ename')
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
        M12DOC.objects.filter(id=id).update(shopsec=shopsec,staff_no=staff_no,in1=str(in1),out=str(out),name=str(ename),cat=scat,month=str(month),total_time=str(total_time),in_date=str(in_date),out_date=str(out_date),shift=str(shift),reasons_for_idle_time=str(detail_no),idle_time=str(idle_time))
         
        obj1=list(M12DOC.objects.filter(staff_no=staff_no,shopsec=shopsec,month=month).values('id','month','in1','out','in_date','out_date','shift','total_time','reasons_for_idle_time','idle_time').order_by('in_date'))

              
        context={
            'obj1':obj1,
            
        }        
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)
def m12indatelink(request):
    if request.method == 'GET' and request.is_ajax():  
        date= request.GET.get('in_date')
        staff_no= request.GET.get('staff_no')
        shop_sec= request.GET.get('shop_sec')
        data_list =list(M21DOCNEW1.objects.filter(shop_sec=shop_sec,staff_no=staff_no,date=date).values('in1','date','out','outdate','total_time').distinct())
        if(len(data_list)>0):
            return JsonResponse(data_list,safe = False)                         
    return JsonResponse({"success":False},status=400)
                   
def m12getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2=Batch.objects.filter(status='R').values('bo_no').exclude(bo_no__isnull=True).distinct()

        wono = list(w2)
        
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)



def m12getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no = list(M12DOC.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m12getempname(request):
   if request.method == "GET" and request.is_ajax():  
        examcode= request.GET.get('two')
        ex = M5SHEMP.objects.filter(staff_no= examcode).all()  
        exam ={
            "exam_type":ex[0].name,
        }
        return JsonResponse({"exam":exam}, safe = False)
        return JsonResponse({"success":False}, status=400)

    

