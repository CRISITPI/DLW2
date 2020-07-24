

from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/mg9initialreportviews/')
def mg9initialreportviews(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = user_master.objects.none()
    tool_no = Tools.objects.values('tool_code').exclude(tool_code__isnull=True).distinct()
    prtlist=[]
    for i in tool_no:
        prtlist.append(i['tool_code'])
    ticket_no = empmast.objects.values('ticket_no').exclude(ticket_no__isnull=True).distinct()
    prtticket=[]
    for i in ticket_no:
        prtticket.append(i['ticket_no'])
    empno = empmast.objects.filter(payrate__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtemp=[]
    for i in empno:
        prtemp.append(i['empno'])
    empno = empmast.objects.filter(scalecode__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtsec=[]
    for i in empno:
        prtsec.append(i['empno'])
    if "Superuser" in rolelist:
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
           
            'roles':tmp,
            'subnav':subnav,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,

        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,    
            'prtemp':prtemp,
            'prtsec':prtsec,
                }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mw_no = request.POST.get('mwno')
            staff_no = request.POST.get('staffno')
            
            current_yr=int(datetime.datetime.now().year)


            obj  = MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).values('sec','mw_no','sl_no','staff_no','handed_date','comp_date','handed_time','comp_time','handed_cmsec','comp_cmsec','handed_cmserv','comp_cmserv','complaint','action').distinct()
            obj1  = MG9Initial.objects.values('id').count()

            leng = obj.count()
            slno=obj1
            slno=slno+1
         
            
            if "Superuser" in rolelist:
                    tm=M5SHEMP.objects.all().values('shopsec').distinct()
                    tmp=[]
                    for on in tm:
                        tmp.append(on['shopsec'])
                    context={
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,   
                        'obj':obj,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'slno':slno,
                        'subnav':subnav,
                        'prtlist':prtlist,
                        'prtticket':prtticket,
                        'prtemp':prtemp,
                        'prtsec':prtsec,



                    }
            elif(len(rolelist)==1):
                    for i in range(0,len(rolelist)):
                        req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
                        wo_nop =wo_nop | req
                    context = {
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,
                        'obj':obj,
                        'slno':slno,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                     
                      
                        'subnav':subnav,
                    }
            elif(len(rolelist)>1):
                    context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'len':leng,
                        'obj':obj,
                        'slno':slno,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                  
                        'subnav':subnav
                    }    
        if submitvalue=='submit':
                    leng=request.POST.get('len')
                    now = datetime.datetime.now()
                    shop_sec=request.POST.get('shop_sec')
                    mw_no = request.POST.get('mw_no')
                    staff_no = request.POST.get('staff_no')
                    comp= request.POST.get('complaint')
                    date_handed=request.POST.get('date_handed')
                    date_com=request.POST.get('date_com')
                    time_handed=request.POST.get('time_handed')
                    time_com=request.POST.get('time_com')
                    sec_handed = request.POST.get('sec_handed')
                    sec_com = request.POST.get('sec_com')
                    serv_com = request.POST.get('serv_com')
                    serv_handed = request.POST.get('serv_handed')
                    action= request.POST.get('action')
                    sl_no = request.POST.get('sl_no')

          

                    mg9obj = MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).distinct()
                    if len(mg9obj) == 0:


                        MG9Initial.objects.create(sec=str(shop_sec),mw_no=str(mw_no),sl_no=str(sl_no),staff_no=str(staff_no),complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=request.user)
                    else:

                        MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).update(complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now))
                       
    return render(request,"mg9initialreportviews.html",context)

