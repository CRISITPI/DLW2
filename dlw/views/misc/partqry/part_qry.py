from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/partqry/')
def partqry(request):
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
        'roles':tmp
    }
    return render(request,'MISC/PARTQRY/partqry.html',context)


def partqry1(request):
    if request.method == 'GET' and request.is_ajax():  
    
        part= request.GET.get('Txtpart_no')
        data_list=list(Partnew.objects.filter(gm_ptno=part).values('gm_ptno','des','part_no','it_cat','um','mb').distinct())        
        if(len(data_list)>0):
            return JsonResponse(data_list,safe = False)
        else:
            data_list=list(Partnew.objects.filter(part_no=part).values('gm_ptno','des','part_no','it_cat','um','mb').distinct())
            if(len(data_list)>0):
                return JsonResponse(data_list,safe = False)                          
    return JsonResponse({"success":False},status=400)

