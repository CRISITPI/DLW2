from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/fitcertificate/')
def fitcertificate(request):
     
    wo_nop = empmast.objects.none() 
    tm=MG36.objects.all().values('shop_sec').distinct()
    tmp=[]
    for on in tm:
        tmp.append(on['shop_sec'])
    d_id=empmast.objects.filter(~Q(desig_longdesc__startswith='CONTRACT'),dept_desc="MEDICAL",decode_paycategory='GAZ').values('empno').distinct()
    tmp1=[]
    for on in d_id:
        tmp1.append(on['empno'])
    form=list(FitCertificate.objects.all().values('id').distinct().order_by('-id'))
    
    if(form==[]):
        formid=1
    else:
        formid=form[0]['id']
        formid=int(formid)+1

    context={
        'sub':0,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'doctors':tmp1,
        'subnav':g.subnav,
        'formid':formid,
        'usermaster':g.usermaster,
    } 
       
    return render(request,"MISC/FITCERTIFICATE/fitcertificate.html",context) 


def fitCertificateGetEmp(request):
    if request.method == "GET" and request.is_ajax():  
        
        shop_sec = request.GET.get('shop_sec')
        staff_no = list(MG36.objects.filter(shop_sec = shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no,safe = False)
    return JsonResponse({"success":False}, status=400)


def fitCertificateGetEmpAllDetails(request):
    if request.method == "GET" and request.is_ajax():   
        shop_sec = request.GET.get('shop_sec')
        
        staff_no = request.GET.get('staff_no')
              
        obj = empmast.objects.all().values('empno')
        
        for staff in obj:
            if staff['empno'][-5:] == staff_no:
                var = staff['empno']
                obj1 =list(empmast.objects.filter(empno=var).values('empname','desig_longdesc','dept_desc','station_des').distinct())

        return JsonResponse(obj1,safe = False)
    return JsonResponse({"success":False}, status=400)

def fitCertificateGetDoctor(request):
    if request.method == "GET" and request.is_ajax():  
        doctor_id = request.GET.get('doctor_id') 
        obj =list(empmast.objects.filter(empno=doctor_id).values('desig_longdesc','empname').distinct())
        return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status=400)

def FitcertificateGetDate(request):
    if request.method == "GET" and request.is_ajax():  
        staff_no = request.GET.get('staff_no')       
        dat=list(MG36.objects.filter(staff_no=staff_no).values('date_app').distinct())
        s=list(dat[0]['date_app'])
        date=''.join(map(str,s))
        date = date[8:10]+"-"+date[5:7]+"-"+date[0:4]
        return JsonResponse(date,safe = False)
    return JsonResponse({"success":False}, status=400)

def FitCertificatePdf(request, *args, **kwargs):
    formno = request.GET.get('formno')
    opdno = request.GET.get('opdno')
    wardno = request.GET.get('wardno')
    namep = request.GET.get('namep')
    desig = request.GET.get('desig')
    dept = request.GET.get('dept')
    station = request.GET.get('station')
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    date3 = request.GET.get('date3')
    date4 = request.GET.get('date4')
    date5 = request.GET.get('date5')
    date6 = request.GET.get('date6')
    date7 = request.GET.get('date7')
    design = request.GET.get('design')
    named = request.GET.get('named')
    data = {
        'formno':formno,
        'opdno':opdno,
        'wardno':wardno,
        'namep':namep,
        'desig':desig,
        'dept':dept,
        'station':station,
        'date1':date1,
        'date2':date2,
        'date3':date3,
        'date4': date4,
        'date5':date5,
        'date6':date6,
        'date7':date7,
        'design':design, 
        'named':named,
        }
    pdf = render_to_pdf('MISC/FITCERTIFICATE/fitcertificatereport.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def FitInfoSave(request):
    context={}
    if request.method == "GET" and request.is_ajax():
            form_no=request.GET.get('form_no')
            opd_no=request.GET.get('opd_no')
            ward_no=request.GET.get('ward_no')   
            shop_section=request.GET.get('shop_section')     
            staff_no=request.GET.get('staff_no')         
            date1=request.GET.get('date1')        
            date2=request.GET.get('date2')
            date3=request.GET.get('date3')
            date4=request.GET.get('date4')
            date5=request.GET.get('date5')
            date6=request.GET.get('date6')
            doc_id=request.GET.get('doc_id')
            doc_name=request.GET.get('doc_name')
            desg_doc=request.GET.get('desg_doc')
            date7=request.GET.get('date7')
            formno=str(form_no)+"/"+opd_no+"/"+ward_no
            cuser=request.user
            now = datetime.datetime.now()

            fitcertiobj =FitCertificate.objects.filter(form_no=formno).distinct()
            if len(fitcertiobj) == 0:
                    
                fitcertiobj=FitCertificate.objects.create(form_no=str(formno),shop_section=shop_section,staff_no=staff_no,treatement_start_date=date1,treatement_end_date=date2,
                leave_from =date3 ,leave_to=date4,fail_to_avail_from=date5,fail_to_avail_to=date6,desg_doc=desg_doc,
                date_of_fitcertificate=date7,login_id=str(cuser),doc_employee_id=doc_id,doctor_name=doc_name,last_modified=now)
            else:
                FitCertificate.objects.filter(form_no=formno).update(form_no=str(formno),shop_section=shop_section,staff_no=staff_no,treatement_start_date=date1,treatement_end_date=date2,
                leave_from =date3 ,leave_to=date4,fail_to_avail_from=date5,fail_to_avail_to=date6,desg_doc=desg_doc,
                date_of_fitcertificate=date7,login_id=str(cuser),doc_employee_id=doc_id,doctor_name=doc_name,last_modified=now)
                staff_no=FitCertificate.objects.all().values('staff_no').distinct()

            return JsonResponse(context,safe=False)
    return JsonResponse({"success":False}, status=400)

def FitDetails(request):
    if request.method == "GET" and request.is_ajax():  
        form_no = request.GET.get('formno') 
        l=[]
        obj =list(FitCertificate.objects.filter(form_no = form_no).values('treatement_start_date','treatement_end_date','staff_no','shop_section','leave_from','leave_to','fail_to_avail_from','fail_to_avail_to','doc_employee_id','doctor_name','desg_doc').distinct())
        for i in obj:
            s = i['staff_no']
        temp = empmast.objects.all().values('empno')
        for staff in temp:
            if staff['empno'][-5:] == s:
                var = staff['empno']
                obj1 =list(empmast.objects.filter(empno=var).values('empname','desig_longdesc','dept_desc','station_des').distinct())
        
        l.append(obj)
        l.append(obj1)
        return JsonResponse(l,safe = False)
    return JsonResponse({"success":False}, status=400)

       
