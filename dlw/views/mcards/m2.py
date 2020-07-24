from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m2view/')
def m2view(request):
        context={}

        wo_nop = empmast.objects.none()
    
        tm2=Batch.objects.filter(status='R').values('bo_no').distinct().order_by('bo_no')
        tm2=list(M2Docnew1.objects.filter(batch_no__in=tm2).values('batch_no').distinct().order_by('batch_no'))
        tmp2=[]
        for on in tm2:
            tmp2.append(on['batch_no'])   
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'work_no':tmp2,
            'usermaster':g.usermaster,
        }  
        if request.method == "POST":
            submitvalue = request.POST.get('proceed')
            if submitvalue=='Save':
                
                leng=request.POST.get('hidtxt')
                work=request.POST.get('work')
                shopsec= request.POST.get('shop_no1')
                partno= request.POST.get('part_no1')
                obj=m2_transaction11.objects.filter(work_order=work,shop_sec=shopsec, part_no=partno).distinct()
                if len(obj)==0:
                    for i in range(1, int(leng)+1):
                        qtypr=request.POST.get('qty_p'+str(i))
                        qtyac = request.POST.get('qty_acc'+str(i))
                        wrrej = request.POST.get('w_rej'+str(i))
                        matrej =request.POST.get('m_rej'+str(i))
                        opn=request.POST.get('onumber'+str(i))
                        ins=request.POST.get('inspect'+str(i))
                        m2_transaction11.objects.create(work_order=str(work),shop_sec=str(shopsec),part_no=str(partno),opn_no=str(opn),qty_prod=str(qtypr), qty_accep=str(qtyac), work_rej=str(wrrej), mat_rej=str(matrej),inspect_id=str(ins))
                else:
                    for i in range(1, int(leng)+1):
                        qtypr=request.POST.get('qty_p'+str(i))
                        qtyac =request.POST.get('qty_acc'+str(i))
                        wrrej =request.POST.get('w_rej'+str(i))
                        matrej =request.POST.get('m_rej'+str(i))
                        opn=request.POST.get('onumber'+str(i))
                        ins=request.POST.get('inspect'+str(i))
                        m2_transaction11.objects.filter(work_order=work,shop_sec=shopsec, part_no=partno, opn_no=opn).update(qty_prod=str(qtypr), qty_accep=str(qtyac), work_rej=str(wrrej), mat_rej=str(matrej),inspect_id=ins)
        return render(request, "MCARD/M2CARD/m2view.html", context)


def m2_view_shop(request):
    obj=[]
    if request.method == "GET" and request.is_ajax():
        work_no = request.GET.get('work')
        shop_no1=request.GET.get('shop_no1')
        obj=list(M2Docnew1.objects.filter(batch_no=work_no,f_shopsec=shop_no1).values('part_no').distinct())
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)

def m2_process_sheet(request):
    l=[]
    if request.method == "GET" and request.is_ajax():
        part_no = request.GET.get('part_no')
        obj1=list(Oprn.objects.filter(part_no=part_no).values('opn', 'shop_sec', 'lc_no', 'des','pa','at','ncp_jbs',).order_by('shop_sec','opn'))
        obj2=list(Nstr.objects.filter(pp_part=part_no).values('pp_part','epc','ptc','cp_part').distinct())
        l.append(obj1)
        l.append(obj2)
        return JsonResponse(l, safe = False)
    return JsonResponse({"success":False}, status=400)

