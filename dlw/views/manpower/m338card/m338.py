from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m338view/')
def m338view(request):
    import datetime
    shopsec=shop_section.objects.all().distinct()
    wo_nop = empmast.objects.none() 
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'shopsec':shopsec,
        'subnav':g.subnav,
        'usermaster':g.usermaster,
    } 
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='proceed':
            from datetime import date
            shop_sec = request.GET.get('shop_sec')
            staff_no = request.GET.get('staff_no')
            obj1 = list(empmast.objects.filter(empno = staff_no).values('empname','desig_longdesc','payrate').distinct())
            noprint=0
            context = {
                'obj1': obj1,
                'ran':range(1,32),
                'len': 31,
                'shop_sec': shop_sec,
                'noprint':noprint,
                'staff_no': staff_no,
                'sub':1,
                'nav':g.nav, 
                'ip':get_client_ip(request),  
                'subnav':g.subnav,  
                'usermaster':g.usermaster,   
            }



        submitvalue = request.POST.get('final')
        if submitvalue=='final':
             
            obj = Intershop338()
    
            obj.shop_sec        = request.POST.get('shop_sec')
            obj.staffNo          = request.POST.get('staffNo')
            obj.staffName        = request.POST.get('staffName')
            obj.staffDesg      = request.POST.get('staffDesg')
            obj.reference_authority = request.POST.get('reference_authority')
            obj.staffRate = request.POST.get('staffRate')
            obj.toshop_sec    = request.POST.get('toshop_sec')
            d = request.POST.get('date1')
            s = d.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]

            date =  year1 + "-" + month1 + "-" + day1
            obj.date1 = datetime.datetime.strptime(date, '%Y-%m-%d')

            obj.login_id = str(request.user)
            obj.status = 'f'

            td = datetime.datetime.now()
            obj.current_date = td.strftime('%Y-%m-%d')
 
            obj.save()
            
        submitvalue = request.POST.get('draft')
        if submitvalue=='Save Draft':
           
            
            obj = Intershop338()          
            obj.shop_sec        = request.POST.get('shop_sec')
            obj.staffNo          = request.POST.get('staffNo')
            obj.staffName        = request.POST.get('staffName')
            obj.staffDesg      = request.POST.get('staffDesg')
            obj.reference_authority = request.POST.get('reference_authority')
            obj.staffRate = request.POST.get('staffRate')
            obj.toshop_sec    = request.POST.get('toshop_sec')
            d = request.POST.get('date1')
            s = d.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]
            date = day1 + "-" + month1 + "-" + year1 
            
            obj.date1 = datetime.datetime.strptime(date, '%d-%m-%Y')
            obj.login_id = str(request.user)
            obj.status = 'd'

            td = datetime.datetime.now()
            obj.current_date = td.strftime('%Y-%m-%d')
 
            obj.save()
    

        submitvalue = request.POST.get('viewdraft')
       
        if submitvalue =='viewdraft':      
            
           
            context = {  
                        'obj': obj, 
                        'usermaster':g.usermaster,
            }

    return render(request,"MANPOWER/M338CARD/m338view.html",context)


def m338getdraftview(request):
    if request.method == "GET" and request.is_ajax():        
        obj = list(Intershop338.objects.filter(status = 'd').values('shop_sec', 'staffNo','staffName', 'staffDesg', 'reference_authority','staffRate', 'toshop_sec','date1').distinct())
        
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)

def m338getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no=list(empmast.objects.filter(shopno=shop_sec).values('empno').distinct())
          
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m338authority(request):
    if request.method == "GET" and request.is_ajax():
        reference_authority = request.GET.get('reference_authority')        
        return JsonResponse(reference_authority, safe = False)
    return JsonResponse({"success":False}, status=400)


def edit_status(request):
  
    if request.method == "GET" and request.is_ajax():       
        id = request.GET.get('id1')   
        shopno = request.GET.get('shopno') 
        empmast.objects.filter(empno = id).update(shopno = shopno) 
        Intershop338.objects.filter(staffNo = id).update(status = 'f')
        obj = list(Intershop338.objects.filter(status = 'd').values('shop_sec', 'staffNo','staffName', 'staffDesg', 'reference_authority','staffRate', 'toshop_sec','date1').distinct())
        
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)
def m338report(request):
    if request.method == "GET" and request.is_ajax():
        obj2 = Intershop338.objects.all()
        return JsonResponse(id, safe = False)
    return JsonResponse({"success":False}, status = 400)


def gen_report(request):
    if request.method == "GET" and request.is_ajax():
        dfrom = request.GET.get('date1')
        dto = request.GET.get('date2')

        obj = list(Intershop338.objects.filter(status = 'f',date1__gte=dfrom,date1__lte=dto).values('shop_sec', 'staffNo','staffName', 'staffDesg', 'reference_authority','staffRate', 'toshop_sec','date1').distinct())
       
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)









def m338get_details(request):
    if request.method == "GET" and request.is_ajax():
        staff_no = request.GET.get('staff_no') 
        shop_sec = request.GET.get('shop_sec')
        obj = empmast.objects.all().values('empno','empname','desig_longdesc') 
        obj1=[]  
        for staff in obj:
            
            if staff['empno'][-5:] == staff_no:
                var = staff['empno']
                obj1 = list(empmast.objects.filter(empno = var).values('empno','empname','desig_longdesc', 'payrate').distinct())
        return JsonResponse(obj1, safe = False)
    return JsonResponse({"success":False}, status=400)

