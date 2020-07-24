from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/mg7view/')
def mg7view(request):    
    rolelist=(g.usermaster).role.split(", ")     
    wo_nop = empmast.objects.none()
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
     
    if(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').exclude(batch_no__isnull=True).distinct()
            wo_nop =wo_nop | req 
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=(g.usermaster).role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            shop_sec1 = request.POST.get('shop_sec1')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            m5no = request.POST.get('job_no')
            obj = Part.objects.filter(partno=part_no).values('des').distinct()
            obj1 = M5DOCnew.objects.filter(batch_no=wo_no, pr_shopsec=shop_sec, n_shopsec=shop_sec1, part_no=part_no).values('m5glsn').distinct()
            obj2 = M13.objects.filter(shop=shop_sec, part_no=part_no, wo=wo_no).values('m13_no').distinct()
            if len(obj2) > 0:
                obj2 = M13.objects.filter(shop=shop_sec, part_no=part_no, wo=wo_no).values('m13_no').distinct()[:1]
            date=len(obj2)
            obj3 = MG7.objects.filter(wo_no=wo_no, fromshop=shop_sec, toshop=shop_sec1, part_no=part_no, m5glsn=m5no).values('date','qty_ord','qty_rej','qty_req','reason').distinct()
            if len(obj3) == 0:
                obj3=range(0, 1) 
            if(len(rolelist)==1):
                  for i in range(0,len(rolelist)):
                      req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').exclude(batch_no__isnull=True).distinct()
                      wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :tmp,
                        'usermaster':g.usermaster,
                        'lenm' :len(rolelist),
                        'nav': g.nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,

                        'date': date,

                        'shop_sec': shop_sec,
                        'shop_sec1': shop_sec1,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'm5no': m5no,
                        'subnav':g.subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'usermaster':g.usermaster,
                        'roles' :tmp,
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,

                        'sub': 1,

                        'date': date,

                        'shop_sec': shop_sec,
                        'shop_sec1': shop_sec1,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'm5no': m5no, 
                        'subnav':g.subnav
                  }

        if submitvalue=='Save':

                shop_sec= request.POST.get('shop_sec11')
                shop_sec1 = request.POST.get('shop_sec12')
                part_no= request.POST.get('part_no1')
                wo_no = request.POST.get('wo_no1')
                m5no = request.POST.get('m5no11')
                des = request.POST.get('des1')
                m13_no = request.POST.get('m13_no11')
               
                qty_ord =request.POST.get('qty_ord')
                qty_req = request.POST.get('qty_req')
                qty_rej = request.POST.get('qty_rej')
                date = request.POST.get('date')
                reason =request.POST.get('reason')

                obj4 = MG7.objects.filter(wo_no=wo_no, fromshop=shop_sec, toshop=shop_sec1, part_no=part_no, m5glsn=m5no).distinct()
                if len(obj4) == 0:
                    MG7.objects.create(wo_no=str(wo_no), m13_no=str(m13_no), des=str(des), fromshop=str(shop_sec), toshop=str(shop_sec1), part_no=str(part_no), m5glsn=str(m5no), qty_ord=int(qty_ord),qty_req=int(qty_req),qty_rej=int(qty_rej),date=str(date),reason=str(reason))

                else:
                    MG7.objects.filter(wo_no=wo_no, fromshop=shop_sec, toshop=shop_sec1, part_no=part_no, m5glsn=m5no).update(qty_ord=int(qty_ord), qty_req=int(qty_req), qty_rej=int(qty_rej), date=str(date), reason=str(reason))

                wo_no=MG7.objects.all().values('wo_no').distinct()
                messages.success(request, 'Successfully Done!, Select new values to proceed')
    return render(request, "MGCARD/MG7CARD/mg7view.html", context)



def mg7getshop(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')
        shop = M5DOCnew.objects.filter(pr_shopsec=shop_sec).values('n_shopsec').exclude(n_shopsec__isnull=True).distinct()
        shop_sec1 = list(shop)
        return JsonResponse(shop_sec1, safe=False)
    return JsonResponse({"success": False}, status=400)

def mg7getjob(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        shop_sec1 = request.GET.get('shop_sec1')
        part_nop = request.GET.get('part_nop')
        job = M5DOCnew.objects.filter(pr_shopsec=shop_sec, n_shopsec=shop_sec1, batch_no=wo_no,  part_no=part_nop).values('m5glsn').distinct()
        jobno = list(job)
        return JsonResponse(jobno, safe=False)
    return JsonResponse({"success": False}, status=400)

def mg7getwono(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')
        shop_sec1 = request.GET.get('shop_sec1')
        wo = M5DOCnew.objects.filter(pr_shopsec=shop_sec, n_shopsec=shop_sec1).values('batch_no').exclude(batch_no__isnull=True).distinct()
        wono = list(wo)
        return JsonResponse(wono, safe=False)
    return JsonResponse({"success": False}, status=400)




def mg7getpartno(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        shop_sec1 = request.GET.get('shop_sec1')
        pa = M5DOCnew.objects.filter(pr_shopsec=shop_sec,n_shopsec=shop_sec1, batch_no=wo_no).values('part_no').exclude(part_no__isnull=True).distinct()
        part_no = list(pa)
        return JsonResponse(part_no, safe=False)
    return JsonResponse({"success": False}, status=400)










  






