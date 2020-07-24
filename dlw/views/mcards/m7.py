from dlw.views import *
import dlw.views.globals as g
                       
def m7getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2=Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)
def m7getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        
        wo_no = request.GET.get('wo_no')
        
        part_no = list(Batch.objects.filter(bo_no=wo_no).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m7getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        staff_no=list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/m7view/')
def m7view(request):
     
    wo_nop = empmast.objects.none()
    
    tmp=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
     
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
    }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
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
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mon = request.POST.get('mon')
            wo_no = request.POST.get('wo_no')
            staff_no = request.POST.get('staff_no')
            part_no = request.POST.get('part_no')
            obj1 = M7.objects.filter(staff_no=staff_no).values('month','date','in1','out')
            obj2 = Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name','cat').distinct()
            leng = obj1.count()
            leng2 = obj2.count()
             
            context={
                'sub':0,
                'lenm' :2,
                'nav':g.nav,
                'subnav':g.subnav,
                'ip':get_client_ip(request),
                'roles':tmp,
                'obj1': obj1,
                'obj2': obj2,
                'ran':range(1,2),
                'len': 31,
                'len2': leng2,
                'shop_sec': shop_sec,
                'wo_no': wo_no,
                'staff_no': staff_no,
                'part_no': part_no, 
                'mon': mon,
                'sub':1,
                'nav':g.nav,
                'ip':get_client_ip(request),  
                'subnav':g.subnav, 
            }
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                    wo_nop =wo_nop | req
                context = {
                    'sub':0,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    'subnav':g.subnav,
                    'obj1': obj1,
                    'obj2': obj2,
                    'ran':range(1,2),
                    'len': 31,
                    'len2': leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no': staff_no,
                    'part_no': part_no, 
                    'mon': mon,
                    'sub':1,
                    'nav':g.nav,
                    'ip':get_client_ip(request),  
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
                    'obj1': obj1,
                    'obj2': obj2,
                    'ran':range(1,2),
                    'len': 31,
                    'len2': leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no': staff_no,
                    'part_no': part_no, 
                    'mon': mon,
                    'sub':1,
                    'nav':g.nav,
                    'ip':get_client_ip(request),  
                    'subnav':g.subnav, 
                }

        if submitvalue =='Submit':
                leng=request.POST.get('len')
                shop_sec= request.POST.get('shopsec')
                staff_no = request.POST.get('staffno')
                wo_no = request.POST.get('wono')
                part_no = request.POST.get('partno')
                inoutnum=request.POST.get("inoutnum")
                m7obj = M7.objects.filter(shop_sec=shop_sec,staff_no=staff_no,part_no=part_no).distinct()
                if((m7obj)):
                    m7obj.delete()
                
                for i in range(1, int(leng)+1):
                    in1 = request.POST.get('in1'+str(i))
                    out = request.POST.get('out'+str(i))
                    date = request.POST.get('date'+str(i))
                    mon = request.POST.get('mon'+str(i))
                
                    if in1 and out and date and mon :
                        objjj=M7.objects.create()
                        objjj.shop_sec=shop_sec
                        objjj.staff_no=staff_no
                        objjj.part_no=part_no
                        objjj.in1=in1
                        objjj.out=out
                        objjj.mon=mon
                        objjj.date=date
                        objjj.save()

                for i in range(1, int(inoutnum)+1):
                    in1 = request.POST.get('in1add'+str(i))
                    out = request.POST.get('outadd'+str(i))
                    month = request.POST.get('month_add'+str(i))
                    date = request.POST.get('dateadd'+str(i))

                    if in1 and out and date and mon :
                        obj5=M7.objects.create()
                        obj5.shop_sec=shop_sec
                        obj5.staff_no=staff_no
                        obj5.part_no=part_no
                        obj5.in1=in1
                        obj5.out=out
                        obj5.mon=mon
                        obj5.date=date
                        obj5.save()

                    
                wo_nop=Batch.objects.all().values('bo_no').distinct()
 
    return render(request,"MCARD/M7CARD/m7view.html",context)
       