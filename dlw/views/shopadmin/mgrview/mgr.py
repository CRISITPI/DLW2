from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/mgrview/')
def mgrview(request):
    import datetime
    
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    wo_nop = empmast.objects.none()
        
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
            req = ms_tools_master.objects.all().filter(shop_code=g.rolelist[i]).values('instrument_number').distinct()
            instrument_number = instrument_number | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'instrument_number':instrument_number,
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
            'roles' :g.rolelist,
            'subnav':g.subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            
            shop_sec = request.POST.get('shop_sec')
            instrument_number = request.POST.get('ins_no')
            obj = ms_tools_master.objects.filter(shop_code=shop_sec,instrument_number=instrument_number).values('calibration_frequency','employee','user_id').distinct()
            obj1 = Mgr.objects.filter(instrument_number=instrument_number).values('tool_des','type_mme','least_count')
            noprint=0
            leng = obj.count()
            leng1 = obj1.count()
            if len(obj1) == 0:
                noprint=1
            
            
                
            context={
                    
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                    'ip':get_client_ip(request),  
                    'usermaster':g.usermaster,
                }
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    req = ms_tools_master.objects.all().filter(shop_code=g.rolelist[i]).values('instrument_number').distinct()
                    instrument_number = instrument_number | req
                context = {
                    
                    'lenm' :len(g.rolelist),
                    'instrument_number':instrument_number,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :g.rolelist,
                    'subnav':g.subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                    'ip':get_client_ip(request),  
                }
        
            elif(len(g.rolelist)>1):
                context = {
                    
                    'lenm':len(g.rolelist),
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :g.rolelist,
                    'subnav':g.subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                }
        if submitvalue =='Submit':
                
                leng=request.POST.get('len')
                now = datetime.datetime.now()
                shop_sec = request.POST.get('shop_sec')
                instrument_number = request.POST.get('ins_no')
                tool_des = request.POST.get('tool_des')
                type_mme = request.POST.get('type_mme')
                least_count = request.POST.get('least_count')
                calibration_frequency = request.POST.get('calibration_frequency')
                employee = request.POST.get('employee')
                mgrobj = Mgr.objects.filter(shop_sec=shop_sec,instrument_number=instrument_number).distinct()
                if len(mgrobj) == 0:
                    
                    Mgr.objects.create(login_id=request.user,shop_sec=str(shop_sec),instrument_number=str(instrument_number),tool_des=str(tool_des),type_mme=str(type_mme),
                    least_count=str(least_count),calibration_frequency=str(calibration_frequency),employee=str(employee),last_modified=str(now))
                
                else:
                    Mgr.objects.filter(shop_sec=shop_sec,instrument_number=instrument_number).update(tool_des=str(tool_des),type_mme=str(type_mme),
                    least_count=str(least_count),calibration_frequency=str(calibration_frequency),employee=str(employee),last_modified=str(now))

                instrument_number=Mgr.objects.all().values('instrument_number').distinct()

        if submitvalue =='Proceed to Report':
            return mgrreports(request)
        

    return render(request,"SHOPADMIN/MGRVIEW/mgrview.html",context)





def mgrgetinsno(request):
    if request.method == "GET" and request.is_ajax():
        
        shop_sec = request.GET.get('shop_sec')
        instrument_number=list(ms_tools_master.objects.filter(shop_code=shop_sec).values('instrument_number').distinct())
        return JsonResponse(instrument_number, safe = False)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/mgrview/')
def mgrreports(request):
    wo_nop = empmast.objects.none()
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
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
            req = ms_tools_master.objects.all().filter(shop_code=g.rolelist[i]).values('instrument_number').distinct()
            instrument_number = instrument_number | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'instrument_number':instrument_number,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist,
            'subnav':g.subnav,
            'usermaster':g.usermaster,

        }
        
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist,
            'subnav':g.subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed to Report':
            
            shop_sec = request.POST.get('shop_sec')
            instrument_number = request.POST.get('ins_no')
            obj = Mgr.objects.filter(shop_sec=shop_sec).values('instrument_number').distinct()
            obj1 = mgrreport.objects.filter(shop_sec=shop_sec,instrument_number=instrument_number).values('tool_des','range','periodicity_check','date_calibration','calibration_status','calibration_due_date')
            noprint=0
            leng = obj.count()
            leng1 = obj1.count()
            if len(obj1) == 0:
                noprint=1
            
            tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
            tmp=[]
            for on in tm:
                tmp.append(on.section_code)
            context={
                
                'lenm' :2,
                'nav':g.nav,
                'subnav':g.subnav,
                'ip':get_client_ip(request),
                'roles':tmp,
                'obj': obj,
                'obj1': obj1,
                'len': leng,
                'len1': leng1,
                'shop_sec': shop_sec,
                'instrument_number':instrument_number,
                'sub' : 1,
                'noprint':noprint,
                'ip':get_client_ip(request),  
                'usermaster':g.usermaster,
            }
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    req = ms_tools_master.objects.all().filter(shop_code=g.rolelist[i]).values('instrument_number').distinct()
                    instrument_number = instrument_number | req
                context = {
                    
                    'lenm' :len(g.rolelist),
                    'instrument_number':instrument_number,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :g.rolelist,
                    'subnav':g.subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                    'noprint':noprint,
                    'nav':g.nav,
                    'ip':get_client_ip(request),  
                }
        
            elif(len(g.rolelist)>1):
                context = {
                    
                    'lenm' :len(g.rolelist),
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :g.rolelist,
                    'subnav':g.subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                    'noprint':noprint,
                    'nav':g.nav,
                    'ip':get_client_ip(request),  
                    'subnav':g.subnav,
                }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Submit':
            now = datetime.datetime.now()
            shop_sec = request.POST.get('shop_sec')
            instrument_number = request.POST.get('ins_no')
            tool_des = request.POST.get('tool_des')
            range = request.POST.get('range')
            periodicity_check = request.POST.get('periodicity_check')
            date_calibration = request.POST.get('date_calibration')
            calibration_status = request.POST.get('calibration_status')
            calibration_due_date = request.POST.get('calibration_due_date')
            

            mgrobj1 = mgrreport.objects.filter(shop_sec=shop_sec,instrument_number=instrument_number).distinct()
            if len(mgrobj1) == 0:
                    
                    mgrreport.objects.create(login_id=request.user,range=str(range),tool_des=str(tool_des),periodicity_check=str(periodicity_check),shop_sec=str(shop_sec),instrument_number=str(instrument_number),
                    date_calibration=str(date_calibration),calibration_status=str(calibration_status),last_modified=str(now),calibration_due_date=str(calibration_due_date))

            else:

                    mgrreport.objects.filter(shop_sec=shop_sec,instrument_number=instrument_number).update(tool_des=str(tool_des),range=str(range),periodicity_check=str(periodicity_check),
                    date_calibration=str(date_calibration),login_id=request.user,last_modified=str(now),calibration_status=str(calibration_status),calibration_due_date=str(calibration_due_date))

            instrument_number=Mgr.objects.all().values('instrument_number').distinct()

        

    return render(request,"SHOPADMIN/MGRVIEW/mgrREPORT.html",context)

