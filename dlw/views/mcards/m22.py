from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m22view/')
def m22view(request):
     
    rolelist=(g.usermaster).role.split(", ")
     
    wo_nop = empmast.objects.none() 
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all().order_by('section_code')
         
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tm
        }
    if(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tm
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tm
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            wo_no1 = request.POST.get('wo_no1')
            staff_no = request.POST.get('staff_no')
            mon = request.POST.get('mon')
            mm=int(mon)
            month=calendar.month_name[mm]
            cy=int(date.today().year)
            cm=int(date.today().month)
            mtt = monthrange(cy, mm)[1]
            mt=int(mtt)
            obj=Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('name').distinct()
            obj1=M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).values('datelw', 'datecc', 'daterw', 'briefdd').distinct()
            datel=len(obj)
            if len(obj1) == 0:
                obj1=range(0, 1)
            obj2=M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).values('no_hrs')[:mt+1]

            obj3=[]
            if len(obj2) == 0:
                for i in range(1, mt+1):
                    obj3.append(0)
            else:
                    obj3=M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).values('no_hrs')[:mt+1]
                  
            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles': tmp,
                        'lenm': 2,
                        'nav': g.nav,
                        'ip': get_client_ip(request),
                        'mt': range(1, mt+1),
                        'mtt': range(1, mt + 1),
                        'mt1': mt,
                        'sub': 1,
                        'wo_no': wo_no,
                        'wo_no1': wo_no1,
                        'shop_sec':shop_sec,
                        'staff_no':staff_no,
                        'obj': obj,
                        'obj1': obj1,
                        'obj3':obj3,
                        'month': month,
                        'datel': datel,
                        'subnav':g.subnav
                  }
            elif(len(rolelist)==1):
                  for i in range(0,len(rolelist)):
                        
                        w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                        req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                        wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':g.usermaster,
                        'lenm' :len(rolelist),
                        'nav': g.nav,
                        'ip': get_client_ip(request),
                        'mt': range(1, mt+1),
                        'mtt': range(1, mt + 1),
                        'mt1': mt,
                        'sub': 1,
                        'wo_no': wo_no,
                        'wo_no1': wo_no1,
                        'shop_sec': shop_sec,
                        'staff_no': staff_no,
                        'obj': obj,
                        'obj1': obj1,
                        'obj3': obj3,
                        'month': month,
                        'datel': datel,
                        'subnav':g.subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'usermaster':g.usermaster,
                        'roles' :rolelist,
                        'mt': range(1, mt+1),
                        'mtt': range(1, mt + 1),
                        'mt1': mt,
                        'sub': 1,
                        'wo_no': wo_no,
                        'wo_no1': wo_no1,
                        'shop_sec': shop_sec,
                        'staff_no': staff_no,
                        'obj': obj,
                        'obj1': obj1,
                        'obj3': obj3,
                        'datel': datel,
                        'month': month,
                        'subnav':g.subnav
                  }
        if submitvalue=='Save':             
     
            obj = M22(
             update=request.POST.get('update_date'),
             letter_no=request.POST.get('letterno'),
             subject=request.POST.get('subject'),
             shop_sec=request.POST.get('shop_sec'),
             staff_no= request.POST.get('staff_no'), 
             month=request.POST.get('mon'), 
             wo_no=request.POST.get('wo_no'),
             wo_no1=request.POST.get('wo_no1'),
             datelw = request.POST.get('datelw'),
             datecc = request.POST.get('datecc'),
             daterw = request.POST.get('daterw'),
             briefdd = request.POST.get('briefdd'), 
             hd1 = request.POST.get('hd1'),
             hd2 = request.POST.get('hd2'),
             hd3 = request.POST.get('hd3'),            
             hd4 = request.POST.get('hd4'),
             hd5 = request.POST.get('hd5'),
             hd6 = request.POST.get('hd6'),
             hd7 = request.POST.get('hd7'),
             hd8 = request.POST.get('hd8'),
             hd9 = request.POST.get('hd9'),
             hd10 = request.POST.get('hd10'),
             hd11 = request.POST.get('hd11'),
             hd12 = request.POST.get('hd12'),
             hd13 = request.POST.get('hd13'),
             hd14 = request.POST.get('hd14'),
             hd15 = request.POST.get('hd15'),
             hd16 = request.POST.get('hd16'),
             hd17 = request.POST.get('hd17'),
             hd18 = request.POST.get('hd18'),
             hd19 = request.POST.get('hd19'),
             hd20 = request.POST.get('hd20'),
             hd21 = request.POST.get('hd21'),
             hd22 = request.POST.get('hd22'),
             hd23 = request.POST.get('hd23'),
             hd24 = request.POST.get('hd24'),
             hd25 = request.POST.get('hd25'),
             hd26 = request.POST.get('hd26'),
             hd27 = request.POST.get('hd27'),
             hd28 = request.POST.get('hd28'),
             hd29 = request.POST.get('hd29'),
             hd30 = request.POST.get('hd30'),
             hd31 = request.POST.get('hd31'),             
             )
            obj.save()
            
            messages.success(request, 'Successfully Updated!, Select new values to update')
    return render(request, "MCARD/M22CARD/m22view.html", context)


