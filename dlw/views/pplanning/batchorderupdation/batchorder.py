from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/batchorderupd/')
def batchorderupd(request):     
    tm=shop_section.objects.all()
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
    return render(request,'PPRODUCTION/BATCHORDERUPDATION/batchorderupd.html',context)

def v_bo(request):
    if request.method == "GET" and request.is_ajax():   
        bno=request.GET.get('val1')
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        seq=request.GET.get('val4')
        brno=request.GET.get('val5')
        ver=request.GET.get('val6')
        lfr=request.GET.get('val7')
        lto=request.GET.get('val8')
        btype=request.GET.get('val9')
        bqty=request.GET.get('val10')
        expldt=request.GET.get('val11')
        reldt=request.GET.get('val12')
        closedt=request.GET.get('val13')
        duewk=request.GET.get('val14')
        ptc=request.GET.get('val15')
        des=request.GET.get('val16')
        id=0        
         
        if(bno==""): 
            pass           
        SrchQry = Batch.objects.filter(bo_no=bno).values('id','bo_no','part_no','ep_type','seq','brn_no','version','loco_fr','loco_to','batch_type','batch_qty','status','uot_wk_f','b_expl_dt','rel_date','b_close_dt').order_by('id').distinct()
        Bo=SrchQry
        if(Bo.count()>0):
            bno=Bo[0]['bo_no']
            pno=Bo[0]['part_no']
            epc=Bo[0]['ep_type']
            seq=Bo[0]['seq']
            brno=Bo[0]['brn_no']
            ver=Bo[0]['version']
            lfr=Bo[0]['loco_fr']
            lto=Bo[0]['loco_to']
            btype=Bo[0]['batch_type']
            bqty=Bo[0]['batch_qty']
            expldt=Bo[0]['b_expl_dt']
            reldt=Bo[0]['rel_date']
            closedt=Bo[0]['b_close_dt']
            duewk=Bo[0]['uot_wk_f']
            id=Bo[0]['id'] 
            SrchQry=Part.objects.filter(partno=pno).values('ptc','des').order_by('partno').distinct()
            PT=SrchQry
            if(PT.count()>0):
                ptc=PT[0]['ptc']
                des=PT[0]['des']
            lst=[bno,pno,epc,seq,brno,ver,lfr,lto,btype,bqty,expldt,reldt,closedt,duewk,ptc,des,id]
        else:
            lst=[bno]         
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)


def v_pt(request):
    if request.method == "GET" and request.is_ajax():   
        bno=request.GET.get('val1')
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        seq=request.GET.get('val4')
        brno=request.GET.get('val5')
        ver=request.GET.get('val6')
        lfr=request.GET.get('val7')
        lto=request.GET.get('val8')
        btype=request.GET.get('val9')
        bqty=request.GET.get('val10')
        expldt=request.GET.get('val11')
        reldt=request.GET.get('val12')
        closedt=request.GET.get('val13')
        duewk=request.GET.get('val14')
        ptc=request.GET.get('val15')
        des=request.GET.get('val16')
        FB=request.GET.get('val17')
        B_UPDT_DT=request.GET.get('val18')
        REL_DT_BC=request.GET.get('val19')
        CLOS_DT_B=request.GET.get('val20')
        CLOS_DT_C=request.GET.get('val21')
        CLOSE_NO=request.GET.get('val22')
        MARK=request.GET.get('val23')
        REMARK=request.GET.get('val24')
        if seq=='':
            seq=0
        print(FB)
        id=0
        print(bno)
        if(pno==""):
            print("Enter Part Number")
        
        SrchQry=Part.objects.filter(partno=pno).values('ptc','des').order_by('partno').distinct()
        PT=SrchQry
        if(PT.count()>0):
            ptc=PT[0]['ptc']
            des=PT[0]['des']
        else:
            print("No Such Part No")

        if bno!='':
            FB=bno[:2]
        else:
            FB=''


        SrchQry=Batch.objects.filter(bo_no=bno,part_no=pno,seq=seq).values('id','bo_no','part_no','ep_type','seq','brn_no','version','loco_fr','loco_to','batch_type','batch_qty','status','uot_wk_f','b_expl_dt','rel_date','b_close_dt','b_updt_dt','rel_dt_bc','clos_dt_b','clos_dt_c','close_no','mark','remark').order_by('id').distinct()
        Bo=SrchQry
        if(Bo.count()>0):
            bno=Bo[0]['bo_no']
            pno=Bo[0]['part_no']
            epc=Bo[0]['ep_type']
            seq=Bo[0]['seq']
            brno=Bo[0]['brn_no']
            ver=Bo[0]['version']
            lfr=Bo[0]['loco_fr']
            lto=Bo[0]['loco_to']
            btype=Bo[0]['batch_type']
            bqty=Bo[0]['batch_qty']
            expldt=Bo[0]['b_expl_dt']
            reldt=Bo[0]['rel_date']
            closedt=Bo[0]['b_close_dt']
            duewk=Bo[0]['uot_wk_f']
            B_UPDT_DT=Bo[0]['b_updt_dt']
            REL_DT_BC=Bo[0]['rel_dt_bc']
            CLOS_DT_B=Bo[0]['clos_dt_b']
            CLOS_DT_C=Bo[0]['clos_dt_c']
            CLOSE_NO=Bo[0]['close_no']
            MARK=Bo[0]['mark']
            REMARK=Bo[0]['remark']
            id=Bo[0]['id']
        else:
            brno=''
            lfr=''
            lto=''
            btype=''
            bqty=''
            expldt=''
            reldt=''
            closedt=''
            duewk=''
            B_UPDT_DT=''
            REL_DT_BC=''
            CLOS_DT_B=''
            CLOS_DT_C=''
            CLOSE_NO=''
            MARK=''
            REMARK=''
            
            
        lst=[bno,pno,epc,seq,brno,ver,lfr,lto,btype,bqty,expldt,reldt,closedt,duewk,ptc,des,id,B_UPDT_DT,REL_DT_BC,CLOS_DT_B,CLOS_DT_C,CLOSE_NO,MARK,REMARK]
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)


def v_seq(request):
    if request.method == "GET" and request.is_ajax():   
        bno=request.GET.get('val1')
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        seq=request.GET.get('val4')
        brno=request.GET.get('val5')
        ver=request.GET.get('val6')
        lfr=request.GET.get('val7')
        lto=request.GET.get('val8')
        btype=request.GET.get('val9')
        bqty=request.GET.get('val10')
        expldt=request.GET.get('val11')
        reldt=request.GET.get('val12')
        closedt=request.GET.get('val13')
        duewk=request.GET.get('val14')
        ptc=request.GET.get('val15')
        des=request.GET.get('val16')
        B_UPDT_DT=request.GET.get('val18')
        REL_DT_BC=request.GET.get('val19')
        CLOS_DT_B=request.GET.get('val20')
        CLOS_DT_C=request.GET.get('val21')
        CLOSE_NO=request.GET.get('val22')
        MARK=request.GET.get('val23')
        REMARK=request.GET.get('val24')
        id=0
    

        SrchQry=Batch.objects.filter(bo_no=bno,part_no=pno,seq=seq).values('id','bo_no','part_no','ep_type','seq','brn_no','version','loco_fr','loco_to','batch_type','batch_qty','status','uot_wk_f','b_expl_dt','rel_date','b_close_dt','b_updt_dt','rel_dt_bc','clos_dt_b','clos_dt_c','close_no','mark','remark').order_by('id').distinct()
        Bo=SrchQry
        if(Bo.count()>0):
            bno=Bo[0]['bo_no']
            pno=Bo[0]['part_no']
            epc=Bo[0]['ep_type']
            seq=Bo[0]['seq']
            brno=Bo[0]['brn_no']
            ver=Bo[0]['version']
            lfr=Bo[0]['loco_fr']
            lto=Bo[0]['loco_to']
            btype=Bo[0]['batch_type']
            bqty=Bo[0]['batch_qty']
            expldt=Bo[0]['b_expl_dt']
            reldt=Bo[0]['rel_date']
            closedt=Bo[0]['b_close_dt']
            duewk=Bo[0]['uot_wk_f']
            B_UPDT_DT=Bo[0]['b_updt_dt']
            REL_DT_BC=Bo[0]['rel_dt_bc']
            CLOS_DT_B=Bo[0]['clos_dt_b']
            CLOS_DT_C=Bo[0]['clos_dt_c']
            CLOSE_NO=Bo[0]['close_no']
            MARK=Bo[0]['mark']
            REMARK=Bo[0]['remark']
            id=Bo[0]['id']
        else:
            brno=''
            lfr=''
            lto=''
            btype=''
            bqty=''
            expldt=''
            reldt=''
            closedt=''
            duewk=''
            B_UPDT_DT=''
            REL_DT_BC=''
            CLOS_DT_B=''
            CLOS_DT_C=''
            CLOSE_NO=''
            MARK=''
            REMARK=''
            
            
        lst=[bno,pno,epc,seq,brno,ver,lfr,lto,btype,bqty,expldt,reldt,closedt,duewk,ptc,des,id,B_UPDT_DT,REL_DT_BC,CLOS_DT_B,CLOS_DT_C,CLOSE_NO,MARK,REMARK]
       
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)

def next(request):
    if request.method == "GET" and request.is_ajax():
        ptc=0
        des=0
        id1=request.GET.get('x')
        if id1==0:
           c=0 
        else:
            SrchQry=Batch.objects.filter(id=int(id1)+1).values('id','bo_no','part_no','ep_type','seq','brn_no','version','loco_fr','loco_to','batch_type','batch_qty','status','uot_wk_f','b_expl_dt','rel_date','b_close_dt').order_by('id')
            Bo=SrchQry
            if(Bo.count()>0):
                c=1
                bno=Bo[0]['bo_no']
                pno=Bo[0]['part_no']
                epc=Bo[0]['ep_type']
                seq=Bo[0]['seq']
                brno=Bo[0]['brn_no']
                ver=Bo[0]['version']
                lfr=Bo[0]['loco_fr']
                lto=Bo[0]['loco_to']
                btype=Bo[0]['batch_type']
                bqty=Bo[0]['batch_qty']
                expldt=Bo[0]['b_expl_dt']
                reldt=Bo[0]['rel_date']
                closedt=Bo[0]['b_close_dt']
                duewk=Bo[0]['uot_wk_f']
                id=Bo[0]['id']
            
                SrchQry=Part.objects.filter(partno=pno).values('ptc','des').order_by('partno').distinct()
                PT=SrchQry
                if(PT.count()>0):
                    ptc=PT[0]['ptc']
                    des=PT[0]['des']
            else:
                c=0
                bno=0
                pno=0
                epc=0
                seq=0
                brno=0
                ver=0
                lfr=0
                lto=0
                btype=0
                bqty=0
                expldt=0
                reldt=0
                closedt=0
                duewk=0
                id=id1
                ptc=0
                des=0
        lst=[bno,pno,epc,seq,brno,ver,lfr,lto,btype,bqty,expldt,reldt,closedt,duewk,ptc,des,id,c]
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)


def Prev(request):
    if request.method == "GET" and request.is_ajax():
        ptc=0
        des=0
        id1=request.GET.get('x')
        if id1==0:
           c=0 
        else:
            SrchQry=Batch.objects.filter(id=int(id1)-1).values('id','bo_no','part_no','ep_type','seq','brn_no','version','loco_fr','loco_to','batch_type','batch_qty','status','uot_wk_f','b_expl_dt','rel_date','b_close_dt').order_by('id')
            Bo=SrchQry
            if(Bo.count()>0):
                c=1
                bno=Bo[0]['bo_no']
                pno=Bo[0]['part_no']
                epc=Bo[0]['ep_type']
                seq=Bo[0]['seq']
                brno=Bo[0]['brn_no']
                ver=Bo[0]['version']
                lfr=Bo[0]['loco_fr']
                lto=Bo[0]['loco_to']
                btype=Bo[0]['batch_type']
                bqty=Bo[0]['batch_qty']
                expldt=Bo[0]['b_expl_dt']
                reldt=Bo[0]['rel_date']
                closedt=Bo[0]['b_close_dt']
                duewk=Bo[0]['uot_wk_f']
                id=Bo[0]['id']
               
                SrchQry=Part.objects.filter(partno=pno).values('ptc','des').order_by('partno').distinct()
                PT=SrchQry
                if(PT.count()>0):
                    ptc=PT[0]['ptc']
                    des=PT[0]['des']
            else:
                c=0
                bno=0
                pno=0
                epc=0
                seq=0
                brno=0
                ver=0
                lfr=0
                lto=0
                btype=0
                bqty=0
                expldt=0
                reldt=0
                closedt=0
                duewk=0
                id=id1
                ptc=0
                des=0
        lst=[bno,pno,epc,seq,brno,ver,lfr,lto,btype,bqty,expldt,reldt,closedt,duewk,ptc,des,id,c]
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400) 

