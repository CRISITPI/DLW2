from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/partmaster/')
def partmaster(request):
    obj=list(Part.objects.values('ptc').distinct())
    tmp=[]
    for on in obj:
        tmp.append(on['ptc'])
    context={
        'role':tmp,
        'nav':g.nav,
        'subnav':g.subnav,
        'usermaster':g.usermaster,
    }    
    if request.method =="POST":
        submitvalue = request.POST.get('submit')
        if submitvalue =='Save/Update':
            part_no=request.POST.get('partno_id')
            descr_id=request.POST.get('descr_id')
            drng_no_id=request.POST.get('drng_no_id')
            shop_unit_id=request.POST.get('shop_unit_id')
            lbl=request.POST.get('lbl')
            ptc_id=request.POST.get('ptc_id')
            m14split_code_id=request.POST.get('m14split_code_id')
            allowance_id=request.POST.get('allowance_id')
            obj=Part.objects.filter(partno=part_no).distinct()
            if len(obj) == 0:
                Part.objects.create(partno=str(part_no),des=str(descr_id),drgno=str(drng_no_id),shop_ut=str(shop_unit_id),ptc=str(ptc_id),m14splt_cd=str(m14split_code_id),allow_perc=int(allowance_id))
            else:
               Part.objects.filter(partno=part_no).update(des=str(descr_id),drgno=str(drng_no_id),shop_ut=str(shop_unit_id),ptc=str(ptc_id),m14splt_cd=str(m14split_code_id),allow_perc=int(allowance_id))
    return render(request,"MISC/PARTMASTER/partmaster.html",context)


def part_get(request):
    if request.method == "GET" and request.is_ajax():
        no= request.GET.get('partno_id')
        majg =no[0:2]
        subg1=no[2:4] 
        subg2=no[4:6] 
        sl_no=no[6:7] 
        lst=[majg,subg1,subg2,sl_no]
        part=''.join(map(str,lst))
        
        lst=[]
        for i in range(0,len(part)):
            lst.insert(i,int(part[i]))
        sum=0 
        cal=8
        for i in range(0,7):
            sum=sum + (lst[i] * cal)
            cal= cal - 1
        mod = sum % 11
        lst.insert(len(lst),mod) 
        part=''.join(map(str,lst)) 
        obj=list(Part.objects.filter(partno=no).values('des','drgno','shop_ut','ptc','m14splt_cd','allow_perc').distinct())
        obj.append(mod)
        return JsonResponse(obj,safe=False)

    return JsonResponse({"success":False}, status=400)   

def part_label(request):
    if request.method == "GET" and request.is_ajax():
        shop= request.GET.get('shop_unit_id')
        obj=list(Code.objects.filter(cd_type='51',code=shop).values('alpha_1').distinct())
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success":False}, status=400)   

