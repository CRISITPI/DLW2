from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m26view/')
def m26view(request):
     
    wo_nop = empmast.objects.none()     
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
        'user':g.usermaster,
        'subnav':g.subnav,
    }
    return render(request,'MCARD/M26CARD/m26view.html',context)



def m26getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(M5DOCnew.objects.all().filter(shop_sec=shop_sec).values('batch_no').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m26getStaffCatWorkHrs(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        w_no     = request.GET.get('wno')
        date     = request.GET.get('date')
        up_dt=[]       
        update_date = M5SHEMP.objects.filter(shopsec=shop_sec, date__isnull=False, updt_date__isnull=False).values('updt_date').order_by('-updt_date')
        for i in update_date:
            up_dt.append(i['updt_date'])    
        if shop_sec and w_no and date:  
            wono = list(M5SHEMP.objects.filter(shopsec=shop_sec,date__contains=date, updt_date__contains=up_dt[0], staff_no__isnull=False, total_time_taken__isnull=False,date__isnull=False).values('staff_no','cat','total_time_taken').distinct())            
            emp_detail= emp_details.objects.filter(card_details='M26').values('email_id','mobileno')   
            mob_temp=[]            
            for i in emp_detail: 
                mob_temp.append(i['mobileno'])
            for j in range(len(mob_temp)):
                smsM18(mob_temp[j],"Dear Employee TimeSheet of indirect labour(M26) card has been generated.")     
        else:
            wono = "NO"
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)