def save(request):
    if request.method == "GET" and request.is_ajax():
        bno=request.GET.get('val1')
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        seq=request.GET.get('val4')
        brno=request.GET.get('val5')
        ver=request.GET.get('val6')
        lfr=request.GET.get('val7')
        lto=request.GET.get('val8')
        btype=request.GET.get('val9')
        bqty=request.GET.get('val10')
        expldt=request.GET.get('val11')
        reldt=request.GET.get('val12')
        closedt=request.GET.get('val13')
        duewk=request.GET.get('val14')
        ptc=request.GET.get('val15')
        des=request.GET.get('val16')
        x=request.GET.get('x')
        y=request.GET.get('y')
        if y=='0':
            Batch.objects.create(bo_no=str(bno), part_no=str(pno), ep_type=str(epc), seq=str(seq), brn_no=str(brno), version=str(ver), loco_fr=str(lfr), loco_to=str(lto), batch_type=str(btype), batch_qty=str(bqty), b_expl_dt=str(expldt), rel_date=str(reldt), b_close_dt=str(closedt), uot_wk_f=str(duewk))
        else:
            Batch.objects.filter(id=x).update(bo_no=str(bno), part_no=str(pno), ep_type=str(epc), seq=str(seq), brn_no=str(brno), version=str(ver), loco_fr=str(lfr), loco_to=str(lto), batch_type=str(btype), batch_qty=str(bqty), uot_wk_f=str(duewk))    
        return JsonResponse(1, safe = False)
    return JsonResponse({"success":False}, status=400)

def key_f6(request):
    if request.method == "GET" and request.is_ajax():
        epc=request.GET.get('val3')
        ptc=request.GET.get('val15')
        des=request.GET.get('val16')
        LblDem_regno=request.GET.get('val27')
        Lblslno=request.GET.get('val28')
        Lbldoc_type=request.GET.get('val29')
        des=''
        ptc=''
        epc=''
        LblDem_regno=''
        Lblslno=''
        Lbldoc_type=''
        r=True
        msg=''
        lst=[]
        totdem=0
        SrchQry = Proddem.objects.filter(status='C',del_fl__isnull=True).values('dem_regno','slno','part_no','epc','qty','bo_no','batch_type','l_fr','l_to','seq','ddoc_type','staff_no','name').order_by('staff_no','dem_regno','slno').distinct() 
        DEM=SrchQry
        print(DEM)
        if DEM.count()>0:
            totdem=DEM.count()
        else:
            msg="No Pending Demands"
            r=False
        lst=[r,msg,totdem]
        lst.append(list(DEM))
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)











def Grid_part_RowCommand(request):
    if request.method == "GET" and request.is_ajax():
        bno=request.GET.get('val1')
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        seq=request.GET.get('val4')
        brno=request.GET.get('val5')
        ver=request.GET.get('val6')
        lfr=request.GET.get('val7')
        lto=request.GET.get('val8')
        btype=request.GET.get('val9')
        bqty=request.GET.get('val10')
        expldt=request.GET.get('val11')
        reldt=request.GET.get('val12')
        closedt=request.GET.get('val13')
        duewk=request.GET.get('val14')
        ptc=request.GET.get('val15')
        des=request.GET.get('val16')
        staffno=request.GET.get('val30')
        slno=request.GET.get('val28')
        dem_regno=request.GET.get('val27')
        NAME=''
        Lblpartno=''
        Lblbo_no=''
        Lblepc=''
        Lblqty=''
        Lblbatch_type=''
        LblSeq=''
        Lblslno=''
        LblDem_regno=''
        Lbldoc_type=''
        M2=''
        M4=''
        M5=''
        M14=''
        DEM_OTHERS=''
        ALT_PART=''
        STATUS=''
        a=0
        
        print(bno)
        SrchQry = Proddem.objects.filter(status='C',del_fl__isnull=True,staff_no=staffno,slno=slno,dem_regno=dem_regno).values('dem_regno','brn_no','bo_no','slno','part_no','epc','qty','week_no','batch_type','l_fr','l_to','seq','status','staff_no','ddoc_type','name','m2','m4','m5','m14','dem_others').order_by('staff_no','dem_regno','slno').distinct() 
        DEM=SrchQry
        if(DEM.count()>0):
            NAME = DEM[0]['name']
            brno=DEM[0]['brn_no']
            pno=DEM[0]['part_no']
            Lblpartno = DEM[0]['part_no']
            bno=DEM[0]['bo_no']
            Lblbo_no = DEM[0]['bo_no']
            epc=DEM[0]['epc']
            Lblepc = DEM[0]['epc']
            bqty=DEM[0]['qty']
            Lblqty = DEM[0]['qty']
            lfr=DEM[0]['l_fr']
            lto=DEM[0]['l_to']
            btype=DEM[0]['batch_type']
            Lblbatch_type = DEM[0]['batch_type']
            seq=DEM[0]['seq']
            LblSeq = DEM[0]['seq']
            duewk=DEM[0]['week_no']
            Lblslno = DEM[0]['slno']
            LblDem_regno = DEM[0]['dem_regno']
            Lbldoc_type = DEM[0]['ddoc_type']
            if DEM[0]['m2']=='Y':
                M2='Y'
            else:
                M2='NIL'

            if DEM[0]['m4']=='Y':
                M4='Y'
            else:
                M4='NIL'
            
            if DEM[0]['m5']=='Y':
                M5='Y'
            else:
                M5='NIL'
            
            if DEM[0]['m14']=='Y':
                M14='Y'
            else:
                M14='NIL'
            
            DEM_OTHERS = DEM[0]['dem_others']
        
        if(Lbldoc_type=='ALT'):
            ALT_PART = pno
            SrchQry = list(Code.objects.filter(cd_type='11',code=epc).values('num_1').order_by('cd_type','code'))
            EP=SrchQry
            if len(EP) == 0:
                a=1
            if a!=1:
                SrchQry=Code.objects.filter(cd_type='11',code=epc).values('num_l')
                pno=SrchQry[0]['num_l']
                SrchQry=Batch.objects.filter(bo_no=bno,part_no=pno,seq=seq).values('brn_no','b_expl_dt','rel_date','status').order_by('bo_no','part_no','seq').distinct()
                BAT=SrchQry
                if(BAT.count()>0):
                    brno=BAT[0]['brn_no']
                    expldt=BAT[0]['b_expl_dt']
                    reldt=BAT[0]['rel_date']
                    STATUS = BAT[0]['status']
        else:
            SrchQry=Batch.objects.filter(bo_no=bno,part_no=pno,seq=seq).values('brn_no','b_expl_dt','rel_date','status').order_by('bo_no','part_no','seq').distinct()
            BAT=SrchQry
            if(BAT.count()>0):
                reldt=BAT[0]['rel_date']
                STATUS = BAT[0]['status']

   
        if a!=1:    
            SrchQry=Part.objects.filter(partno=pno).values('ptc','des').order_by('partno').distinct()
            PT=SrchQry
            if(PT.count()>0):
                ptc=PT[0]['ptc']
                des=PT[0]['des']
        if a==0:
            a=1


        lst=[bno,pno,epc,seq,brno,ver,lfr,lto,btype,bqty,expldt,reldt,closedt,duewk,ptc,des,NAME,Lblpartno,Lblbo_no,Lblepc,Lblqty,Lblbatch_type,LblSeq,Lblslno,LblDem_regno,Lbldoc_type,M2,M4,M5,M14,DEM_OTHERS,ALT_PART,STATUS]
        
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)


def V_EP(request):
    if request.method == "GET" and request.is_ajax():   
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        print(pno,epc)
        msg=''
        lst=[]
        EP_PART=''
        DIV=''
        Txtepc= ""
        Txtversion=''
        r=True
        a=0
        b=0
        if (epc == ""):
            msg = "EPC Must be Entered"
            r=False
            a=1
        if r != False:
            SrchQry = list(Code.objects.filter(cd_type='11',code=epc).values('num_1').order_by('cd_type','code'))
            if len(SrchQry)!=0:
                EP_PART = SrchQry[0]['num_1']
            cursor = connection.cursor()
            cursor.execute('''select trim(substr("ALPHA_2",1,2)) FROM public."CODE" where "CD_TYPE"='11' AND "CODE"=%s order by "CD_TYPE", "CODE";''',[epc])
            row = cursor.fetchall()
            if len(row)!=0:
                SrchQry = row[0][0]
            else:
                SrchQry = ''
            if len(SrchQry)!=0:
                DIV = SrchQry
            check=["16010085","17230184","17010019","16010255","17010421","16010206","17010391"]
            if pno not in check:
                a=list(Nstr.objects.filter(pp_part=pno,epc=epc).values('pp_part'))
                if len(a)==0:
                    msg= "Part has no Child!"
                    Txtepc= ""
                    r=False
                    a=1
            if r!= False:
                if pno==EP_PART:
                    r= True
                    a=1
                    b=1
                if r == True and  b==0:
                    check=["16010085","17230184","17010019","16010255","17010421","16010206","17010391"]
                    if pno not in check:
                        a=list(Nstr.objects.filter(cp_part=pno,epc=epc).values('pp_part'))
                        if len(a)==0:
                            msg= "Part Not in this End Product!"
                            Txtepc = ""
                            r=False
                            a=1
        if a==0:
            r=True
        lst=[r,msg,EP_PART,DIV,Txtepc,Txtversion]
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)


