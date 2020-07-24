from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m3view/')
def m3view(request):
    
    wo_nop = empmast.objects.none()
    if "Superuser" in g.rolelist:
        tm=list(shop_section.objects.all())
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tm,
            'usermaster':g.usermaster,
            
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = M2Docnew1.objects.all().filter(f_shopsec=g.rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'roles' :g.rolelist,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'roles' :g.rolelist,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
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
            
            obj = Part.objects.filter(partno=part_no).values('drgno','des')
            objj = list(M2Docnew1.objects.filter(m2sln=doc_no,f_shopsec=shop_sec,part_no=part_no).values('qty','rm_partno','m4_no','scl_cl','rm_qty','m2prtdt','rc_st_wk','cut_shear').distinct())
            obj1 = empmast.objects.filter(role=shop_sec).values('empname','dept_desc')
            
            prod = list(Proddem.objects.filter(part_no=part_no).values('l_fr','l_to').distinct())             
            rm_partno=objj[0]['rm_partno']
            obj3= list(Part.objects.filter(partno=rm_partno).values('des','shop_ut').distinct())            
            cuntdia=list(Cutdia.objects.filter(ep_part=part_no,rm_part=rm_partno).values('cutdia_no').distinct())    
            date = M2Docnew1.objects.filter(m2sln=doc_no).values('m2prtdt').distinct()
            shop_ut=  obj3[0]['shop_ut']
            unit_code=list(Code.objects.filter(cd_type='51',code=shop_ut).values('alpha_1').distinct()) 
            order_type=list(Batch.objects.filter(bo_no=wo_no,brn_no=brn_no,part_no=assembly_no).values('batch_type','loco_fr','loco_to'))
            assembly_desc= list(Part.objects.filter(partno=assembly_no).values('des').distinct()) 
            
            leng = obj.count()
            leng1 = obj1.count()
            
            leng2 = len(objj)

            objj[0].update({'assembly_no':assembly_no})
            objj[0].update({'part_no':part_no})
            objj[0].update({'doc_no':doc_no})

            if len(assembly_desc)==0:
                objj[0].update({'assembly_desc':''})
            else:
                objj[0].update({'assembly_desc':assembly_desc[0]['des'] })
                

            if len(order_type)==0:
                objj[0].update({'order_type':'','l_fr':'','l_to':''})
            else:
                objj[0].update({'order_type':order_type[0]['batch_type'],'l_fr':order_type[0]['loco_fr'],'l_to':order_type[0]['loco_to'] })
                
            if len(unit_code)==0:
                objj[0].update({'unit':''})
            else:
                objj[0].update({'unit':unit_code[0]['alpha_1'] })
                
            if len(obj)==0:
                objj[0].update({'drgno':'','part_des':''})
            else:
                objj[0].update({'drgno':obj[0]['drgno'],'part_des':obj[0]['des']})
                
            if len(obj3)==0:
                objj[0].update({'rm_des':'','shop_ut':''})
            else:
                objj[0].update({'rm_des':obj3[0]['des'],'shop_ut':obj3[0]['shop_ut']})
                
            if len(cuntdia)==0:
                objj[0].update({'cutdia_no':''}) 
            else:
                objj[0].update([{'cutdia_no':cuntdia[0]['cutdia_no'] }])

            if "Superuser" in g.rolelist:
                tm=list(shop_section.objects.all())              
                context={
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles':tm,
                    'obj': obj,
                    'objj': objj,
                    'obj1': obj1,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'date': date,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                    'sub':1,
                    'usermaster':g.usermaster,
                     
                }
            elif(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    req = M2Docnew1.objects.all().filter(f_shopsec=g.rolelist[i]).values('batch_no').distinct()
                    wo_nop =wo_nop | req
                context = {
                    'lenm' :len(g.rolelist),
                    'wo_nop':wo_nop,
                    'roles' :g.rolelist,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'obj': obj,
                    'objj': objj,
                    'obj1': obj1,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'date': date,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                    'sub':1,
                }
            elif(len(g.rolelist)>1):
                context = {
                    'lenm' :len(g.rolelist),
                    'roles' :g.rolelist,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'obj': obj,
                    'objj': objj,
                    'obj1': obj1,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'date': date,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                    'sub':1,
                }
    return render(request,"MCARD/M3CARD/m3view.html",context)


def m3getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = list(M2Docnew1.objects.filter(f_shopsec = shop_sec).values('batch_no').distinct())     
        return JsonResponse(wo_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m3getbr(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = list(M2Docnew1.objects.filter(batch_no =wo_no).values('brn_no').distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m3shopsec(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = list(M2Docnew1.objects.filter(batch_no =wo_no,brn_no=br_no).values('f_shopsec').distinct())
        return JsonResponse(shop_sec, safe = False)
    return JsonResponse({"success":False}, status=400)

def m3getassly(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = list(M2Docnew1.objects.filter(batch_no =wo_no,brn_no=br_no,f_shopsec=shop_sec).values('assly_no').distinct())
        return JsonResponse(assembly_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m3getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        part_no = list(M2Docnew1.objects.filter(batch_no =wo_no,brn_no=br_no,f_shopsec=shop_sec,assly_no=assembly_no).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m3getdoc_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M2Docnew1.objects.filter(batch_no =wo_no,brn_no=br_no,f_shopsec=shop_sec,assly_no=assembly_no,part_no=part_no).values('m2sln').distinct())
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m3sub(request):
    if request.method == "POST":
        shop_sec = request.POST.get('shop_sec')
        part_no = request.POST.get('part_nop')
        wo_no = request.POST.get('wo_no')
        brn_no = request.POST.get('br_no')
        assembly_no = request.POST.get('assm_no')
        doc_no = request.POST.get('doc_no')
        obj = Part.objects.filter(partno=part_no).values('drgno','des') 
        objj = M2Docnew1.objects.filter(m2sln=doc_no,f_shopsec=shop_sec,partno=part_no).values('qty','m4_no','scl_cl','rm_partno')
        obj1 = empmast.objects.filter(role=shop_sec).values('empname','dept_desc')
        date = M2Docnew1.objects.filter(m2sln=doc_no).values('m2prtdt').distinct()
        leng = obj.count()
        leng1 = obj1.count()
        leng2 = objj.count()
         
        context = {
                    'obj': obj,
                    'objj': objj,
                    'obj1': obj1,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'date': date,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
    }

    return render(request, "MCARD/M3CARD/m3view.html", context)



