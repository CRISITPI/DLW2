from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/mg6views/')
def mg6views(request):
    rolelist=(g.usermaster).role.split(", ")
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
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    tmp=[]
    for on in tm:
            tmp.append(on.section_code)
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,
            'usermaster':g.usermaster,

        }
    if(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,
            'usermaster':g.usermaster,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,    
            'prtemp':prtemp,
            'prtsec':prtsec,
            'usermaster':g.usermaster,
                }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mc_no = request.POST.get('mcno')
            cd_no = request.POST.get('cd_no')
            tool_no = request.POST.get('tool_no')

            obj  = MG6.objects.filter(tool_no=tool_no,machine_no=mc_no,cd_no=cd_no).values('tool_no','ticket_no','tool_des','date_of_damage','machine_no','cd_no','cause_of_damage','shop_suprintendent','sec_chargeman','remarks')
            obj1 = Lc1.objects.filter(lcno=mc_no)
            
            leng = obj.count()
            leng1 = obj1.count()
            
            context={
                        'lenm' :2,
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,   
                        'len1':leng1,  
                        'obj':obj,
                        'obj1':obj1,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mc_no': mc_no,
                        'cd_no': cd_no,
                        'tool_no':tool_no,
                        'subnav':g.subnav,
                        'prtlist':prtlist,
                        'prtticket':prtticket,
                        'prtemp':prtemp,
                        'prtsec':prtsec,
                        'usermaster':g.usermaster,


                    }
            if(len(rolelist)==1):
                    for i in range(0,len(rolelist)):
                        req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
                        wo_nop =wo_nop | req
                    context = {
                        'lenm' :2,
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'obj':obj,
                        'obj1':obj1,    
                        'len':leng,
                        'len1':leng1,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mc_no': mc_no,
                        'cd_no': cd_no,
                        'tool_no':tool_no,
                        'usermaster':g.usermaster,
                        'subnav':g.subnav,
                    }
            elif(len(rolelist)>1):
                    context = {
                        'lenm' :len(rolelist),
                        'nav':g.nav,
                        'subnav':g.subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'obj':obj,
                        'obj1':obj1,
                        'len':leng,
                        'len1':leng1,
                        'shop_sec': shop_sec,
                        'mc_no': mc_no,
                        'cd_no': cd_no,
                        'tool_no':tool_no,
                        'usermaster':g.usermaster,
                    }    
        if submitvalue=='submit':
                    leng=request.POST.get('len')
                    now = datetime.datetime.now()
                    des=request.POST.get('tool_des')
                    tool_no = request.POST.get('tool_no')
                    ticket_no= request.POST.get('ticket_no')
                    date=request.POST.get('date_of_damage')
                    mc_no = request.POST.get('mc_no')
                    cd_no=request.POST.get('cd_no')
                    cause = request.POST.get('cause_of_damage')
                    shop_sup = request.POST.get('shop_sup')
                    sec = request.POST.get('sec_chargeman')
                    rem = request.POST.get('rem')

                    mg6obj = MG6.objects.filter(tool_no=tool_no,machine_no=mc_no,cd_no=cd_no).distinct()
                    if len(mg6obj) == 0:

                        MG6.objects.create(tool_no=str(tool_no),tool_des=str(des),ticket_no=str(ticket_no),date_of_damage=str(date),machine_no=str(mc_no),cd_no=str(cd_no),cause_of_damage=str(cause),last_modified=str(now),login_id=request.user,shop_suprintendent=str(shop_sup),sec_chargeman=str(sec),remarks=str(rem))

                    else:

                        MG6.objects.filter(tool_no=tool_no,machine_no=mc_no,cd_no=cd_no).update(tool_no=str(tool_no),tool_des=str(des),ticket_no=str(ticket_no),date_of_damage=str(date),machine_no=str(mc_no),cd_no=str(cd_no),cause_of_damage=str(cause),shop_suprintendent=str(shop_sup),sec_chargeman=str(sec),last_modified=str(now),remarks=str(rem))
                       
    return render(request,"MGCARD/MG6CARD/mg6views.html",context)

def mg6getmc(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(Lc1.objects.filter(shop_sec = shop_sec).values('lcno').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg6getcd(request):
    if request.method == "GET" and request.is_ajax():
        mc_no = request.GET.get('mcno')
        shop_sec = request.GET.get('shop_sec')
        cd_no = list(Oprn.objects.filter(shop_sec = shop_sec).values('part_no'))
        return JsonResponse(cd_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg6gettool(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        tool_no=list(ms_tools_master.objects.filter(shop_code=shop_sec).values('instrument_number').distinct())
        return JsonResponse(tool_no, safe = False)
    return JsonResponse({"success":False}, status=400)