def m2_sheet1(request):
    if request.method == "GET" and request.is_ajax():
        l=[]
        brn_no=0
        assembly_no=0
        doc_no=0
        rm_partno=0
        shop_unit=0
        opn_no=0
        l2=[]
        obj12=[]
        l3=[]
        shop_sec = request.GET.get('shop_no1')
        part_no = request.GET.get('part_no')
        wo_no = request.GET.get('work')
        
        kkk=Oprn.objects.all()
        obj=list(M2Docnew1.objects.filter(batch_no=wo_no).values('m2sln','brn_no','assly_no','scl_cl','rm_partno','m4_no','rc_st_wk').distinct())

        if len(obj):
            brn_no=obj[0]['brn_no']
            assembly_no=obj[0]['assly_no']
            doc_no=obj[0]['m2sln']
            rm_partno=obj[0]['rm_partno']
        if len(obj)==0:
            obj=[{'m2sln':"",'brn_no':'','assly_no':'','scl_cl':'','rm_partno':'','m4_no':'','rc_st_wk':''}]
        obj1=list(Part.objects.filter(partno=part_no).values('des','drgno').distinct())
        if len(obj1)==0:
            obj1=[{'des':'','drgno':''}]
        obj2=list(Part.objects.filter(partno=assembly_no).values('des').distinct())
        if len(obj2)==0:
            obj2=[{'des':''}]
        obj3=list(Batch.objects.filter(bo_no=wo_no,brn_no=brn_no,part_no=assembly_no).values('batch_type'))
        if len(obj3)==0:
            obj3=[{'batch_type':''}]
        obj4= list(Oprn.objects.filter(part_no=part_no,shop_sec=shop_sec).values('opn', 'shop_sec', 'lc_no', 'des','pa','at','lot').order_by('opn'))
        for i in range(1, int(len(obj4))+1):
            opn_no=obj4[i-1]['opn']
            l2.append(opn_no)
        if len(obj4)==0:
            obj4=[{'opn':'', 'shop_sec':'', 'lc_no':'', 'des':'','pa':'','at':'','lot':''}]
     
        obj5 = list(M2Docnew1.objects.filter(batch_no=wo_no).values('m2prtdt','qty').distinct())
        if len(obj5)==0:
            obj5=[{'m2prtdt':'','qty':""}]
        now =obj5[0]['m2prtdt']
        date_string = now
        obj5[0]['m2prtdt']=date_string
        obj6=list(Batch.objects.filter(bo_no=wo_no).values('loco_fr','loco_to').distinct())
        obj7=list(Part.objects.filter(partno=rm_partno).values('des').distinct())
        obj8=list(M2Docnew1.objects.filter(rm_partno=rm_partno).values('rm_qty').distinct())
        obj9=list(Part.objects.filter(partno=part_no).values('shop_ut').distinct())
        if len(obj9):
            shop_unit=obj9[0]['shop_ut']
        if len(obj6)==0:
            
            obj6=[{'loco_fr':'','loco_to':''}]
        if len(obj7)==0:
            obj7=[{'des':''}]  
        if len(obj8)==0:
            obj8=[{'rm_qty':''}]  
        if len(obj9)==0:
            obj9=[{'shop_ut':''}]
        obj10=list(Code.objects.filter(cd_type='51',code=shop_unit).values('alpha_1').distinct()) 
        
        if len(obj10)==0:
            obj10=[{'alpha_1':''}]  
        obj11=list(Cutdia.objects.filter(ep_part=part_no,rm_part=rm_partno).values('cutdia_no').distinct())    
        
        if len(obj11)==0:
            obj11=[{'cutdia_no':''}]
        for i in range(1,len(l2)+1):

            l3=list(m2_transaction11.objects.filter(work_order=wo_no,opn_no=l2[i-1]).values('qty_prod','qty_accep','work_rej','mat_rej','inspect_id').distinct())
            if len(l3)==0:
                l3=[{'qty_prod':'','qty_accep':'','work_rej':'','mat_rej':'','inspect_id':''}]
            obj12.append(l3)
        l.append(obj)
        l.append(obj1)
        l.append(obj2)
        l.append(obj3)
        l.append(obj4)
        l.append(obj5)
        l.append(obj6)
        l.append(obj7)
        l.append(obj8)
        l.append(obj9)
        l.append(obj10)
        l.append(obj11)
        l.append(obj12)
        return JsonResponse(l, safe = False)
    return JsonResponse({"success":False}, status=400)    

def m2_shop(request):
    if request.method == "GET" and request.is_ajax():
        
        work=request.GET.get('work')
        obj=list(M2Docnew1.objects.filter(batch_no=str(work)).values('f_shopsec').distinct())
        
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)

def m2_getname(request):
    if request.method =="GET" and request.is_ajax():
        ins_id=request.GET.get('ins_id')
        for i in (empmast.objects.annotate(emp=Substr("empno",7,5)).filter(emp=ins_id).values('empname').distinct()):
            break
        obj=i['empname']
        if len(obj)==0:
            obj=[]
        return JsonResponse(obj, safe=False)
    return JsonResponse({"success":False}, status=400)   

