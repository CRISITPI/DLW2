from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m4hwview/')
def m4hwview(request):
    import datetime
    rolelist=(g.usermaster).role.split(", ")
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
    if(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = M14M4.objects.filter(assly_no__in=w1).values('bo_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'subnav':g.subnav,
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
            obj = M14M4.objects.filter(doc_no=doc_no,assly_no=assembly_no,brn_no=brn_no,part_no=part_no).values('received_mat', 'issued_qty', 'received_qty', 'laser_pst', 'line', 'closing_bal', 'remarks', 'posted_date', 'wardkp_date', 'shopsup_date', 'posted1_date')

            if len(obj) == 0:
                obj = range(0,1)
            date = M14M4.objects.filter(doc_no=doc_no,assly_no=assembly_no,brn_no=brn_no,part_no=part_no).values('prtdt','qty').distinct()
            leng = obj.count()
            datel = date.count()           
           
                
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
                    'usermaster':g.usermaster,

                }
            if(len(rolelist)==1):
                for i in range(0,len(rolelist)):                    

                    w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    req = M14M4.objects.filter(assly_no__in=w1).values('bo_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'wo_nop':wo_nop,
                    'roles' :tmp,
                    'subnav':g.subnav,
                    'usermaster':g.usermaster,
                    'lenm' :len(rolelist),
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
            elif(len(rolelist)>1):
                context = {
                    'lenm' :len(rolelist),
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
            rand  = random.choice('0123456789')           
            rand1 = random.choice('0123456789')        
            rand2 = random.choice('0123456789')           
            rand3 = random.choice('0123456789')         
            rand4 = random.choice('0123456789')          
            rand5 = random.choice('0123456789')           
            num = rand + rand1 + rand2 + rand3 + rand4 + rand5           
            number = num

            prtDate= request.POST.get('prtdt')              
            monthTemp = prtDate.split(' ')[0]            
            dateTemp = prtDate.split(' ')[1]                    
            final1 = monthTemp[0:3]+' '+dateTemp.split(',')[0]+' '+prtDate.split(' ')[2]
            date_time_str = final1
            date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y')
            wo_no= request.POST.get('wo_no')          
            brn_no=request.POST.get('brn_no')         
            qty=request.POST.get('qty')  
            end_prod = request.POST.get('end_prod')         
            epdes = request.POST.get('epdes')        
            shop_section_temp = request.POST.get('shop_section_temp')        
            part_no = request.POST.get('part_no')        
            partdes= request.POST.get('partdes')        
            drgno = request.POST.get('drgno')           
            doc_no = request.POST.get('doc_no')         
            batch_type = request.POST.get('batch_type')          
            received_mat = request.POST.get('received_mat')        
            issued_qty = request.POST.get('issued_qty')        
            received_qty = request.POST.get('received_qty')      
            laser_pst = request.POST.get('laser_pst')        
            line = request.POST.get('line')                  
            closing_bal = request.POST.get('closing_bal')          
            remarks = request.POST.get('remarks')       
            posted_date = request.POST.get('posted_date')        
            wardkp_date = request.POST.get('wardkp_date')            
            shopsup_date = request.POST.get('shopsup_date')        
            posted1_date = request.POST.get('posted1_date')
            causesofHW = request.POST.get('causesofHW')        
            
            M4HW.objects.create(prtdt=str(date_time_obj.date()),doc_no=str(doc_no),part_no=str(part_no),wo_no=str(wo_no),brn_no=str(brn_no),qty=str(qty),end_prod=str(end_prod),epdes=str(epdes),shop_section_temp=str(shop_section_temp),partdes=str(partdes),drgno=str(drgno),batch_type=str(batch_type),received_mat=str(received_mat),issued_qty=str(issued_qty),received_qty=str(received_qty),laser_pst=str(laser_pst),line=str(line),closing_bal=str(closing_bal),remarks=str(remarks),posted_date=str(posted_date),wardkp_date=str(wardkp_date),shopsup_date=str(shopsup_date),posted1_date=str(posted1_date),number=str(number),causesofHW=str(causesofHW))         
            messages.success(request, 'M4 Card Hand Written generated Successfully, Your Reference number is : '+number)
           
    return render(request,"MCARD/M4HWCARD/m4hwview.html",context)   


def m4getbrhw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = list(M14M4.objects.filter(bo_no =wo_no).values('brn_no').exclude(brn_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m4getwonohw(request):
    if request.method == "GET" and request.is_ajax():
        from.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1 = Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2 = M14M4.objects.filter(assly_no__in=w1).values('bo_no').exclude(bo_no__isnull=True).distinct()
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)








def m4getasslyhw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assm_no = list(M14M4.objects.filter(bo_no =wo_no,brn_no=br_no).values('assly_no').exclude(assly_no__isnull=True).distinct())
        return JsonResponse(assm_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m4getpart_nohw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assembly_no = request.GET.get('assm_no')
        part_no = list(M14M4.objects.filter(brn_no=br_no,assly_no=assembly_no,bo_no=wo_no).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m4getdoc_nohw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M14M4.objects.filter(bo_no =wo_no,brn_no=br_no,assly_no=assembly_no,part_no=part_no).values('doc_no').exclude(doc_no__isnull=True).distinct())
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)


      
