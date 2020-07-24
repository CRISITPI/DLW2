from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m15view/')
def m15view(request):
    import datetime 
    wo_nop = empmast.objects.none()
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)

    if "Superuser" in g.rolelist:        
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = M13.objects.all().filter(shop=g.rolelist[i]).values('wo').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles':tmp,             
            'subnav':g.subnav,
        }
        
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'subnav':g.subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            part_no = request.POST.get('part_no')
            obj = M13.objects.filter(shop=shop_sec,part_no=part_no,wo=wo_no).values('m13_no','rate','allocation').distinct()
            obj1 = Part.objects.filter(partno=part_no).values('des')
            obj2 = M15.objects.filter(shop=shop_sec,wo=wo_no,part_no=part_no).values('doc_no','c_d_no','unit','metric_ton_returned','qty_ret','metric_ton_received','qty_rec_inward','rupees','paise','allocation','rate','mat_ret_date','mat_rec_date','posted_date')
            noprint=0
            leng = obj.count()
            leng1 = obj1.count()
            leng2 = obj2.count()
            if len(obj2) == 0:
                noprint=1

            context = {
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'len': leng,
                        'len1':leng1,
                        'len2':leng2,
                        'shop_sec': shop_sec,
                        'wo_no': wo_no,
                        'part_no': part_no,
                        'noprint':noprint,
                        'sub' : 1,
                        'nav':g.nav,
                        'ip':get_client_ip(request),  
                        'subnav':g.subnav,
                        'usermaster':g.usermaster,
                        'roles' :tmp,
            }
             
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    req = M13.objects.all().filter(shop=g.rolelist[i]).values('wo').distinct()
                    wo_nop =wo_nop | req
                context = {
                    'sub':0,
                    'lenm' :len(g.rolelist),
                    'wo_nop':wo_nop,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    'subnav':g.subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                    'noprint':noprint,
                    'sub' : 1,
                    'nav':g.nav,
                    'ip':get_client_ip(request),  
                    'subnav':g.subnav,
                }
        
            elif(len(g.rolelist)>1):
                context = {
                    'sub':0,
                    'lenm' :len(g.rolelist),
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    'subnav':g.subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                    'noprint':noprint,
                    'sub' : 1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':g.subnav,
                }
        if submitvalue =='Submit':
                leng=request.POST.get('len')
                shop_sec= request.POST.get('shop_sec')
                wo_no = request.POST.get('wo_no')
                part_no = request.POST.get('part_no')
                unit = request.POST.get('unit')
                allocation = request.POST.get('allocation')
                rate = request.POST.get('rate')
                rupees = request.POST.get('rupees')
                paise = request.POST.get('paise')
                mat_ret_date = request.POST.get('mat_ret_date')
                mat_rec_date = request.POST.get('mat_rec_date')
                m13_no = request.POST.get('m13_no')
                des = request.POST.get('des')
                posted_date = request.POST.get('posted_date')
                doc_no = request.POST.get('doc_no')
                c_d_no = request.POST.get('c_d_no')
                qty_ret = request.POST.get('qty_ret')
                qty_rec_inward = request.POST.get('qty_rec_inward')
                metric_ton_returned = request.POST.get('metric_ton_returned')
                metric_ton_received = request.POST.get('metric_ton_received')
                now = datetime.datetime.now()

                m15obj = M15.objects.filter(shop=shop_sec,wo=wo_no).distinct()
                if len(m15obj) == 0:
                    
                    M15.objects.create(login_id=request.user,shop=str(shop_sec),wo=str(wo_no),part_no=str(part_no),last_modified=str(now),unit=str(unit),allocation=str(allocation),rate=str(rate),rupees=str(rupees),paise=str(paise),mat_ret_date=str(mat_ret_date),
                    mat_rec_date=str(mat_rec_date),m13_no=str(m13_no),metric_ton_returned=str(metric_ton_returned),metric_ton_received=str(metric_ton_received),des=str(des),posted_date=str(posted_date),doc_no=str(doc_no),c_d_no=str(c_d_no),qty_ret=str(qty_ret),qty_rec_inward=str(qty_rec_inward))
                    
                

                else:
                    M15.objects.filter(shop=shop_sec,wo=wo_no,part_no=str(part_no)).update(unit=str(unit),allocation=str(allocation),rate=str(rate),rupees=str(rupees),paise=str(paise),mat_ret_date=str(mat_ret_date),
                    mat_rec_date=str(mat_rec_date),last_modified=str(now),login_id=request.user.username,posted_date=str(posted_date),metric_ton_returned=str(metric_ton_returned),metric_ton_received=str(metric_ton_received),m13_no=str(m13_no),des=str(des),doc_no=str(doc_no),c_d_no=str(c_d_no),qty_ret=str(qty_ret),qty_rec_inward=str(qty_rec_inward))
            
                wo_nop=M13.objects.all().values('wo').distinct()
   
    return render(request,"MCARD/M15CARD/m15view.html",context)


def m15getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = list(M13.objects.filter(shop = shop_sec).values('wo').distinct())
        return JsonResponse(wo_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m15getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        part_no = list(M13.objects.filter(shop = shop_sec,wo=wo_no).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m18getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)    

def m18getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        part_no = list(M5DOCnew.objects.filter(batch_no =wo_no,shop_sec=shop_sec).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)    

def m18getoperation_no(request):
    if request.method == "GET" and request.is_ajax():
        part_nop = request.GET.get('part_nop')
        shop_sec = request.GET.get('shop_sec')
        opnno = list(Oprn.objects.filter(part_no =part_nop,shop_sec=shop_sec).values('opn').exclude(part_no__isnull=True).distinct())
        return JsonResponse(opnno, safe = False)
    return JsonResponse({"success":False}, status=400) 

def m18getoperation_desc(request):
    if request.method == "GET" and request.is_ajax():
        part_nop = request.GET.get('part_nop')
        shop_sec = request.GET.get('shop_sec')
        opno = request.GET.get('opno')
        opndesc = list(Oprn.objects.filter(part_no=part_nop,shop_sec=shop_sec,opn=opno).values('des').exclude(part_no__isnull=True).distinct())
        return JsonResponse(opndesc, safe = False)
    return JsonResponse({"success":False}, status=400) 

def m18getRef_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        part_nop = request.GET.get('part_nop')
        refno = list(M5DOCnew.objects.filter(batch_no =wo_no,shop_sec=shop_sec,part_no =part_nop).values('m5glsn').exclude(part_no__isnull=True).distinct())
        return JsonResponse(refno, safe = False)
    return JsonResponse({"success":False}, status=400) 







