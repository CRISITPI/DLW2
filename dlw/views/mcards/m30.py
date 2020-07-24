from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m30view/')
def m30view(request):
     
    wo_nop = empmast.objects.none()
    rolelist=(g.usermaster).role.split(", ")
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
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
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):

            req = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
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
            part_no = request.POST.get('part_nop')
            staff_no = request.POST.get('staff_no')
            date = request.POST.get('date')
            req = request.POST.get('req')
            obj = Part.objects.filter(partno=part_no).values('des', 'drgno').distinct()
            rand=random.randint(0, 100000000)
            obj1= Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('name', 'desgn', 'cat', 'emp_type').distinct()
            obj2=Batch.objects.filter(part_no=part_no).values('loco_fr', 'loco_to').distinct()
            obj3 = M30.objects.filter(shop_sec=shop_sec, staff_no=staff_no, part_no=part_no, date=date).values('qty', 'dimension','spe_val','obt_val','interc', 'waiver_no', 'waiver_date','non_conf_des','reason_for_non_conf','corr_action_plan','remarks_hod','remarks_cde','remarks_cqam','request_no').distinct()
            if len(obj3) == 0:
                obj3 =range(0, 1)
             
            if(len(rolelist)==1):
                  for i in range(0,len(rolelist)):
                        req = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
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


                        'req': req,
                        'staff_no': staff_no,
                        'rand': rand,

                        'sub': 1,

                        'date': date,

                        'shop_sec': shop_sec,
                        'part_no': part_no,

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
                        'req': req,
                        'staff_no': staff_no,
                        'rand': rand,

                        'sub': 1,

                        'date': date,

                        'shop_sec': shop_sec,
                        'part_no': part_no,

                        'subnav':g.subnav
                  }

        if submitvalue=='Save':

            shop_sec= request.POST.get('shop_sec1')
            part_no= request.POST.get('part_no1')
            staff_no = request.POST.get('staff_no1')
            req = request.POST.get('req1')
            date = request.POST.get('date1')


            qty = request.POST.get('qty')
            dimension = request.POST.get('dimension')
            spe_val = request.POST.get('spe_val')
            obt_val = request.POST.get('obt_val')
            loco_fr = request.POST.get('loco_fr1')
            loco_to = request.POST.get('loco_to1')
            interc = request.POST.get('interc')
            waiver_no = request.POST.get('waiver_no')
            waiver_date = request.POST.get('waiver_date')
            non_conf_des = request.POST.get('non_conf_des')
            reason_for_non_conf = request.POST.get('reason_for_non_conf')
            corr_action_plan = request.POST.get('corr_action_plan')
            remarks_hod = request.POST.get('remarks_hod')
            remarks_cqam = request.POST.get('remarks_cqam')
            remarks_cde = request.POST.get('remarks_cde')
            request_no = request.POST.get('rand1')
            specification_no=request.POST.get('spec_no1')
            obj5 = M30.objects.filter(shop_sec=shop_sec, staff_no=staff_no, part_no=part_no, date=date).distinct()
            if len(obj5) == 0:
                M30.objects.create(shop_sec=str(shop_sec), staff_no=str(staff_no), part_no=str(part_no), specification_no=str(specification_no),  request_no=str(request_no), loco_fr=str(loco_fr), loco_to=str(loco_to), req=str(req), date=str(date), qty=str(qty), dimension=str(dimension), spe_val=str(spe_val), obt_val=str(obt_val), interc=str(interc), waiver_no=str(waiver_no), waiver_date=str(waiver_date), non_conf_des=str(non_conf_des), reason_for_non_conf=str(reason_for_non_conf),  corr_action_plan=str( corr_action_plan), remarks_hod=str(remarks_hod), remarks_cqam=str(remarks_cqam), remarks_cde=str(remarks_cde))
            else:
                M30.objects.filter(shop_sec=shop_sec, staff_no=staff_no, part_no=part_no, date=date).update(specification_no=str(specification_no),  request_no=str(request_no), loco_fr=str(loco_fr), loco_to=str(loco_to), req=str(req), qty=str(qty), dimension=str(dimension), spe_val=str(spe_val), obt_val=str(obt_val), interc=str(interc), waiver_no=str(waiver_no), waiver_date=str(waiver_date), non_conf_des=str(non_conf_des), reason_for_non_conf=str(reason_for_non_conf),  corr_action_plan=str( corr_action_plan), remarks_hod=str(remarks_hod), remarks_cqam=str(remarks_cqam), remarks_cde=str(remarks_cde))
            wo_no=M2Doc.objects.all().values('batch_no').distinct()
            messages.success(request, 'Successfully Updated!, Select new values to update')
    return render(request, "MCARD/M30CARD/m30view.html", context)


def m30getpartno(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        partno = list(w1)
        return JsonResponse(partno, safe = False)
    return JsonResponse({"success": False}, status=400)




def m30getstaffno(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')

        staff = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
        staff_no = list(staff)
        return JsonResponse(staff_no, safe=False)
    return JsonResponse({"success": False}, status=400)



