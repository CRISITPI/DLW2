from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m4view/')
def m4view(request):
    wo_nop = empmast.objects.none()
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
        'roles':tmp,
        'usermaster':g.usermaster,
    }
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):

            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = M14M4new1.objects.filter(assly_no__in=w1).values('bo_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'subnav':g.subnav,
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
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            brn_no = request.POST.get('br_no')
            assembly_no = request.POST.get('assm_no')
            doc_no = request.POST.get('doc_no')
            kkk=Oprn.objects.all()
            obj1 = Part.objects.filter(partno=part_no).values('des', 'drgno').distinct()
            obj2 = Part.objects.filter(partno=assembly_no).values('des').distinct()
            obj3 = Batch.objects.filter(bo_no=wo_no,brn_no=brn_no,part_no=assembly_no).values('batch_type')
            obj4 =  M14M4new1.objects.filter(doc_no=doc_no,brn_no=brn_no,assly_no=assembly_no,bo_no=wo_no,part_no=part_no).values('l_fr','l_to')
            obj5 =  M14M4new1.objects.filter(doc_no=doc_no,brn_no=brn_no,assly_no=assembly_no,bo_no=wo_no,part_no=part_no).values('opn_no','pm_no','due_wk')            
            obj6 = Part.objects.filter(partno=part_no).values('m14splt_cd').distinct()
            code = M14M4new1.objects.filter(doc_no=doc_no,brn_no=brn_no,assly_no=assembly_no,bo_no=wo_no,part_no=part_no).values('unit').distinct()           
            obj7 = Code.objects.filter(cd_type='51',code=code[0]['unit']).values('alpha_1').distinct()
            check_obj=Oprn.objects.all().filter(shop_sec=shop_sec)
            obj = M14M4new1.objects.filter(doc_no=doc_no,assly_no=assembly_no,brn_no=brn_no,part_no=part_no).values('received_mat', 'issued_qty', 'received_qty', 'laser_pst', 'line', 'closing_bal', 'remarks', 'posted_date', 'wardkp_date', 'shopsup_date', 'posted1_date')
            if len(obj) == 0:
                obj = range(0,1)
            if len(obj7)==0:
                obj7=[{'alpha_1':'None'}] 
            if obj6[0]['m14splt_cd'] is None:
                obj6=[{'m14splt_cd':'1'}]    

            if len(obj4) == 0:
                obj4 = range(0, 1)

            if len(obj5) == 0:
                obj5 = range(0, 1)
            
            if len(obj6) == 0:
                obj6 = range(0, 1)
            date = M14M4new1.objects.filter(doc_no=doc_no,assly_no=assembly_no,brn_no=brn_no,part_no=part_no).values('prtdt','qty').distinct()
            leng = obj.count()
            lenm = obj4.count()
            lenn = obj5.count()
            datel = date.count()
            if(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                    req = M14M4new1.objects.filter(assly_no__in=w1).values('bo_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'wo_nop':wo_nop,
                    'roles' :tmp,
                    'subnav':g.subnav,
                    'usermaster':g.usermaster,
                    'lenm' :len(g.rolelist),
                    'nav': g.nav,
                    'ip': get_client_ip(request),
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }
            elif(len(g.rolelist)>1):
                context = {
                    'lenm' :len(g.rolelist),
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }


        if submitvalue=='Save':
            doc_no= request.POST.get('doc_no1')
            part_no= request.POST.get('part_no1')
            wo_no=request.POST.get('wo_no1')
            brn_no=request.POST.get('brn_no1')
            received_mat = request.POST.get('received_mat')
            issued_qty = request.POST.get('issued_qty')
            received_qty = request.POST.get('received_qty')
            laser_pst = request.POST.get('laser_pst')
            line= request.POST.get('line')
            closing_bal = request.POST.get('closing_bal')
            remarks = request.POST.get('remarks')
            posted_date = request.POST.get('posted_date')
            wardkp_date = request.POST.get('wardkp_date')
            shopsup_date = request.POST.get('shopsup_date')
            posted1_date = request.POST.get('posted1_date')
            M14M4new1.objects.filter(part_no=part_no,doc_no=doc_no,brn_no=brn_no,bo_no=wo_no).update(received_mat=str(received_mat), issued_qty=int(issued_qty), received_qty=int(received_qty), laser_pst=str(laser_pst), line=str(line), closing_bal=int(closing_bal), remarks=str(remarks), posted_date=str(posted_date), wardkp_date=str(wardkp_date), shopsup_date=str(shopsup_date), posted1_date=str(posted1_date))
            wo_no=M14M4new1.objects.all().values('bo_no').distinct()
            messages.success(request, 'Successfully Updated!, Select new values to update')
    return render(request, "MCARD/M4CARD/m4view.html", context)



def m4getwono(request):
    if request.method == "GET" and request.is_ajax():
        from dlw.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1 = Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2 =Batch.objects.filter(status='R').values('bo_no').exclude(bo_no__isnull=True).distinct()
        wono=list(M14M4new1.objects.filter(bo_no__in=w2,doc_code='88').values('bo_no').distinct().order_by('bo_no'))
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m4getbr(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = list(M14M4new1.objects.filter(doc_code='88',bo_no =wo_no).values('brn_no').exclude(brn_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m4getassly(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assm_no = list(M14M4new1.objects.filter(doc_code='88',bo_no =wo_no,brn_no=br_no).values('assly_no').exclude(assly_no__isnull=True).distinct())
        return JsonResponse(assm_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m4getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assembly_no = request.GET.get('assm_no')
        part_no = list(M14M4new1.objects.filter(doc_code='88',brn_no=br_no,assly_no=assembly_no,bo_no=wo_no).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m4getdoc_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M14M4new1.objects.filter(doc_code='88',bo_no =wo_no,brn_no=br_no,assly_no=assembly_no,part_no=part_no).values('doc_no').exclude(doc_no__isnull=True).distinct())
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)






