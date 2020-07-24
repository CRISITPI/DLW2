from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/railwayshedmastermaintence/')
def railwayshedmastermaintence(request):
    wo_nop = empmast.objects.none() 
    bono=Batch.objects.filter(Q(bo_no__startswith='21') | Q(bo_no__startswith='24') | Q(bo_no__startswith='69') , status='R').values('bo_no').distinct().order_by('bo_no')
    tmp1=[]
    for on in bono:
        tmp1.append(on['bo_no'])
    context={
        'nav':g.nav,
        'ip':get_client_ip(request),
        'subnav':g.subnav,
        'bono':tmp1,
        'usermaster':g.usermaster,

    }
    return render(request, "MISC/RAILWAYSHEDMASMNT/railwayshedmastermaintence.html",context)


def RailwayMasterGetDetails(request):
    if request.method == "GET" and request.is_ajax():
        bono=request.GET.get('bono')
        obj=list(Rlyshed.objects.filter(bo_no=bono).values('consignee','railway','shed').distinct())
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success":False},status=400)

def SaveInfoRailwayShed(request):
    if request.method == "GET" and request.is_ajax():
        bono=request.GET.get('bono')
        consignee=request.GET.get('consignee')
        railway=request.GET.get('railway')
        shed=request.GET.get('shed')
        obj1=[]
        d1 = date.today()

        temp=Rlyshed.objects.values('bo_no').filter(bo_no=bono).distinct()
        if len(temp) == 0:
            temp=Rlyshed.objects.create(bo_no=str(bono),consignee=str(consignee),railway=str(railway),shed=str(shed),updt_dt=d1)
        else:
            Rlyshed.objects.filter(bo_no=bono).update(bo_no=str(bono),consignee=str(consignee),railway=str(railway),shed=str(shed),updt_dt=d1)
        return JsonResponse(obj1,safe=False)
    return JsonResponse({"success":False},status=400)