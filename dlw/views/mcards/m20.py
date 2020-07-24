from dlw.views import *
import dlw.views.globals as g


@login_required
@role_required(urlpass='/M20view/')
def M20view(request):
    import datetime 
    rolelist=(g.usermaster).role.split(", ")
    wo_nop = empmast.objects.none()
    dictemper={}
    totindb=0
    cyear = datetime.date.today().year 
    tm=shop_section.objects.all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    hd1=list(holidaylist.objects.filter(holiday_year=cyear))
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'usermaster':g.usermaster,
        'hd':hd1,
        'lvdate':"dd-mm-yyyy",          
    } 
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')

        if submitvalue=="Print pdf":
            shop_sec = request.POST.get('shop_sec')
            lvdate=request.POST.get('lv_date')  
            m2=list(M20new.objects.filter(shop_sec=shop_sec,lv_date=datetime.datetime.strptime(lvdate,"%d-%m-%Y").date()))
            data={
                'm2':m2,
                'shop_sec':shop_sec,
                'lvdate':lvdate,
                'usermaster':g.usermaster,
            }
            
            pdf = render_to_pdf('MCARD/M20CARD/M20pdf.html',data)
            return HttpResponse(pdf, content_type='application/pdf')
           

        if submitvalue=='Add':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            
            lvdate=request.POST.get('lv_date')
            
            
            m2=M20new.objects.filter(shop_sec=shop_sec,lv_date=datetime.datetime.strptime(lvdate,"%d-%m-%Y").date())
            if m2 is not None and len(m2):
                for mm in range(len(m2)):
                    temper = {str(mm):{"name":m2[mm].name,
                                               "ticketno":m2[mm].ticketno,
                                               "date":m2[mm].alt_date,
                                               "shift":m2[mm].shift,
                                               
                                               }}


                    totindb=totindb+1

                    dictemper.update(copy.deepcopy(temper))

            w1=M5SHEMP.objects.filter(shopsec=shop_sec).order_by('name').values('name').distinct() 
           
            wono=[]
            for w in range(len(w1)):
                wono.append(w1[w]['name'])
            
            alt_date="dd-mm-yy"
            
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'names':wono,
                    'dictemper':dictemper,
                    'totindb':totindb,
                    'alt_date':alt_date,
                    'usermaster':g.usermaster,
                }
            elif(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    w1 = empmast.objects.filter(shop_sec=g.rolelist[i]).values('empno').distinct()
                    req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'sub':1,
                    'subnav':g.subnav,
                    'lenm' :len(g.rolelist),
                    'wo_nop':wo_nop,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                }
            elif(len(g.rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                }
        
        if submitvalue=='Save':
            shop_sec= request.POST.get('shop_sec')
            lv_date= request.POST.get('lv_date')
            tot=0
            tot=request.POST.get('totmebs')
            totindb=request.POST.get('totindb')
            for tb in range(1,int(totindb)+1):
                namedb=request.POST.get('namedb'+str(tb))
                ticketnodb=request.POST.get('ticketnodb'+str(tb))
                datedb=request.POST.get('datedb'+str(tb))
                shift=request.POST.get('shift'+str(tb))
                M20new.objects.filter(shop_sec=str(shop_sec),staff_no=str(ticketnodb), lv_date=datetime.datetime.strptime(lv_date,"%d-%m-%Y").date()).update(alt_date=str(datedb))
                

            for t in range(1,int(tot)+1):
                name=request.POST.get('name'+str(t))
                ticketno=request.POST.get('ticket'+str(t))
                date=request.POST.get('date'+str(t))
                shift=request.POST.get('shift'+str(t))

                M20new.objects.create(shop_sec=str(shop_sec),staff_no=str(ticketno), lv_date=datetime.datetime.strptime(lv_date,"%d-%m-%Y"), name=str(name), ticketno=str(ticketno), alt_date=str(date), shift=str(shift))

                try:
                    emp_detail= emp_details.objects.filter(shopsec=shop_sec, empno=ticketno).values('email_id','mobileno')
                    sms(emp_detail[0]['mobileno'],"Sunday/Holiday ("+lv_date +" ) alloted for working.")
                    email('crisdlwproject@gmail.com', 'cris@1234', emp_detail[0]['email_id']," Sunday/Holiday ("+lv_date +" ) alloted for working.")             
                except:
                    print("sending mail and SMS problem")
            messages.success(request, 'Successfully Saved !!!, Select new values to update')
    return render(request, "MCARD/M20CARD/M20view.html", context)

def m20getstaffName(request):
    if request.method == "GET" and request.is_ajax():  
        from dlw.models import Batch     
        shop_sec = request.GET.get('shop_sec')
        staff_no = request.GET.get('staff_no')
        w1=M5SHEMP.objects.filter(staff_no=staff_no).values('staff_no','name').distinct()
        wono = list(w1)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/M20view/')
def holidaycalender(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    holiday=holidaylist.objects.all()
    if "Superuser" in rolelist:
        cyear = date.today().year
        hd1=list(holidaylist.objects.filter(holiday_year=cyear).order_by('id'))
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'holiday_list':hd1,
        }
        if request.method == "POST":
            hd=request.POST.get('h_date')
            hn=request.POST.get('h_name')
            remark=request.POST.get('remark')
            year=hd[-4:]
            ht='GH'
            holidaylist.objects.create(holiday_year=year,holiday_name=hn, holiday_date=hd, holiday_type=ht, remark=remark)
        
    return render(request, "MCARD/M20CARD/holidaycalender.html", context)
def m20reppdf(request):
    if(request.method=="POST"):            
        shop_sec = request.POST.get('shop_sec')
        lvdate = request.POST.get('lv_date')  
        m2=list(M20new.objects.filter(shop_sec__startswith=shop_sec,lv_date=lvdate).values('shop_sec','name','ticketno','alt_date','shift').order_by('shop_sec','name'))
        data={
            'm2':m2,
            'shop_sec':shop_sec,
            'lvdate':lvdate,
        }    
        pdf = render_to_pdf('MCARD/M20CARD/M20pdfc.html',data)
        return HttpResponse(pdf, content_type='application/pdf')
def m20getroster(request):
    if request.method == "GET" and request.is_ajax():  
        from.models import Batch      
        shop_sec = request.GET.get('shop_sec')
        ldate=request.GET.get('myd')
        ticket=request.GET.get('myt')
        w1=roster1.objects.filter(shop_sec=shop_sec,staffNo=ticket,date=ldate).values('shift')
        wono = w1[0]['shift']
        cont ={
            "wono":wono,
        }
        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)