def m22getwono(request):
    if request.method == "GET" and request.is_ajax():
        from dlw.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1 = Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2 = Batch.objects.filter(status='R').values('bo_no').exclude(bo_no__isnull=True).order_by('bo_no').distinct('bo_no')
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m22getstaff(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no','name', 'desgn').order_by('staff_no').distinct())

        return JsonResponse({'data':staff_no}, safe = False)
    return JsonResponse({"success":False}, status=400)

def m22getdata(request):
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get('id')
        m22list = M22.objects.filter(id=id).all()
        staff_no=m22list[0].staff_no
        staff_details = list(Shemp.objects.filter(staff_no=staff_no).values('staff_no','name', 'desgn').distinct())
        
        data={
        "update":m22list[0].update,
        "letter_no":m22list[0].letter_no,
        "subject":m22list[0].subject,
        "datelw":m22list[0].datelw,
        "datecc":m22list[0].datecc,
        "daterw":m22list[0].daterw,
        "briefdd":m22list[0].briefdd,
        "no_hrs":m22list[0].no_hrs,
        "wo_no":m22list[0].wo_no,
        "wo_no1":m22list[0].wo_no1,
        "shop_sec":m22list[0].shop_sec,
        "staff_no":m22list[0].staff_no,
        "month":m22list[0].month,
        "name":staff_details[0]['name'],
        "design":staff_details[0]['desgn'],
        "hd1":m22list[0].hd1,
        "hd2":m22list[0].hd2,
        "hd3":m22list[0].hd3,
        "hd4":m22list[0].hd4,
        "hd5":m22list[0].hd5,
        "hd6":m22list[0].hd6,
        "hd7":m22list[0].hd7,
        "hd8":m22list[0].hd8,
        "hd9":m22list[0].hd9,
        "hd10":m22list[0].hd10,
        "hd11":m22list[0].hd11,
        "hd12":m22list[0].hd12,
        "hd13":m22list[0].hd13,
        "hd14":m22list[0].hd14,
        "hd15":m22list[0].hd15,
        "hd16":m22list[0].hd16,
        "hd17":m22list[0].hd17,
        "hd18":m22list[0].hd18,
        "hd19":m22list[0].hd19,
        "hd20":m22list[0].hd20,
        "hd21":m22list[0].hd21,
        "hd22":m22list[0].hd22,
        "hd23":m22list[0].hd23,
        "hd24":m22list[0].hd24,
        "hd25":m22list[0].hd25,
        "hd26":m22list[0].hd26,
        "hd27":m22list[0].hd27,
        "hd28":m22list[0].hd28,
        "hd29":m22list[0].hd29,
        "hd30":m22list[0].hd30,
        "hd31":m22list[0].hd31,
        }
        return JsonResponse({'data':data}, safe = False)
    return JsonResponse({"success":False},status=400)




@login_required
@role_required(urlpass='/m22view/')
def m22viewlist(request):     
    ex=M22.objects.all().order_by('-id')
    context={
            'totindb':0,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'subnav':g.subnav,
            'obj':ex,
        }
         
    return render(request,"MCARD/M22CARD/m22viewlist.html",context)


