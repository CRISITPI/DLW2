from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m21view/')
def m21view(request):
   
    wo_nop = empmast.objects.none()
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    if "Superuser" in g.rolelist:
       
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = M5SHEMP.objects.all().filter(shopsec=g.rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'staff_no':staff_no,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'subnav':g.subnav,
        }
        
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'subnav':g.subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':            
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            yymm = request.POST.get('yymm')
            obj = M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no,yymm=yymm).values('name','desgn','cat').distinct()
            obj1 =M21.objects.filter(shop_sec=shop_sec,staff_no=staff_no).values('in1','out','in2','out2','total_time','date')
          
            leng = obj.count()
            leng1 = obj1.count()           

            context = {
                        'obj': obj,
                        'obj1': obj1,
                        'len': leng,
                        'len1': leng1,
                        'shop_sec': shop_sec,
                        'ran':range(1,2),
                        'staff_no': staff_no,                        
                        'yymm': yymm,
                        'sub' : 1,
                        'nav':g.nav,
                        'roles':tmp,
                        'ip':get_client_ip(request),  
                        'subnav':g.subnav,
                        'usermaster':g.usermaster,
            }
        
        if submitvalue =='Submit': 
            inoutnum         =   request.POST.get("inoutnum")   
            in1     =   request.POST.get('in1')
            date    =   request.POST.get('date')
            out     =   request.POST.get('out')
            outdate =   request.POST.get('outdate')
            in2     =   request.POST.get('in2')
            out2    =   request.POST.get('out2')
            total_time = request.POST.get('total_time')                  
                    

            leng                    =   request.POST.get('len')               
            shop_sec                =  request.POST.get('shop_sec')
            staff_no                =  request.POST.get('staff_no')
            name                    =   request.POST.get('name')
            cat                     =   request.POST.get('cat')
            desgn                   =   request.POST.get('desgn')
            lastWeekPerHour         =   request.POST.get('lastWeekPerHour')
            lastWeekPerAmount       =   request.POST.get('lastWeekPerAmount')
            baseRatePerHour         =   request.POST.get('baseRatePerHour')
            baseRatePerHourAmount   =   request.POST.get('baseRatePerHourAmount')  
            cutTimeDay              =   request.POST.get('cutTimeDay')  
            cutTimeHours            =   request.POST.get('cutTimeHours')  
            additionalWagesDay      =   request.POST.get('additionalWagesDay')  
            additionalWagesHours    =   request.POST.get('additionalWagesHours')  
            factoryHalfDay          =   request.POST.get('factoryHalfDay')  
            factoryHalfHours        =   request.POST.get('factoryHalfHours')  
            generalOTDay            =   request.POST.get('generalOTDay')  
            generalOTHours          =   request.POST.get('generalOTHours')  
            nightAllowanceDay       =   request.POST.get('nightAllowanceDay')
            nightAllowanceHours     =   request.POST.get('nightAllowanceHours')
            halfHolidayDay          =   request.POST.get('halfHolidayDay')
            halfHolidayHours        =   request.POST.get('halfHolidayHours')
            payOffLeaveDay          =   request.POST.get('payOffLeaveDay')
            payOffLeaveHours        =   request.POST.get('payOffLeaveHours')
            unusedHolidaysDay       =   request.POST.get('unusedHolidaysDay')
            unusedHolidaysHours     =   request.POST.get('unusedHolidaysHours')
            supplementaryHolidaysDay=   request.POST.get('supplementaryHolidaysDay')
            supplementaryHolidaysHours  =   request.POST.get('supplementaryHolidaysHours')
                    
            M21DOCNEW1.objects.create(shop_sec=shop_sec,staff_no=staff_no,name=str(name),cat=str(cat),desgn=str(desgn),lastWeekPerHour=str(lastWeekPerHour),lastWeekPerAmount=str(lastWeekPerAmount),baseRatePerHour=str(baseRatePerHour),baseRatePerHourAmount=str(baseRatePerHourAmount),cutTimeDay=str(cutTimeDay), cutTimeHours=str(cutTimeHours),additionalWagesDay=str(additionalWagesDay),additionalWagesHours=str(additionalWagesHours),factoryHalfDay=str(factoryHalfDay), factoryHalfHours=str(factoryHalfHours),generalOTDay=str(generalOTDay),generalOTHours=str(generalOTHours),nightAllowanceDay=str(nightAllowanceDay), nightAllowanceHours=str(nightAllowanceHours),halfHolidayDay=str(halfHolidayDay),halfHolidayHours=str(halfHolidayHours),payOffLeaveDay=str(payOffLeaveDay),payOffLeaveHours=str(payOffLeaveHours),unusedHolidaysDay=str(unusedHolidaysDay),unusedHolidaysHours=str(unusedHolidaysHours),supplementaryHolidaysDay=str(supplementaryHolidaysDay), supplementaryHolidaysHours=str(supplementaryHolidaysHours),date=str(date), in1=str(in1),out=str(out), in2=str(in2),out2=str(out2), total_time=str(total_time), outdate = str(outdate))


            for i in range(1, int(inoutnum)+1):
                    
                    in1     =   request.POST.get('in1'+str(i))
                    date    =   request.POST.get('date'+str(i))
                    out     =   request.POST.get('outA'+str(i))
                    outdate =   request.POST.get('outdate'+str(i))
                    in2     =   request.POST.get('in2'+str(i))
                    out2    =   request.POST.get('out2'+str(i))
                    total_time = request.POST.get('total_time'+str(i)) 

                    leng                    =   request.POST.get('len')               
                    shop_sec                =  request.POST.get('shop_sec')
                    staff_no                =  request.POST.get('staff_no')
                    name                    =   request.POST.get('name')
                    cat                     =   request.POST.get('cat')
                    desgn                   =   request.POST.get('desgn')
                    lastWeekPerHour         =   request.POST.get('lastWeekPerHour')
                    lastWeekPerAmount       =   request.POST.get('lastWeekPerAmount')
                    baseRatePerHour         =   request.POST.get('baseRatePerHour')
                    baseRatePerHourAmount   =   request.POST.get('baseRatePerHourAmount')  
                    cutTimeDay              =   request.POST.get('cutTimeDay')  
                    cutTimeHours            =   request.POST.get('cutTimeHours')  
                    additionalWagesDay      =   request.POST.get('additionalWagesDay')  
                    additionalWagesHours    =   request.POST.get('additionalWagesHours')  
                    factoryHalfDay          =   request.POST.get('factoryHalfDay')  
                    factoryHalfHours        =   request.POST.get('factoryHalfHours')  
                    generalOTDay            =   request.POST.get('generalOTDay')  
                    generalOTHours          =   request.POST.get('generalOTHours')  
                    nightAllowanceDay       =   request.POST.get('nightAllowanceDay')
                    nightAllowanceHours     =   request.POST.get('nightAllowanceHours')
                    halfHolidayDay          =   request.POST.get('halfHolidayDay')
                    halfHolidayHours        =   request.POST.get('halfHolidayHours')
                    payOffLeaveDay          =   request.POST.get('payOffLeaveDay')
                    payOffLeaveHours        =   request.POST.get('payOffLeaveHours')
                    unusedHolidaysDay       =   request.POST.get('unusedHolidaysDay')
                    unusedHolidaysHours     =   request.POST.get('unusedHolidaysHours')
                    supplementaryHolidaysDay=   request.POST.get('supplementaryHolidaysDay')
                    supplementaryHolidaysHours  =   request.POST.get('supplementaryHolidaysHours')
                    
                    M21DOCNEW1.objects.create(shop_sec=shop_sec,staff_no=staff_no,name=str(name),cat=str(cat),desgn=str(desgn),lastWeekPerHour=str(lastWeekPerHour),lastWeekPerAmount=str(lastWeekPerAmount),baseRatePerHour=str(baseRatePerHour),baseRatePerHourAmount=str(baseRatePerHourAmount),cutTimeDay=str(cutTimeDay), cutTimeHours=str(cutTimeHours),additionalWagesDay=str(additionalWagesDay),additionalWagesHours=str(additionalWagesHours),factoryHalfDay=str(factoryHalfDay), factoryHalfHours=str(factoryHalfHours),generalOTDay=str(generalOTDay),generalOTHours=str(generalOTHours),nightAllowanceDay=str(nightAllowanceDay), nightAllowanceHours=str(nightAllowanceHours),halfHolidayDay=str(halfHolidayDay),halfHolidayHours=str(halfHolidayHours),payOffLeaveDay=str(payOffLeaveDay),payOffLeaveHours=str(payOffLeaveHours),unusedHolidaysDay=str(unusedHolidaysDay),unusedHolidaysHours=str(unusedHolidaysHours),supplementaryHolidaysDay=str(supplementaryHolidaysDay), supplementaryHolidaysHours=str(supplementaryHolidaysHours),date=str(date), in1=str(in1),out=str(out), in2=str(in2),out2=str(out2), total_time=str(total_time), outdate = str(outdate))
               
            messages.success(request, 'GATE ATTENDANCE CARD Successfully generated.')
    return render(request,"MCARD/M21CARD/m21view.html",context)

               
def m21getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no=list(M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m21getyymm(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no = request.GET.get('staff_no')
        yymm = list(M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('yymm').distinct())
        return JsonResponse(yymm, safe = False)
    return JsonResponse({"success":False}, status=400)



def mg21getstaff(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')

        staff = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
        staff_no = list(staff)
        return JsonResponse(staff_no, safe=False)
    return JsonResponse({"success": False}, status=400)





def mg21getreportno(request):
    if request.method == "GET" and request.is_ajax():
        reportno = request.GET.get('reportno')
        reportno=list(MG21TAB.objects.filter(reportno=reportno).values('staffNo').distinct())
        return JsonResponse(reportno, safe = False)
    return JsonResponse({"success":False}, status=400)