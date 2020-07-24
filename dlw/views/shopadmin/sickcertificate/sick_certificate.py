from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/sickcetificate/')
def sickcetificate(request):
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
        emp =empmast.objects.all() 
        ob=Med1.objects.all().count()
        rno= datetime.datetime.now().strftime ("%Y%m")+"/HOD/"+ str(ob+1)
        d_id=empmast.objects.filter(~Q(desig_longdesc__startswith='CONTRACT'),dept_desc="MEDICAL",decode_paycategory='GAZ').all()
        ex=Med1.objects.all().order_by('-recordno')
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':emp,
            'rno':rno,
            'doctor':d_id,
            'obj':ex,
            'sub':0
        }

        if request.method == "POST":
           submitvalue = request.POST.get('proceed')
           if submitvalue=='Submit':
                update = request.POST.get('update')
                recordno = request.POST.get('recordno')
                empno = request.POST.get('employeeno')
                doctorid = request.POST.get('doctorid')
                doctorname = request.POST.get('doctorname')
                doctordesignation = request.POST.get('doctordesignation')
                empname= request.POST.get('employeename')
                empdesignation = request.POST.get('empdesignation')
                empdepartment = request.POST.get('empdepartment')
                stationempno = request.POST.get('stationempno')
                suffingfrom = request.POST.get('suffingfrom')
                dutyfordays = request.POST.get('dutyfordays')
                effectdate = request.POST.get('effectdate')
                
                
                newdoc= Med1(
                    update=str(update),
                    recordno=str(recordno),
                    empno = str(empno),
                    doctorname =str(doctorname),
                    doctorid=str(doctorid),
                    doctordesignation =str(doctordesignation),
                    empname=str(empname),
                    empdesignation=str(empdesignation),
                    empdepartment = str(empdepartment),
                    stationempno=str(stationempno), 
                    suffingfrom=str(suffingfrom),
                    dutyfordays=str(dutyfordays),                 
                    effectdate= str(effectdate),                    
                     )

                newdoc.save()
                ob=Med1.objects.all().count()
                rno= datetime.datetime.now().strftime ("%Y%m")+"/HOD/"+ str(ob+1)  
                ex=Med1.objects.all().order_by('-recordno')    
                context={
                    'sub':0,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':emp,
                    'rno':rno,
                    'doctor':d_id,
                    'obj':ex,
                    'sub':1
                }
                messages.success(request, 'Successfully Done!, Select new values to proceed')   
       
    return render(request,'SHOPADMIN/SICKCERTIFICATE/sickcetificate.html',context)

def sickcetificate_edit(request):
    if request.method == "GET" and request.is_ajax():
        recno = request.GET.get('recno')
        obj = Med1.objects.filter(recordno=recno).all()        

        context={            
            'update':obj[0].update,
            'recordno':obj[0].recordno,
            'empno' :obj[0].empno,
            'doctorid':obj[0].doctorid,
            'doctorname':obj[0].doctorname,
            'doctordesignation':obj[0].doctordesignation,
            'empname':obj[0].empname,
            'empdesignation':obj[0].empdesignation,
            'empdepartment' :obj[0].empdepartment,
            'stationempno':obj[0].stationempno, 
            'suffingfrom':obj[0].suffingfrom,
            'dutyfordays':obj[0].dutyfordays,                 
            'effectdate':obj[0].effectdate,
                       
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)
