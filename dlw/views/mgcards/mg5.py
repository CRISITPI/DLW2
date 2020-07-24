
from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/mg5report/')
def mg5report(request):
    from datetime import date
    import datetime
    idcard_no = empmast.objects.none()
    obj=empmast.objects.all().values('idcard_no').distinct()
    objj=empmast.objects.filter(idcard_no=idcard_no).values('ticket_no').distinct()
    if "Superuser" in g.rolelist:
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'obj':obj,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)==1):
        for i in range(0, len(g.rolelist)):
            req = empmast.objects.all().filter(idcard_no=g.rolelist[i]).distinct()
            idcard_no =idcard_no | req

        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'idcard_no':idcard_no,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            wo_nop = empmast.objects.none()
            ti_no = request.POST.get('t_no')
            id_no = request.POST.get('id_no')
            instrument_number= request.POST.get('t_id')
            today = date.today()
            obj = MG5.objects.filter( id_no=id_no,t_no=ti_no).values('shop_sec','staff_no', 'name', 'date', 'super_in', 'optr', 'chkr', 'id_no', 't_no', 't_id', 'last_modified', 'to_no', 't_desc').distinct()
            obj1 = MG5.objects.filter(id_no=id_no,t_no=ti_no).values('optr','chkr').distinct()
            obj2 = ms_tools_master.objects.values('instrument_number','make').distinct()
            obj3=  ms_tools_master.objects.filter(instrument_number=instrument_number).values('make').distinct()
            if len(obj1)== 0:
                obj1=range(0, 1)
            if "Superuser" in g.rolelist:
                  
                  context = {
                         
                        'lenm' :2,
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'date':today,
                        'ticket_no': ti_no,
                        'id_no': id_no,
                        'subnav':g.subnav,
                         'usermaster':g.usermaster,

                  }
            elif(len(g.rolelist)==1):
                  for i in range(0, len(g.rolelist)):
                      req = empmast.objects.all().filter(idcard_no=rolelist[i]).distinct()
                      idcard_no =idcard_no | req
                      
                  context = {
                        'roles' :g.rolelist,
                        'usermaster':g.usermaster,
                        'lenm' :len(g.rolelist),
                        'nav': g.nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj3': obj3,
                        'sub': 1,
                        'idcard_no': idcard_no,
                        'subnav':g.subnav,
                        'date':today, 
                        'ticket_no': ti_no,
                        'obj2': obj2,
                  }
            elif(len(g.rolelist)>1):
                  context = {
                        'lenm' :len(g.rolelist),
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'usermaster':g.usermaster,
                        'roles' :g.rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'ticket_no': ti_no,
                        'id_no': id_no,
                        'subnav':g.subnav,
                        'date':today, 

                  }
        if submitvalue=='Save':
                shopno= request.POST.get('shop_no')
                empno = request.POST.get('staff_no')
                emp_name= request.POST.get('name')
                super_in = request.POST.get('emptype')
                id_no=request.POST.get('id_no')
                ticket_no=request.POST.get('t_no')
                t_id=request.POST.get('t_id')
                
                date=request.POST.get('date')
                t_desc=request.POST.get('make1')
                optr=request.POST.get('optr')
                chkr=request.POST.get('chkr')
                now = datetime.datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                tot = request.POST.get('totaltools')
                
                MG5.objects.create(id_no=str(id_no),t_id=str(t_id),t_desc=str(t_desc), t_no=str(ticket_no), shop_sec=str(shopno), staff_no=str(empno), name=str(emp_name), super_in=str(super_in), date=str(date), optr=str(optr), chkr=str(chkr), last_modified=str(dt_string) )
                
                messages.success(request, 'Successfully Done!, Select new values to proceed')

        if submitvalue=='Generate report':
            return mg5report(request)
            
    return render(request, "MGCARD/MG5CARD/mg5report.html", context)




