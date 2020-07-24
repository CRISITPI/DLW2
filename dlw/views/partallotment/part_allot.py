from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/partallotement/')
def partallotement(request):
    
    partnew = list(Partnew.objects.all().values('part_no').distinct())
    partgrp = list(Ngr.objects.all().values('mgr').distinct())
    subgrp2 = list(Ngr.objects.all().values('sgr2','sln'))
    it_cat = list(GmCode.objects.filter(cd_type='IT').values('alpha_1').distinct())
    unit = list(GmCode.objects.filter(cd_type='UT').values('alpha_1').distinct())
    MB = list(GmCode.objects.filter(cd_type='MB').values('alpha_1').distinct())
 
    tm=shop_section.objects.all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'subnav':g.subnav,
        'partnew' : partnew,
        'partgrp' : partgrp,
        'it_cat' : it_cat,
        'usermaster':g.usermaster,
        'unit' : unit,
        'mb' : MB,
        'subgrp2': subgrp2, 
    }
   
    return render(request,"PARTALLOTMENT/partallotement.html",context)


def getpartnewdetails(request):
    if request.method == "GET" and request.is_ajax():        
        partno_temp = request.GET.get("partno_temp")
        partnew = list(Partnew.objects.filter(part_no=partno_temp).values('gm_ptno','rev','des','mb','unit','size_pc','mat_specn','ind_buy','it_cat','unit_wt').distinct())
        return JsonResponse(partnew, safe = False)
    return JsonResponse({"success":False}, status=400)

def getpartnewdetails123(request):
    if request.method == "GET" and request.is_ajax():        
        partgrp_temp = request.GET.get("maj_grp_temp")        
        partgrp = list(Ngr.objects.filter(mgr = partgrp_temp).values('sgr1').distinct())
        return JsonResponse(partgrp, safe = False)
    return JsonResponse({"success":False}, status=400)

def getsubgrp2(request):
    if request.method == "GET" and request.is_ajax():
        subgrp_temp_temp = request.GET.get("subgrp_temp_temp")  
        subgrp2 = list(Ngr.objects.filter(sgr1 = subgrp_temp_temp).values('sgr2').exclude(sgr2__isnull=True))
        return JsonResponse(subgrp2, safe = False)
    return JsonResponse({"success":False}, status=400)

def getDiscription(request):
    if request.method == "GET" and request.is_ajax():
        SUB_GROUP2_temp = request.GET.get("SUB_GROUP2_temp")  
        subgrpDesc = list(Ngr.objects.filter(sgr2 = SUB_GROUP2_temp).values('sln','gdes').exclude(sgr2__isnull=True))
        return JsonResponse(subgrpDesc, safe = False)
    return JsonResponse({"success":False}, status=400)

def getpartdecription(request):
    if request.method == "GET" and request.is_ajax():        
        subgrp_temp_temp = request.GET.get("subgrp_temp")        
        partgrp = list(Ngr.objects.filter(gdes = subgrp_temp_temp).values('gdes'))
        return JsonResponse(partgrp, safe = False)
    return JsonResponse({"success":False}, status=400)

def GenerateNewPartNo(request):
    if request.method == "GET" and request.is_ajax():        
        majg = request.GET.get("majg")  
        subg1= request.GET.get("subg1")
        subg2= request.GET.get("subg2")
        sl_no= request.GET.get("sl_no")
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
        return JsonResponse(part, safe = False)
    return JsonResponse({"success":False}, status=400)




