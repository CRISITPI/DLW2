from dlw.views import *
import dlw.views.globals as g


@login_required
@role_required(urlpass='/staff_auth_report_view/')
def staff_auth_report_view(request):
   
    tm1=empmast.objects.all().filter(payrate__gt='4200').values('empno').distinct()

   
    staff_no = empmast.objects.none()
    tm=Shemp.objects.all().values('shopsec').distinct()
    sh=Shemp.objects.all().values('staff_no','name').distinct()
    formno=staff_auth.objects.all().values('form_id').distinct().order_by('form_id')
    tmp=[]
    for on in tm:
        tmp.append(on['shopsec'])
    context={
        'sh':sh,
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'usermaster':g.usermaster,
        'tm1':tm1,
        'formno':formno,
        'subnav':g.subnav,
    }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = Shemp.objects.all().filter(shop_sec=g.rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'staff_no':staff_no,
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
        submitvalue = request.POST.get('proceed')
        if(submitvalue=='Proceed'):
            shop_sec = request.POST.get('shop_sec')
            formno = request.POST.get('formno1')
            shop_name = Shop.objects.filter(shop=shop_sec).values('sh_desc').distinct()
            wono =(shop_name[0].get('sh_desc')).strip()
            alldata=staff_auth.objects.filter(form_id=formno,shopsec=shop_sec).values('srno','shopsec','staff_no','staff_name','auth','mwno','empno_shop_mang','date_shop_mang','empno_sse','date_sse').distinct().order_by('form_id')
            auth=alldata[0]['auth']
            empnomanager=alldata[0]['empno_shop_mang']
            datemanager=alldata[0]['date_shop_mang']
            sse=alldata[0]['empno_sse']
            datesse=alldata[0]['date_sse']

            mana =empmast.objects.filter(empno=empnomanager).values('empname').distinct()[0]
            ss =empmast.objects.filter(empno=sse).values('empname').distinct()[0]
            
            context = {
                'alldata':alldata,
                'auth':auth,
                'nav':g.nav,
                'subnav':g.subnav,
                'ip':get_client_ip(request),
                'roles' :g.rolelist,
                'wono':wono,
                'manager':mana,
                'datemanager':datemanager,
                'usermaster':g.usermaster,
                'sse':ss,
                'datesse':datesse,
                'form':formno,
            }
                        
            
    return render(request,"MISC/STAFFAUTH/staff_auth_report_view.html",context) 

@login_required
@role_required(urlpass='/staff_auth_view/')
def staff_auth_view(request):
   
    tm1=empmast.objects.all().filter(payrate__gt='4200').values('empno').distinct() 
    staff_no = empmast.objects.none()
    tm=Shemp.objects.all().values('shopsec').distinct()
    sh=Shemp.objects.all().values('staff_no','name').distinct()
    
    tmp=[]
    for on in tm:
        tmp.append(on['shopsec'])
        
    context={
            'sh':sh,
            'sub':0,
            'lenm' :2,
            'usermaster':g.usermaster,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'tm1':tm1,
            'subnav':g.subnav,
        }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = Shemp.objects.all().filter(shop_sec=g.rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(rolelist),
            'staff_no':staff_no,
            'nav':g.nav,
            'usermaster':g.usermaster,
            'ip':get_client_ip(request),
            'roles' :tmp
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
        submitvalue = request.POST.get('proceed')

        if submitvalue=='submit':
            shop_sec = request.POST.get('shop_sec')
            totauth = request.POST.get('totauth')
            totstaff = request.POST.get('totstaff')
            empno_shop_mang = request.POST.get('empno_shop_mang')
            empno_sse = request.POST.get('empno_sse')
            date_shop_mang = request.POST.get('date_shop_mang')
            date_sse = request.POST.get('date_sse')
            now = datetime.datetime.now()
            user=request.user
            form=staff_auth.objects.all().values('form_id').distinct().order_by('-form_id')
            if(form.count()==0):
                formid=1
            else:
                formid=form[0]['form_id']
                formid=int(formid)+1
            j=0
            auth=""
            for i in range(0,int(totauth)+1):
                auth1 = request.POST.get('auth'+str(i))
                if(auth1!=None):
                    auth=auth1+", "
                    j=i
                    break
                   
                
            for i in range(j+1,int(totauth)+1):
                auth1 = request.POST.get('auth'+str(i))
                auth=auth+auth1+", "
            auth=auth[:len(auth)-2]
            k=0
            no=0
            for i in range(0,int(totstaff)+1):
                staff_no = request.POST.get('staff_no'+str(i))
                staff_name = request.POST.get('staff_name'+str(i))
                staff_sec = request.POST.get('staff_sec'+str(i))
                mwnoj=""
                for j in range(1,3):
                    mwnoj1 = request.POST.get('mwno'+str(i)+str(j))
                    if mwnoj1 !=None:
                        mwnoj=mwnoj1+", "
                        k=j
                        break
                for j in range(k+1,10):
                    mwnoj1 = request.POST.get('mwno'+str(i)+str(j))
                    if mwnoj1!=None:
                        mwnoj=str(mwnoj)+str(mwnoj1)+", "
                mwnoj=mwnoj[:len(mwnoj)-2]
                if(staff_no!=None):
                    no=no+1
                    staff_auth.objects.create(form_id=str(formid), srno=str(no), shopsec=str(shop_sec),staff_no=str(staff_no),staff_name=str(staff_name), auth=str(auth), mwno=str(mwnoj), empno_shop_mang=str(empno_shop_mang), date_shop_mang=str(date_shop_mang), empno_sse=str(empno_sse), date_sse=str(date_sse), psnt_date=str(now)     ,login_id=str(user), last_modified=str(now))
                
    return render(request,"MISC/STAFFAUTH/staff_auth_view.html",context)  

  
def staff_auth_viewgetshop_name(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        shop_name = Shop.objects.filter(shop=shop_sec).values('sh_desc').distinct()
        wono =(shop_name[0].get('sh_desc')).strip()

        mnno=list(Mnp.objects.filter(location=wono).values('mwno').distinct())
        cont ={
            "wono":wono,
            "mno":mnno,
        }
        
        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)
def staff_auth_viewgetstaff_name(request):
    if request.method == "GET" and request.is_ajax():
        staff_no = request.GET.get('staff_no')
        name = list(Shemp.objects.filter(staff_no=staff_no).values('name').distinct())
        wono = name[0]['name']
        cont ={
            "wono":wono,
        }

        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)

def staff_auth_viewgetemp_name(request):
    if request.method == "GET" and request.is_ajax():
        emp_no = request.GET.get('emp_no')
        
        name = list(empmast.objects.filter(empno=emp_no).values('empname','desig_longdesc').distinct())
        wono1 = name[0]['empname']
        wono2= name[0]['desig_longdesc']
        cont ={
            "wono1":wono1,
            "wono2":wono2,
        }

        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)


      