def m20getstaffno(request):
    if request.method == "GET" and request.is_ajax():  
        from.models import Batch      
        shop_sec = request.GET.get('shop_sec')
        name=request.GET.get('name')
        
        w1=M5SHEMP.objects.filter(shopsec=shop_sec,name=name).values('staff_no').distinct()
        wono = w1[0]['staff_no']
        cont ={
            "wono":wono,
        }
        return JsonResponse({"cont":cont}, safe = False)

    return JsonResponse({"success":False}, status=400)


def m20rep(request):
    if request.method=="GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        sundate = request.GET.get('sundate')
        sundate= datetime.datetime.strptime(sundate,'%d-%m-%Y').date()
        myval=list(M20new.objects.filter(shop_sec__startswith=shop_sec,lv_date=sundate).values('shop_sec','name','ticketno','alt_date','shift').order_by('shop_sec','name'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)
@login_required
@role_required(urlpass='/M20view/')
def M20report(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    cyear = date.today().year
    if "Superuser" in rolelist:
        hd1=list(holidaylist.objects.filter(holiday_year=cyear))
        tm=shop_section.objects.all().distinct('shop_code')
        tmp=[]
        for on in tm:
            tmp.append(on.shop_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'hd':hd1,
            'lvdate':"dd-mm-yyyy",          
        }    
    if request.method == "POST":
            shop_sec = request.POST.get('shop_sec')
            lvdate=request.POST.get('lv_date') 
            sh_name=shop_section.objects.filter(shop_code=shop_sec).values('section_desc')
            shop_n=shop_sec[:-2]
            shop_sec = shop_sec[-2:] 
            m2=list(M20new.objects.filter(shop_sec__startswith=shop_sec,lv_date=datetime.datetime.strptime(lvdate,"%d-%m-%Y").date()).order_by('shop_sec'))
            data={
                'm2':m2,
                'shop_sec':shop_n,
                'lvdate':lvdate,
            }
            
            pdf = render_to_pdf('MCARD/M20CARD/M20pdfc.html',data)
            return HttpResponse(pdf, content_type='application/pdf')
    return render(request, "MCARD/M20CARD/M20report.html", context)


