from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/screenforloadmasterupdation/')
def screenforloadmasterupdation(request):
    
    wo_nop = empmast.objects.none()
     
    context={
        'nav' : g.nav,
        'ip' : get_client_ip(request),
        'subnav' : g.subnav,
        'usermaster':g.usermaster,
    }
    return render(request, "SHOPADMIN/SCREENFORLOADMASUDT/screenforloadmasterupdation.html",context) 

def ScreenLoadMasterUpdateValidShop(request):
    if request.method == "GET" and request.is_ajax():
        shopsec = request.GET.get('shopsec')
        obj=list(Lc1.objects.filter(shop_sec=shopsec).exclude(del_fl='Y').values('shop_sec'))
        if len(obj) != 0:
            obj=list(shop_section.objects.filter(section_code=shopsec).values('section_desc'))   
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success=false"},status=400)

def ScreenLoadMasterUpdateGetAll(request):
    if request.method == "GET" and request.is_ajax():
        shopsec = request.GET.get('shopsec')
        loadcentre = request.GET.get('loadcentre')
        obj=list(Lc1.objects.filter(shop_sec=shopsec,lcno=loadcentre).exclude(del_fl='Y').values('des','no_men','no_mcs1','no_mcs2','no_mcs3').distinct())
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success=false"},status=400)

def ScreenLoadMasterUpdateSave(request):
    if request.method == "GET" and request.is_ajax():
        obj=[]
        shopsec=request.GET.get('shopsec')
        loadcentre=request.GET.get('loadcentre')
        desc=request.GET.get('desc')
        noman=request.GET.get('noman')
        nomcs1=request.GET.get('nomcs1')
        nomcs2=request.GET.get('nomcs2')
        nomcs3=request.GET.get('nomcs3')
        mwno=request.GET.get('mwno')
        mcgr=request.GET.get('mcgr')
        d1 = date.today()
        temp=list(Lc1.objects.filter(shop_sec=shopsec,lcno=loadcentre).exclude(del_fl='Y').values('shop_sec').distinct())
        if len(temp) == 0:
            temp=Lc1.objects.create(shop_sec=str(shopsec),lcno=str(loadcentre),des=str(desc),
            no_men=noman,no_mcs1=nomcs1,no_mcs2=nomcs2,no_mcs3=nomcs3,updt_dt=d1)
        
        else:
            obj=[1]
        return JsonResponse(obj,safe=False) 
    return JsonResponse({"success:False"},status=400) 

def ScreenLoadMasterUpdateUYes(request):
    if request.method == "GET" and request.is_ajax():
        obj=[]
        shopsec=request.GET.get('shopsec')
        loadcentre=request.GET.get('loadcentre')
        desc=request.GET.get('desc')
        noman=request.GET.get('noman')
        nomcs1=request.GET.get('nomcs1')
        nomcs2=request.GET.get('nomcs2')
        nomcs3=request.GET.get('nomcs3')
        d1 = date.today()
        Lc1.objects.filter(shop_sec=shopsec,lcno=loadcentre).update(shop_sec=str(shopsec),lcno=str(loadcentre),des=str(desc),
            no_men=noman,no_mcs1=nomcs1,no_mcs2=nomcs2,no_mcs3=nomcs3,updt_dt=d1)

        return JsonResponse(obj,safe=False) 
    return JsonResponse({"success:False"},status=400) 

def ScreenLoadMasterUpdateDelete(request):
    if request.method == "GET" and request.is_ajax():
        obj=[]
        shopsec=request.GET.get('shopsec')
        loadcentre=request.GET.get('loadcentre')
        d1 = date.today()
        Lc1.objects.filter(shop_sec=shopsec,lcno=loadcentre).update(del_fl='Y',updt_dt=d1)   
        return JsonResponse(obj,safe=False) 
    return JsonResponse({"success:False"},status=400) 

    
def ScreenLoadMasterUpdateAddMwNo(request):
    if request.method == "GET" and request.is_ajax():
        shopsec=request.GET.get('shopsec')
        loadcentre=request.GET.get('loadcentre')
        mwno=request.GET.get('mwno')
        mcgr=request.GET.get('mcgr')
        desc=request.GET.get('desc')
        obj2=list(Mp.objects.filter(shop_sec=shopsec,lcno=loadcentre,mwno=mwno,mc_gr=mcgr).exclude(del_fl='Y').values('mwno','mc_gr').distinct())
        d1 = date.today()
        if len(obj2) == 0:
            temp=Mp.objects.create(shop_sec=str(shopsec),lcno=str(loadcentre),des=str(desc),
            mwno=str(mwno),mc_gr=str(mcgr),updt_dt=d1)
        
        return JsonResponse(obj2,safe=False) 
    return JsonResponse({"success:False"},status=400) 

def ScreenLoadMasterUpdateDelMwNo(request):
    if request.method == "GET" and request.is_ajax():
        shopsec=request.GET.get('shopsec')
        loadcentre=request.GET.get('loadcentre')
        mwno=request.GET.get('mwno')
        mcgr=request.GET.get('mcgr')
        obj2=list(Mp.objects.filter(shop_sec=shopsec,lcno=loadcentre,mwno=mwno,mc_gr=mcgr).exclude(del_fl='Y').values('mwno').distinct())
        d1 = date.today()
        if len(obj2) != 0:
            Mp.objects.filter(shop_sec=shopsec,lcno=loadcentre,mwno=mwno,mc_gr=mcgr).update(del_fl='Y',updt_dt=d1)   

        return JsonResponse(obj2,safe=False) 
    return JsonResponse({"success:False"},status=400)  

def ScreenLoadMasterUpdateAutoDesc(request):
    if request.method=="GET" and request.is_ajax():
        obj1=list(Lc1.objects.filter(des__isnull=False).values('des').distinct())  
        return JsonResponse(obj1,safe=False)
    return JsonResponse({"success":False}, status=400)

def ScreenLoadMasterUpdateAutomw_no(request):
    if request.method=="GET" and request.is_ajax():
        loadcentre=request.GET.get('loadcentre')
        shopsec=request.GET.get('shopsec')
        obj1=list(Mp.objects.filter(mwno__isnull=False,shop_sec=shopsec,lcno=loadcentre).values('mwno').distinct())  
        return JsonResponse(obj1,safe=False)
    return JsonResponse({"success":False}, status=400)

def ScreenLoadMasterUpdateAutoMcgr(request):
    if request.method=="GET" and request.is_ajax():
        loadcentre=request.GET.get('loadcentre')
        shopsec=request.GET.get('shopsec')
        obj1=list(Mp.objects.filter(mc_gr__isnull=False,shop_sec=shopsec,lcno=loadcentre).values('mc_gr').distinct())  
        return JsonResponse(obj1,safe=False)
    return JsonResponse({"success":False}, status=400) 

def ScreenLoadMasterUpdateView(request):
    if request.method == "GET" and request.is_ajax():
        loadcentre=request.GET.get('loadcentre')
        obj=list(Lc1.objects.filter(lcno=loadcentre).exclude(del_fl='Y').values('lcno','des').distinct())
        return JsonResponse(obj,safe=False) 
    return JsonResponse({"success:False"},status=400) 



