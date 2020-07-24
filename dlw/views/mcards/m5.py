from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m5newview/')
def m5newview(request):
    rolelist=(g.usermaster).role.split(", ")
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'subnav':g.subnav,
        'usermaster':g.usermaster,
    }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            brn_no = request.POST.get('br_no')
            doc_no = request.POST.get('doc_no')
            res = [int(x) for x in str(wo_no)] 

            s = [str(i) for i in res] 
            workorder = int("".join(s)) 
            obj1 = M5Docnew1.objects.filter(batch_no=wo_no,shop_sec=shop_sec, part_no=part_no,brn_no=brn_no,m5glsn=doc_no).values('opn','n_shopsec','rm_partno','cut_shear','pr_shopsec','n_shopsec','l_fr','l_to','qty_insp','inspector','date','remarks','worker','m2slno','qty_ord','m5prtdt','rm_ut','rm_qty','tot_rm_qty','rej_qty','rev_qty','lc_no','pa','at','opn_desc').distinct()
            obj2 = Part.objects.filter(partno=part_no).values('drgno','des','partno').order_by('partno').distinct()
            obj3 = Batch.objects.filter(bo_no=workorder,brn_no=brn_no,b_close_dt__isnull=True).values('part_no').distinct()
            obj4 = M5SHEMP1.objects.filter(shopsec=shop_sec).values('shopsec','staff_no','in_date','flag','name','cat','in1','out','ticket_no','month_hrs','total_time_taken','out_date','in_date','shift_typename').distinct()
            obj5 = M5SHEMP1.objects.filter(shopsec=shop_sec).values('shopsec','staff_no','name','ticket_no','flag').distinct()
            obj6  = Oprn.objects.filter(shop_sec=shop_sec,part_no=part_no).values('qtr_accep','mat_rej').exclude(qtr_accep=None,mat_rej=None).distinct()
            obj10= Batch.objects.filter(bo_no=workorder).values('batch_type','loco_fr','loco_to')
            if len(obj10)!=0:
                obj10=[{'batch_type':obj10[0]['batch_type'],'loco_fr':obj10[0]['loco_fr'],'loco_to':obj10[0]['loco_to']}]
            else:
                obj10=[{'batch_type':'','loco_fr':'','loco_to':''}]
            leng=0
            leng5=0
            leng9=0
            obj=0
            obj7=0
            obj9=0
            if len(obj1):
                raw_mat= obj1[0]['rm_partno']
                opn= obj1[0]['opn']
                obj7 = Part.objects.filter(partno=raw_mat).values('des').distinct()
                obj  = Oprn.objects.filter(part_no=part_no,opn=opn).values('ncp_jbs').distinct()
                leng = obj.count()
                leng5=obj7.count()
            if len(obj3):
                end_part=obj3[0]['part_no']
                obj9 = Part.objects.filter(partno=end_part).values('des').distinct()
                leng9=obj9.count()

            obj8 = M5SHEMP1.objects.filter(shopsec=shop_sec).values('flag').distinct()
            staff=5548
            rr=0

            staff=M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
           
            prtstaff=[]
            for i in staff:
              prtstaff.append(i['staff_no'])
            ticket= randint(1111,9999)
           
            leng1=obj1.count()
            leng2=obj2.count()
            leng3=obj3.count()
            leng4=obj4.count()
           
            leng7=obj5.count()
            leng6=obj6.count()
           
            leng8=obj8.count()
            
            
            if obj != None:
                
                context={
                        'lenm' :2,
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'obj': obj,
                        'obj1':obj1,
                        'obj2':obj2,
                        'obj3':obj3,
                        'obj4':obj4,
                        'obj7':obj7,
                        'obj5':obj5,
                        'obj6' :obj6,
                        'obj8':obj8,
                        'obj9':obj9,
                        'obj10':obj10,
                        'len9':leng9,
                        'len8':leng8,
                        'ticket1':ticket,
                        'rr':rr,
                        'sub': 1,
                        'len': leng,
                        'len1':leng1,
                        'len2':leng2,
                        'len3':leng3,
                        'len4':leng4,
                        'len5':leng5,
                        'len6':leng6,
                        'len7':leng7,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'brn_no': brn_no,
                        'doc_no': doc_no,
                        'prtstaff':prtstaff,
                        'subnav':g.subnav,
                        'usermaster':g.usermaster,
                    } 
        if submitvalue=='submit':
            leng=request.POST.get('len')
            shopsec= request.POST.get('shop_sec')
            partno= request.POST.get('partno')
            brn_no = request.POST.get('brn_no')
            inoutnum=request.POST.get("inoutnum")
            len4=request.POST.get('len4')
            qty_insp = request.POST.get('qty_insp')
            inspector = request.POST.get('inspector')
            date = request.POST.get('date')
            remarks = request.POST.get('remarks')
            rev_qty=request.POST.get('rev_qty')
            rej_qty=request.POST.get('rej_qty')
            worker=request.POST.get('worker')
            qty_acc=request.POST.get('qtyac')
            mat_rej=request.POST.get('mat_rej')
            
            M5Docnew1.objects.filter(shop_sec=shopsec,part_no=partno,brn_no=brn_no).update(qty_insp=str(qty_insp),inspector=str(inspector),date=str(date),remarks=str(remarks),rev_qty=str(rev_qty),rej_qty=str(rej_qty),worker=str(worker),acc_qty=str(qty_acc),rej_mat=str(mat_rej))           
            len4=request.POST.get('len4')
            
            for i in range(int(len4)+1, int(inoutnum)+1):
                in1 = request.POST.get('in1add'+str(i))
                out = request.POST.get('outadd'+str(i))
                lc_no = request.POST.get('lc_no'+str(i))
                cat = request.POST.get('catadd'+str(i))
                staff_no = request.POST.get('staff_noadd'+str(i))
                staff_name = request.POST.get('staff_nameadd'+str(i))
                ticket_no = request.POST.get('ticket_noadd'+str(i))
                month_hrs = request.POST.get('month_hrsadd'+str(i))
                total_time_taken = request.POST.get('total_time_takenadd'+str(i))
                in_date = request.POST.get('in_date'+str(i))
                out_date = request.POST.get('out_date'+str(i))
                shift = request.POST.get('shiftadd'+str(i))
                
                if len(cat)==1:
                    cat="0"+cat
                M5SHEMP1.objects.create(shopsec=shopsec,staff_no=str(staff_no),name=str(staff_name),in1=str(in1),out=str(out),month_hrs=int(month_hrs),total_time_taken=str(total_time_taken),cat=str(cat),in_date=str(in_date),out_date=str(out_date),ticket_no=int(ticket_no),shift_typename=str(shift))
            messages.success(request, 'Successfully Updated!, Select new values to update')

    return render(request,"MCARD/M5CARD/m5newview.html",context)
