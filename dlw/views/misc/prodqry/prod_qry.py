from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/prodqry/')
def prodqry(request):
    
    wo_nop = empmast.objects.none()
    tm=shop_section.objects.filter(shop_id=g.usermaster.shopno).all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)

    if "Superuser" in rolelist:
        
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
            'roles' :g.rolelist,
            'subnav':g.subnav,
        }
        
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :g.rolelist,
            'subnav':g.subnav,
        }
    return render(request,'MISC/PRODQRY/prodqry.html',context)



def sel_main(request):
    if request.method == "GET" and request.is_ajax():   
        sel_val=request.GET.get('val')
    

        if(sel_val=="11"):
            bno=request.GET.get('val1')
            pno=request.GET.get('val2')
            bono=Batch.objects.values('bo_no')
            x=[]
            for i in bono:
                x.append(i['bo_no'])
            if pno is None and bno in x:
                qry=Batch.objects.filter(bo_no=bno).values('part_no','bo_no','ep_type','loco_fr','loco_to','batch_qty','batch_type','seq','brn_no','status','so_no').order_by('bo_no','part_no','seq').distinct()
                BT=qry
                if(BT.count()>0):
                    a=''
                else:
                    BT=list(BT)
                    BT.insert(0,'B')
            else:
                qry=Batch.objects.filter(bo_no=bno,part_no=pno).values('part_no','bo_no','ep_type','loco_fr','loco_to','batch_qty','batch_type','seq','brn_no','status','so_no').order_by('bo_no','part_no','seq').distinct()
                BT=qry
                if(BT.count()>0):
                    a=''
                else:
                    BT=list(BT)
                    BT.insert(0,'BP')


        if(sel_val=="12"):
            pno=request.GET.get('val1')
            qry=Batch.objects.filter(part_no=pno).values('part_no','bo_no','ep_type','loco_fr','loco_to','batch_qty','batch_type','seq','brn_no','status','so_no').order_by('bo_no','part_no','seq').distinct()
            BT=qry
            if(BT.count()>0):
                a=''
            else:
                BT=list(BT)
                BT.insert(0,'P')

        
        if(sel_val=="13"):
            brn=request.GET.get('val1')
            qry=Batch.objects.filter(brn_no=brn).values('part_no','bo_no','ep_type','loco_fr','loco_to','batch_qty','batch_type','seq','brn_no','status','so_no').order_by('brn_no').distinct()
            BT=qry
            if(BT.count()>0):
                a=''
            else:
                BT=list(BT)
                BT.insert(0,'Brn')


        if(sel_val=="21"):
            bno=request.GET.get('val1')
            asno=request.GET.get('val2')
            if asno is not None:
                qry=M2Docnew1.objects.filter(batch_no=bno,assly_no=asno).values('scl_cl','part_no','epc','f_shopsec','qty','ptc','assly_no','rm_partno','rm_qty','rm_ptc','m4_no','brn_no','m2sln','m2prtdt','cut_shear').order_by('batch_no','assly_no','seq','scl_cl','f_shopsec','part_no').distinct()
                BT=qry
                if(BT.count()>0):
                    a=''
                else:
                    BT=list(BT)
                    BT.insert(0,'BA')
            else:
                qry=M2Docnew1.objects.filter(batch_no=bno).values('scl_cl','part_no','epc','f_shopsec','qty','ptc','assly_no','rm_partno','rm_qty','rm_ptc','m4_no','brn_no','m2sln','m2prtdt','cut_shear').order_by('batch_no','assly_no','seq','scl_cl','f_shopsec','part_no').distinct()
                BT=qry
                if(BT.count()>0):
                    a=''
                else:
                    BT=list(BT)
                    BT.insert(0,'B')


        if(sel_val=="22"):
            rcno=request.GET.get('val1')
            qry=M2Docnew1.objects.filter(m2sln=rcno).values('scl_cl','part_no','epc','f_shopsec','qty','ptc','assly_no','rm_partno','rm_qty','rm_ptc','m4_no','brn_no','m2sln','m2prtdt','cut_shear').order_by('brn_no').distinct()
            BT=qry
            if(BT.count()>0):
                a=''
            else:
                BT=list(BT)
                BT.insert(0,'RCN')
              


        if(sel_val=="23"):
            pno=request.GET.get('val1')
            bno=request.GET.get('val2')
            brn_no=0
            if bno is not None:
                qry=M2Docnew1.objects.filter(batch_no=bno).values('brn_no').order_by('batch_no','assly_no','seq','scl_cl','f_shopsec','part_no').distinct()
                

                JOIN=qry
                if(JOIN.count()>0):
                    brn_no=JOIN[0]['brn_no']
                qry=M2Docnew1.objects.filter(part_no=pno,brn_no=brn_no).values('scl_cl','part_no','epc','f_shopsec','qty','ptc','assly_no','rm_partno','rm_qty','rm_ptc','m4_no','brn_no','m2sln','m2prtdt','cut_shear').order_by('brn_no').distinct()
            else:
                qry=M2Docnew1.objects.filter(part_no=pno).values('scl_cl','part_no','epc','f_shopsec','qty','ptc','assly_no','rm_partno','rm_qty','rm_ptc','m4_no','brn_no','m2sln','m2prtdt','cut_shear').order_by('brn_no').distinct()
            BT=qry
            if pno is None:
                BT=list(BT)
                BT.insert(0,'EP')
            if(len(BT)>0):
                a=''
            else:   
                BT=list(BT)
                BT.insert(0,'BP')


        if(sel_val=="24"):
            brn=request.GET.get('val1')
            qry=M2Docnew1.objects.filter(brn_no=brn).values('scl_cl','part_no','epc','f_shopsec','qty','ptc','assly_no','rm_partno','rm_qty','rm_ptc','m4_no','brn_no','m2sln','m2prtdt','cut_shear').order_by('brn_no').distinct()
            BT=qry
            if(BT.count()>0):
                a=''
            else:
                BT=list(BT)
                BT.insert(0,'Brn')


        if(sel_val=="31"):
            bno=request.GET.get('val1')
            asno=request.GET.get('val2')
            if asno is not None:
                qry=list(M5Docnew1.objects.filter(batch_no=bno,assly_no=asno).values('scl_cl','part_no','qty_ord','assly_no','rm_partno','rm_qty','cut_shear','m5glsn','brn_no','m2slno','m5prtdt','shop_sec','lc_no','opn').order_by('batch_no','assly_no','scl_cl','shop_sec','part_no','opn','l_fr').distinct())
                for j in range(len(qry)):
                    qry[j].update({'des':None})
                BT=qry
                if(len(BT)>0):
                    for i in range(len(BT)):
                        part=BT[i]['part_no']
                        qry=Oprn.objects.filter(part_no=part).values('des').order_by('part_no','opn').distinct()
                        OP=qry
                        if(OP.count()>0):
                            BT[i]['des']=OP[0]['des'][0:37]
                else:
                    BT=list(BT)
                    BT.insert(0,'BA')
            else:
                qry=list(M5Docnew1.objects.filter(batch_no=bno).values('scl_cl','part_no','qty_ord','assly_no','rm_partno','rm_qty','cut_shear','m5glsn','brn_no','m2slno','m5prtdt','shop_sec','lc_no','opn').order_by('batch_no','assly_no','scl_cl','shop_sec','part_no','opn','l_fr').distinct())
                for j in range(len(qry)):
                    qry[j].update({'des':None})
                BT=qry
                if(len(BT)>0):
                    for i in range(len(BT)):
                        part=BT[i]['part_no']
                        qry=Oprn.objects.filter(part_no=part).values('des').order_by('part_no','opn').distinct()
                        OP=qry
                        if(OP.count()>0):
                            BT[i]['des']=OP[0]['des'][0:37]
                else:
                    BT=list(BT)
                    BT.insert(0,'B')




        
        if(sel_val=="32"):
            rcn=request.GET.get('val1')
            batchno=''
            if rcn is not None:
                qry=M2Docnew1.objects.filter(m2sln=rcn).values('batch_no').order_by('m2sln').distinct()
                DOC=qry
                if(DOC.count()>0):
                    batchno=DOC[0]['batch_no']

                oprn_sub=Oprn.objects.all().distinct()
                qry=M5Docnew1.objects.filter(batch_no=batchno,opn__in=Subquery(oprn_sub.values('opn')),part_no__in=Subquery(oprn_sub.values('part_no'))).values('scl_cl', 'part_no', 'batch_no', 'qty_ord', 'assly_no', 'rm_partno', 'rm_qty', 'cut_shear', 'm5glsn', 'brn_no', 'm2slno', 'm5prtdt', 'shop_sec', 'lc_no', 'opn_desc').order_by('batch_no','assly_no','scl_cl','shop_sec','part_no','opn','l_fr').distinct()
                BT=qry
                if(BT.count()>0):
                    a=''
                else:
                    BT=list(BT)
                    BT.insert(0,'RCN')
                
        
        if(sel_val=="33"):
            jcn=request.GET.get('val1')
            print(jcn)
            oprn_sub=Oprn.objects.all().distinct()
            qry=M5Docnew1.objects.filter(m5glsn=jcn,opn__in=Subquery(oprn_sub.values('opn')),part_no__in=Subquery(oprn_sub.values('part_no'))).values('scl_cl', 'part_no', 'batch_no', 'qty_ord', 'assly_no', 'rm_partno', 'rm_qty', 'cut_shear', 'm5glsn', 'brn_no', 'm2slno', 'm5prtdt', 'shop_sec', 'lc_no', 'opn_desc').order_by('m5glsn').distinct()
            BT=qry
            if(BT.count()>0):
                a=''
            else:
                BT=list(BT)
                BT.insert(0,'JCN')

       

        if(sel_val=="34"):
            pno=request.GET.get('val1')
            bno=request.GET.get('val2')
            if pno is None:
                print("Enter Part Number")
            if bno is not None:
                qry=M5Docnew1.objects.filter(batch_no=bno).values('brn_no').order_by('batch_no','assly_no','scl_cl','shop_sec','part_no','opn','l_fr').distinct()
                JOIN=qry
                brnno=''
                if(JOIN.count()>0):
                    brnno=JOIN[0]['brn_no']
                oprn_sub=Oprn.objects.all().distinct()
                qry=M5Docnew1.objects.filter(part_no=pno,brn_no=brnno,opn__in=Subquery(oprn_sub.values('opn')),part_no__in=Subquery(oprn_sub.values('part_no'))).values('scl_cl', 'part_no', 'batch_no', 'qty_ord', 'assly_no', 'rm_partno', 'rm_qty', 'cut_shear', 'm5glsn', 'brn_no', 'm2slno', 'm5prtdt', 'shop_sec', 'lc_no', 'opn_desc').order_by('part_no','brn_no','scl_cl').distinct()
            else:
                oprn_sub=Oprn.objects.all().distinct()
                qry=M5Docnew1.objects.filter(part_no=pno,opn__in=Subquery(oprn_sub.values('opn')),part_no__in=Subquery(oprn_sub.values('part_no'))).values('scl_cl', 'part_no', 'batch_no', 'qty_ord', 'assly_no', 'rm_partno', 'rm_qty', 'cut_shear', 'm5glsn', 'brn_no', 'm2slno', 'm5prtdt', 'shop_sec', 'lc_no', 'opn_desc').order_by('part_no','brn_no','scl_cl').distinct()
            BT=qry
            if(BT.count()>0):
                a=''
            else:
                BT=list(BT)
                BT.insert(0,'BP')
            


        if(sel_val=="35"):
            brno=request.GET.get('val1')
            if brno is not None:
                qry=list(M5Docnew1.objects.filter(brn_no=brno).values('scl_cl','part_no','qty_ord','assly_no','rm_partno','rm_qty','cut_shear','m5glsn','batch_no','m2slno','m5prtdt','shop_sec','lc_no','opn').order_by('m5glsn').distinct())
                for j in range(len(qry)):
                    qry[j].update({'des':None})
                BT=qry
                if(len(BT)>0):
                    for i in range(len(BT)):
                        part=BT[i]['part_no']
                        qry=Oprn.objects.filter(part_no=part).values('des').order_by('part_no','opn')
                        OP=qry
                        if(OP.count()>0):
                            if(len(OP[0]['des'])>=37):
                                BT[i]['des']=OP[0]['des'][0:37]
                            else:
                               BT[i]['des']=OP[0]['des'] 
                else:
                    BT=list(BT)
                    BT.insert(0,'Brn')


        if(sel_val=="41"):
            bno=request.GET.get('val1')
            pno=request.GET.get('val2')
            brn_no=0
            if pno is None:
                print("Enter Part Number")
            if bno is not None:
                qry=Batch.objects.filter(bo_no=bno).values('brn_no').order_by('bo_no','part_no','seq').distinct()
                JOIN=qry
                if(JOIN.count()>0):
                    brn_no=JOIN[0]['brn_no']
                qry=M14M4new1.objects.filter(part_no=pno,brn_no=brn_no).values('part_no','bo_no','pm_no','qty','l_fr','l_to','assly_no','brn_no','doc_no').order_by('doc_no').distinct()
            else:
                qry=M14M4new1.objects.filter(part_no=pno).values('part_no','bo_no','pm_no','qty','l_fr','l_to','assly_no','brn_no','doc_no').order_by('l_fr').distinct()
            BT=qry
            if(BT.count()>0):
                a=''
            else:        
                BT=list(BT)
                BT.insert(0,'BP')


        if(sel_val=="42"):
            brno=request.GET.get('val1')
            qry=M14M4new1.objects.filter(brn_no=brno,doc_code='89').values('part_no','bo_no','pm_no','qty','l_fr','l_to','assly_no','brn_no','doc_no').order_by('brn_no','assly_no','kit_ind','station','stg','sub_kit','part_no').distinct()
            BT=qry
            if(BT.count()>0):
                a=''
            else:   
                BT=list(BT)
                BT.insert(0,'Brn')



        if(sel_val=="71"):
            bno=request.GET.get('val1')
            pno=request.GET.get('val2')
            qry=Batch.objects.filter(bo_no=bno).values('brn_no').order_by('bo_no','part_no','seq').distinct()
            JOIN=qry
            
            if((bno is not None) and (JOIN.count()>0)):
                sub=Batch.objects.values('brn_no').distinct()
                qry=Altdoc.objects.filter(part_no=pno,brn_no__in=Subquery(sub.values('brn_no'))).values('brn_no', 'part_no', 'l_fr', 'l_to', 'm2_fr', 'm2_to', 'm5_fr', 'm5_to', 'm14_fr', 'm14_to','m4_fr', 'm4_to','expl_dt','prt_dt').order_by('brn_no','alt_link','l_fr','l_to').distinct()
            else:
                sub=Batch.objects.all().distinct()
                qry=Altdoc.objects.filter(part_no=pno,brn_no__in=Subquery(sub.values('brn_no'))).values('brn_no', 'part_no', 'l_fr', 'l_to', 'm2_fr', 'm2_to', 'm5_fr', 'm5_to', 'm14_fr', 'm14_to','m4_fr', 'm4_to','expl_dt','prt_dt').order_by('brn_no','alt_link','l_fr','l_to').distinct()
            BT=qry
            if(BT.count()>0):
                a=''
            else:
                BT=list(BT)
                BT.insert(0,'BrP')
        return JsonResponse(list(BT), safe = False)
    return JsonResponse({"success":False}, status=400)
