
from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m23view/')
def m23view(request):
    current_time = datetime.datetime.now().strftime("%d-%m-%Y") 
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    name= usermaster.empname
    wo_nop = empmast.objects.none()
    tm=shop_section.objects.all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    context={}
    print(g.rolelist)
    if "Superuser" in g.rolelist:
        
        context={
            'sub':0,
            'lenm' :2,
            'usermaster':g.usermaster,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'current_time':current_time,
            'name':name,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = M5SHEMP.objects.filter(shopsec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
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
            'current_time':current_time,
            'name':name
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
            'current_time':current_time,
            'name':name,
            
        }
    a=[]
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            from datetime import date
            from time import gmtime, strftime 
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            ddate = request.POST.get('ddate')
            obj1 =  M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name').distinct()
            noprint=0
            tod = date.today()
           
            ctime=(strftime("%H:%M"))
            idlist=(list(m23doc.objects.values('id')))
            for i in range(len(idlist)):
                a.append(idlist[i]['id'])
            
            sno=0
            if(a==[]):
                a=0
                sno=1
            else:
                sno=max(a)+1
            
            
            context = {
                'ctime':ctime, 
                'sno':sno, 
                'obj1': obj1,                 
                'ran':range(1,32),
                'len': 31,
                'usermaster':g.usermaster,
                'shop_sec': shop_sec,
                 'noprint':noprint,               
                'staff_no': staff_no,                 
                'curdate':tod,
                'sub':1,
                'nav':g.nav,
                'ddate': ddate,
                'ip':get_client_ip(request),  
                'subnav':g.subnav, 
                'current_time':current_time  
            }
        if submitvalue =='Save':
                    leng=request.POST.get('len')
                    
                    todate=request.POST.get('d1date')
                    sno=request.POST.get('sno')
                    from_time = request.POST.get('from_time')
                    to_time = request.POST.get('to_time')
                    purpose = request.POST.get('pur')
                    shops=request.POST.get('shopsec')
                    staffn=request.POST.get('staffno')
                    date=request.POST.get('dddate')
                    name=request.POST.get('employeename')
                     
                    now = datetime.datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    if(todate==date):

                        if to_time >= from_time and from_time >= current_time or from_time == current_time  :
                            m23obj1 = m23doc.objects.filter(shop_no=shops,emp_no=staffn, date=date).values('to_time')
                            if len(m23obj1)>0 :
                                if (m23obj1[0]['to_time'] <= str(from_time) and str(from_time) <= str(to_time) ) :
                                    m23doc.objects.create(shop_no=str(shops),emp_no=str(staffn),emp_name=str(name), from_time=str(from_time), to_time=str(to_time), purpose=str(purpose), date=str(date),sno=sno,todate=todate)
                                    messages.success(request,'New gate pass created')
                                    return HttpResponseRedirect("/m23report/") 
                                else :
                                    messages.success(request,'From-time and to-time of new gate pass should be greater than issued time of previous gate pass')
                            else:
                                m23doc.objects.create(shop_no=str(shops),emp_no=str(staffn),emp_name=str(name), from_time=str(from_time), to_time=str(to_time), purpose=str(purpose), date=str(date),sno=sno,todate=todate)
                                messages.success(request,'First gate pass created')
                                return HttpResponseRedirect("/m23report/") 
                        else :
                            messages.success(request,'To_time should be greater than From_time  and from time should be greater than current time')
                    else:
                        m23doc.objects.create(shop_no=str(shops),emp_no=str(staffn),emp_name=str(name), from_time=str(from_time), to_time=str(to_time), purpose=str(purpose), date=str(date),sno=sno,todate=todate)
                        messages.success(request,'New gate pass created')  
                        return HttpResponseRedirect("/m23report/")     
        if submitvalue=='Generate report':
            return m23report(request)
    
    return render(request,"MCARD/M23CARD/m23view.html",context)
                        

def m23getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')        
        staff_no=list(M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def getm23date(request):
    from .models import m23doc
    if request.method == "GET" and request.is_ajax():
        shopsec = request.GET.get('shpsec')
        stfno=request.GET.get('stfno')
        cdate=request.GET.get('insertdate') 
        cddate=list(m23doc.objects.filter(shop_no=shopsec,emp_no=stfno).values('date').order_by('-id'))
        print("list")
        print(cddate)
        return JsonResponse(cddate, safe = False)
    return JsonResponse({"success":False}, status=400)
  
@login_required 
def m23report(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first() 
    name=usermaster.empname
    tabledata=m23doc.objects.values().all()
    if "Superuser" in g.rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'usermaster':g.usermaster,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'tabledata':tabledata,
            'name':name
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
           
            w1 = M5SHEMP.objects.filter(shopsec=rolelist[i]).values('empno').distinct()
             
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist), 
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            
            'roles' :g.rolelist,
            'tabledata':tabledata,
            'name':name
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
            'tabledata':tabledata,
            'name':name
            
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='proceed':
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            ddate = request.POST.get('ddate')
            print(shop_sec,staff_no,ddate)
            obj1 = m23doc.objects.filter(shop_no=shop_sec,emp_no=staff_no,date=ddate).values().distinct()
            obj2 = m23doc.objects.filter(shop_no=shop_sec,emp_no=staff_no,date=ddate).values('emp_name').distinct()
            leng = obj1.count()
            print("obj1",obj1)
            context = {
                'obj1': obj1,
                'obj2': obj2,
                'ran':range(1,32),
                'len': 31,
               
                'shop_sec': shop_sec,
               
                'staff_no': staff_no,
                
                'sub':1,
                'nav':g.nav,
                'ip':get_client_ip(request),  
                'subnav':g.subnav,  
                'date': ddate, 
                'tabledata':tabledata,
                'name':name
            }
            pdf = render_to_pdf('MCARD/M23CARD/M23pdf.html',context)
            return HttpResponse(pdf, content_type='application/pdf')
    if request.method == "POST":
        
        submitvalue = request.POST.get('print')
        if submitvalue=='print':
            shop_sec = request.POST.get('test1')
            staff_no = request.POST.get('test3')
            ddate = request.POST.get('test2')
            print(shop_sec,staff_no,ddate)
            obj1 = m23doc.objects.filter(shop_no=shop_sec,emp_no=staff_no,date=ddate).values().distinct()
            obj2 = m23doc.objects.filter(shop_no=shop_sec,emp_no=staff_no,date=ddate).values('emp_name').distinct()
            leng = obj1.count()
            print("obj1",obj1)
            context = {
                'obj1': obj1,
                'obj2': obj2,
                'ran':range(1,32),
                'len': 31,
                
                'shop_sec': shop_sec,
                
                'staff_no': staff_no,
                'usermaster':g.usermaster,
                'sub':1,
                'nav':g.nav,
                'ip':get_client_ip(request),  
                'subnav':g.subnav,  
                'date': ddate, 
                'tabledata':tabledata,
                'name':name
            }
            pdf = render_to_pdf('MCARD/M23CARD/M23pdf.html',context)
            return HttpResponse(pdf, content_type='application/pdf')
            if submitvalue =='Submit':
                leng=request.POST.get('len')
                shop_sec= request.POST.get('s_spass')
                staff_no = request.POST.get('s_fpass')  
                m23obj = M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).distinct()
              
                if((m23obj)):
                    m23obj.delete() 
                from_time = request.POST.get('from_time')
                to_time = request.POST.get('to_time')
                purpose = request.POST.get('pur')
                shops=request.POST.get('shopsec')
                staffn=request.POST.get('staffno')
                
                if from_time and to_time and purpose :
                    
                    objjj=m23doc.objects.create()
                    objjj.shop_no=shops
                    objjj.emp_no=staffn
                    objjj.emp_name=request.POST.get('employeename')
                    objjj.from_time=from_time
                    objjj.to_time=to_time
                    objjj.purpose=purpose
                    objjj.save()
                    
                    
                wo_nop=M5SHEMP.objects.all().values('staff_no').distinct()
        if request.method == "POST":
            submitvalue = request.POST.get('back')
            if submitvalue=='back':
                return m23view(request)
        if request.method == "POST":
            submitvalue = request.POST.get('edit')
            if submitvalue=='edit':
                sno=request.POST.get('test')
                shopsec=request.POST.get('test1')
                empno=request.POST.get('test3')
                date=request.POST.get('test2')
                name=request.POST.get('test4')
                fdate=request.POST.get('test5')
                tdate=request.POST.get('test6')
                ftime=request.POST.get('test7')
                ttime=request.POST.get('test8')
                purpose=request.POST.get('test9')
                context={
                   'shopsec':shopsec,
                    'empno':empno,
                    'curdate':date,
                    'name':name,
                    'sno':sno,
                    'ftime':ftime,
                    'ttime':ttime,
                    'fdate':fdate,
                    'tdate':tdate,
                    'purpose':purpose,
                    'name':name
                }
                return render(request,"MCARD/M23CARD/m23edit.html",context) 

    return render(request,"MCARD/M23CARD/m23report.html",context)
    
def m23edit(request):
    cuser=request.user 
    tabledata=m23doc.objects.values().all()
    tm=shop_section.objects.all()
    
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    context={
        'sub':0,
        'lenm' :2,
        'usermaster':g.usermaster,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'tabledata':tabledata
    }
    if request.method == "POST":
        submitvalue = request.POST.get('update')
        if submitvalue=='update':
             
            sno=request.POST.get('sno')
            purpose=request.POST.get('pur')
            fdate=request.POST.get('f1date')
            tdate=request.POST.get('d1date')
            ftime=request.POST.get('ftime')
            ttime=request.POST.get('ttime')
            m23doc.objects.filter(id=sno).update(from_time=str(ftime), to_time=str(ttime), purpose=str(purpose), date=str(fdate),todate=tdate)
            messages.success(request,' Gate pass is updated')
            return HttpResponseRedirect("/m23report/") 
    return render(request,"MCARD/M23CARD/m23edit.html",context)

def m23pdf(request, *args, **kwargs):

    pdf = render_to_pdf('MCARD\M23CARD/M23pdf.html',context)
    return HttpResponse(pdf, content_type='application/pdf')