def m5getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(M5Docnew1.objects.filter(shop_sec = shop_sec).values('batch_no').exclude(batch_no__isnull=True).distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m5getbr(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        br_no = list(M5Docnew1.objects.filter(batch_no =wo_no,shop_sec=shop_sec).values('brn_no').exclude(brn_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

   

def m5getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        part_no = list(M5Docnew1.objects.filter(batch_no =wo_no,brn_no=br_no,shop_sec=shop_sec).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m5getdoc_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        part_no = request.GET.get('part_no')
        doc_no = list(M5Docnew1.objects.filter(batch_no =wo_no,brn_no=br_no,shop_sec=shop_sec,part_no=part_no).values('m5glsn').distinct())
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m5getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        br_no = list(M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m5getshop_name(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        shop_name = list(shop_section.objects.filter(section_code=shop_sec).values('section_desc').distinct())
        return JsonResponse(shop_name , safe = False)
    return JsonResponse({"success":False}, status=400)

def m5getempname(request):

   if request.method == "GET" and request.is_ajax():  
        examcode= request.GET.get('two')
        x =512000
        y=15719
        a = math.floor(math.log10(y))
        hello= int(x*10**(1+a)+y)
        ex = M5SHEMP.objects.filter(staff_no= examcode).all()  
        obj10= empmast.objects.filter(empno__contains=examcode).all()
        ticket=0
        if len(obj10):
            ticket=obj10[0].ticket_no
        exam ={
            "exam_type":ex[0].name,
            "ticket":ticket,
              }
        return JsonResponse({"exam":exam}, safe = False)
        return JsonResponse({"success":False}, status=400)

def m5getcat(request):
   if request.method == "GET" and request.is_ajax():  
        staff_no= request.GET.get('two')
        O=[]
        obj7=Shemp.objects.filter(staff_no=staff_no).values('cat').order_by('-updt_date')
        if len(obj7)!=0:
            O.append(obj7[0])
        return JsonResponse(O, safe = False)
        return JsonResponse({"success":False}, status=400)