def mg9getmw(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(Lc1.objects.filter(shop_sec = shop_sec).values('lcno').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg9getstaff(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(staff, safe = False)
    return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/mg9compreportviews/')
def mg9compreportviews(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = user_master.objects.none()
    tool_no = Tools.objects.values('tool_code').exclude(tool_code__isnull=True).distinct()
    prtlist=[]
    for i in tool_no:
        prtlist.append(i['tool_code'])
    ticket_no = empmast.objects.values('ticket_no').exclude(ticket_no__isnull=True).distinct()
    prtticket=[]
    for i in ticket_no:
        prtticket.append(i['ticket_no'])
    empno = empmast.objects.filter(payrate__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtemp=[]
    for i in empno:
        prtemp.append(i['empno'])
    empno = empmast.objects.filter(scalecode__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtsec=[]
    for i in empno:
        prtsec.append(i['empno'])
    if "Superuser" in rolelist:
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
           
            'roles':tmp,
            'subnav':subnav,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,

        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,    
            'prtemp':prtemp,
            'prtsec':prtsec,
                }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mw_no = request.POST.get('mwno')
            staff_no = request.POST.get('staffno')
            
            current_yr=int(datetime.datetime.now().year)


            obj2 = MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no).values('sl_no','handed_date','handed_time','handed_cmserv','handed_cmsec','complaint').distinct()
            obj  = MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).values('sec','mw_no','staff_no','comp_date','comp_time','comp_cmsec','comp_cmserv','action','total_losthrs','cause_hrs','mp_time','mismp_time','inv_time').distinct()
        
            leng = obj.count()
            leng2 = obj2.count()
            if "Superuser" in rolelist:
                    tm=M5SHEMP.objects.all().values('shopsec').distinct()
                    tmp=[]
                    for on in tm:
                        tmp.append(on['shopsec'])
                    context={
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,   
                        'obj':obj,
                        'obj2':obj2,
                        'len2':leng2,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'cyear':current_yr,
                        'subnav':subnav,
                        'prtlist':prtlist,
                        'prtticket':prtticket,
                        'prtemp':prtemp,
                        'prtsec':prtsec,



                    }
            elif(len(rolelist)==1):
                    for i in range(0,len(rolelist)):
                        req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
                        wo_nop =wo_nop | req
                    context = {
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,
                        'obj':obj,
                        'obj2':obj2,
                        'len2':leng2,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'cyear':current_yr,
                        'subnav':subnav,
                    }
            elif(len(rolelist)>1):
                    context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'len':leng,
                        'obj':obj,
                        'obj2':obj2,
                        'len2':leng2,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'cyear':current_yr,
                        'subnav':subnav
                    }    
        if submitvalue=='submit':
                    leng=request.POST.get('len')
                    now = datetime.datetime.now()
                    shop_sec=request.POST.get('shop_sec')
                    mw_no = request.POST.get('mw_no')
                    staff_no = request.POST.get('staff_no')
                    comp= request.POST.get('complaint')
                    date_handed=request.POST.get('date_handed')
                    date_com=request.POST.get('date_com')
                    time_handed=request.POST.get('time_handed')
                    time_com=request.POST.get('time_com')
                    sec_handed = request.POST.get('sec_handed')
                    sec_com = request.POST.get('sec_com')
                    serv_com = request.POST.get('serv_com')
                    serv_handed = request.POST.get('serv_handed')
                    action= request.POST.get('action')
                    sl_no = request.POST.get('sl_no')
                    lost_hrs = request.POST.get('lost_hrs')
                    elec = request.POST.get('elec')
                    mech = request.POST.get('mech')
                    mech_ele = request.POST.get('mech_ele')
                    mp = request.POST.get('mp')
                    inv = request.POST.get('inv')
                    mismp = request.POST.get('mismp')
                    inv_time = request.POST.get('inv_time')
                    mismp_time = request.POST.get('mismp_time')
                    mp_time=request.POST.get('mp_time')



                   
                    tmp=""
                    if(elec is not None):
                        tmp=str(elec)+str("   ")
                    if(mech is not None):
                        tmp=tmp+str(mech)+str("   ")
                    if(mech_ele is not None):
                        tmp=tmp+str(mech_ele)+str("   ")
                    if(mp is not None):
                        tmp=tmp+str(mp)+str("   ")
                    if(inv is not None):
                        tmp=tmp+str(inv)+str("   ")
                    if(mp_time is None):
                        mp_time='00:00'
                    if(inv_time is None):
                        inv_time='00:00'
                    if(mismp_time is None):
                        mismp_time='00:00'                   

                    mg9obj = MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).distinct()
                    if len(mg9obj) == 0:
                        MG9Complete.objects.create(sec=str(shop_sec),mw_no=str(mw_no),sl_no=str(sl_no),staff_no=str(staff_no),complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=request.user,total_losthrs=str(lost_hrs),cause_hrs=str(tmp),mp_time=str(mp_time),inv_time=str(inv_time),mismp_time=str(mismp_time))
                    else:
                        cause=request.POST.get('cause_hrs')

                        MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).update(complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=str(request.user),total_losthrs=str(lost_hrs),cause_hrs=str(cause),mp_time=str(mp_time),inv_time=str(inv_time),mismp_time=str(mismp_time))
                
    return render(request,"mg9compreportviews.html",context)

def mg9getmwno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(Lc1.objects.filter(shop_sec = shop_sec).values('lcno').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)


def mg9getstaffno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(staff, safe = False)
    return JsonResponse({"success":False}, status=400)

