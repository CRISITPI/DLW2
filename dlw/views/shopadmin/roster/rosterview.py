from dlw.views import *
import dlw.views.globals as g


@login_required
@role_required(urlpass='/roster/')
def roster(request): 
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = empmast.objects.none()
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
         
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tm,
            'subnav':subnav,
        }
        d1=[]
    if request.method == "POST":
            submitvalue = request.POST.get('save')
            if submitvalue=='save':
                noofemployee=request.POST.get('hide3')
                noofdays=request.POST.get('hide2')
                for j in range(int(noofemployee)):
                    shop_sec = request.POST.get('shop_sec')
                    staffNo = request.POST.get(str('staff'+str(j+1)))
                    staffName=request.POST.get(str('staffname'+str(j+1)))
                    stafftype=request.POST.get(str('stafftype'+str(j+1)))
                    for i in range(int(noofdays)):
                        fromdate=request.POST.get('from')
                        fromdate1=fromdate[6:] + "/" + fromdate[3:5] + "/" + fromdate[:2]
                        date = datetime.datetime.strptime(fromdate1, "%Y/%m/%d")
                        modified_date = date + timedelta(days=i)
                        datee=datetime.datetime.strftime(modified_date, "%d-%m-%Y")
                        d1.append(datee)
                        shift=request.POST.get(str(j+1)+str(i))
                        roster1.objects.filter(shop_sec=shop_sec,staffNo=staffNo,date=datee).delete()
                        roster1.objects.create(shop_sec=shop_sec,staffNo=staffNo,stafftype=stafftype,staffName=staffName,shift=shift,date=datee)
                            
    return render(request, 'SHOPADMIN/ROSTER/roster.html',context)
                
def rosterempno(request):
    context={}
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')

        staff_no = list(empmast.objects.filter(shopno = shop_sec).values('empno','empname','emp_inctype').distinct())
      
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def rosterempname(request):
    if request.method == "GET" and request.is_ajax():
        
        staffNo = request.GET.get('staffNo')        
        getdetail = list(Shemp.objects.filter(staff_no = staffNo).values('name','desgn').exclude(name__isnull=True).distinct())
        return JsonResponse(getdetail, safe = False)
    return JsonResponse({"success":False}, status=400)

def rosterempdesg(request):
    if request.method == "GET" and request.is_ajax():
        staffNo = request.GET.get('staffNo')    
        staffName = request.GET.get('staffName')      
        getdetaildesgn = list(Shemp.objects.filter(staff_no = staffNo, name = staffName).values('desgn').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(getdetaildesgn, safe = False)
    return JsonResponse({"success":False}, status=400)


    
@login_required
@role_required(urlpass='/rosterreport/')
def rosterreport(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = empmast.objects.none()

    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    return render(request, 'SHOPADMIN/ROSTER/rosterreport.html',context)

def getrosterreport(request):
    if request.method=="GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        noofday=request.GET.get('leng')

        datee=request.GET.get('sdate')
        datew=datee[6:] + "-" + datee[3:5] + "-" + datee[:2]
        lst=[]
        ls=[]
        tdate = datetime.datetime.strptime(datee, "%d-%m-%Y")
        x=int(noofday)
        d1=[]

        for i in range(0,x):
            modified_date = tdate + timedelta(days=i)
            fdate=datetime.datetime.strftime(modified_date, "%d-%m-%Y")
            d1.append(fdate)
        tmpstr1=list(roster1.objects.filter(shop_sec=shop_sec,date__in=d1).values('staffNo','staffName','shift'))
        c=-1
        for j in range(len(tmpstr1)):
            a=[]
            if tmpstr1[j]['staffNo'] not in ls:
                ls.append(tmpstr1[j]['staffNo'])
                lst.append({'staffNo': tmpstr1[j]['staffNo'],'staffName':tmpstr1[j]['staffName']})
                c=c+1
                for i in range(len(tmpstr1)):
                    if tmpstr1[j]['staffNo']==tmpstr1[i]['staffNo']:
                        a.append(tmpstr1[i]['shift'])
                lst[c].update({'shift':a})
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)

def genrosterpdf(request, *args, **kwargs):

    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    shop_sec = request.GET.get('shop_sec')
    noofday=request.GET.get('hide2')
    datew=date1[6:] + "/" + date1[3:5] + "/" + date1[:2]
    lst=[]
    ls=[]
    tdate = datetime.datetime.strptime(date1, "%d-%m-%Y")
    x=int(noofday)
    d1=[]
    d2=[]
    for i in range(0,x):
        modified_date = tdate + timedelta(days=i)
        fdate=datetime.datetime.strftime(modified_date,"%d-%m-%Y")
        fdate1=datetime.datetime.strftime(modified_date,"%d-%m-%Y")
        d1.append(fdate)
        d2.append(fdate1)
    tmpstr1=list(roster1.objects.filter(shop_sec=shop_sec, date__in=d2).values('staffNo','staffName','shift'))
    c=-1
    sft=[]
    for j in range(len(tmpstr1)):
        a=[]
        if tmpstr1[j]['staffNo'] not in ls:
            ls.append(tmpstr1[j]['staffNo'])
            lst.append({'staffNo': tmpstr1[j]['staffNo'],'staffName':tmpstr1[j]['staffName']})
            c=c+1
            for i in range(len(tmpstr1)):
                if tmpstr1[j]['staffNo']==tmpstr1[i]['staffNo']:
                    a.append(tmpstr1[i]['shift'])
            sft.append(a)   
            lst[c].update({'shift':a})

    context={
        'date3':date1,
        'date4':date2,
        'shop_sec':shop_sec,
        'lst':lst,
        'd2':d2,
        'noofday':noofday,
        'sft':sft,
    }

    pdf = render_to_pdf('SHOPADMIN/ROSTER/rosterpdf.html',context)
    return HttpResponse(pdf, content_type='application/pdf')

            

            