def v_bt(request):
    if request.method == "GET" and request.is_ajax():
        bno=request.GET.get('val1')
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        btype=request.GET.get('val9')
        ptc=request.GET.get('val15')
        EP_PART=request.GET.get('val25')
        MUSR_CD=request.GET.get('val26')
        msg=''
        lst=[]
        Txtbatch_type=''
        a=0
        r=True
        FB = ''
        SB = ''
        TB = ''
        if (bno != ''):
            if (len(bno) > 1):
                FB = bno[:2]
            else:
                FB = ''
            if (len(bno) > 4):
                SB = bno[2:5]
            else:
                SB=''
            if (len(bno) > 6):
                TB = bno[5:7]
            else:
                TB = ''
        check=["O", "S", "R", "M", "B", "N"]
        if btype not in check:
            msg= "Enter O, S, R, M, B or N"
            Txtbatch_type = ''
            r = False
            a=1
        if r != False:
            if (btype == "O" and pno != EP_PART):
                msg = "ORDINARY BATCH CAN BE LOADED ONLY FOR END-PRODUCT["+str(EP_PART)+"]"
                Txtbatch_type = ''
                r = False
                a=1
            if r != False:
                if (btype == "O"):
                    check1=["04", "05", "13", "12","33"]
                    if FB not in check1:
                        msg = "ORDINARY BATCH SHOULD START WITH EITHER 04/05/13/33"
                        Txtbatch_type = ''
                        r = False
                        a=1
                    if r != False:
                        check2=["01", "02", "05", "1A", "1C", "1F", "1U", "26", "1Y", "07", "21","46"]
                        if ((FB == "04") and (epc not in check2)):
                            msg = "EPC SHOULD BE 01/02/05/1A/1C/1F/1U/26/1Y/07/< FOR BATCH STARTING WITH [04]"
                            Txtbatch_type = ''
                            r = False
                            a=1
                        if r != False:
                            check3=["03", "04", "06", "07", "08", "09", "1B", "1G", "1H", "1J", "1K", "1L", "1D", "1M", "1P", "1E", "1N", "1R", "11", "1Q", "12", "28", "18", "14","22","33","42"]
                            if ((FB == "05") and (epc not in check3)):
                                msg = "EPC SHOULD BE 03/04/06/07/08/09/1B/1G/1H/1J/1K/1L/1D/1M/1Q/12/28/18/14/33/42  FOR BATCH STARTING WITH [05]"
                                Txtbatch_type = ''
                                r = False
                                a=1
                            if r != False:
                                check4=["O","M","N"]
                                if((btype not in check4) and (pno==EP_PART)):
                                    check5=["16010085", "17230184", "17010019", "16010255", "17010421", "16010206"]
                                    if pno not in check5:
                                        msg = "END-PRODUCT CAN BE LOADED ONLY AGAINST  ORDINARY/MISC BATCHES"
                                        Txtbatch_type = ''
                                        r = False
                                        a=1
                                if r != False:        
                                    if (btype == "S"):
                                        if (FB != "07"):
                                            msg = "STOCK SUSPENSE WORK ORDER SHOULD START WITH 07"
                                            Txtbatch_type = ''
                                            r = False
                                            a=1
                                        if r != False:
                                            if (ptc != "L"):
                                                msg = "NOT A STOCK SUSPENSE ITEM [L]"
                                                Txtbatch_type = ''
                                                r = False
                                                a=1
                                    if r != False:
                                        if (btype == "N"):
                                            check6=["13","12"]
                                            if FB not in check6:
                                                msg = "WO FOR SPARES TO NRC'S SHOULD START WITH 13 OR 12"
                                                Txtbatch_type = ''
                                                r = False
                                                a=1
                                        if r != False:
                                            if (btype == "B"):
                                                if (FB != "25"):
                                                    msg = "WORK ORDER FOR B.I. ITEMS  SHOULD START WITH 25"
                                                    Txtbatch_type = ''
                                                    r = False
                                                    a=1
                                            if r != False:
                                                if (MUSR_CD != "APM2"):
                                                    if (btype == "M"):
                                                        check7=["01", "02", "10", "18", "21", "24", "69", "08"]
                                                        if FB not in check7:
                                                            msg = "MISC WORK ORDER SHOULD START WITH 10/18/21/24/69/08"
                                                            Txtbatch_type = ''
                                                            r = False
                                                            a=1
                                                        if r != False:
                                                            check8=["01", "02"]
                                                            check9=["117", "118", "119"]
                                                            if ((FB in check8) and (SB in check9)):
                                                                msg = "MISC WORK ORDER CAN NOT HAVE SECOND BARREL AS 117/118/119"
                                                                Txtbatch_type = ''
                                                                r = False
                                                                a=1
                                                if r != False:
                                                    if (btype == "R"):
                                                        check10=["01", "02"]
                                                        if FB not in check10:
                                                            msg = "REPL. WORK ORDER SHOULD START WITH 01/02"
                                                            Txtbatch_type = ''
                                                            r = False
                                                            a=1
                                                        if r != False:
                                                            if (FB=="01"):
                                                                check11=["117", "118"]
                                                                if SB in check11:
                                                                    msg = "WORK ORDER STARTING WITH [01]  SHOULD HAVE 117/118 IN SECOND BARREL"
                                                                    Txtbatch_type = ''
                                                                    r = False
                                                                    a=1
                                                                else:
                                                                    a=list(Shop.objects.filter(shop=TB).values('shop'))
                                                                    if len(a)==0:
                                                                        msg = "WORK ORDER STARTING WITH [01]  SHOULD HAVE VALID SHOP AS THIRD BARREL"
                                                                        Txtbatch_type = ''
                                                                        r = False
                                                                        a=1
                                                    if r != False:
                                                        if (FB == "02" and bno != "0211966"):
                                                            msg = "REPL WO STARTING WITH 02 SHOULD BE 0211966"
                                                            Txtbatch_type = ''
                                                            r = False
                                                            a=1
        if a==0:
            r=True                                               
        lst=[r,msg,Txtbatch_type]
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)


def vlft(request):
    if request.method == "GET" and request.is_ajax():   
        bno=request.GET.get('val1')
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        lfr=request.GET.get('val7')
        lto=request.GET.get('val8')
        ptc=request.GET.get('val15')
        EP_PART=request.GET.get('val25')
        MUSR_CD=request.GET.get('val26')
        msg=''
        lst=[]
        Txtloco_to = ''
        r=True
        a=0
        b=0
        if (lfr == "" or lto == ""):
            msg = "Proper Loco-To Must be Entered"
            r = False
            b=1
        if r != False:
            if(int(lfr)>int(lto)):
                msg = "Proper Loco-To Must be Entered.."
                r = False
                b=1
            if r != False:
                if (pno == EP_PART):
                    r = True
                    a=1
                    b=1
                if r == True and  a==0:
                    MUSR_CD="APM2"
                    if (CPQ(pno,epc,EP_PART,lto) == 0 and MUSR_CD!="APM2"):
                        msg = " Part Not in current structure for this End Product"
                        r = False
                        b=1
                    if r != False:
                        if (MUSR_CD != "APM2"):
                            SrchQry = list(Nstr.objects.filter(cp_part=pno,epc=epc).values('cp_part').order_by('cp_part','epc'))
                            if (len(SrchQry)==0):
                                msg = " Part Not in current structure for this End Product.."
                                Txtloco_to = ''
                                r = False
                                b=1
                        if r != False:
                            if (MUSR_CD != "APM2"):
                                SrchQry = list(Nstr.objects.filter(cp_part=pno,epc=epc,l_fr__lte=lto,l_to__gte=lto).values('ptc').order_by('cp_part','epc'))
                                if (len(SrchQry)==0):
                                    msg = " Part Not Currently in this End Product"
                                    Txtloco_to = ''
                                    r = False
                                    b=1
                                if r != False:
                                    ptc = SrchQry[0]['ptc']
                                    check=["M", "Z", "L", "B"]
                                    if ptc not in check:
                                        msg = "Not a Shop Manufactured Part"
                                        Txtloco_to = ''
                                        r = False
                                        b=1
                            if r != False:
                                FB = ''
                                if (bno != ""):
                                    if (len(bno) > 1):
                                        FB = bno[:2]
                                    else:
                                        FB = ""
                                if (FB == "25"):
                                    if (ptc != "B"):
                                        msg = 'View_GM'
        if b==0:
            r = True
        lst=[r,msg,Txtloco_to]
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)

def CPQ( _pn, _ep, _epn, _lto):
        if _lto== "":
            _lto = "9999"
        if _pn == _ep:
            return 1
        dt = []
        q = 0
        ds=list(Nstr.objects.filter(cp_part=_pn,epc=_ep).values('pp_part').order_by('cp_part','epc'))
        if len(ds)<=0:
            q = 0
            return q
        else:
            Dss=[]
            Dss=impl(_pn, "1", _ep, dt, _epn,_lto)
            for i in range(len(Dss)):
                if str(Dss[i]["part"]) == _epn:
                    q1 = 0
                    if str(Dss[i]["wt"]) != "":
                        q1 = float(Dss[i]["wt"])
                    q = q + q1
        return q

def impl( _pn,  wt, _ep, dt, _epn, _lt):
        ds1=list(Nstr.objects.filter(cp_part=_pn,epc=_ep,l_fr__lte=_lt,l_to__gte=_lt).values('pp_part','cp_part','qty','ptc','alt_link').order_by('cp_part','epc'))
        val = 0
        if len(ds1) > 0:
            for i in range(len(ds1)):
                pp_part = ds1[i]["pp_part"]
                qty = 0
                if ds1[i]["qty"] != "":
                    qty = float(ds1[i]["qty"])
                val = qty * float(wt)
                if pp_part == _epn:
                    dt=write_row(pp_part, str(round(val, 3)),dt)
                val = qty * float(wt)
                mpp_part = pp_part
                p=['M','Z','L','B']
                RecDs=list(Nstr.objects.filter(cp_part=mpp_part,epc=_ep,ptc__in=p).values('cp_part'))        
                if len(RecDs) > 0:
                    impl(mpp_part, str(val), _ep, dt, _epn,_lt)
            return dt
        return dt

def write_row( one, two, dt):
        dt.append({'part':one,'wt':two})
        return dt

def vwk(request):
    if request.method == "GET" and request.is_ajax():
        duewk=request.GET.get('val14')
        r=True
        lst=[]
        msg=''
        y2kwk = 0
        a=0
        if (duewk == ""):
            msg = "Due Week Must be Entered"
            r = False
            a=1
        if r != False:
            y2kwk = int(duewk)
            duewk=duewk.rjust(2,'0')[0:2]
            if int(duewk) < 30:
                y2kwk = 200000 + y2kwk
            else:
                y2kwk = 190000 + y2kwk
            if (y2kwk < 199601):
                msg = "Batch too Old!!"
                r = False
                a=1
        if a==0:
            r = True
        lst=[r,msg]
        print(lst)
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)


def vqt(request):
    if request.method == "GET" and request.is_ajax():   
        lfr=request.GET.get('val7')
        lto=request.GET.get('val8')
        btype=request.GET.get('val9')
        bqty=request.GET.get('val10')
        lst=[]
        lfr1 = "0"
        lft = "0"
        msg=''
        r=True
        a=0
        if (bqty == ""):
            msg = "Batch Qty Must be Entered"
            r = False
            a=1
        if r != False:
            if (lfr != ""):
                lfr1 = lfr
            if (lto != ""):
                lft = lto
            if (btype == "O" and bqty != str(int(lft) - int(lfr1) + 1)):
                msg = "BATCH-QTY WRONG"
                r = False
                a=1
        if a==0:
            r = True
        lst=[r,msg]
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)


def altdoc(request):
    if request.method == "GET" and request.is_ajax():   
        bno=request.GET.get('val1')
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        seq=request.GET.get('val4')
        brno=request.GET.get('val5')
        ver=request.GET.get('val6')
        lfr=request.GET.get('val7')
        lto=request.GET.get('val8')
        btype=request.GET.get('val9')
        bqty=request.GET.get('val10')
        expldt=request.GET.get('val11')
        reldt=request.GET.get('val12')
        closedt=request.GET.get('val13')
        duewk=request.GET.get('val14')
        ptc=request.GET.get('val15')
        des=request.GET.get('val16')
        ALT_PART=request.GET.get('val31')
        STATUS=request.GET.get('val32')
        Txtl_fr = ''
        Txtl_to = ''
        msg=''
        a=0
        TxtApart_no = ''
        L_bo_no = ''
        L_brn_no = ''
        L_part_no = ''
        L_ptc = ''
        L_seq = ''
        TxtAbrn_no = ''
        L_epc = ''
        L_epcdes = ''
        L_version = ''
        L_lfr = ''
        L_lto = ''
        tmp_asslyno = pno
        IsAlt = 'T'
        r = True
        if (bno == ""):
            msg = "Cannot Proceed Without BRN-NO!"
            r = False
            a=1
        if r != False:
            check=["E","R"]
            if STATUS not in check:
                msg = STATUS + " : Status invalid for Action!"
                r = False
                a=1
            if r != False:
                if (btype != "O"):
                    msg = "This Option Permitted only for Ordinary Batches!"
                    r = False
                    a=1
        if a==0:
            TxtApart_no = ALT_PART
            L_bo_no = bno
            L_brn_no = brno
            L_part_no = pno
            L_ptc = ptc
            L_seq = seq
            TxtAbrn_no = L_brn_no
            L_epc = epc
            L_epcdes = des
            L_version = ver
            L_lfr = lfr
            L_lto = lto
            r = True
        lst=[r,msg,Txtl_fr,Txtl_to,tmp_asslyno,IsAlt,TxtApart_no,L_bo_no,L_brn_no,L_part_no,L_ptc,L_seq,TxtAbrn_no,L_epc,L_epcdes,L_version,L_lfr,L_lto]
        
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)



def v_altpart(request):
    if request.method == "GET" and request.is_ajax():   
        bno=request.GET.get('val1')
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        seq=request.GET.get('val4')
        brno=request.GET.get('val5')
        ver=request.GET.get('val6')
        lfr=request.GET.get('val7')
        lto=request.GET.get('val8')
        btype=request.GET.get('val9')
        bqty=request.GET.get('val10')
        expldt=request.GET.get('val11')
        reldt=request.GET.get('val12')
        closedt=request.GET.get('val13')
        duewk=request.GET.get('val14')
        ptc=request.GET.get('val15')
        des=request.GET.get('val16')
        TxtApart_no=request.GET.get('val33')
        Txtalt_des=''
        Txtalt_link=''
        EP_TYPE=''
        Txtl_to=request.GET.get('val34')
        r=True
        a=0
        msg=''
        SrchQry = Part.objects.filter(partno=TxtApart_no).values('des','alt_link').order_by('partno')
        PT=SrchQry
        print(PT)
        if (PT.count() <= 0):
            msg = "Non Existent Part!"
            r = False
            a=1
        if a==0:
            Txtalt_des = PT[0]['des']
            Txtalt_link = PT[0]['alt_link']    
            EP_TYPE = epc
            if (Txtalt_link == ""):
                msg = "This is not an Alternative Part!"
                r = False
                a=1
            SrchQry = Nstr.objects.filter(cp_part=TxtApart_no,epc=EP_TYPE).values('epc')
            if a==0:
                if (SrchQry.count()==0):
                    r = True
                    a=1
                SrchQry = Nstr.objects.filter(cp_part=TxtApart_no,epc=EP_TYPE,l_fr__lte=Txtl_to,l_to__gte=Txtl_to).values('epc')
                if  a==0:
                    if (SrchQry.count()!=0):
                        r = True
                        a=1
                    else:
                        msg = "Part Not Current in this EP!"
                        r = False
        lst=[r,msg,Txtalt_des,Txtalt_link,EP_TYPE]
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)



