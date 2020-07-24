from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/nstrExpl/')
def nstrExpl(request): 
    wo_nop = empmast.objects.none()
    obj = list(Code.objects.filter(cd_type = 'M1').values('cd_type','code','alpha_1').order_by('code').distinct())
     
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'obj':obj,
        'usermaster':g.usermaster,
        'ip':get_client_ip(request),
        'op_opnno' : wo_nop,
        'subnav':g.subnav,
    }
    return render(request,'MISC/NSTREXPL/nstrExpl.html',context)

def nstrExpl_assdet(request):
    if request.method == "GET" and request.is_ajax():
        cd = request.GET.get('t')
        obj = list(Code.objects.filter(code = cd).values('alpha_2').distinct())
        alpha_2 = str(obj[0]['alpha_2'])
        t ={}
        if alpha_2.find(' ')-1 < 0:
            t['epc'] = alpha_2[:2]
        else:
            t['epc'] = alpha_2[:alpha_2.find(' ')]
        t2 = list(Code.objects.filter(code = cd,cd_type='M1').values('num_1','alpha_1').order_by('code').distinct())
        obj= []
        obj.append(t)
        obj.append(t2)
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400) 

def nstrassly_det(request):
    if request.method == "GET" and request.is_ajax():
        epc = request.GET.get('t1')
        assly = request.GET.get('t2')
        o = []
        obj1 = list(Nstr.objects.filter(epc = epc, pp_part = assly).values('pp_part','cp_part','ptc','epc','l_fr','l_to','qty').order_by('cp_part').distinct())
        for i in range(0,len(obj1)):
           p = list(Part.objects.filter(partno = obj1[i]['pp_part']).values('des'))
           if len(p)!=0:
                obj1[i].update({'des':p[0]['des']})
        return JsonResponse(obj1, safe = False)
    return JsonResponse({"success":False}, status = 400)  

def nstrassly_parent(request):
    if request.method == "GET" and request.is_ajax():
        pp = request.GET.get('t1')
        cp = request.GET.get('t2')
        obj1 = list(Nstr.objects.filter( cp_part = pp ).values('pp_part','cp_part','ptc','epc','l_fr','l_to','qty').order_by('cp_part').distinct())
        for i in range(0,len(obj1)):
           p = list(Part.objects.filter(partno = obj1[i]['pp_part']).values('des'))
           if len(p)!=0:
                obj1[i].update({'des':p[0]['des']})
        return JsonResponse(obj1, safe = False)
    return JsonResponse({"success":False}, status = 400)

def nstrassly_child(request):
    if request.method == "GET" and request.is_ajax():
        pp = request.GET.get('t1') 
        cp = request.GET.get('t2') 
        obj1 = list(Nstr.objects.filter( pp_part = cp).values('pp_part','cp_part','ptc','epc','l_fr','l_to','qty').order_by('cp_part').distinct())
        for i in range(0,len(obj1)):
           p = list(Part.objects.filter(partno = obj1[i]['cp_part']).values('des'))
           if len(p)!=0:
                obj1[i].update({'des':p[0]['des']})
        return JsonResponse(obj1, safe = False)
    return JsonResponse({"success":False}, status = 400)  

def nstrassly_back(request):
    if request.method == "GET" and request.is_ajax():
        pp = request.GET.get('t1')
        cp = request.GET.get('t2')
        for i in range(0,len(obj1)):
           p = list(Part.objects.filter(partno = obj1[i]['pp_part']).values('des'))
           if len(p)!=0:
                obj1[i].update({'des':p[0]['des']})
        obj1 = list(Nstr.objects.filter( cp_part = pp).values('pp_part','cp_part','ptc','epc','l_fr','l_to','qty').order_by('cp_part').distinct())
        return JsonResponse(obj1, safe = False)
    return JsonResponse({"success":False}, status = 400)


