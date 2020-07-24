from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m2hwview/')
def m2hwview(request):
    import datetime
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    tmp=[]        
    for on in tm:
        tmp.append(on.section_code)

    wo_nop = user_master.objects.none()  
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

            w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
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
            check_obj=Oprn.objects.all().filter(shop_sec=shop_sec)            
            obj = Oprn.objects.filter(part_no=part_no).values('opn', 'shop_sec', 'lc_no', 'des','pa','at','lot','mat_rej','qtr_accep', 'qty_prod','work_rej').order_by('opn')
            date = M2Doc.objects.filter(m2sln=doc_no).values('m2prtdt','qty').distinct()
            leng = obj.count()
            datel= date.count()

            if "Superuser" in g.rolelist:
                
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':g.nav,
                        'ip':get_client_ip(request),
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
                        'subnav':g.subnav,
                        'usermaster':g.usermaster,
                  }
            elif(len(g.rolelist)==1):
                  for i in range(0,len(g.rolelist)):                        

                        w1 = Oprn.objects.filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                        req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                        wo_nop = wo_nop | req

                  context = {
                        'wo_nop':wo_nop,
                        'roles' :tmp,
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
                        'subnav':g.subnav
                  }
            elif(len(g.rolelist)>1):
                  context = {
                        'lenm' :len(g.rolelist),
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
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
                        'subnav':g.subnav
                  }
        
        rand = random.choice('0123456789') 
        rand1 = random.choice('0123456789')
        rand2 = random.choice('0123456789')
        rand3 = random.choice('0123456789')
        rand4 = random.choice('0123456789')
        rand5 = random.choice('0123456789')
        num = rand + rand1 + rand2 + rand3 + rand4 + rand5    

        if submitvalue=='Save':
            leng=request.POST.get('len')
              
            for i in range(1, int(leng)+1):           
                
                shopsec= request.POST.get('shopsec')
                partno= request.POST.get('partno')
                prtDate     = request.POST.get('prtDate')                                          
                monthTemp = prtDate.split(' ')[0]            
                dateTemp = prtDate.split(' ')[1]                    
                final1 = monthTemp[0:3]+' '+dateTemp.split(',')[0]+' '+prtDate.split(' ')[2]                              
                date_time_str = final1
                date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y')

                workOrdNo   = request.POST.get('workOrdNo')
                brnNo       = request.POST.get('brnNo')
                orderQuantity= request.POST.get('orderQuantity')
                asmlyPartNo = request.POST.get('asmlyPartNo')
                asmlyDesc   = request.POST.get('asmlyDesc')
                shopSection = request.POST.get('shopSection')
                partNum     = request.POST.get('partNum')
                partDescription= request.POST.get('partDescription')
                drawingNum  = request.POST.get('drawingNum')
                documentNum = request.POST.get('documentNum')
                orderType   = request.POST.get('orderType')          
                number   = num  
                causesofHW  =   request.POST.get('causesofHW')    

                operationNum=request.POST.get('operationNum'+str(i)) 
                shopSecTemp=request.POST.get('shopSecTemp'+str(i)) 
                loadCenter=request.POST.get('loadCenter'+str(i)) 
                operationDescription=request.POST.get('operationDescription'+str(i)) 
                paTemp=request.POST.get('paTemp'+str(i)) 
                taTemp=request.POST.get('taTemp'+str(i))
                noTemp=request.POST.get('noTemp'+str(i))    
                qtypr=request.POST.get('qtypr'+str(i))
                qtyac = request.POST.get('qtyac'+str(i))
                wrrej = request.POST.get('wrrej'+str(i))
                matrej = request.POST.get('matrej'+str(i))               

                M2HW.objects.create(prtDate=str(date_time_obj.date()),workOrdNo=str(workOrdNo),brnNo=str(brnNo),orderQuantity=str(orderQuantity),asmlyPartNo=str(asmlyPartNo),asmlyDesc=str(asmlyDesc),shopSection=str(shopSection),partNum=str(partNum),partDescription=str(partDescription),drawingNum=str(drawingNum),documentNum=str(documentNum),orderType=str(orderType),operationNum=str(operationNum),shopSecTemp=str(shopSecTemp),loadCenter=str(loadCenter),operationDescription=str(operationDescription),paTemp=str(paTemp),taTemp=str(taTemp),noTemp=str(noTemp),qtypr=str(qtypr),qtyac=str(qtyac),wrrej=str(wrrej),matrej=str(matrej),number=str(number),causesofHW=str(causesofHW))

            messages.success(request, 'M2 Card Hand Written generated Successfully, Your Reference number is : '+number)
    return render(request, "MCARD/M2HWCARD/m2hwview.html", context)

def m2getwonohw(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2=M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m2getbrhw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        br_no = list(M2Doc.objects.filter(batch_no =wo_no).values('brn_no').distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m2getasslyhw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        w2=M2Doc.objects.filter(batch_no=wo_no).values('assly_no').distinct()
        w1=Oprn.objects.filter(part_no__in=w2).values('shop_sec', 'part_no').distinct()
        w3=w1.filter(shop_sec=shop_sec).values('part_no').distinct()
        w4=M2Doc.objects.filter(batch_no=wo_no, f_shopsec=shop_sec, brn_no=br_no).values('assly_no').distinct()
        w5=w3.union(w4)
        w6=w5.distinct()
        assm_no = list(w6)
        return JsonResponse(assm_no, safe=False)
    return JsonResponse({"success":False}, status=400)    

def m2getpart_nohw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        w2 = M2Doc.objects.filter(batch_no=wo_no).values('part_no').distinct()
        w1 = Oprn.objects.filter(part_no__in=w2).all().distinct()
        w3= w1.filter(shop_sec=shop_sec).values('part_no').distinct()
        w4 = M2Doc.objects.filter(batch_no=wo_no, f_shopsec=shop_sec, brn_no=br_no,assly_no=assembly_no).values('part_no').distinct()
        w5=w3.union(w4)
        w6=w5.distinct()
        part_no = list(w6)
        return JsonResponse(part_no, safe=False)
    return JsonResponse({"success":False}, status=400)    

def m2getdoc_nohw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M2Doc.objects.filter(batch_no=wo_no,part_no=part_no).values('m2sln').distinct())

        return JsonResponse(doc_no, safe=False)
    return JsonResponse({"success": False}, status=400) 