def v_alto(request):
    if request.method == "GET" and request.is_ajax():   
        bno=request.GET.get('val1')
        pno=request.GET.get('val2')
        epc=request.GET.get('val3')
        seq=request.GET.get('val4')
        brno=request.GET.get('val5')
        ver=request.GET.get('val6')
        lfr=request.GET.get('val7')
        lto=request.GET.get('val8')
        btype=request.GET.get('val9')
        bqty=request.GET.get('val10')
        expldt=request.GET.get('val11')
        reldt=request.GET.get('val12')
        closedt=request.GET.get('val13')
        duewk=request.GET.get('val14')
        ptc=request.GET.get('val15')
        des=request.GET.get('val16')
        Txtl_fr=request.GET.get('val35')
        Txtl_to=request.GET.get('val34')
        Txtalt_des=''
        Txtalt_link=request.GET.get('val36')
        EP_TYPE=''
        a=0
        c=0
        msg=''
        if (Txtl_fr == "" or Txtl_to == ""):
            msg = "Loco From & To Must be Entered!"
            a=1
            c=1
        if a==0:
            if (int(Txtl_to)<int(Txtl_fr)):
                Txtl_to = ""
                msg = "Enter Proper Loco From & To!!"
                a=1
                c=1
            if a==0:
                cursor=connection.cursor()
                cursor.execute('''select "ALT_LINK" from public."ALTDOC" where ("BRN_NO")=
	                        %s and trim("ALT_LINK"::text)=%s
	                        order by "BRN_NO", "ALT_LINK","L_FR", "L_TO";''',[brno,Txtalt_link])
                SrchQry=list(cursor.fetchall())
                if len(SrchQry)>0:
                    alt_link = SrchQry[0][0]
                else:
                    alt_link=''
                if (alt_link == ""):
                    c=0
                    a=1
                    msg="Alt Link is Null!!"
                if  a==0:
                    SrchQry = Altdoc.objects.filter((Q(l_fr__lte=Txtl_fr,l_to__gte=Txtl_fr) | Q(l_fr__lte=Txtl_to,l_to__gte=Txtl_to)),brn_no='6323',alt_link=alt_link).values('l_fr','l_to','alt_link','expl_dt').order_by('brn_no','alt_link','l_fr','l_to')
                    ALT=SrchQry
                    for i in ALT.count():
                        if (ctrl == "1"):
                            msg = "Record Exists for " + ALT[i]['l_fr'] + "-" + ALT[i]['l_to']
                            c=1
                            a=1
                        if a==0:
                            if (ALT[i]['expl_dt'] != ""):
                                msg = "Document Already Given for "+ALT[i]['l_fr']+ "-"+ ALT[i]['l_to']
                                c=1
                                a=1
            
        lst=[c,msg,Txtl_to]
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)


