from dlw.views import *
import dlw.views.globals as g






def certificate(request):
    if request.method == "GET" and request.is_ajax():
        emp= request.GET.get('emp_no')
        obj=list(empmast.objects.filter(empno=emp).values('empname','desig_longdesc','ticket_no').distinct())
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success":False}, status=400)       

def certificate1(request):
    if request.method == "GET" and request.is_ajax():
        demp= request.GET.get('emp_no')
        obj=list(empmast.objects.filter(empno=demp).values('empname','desig_longdesc').distinct())
        return JsonResponse(obj,safe=False)
    
    return JsonResponse({"success":False}, status=400)

def certificate2(request):
    l=[]
    if request.method == "GET" and request.is_ajax():
        no= request.GET.get('mc_no')
        obj=list(table1_id.objects.filter(medical=no).values('empno','demp_no','bookno').distinct())
        obj1=list(table2_id.objects.filter(medicalcno=no).values('accdient','part','nature','disability').distinct())
       
        l.append(obj)
        l.append(obj1)
        return JsonResponse(l,safe=False)
    
    return JsonResponse({"success":False}, status=400)

def save_s(request):
    context={}
    if request.method == "GET" and request.is_ajax():
            eno=request.GET.get('emp_no')
            dno=request.GET.get('demp_no')
            bno=request.GET.get('book_no')
            mcno=request.GET.get('mc_no')
            pb=request.GET.get('inj_part')
            n=request.GET.get('nature')
            dc=request.GET.get('contd')
            ad=request.GET.get('acc_date')
            obj=table1_id.objects.filter(medical=mcno).distinct()
            b=obj
            if len(obj) == 0:
                table1_id.objects.create(bookno=str(bno),medical=str(mcno),empno=str(eno),demp_no=str(dno))
                table2_id.objects.create(accdient=str(ad),part=str(pb),nature=str(n),disability=dc,medicalcno=b)
            else:
                table1_id.objects.filter(medical=mcno).update(bookno=str(bno),medical=str(mcno),empno=str(eno),demp_no=str(dno))
                table2_id.objects.filter(medicalcno=mcno).update(accdient=str(ad),part=str(pb),nature=str(n),disability=dc)
                

            return JsonResponse(context,safe=False)
    return JsonResponse({"success":False}, status=400)

def GenPdf(request, *args, **kwargs):
    date1 = request.GET.get('date1')
    book_no = request.GET.get('book_no')
    mc_no = request.GET.get('mc_no')
    acc_date = request.GET.get('acc_date')
    t_no=request.GET.get('t_no')
    emp_no = request.GET.get('emp_no')
    emp_name = request.GET.get('emp_name')
    emp_des = request.GET.get('emp_des')
    demp_no = request.GET.get('demp_no')
    dname = request.GET.get('dname')
    d_des = request.GET.get('d_des')
    inj_part = request.GET.get('inj_part')
    nature = request.GET.get('nature')
    contd = request.GET.get('contd')
   
    data = {
        'date1':date1,
        'book_no':book_no,
        'mc_no':mc_no,
        'acc_date':acc_date,
        'emp_no':emp_no,
        't_no':t_no,
        'emp_name':emp_name,
        'emp_des':emp_des,
        'demp_no':demp_no,
        'dname':dname,
        'd_des':d_des,
        'inj_part':inj_part,
        'nature':nature,
        'contd':contd,
           
        }
    pdf = render_to_pdf('MISC/IDCERTIFICATE/certi.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
    

@login_required
@role_required(urlpass='/IDcertificate/')
def IDcertificate(request):
     
    wo_nop = empmast.objects.none()    
    d_id=list(empmast.objects.filter(~Q(desig_longdesc__startswith='CONTRACT'),dept_desc="MEDICAL",decode_paycategory='GAZ').values('empno').distinct())
    tmp=[]
    for on in d_id:
        tmp.append(on['empno'])
    context = {
        'sub':0,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'doctors':tmp,
        'usermaster':g.usermaster,
    }

    return render(request,"MISC/IDCERTIFICATE/IDcertificate.html",context)   


def certificate(request):
    if request.method == "GET" and request.is_ajax():
        emp= request.GET.get('emp_no')
        obj=list(empmast.objects.filter(empno=emp).values('empname','desig_longdesc','ticket_no').distinct())
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success":False}, status=400)       

def certificate1(request):
    if request.method == "GET" and request.is_ajax():
        demp= request.GET.get('emp_no')
        obj=list(empmast.objects.filter(empno=demp).values('empname','desig_longdesc').distinct())
        return JsonResponse(obj,safe=False)
    
    return JsonResponse({"success":False}, status=400)

def certificate2(request):
    l=[]
    if request.method == "GET" and request.is_ajax():
        no= request.GET.get('mc_no')
        obj=list(table1_id.objects.filter(medical=no).values('empno','demp_no','bookno').distinct())
        obj1=list(table2_id.objects.filter(medicalcno=no).values('accdient','part','nature','disability').distinct())
       
        l.append(obj)
        l.append(obj1)
        return JsonResponse(l,safe=False)
    
    return JsonResponse({"success":False}, status=400)

def save_s(request):
    context={}
    if request.method == "GET" and request.is_ajax():
            eno=request.GET.get('emp_no')
            dno=request.GET.get('demp_no')
            bno=request.GET.get('book_no')
            mcno=request.GET.get('mc_no')
            pb=request.GET.get('inj_part')
            n=request.GET.get('nature')
            dc=request.GET.get('contd')
            ad=request.GET.get('acc_date')
            obj=table1_id.objects.filter(medical=mcno).distinct()
            b=obj
            if len(obj) == 0:
                table1_id.objects.create(bookno=str(bno),medical=str(mcno),empno=str(eno),demp_no=str(dno))
                table2_id.objects.create(accdient=str(ad),part=str(pb),nature=str(n),disability=dc,medicalcno=b)
            else:
                table1_id.objects.filter(medical=mcno).update(bookno=str(bno),medical=str(mcno),empno=str(eno),demp_no=str(dno))
                table2_id.objects.filter(medicalcno=mcno).update(accdient=str(ad),part=str(pb),nature=str(n),disability=dc)
                

            return JsonResponse(context,safe=False)
    return JsonResponse({"success":False}, status=400)

def GenPdf(request, *args, **kwargs):
    date1 = request.GET.get('date1')
    book_no = request.GET.get('book_no')
    mc_no = request.GET.get('mc_no')
    acc_date = request.GET.get('acc_date')
    t_no=request.GET.get('t_no')
    emp_no = request.GET.get('emp_no')
    emp_name = request.GET.get('emp_name')
    emp_des = request.GET.get('emp_des')
    demp_no = request.GET.get('demp_no')
    dname = request.GET.get('dname')
    d_des = request.GET.get('d_des')
    inj_part = request.GET.get('inj_part')
    nature = request.GET.get('nature')
    contd = request.GET.get('contd')
   
    data = {
        'date1':date1,
        'book_no':book_no,
        'mc_no':mc_no,
        'acc_date':acc_date,
        'emp_no':emp_no,
        't_no':t_no,
        'emp_name':emp_name,
        'emp_des':emp_des,
        'demp_no':demp_no,
        'dname':dname,
        'd_des':d_des,
        'inj_part':inj_part,
        'nature':nature,
        'contd':contd,
           
        }
    pdf = render_to_pdf('MISC/IDCERTIFICATE/certi.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
        