@login_required
@role_required(urlpass='/mg5view/')
def mg5view(request):
    from datetime import date
    import datetime
    idcard_no = empmast.objects.none()
    obj=empmast.objects.all().values('idcard_no').distinct()
    objj=empmast.objects.filter(idcard_no=idcard_no).values('ticket_no').distinct()
    if "Superuser" in g.rolelist:
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'obj':obj,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)==1):
        for i in range(0, len(g.rolelist)):
            req = empmast.objects.all().filter(idcard_no=g.rolelist[i]).distinct()
            idcard_no =idcard_no | req

        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'idcard_no':idcard_no,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            wo_nop = empmast.objects.none()
            ti_no = request.POST.get('t_no')
            id_no = request.POST.get('id_no')
            instrument_number= request.POST.get('t_id')
            today = date.today()
            obj = empmast.objects.filter( idcard_no=id_no,ticket_no=ti_no).values('empname','emptype','shopno','empno').distinct()
            obj1 = MG5.objects.filter(id_no=id_no,t_no=ti_no).values('optr','chkr').distinct()
            obj2 = ms_tools_master.objects.values('instrument_number','make').distinct()
            obj3=ms_tools_master.objects.filter(instrument_number=instrument_number).values('make').distinct()
            if len(obj1)== 0:
                obj1=range(0, 1)
            if "Superuser" in g.rolelist:
                  
                  context = {
                         
                        'lenm' :2,
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'date':today,
                        'ticket_no': ti_no,
                        'id_no': id_no,
                        'subnav':g.subnav,
                        'usermaster':g.usermaster,
                  }
            elif(len(g.rolelist)==1):
                  for i in range(0, len(g.rolelist)):
                      req = empmast.objects.all().filter(idcard_no=g.rolelist[i]).distinct()
                      idcard_no =idcard_no | req
                      
                  context = {
                        'roles' :g.rolelist,
                        'usermaster':g.usermaster,
                        'lenm' :len(g.rolelist),
                        'nav': g.nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj3': obj3,
                        'sub': 1,
                        'idcard_no': idcard_no,
                        'subnav':g.subnav,
                        'date':today, 
                        'ticket_no': ti_no,
                        'obj2': obj2,
                  }
            elif(len(g.rolelist)>1):
                  context = {
                        'lenm' :len(g.rolelist),
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'usermaster':g.usermaster,
                        'roles' :g.rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'ticket_no': ti_no,
                        'id_no': id_no,
                        'subnav':g.subnav,
                        'date':today, 

                  }
        if submitvalue=='Save':
                shopno= request.POST.get('shop_no')
                empno = request.POST.get('staff_no')
                emp_name= request.POST.get('name')
                super_in = request.POST.get('emptype')
                id_no=request.POST.get('id_no')
                ticket_no=request.POST.get('t_no')
                t_id=request.POST.get('t_id')
                date=request.POST.get('date')
                t_desc=request.POST.get('make1')
                optr=request.POST.get('optr')
                chkr=request.POST.get('chkr')
                now = datetime.datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                MG5.objects.create(id_no=str(id_no),t_id=str(t_id),t_desc=str(t_desc), t_no=str(ticket_no), shop_sec=str(shopno), staff_no=str(empno), name=str(emp_name), super_in=str(super_in), date=str(date), optr=str(optr), chkr=str(chkr), last_modified=str(dt_string) )
                messages.success(request, 'Successfully Done!, Select new values to proceed')

        if submitvalue=='Generate report':
            return mg5report(request)
            
    return render(request, "MGCARD/MG5CARD/mg5view.html", context)


def mg5getticket(request):
    if request.method == "GET" and request.is_ajax():

        idcard_no = request.GET.get('id_no')

        ticket = empmast.objects.filter(idcard_no=idcard_no).values('ticket_no').exclude(ticket_no__isnull=True).distinct()
        ticket_no = list(ticket)
        return JsonResponse(ticket_no, safe=False)
    return JsonResponse({"success": False}, status=400)

def mg5gettooldesc(request):
    if request.method == "GET" and request.is_ajax():

        make = request.GET.get('make')

        tool_desc = list(ms_tools_master.objects.filter(instrument_number=make).values('make'))
        return JsonResponse(tool_desc, safe=False)
    return JsonResponse({"success": False}, status=400)
