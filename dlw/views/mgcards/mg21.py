from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/mg21report/')
def mg21report(request): 
    a=0 
    wo_nop = empmast.objects.none()     
    obj = list(MG21TAB.objects.values('reportno').distinct())
    context={
        'a':a,
        'sub':0,
        'lenm' :2,
        'obj': obj,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'usermaster':g.usermaster,
    }
    
    if request.method == "POST":
        
        submitvalue = request.POST.get('Proceed')
        if submitvalue=='Proceed':
            a=1
            shop_sec = request.POST.get('shop_sec')
            staffNo = request.POST.get('staffNo')
            staffName = request.POST.get('staffName')
            staffDesg = request.POST.get('staffDesg')
            reportdate = request.POST.get('reportdate')
            resumedate = request.POST.get('resumedate')
            sse = request.POST.get('sse')
            reportNumber = request.POST.get('reportNumber')
            login_id = request.POST.get('login_id')
            current_date = request.POST.get('current_date')
           
            obj = list(MG21TAB.objects.filter(reportno=reportNumber).values('reportno','shop_sec','staffNo','staffName','staffDesg','reportdate','resumedate','sse','current_date').distinct())
            
            context = {                        
                'a':a,
                'obj': obj,
                'shop_sec': shop_sec,
                'staffNo' :staffNo,
                'staffName' : staffName,
                'staffDesg':staffDesg,
                'reportNumber':reportNumber,
                'resumedate':resumedate,
                'reportdate':reportdate,
                'sse':sse,
                'login_id':login_id,
                'current_date' : current_date,
                'subnav':g.subnav,
                'usermaster':g.usermaster,
            }                       
    return render(request,"MGCARD/MG21CARD/mg21report.html",context)

@login_required
@role_required(urlpass='/mg21views/')
def mg21views(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    tmp=shop_section.objects.filter(shop_id=usermaster.shopno).all()       
    wo_nop = empmast.objects.none()
    if "Superuser" in g.rolelist:
        
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=g.rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
            
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'usermaster':g.usermaster,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('save')
        if submitvalue=='proceed':
            shop_sec = request.GET.get('shop_sec')
            staff_no = request.GET.get('staff_no')
            obj1 = list(empmast.objects.filter(empno = staff_no).values('empname','desig_longdesc','payrate').distinct())
            noprint=0
            context = {
                'obj1': obj1,
                'ran':range(1,32),
                'len': 31,
                'shop_sec': shop_sec,
                'noprint':noprint,
                'staff_no': staff_no,
                'sub':1,
                'nav':g.nav,
                'ip':get_client_ip(request),  
                'subnav':g.subnav,   
                'usermaster':g.usermaster,  
            }


        submitvalue = request.POST.get('SAVE')
        if submitvalue=='SAVE':
             
            obj = MG21TAB()
    
            obj.shop_sec        = request.POST.get('shop_sec')
            obj.staffNo          = request.POST.get('staffNo')
            obj.staffName        = request.POST.get('staffName')
            obj.staffDesg      = request.POST.get('staffDesg')
            obj.reportno      = request.POST.get('sse1')
            obj.reportdate = request.POST.get('date1')
            obj.resumedate = request.POST.get('date2')
            obj.sse    = request.POST.get('sse')
            obj.login_id            = str(request.user)
            obj.current_date     = datetime.datetime.now().strftime("%d-%m-%Y")
            obj.save()

            context = {
                        'obj': obj,
                        'subnav':g.subnav,
            }

    return render(request,"MGCARD/MG21CARD/mg21views.html",context)