def m2Pdf(request, *args, **kwargs):
    l=[]
    brn_no=0
    assembly_no=0
    doc_no=0
    rm_partno=0
    shop_unit=0
    opn_no=0
    l2=[]
    obj12=[]
    l3=[]
    m4_no=0
    scl_cl=0
    rc_st_wk=0
    rm_qty=0
    alpha_1=0
    cutdia_no=0
    date_string=0
    l_to=0
    l_fr=0
    des1=0
    drgno=0
    shop_sec = request.GET.get('shop_no1')
    part_no = request.GET.get('part_no1')
    wo_no = request.GET.get('work')
    obj=list(M2Docnew1.objects.filter(batch_no=wo_no).values('m2sln','brn_no','assly_no','scl_cl','rm_partno','m4_no','rc_st_wk').distinct())

    if len(obj):
        brn_no=obj[0]['brn_no']
        assembly_no=obj[0]['assly_no']
        doc_no=obj[0]['m2sln']
        rm_partno=obj[0]['rm_partno']
        scl_cl=obj[0]['scl_cl']
        m4_no=obj[0]['m4_no']
        rc_st_wk=obj[0]['rc_st_wk']
    obj1=list(Part.objects.filter(partno=part_no).values('des','drgno').distinct())  
    obj2=list(Part.objects.filter(partno=assembly_no).values('des').distinct())
    obj3=list(Batch.objects.filter(bo_no=wo_no,brn_no=brn_no,part_no=assembly_no).values('batch_type'))
    obj4= list(Oprn.objects.filter(part_no=part_no,shop_sec=shop_sec).values('opn', 'shop_sec', 'lc_no', 'des','pa','at','lot').order_by('opn'))
    if len(obj1):
        des1=obj1[0]['des']
        drgno=obj1[0]['drgno']
    for i in range(1, int(len(obj4))+1):
        opn_no=obj4[i-1]['opn']
        l2.append(opn_no)
    
    obj5 = list(M2Docnew1.objects.filter(batch_no=wo_no).values('m2prtdt','qty').distinct())
    
    now =obj5[0]['m2prtdt']
    qty =obj5[0]['qty']
    date_string = now
    obj5[0]['m2prtdt']=date_string
    obj6=list(Proddem.objects.filter(part_no=part_no).values('l_fr','l_to').distinct())
    if len(obj6):
        l_to=obj6[0]['l_to']
        l_fr=obj6[0]['l_fr']
    obj7=list(Part.objects.filter(partno=rm_partno).values('des').distinct())
    obj8=list(M2Docnew1.objects.filter(rm_partno=rm_partno).values('rm_qty').distinct())
    if len(obj8):
        rm_qty=obj8[0]['rm_qty']

    obj9=list(Part.objects.filter(partno=part_no).values('shop_ut').distinct())
    
    obj10=list(Code.objects.filter(cd_type='51',code=shop_unit).values('alpha_1').distinct())
    if len(obj10):
        alpha_1=obj10[0]['alpha_1'] 
    if len(obj9):
            shop_unit=obj9[0]['shop_ut']
    if len(obj6)==0:    
        obj6=[{'l_fr':'','l_to':''}]
    if len(obj7)==0:
        obj7=[{'des':''}]  
    if len(obj8)==0:
        obj8=[{'rm_qty':''}]  
    if len(obj9)==0:
        obj9=[{'shop_ut':''}]  
    obj11=list(Cutdia.objects.filter(ep_part=part_no,rm_part=rm_partno).values('cutdia_no').distinct())    
    if len(obj11):
        cutdia_no=obj11[0]['cutdia_no']
    for i in range(1,len(l2)+1):
        l3=list(m2_transaction11.objects.filter(work_order=wo_no,opn_no=l2[i-1]).values('qty_prod','qty_accep','work_rej','mat_rej','inspect_id').distinct())
        if len(l3)==0:
            l3=[{'qty_prod':'','qty_accep':'','work_rej':'','mat_rej':'','inspect_id':''}]
        obj12.append(l3)
    for i in range(0,int(len(obj4))):
        obj4[i].update({'qty_prod':obj12[i][0]['qty_prod'],'qty_accep':obj12[i][0]['qty_accep'],'work_rej':obj12[i][0]['work_rej'],'mat_rej':obj12[i][0]['mat_rej'],'inspect_id':obj12[i][0]['inspect_id']})
    pdfcontext={
        'des1':des1,
        'drgno':drgno,
        'l_to':l_to,
        'qty':qty,
        'l_fr':l_fr,
        'shop_unit':shop_unit,
        'date_string':date_string,
        'cutdia_no':cutdia_no,
        'alpha_1':alpha_1,
        'rm_qty':rm_qty,
        'm4_no':m4_no,
        'scl_cl':scl_cl,
        'rc_st_wk':rc_st_wk,
        'brn_no':brn_no,
        'assembly_no':assembly_no,
        'doc_no':doc_no,
        'rm_partno':rm_partno,
        'shop_unit':shop_unit,
        'wo_no':wo_no,
        'part_no':part_no,
        'shop_sec':shop_sec,
        'obj':obj,
        'obj1':obj1,
        'obj2':obj2,
        'obj3':obj3,
        'obj4':obj4,
        'obj5':obj5,
        'obj6':obj6,
        'obj7':obj7,
        'obj8':obj8,
        'obj9':obj9,
        'obj10':obj10,
        'obj11':obj11,
        'obj12':obj12
    }  
    pdf = render_to_pdf('MCARD/M2CARD/m2report.html',pdfcontext)
    return HttpResponse(pdf, content_type='application/pdf')