def Key_F9_F11(request):
    if request.method=='GET' and request.is_ajax():
            Txtbrn_no=request.GET.get('val5')
            Rej_Type=request.GET.get('Rej_Type')           
            a=0
            if Txtbrn_no != "":
                msg= "Please Click clear button first"
                a=1
            if a==0:
                SrchQry = M13.objects.filter(status__isnull=True).values('status')
                print(SrchQry.count())
                if SrchQry.count()!=0:
                    msg= "No Rej_M14s/Rej_M4s for Processing"
                    a=1
                if a==0:
                    from django.db import connection		
                    cursor = connection.cursor()
                    cursor.execute('''select "WO_REP" as bo_no,"PART_NO","EPC" as ep_type,substr("SHOP",1,2) as pm_no,max("WO") as org_batch,99999 as brn_no,
                    SUM("QTY_REJ") as batch_qty,'R' As batch_Type,000 as seq,'    ' as loco_fr,'    '  as loco_to,'R' as status,CURRENT_DATE as b_expl_dt ,
                    CURRENT_DATE as bo_updt_dt,' ' as ptc, %s as remark  from public."M13" where coalesce(trim("STATUS"),'#')='#' 
                    AND trim("REJ_CAT")=%s  and coalesce(trim("REMARK"),'*')='*' GROUP by "WO_REP", "PART_NO","EPC", "SHOP";''',[Rej_Type,Rej_Type])
                    row = cursor.fetchall()
                    DTM13 = list(row)              
                
                    if len(DTM13) < 1:
                        msg= "No Rej_M14s/Rej_M4s for Processing"
                        a=1
                    if a==0:
                        m13tmp2.objects.all().delete()
                        cursor.execute('''INSERT INTO public.dlw_m13tmp2("BO_NO", "PART_NO", "EP_TYPE", "PM_NO", "ORG_BATCH", "BRN_NO", "BATCH_QTY", "BATCH_TYPE", "SEQ", "LOCO_FR", "LOCO_TO", "STATUS", "B_EXPL_DT", "BO_UPDT_DT", "PTC", "REMARK")
	                                        select "WO_REP" as bo_no,"PART_NO","EPC" as ep_type,substr("SHOP",1,2) as pm_no,max("WO") as org_batch,99999 as brn_no,
                                            SUM("QTY_REJ") as batch_qty,'R' As batch_Type,000 as seq,'    ' as loco_fr,'    '  as loco_to,'R' as status,CURRENT_DATE as b_expl_dt ,
                                            CURRENT_DATE as bo_updt_dt,' ' as ptc, 'M14' as remark  from public."M13" where coalesce(trim("STATUS"),'#')='#' 
                                            AND trim("REJ_CAT")='0000000'  and coalesce(trim("REMARK"),'*')='*' GROUP by "WO_REP", "PART_NO","EPC", "SHOP";''')
                        
                        nm = len(DTM13)
                        SrchQry=list(Code.objects.filter(cd_type='M2',code='BRN').values('num_1').order_by('cd_type','code'))
                        num1 =SrchQry
                        if len(num1) == 0:
                            msg= "No BRN_NO Counter in Code!?"
                            a=1
                        if a==0:
                            new_num = int(num1)
                            seq
                            maxseq
                            new_num = new_num + nm
                            Code.objects.filter(cd_type='M2',code='BRN').update(code=new_num)
                            for i in range(len(DTM13)):
                                DTM13[i]["brn_no"] = int(num1) + int(i + 1)
                                SrchQry = Batch.objects.filter(bo_no=DTM13[i]["org_batch"],ep_type=DTM13[i]["ep_type"]).values('loco_fr','loco_to').order_by('bo_no','ep_type')
                                dsb = list(SrchQry)
                                if len(dsb) > 0:
                                    DTM13[i]["loco_fr"] = dsb[0]["loco_fr"]
                                    DTM13[i]["loco_to"] = dsb[0]["loco_to"]
                                SrchQry = list(Nstr.objects.filter(cp_part=DTM13[i]["part_no"],epc=DTM13[i]["ep_type"]).values('ptc').order_by('cp_part','epc'))
                                if len(SrchQry)>0:
                                    SrchQry=SrchQry[0]['ptc']
                                else:
                                    SrchQry=''
                                DTM13[i]["ptc"] = SrchQry
                                if (DTM13[i]["loco_to"] == ""):
                                    a=Nstr.objects.filter(cp_part=DTM13[i]["part_no"],epc=DTM13[i]["ep_type"]).aggregate(Max('l_fr'))
                                    DTM13[i]["loco_to"] =a['l_fr__max']
                                if DTM13[i]["loco_fr"] == "":
                                    DTM13[i]["loco_fr"] = DTM13[i]["loco_to"]
                                cursor = connection.cursor()
                                cursor.execute('''insert into public.dlw_m13tmp2 ("BO_NO","PM_NO","PART_NO", "EP_TYPE","LOCO_FR","LOCO_TO","BATCH_QTY", "BATCH_TYPE",
                                                        "BRN_NO","SEQ", "STATUS","B_EXPL_DT","REMARK","PTC") values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',[DTM13[i]["BO_NO"],DTM13[i]["pm_no"], DTM13[i]["PART_NO"],DTM13[i]["EP_TYPE"],DTM13[i]["LOCO_FR"], 
                                                        DTM13[i]["LOCO_TO"],DTM13[i]["BATCH_QTY"], DTM13[i]["BATCH_TYPE"],DTM13[i]["BRN_NO"], DTM13[i]["SEQ"],DTM13[i]["status"],CURRENT_DATE,DTM13[i]["remark"],DTM13[i]["ptc"]])
                                row = cursor.fetchall()
                            SrchQry=m13tmp2.objects.values('bo_no','part_no').order_by('brn_no')
                            dst = list(SrchQry)
                            for i in range(len(dst)):
                                seq = 0
                                maxseq = 0
                                SrchQry = list(Batch.objects.filter(bo_no= dst[i]["bo_no"],part_no=dst[i]["part_no"]).values('seq'))
                                if len(SrchQry) > 0:
                                    SrchQry =Batch.objects.filter(bo_no= dst[i]["bo_no"],part_no=dst[i]["part_no"]).aggregate(Max('seq'))
                                    
                                    
                                    s = SrchQry['seq__max']
                                    maxseqint(s)
                                SrchQry = m13tmp2.objects.filter(bo_no=dst[i]["bo_no"],part_no=dst[i]["part_no"]).values('bo_no','part_no','id').order_by('brn_no')
                                
                                dsit = list(SrchQry)
                                for  j in range(len(dsit)):
                                    s = 0
                                    seq = seq + 1
                                    s = seq + maxseq
                                    m13tmp2.objects.filter(id= dsit[j]["id"]).update(seq=s)
                             
                            cursor.execute('''insert into public."BATCH"("BO_NO", "PART_NO", "EP_TYPE","LOCO_FR", "LOCO_TO","BATCH_QTY", "BATCH_TYPE","BRN_NO","SEQ","STATUS","B_EXPL_DT","REMARK") 
                                             (select "BO_NO", "PART_NO", "EP_TYPE","LOCO_FR", "LOCO_TO","BATCH_QTY":: int, "BATCH_TYPE","BRN_NO" ::int,"SEQ"::int,"STATUS",TO_DATE("B_EXPL_DT", 'YYYY/MM/DD'),"REMARK" FROM public.dlw_m13tmp2 where  coalesce("LOCO_TO",'*')<>'*');''')
                            InsrtQry = "insert into batch(BO_NO,PART_NO,EP_TYPE,LOCO_FR,LOCO_TO,BATCH_QTY,BATCH_TYPE,BRN_NO,SEQ,status,B_EXPL_DT,remark) (select BO_NO,PART_NO,EP_TYPE,LOCO_FR,LOCO_TO,BATCH_QTY,BATCH_TYPE,BRN_NO,SEQ,status,B_EXPL_DT,remark from m13tmp2 where  nvl(loco_to,'*')<>'*')";
                           
                            mdc = "89" if Rej_Type == "M14" else "88"
                            nm14 = len(DTM13)
                            _sn = updtcode(nm14, "21", "M14", "m14")
                            if (_sn != 0):
                                seqs = _sn + 1
                                cursor.execute('''CREATE SEQUENCE M4SEQ MINVALUE 1 START WITH %s INCREMENT BY 1 CACHE 20''',[seqs])
                                M13Tmp21.objects.all().delete()
                                cursor.execute('''insert into public."M13TMP21"("BO_NO", "PART_NO", "EP_TYPE", "PM_NO", "ORG_BATCH", "BRN_NO", "BATCH_QTY", "BATCH_TYPE", "SEQ", "LOCO_FR", "LOCO_TO", "STATUS", "B_EXPL_DT", "BO_UPDT_DT", "PTC", "REMARK")
                                                (SELECT "BO_NO", "PART_NO", "EP_TYPE", "PM_NO", "ORG_BATCH", "BRN_NO" ::int, "BATCH_QTY" ::int, "BATCH_TYPE", "SEQ" ::int, "LOCO_FR", "LOCO_TO", "STATUS", TO_DATE("B_EXPL_DT", 'YYYY/MM/DD'), TO_DATE("BO_UPDT_DT", 'YYYY/MM/DD'), "PTC", "REMARK"
	                                                FROM public.dlw_m13tmp2)''')
                                cursor.execute('''INSERT INTO public."M14M4NEW1"("DOC_CODE", "DOC_NO", "PM_NO", "PART_NO", "QTY", "L_FR", "L_TO", "BO_NO", "ASSLY_NO", "SEQ", "DUE_WK", "PRTDT", "BRN_NO", "DOC_IND", "UNIT", "EPC", "VERSION", "STAGE", "WARD_NO", "FINYEAR", "VR_NO", "KIT_IND", "STATION", "STG", "SUB_KIT", "OPN_NO", "KIT_NO", "STATUS", "SUB_DOCNO", "LIEU_PART", "DRAWN_BY", "MARK", "DEL_FL", "DOC_NO_OLD", "EPC_OLD", "RECEIVED_MAT", "ISSUED_QTY", "RECEIVED_QTY", "REMARKS", "LINE", "CLOSING_BAL", "LASER_PST", "POSTED_DATE", "WARDKP_DATE", "SHOPSUP_DATE", "POSTED1_DATE", "RECEIVED_MAT14", "ISSUED_QTY14", "RECEIVED_QTY14", "REMARKS14", "LINE14", "CLOSING_BAL14", "LASER_PST14", "POSTED_DATE14", "WARDKP_DATE14", "SHOPSUP_DATE14", "POSTED1_DATE14")
                                                    select %s as  doc_code,nextval('M4SEQ') doc_no,"PM_NO"::int,"PART_NO","BATCH_QTY"::int as qty,"LOCO_FR"::int as l_fr,"LOCO_TO"::int as l_to,"BO_NO","PART_NO" as assly_no,
                                                    "SEQ" ::int,null as due_wk,CURRENT_DATE as prd_dt,0 as brn_no,"PTC" as doc_ind, null as unit,"EP_TYPE" as epc ,null as version,null as stage,null as wrd_no,null as finyear ,
                                                    null as vr_no,null as kit_ind,null as station,null as stg,null as sub_kit,null as opn_no, 0 as kit_no,
                                                    null as status,0 as sub_docno,null as lieu_part,null as drawn_by,null as mark,null as del_fl,0 as doc_no_old,
                                                    null as epc_old,NULL AS "RECEIVED_MAT",NULL AS "ISSUED_QTY",NULL AS "RECEIVED_QTY", NULL AS "REMARKS",NULL AS "LINE", 
                                                    NULL AS "CLOSING_BAL",0 AS "LASER_PST",0 AS "POSTED_DATE",0 AS "WARDKP_DATE",0 AS "SHOPSUP_DATE",0 AS "POSTED1_DATE", 
                                                    NULL AS "RECEIVED_MAT14",NULL AS "ISSUED_QTY14",NULL AS "RECEIVED_QTY14",NULL AS "REMARKS14",NULL AS "LINE14",NULL AS "CLOSING_BAL14",
                                                    0 AS "LASER_PST14",0 AS "POSTED_DATE14",0 AS "WARDKP_DATE14",0 AS "SHOPSUP_DATE14",0 AS "POSTED1_DATE14"
                                                    from  public."M13TMP21"''',[mdc])
                            else:
                                m14fr= "0"
                                m14to = "0"
                                a=1
                            if a==0:
                                if (m14to != "0"):
                                    #//not sure abt exact record entries in doclog tbl 
                                    date=datetime.datetime.now()
                                    Doclog.objects.create(expl_dt=date,doc_type=Rej_Type,doc_fr=m14fr,doc_to=m14to,batch_type='R')
                                M13.objects.filter(status__isnull=True,sel_sw__isnull=False,rej_cat=Rej_Type,remark__isnull=True).update(status='P')
                                
            lst=[a,msg]
            return JsonResponse(lst,safe=False)
    return JsonResponse({"success":False},status=400)

def key_F7_1(request):
    if request.method=='GET' and request.is_ajax():
            Txtbo_no=request.GET.get('val1')
            Txtpart_no=request.GET.get('val2')
            Txtepc=request.GET.get('val3')
            Txtseq=request.GET.get('val4')
            Txtbrn_no=request.GET.get('val5')
            Txtversion=request.GET.get('val6')
            Txtloco_fr=request.GET.get('val7')
            Txtloco_to=request.GET.get('val8')
            Txtbatch_type=request.GET.get('val9')
            Txtbatch_qty=request.GET.get('val10')
            expldt=request.GET.get('val11')
            reldt=request.GET.get('val12')
            closedt=request.GET.get('val13')
            Txtuot_wk_f=request.GET.get('val14')
            ptc=request.GET.get('val15')
            des=request.GET.get('val16')
            Txtl_fr=request.GET.get('val35')
            Txtl_to=request.GET.get('val34')
            Txtalt_des=''
            Txtalt_link=request.GET.get('val36')
            M14=request.GET.get('M14')
            M5=request.GET.get('M5')
            M4=request.GET.get('M4')
            M2=request.GET.get('M2')
            IsAlt=request.GET.get('IsAlt')
            SCH=request.GET.get('SCH')
            EP_TYPE=''
            noM5Rej = "0"
            a=0
            if (Txtbrn_no != ""):
                msg="Please Click clear button first"
                a=1
            if a==0:
                SrchQry =M13.objects.filter(status__isnull=True).values('status').order_by('status')
                if (SrchQry.count()!=0):
                    msg= "No M13s for Processing "
                    a=1
                if a==0:   
                    connectin.cursor()
                    cursor.execute('''select "WO_REP" as bo_no, "PART_NO",max("EPC") as ep_type,max("WO") as wo,99999 as "BRN_NO",  SUM( "QTY_REJ") as batch_qty,
	                                'R' As batch_Type,000 as seq,'    ' as loco_fr,'    '  as loco_to ,CURRENT_DATE as bo_updt_dt  from public."M13"   where 
	                                coalesce(trim("STATUS"),'#')='#' and  coalesce("SEL_SW",'*')='Y'  AND coalesce(trim("REJ_CAT"),'#')='#' and coalesce(trim("REMARK"),'*')='*' 
	                                GROUP by "WO_REP", "PART_NO" order by 1,2;''')
                    SrchQry =list(cursor.fetchall())
                    DTM13 = SrchQry
                    if len(DTM13) < 1:                    
                        msg= "No M13s for Processing!!!"
                        a=1
                    if a==0:
                        m13tmp2.objects.all().delete()
                        cursor.execute('''insert into public.dlw_m13tmp2("BO_NO", "PART_NO", "EP_TYPE",  "ORG_BATCH", "BRN_NO" , "BATCH_QTY" , "BATCH_TYPE",
	                                     "SEQ", "LOCO_FR", "LOCO_TO", "STATUS", "B_EXPL_DT")  select "WO_REP" as bo_no, "PART_NO",max("EPC") as ep_type,max("WO") as wo,99999 as "BRN_NO",  SUM( "QTY_REJ") as batch_qty,
	                                    'R' As batch_Type,000 as seq,'    ' as loco_fr,'    '  as loco_to ,"STATUS",CURRENT_DATE as bo_updt_dt  from public."M13"   where 
	                                    coalesce(trim("STATUS"),'#')='#' and  trim("REJ_CAT")='0000000'  AND coalesce(trim("REJ_CAT"),'#')='#' and coalesce(trim("REMARK"),'*')='*' 
	                                    GROUP by "WO_REP", "PART_NO","STATUS" order by 1,2;''')
                
                        nm = len(DTM13)
                        SrchQry=Code.objects.filter(cd_type="M2",code='BRN').values(num_1).order('cd_type','code')
                        num1 =list(SrchQry)
                        if len(num1) == 0:
                            msg= "No BRN_NO Counter in Code!?"
                            a=1
                        if a==0:
                            new_num = int(num1)
                            seq=0
                            maxseq=0
                            new_num = new_num + nm
                            Code.objects.filter(cd_type='M2',code="BRN").update(num_1=new_num)
                            
                            dsb = []
                            for i in range(len(DTM13)):
                                DTM13[i]["brn_no"] = int(num1) + (i + 1)
                                SrchQry=Batch.objects.filter(bo_no=DTM13[i]['wo'],ep_type=DTM13[i]["ep_type"]).values('loco_to').order_by('b_expl_dt')
                                dsb = list(SrchQry)
                                if len(dsb) > 0:
                                    DTM13[i]["loco_fr"] = dsb[0]["loco_to"]
                                    DTM13[i]["loco_to"] = dsb[0]["loco_to"]
                                if (DTM13[i]["loco_to"]== ""):
                                    a=Nstr.objects.filter(cp_part=DTM13[i]["part_no"],epc=DTM13[i]["ep_type"]).aggregate(Max('l_fr'))
                                    a=a['l_fr__Max']
                                    DTM13[i]["loco_to"] = a
                                    #GlobalCls.OracleExecuteScaler("select max(l_fr) from nstr where trim(cp_part)='" + DTM13.Rows[i]["part_no"].ToString().Trim() + "' and trim(epc)='" + DTM13.Rows[i]["ep_type"].ToString().Trim() + "'");
                                if (DTM13[i]["loco_fr"] == ""):
                                    DTM13[i]["loco_fr"] = DTM13[i]["loco_to"]
                                cursor.execute('''insert into public.dlw_m13tmp2("BO_NO","PART_NO","EP_TYPE","ORG_BATCH","LOCO_FR","LOCO_TO","BATCH_QTY","BATCH_TYPE","BRN_NO","SEQ","BO_UPDT_DT") 
                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''[ DTM13[i]["BO_NO"], DTM13[i]["PART_NO"],DTM13[i]["EP_TYPE"],DTM13[i]["wo"],  DTM13[i]["LOCO_FR"],DTM13[i]["LOCO_TO"],
								DTM13[i]["BATCH_QTY"], DTM13[i]["BATCH_TYPE"], DTM13[i]["BRN_NO"],DTM13[i]["SEQ"],CURRENT_DATE])
                                
                            
                            SrchQry=list(m13tmp2.objects.values('bo_no','part_no').order_by('brn_no'))
                            dst = SrchQry
                            dsit=[]
                            for i in range(len(dst)):
                                seq = 0
                                maxseq = 0
                                SrchQry=Batch.objects.filter(bo_no=dst[i]["bo_no"],part_no= dst[i]["part_no"]).values('seq')
                                
                                if (SrchQry.count()):
                                    SrchQry=Batch.objects.filter(bo_no=dst[i]["bo_no"],part_no= dst[i]["part_no"]).aggregate(Max('seq'))
                                    
                                    s =SrchQry['seq__Max']
                                    maxseq =int(s)
                                SrchQry=m13tmp2.objects.filter(bo_no=dst[i]["bo_no"],part_no= dst[i]["part_no"]).values('bo_no','part_no','id').order_by('brn_no')
                                
                                dsit = list(SrchQry)
                                for j in range(len(dsit)):
                                    s = 0
                                    seq = seq + 1
                                    s = seq + maxseq
                                    m13tmp2.objects.filter(id=dsit[j]["id"]).update(seq=s)
                                   
                                    cursor.execute('''insert into public."BATCH"("BO_NO","PART_NO","EP_TYPE","LOCO_FR","LOCO_TO","BATCH_QTY","BATCH_TYPE","BRN_NO","SEQ") 
							                        (select "BO_NO","PART_NO","EP_TYPE","LOCO_FR","LOCO_TO","BATCH_QTY"::int,"BATCH_TYPE","BRN_NO"::int,"SEQ"::int from public.dlw_m13tmp2
							                         where coalesce("LOCO_TO",'*')<>'*');''')
                                    
                                    SrchQry = m13tmp2.objects.all()
                                    dsM13Updt = SrchQry
                                    if (dsM13Updt.Count() > 0):
                                        for i in range(dsM13Updt.Count()):
                                            M13.objects.filter(wo_rep=dsM13Updt[i]["bo_no"],part_no=dsM13Updt[i]["part_no"],epc=dsM13Updt[i]["ep_type"]).update(brn_no=dsM13Updt[i]["BRN_NO"])
                                            
                                    SrchQry = m13tmp2.objects.filter(loco_to__isnull=False).values('bo_no','part_no','seq').order_by('brn_no')
                                    dsa = SrchQry
                                    M13.objects.filter(status__isnull=True,sel_sw__isnull=False,rej_cat=True,remark__isnull=True).update(status='P')
                                    
                                    m2_fr1 = "0"
                                    m2_to1 = "0"
                                    m5_fr1 = "0"
                                    m5_to1 = "0"
                                    m14_fr1 = "0"
                                    m14_to1 = "0"
                                    m4_fr1 = "0"
                                    m4_to1 = "0"
                                    bepc = ""
                                    SrchQry = Code.objects.filter(cd_type='21',code='M2').values('num_1')
                                    StartM2NoCD = list(SrchQry)
                                    SrchQry = Code.objects.filter(cd_type='21',code='M14').values('num_1')
                                    StartM4M14NoCD = list(SrchQry)
                                    SrchQry = Code.objects.filter(cd_type='21',code='M5').values('num_1')
                                    StartM5NoCD= list(SrchQry)
                                    for i in range(dsa.count()):
                                        Txtbo_no= dsa[i]["BO_NO"]
                                        Txtpart_no = dsa[i]["PART_NO"]
                                        Txtseq = dsa[i]["SEQ"]
                                        
                                        cursor.execute('''select id,"BRN_NO","EP_TYPE","PART_NO","BATCH_TYPE","VERSION",coalesce("LOCO_FR",0) loco_fr,coalesce("LOCO_TO",0) loco_to,
                                                            coalesce("SEQ",0) seq ,nvl("BATCH_QTY",0) batch_qty,"UOT_WK_F" from batch where trim("BO_NO")= %s and trim("PART_NO")= %s 
                                                            and trim("SEQ")= %s  order by "BO_NO", "PART_NO","SEQ";''',[Txtbo_no,Txtpart_no,Txtseq])
                                        SrchQry = cursor.fetchall()
                                        dsbt = SrchQry
                                        if (dsbt.Count() > 0):
                                            ROWID = dsbt[0]["id"]
                                            Txtbrn_no = dsbt[0]["brn_no"]
                                            Txtepc = dsbt["ep_type"]
                                            Txtbatch_type = dsbt[0]["batch_type"]
                                            Txtversion = dsbt[0]["version"]
                                            Txtloco_fr = dsbt[0]["loco_fr"]
                                            Txtloco_to = dsbt[0]["loco_to"]
                                            Txtseq = dsbt[0]["seq"]
                                            Txtbatch_qty = dsbt[0]["batch_qty"]
                                            Txtuot_wk_f = dsbt[0]["uot_wk_f"]
                                        if (bno == ""):
                                            continue
                                        m2fr = "0"
                                        m2to = "0"
                                        m5fr = "0"
                                        m5to = "0"
                                        m14fr = "0"
                                        m14to = "0"
                                        m4fr = "0"
                                        m4to = "0"
                                        
                                        
                                        if (m2to != "0"):
                                            if (int(m2to) > 0):
                                                if m2_fr1 == "0":
                                                    m2_fr1 =  m2fr
                                                else:
                                                    m2_fr1 = m2_fr1
                                                m2_to1 = m2to
                                        if (m5to != "0"):
                                            if (int(m5to) > 0):
                                                if m5_fr1 == "0":
                                                    m5_fr1 =  m5fr
                                                else:
                                                    m5_fr1 = m5_fr1
                                                if (Txtbatch_type == "R"):
                                                    m5_to1 = noM5Rej
                                                else:
                                                    if m5_to1 == "0":
                                                        m5_to1 = m5to
                                                    else:
                                                        m5_to1 = (int(m5_to1) + (int(m5to) - int(m5fr) - 1))
                                        if (m14to != "0"):
                                            if (int(m14to) > 0):
                                                if m14_fr1 == "0":
                                                    m14_fr1 =  m14fr
                                                else:
                                                    m14_fr1 = m14_fr1
                                                m14_to1 =  m14to
                                        if (m4to != "0"):
                                            if (int(m4to) > 0):
                                                if m4_fr1 == "0":
                                                    m4_fr1 =  m4fr
                                                else:
                                                    m4_fr1 = m4_fr1
                                                m4_to1 =  m4to
                                        date=datetime.datetime.now()
                                        Batch.objects.filter(id=ROWID).update(b_expl_dt=date,status='R',mark='')
                                       

                                    m2fr = m2_fr1
                                    m2to = m2_to1
                                    m5fr = m5_fr1
                                    m5to = m5_to1
                                    m14fr = m14_fr1
                                    m14to = m14_to1
                                    m4fr = m4_fr1
                                    m4to = m4_to1
                                    befNum_1 = int(StartM2NoCD)
                                    SrchQry = M2Docnew1.objects.filter(m2sln__gte=m2fr,m2sln__lte=m2to).count()
                                    CardsM2No =int(SrchQry)
                                    if (CardsM2No > 0):
                                        
                                        if (befNum_1+ CardsM2No > 899000):
                                            Code.objects.filter(cd_type='21',code='M2').update(num_1=100001)
                                            #QRY_LST.Add("update code set num_1=100001 where trim(cd_type)='21' and  trim(code)='M2'");
                                        Code.objects.filter(cd_type='21',code='M2').update(num_1=befNum_1 + CardsM2No)
                                    SrchQry= M14M4new1.objects.filter(doc_no__gte=m4fr,doc_no__lte=m4to).count()
                                    CardsM4No = int(SrchQry)
                                    SrchQry= M14M4new1.objects.filter(doc_no__gte=m14fr,doc_no__lte=m14to).count()
                                    CardsM14No = int(SrchQry)
                                    befNum_1 = int(StartM4M14NoCD)

                                    if (CardsM4No > 0 and CardsM14No>0):
                                        if ((befNum_1 + CardsM4No + CardsM14No) > 899000):
                                            Code.objects.filter(cd_type='21',code='M14').update(num_1=100001)
                                        Code.objects.filter(cd_type='21',code='M14').update(num_1= befNum_1+ CardsM4No+CardsM14No)
                                    elif (CardsM4No > 0 and CardsM14No <= 0):
                                        if ((befNum_1 + CardsM4No) > 899000):
                                            Code.objects.filter(cd_type='21',code='M14').update(num_1=100001)
                                        Code.objects.filter(cd_type='21',code='M14').update(num_1= befNum_1 + CardsM4No)
                                    elif (CardsM4No <= 0 and CardsM14No > 0):
                                        if ((befNum_1 + CardsM14No) > 899000):
                                            Code.objects.filter(cd_type='21',code='M14').update(num_1=100001)
                                        Code.objects.filter(cd_type='21',code='M14').update(num_1= befNum_1 + CardsM4No)
                                    
                                    SrchQry = M5Docnew1.objects.filter(m5glsn__gte=m5fr,m5glsn__lte=m5to).count()
                                    CardsM5No = int(SrchQry)
                                    if (CardsM5No > 0):
                                    
                                        befNum_1 = int(StartM5NoCD)
                                        if (befNum_1 + CardsM5No > 899000):
                                            Code.objects.filter(cd_type='21',code='M5').update(num_1= 100001)
                                        Code.objects.filter(cd_type='21',code='M5').update(num_1= befNum_1 + CardsM4No)
                                    
                                    Txtbo_no = "       "
                                    Txtbatch_type = "R"
                                    Txtbrn_no = "0"
                                    IsAlt = "F"
                                    assly_no = ""
                                    l_fr = ""
                                    l_to = ""
                                    doclog(assly_no, l_fr, l_to, bepc,M14,m14to,m14fr,M5,m5to,m5fr,m4to,m4fr,M4,M2,m2to,m2fr,IsAlt,SCH,Txtbatch_type,Txtbrn_no,Txtpart_no)
                                   
            lst=[a,msg,Txtbo_no,Txtpart_no,Txtbrn_no,Txtepc,Txtbatch_type,Txtversion,Txtloco_fr,Txtloco_to,Txtseq,Txtbatch_qty,Txtuot_wk_f]
            return JsonResponse(lst,safe=False)
    return JsonResponse({"success":False},status=400)

