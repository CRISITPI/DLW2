from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/mg36view/')
def mg36view(request):
    import datetime

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
     
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            obj = Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name','desgn').distinct()
            obj1 = MG36.objects.filter(shop_sec=shop_sec,staff_no=staff_no).values('shop_arr','shop_dept','time_arr','time_dept','hosp_arr','hosp_dept','dept','office','date','med_officer','resumed_time','resumed_date','date_app')
            noprint=0
            leng = obj.count()
            leng1 = obj1.count()
            if len(obj1) == 0:
                noprint=1            
            context = {
                'roles':tmp,
                'obj': obj,
                'obj1': obj1,
                'len': leng,
                'len1': leng1,
                'shop_sec': shop_sec,
                'ran':range(1,2),
                'staff_no': staff_no,
                'sub' : 1,
                'noprint':noprint,
                'nav':g.nav,
                'usermaster':g.usermaster,
                'ip':get_client_ip(request),  
                'subnav':g.subnav,
            }
             
            
        if submitvalue =='Submit':
                
                leng=request.POST.get('len')
                now = datetime.datetime.now()
                shop_sec = request.POST.get('shop_sec')
                staff_no = request.POST.get('staff_no')
                shop_arr = request.POST.get('shop_arr')
                shop_dept = request.POST.get('shop_dept')
                time_arr = request.POST.get('time_arr')
                time_dept = request.POST.get('time_dept')
                hosp_arr = request.POST.get('hosp_arr')
                hosp_dept = request.POST.get('hosp_dept')
                dept = request.POST.get('dept')
                office = request.POST.get('office')
                med_officer = request.POST.get('med_officer')
                date = request.POST.get('date')
                resumed_time = request.POST.get('resumed_time')
                resumed_date = request.POST.get('resumed_date')
                date_app = request.POST.get('date_app')

                mg36obj = MG36.objects.filter(shop_sec=shop_sec,staff_no=staff_no).distinct()
                if len(mg36obj) == 0:
                    
                    MG36.objects.create(login_id=request.user,shop_sec=str(shop_sec),staff_no=str(staff_no),shop_arr=str(shop_arr),shop_dept=str(shop_dept),
                    time_arr=str(time_arr),time_dept=str(time_dept),hosp_arr=str(hosp_arr),hosp_dept=str(hosp_dept),dept=str(dept),office=str(office),med_officer=str(med_officer),
                    date=str(date),date_app=str(date_app),resumed_time=str(resumed_time),resumed_date=str(resumed_date),last_modified=str(now))

                else:
                    MG36.objects.filter(shop_sec=shop_sec,staff_no=staff_no).update(shop_arr=str(shop_arr),shop_dept=str(shop_dept),
                    time_arr=str(time_arr),time_dept=str(time_dept),hosp_arr=str(hosp_arr),hosp_dept=str(hosp_dept),dept=str(dept),office=str(office),med_officer=str(med_officer),
                    date=str(date),date_app=str(date_app),resumed_time=str(resumed_time),resumed_date=str(resumed_date),last_modified=str(now))

                staff_no=MG36.objects.all().values('staff_no').distinct()

    return render(request,"MGCARD/MG36CARD/mg36view.html",context)



def mg36getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no=list(SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

