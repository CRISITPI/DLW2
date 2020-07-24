from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/mg15view/')
def mg15view(request): 
    wo_nop = empmast.objects.none() 
    rolelist=(g.usermaster).role.split(", ")
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
        'roles':tmp
    }
    if(len(rolelist)==1):
        for i in range(0, len(rolelist)):
            req = Shemp.objects.all().filter(shopsec=rolelist[i]).values('staff_no').exclude(staff_no__isnull=True).distinct()
            wo_nop =wo_nop | req



        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=(g.usermaster).role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            date = request.POST.get('date')
            obj = Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('name', 'desgn', 'cat', 'emp_type').distinct()
            obj1 = MG15.objects.filter(shop_sec=shop_sec, staff_no=staff_no, date=date).values('remarks', 'h1a', 'h2a', 'causeofab', 'ticket_no').distinct()
            tt = Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('ticket_no').distinct()
            if len(obj1)== 0:
                obj1=range(0, 1)
            if "Superuser" in rolelist:
                  
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'tt': tt,
                        'usermaster':g.usermaster,
                        'date' : date,


                        'sub': 1,

                        'staff_no': staff_no,
                        'shop_sec': shop_sec,

                        'subnav':g.subnav
                  }
            elif(len(rolelist)==1):
                  for i in range(0, len(rolelist)):
                      req = Shemp.objects.all().filter(shopsec=rolelist[i]).values('staff_no').exclude(staff_no__isnull=True).distinct()
                      wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':g.usermaster,
                        'lenm' :len(rolelist),
                        'nav': g.nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'tt': tt,

                        'sub': 1,
                        'date': date,

                        'staff_no': staff_no,
                        'shop_sec': shop_sec,

                        'subnav': g.subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'usermaster':g.usermaster,
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'tt': tt,

                        'date': date,
                        'sub': 1,

                        'staff_no': staff_no,
                        'shop_sec': shop_sec,

                        'subnav':g.subnav
                  }

        if submitvalue=='Save':

                shop_sec= request.POST.get('shop_sec1')
                staff_no = request.POST.get('staff_no1')
                date = request.POST.get('date1')
                name= request.POST.get('name1')
                desgn = request.POST.get('desgn1')
                emp_type = request.POST.get('emp_type1')
                cat = request.POST.get('cat1')
                ticket_no = request.POST.get('ticket_no')
                h1a = request.POST.get('h1a')
                h2a = request.POST.get('h2a')
                remarks = request.POST.get('remarks')
                causeofab = request.POST.get('causeofab')

                obj2 = MG15.objects.filter(shop_sec=shop_sec, staff_no=staff_no, date=date, ).distinct()
                if len(obj2) == 0:
                    MG15.objects.create(date=str(date), shop_sec=str(shop_sec), staff_no=str(staff_no), cat=str(cat), name=str(name), desgn=str(desgn), emp_type=str(emp_type), remarks=str(remarks), causeofab=str(causeofab), ticket_no=str(ticket_no), h1a=str(h1a), h2a=str(h2a))
                else:
                    MG15.objects.filter(shop_sec=shop_sec, staff_no=staff_no, date=date).update(cat=str(cat), ticket_no=str(ticket_no), name=str(name), desgn=str(desgn), emp_type=str(emp_type), remarks=str(remarks), causeofab=str(causeofab), h1a=str(h1a), h2a=str(h2a))
                wo_no=MG15.objects.all().values('staff_no').distinct()
                messages.success(request, 'Successfully Done!, Select new values to proceed')
    return render(request, "MGCARD/MG15CARD/mg15view.html", context)

def mg15getstaff(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
        staff_no = list(staff)
        return JsonResponse(staff_no, safe=False)
    return JsonResponse({"success": False}, status=400)
 
