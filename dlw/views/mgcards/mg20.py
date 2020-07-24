from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/mg20view/')
def mg20view(request):
     
    rolelist=(g.usermaster).role.split(", ")
     
    wo_nop = empmast.objects.none()
    
    tm=shop_section.objects.all()
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
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=(g.usermaster).role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            current_date = date.today()
            obj = Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('name', 'desgn', 'cat', 'emp_type').distinct()
            obj1 = MG20.objects.filter(shop_sec=shop_sec, staff_no=staff_no).values('no_of_days', 'nature', 'appr_datej').distinct()
            if len(obj1)== 0:
                obj1=range(0, 1)             
                
                context = {
                    'roles':tmp,
                    'lenm' :2,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'obj': obj,
                    'obj1': obj1,
                    'date' : current_date,
                    'usermaster':g.usermaster,

                    'sub': 1,

                    'staff_no': staff_no,
                    'shop_sec': shop_sec,

                    'subnav':g.subnav
                } 

        if submitvalue=='Save':

                shop_sec= request.POST.get('shop_sec1')
                staff_no = request.POST.get('staff_no1')
                name= request.POST.get('name1')
                desgn = request.POST.get('desgn1')
                cat = request.POST.get('cat1')
                emp_type = request.POST.get('emp_type1')
                no_of_days = request.POST.get('no_of_days')
                nature = request.POST.get('nature')
                appr_datej = request.POST.get('appr_datej')
                current_date=date.today()
                obj2 = MG20.objects.filter(shop_sec=shop_sec, staff_no=staff_no, cat=cat, current_date=current_date).distinct()
                if len(obj2) == 0:
                    MG20.objects.create(current_date=str(current_date), shop_sec=str(shop_sec), staff_no=str(staff_no), cat=str(cat), name=str(name), desgn=str(desgn), emp_type=str(emp_type), nature=str(nature), no_of_days=str(no_of_days), appr_datej=str(appr_datej))
                else:
                    MG20.objects.filter(shop_sec=shop_sec, staff_no=staff_no, cat=cat).update(name=str(name), desgn=str(desgn), emp_type=str(emp_type), nature=str(nature), no_of_days=str(no_of_days), appr_datej=str(appr_datej))
                wo_no=MG20.objects.all().values('staff_no').distinct()
                messages.success(request, 'Successfully Done!, Select new values to proceed')
    return render(request, "MGCARD/MG20CARD/mg20view.html", context)



def mg20getstaff(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
        staff_no = list(staff)
        return JsonResponse(staff_no, safe=False)
    return JsonResponse({"success": False}, status=400)



