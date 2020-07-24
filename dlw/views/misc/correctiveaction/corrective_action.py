from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/correctiveaction/')
def correctiveaction(request):
     
    wo_nop = empmast.objects.none()
    temp=list(Code.objects.filter(cd_type='11').values('alpha_1').distinct())
    tmp1=[]
    for on in temp:
            tmp1.append(on['alpha_1'])   
    
    form=list(CorrectiveAction.objects.all().values('id').distinct().order_by('-id')) 
    if form==[]:
        sno=1
    else:
        sno=form[0]['id']
        sno=int(sno)+1  
     
    context={
        'nav' : g.nav,
        'ip' : get_client_ip(request),
        'subnav' : g.subnav,
        'engtype' : tmp1,
        'sno' :sno,
        'usermaster':g.usermaster
    }
    if request.method == "POST": 
        submitvalue = request.POST.get('Report')
        past_failure_details=[]
        if submitvalue=='Report':
            sno = request.POST.get('sno')
            obj=list(CorrectiveAction.objects.filter(sno=sno).values('sno','date','pl_no','engine_loco_type','supplier_name',
            'rejection_percentage','past_failure_details','reporting_agency_name','failure_since_last_six_months',
            'probable_cause_redemy','employee_id','ca_regis_no','date_by_mroffice','follow_up','mr_office_decision').distinct())
            v=''
            if len(obj)!=0:
                v=obj[0]['employee_id']
            obj1=[]
            
            if v != "":   
                obj1=list(empmast.objects.filter(empno=v).values('empname','desig_longdesc').distinct())
            data={
                'obj':obj,
                'obj1' : obj1,
            }
            pdf = render_to_pdf('MISC/CORRECTIVEACTION/correctiveactionreport.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
                
    return render(request, "MISC/CORRECTIVEACTION/correctiveaction.html",context) 


def CorrectionActionSave(request):
    if request.method == "GET" and request.is_ajax():
        obj=[]
        sno=request.GET.get('sno')
        date=request.GET.get('date')
        plno=request.GET.get('plno')
        engine=request.GET.get('engine')
        suppliername=request.GET.get('suppliername')
        perrejection=request.GET.get('perrejection')
        pastfailure=request.GET.get('pastfailure')
        reportagencyname=request.GET.get('reportagencyname')
        failure=request.GET.get('failure')
        cause=request.GET.get('cause')
        employee=request.GET.get('employee')
        caregisno=request.GET.get('caregisno')
        date2=request.GET.get('date2')
        followup=request.GET.get('followup')
        decision_mr=request.GET.get('decision_mr')
        cuser=request.user
        now = datetime.datetime.now()
        temp=CorrectiveAction.objects.filter(sno=sno).values('sno').distinct()
        if len(temp) == 0:
            temp=CorrectiveAction.objects.create(sno=str(sno),date=str(date),pl_no=str(plno),engine_loco_type=str(engine),
            supplier_name=str(suppliername),rejection_percentage=str(perrejection),past_failure_details=str(pastfailure),
            reporting_agency_name=str(reportagencyname),failure_since_last_six_months=str(failure),
            probable_cause_redemy=str(cause),employee_id=str(employee),ca_regis_no=str(caregisno),date_by_mroffice=str(date2),
            follow_up=str(followup),mr_office_decision=str(decision_mr),login_id=str(cuser),last_modified=now)
        
        else:
            obj=[1]
        return JsonResponse(obj,safe=False) 
    return JsonResponse({"success:False"},status=400) 

def CorrectiveActionValidatePlno(request):
    if request.method == "GET" and request.is_ajax():
        plno = request.GET.get('plno')
        obj=list(Part.objects.filter(partno=plno).values('partno').distinct())
        if len(obj)==0:
            i=[]
            return JsonResponse(i,safe=False)
        else:
            return JsonResponse(obj,safe=False)
    return JsonResponse({"success:False"},status=400)

def CorrectiveActionValidateEid(request):
    if request.method == "GET" and request.is_ajax():
        employee = request.GET.get('employee')
        obj=list(empmast.objects.filter(empno=employee).values('empname','desig_longdesc').distinct())
        if len(obj)==0:
            i=[]
            return JsonResponse(i,safe=False)
        else:
            return JsonResponse(obj,safe=False)
    return JsonResponse({"success:False"},status=400)

def CorrectiveActionGetAllDetails(request):
    if request.method == "GET" and request.is_ajax():
        sno = request.GET.get('sno')
        i=[]
        obj=list(CorrectiveAction.objects.filter(sno=sno).values('date','pl_no','engine_loco_type','supplier_name',
        'rejection_percentage','past_failure_details','reporting_agency_name','failure_since_last_six_months',
        'probable_cause_redemy','employee_id','ca_regis_no','date_by_mroffice','follow_up','mr_office_decision').distinct())
        v=''
        if len(obj)!=0:
            v=obj[0]['employee_id']
                
        obj1=[]
          
        if v != "":      
            obj1=list(empmast.objects.filter(empno=v).values('empname','desig_longdesc').distinct())
        i.append(obj)
        i.append(obj1)
        return JsonResponse(i,safe=False)
    return JsonResponse({"success:False"},status=400)

def CorrectionActionUpdate(request):
    if request.method == "GET" and request.is_ajax():
        obj=[]
        sno=request.GET.get('sno')
        date=request.GET.get('date')
        plno=request.GET.get('plno')
        engine=request.GET.get('engine')
        suppliername=request.GET.get('suppliername')
        perrejection=request.GET.get('perrejection')
        pastfailure=request.GET.get('pastfailure')
        reportagencyname=request.GET.get('reportagencyname')
        failure=request.GET.get('failure')
        cause=request.GET.get('cause')
        employee=request.GET.get('employee')
        caregisno=request.GET.get('caregisno')
        date2=request.GET.get('date2')
        followup=request.GET.get('followup')
        decision_mr=request.GET.get('decision_mr')
        cuser=request.user
        now = datetime.datetime.now()
        CorrectiveAction.objects.filter(sno=str(sno)).update(sno=str(sno),date=str(date),pl_no=str(plno),engine_loco_type=str(engine),
        supplier_name=str(suppliername),rejection_percentage=str(perrejection),past_failure_details=str(pastfailure),
        reporting_agency_name=str(reportagencyname),failure_since_last_six_months=str(failure),
        probable_cause_redemy=str(cause),employee_id=str(employee),ca_regis_no=str(caregisno),date_by_mroffice=str(date2),
        follow_up=str(followup),mr_office_decision=str(decision_mr),login_id=str(cuser),last_modified=now)

        return JsonResponse(obj,safe=False)
    return JsonResponse({"success:False"},status=400)





     

   
