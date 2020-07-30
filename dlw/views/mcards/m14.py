from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/m14view/')
def m14view(request):
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
    
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            brn_no = request.POST.get('br_no')
            assembly_no = request.POST.get('assm_no')
            doc_no = request.POST.get('doc_no')
            obj1 = Part.objects.filter(partno=part_no).values('des', 'drgno').distinct()
            obj2 = Part.objects.filter(partno=assembly_no).values('des').distinct()
            obj3 = Batch.objects.filter(bo_no=wo_no,brn_no=brn_no,part_no=assembly_no).values('batch_type')
            obj4 =  M14M4new1.objects.filter(doc_no=doc_no,brn_no=brn_no,assly_no=assembly_no,bo_no=wo_no,part_no=part_no).values('l_fr','l_to')
            obj5 =  M14M4new1.objects.filter(doc_no=doc_no,brn_no=brn_no,assly_no=assembly_no,bo_no=wo_no,part_no=part_no).values('opn_no','pm_no','due_wk')
            obj = M14M4new1.objects.filter(doc_no=doc_no,brn_no=brn_no,assly_no=assembly_no,bo_no=wo_no,part_no=part_no).values('received_mat14', 'issued_qty14', 'received_qty14', 'laser_pst14', 'line14', 'closing_bal14', 'remarks14', 'posted_date14', 'wardkp_date14', 'shopsup_date14', 'posted1_date14')
            obj6 = Part.objects.filter(partno=part_no).values('m14splt_cd').distinct()
            code = M14M4new1.objects.filter(doc_no=doc_no,brn_no=brn_no,assly_no=assembly_no,bo_no=wo_no,part_no=part_no).values('unit').distinct()
            obj7 = Code.objects.filter(cd_type='51',code=code[0]['unit']).values('alpha_1').distinct()
          
            if len(obj7)==0:
                obj7=[{'alpha_1':'None'}] 
            if obj6[0]['m14splt_cd'] is None:
                obj6=[{'m14splt_cd':'1'}]    
            if len(obj) == 0:
                obj = range(0, 1)

            if len(obj4) == 0:
                obj4 = range(0, 1)

            if len(obj5) == 0:
                obj5 = range(0, 1)
            
            if len(obj6) == 0:
                obj6 = range(0, 1)
            
            date = M14M4new1.objects.filter(doc_no=doc_no,brn_no=brn_no,assly_no=assembly_no,bo_no=wo_no).values('prtdt','qty').distinct()
            leng = obj.count()
            lenm = obj4.count()
            lenn = obj5.count()
            datel= date.count()
            context = {
                    'roles':tmp,
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'obj4': obj4,
                    'obj5': obj5,
                    'obj6': obj6,
                    'obj7': obj7,
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
                    'usremaster':g.usermaster,
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
            M14M4new1.objects.filter(part_no=part_no,doc_no=doc_no,brn_no=brn_no,bo_no=wo_no).update(received_mat14=str(received_mat), issued_qty14=str(issued_qty), received_qty14=str(received_qty), laser_pst14=str(laser_pst), line14=str(line), closing_bal14=str(closing_bal), remarks14=str(remarks), posted_date14=str(posted_date), wardkp_date14=str(wardkp_date), shopsup_date14=str(shopsup_date), posted1_date14=str(posted1_date))
           
            messages.success(request, 'Successfully Updated!, Select new values to update')
    return render(request, "MCARD/M14CARD/m14view.html", context)




def m14getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        w1 = Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w3=M14M4new1.objects.values('bo_no')
        w2 = Batch.objects.filter(status='R',bo_no__in=w3).values('bo_no').exclude(bo_no__isnull=True).distinct()
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14getbr(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = list(M14M4new1.objects.filter(bo_no =wo_no).values('brn_no').exclude(brn_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14getassly(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assm_no = list(M14M4new1.objects.filter(bo_no =wo_no,brn_no=br_no).values('assly_no').exclude(assly_no__isnull=True).distinct())
        return JsonResponse(assm_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m14getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assembly_no = request.GET.get('assm_no')
        part_no = list(M14M4new1.objects.filter(brn_no=br_no,assly_no=assembly_no,bo_no=wo_no).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m14getdoc_no1(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M14M4new1.objects.filter(bo_no =wo_no,brn_no=br_no,assly_no=assembly_no,part_no=part_no).values('doc_no').exclude(doc_no__isnull=True).distinct())
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)













