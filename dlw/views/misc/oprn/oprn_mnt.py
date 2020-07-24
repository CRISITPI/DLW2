from dlw.views import *
import dlw.views.globals as g

def oprn_part_details(request):
    if request.method == "GET" and request.is_ajax():
        pno = request.GET.get('partno')
        obj = list(Part.objects.filter(partno = pno).values('des','ptc').distinct())
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)

def oprnget_opn(request):
    if request.method == "GET" and request.is_ajax():
        pno = request.GET.get('partno')
        obj = list(Oprn.objects.filter(part_no = pno).values('opn').distinct())
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)

def oprn_opndetails(request):
    
    if request.method == "GET" and request.is_ajax():
        op = request.GET.get('opnno')
        pno = request.GET.get('partno')
        obj = list(Oprn.objects.filter(opn = op, part_no = pno).values('shop_sec','des','lc_no','m5_cd','ncp_jbs','pa','at','lot').distinct())

        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)
def oprn_dele_status(request):
    if request.method == "GET" and request.is_ajax():
        pno = request.GET.get('partno')
        op = request.GET.get('opnno')
        d = date.today().isoformat()
        Oprn.objects.filter(opn = op , part_no = pno).update(del_fl = 'y', updt_dt = d)
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)
    
def oprn_dupdate(request):
    if request.method == "GET" and request.is_ajax():
        pno = request.GET.get('partno')     
        obj = list(Oprn.objects.filter( part_no = pno).values('opn').distinct())
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)
def oprn_insert(request):
    if request.method == "GET" and request.is_ajax():
        part_no = request.GET.get('part_no')
        des = request.GET.get('des')
        opn = request.GET.get('opn')
        lc_no = request.GET.get('lc_no')
        shop_sec = request.GET.get('shop_sec')
        m5_cd = request.GET.get('m5_cd')
        ncp_jbs = request.GET.get('ncp_jbs')
        pa = request.GET.get('pa')
        at = request.GET.get('at')
        lot = request.GET.get('lot')
        Oprn.objects.create(part_no = part_no , opn = opn, des = des, lc_no = lc_no, shop_sec = shop_sec, m5_cd = m5_cd, ncp_jbs = ncp_jbs, pa = pa, at = at, lot = lot)
        return JsonResponse(opn, safe = False)
    return JsonResponse({"success":False}, status = 400)  

def oprn_update(request):

    if request.method == "GET" and request.is_ajax():
        part_no = request.GET.get('part_no')
        des = request.GET.get('des')
        opn = request.GET.get('opnno')
        lc_no = request.GET.get('lc_no')
        shop_sec = request.GET.get('shop_sec')
        m5_cd = request.GET.get('m5_cd')
        ncp_jbs = request.GET.get('ncp_jbs')
        pa = request.GET.get('pa')
        at = request.GET.get('at')
        lot = request.GET.get('lot') 
        obj = list(Oprn.objects.filter(part_no = part_no, opn = opn).values('part_no','opn','shop_sec','des','lc_no','m5_cd','ncp_jbs','pa','at','lot').distinct())
        Oprn.objects.filter(part_no = part_no, opn = opn).update(opn = opn, des = des, lc_no = lc_no, shop_sec = shop_sec, m5_cd = m5_cd, ncp_jbs = ncp_jbs, pa = pa, at = at, lot = lot)    
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)     

def oprn_lc_des(request):
    if request.method == "GET" and request.is_ajax():
        lc = request.GET.get('lcno')
        ss = request.GET.get('shopsec')
        obj = list(Lc1.objects.filter(lcno = lc, shop_sec = ss).values('des').distinct())
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)

def oprn_lc_no(request):
    if request.method == "GET" and request.is_ajax():
        ss = request.GET.get('shopsec')
        obj = list(Lc1.objects.filter(shop_sec = ss).values('lcno').distinct())
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)

def oprn_shop_validate(request):
    if request.method == "GET" and request.is_ajax():
        shop = request.GET.get('sec')
        obj = list(Shop.objects.values('shop').order_by('shop').distinct())
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)

def oprn_audit_save(request):
    if request.method == "GET" and request.is_ajax():
        by = str(request.user)
        time = datetime.datetime.now().time()
        val = dict(request.GET)
        k = list(val.keys())
        Oprn_audit.objects.create(updt_by = by, updt_time = time, updt_col = k)
        return JsonResponse(by, safe = False)
    return JsonResponse({"success":False}, status = 400)

 
@login_required
@role_required(urlpass='/oprnview/')
def oprnview(request):

    
    wo_nop = empmast.objects.none()
    
     
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'op_opnno' : wo_nop,
        'subnav':g.subnav,
        'usermaster':g.usermaster
    }

    return render(request,'MISC/OPRN/oprnview.html',context)