def key_f1_alt(request):
    if request.method=='GET' and request.is_ajax():
        rvalt=request.GET.get('rvalt')
        rvalto=request.GET.get('rvalto')
        Txtbrn_no=request.GET.get('Txtbrn_no')
        Txtalt_link=request.GET.get('Txtalt_link')
        TxtApart_no=request.GET.get('TxtApart_no')
        Txtl_fr=request.GET.get('Txtl_fr')
        Txtl_to=request.GET.get('Txtl_to')
        if Txtalt_link=='':
            Txtalt_link=0

        a=0
        if (rvalto==0 and rvalt=='False'):
            a=1
            msg=' Some Error Occured'
        if a==0:
            SrchQry=list(Altdoc.objects.filter(brn_no=Txtbrn_no,alt_link=Txtalt_link,l_fr=Txtl_fr,l_to=Txtl_to).values('alt_link'))
            if (len(SrchQry)>0):
                msg= " Record Exists! "
                a=1
            else:
                date=datetime.datetime.now()
                Altdoc.objects.create(brn_no=Txtbrn_no,alt_link=Txtalt_link,part_no=TxtApart_no,l_fr=Txtl_fr,l_to=Txtl_to,updt_dt=date,m2_fr=0,m2_to=0,m4_fr=0,m4_to=0,m5_fr=0,m5_to=0,m14_fr=0,m14_to=0)
                
                a=2
                msg="Data Saved Successfully!"
        lst=[a,msg]
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success":False},status=400)

def key_F5_alt(request):
    if request.method=='GET' and request.is_ajax():
        Lblstaffno=request.GET.get('Lblstaffno')
        LblDem_regno=request.GET.get('LblDem_regno')
        Lblslno=request.GET.get('Lblslno')
        Txtbrn_no=request.GET.get('Txtbrn_no')
        Txtalt_link=request.GET.get('Txtalt_link')
        Txtepc=request.GET.get('Txtepc')
        Txtl_fr=request.GET.get('Txtl_fr')
        Txtl_to=request.GET.get('Txtl_to')
        TxtApart_no=request.GET.get('TxtApart_no')
        Txtpart_no=request.GET.get('Txtpart_no')
        Txtseq=request.GET.get('Txtseq')
        Txtbatch_type=request.GET.get('Txtbatch_type')
        M14=request.GET.get('M14')
        M5=request.GET.get('M5')
        M4=request.GET.get('M4')
        M2=request.GET.get('M2')
        IsAlt=request.GET.get('IsAlt')
        SCH=request.GET.get('SCH')
        Txtloco_fr=request.GET.get('Txtloco_fr')
        Txtloco_to=request.GET.get('Txtloco_to')
        altdoc_row = ""
        a=0
        cursor=connection.cursor()
        cursor.execute('''select "EXPL_DT" expl_dt,id from public."ALTDOC" where ("BRN_NO")=
	                        %s and trim("ALT_LINK"::text)=%s and trim("L_FR")=%s and trim("L_TO")=%s 
	                        order by "BRN_NO", "ALT_LINK","L_FR", "L_TO";''',[Txtbrn_no,Txtalt_link,Txtl_fr,Txtl_to])
        SrchQry=cursor.fetchall()
        ds =list( SrchQry)
        if (len(ds) <= 0):
            msg= "Must Save Alt Part Details!"
            a=1
        if a==0:
            if (ds[0][0] != ""):

                msg= "Already Exploded!"
                a=1
        
            if a==0:
                tempepc = Txtepc
                temppart = Txtpart_no
                tempseq = Txtseq
                templfr = Txtl_fr
                templto = Txtl_to
                Txtpart_no = TxtApart_no
                Txtloco_fr = Txtl_fr
                Txtloco_to = Txtl_to
                altdoc_row = ds[0][1]
                Txtseq= "0"
                m2fr = "0"
                m2to = "0"
                m5fr = "0"
                m5to = "0"
                m14fr = "0"
                m14to = "0"
                m4fr = "0"
                m4to = "0"
                Altdoc.objects.filter(id=altdoc_row).update(m2_fr=m2fr,m2_to=m2to,m5_fr=m5fr,m5_to=m5to,m14_fr=m14fr,m14_to=m14to)
                    
                doclog("", Txtl_fr, Txtl_to, "",M14,m14to,m14fr,M5,m5to,m5fr,m4to,m4fr,M4,M2,m2to,m2fr,IsAlt,SCH,Txtbatch_type,Txtbrn_no,Txtpart_no)#########################################


                m2no = (int(m2to)-int(m2fr) +1) if m2to > 0 else "0"
                if (m2no == "0"):
                
                    m2fr = ""   
                    m2to= ""
                    m2no = ""
                m4no= (int(m4to)-int(m4fr) +1) if m4to > 0 else "0"
                if (m4no == "0"):
                
                    m4_f = ""
                    m4to = ""
                    m4no = ""
                
                m5no = (int(m5to)-int(m5fr) +1) if m5to > 0 else "0"
                if (m5no == "0"):
                
                    m5fr=""
                    m5to=""
                    m5no=""
                
                m14no = (int(m14to)-int(m14fr) +1) if m14to > 0 else "0"
                if (m14no == "0"):
                    m14fr=""
                    m14to=""
                    m14no=""
                Txtpart_no = temppart
                Txtseq = tempseq
                Txtloco_fr = templfr
                Txtloco_to= templto
                Txtepc = tempepc
                a=0
        lst=[a,msg,Txtpart_no,Txtseq,Txtloco_fr,Txtloco_to,Txtepc]
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success":False},status=400)

