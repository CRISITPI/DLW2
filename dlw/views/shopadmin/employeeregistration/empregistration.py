from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/empregist/')
def empregist(request):
    rolelist=(g.usermaster).role.split(", ")
    wo_nop = empmast.objects.none()  
    shop=shop_section.objects.all()  
    empdes= empmast.objects.all().distinct('desig_longdesc')
    empdep= empmast.objects.all().distinct('dept_desc')
    empst= empmast.objects.all().distinct('emp_status')

          
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'shop':shop,
            'empdes':empdes,
            'empdep':empdep,
            'empst':empst,
            'subnav':g.subnav,
            'usermaster':g.usermaster,
        }
    if request.method=="POST":
        Submit=request.POST.get('Submit')
        empno=request.POST.get('empno')
        empname=request.POST.get('empname')
        birthdate=request.POST.get('dobdate')
        dateapp=request.POST.get('dateapp')
        sex=request.POST.get('empsex')
        marital_status=request.POST.get('empmarital')            
        email=request.POST.get('empemail')            
        contactno=request.POST.get('empphone')
        shopno=request.POST.get('shop_sec')  
        sub_shop_sec=request.POST.get('sub_shop_sec')
        emp_inctype=request.POST.get('emptype') 
        empdesignation=request.POST.get('empdesignation') 
        emptdepartment=request.POST.get('emptdepartment') 
        empstatus=request.POST.get('empstatus') 
        office_orderno=request.POST.get('officeor') 
        if Submit=='Submit':     
           
            empmast.objects.create(empno=empno, empname=empname, birthdate=birthdate,appointmentdate=dateapp,sex=sex,marital_status=marital_status,email=email,contactno=contactno,parentshop=shopno,shopno=sub_shop_sec,emp_inctype=emp_inctype,desig_longdesc=empdesignation,emp_status=empstatus,dept_desc=emptdepartment,office_orderno=office_orderno)
            messages.success(request,'Record has successful inserted !')
        else:
            empmast.objects.filter(empno=empno).update(emp_status=empstatus,email=email,contactno=contactno,emp_inctype=emp_inctype)
            messages.error(request,'Record has successful updated ')

         
    return render(request, 'SHOPADMIN/EMPLOYEEREGISTRATION/empRegistration.html',context)

def  get_emp_det(request):
    if request.method == "GET" and request.is_ajax():
        empno = request.GET.get('empno')

        obj = empmast.objects.filter(empno=empno).all() 
        rno=len(obj)
        if rno==0:            
           context={            
            'rno':rno ,
           }  
        else:          
           context={  
            'rno':rno ,          
            'empno':obj[0].empno,
            'empname':obj[0].empname,
            'birthdate':obj[0].birthdate,
            'dateapp':obj[0].appointmentdate,
            'office_or':obj[0].office_orderno,
            'sex':obj[0].sex,
            'emp_inctype':obj[0].emp_inctype,
            'marital_status':obj[0].marital_status,
            'email':obj[0].email,
            'contactno':obj[0].contactno,
            'shopno':obj[0].shopno,
            'parentshop':obj[0].parentshop,
            'desig':obj[0].desig_longdesc,
            'status':obj[0].emp_status,
            'dept':obj[0].dept_desc,      
           }  
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)
