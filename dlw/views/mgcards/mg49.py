from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/mg49view/')
def mg49view(request):
    import datetime     
    wo_nop = empmast.objects.none()
    tm=Shemp.objects.all().values('shopsec').distinct()    
    tmp=[]
    for on in tm:
        tmp.append(on['shopsec'])
         
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'usermaster':g.usermaster,
        }
    if(len(rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = Shemp.objects.all().filter(shop_sec=g.rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'staff_no':staff_no,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :tmp,
             'usermaster':g.usermaster,
        }
        
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            tm1=Part.objects.all().values('des').distinct()
            
            temp=Part.objects.all().values('shop_ut').distinct()
            tm2=Code.objects.filter(code__in=temp,cd_type='51').values('alpha_1').distinct()
            
            shop_sec = request.POST.get('shop_sec')
            updt_date = request.POST.get('updt_date')
            staff_no = request.POST.get('staff_no')

            obj = Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name','desgn').distinct().order_by('-yymm')[0];
            leng = 1
            tm=Shemp.objects.all().values('shopsec').distinct()
                
            tmp=[]
            for on in tm:
                    tmp.append(on['shopsec'])
            context={
                    'tm1':tm1,
                    'tm2':tm2,
                    'obj': obj,
                    'len': leng,
                    'updt_date':updt_date,
                    'shop_sec': shop_sec,
                    'staff_no':staff_no,
                    'sub' : 1,
                    'lenm' :2,
                    'roles':tmp,
                    'nav':g.nav,
                    'ip':get_client_ip(request),  
                    'subnav':g.subnav,
                    'usermaster':g.usermaster,
                }
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    req = Shemp.objects.all().filter(shop_sec=g.rolelist[i]).values('staff_no').distinct()
                    staff_no =staff_no | req
                context = {
                    'tm1':tm1,
                    'tm2':tm2,
                    'obj': obj,
                    'len': leng,
                    'updt_date':updt_date,
                    'shop_sec': shop_sec,
                    'staff_no':staff_no,
                    'sub' : 1,
                    'nav':g.nav,
                    'ip':get_client_ip(request),  
                    'subnav':g.subnav,
                    'usermaster':g.usermaster,
                }
            elif(len(g.rolelist)>1):
                context = {
                    'tm1':tm1,
                    'tm2':tm2,
                    'obj': obj,
                    'len': leng,
                    'updt_date':updt_date,
                    'shop_sec': shop_sec,
                    'staff_no':staff_no,
                    'sub' : 1,
                    'nav':g.nav,
                    'ip':get_client_ip(request),  
                    'subnav':g.subnav,
                    'usermaster':g.usermaster,
                }
        
        if submitvalue=='submit':
            updt_date = request.POST.get('update')
            shop_sec= request.POST.get('shopsec')
            staff_no = request.POST.get('staffno')
            part_no = request.POST.get('part_no')
            matdes = request.POST.get('matdes')
            quantity = request.POST.get('quantity')
            weight = request.POST.get('weight')
            unit = request.POST.get('unit')
            now = datetime.datetime.now()
            user=request.user
            MG49.objects.create(shopsec=str(shop_sec), staff_no=str(staff_no), date=str(updt_date), part_no=str(part_no), desc=str(matdes), quan=str(quantity), weight=str(weight),login_id=str(user), last_modified=str(now), unit=str(unit))

            totindb=request.POST.get('totmebs')
            print('totindb',totindb)
            for tb in range(2,int(totindb)+1):
                part_no=request.POST.get('part_no'+str(tb))
                shop_sec= request.POST.get('shopsec')
                staff_no = request.POST.get('staffno')
                matdes=request.POST.get('matdes'+str(tb))
                quantity=request.POST.get('quan'+str(tb))
                weight=request.POST.get('weight'+str(tb))
                unit=request.POST.get('unit'+str(tb))
                now = datetime.datetime.now()
                user=request.user
                updt_date = request.POST.get('update')
                MG49.objects.create(shopsec=str(shop_sec), staff_no=str(staff_no), date=str(updt_date), part_no=str(part_no),desc=str(matdes), quan=str(quantity), weight=str(weight),login_id=str(user), last_modified=str(now), unit=str(unit))

        
    return render(request,"MGCARD/MG49CARD/mg49view.html",context)


def mg49getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg49getpart_no(request):
    
    if request.method == "GET" and request.is_ajax():
        matdes = request.GET.get('matdes')
        w1 = list(Part.objects.filter(des=matdes).values('partno').distinct())
        w2 = list(Part.objects.filter(des=matdes).values('shop_ut').distinct())
        ut=w2[0]['shop_ut']
        tm2=Code.objects.filter(code=ut,cd_type='51').values('alpha_1').distinct()
        wono = w1[0]['partno']
        if(tm2.count()==0):
            k='NULL'
        else:
            k=tm2[0]['alpha_1']


        cont ={
            "wono":wono,
            "ut":k,
        }
        
        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)


def mg49report(request):
    
    tm1=Part.objects.all().values('partno').distinct()
    
    staff_no = empmast.objects.none()
    tm=Shemp.objects.all().values('shopsec').distinct()
        
    tmp=[]
    
    for on in tm:
            tmp.append(on['shopsec'])
        
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'tm1':tm1,
            'subnav':g.subnav,
        }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = Shemp.objects.all().filter(shop_sec=g.rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'staff_no':staff_no,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles' :g.rolelist
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :g.rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            
            
            shop_sec = request.POST.get('shop_sec')
            updt_date = request.POST.get('updt_date')
            staff_no = request.POST.get('staff_no')
            part_no=request.POST.get('part_no')
            obj = Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name','desgn').distinct().order_by('-yymm')[0];
            leng = 1
            alldata = MG49.objects.filter(shopsec=shop_sec,staff_no=staff_no,date=updt_date).values('shopsec','staff_no','date','part_no','quan','weight','login_id','unit','desc').distinct();
            
            leng2 = alldata.count()
            context = {
                        'tm1':tm1,
                        'alldata':alldata,
                        'tm1':tm1,
                        'obj': obj,
                        'len': leng,
                        'len2':leng2,
                        'updt_date':updt_date,
                        'shop_sec': shop_sec,
                        'staff_no':staff_no,
                        'sub' : 1,
                        'nav':g.nav,
                        'ip':get_client_ip(request),  
                        'subnav':g.subnav,
            }
    return render(request,"MGCARD/MG49CARD/mg49report.html",context)