def Update_Dem_Status(Lblstaffno,LblDem_regno,Lblslno,Txtbrn_no, m2fr,m2to, m5fr, m5to,m14fr,m14to,m4fr,m4to) :     
        SrchQry=Proddem.objects.filter(staff_no=Lblstaffno,dem_regno=LblDem_regno,slno=Lblslno).values('id')
        dem_row =SrchQry
        if dem_row.count() > 0:
            datea=datetime.datetime.now()
            abc=Proddem.objects.filter(id=dem_row[0]['id']).update(brn_no=Txtbrn_no,m2_fr= m2fr,m2_to=m2to,m5_fr= m5fr,m5_to= m5to,m14_fr=m14fr,m14_to= m14to,m4_fr=m4fr,m4_to= m4to,process_dt=datea,status='E')
            
        if abc < 0:
            return False
        else:
            return True

    
def doclog(assly,lfr, lto, bepc,M14,m14to,m14fr,M5,m5to,m5fr,m4to,m4fr,M4,M2,m2to,m2fr,IsAlt,SCH,Txtbatch_type,Txtbrn_no,Txtpart_no):   
    doc_type = "" 
    doc_to = ""
    btyp = ""
    if (m2to != "0"):
        if (int(m2to) > 0):
            doc_type = "M2"
            doc_fr = m2fr
            doc_to = m2to
            if (IsAlt == "T"):
                btyp = "A"
                assly = Txtpart_no
                lfr = Txtl_fr
                lto = Txtl_to
            else:
                btyp = Txtbatch_type         
            sch = ""
            if (len(SCH) > 0):
                sch = (str(SCH))[0, 1]
            if (M2 == "Y" or Txtbatch_type=="R"):
                date=datetime.datetime.now()
                InsertQry= Doclog.objects.update(expl_dt=date,doc_type=doc_type,brn_no=Txtbrn_no,scl_cl=sch,batch_type=btyp,doc_fr=doc_fr,doc_to=doc_to,assly_no=assly,l_fr=lfr,l_to=lto,epc=bepc)
                       
    if (m5to != "0"):
        if (int(m5to) > 0):
            doc_type = "M5"
            doc_fr = m5fr
            doc_to = m5to
            if (IsAlt == "T"):
                btyp = "A"
                assly = Txtpart_no
                lfr = Txtl_fr
                lto = Txtl_to
            else:
                btyp = Txtbatch_type                                     
            sch = ""
            if len(SCH) > 0:
                sch = str(SCH)[0:1]
            if (M5 == "Y" or Txtbatch_type == "R"):
                date=datetime.datetime.now()
                InsertQry= Doclog.objects.update(expl_dt=date,doc_type=doc_type,brn_no=Txtbrn_no,scl_cl=sch,batch_type=btyp,doc_fr=doc_fr,doc_to=doc_to,assly_no=assly,l_fr=lfr,l_to=lto,epc=bepc)

           
    if (m14to != "0"): 
        if (int(m14to) > 0):
            doc_type = "M14"
            doc_fr = m14fr
            doc_to = m14to
            if (IsAlt == "T"):
                btyp = "A"
                assly = Txtpart_no
                lfr = Txtl_fr
                lto = Txtl_to
            else:
                btyp = Txtbatch_type    
            sch = ""
            if len(SCH) > 0:
                sch = str(SCH)[0:1]
            if (int(doc_to) >=int(doc_fr)):
                if (M14 == "Y" or Txtbatch_type == "R" or SCH == "M14"):
                    date=datetime.datetime.now()
                    InsertQry= Doclog.objects.update(expl_dt=date,doc_type=doc_type,brn_no=Txtbrn_no,scl_cl=sch,batch_type=btyp,doc_fr=doc_fr,doc_to=doc_to,assly_no=assly,l_fr=lfr,l_to=lto,epc=bepc)

    if (m4to) != "0":   
        if (int(m4to) > 0):
            doc_type = "M4"
            doc_fr = m4fr
            doc_to = m4to
            if (IsAlt== "T"):
                btyp = "A"
                assly = Txtpart_no
                lfr = Txtl_fr
                lto = Txtl_to
            else:
                btyp = Txtbatch_type
            sch = ""
            if len(SCH) > 0:
                sch = str(SCH)[0:1]
            if (M4 == "Y" or Txtbatch_type == "R"):
                date=datetime.datetime.now()
                InsertQry= Doclog.objects.update(expl_dt=date,doc_type=doc_type,brn_no=Txtbrn_no,scl_cl=sch,batch_type=btyp,doc_fr=doc_fr,doc_to=doc_to,assly_no=assly,l_fr=lfr,l_to=lto,epc=bepc)

    return true






def key_f1(request): 
    if request.method=='GET' and request.is_ajax():
        Txtbo_no=request.GET.get('val1')    
        Txtpart_no=request.GET.get('val2')
        Txtepc=request.GET.get('val3')
        Txtseq=request.GET.get('val4')
        Txtbrn_no=request.GET.get('val5')
        Txtversion=request.GET.get('val6')
        Txtloco_fr=request.GET.get('val7')
        Txtloco_to=request.GET.get('val8')
        Txtbatch_type=request.GET.get('val9')
        Txtbatch_qty=request.GET.get('val10')
        Txtb_expl_dt=request.GET.get('val11')
        Txtrel_date=request.GET.get('val12')
        Txtb_close_dt=request.GET.get('val13')
        Txtuot_wk_f=request.GET.get('val14')      
        Txtptc=request.GET.get('val15')
        Txtdes=request.GET.get('val16')
        vep=request.GET.get('vep')
        vbt=request.GET.get('vbt')
        vlft=request.GET.get('vlft')
        vwk=request.GET.get('vwk')
        vqt=request.GET.get('vqt')
        MUSR_CD=request.GET.get('MUSR_CD')
        lblGridFlg=request.GET.get('lblGridFlg')
        x=request.GET.get('x')
        y=request.GET.get('y')
        B_UPDT_DT=request.GET.get('B_UPDT_DT')
        REL_DT_BC=request.GET.get('REL_DT_BC')
        CLOS_DT_B=request.GET.get('CLOS_DT_B')
        CLOS_DT_C=request.GET.get('CLOS_DT_C')
        DIV=request.GET.get('DIV')
        MARK=request.GET.get('MARK')
        REMARK=request.GET.get('REMARK')
        STATUS=request.GET.get('STATUS')
        DIV1=request.GET.get('DIV1')
        lblDIV=request.GET.get('lblDIV')
        seq=Txtseq
        a=0
        msg=''
        MUSR_CD = "107701"
        r='I'
        msg1=''
        if (Txtbrn_no==''):
            Txtbrn_no=0
        if (Txtbo_no == ""):
            msg= "Batch No. Must be Entered"
            a=1
        if a == 0:
            if (MUSR_CD != "APM2"):
                if (vep=="False" and vbt=="False" and vlft=="False" and vwk=="False" and vqt=="False"):
                    a=1 
            if a == 0:
                if (Txtbo_no == "O"):
                    Txtseq = "0"
                if Txtseq=='':
                    seq=0
                cursor=connection.cursor()
                cursor.execute('''select id from public."BATCH" where "BO_NO"=%s  and "PART_NO"=%s and coalesce("SEQ",'0')=%s  order by "BO_NO", "PART_NO","SEQ","id";''',[Txtbo_no,Txtpart_no,seq])
                ROWID=list(cursor.fetchall())
                
                if len(ROWID) > 0:
                    ROWID=ROWID[0][0]
                else:
                    ROWID=""
                print('rowid',ROWID) 
                if (ROWID == ""):
                    if (MUSR_CD == "APM2"):
                        DIV1 = "true"
                        lblDIV = "true"
                    else:
                        lblDIV = "false"
                    msg1="Show Div"
                else:
                    if (lblGridFlg == "N"): 
                        STATUS = Batch.objects.filter(id=ROWID).values('status')
                        STATUS=STATUS[0]['status']
                        if (MUSR_CD != "107701" and STATUS != "B"):
                            msg = "Cannot Modify Batch!"
                            a=1
                        if a==0:
                            STATUS = Batch.objects.filter(id=ROWID).values('status')
                            STATUS=STATUS[0]['status']
                            print(STATUS)
                            if (MUSR_CD == "107701" and STATUS == "B"):
                                up="0"
                                if Txtb_expl_dt !='' and Txtrel_date !='' and Txtb_close_dt!='':
                                    UpdtQry=cursor.execute('''UPDATE public."BATCH" SET "BO_NO"=%s, "PART_NO"=%s, "EP_TYPE"=%s, "VERSION"=%s, "DIV"=%s, "LOCO_FR"=%s, "LOCO_TO"=%s, "BATCH_QTY"=%s, "BATCH_TYPE"=%s,
                                                          "UOT_WK_F"=%s, "B_EXPL_DT"=%s, "B_CLOSE_DT"=%s, "SEQ"=%s,  "BRN_NO"=%s, "REL_DATE"=%s,
                                                           "STATUS"=%s, "MARK"=%s, "REMARK"=%s WHERE id=%s;''',[Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,Txtb_expl_dt,Txtb_close_dt,Txtseq,
                                                         Txtbrn_no,Txtrel_date,STATUS,MARK,REMARK,ROWID])
                                    up="1"
                                if Txtb_expl_dt !='' and Txtrel_date !='' and Txtb_close_dt=='':
                                    UpdtQry=cursor.execute('''UPDATE public."BATCH" SET "BO_NO"=%s, "PART_NO"=%s, "EP_TYPE"=%s, "VERSION"=%s, "DIV"=%s, "LOCO_FR"=%s, "LOCO_TO"=%s, "BATCH_QTY"=%s, "BATCH_TYPE"=%s,
                                                          "UOT_WK_F"=%s, "B_EXPL_DT"=%s, "SEQ"=%s,  "BRN_NO"=%s, "REL_DATE"=%s,
                                                           "STATUS"=%s, "MARK"=%s, "REMARK"=%s WHERE id=%s;''',[Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,Txtb_expl_dt,Txtseq,
                                                         Txtbrn_no,Txtrel_date,STATUS,MARK,REMARK,ROWID])
                                    up="1"
                                if Txtb_expl_dt !='' and Txtrel_date =='' and Txtb_close_dt!='':
                                    UpdtQry=cursor.execute('''UPDATE public."BATCH" SET "BO_NO"=%s, "PART_NO"=%s, "EP_TYPE"=%s, "VERSION"=%s, "DIV"=%s, "LOCO_FR"=%s, "LOCO_TO"=%s, "BATCH_QTY"=%s, "BATCH_TYPE"=%s,
                                                          "UOT_WK_F"=%s, "B_EXPL_DT"=%s, "B_CLOSE_DT"=%s, "SEQ"=%s,  "BRN_NO"=%s,
                                                           "STATUS"=%s, "MARK"=%s, "REMARK"=%s WHERE id=%s;''',[Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,Txtb_expl_dt,Txtb_close_dt,Txtseq,
                                                         Txtbrn_no,STATUS,MARK,REMARK,ROWID])
                                    up="1"
                                if Txtb_expl_dt !='' and Txtrel_date =='' and Txtb_close_dt=='':
                                    UpdtQry=cursor.execute('''UPDATE public."BATCH" SET "BO_NO"=%s, "PART_NO"=%s, "EP_TYPE"=%s, "VERSION"=%s, "DIV"=%s, "LOCO_FR"=%s, "LOCO_TO"=%s, "BATCH_QTY"=%s, "BATCH_TYPE"=%s,
                                                          "UOT_WK_F"=%s, "B_EXPL_DT"=%s, "SEQ"=%s,  "BRN_NO"=%s, 
                                                           "STATUS"=%s, "MARK"=%s, "REMARK"=%s WHERE id=%s;''',[Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,Txtb_expl_dt,Txtseq,
                                                         Txtbrn_no,STATUS,MARK,REMARK,ROWID])
                                    up="1"
                                if Txtb_expl_dt =='' and Txtrel_date !='' and Txtb_close_dt!='':
                                    UpdtQry=cursor.execute('''UPDATE public."BATCH" SET "BO_NO"=%s, "PART_NO"=%s, "EP_TYPE"=%s, "VERSION"=%s, "DIV"=%s, "LOCO_FR"=%s, "LOCO_TO"=%s, "BATCH_QTY"=%s, "BATCH_TYPE"=%s,
                                                          "UOT_WK_F"=%s,  "B_CLOSE_DT"=%s, "SEQ"=%s,  "BRN_NO"=%s, "REL_DATE"=%s,
                                                           "STATUS"=%s, "MARK"=%s, "REMARK"=%s WHERE id=%s;''',[Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,Txtb_close_dt,Txtseq,
                                                         Txtbrn_no,Txtrel_date,STATUS,MARK,REMARK,ROWID])
                                    up="1"
                                if Txtb_expl_dt =='' and Txtrel_date !='' and Txtb_close_dt=='':
                                    UpdtQry=cursor.execute('''UPDATE public."BATCH" SET "BO_NO"=%s, "PART_NO"=%s, "EP_TYPE"=%s, "VERSION"=%s, "DIV"=%s, "LOCO_FR"=%s, "LOCO_TO"=%s, "BATCH_QTY"=%s, "BATCH_TYPE"=%s,
                                                          "UOT_WK_F"=%s,   "SEQ"=%s,  "BRN_NO"=%s, "REL_DATE"=%s,
                                                           "STATUS"=%s, "MARK"=%s, "REMARK"=%s WHERE id=%s;''',[Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,Txtseq,
                                                         Txtbrn_no,Txtrel_date,STATUS,MARK,REMARK,ROWID])


                                    up="1"
                                if Txtb_expl_dt =='' and Txtrel_date=='' and Txtb_close_dt!='':
                                    UpdtQry=cursor.execute('''UPDATE public."BATCH" SET "BO_NO"=%s, "PART_NO"=%s, "EP_TYPE"=%s, "VERSION"=%s, "DIV"=%s, "LOCO_FR"=%s, "LOCO_TO"=%s, "BATCH_QTY"=%s, "BATCH_TYPE"=%s,
                                                          "UOT_WK_F"=%s,  "B_CLOSE_DT"=%s, "SEQ"=%s,  "BRN_NO"=%s,
                                                           "STATUS"=%s, "MARK"=%s, "REMARK"=%s WHERE id=%s;''',[Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,Txtb_close_dt,Txtseq,
                                                         Txtbrn_no,STATUS,MARK,REMARK,ROWID])

                                if Txtb_expl_dt =='' and Txtrel_date =='' and Txtb_close_dt=='':
                                    UpdtQry=cursor.execute('''UPDATE public."BATCH" SET "BO_NO"=%s, "PART_NO"=%s, "EP_TYPE"=%s, "VERSION"=%s, "DIV"=%s, "LOCO_FR"=%s, "LOCO_TO"=%s, "BATCH_QTY"=%s, "BATCH_TYPE"=%s,
                                                          "UOT_WK_F"=%s,   "SEQ"=%s,  "BRN_NO"=%s,
                                                           "STATUS"=%s, "MARK"=%s, "REMARK"=%s WHERE id=%s;''',[Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,Txtseq,
                                                         Txtbrn_no,STATUS,MARK,REMARK,ROWID])
                                    up="1"
                                print("the game",UpdtQry)
                                if (up=='1'):
                                    msg = " Batch Saved!"
                                    a=0
                                    r='I'
                
        lst=[a,msg,STATUS,DIV1,lblDIV,Txtseq,r,msg1]                        
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success:False"},status=400)

