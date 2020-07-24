from dlw.views import *
import dlw.views.globals as g


@login_required
@role_required(urlpass='/machineviews/')
def machineviews(request):
   
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
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mw_no = request.POST.get('mwno')
            cause=request.POST.get('cause')
            lost=request.POST.get('losthrs')
            current_yr=int(datetime.datetime.now().year)

            tmp=str(cause)+str("   ")
        
            obj = Shop.objects.filter(shop=shop_sec).values('sh_desc')[0]
            obj2  = Lc1.objects.filter(shop_sec=shop_sec,lcno=mw_no).values('des')[0]
            obj1 = MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,cause_hrs=tmp,total_losthrs__gte=lost).values('sl_no','complaint','handed_date','handed_time','comp_date','comp_time','action','total_losthrs').distinct()
            obj3 = MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no).values('sl_no','complaint','handed_date','handed_time').distinct()
            pending='pending'
            
            leng1 = obj1.count()
            leng3 = obj3.count()
           
            context={
                        'lenm' :2,
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'obj':obj,
                        'obj2':obj2,
                        'obj1':obj1,
                        'obj3':obj3,
                        'len3':leng3,
                        'len1':leng1,
                        'p':pending,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'cause':cause,
                        'cyear':current_yr,
                       
                      
                        'subnav':g.subnav,
                        'prtlist':prtlist,
                        'prtticket':prtticket,
                        'prtemp':prtemp,
                        'prtsec':prtsec,
                        'usermaster':g.usermaster,



                    }
            
    return render(request,"MISC/MACHINEBREAKDOWN/machineviews.html",context)

def machinegetcause(request):
    if request.method == "GET" and request.is_ajax():
        mwno = request.GET.get('mwno')
        wono = list(MG9Complete.objects.filter(mw_no = mwno).values('cause_hrs').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)  
