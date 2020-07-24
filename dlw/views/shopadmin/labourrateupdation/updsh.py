from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/updsh/')
def updsh(request):     
    wo_nop = empmast.objects.none()
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
     
    return render(request,'SHOPADMIN/LABOURRATEUPDATION/updsh.html',context)

def updshsave(request):
    if request.method == "GET" and request.is_ajax():
        txtshop=request.GET.get('shop_val')
        cat_value=request.GET.get('cat_value')
        lr_1=request.GET.get('lr_1')
        lr_2=request.GET.get('lr_2')
        lr_3=request.GET.get('lr_3')
        lr_4=request.GET.get('lr_4')
        up_dt=request.GET.get('up_dt')
        ls=up_dt.split('-')
        dt=ls[2]+"-"+ls[1]+"-"+ls[0]
        ovd_per=request.GET.get('ovd_per')
        if(txtshop==""):
            return JsonResponse({"success":False}, status = 400)
        shop_list=list(Shop.objects.values('shop'))
        shop_lt=[d['shop'] for d in shop_list]
        for i in range(0,len(shop_lt)):
            if shop_lt[i][0:2] == txtshop:
                Shop.objects.filter(shop=shop_lt[i]).update(cat_02=cat_value,lr1=lr_1,lr2=lr_2,lr3=lr_3,lr4=lr_4,updt_dt=dt,ovhd_perc=ovd_per)
        obj=[]
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)


def updsh1(request):
    if request.method == 'GET' and request.is_ajax():  
        shop_val= request.GET.get('Txt_shop')
        shop_list=list(Shop.objects.values('shop'))
        shop_lt=[d['shop'] for d in shop_list]
        data_list=None
        for i in range(0,len(shop_lt)):
            
            if(shop_lt[i][0:2]==shop_val):
                
                data_list=list(Shop.objects.filter(shop=shop_lt[i]).values('cat_02','lr1','lr2','lr3','lr4','updt_dt','ovhd_perc','sh_desc'))   

        if(len(data_list)>0):
            return JsonResponse(data_list,safe = False)
    return JsonResponse({"success":False}, status = 400)