def key_f1_con(request):
    if request.method=='GET' and request.is_ajax():
        Txtbo_no=request.GET.get('val1')    
        Txtpart_no=request.GET.get('val2')
        Txtepc=request.GET.get('val3')
        Txtseq=request.GET.get('val4')
        Txtbrn_no=request.GET.get('val5')
        Txtversion=request.GET.get('val6')
        Txtloco_fr=request.GET.get('val7')
        Txtloco_to=request.GET.get('val8')
        Txtbatch_type=request.GET.get('val9')
        Txtbatch_qty=request.GET.get('val10')
        Txtb_expl_dt=request.GET.get('val11')
        Txtrel_date=request.GET.get('val12')
        Txtb_close_dt=request.GET.get('val13')
        Txtuot_wk_f=request.GET.get('val14')      
        Txtptc=request.GET.get('val15')
        Txtdes=request.GET.get('val16')
        vep=request.GET.get('vep')
        vbt=request.GET.get('vbt')
        vlft=request.GET.get('vlft')
        vwk=request.GET.get('vwk')
        vqt=request.GET.get('vqt')
        MUSR_CD=request.GET.get('MUSR_CD')
        lblGridFlg=request.GET.get('lblGridFlg')
        x=request.GET.get('x')
        y=request.GET.get('y')
        B_UPDT_DT=request.GET.get('B_UPDT_DT')
        REL_DT_BC=request.GET.get('REL_DT_BC')
        CLOS_DT_B=request.GET.get('CLOS_DT_B')
        CLOS_DT_C=request.GET.get('CLOS_DT_C')
        DIV=request.GET.get('DIV')
        MARK=request.GET.get('MARK')
        REMARK=request.GET.get('REMARK')
        STATUS=request.GET.get('STATUS')
        DIV1=request.GET.get('DIV1')
        lblDIV=request.GET.get('lblDIV')
        seq=Txtseq
        a=0
        msg=''
        MUSR_CD = "107701"
        r='U'
        if (DIV1 == "" and MUSR_CD == "APM2"): 
            a=1
        if a==0:
            qryarr = []
            count = 0
            num1 = ""
            SrchQry=list(Code.objects.filter(cd_type='M2',code='BRN').values('num_1').order_by('cd_type','code'))
            if len(SrchQry)>0:
                num1 = SrchQry[0]['num_1']
            if (MUSR_CD == "APM2"):
                REMARK = "MANUALLY RELEASED"
                B_UPDT_DT = datetime.datetime.now()
                Txtrel_date = B_UPDT_DT
                REL_DT_BC = B_UPDT_DT
                DIV = DIV1
                STATUS = "R"
            if num1!='':
                new_num = int(num1)
                new_num=new_num+1
                count ='0' 
                cursor=connection.cursor()
                cursor.execute('''update "CODE" set "NUM_1"="NUM_1"+1 where trim("CD_TYPE")='M2' and  trim("CODE")='BRN';''')
                Txtbrn_no=new_num
                if (STATUS == ""):
                    STATUS = "B"
                
                

                if Txtb_expl_dt !='' and Txtrel_date !='' and Txtb_close_dt!='':
                    cursor.execute('''insert into "BATCH"("BO_NO","PART_NO","EP_TYPE","VERSION","DIV","LOCO_FR","LOCO_TO","BATCH_QTY","BATCH_TYPE","UOT_WK_F", 
                    "B_EXPL_DT", "B_CLOSE_DT","SEQ","BRN_NO","REL_DATE","STATUS","MARK","REMARK")values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                    [Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,
                    Txtb_expl_dt,Txtb_close_dt,Txtseq,Txtbrn_no,Txtrel_date,STATUS,MARK,REMARK])
                    count ='1'
                if Txtb_expl_dt !='' and Txtrel_date =='' and Txtb_close_dt!='':
               
                    cursor.execute('''insert into "BATCH"("BO_NO","PART_NO","EP_TYPE","VERSION","DIV","LOCO_FR","LOCO_TO","BATCH_QTY","BATCH_TYPE","UOT_WK_F",    
                    "B_EXPL_DT", "B_CLOSE_DT","SEQ","BRN_NO","STATUS","MARK","REMARK")values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                    [Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,
                    Txtb_expl_dt,Txtb_close_dt,Txtseq,Txtbrn_no,STATUS,MARK,REMARK])
                    count ='1'
                if Txtb_expl_dt !='' and Txtrel_date !='' and Txtb_close_dt=='':
                
                    cursor.execute('''insert into "BATCH"("BO_NO","PART_NO","EP_TYPE","VERSION","DIV","LOCO_FR","LOCO_TO","BATCH_QTY","BATCH_TYPE","UOT_WK_F",     
                    "B_EXPL_DT","SEQ","BRN_NO","REL_DATE","STATUS","MARK","REMARK")values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                    [Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,
                    Txtb_expl_dt,Txtseq,Txtbrn_no,Txtrel_date,STATUS,MARK,REMARK])
                    count ='1'
                if Txtb_expl_dt !='' and Txtrel_date =='' and Txtb_close_dt=='':
                
                    cursor.execute('''insert into "BATCH"("BO_NO","PART_NO","EP_TYPE","VERSION","DIV","LOCO_FR","LOCO_TO","BATCH_QTY","BATCH_TYPE","UOT_WK_F",     
                    "B_EXPL_DT","SEQ","BRN_NO","STATUS","MARK","REMARK")values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                    [Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,
                    Txtb_expl_dt,Txtseq,Txtbrn_no,STATUS,MARK,REMARK])
                    count ='1'
                if Txtb_expl_dt =='' and Txtrel_date !='' and Txtb_close_dt!='':
                
                    cursor.execute('''insert into "BATCH"("BO_NO","PART_NO","EP_TYPE","VERSION","DIV","LOCO_FR","LOCO_TO","BATCH_QTY","BATCH_TYPE","UOT_WK_F",  
                    "B_CLOSE_DT","SEQ","BRN_NO","REL_DATE","STATUS","MARK","REMARK")values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                    [Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,
                    Txtb_close_dt,Txtseq,Txtbrn_no,Txtrel_date,STATUS,MARK,REMARK])
                    count ='1'
                if Txtb_expl_dt =='' and Txtrel_date =='' and Txtb_close_dt!='':
                
                    cursor.execute('''insert into "BATCH"("BO_NO","PART_NO","EP_TYPE","VERSION","DIV","LOCO_FR","LOCO_TO","BATCH_QTY","BATCH_TYPE","UOT_WK_F",        
                    "B_CLOSE_DT","SEQ","BRN_NO","STATUS","MARK","REMARK")values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                    [Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,
                    Txtb_close_dt,Txtseq,Txtbrn_no,STATUS,MARK,REMARK])
                    count ='1'
                if Txtb_expl_dt =='' and Txtrel_date !='' and Txtb_close_dt=='':
                
                    cursor.execute('''insert into "BATCH"("BO_NO","PART_NO","EP_TYPE","VERSION","DIV","LOCO_FR","LOCO_TO","BATCH_QTY","BATCH_TYPE","UOT_WK_F",  
                    "SEQ","BRN_NO","REL_DATE","STATUS","MARK","REMARK")values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',  
                    [Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,
                    Txtseq,Txtbrn_no,Txtrel_date,STATUS,MARK,REMARK])
                    count ='1'
                if Txtb_expl_dt =='' and Txtrel_date =='' and Txtb_close_dt=='':
                    cursor.execute('''insert into "BATCH"("BO_NO","PART_NO","EP_TYPE","VERSION","DIV","LOCO_FR","LOCO_TO","BATCH_QTY","BATCH_TYPE","UOT_WK_F",        
                    "SEQ","BRN_NO","STATUS","MARK","REMARK")values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                    [Txtbo_no,Txtpart_no,Txtepc,Txtversion,DIV,Txtloco_fr,Txtloco_to,Txtbatch_qty,Txtbatch_type,Txtuot_wk_f,
                    Txtseq,Txtbrn_no,STATUS,MARK,REMARK])
                    count ='1'

                rid=Batch.objects.all().aggregate(Max('id'))  
                rid=rid['id__max']
                if REL_DT_BC !='':
                    Batch.objects.filter(id=rid).update(rel_dt_bc=REL_DT_BC)
                if CLOS_DT_B !='':
                    Batch.objects.filter(id=rid).update(clos_dt_b=CLOS_DT_B)
                if B_UPDT_DT !='':
                    Batch.objects.filter(id=rid).update(b_updt_dt=B_UPDT_DT)
                if CLOS_DT_C !='':
                    Batch.objects.filter(id=rid).update(clos_dt_c=CLOS_DT_C) 
                old_num=list(Code.objects.filter(cd_type='M2',code='BRN').values('num_1').order_by('cd_type','code'))
                if len(old_num) >0:
                    old_num=old_num[0]['num_1']
                if num1 == old_num:
                    if  count== '1':       
                        a=0
                    else:
                        a=1
        lst=[a,STATUS,DIV,REL_DT_BC,Txtrel_date,B_UPDT_DT,REMARK]                        
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success:False"},status=400)      