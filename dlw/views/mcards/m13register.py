from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/M13register/')
def M13register(request): 

    tm=shop_section.objects.all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'usermaster':g.usermaster,

    }
    
    if request.method == "POST":       
        submitvalue = request.POST.get('proceed')
        print(submitvalue)
        if submitvalue=='Proceed':
            shop = request.POST.get('shop_sec')
            month = request.POST.get('month')  
            month_temp1 = month.split("-")[0]
            month_temp2 = month.split("-")[1]
            month_final = month_temp1+'/'+month_temp2             
            obj = M13.objects.filter(shop=shop,m13_date__contains=month_final).values('m13_no','wo','m13_date','part_no','qty_tot','opn','fault_cd','reason','wo_rep','job_no','shop').distinct()
            
            if obj:   
                leng = obj.count() 
                context = { 
                        'sub':1,
                        'lenm' :2,
                        'nav':g.nav,
                        'subnav':g.subnav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'obj': obj,
                        'len': leng,
                        'shop_sec': shop,
                        'month': month_final,
                        'usermaster':g.usermaster,
                }
            else:
                    messages.error(request,"Data Not Found ! - Please select correct Shop and Month data to display data ")  
    return render(request,"MCARD/M13REGISTER/M13register.html",context)

