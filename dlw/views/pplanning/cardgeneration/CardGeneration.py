from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/CardGeneration/')
def CardGeneration(request):
    context = {
        'ip':get_client_ip(request),
        'nav':g.nav,
        'subnav':g.subnav,
        'usermaster':g.usermaster,
    }
    if request.method=="POST":
        batch = request.POST.get('batchno')
        bval=request.POST.get('cardbutton')
        asmno=request.POST.get('asslyno')
        card = 'X'
        et = request.POST.get('ep_type')
        et=et.upper()
        lofr=request.POST.get('loco_fr')
        loto=request.POST.get('loco_to')
        bpe = request.POST.get('b_type')
        bpe=bpe.upper()
        bty=request.POST.get('b_qty')
        wkf1 = request.POST.get('wkf')
        alt = request.POST.get('ralt')
        bno1 = request.POST.get('brn_no')
        prtdt=datetime.datetime.now().strftime ("%Y-%m-%d")
        Batch1=Batch.objects.filter(part_no=asmno,bo_no=batch,brn_no=bno1).values('bo_no')
        if len(Batch1)==0:
            Batch.objects.create(bo_no=batch,part_no =asmno,ep_type =et,loco_fr =lofr,loco_to =loto,batch_qty =int(bty),batch_type =bpe,uot_wk_f =int(wkf1),brn_no =int(bno1),b_expl_dt=prtdt )
             
        ades=list(Part.objects.filter(partno = asmno).values('des').distinct()) 
       
        if len(ades)!=0:
            ades=ades[0]['des']
                         
        bat=Batch.objects.filter(part_no=asmno,bo_no=batch,brn_no=bno1).values('ep_type','brn_no','loco_to','loco_fr','batch_type','batch_qty','seq','uot_wk_f','version','rel_date')
        if len(bat)!=0:
            reldate=bat[0]['rel_date']
            epc=bat[0]['ep_type']
            version=bat[0]['version']
            brn=bno1
            l_to=bat[0]['loco_to']
            l_fr=bat[0]['loco_fr']
            seq=bat[0]['seq']
            bqty=bat[0]['batch_qty']
            btype=bat[0]['batch_type']
            DUE_WK=bat[0]['uot_wk_f']
             
        else:
            reldate=None
            epc=''
            brn=bno1
            l_to=''
            l_fr=''
            seq=''
            bqty=''
            btype=''
            DUE_WK=''
            version=''
        ep=''
        if reldate != None:
            messages.error(request, "This Batch No is Already Released. Can't Generate Again!!!")
            return render(request,'PPRODUCTION/CARDGENERATION/CardGeneration.html',context)
        for i in Code.objects.raw('select id,substr("NUM_1" :: text, 1,8) as num_1 from public."CODE" where "CD_TYPE"=%s and "CODE"=%s order by "CD_TYPE","CODE";',['11',epc]):
            ep=i.num_1
            break
        if ep=='':
            msg="No Such End Product"
        EP_PART= ep
        if ep ==asmno:
            NASSLY='1'
        else:
            NASSLY = str(CPQm14(asmno, epc, ep, l_to))
        u=0
        if DUE_WK != '':
            u=DUE_WK
        if u>3000:
            OUT_WK=(int(u/100)*52)+(u%100)
        else:
            OUT_WK=(int((u/100) + 100)*52)+(u%100)
        dt=[]
        DTS=batchExplode(request,asmno,'1',dt,epc,l_fr,l_to,'')
        if (btype == "R"):
            Tempm14expl.objects.filter(rm_partno__isnull=True).delete()
            DTS=list(Tempm14expl.objects.all())
            
        nom14 = 0
        check=M2Docnew1.objects.filter(batch_no=batch,assly_no=asmno,brn_no=brn).values('brn_no')
        print(check)
       
        if check.count()>0:
            M2Docnew1.objects.filter(batch_no=batch,assly_no=asmno,brn_no=brn).delete()
            M5Docnew1.objects.filter(batch_no=batch,assly_no=asmno,brn_no=brn).delete()
            M14M4new1.objects.filter(bo_no=batch,assly_no=asmno,brn_no=brn).delete()
        if batch and bval and asmno:
            cursor = connection.cursor()
            DTM2=DTS
            SCH='M'
            sch=''
            n=[]
            if (btype == "O" and alt == "F" and sch == "M"):
                return true
            if btype=="O":
                for i in range(len(DTM2)):
                    if DTM2[i]['ptc']  not in ['M','Z','C']:
                        n.append(i)
                    else:
                        DTM2[i].update({'del_fl':'','f_shopsec':'','rc_st_wk':'','scl_cl':'','cut_sher':'','m2sln':'','brn_no':'','m4_no':'',})                
            else:
                for i in range(len(DTM2)):
                    if DTM2[i]['ptc']  not in ['M','Z']:
                        n.append(i)
                    else:
                        DTM2[i].update({'del_fl':'','f_shopsec':'','rc_st_wk':'','scl_cl':'','cut_sher':'','m2sln':'','brn_no':'','m4_no':'',})                
            n.sort(reverse=True)
            for j in n:
                del DTM2[j]
            count = 1
            a=''
            b=''
            st=''
            for i in range(len(DTM2)):
                if alt == "F":
                    tm=list(M2Docnew1.objects.filter(~Q(scl_cl='T'),part_no=DTM2[i]["part_no"],brn_no=brn).values('scl_cl'))
                    if len(tm) > 0 :
                        DTM2[i]["del_fl"] = "Y"
                tm=list(Oprn.objects.filter(part_no=DTM2[i]["part_no"],del_fl__isnull=True).values('shop_sec').order_by('part_no','opn'))
                if len(tm)!=0:
                    tm=tm[0]['shop_sec']
                else:
                    tm=''
                if DTM2[i]["del_fl"] =="":
                    DTM2[i]["f_shopsec"] = tm
                if DTM2[i]["f_shopsec"] == "":
                    DTM2[i]["del_fl"] = "Y"
                r = 0
                o = 0
                s = 0
                if OUT_WK != '':
                    o = int(OUT_WK)
                sh=list(Shop.objects.filter(shop=DTM2[i]["f_shopsec"]).values('shop_ldt').order_by('shop'))
                if len(sh) != 0:
                    s=int(sh[0]['shop_ldt'])
                if DTM2[i]["del_fl"] == "":
                    d=int((o-s)/52)
                    r=((d % 100) * 100 + ((o - s) % 52))
                    DTM2[i]["rc_st_wk"] =r
                    DTM2[i]["scl_cl"] = scl_cl(s,alt,epc)
                if btype == "O" and alt == "F":
                    if (DTM2[i]["scl_cl"]!= ""):
                        if len(SCH) > 1:
                            st = SCH
                        else:
                            st = SCH
                        a= DTM2[i]["scl_cl"]
                        b= st
                        if a > b:
                            if DTM2[i]["del_fl"] == "":
                                DTM2[i]["del_fl"]="Y"
                        if DTM2[i]["scl_cl"] == "" and DTM2[i]["del_fl"] != "":
                            DTM2[i]["del_fl"] = "Y"
                        if DTM2[i]["rm_ptc"] == "R" and DTM2[i]["del_fl"] == "":
                            cuts=Cutpart.objects.filter(partno=DTM2[i]["part_no"],epc=epc).values('cut_dia').order_by('cut_dia','partno')
                            if len(cuts)>0:
                                DTM2[i]["cut_sher"] ==cuts[0]['cut_dia']
                            else:
                                DTM2[i]["cut_sher"] =''
                if DTM2[i]["del_fl"] == "":
                    DTM2[i]["m2sln"] = i+1
                    DTM2[i]["del_fl"] = "B"
            import copy
            start_with=0
            DTM4 = copy.deepcopy(DTM2)
            _sn = 0
            sch='X'
            if (btype == "O" and alt == "F" and sch == "M"):
                return True
            DTM4=list(filter(lambda x: (x['rm_partno'] !='' and x['m2sln']!=''),DTM4))
            if (alt == "T"):
                for i in range(len(DTM4)):
                    DTM4[i].update({'pm_no':XXALT,'assly_no':EP_PART})                
            else:
                for d in DTM4:
                    d['pm_no'] = d.pop('f_shopsec')
                for i in range(len(DTM4)):
                    DTM4[i].update({'assly_no':asmno})  
            Tempm14M4new.objects.all().delete()
            r = 0
            for i in range(len(DTM4)):
                if (DTM4[i]["cut_sher"] != ""):
                    continue
                InsrtQry = ""
                if DTM4[i]["ptc"]!="C":
                    rmpart=DTM4[i]["rm_partno"]
                else:
                    rmpart=DTM4[i]["m2sln"]

                if DTM4[i]["ptc"]=="C":
                    qt=DTM4[i]["rm_qty"]
                    doci="C"
                else:
                    qt=float(DTM4[i]["rm_qty"])*float(DTM4[i]["qty"])*float(bqty)
                    doci=DTM4[i]["rm_ptc"]
                Tempm14M4new.objects.create(doc_code='88',rm_part =rmpart ,pm_no = DTM4[i]["pm_no"],part_no = DTM4[i]["rm_partno"],qty = qt,l_fr =l_fr ,l_to = l_to,bo_no = batch,assly_no = DTM4[i]["assly_no"],seq =seq ,due_wk = DTM4[i]["rc_st_wk"],brn_no = brn,doc_ind =doci ,epc = epc)
                r = r + 1
            if (r > 0):
                if (btype != "O"):
                    cursor.execute('''select count(*) from (select t.*, p."SHOP_UT" unit from  (select max("DOC_CODE") doc_code, "PM_NO", "RM_PART",max("RM_PART") part_no,sum("QTY"),max("L_FR") l_fr,max( "L_TO") l_to, 
                    max("BO_NO") bo_no,max("ASSLY_NO") assly_no,max("SEQ") seq,min("DUE_WK") due_wk,max("BRN_NO") brn_no,max("EPC") epc,max("DOC_IND") doc_ind 
                    from public.dlw_tempm14m4new where trim("DOC_IND")<>'C' group by "PM_NO", "RM_PART" order by "PM_NO", "RM_PART") t,public."PART" p where trim(p."PARTNO")=trim(t.part_no)) foo ;''')
                    SrchQry=list(cursor.fetchall())
                else:
                    cursor.execute('''select count(*) from (select t.*, p."SHOP_UT" unit from  (select max("DOC_CODE") doc_code, "PM_NO", "RM_PART",max("RM_PART") part_no,sum("QTY"),max("L_FR") l_fr,max( "L_TO") l_to, 
                    max("BO_NO") bo_no,max("ASSLY_NO") assly_no,max("SEQ") seq,min("DUE_WK") due_wk,max("BRN_NO") brn_no,max("EPC") epc,max("DOC_IND") doc_ind 
                    from public.dlw_tempm14m4new group by "PM_NO", "RM_PART" order by "PM_NO", "RM_PART") t,public."PART" p where trim(p."PARTNO")=trim(t.part_no)) foo ;''')
                    SrchQry=list(cursor.fetchall())
                snm4 = "0"
                snm4 = len(SrchQry)
                nm4 = snm4
                _sn = updtcodem14(nm4+nom14, "21", "M14","m4")
                if (_sn != 0):
                    if (nm4 > 0):
                        m4fr= _sn + 1+nom14
                        m4to= _sn + nm4+nom14
                snm = _sn +nom14
                start_with = snm + 2
                cursor.execute('''ALTER SEQUENCE M4SEQ RESTART WITH %s''',[start_with])
                if btype == "O":
                    cursor.execute('''insert into public."M14M4NEW1" select nextval('id'),doc_code,nextval('M4SEQ') doc_no,"PM_NO",part_no,qty,l_fr,l_to,bo_no,assly_no,
                    seq,due_wk,CURRENT_DATE as prd_dt,brn_no,doc_ind,unit,epc ,null as version,null as stage,null as wrd_no,null as finyear ,
                    null as vr_no,null as kit_ind,null as station,null as stg,null as sub_kit,null as opn_no, 0 as kit_no,
                    null as status,0 as sub_docno,null as lieu_part,null as drawn_by,null as mark,null as del_fl,0 as doc_no_old,
                    null as epc_old,NULL AS "RECEIVED_MAT",NULL AS "ISSUED_QTY",NULL AS "RECEIVED_QTY", NULL AS "REMARKS",NULL AS "LINE", 
                    NULL AS "CLOSING_BAL",0 AS "LASER_PST",0 AS "POSTED_DATE",0 AS "WARDKP_DATE",0 AS "SHOPSUP_DATE",0 AS "POSTED1_DATE", 
                    NULL AS "RECEIVED_MAT14",NULL AS "ISSUED_QTY14",NULL AS "RECEIVED_QTY14",NULL AS "REMARKS14",NULL AS "LINE14",NULL AS "CLOSING_BAL14",
                    0 AS "LASER_PST14",0 AS "POSTED_DATE14",0 AS "WARDKP_DATE14",0 AS "SHOPSUP_DATE14",0 AS "POSTED1_DATE14"
                    from  (select t.*, p."SHOP_UT" unit from  (select max("DOC_CODE") doc_code, "PM_NO", "RM_PART",max("RM_PART") part_no,sum("QTY") qty,max("L_FR") l_fr,max( "L_TO") l_to, 
                    max("BO_NO") bo_no,max("ASSLY_NO") assly_no,max("SEQ") seq,min("DUE_WK") due_wk,max("BRN_NO") brn_no,max("EPC") epc,max("DOC_IND") doc_ind 
                    from public.dlw_tempm14M4new group by "PM_NO", "RM_PART" order by "PM_NO", "RM_PART") t,public."PART" p where trim(p."PARTNO")=trim(t.PART_NO) order by t."PM_NO", t."RM_PART")o;''')
                        
                else:
                    cursor.execute('''insert into public."M14M4NEW1" select nextval('id'),doc_code,nextval('M4SEQ') doc_no,"PM_NO",part_no,qty,l_fr,l_to,bo_no,assly_no,
                        seq,due_wk,CURRENT_DATE as prd_dt,brn_no,doc_ind,unit,epc ,null as version,null as stage,null as wrd_no,null as finyear ,
                        null as vr_no,null as kit_ind,null as station,null as stg,null as sub_kit,null as opn_no, 0 as kit_no,
                        null as status,0 as sub_docno,null as lieu_part,null as drawn_by,null as mark,null as del_fl,0 as doc_no_old,
                        null as epc_old,NULL AS "RECEIVED_MAT",NULL AS "ISSUED_QTY",NULL AS "RECEIVED_QTY", NULL AS "REMARKS",NULL AS "LINE", 
                        NULL AS "CLOSING_BAL",0 AS "LASER_PST",0 AS "POSTED_DATE",0 AS "WARDKP_DATE",0 AS "SHOPSUP_DATE",0 AS "POSTED1_DATE", 
                        NULL AS "RECEIVED_MAT14",NULL AS "ISSUED_QTY14",NULL AS "RECEIVED_QTY14",NULL AS "REMARKS14",NULL AS "LINE14",NULL AS "CLOSING_BAL14",
                        0 AS "LASER_PST14",0 AS "POSTED_DATE14",0 AS "WARDKP_DATE14",0 AS "SHOPSUP_DATE14",0 AS "POSTED1_DATE14"
                        from  (select t.*, p."SHOP_UT" unit from  (select max("DOC_CODE") doc_code, "PM_NO", "RM_PART",max("RM_PART") part_no,sum("QTY") qty,max("L_FR") l_fr,max( "L_TO") l_to, 
                        max("BO_NO") bo_no,max("ASSLY_NO") assly_no,max("SEQ") seq,min("DUE_WK") due_wk,max("BRN_NO") brn_no,max("EPC") epc,max("DOC_IND") doc_ind 
                        from public.dlw_tempm14M4new where trim("DOC_IND")<>'C' group by "PM_NO", "RM_PART" order by "PM_NO", "RM_PART") t,public."PART" p where trim(p."PARTNO")=trim(t.PART_NO) order by t."PM_NO", t."RM_PART")o;''')
                                   
                    for i in range(len(DTM2)):
                        m2s = 0
                        if DTM2[i]["m2sln"] != "":
                            m2s = int(DTM2[i]["m2sln"])
                        m4n=""
                        if alt == "T" and DTM2[i]["ptc"] != "C" and DTM2[i]["cut_sher"]== "" and m2s> 0:
                            a=list(Tempm14M4new.objects.filter(pm_no='XXALT',rm_part=DTM2[i]["rm_partno"]).values('doc_no').order_by('pm_no','rm_part'))
                            if len(a)>0:
                                m4n=a[0]['doc_no']
                        if alt == "F" and DTM2[i]["ptc"] != "C" and DTM2[i]["cut_sher"] == "" and m2s > 0:
                            a=list(Tempm14M4new.objects.filter(pm_no=DTM2[i]["f_shopsec"],rm_part=DTM2[i]["rm_partno"]).values('doc_no').order_by('pm_no','rm_part'))
                            if len(a)>0:
                                m4n=a[0]['doc_no']
                        if alt == "T" and DTM2[i]["ptc"] == "C" and DTM2[i]["cut_sher"] == "" and m2s > 0:
                            a=list(Tempm14M4new.objects.filter(pm_no=DTM2[i]["f_shopsec"],rm_part=DTM2[i]["m2sln"]).values('doc_no').order_by('pm_no','rm_part'))
                            if len(a)>0:
                                m4n=a[0]['doc_no']
                        if alt == "F" and DTM2[i]["ptc"] == "C" and DTM2[i]["cut_sher"] == "" and m2s > 0:
                            a=list(Tempm14M4new.objects.filter(pm_no='XXALT',rm_part=DTM2[i]["rm_partno"]).values('doc_no').order_by('pm_no','rm_part'))
                            if len(a)>0:
                                m4n=a[0]['doc_no']
                        if m4n != "":
                            DTM2[i]["m4_no"] = m4n
                        else:
                            DTM2[i]["m4_no"] = "999999"
            if (alt == "T"):
                cla = EP_PART
            else:
                cla = asmno
            for i in range(len(DTM4)):
                    DTM4[i].update({'assly_no':cla}) 
            dvm=list(filter(lambda x:(x['del_fl']=='B'),DTM2))
            d = dvm
            snm2 = 0
            snm2 = len(d)
            nm2 = snm2
            _sn = 0
            _sn = updtcodem14(nm2, "21", "M2", "m2")
            nom2 = _sn
            if (_sn != 0):
                if (nm2 > 0):
                    m2fr = int (_sn) + 1
                    m2to = int(_sn )+ nm2
            snm2 = len(DTM2)
        
            TempM5Docnew.objects.all().delete()
            c = 0
            ds=[]
            pn = ""
            pn_r = ""
            pr_shopsec = ""
            rm_unit=""
            pt_shop=""
            b_type=""
            prt_batch=""
            total_qty=0
            locoqty=0
            docqty = 0
            cardqty = 0
            n_shopsec=""
            lfri = ""
            pa = "00.00"
            sch = ""
            if len(SCH) > 0:
                sch = SCH[0:1]
            sch='K'
            if (btype == "O" and alt == "F" and sch == "M"):
                return true
            DTM5 = copy.deepcopy(DTM2)
            m2assly = ""
            if (alt == "T"):
                m2assly = EP_PART
            else:
                m2assly = asmno
            for i in range(len(DTM5)):
                pn = DTM5[i]["part_no"]
                obj=Oprn.objects.filter(part_no=pn,del_fl__isnull=True).values('shop_sec')	
                if (DTM5[i]["del_fl"] != "B" or len(obj)==0):
                    continue
                pn_r = DTM5[i]["rm_partno"]
                pr_shopsec = ""
                obj=Part.objects.filter(partno=pn_r).values('shop_ut').order_by('partno')
                pt_shop=''
                if len(obj)>0:
                    pt_shop=obj[0]['shop_ut']
                if(DTM5[i]["rm_partno"]=="" or pt_shop==""):
                    rm_unit=""
                else:
                    rm_unit=pt_shop
            
                cursor.execute('''select "SHOP_SEC", "PART_NO",trim("M5_CD"),to_char(coalesce("PA",0),'00.00') pa ,to_char(coalesce("AT",0),'000.00')as at,"LC_NO","OPN" ,
                substr(trim("DES"),1,30) des,substr("LOT"::text,1,2) lot from public."OPRN" where trim("PART_NO")=%s and coalesce("NCP_JBS",'#')='#'  
                and coalesce("DEL_FL",'#')='#' order by "PART_NO","OPN";''',[pn])
                ds=list(cursor.fetchall())
                for  j in range(len( ds)):
                    if (btype=="R"):
                        obj=Batch.objects.filter(bo_no=batch).values('batch_type').order_by('brn_no')
                        if len(obj)>0:
                            b_type=obj[0]['batch_type']
                    else:
                        obj=Batch.objects.filter(bo_no=DTM5[i]["brn_no"]).values('batch_type').order_by('brn_no')
                        if len(obj)>0:
                            b_type=obj[0]['batch_type']
                    
                    prt_batch = batch
                    if(DTM5[i]["ptc"])!="C":
                        total_qty=float(DTM5[i]["qty"])* float(bqty)
                    else:
                        total_qty=DTM5[i]["qty"]

                    opn = ds[j][6]
                    cursor.execute('''select  "SHOP_SEC","PART_NO","M5_CD",to_char(coalesce("PA",0),'00.00') pa ,to_char(coalesce("AT",0),'000.00')as at,
                    "LC_NO","OPN" ,substr(trim("DES"),1,30) des,substr("LOT" :: text,1,2) lot from public."OPRN" where trim("PART_NO")=%s and "OPN" :: int>%s 
                    and coalesce("DEL_FL",'#')='#' order by "PART_NO", "OPN";''',[pn,opn])
                    dso=list(cursor.fetchall())
                    n_shopsec=nextshop(dso,j,pn)
                    if (ds[j][2]== "5"):
                        ii = 0
                        locoqty = float(DTM5[i]["qty"]) * float(NASSLY)
                        if (total_qty > locoqty):
                            cardqty = max(math.ceil(total_qty / 5), locoqty )
                        else:
                            cardqty = total_qty
                        lfri =l_fr.zfill(4) if btype == "O" else ""
                        while (total_qty > 0):
                            docqty = total_qty if total_qty < cardqty else cardqty
                            pa = "00.00"
                            if (b_type == "R"):
                                if (docqty > locoqty * 2):
                                    pa = ds[j][3]
                            p=pa if btype =="R" else ds[j][3]
                            cursor.execute('''INSERT INTO public.dlw_tempm5docnew(
                            "SCL_CL", "BATCH_NO", "ASSLY_NO", "PART_NO", "M2SLNO", "RM_PARTNO", "RM_UT", "CUT_SHEAR", "RM_QTY", "SHOP_SEC", "LC_NO", "OPN",
                            "OPN_DESC", "PA", "AT", "NO_OFF", "M5_CD", "PR_SHOPSEC", "N_SHOPSEC", "QTY_ORD", "TOT_RM_QTY", "L_FR", "L_TO", "M5GLSN",
                            "M5PRTDT", "SEQ", "BRN_NO", "MARK", "DEL_FL", "STATUS")
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE,%s,%s,%s,%s,%s);''',[DTM5[i]["scl_cl"], prt_batch , m2assly , ds[j][1],None,DTM5[i]["rm_partno"],rm_unit,DTM5[i]["cut_sher"],
                            DTM5[i]["rm_qty"],ds[j][0],ds[j][5], ds[j][6],ds[j][7], p ,ds[j][4],ds[j][8], 
                            ds[j][2],pr_shopsec ,n_shopsec,docqty,docqty * float(DTM5[i]["rm_qty"]),lfri,lfri,000000, seq, brn,'','',''])
                            
                            c = c + 1
                            total_qty = total_qty - cardqty
                            ii = ii + 1
                            if (btype == "O" and ii < 5):
                                lfri =str (int(l_fr) + ii).zfill(4)
                            else:
                                lfri = ""
                    else:
                        pa = "00.00"
                        locoqty = float(DTM5[i]["qty"]) * float(NASSLY)
                        if (b_type == "R"):
                            if (total_qty > locoqty * 2):
                                pa = ds[j][3]
                        lt = ""
                        lf = ""
                        if (btype == "O"):
                            lf = l_fr
                            lt = l_to
                        p =pa if btype == "R" else ds[j][3]
                        cursor.execute('''INSERT INTO public.dlw_tempm5docnew(
                        "SCL_CL", "BATCH_NO", "ASSLY_NO", "PART_NO", "M2SLNO", "RM_PARTNO", "RM_UT", "CUT_SHEAR", "RM_QTY", "SHOP_SEC", "LC_NO", "OPN",
                        "OPN_DESC", "PA", "AT", "NO_OFF", "M5_CD", "PR_SHOPSEC", "N_SHOPSEC", "QTY_ORD", "TOT_RM_QTY", "L_FR", "L_TO", "M5GLSN",
                        "M5PRTDT", "SEQ", "BRN_NO", "MARK", "DEL_FL", "STATUS")
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE,%s,%s,%s,%s,%s);''',[DTM5[i]["scl_cl"], prt_batch , m2assly ,
                        ds[j][1],None,DTM5[i]["rm_partno"],rm_unit,DTM5[i]["cut_sher"],
                        DTM5[i]["rm_qty"],ds[j][0],ds[j][5], ds[j][6],ds[j][7], p ,ds[j][4],ds[j][8], 
                        ds[j][2],pr_shopsec ,n_shopsec,total_qty,total_qty * float(DTM5[i]["rm_qty"]),lf,lt,000000, seq, brn,'','',''])
                        
                        c= c + 1
                    pr_shopsec = ds[j][0]
            DTM2S = copy.deepcopy(DTM2)
            start_with -=1
            for d in range(len(DTM2S)):
                m4s = ""
                if (DTM2S[d]["rm_partno"]!= ""):#//previously done 9999 forcefully for order by in table
                    m4s = start_with+1
                    start_with +=1
                m2n = nextsn(int(nom2) + d)
                if (DTM2S[d]["ptc"] != "C"):
                    DTM2S[d]["qty"] =float(DTM2S[d]["qty"]) * float(bqty)
                if (DTM2S[d]["del_fl"] == "B"):
                    #InsrtQry = "";
                    cursor.execute('''insert into public."M2DOCNEW1"("SCL_CL","BATCH_NO","ASSLY_NO","F_SHOPSEC","PART_NO","PTC","QTY","RM_PARTNO","RM_QTY","RC_ST_WK","RM_PTC","CUT_SHEAR","M2SLN",
                    "M2PRTDT","SEQ","BRN_NO","M4_NO","EPC","VERSION")values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE,%s,%s,%s,%s,%s);''',[DTM2S[d]["scl_cl"], batch,m2assly,DTM2S[d]["f_shopsec"],DTM2S[d]["part_no"],DTM2S[d]["ptc"], DTM2S[d]["qty"]
                    , DTM2S[d]["rm_partno"],DTM2S[d]["rm_qty"],DTM2S[d]["rc_st_wk"],DTM2S[d]["rm_ptc"],DTM2S[d]["cut_sher"], m2n ,
                    seq,brn, m4s ,epc,version])
                    
                
            nm5 = c
            m5fr=0
            _sn = updtcodem14(nm5, "21", "M5", "m5")
            if (_sn != 0):
                if (nm5 > 0):
                    m5fr= (_sn + 1)
                    m5to = (_sn + nm5)
            else:
                return False
            cnt = 0
            temp=list(TempM5Docnew.objects.values('id').order_by('scl_cl','shop_sec','part_no','opn','l_fr'))
            ds = temp
            temp = m5fr
            for k in range(len(ds)):
                TempM5Docnew.objects.filter(id=ds[k]['id']).update(m5glsn=temp)
               
                temp = int(temp) + 1
            selQry=M2Docnew1.objects.filter(brn_no=brn).values('batch_no','assly_no','part_no','m2sln').order_by('scl_cl','batch_no','assly_no','part_no')
            dsU = list(selQry)
            
            for i in range(len(dsU)):
                TempM5Docnew.objects.filter(batch_no=dsU[i]["batch_no"],assly_no=dsU[i]["assly_no"],part_no=dsU[i]["part_no"]).update(m2slno=dsU[i]["m2sln"])
               

            
            cursor.execute('''insert into public."M5DOCNEW1"("SCL_CL", "BATCH_NO", "ASSLY_NO", "PART_NO", "M2SLNO", "RM_PARTNO", "RM_UT", "CUT_SHEAR", "RM_QTY", "SHOP_SEC", "LC_NO", "OPN", "OPN_DESC", "PA", "AT", "NO_OFF", "M5_CD", "PR_SHOPSEC", "N_SHOPSEC", "QTY_ORD", "TOT_RM_QTY", "L_FR", "L_TO", "M5GLSN", "M5PRTDT", "SEQ", "BRN_NO", "MARK", "DEL_FL", "STATUS") select "SCL_CL", "BATCH_NO", "ASSLY_NO", "PART_NO", "M2SLNO", "RM_PARTNO", "RM_UT", "CUT_SHEAR", "RM_QTY", "SHOP_SEC", "LC_NO", "OPN", "OPN_DESC", "PA", "AT", "NO_OFF", "M5_CD", "PR_SHOPSEC", "N_SHOPSEC", "QTY_ORD", "TOT_RM_QTY", "L_FR", "L_TO", "M5GLSN", "M5PRTDT", "SEQ", "BRN_NO", "MARK", "DEL_FL", "STATUS" from public.dlw_tempm5docnew;''')
             
            noM5Rej = m5fr+cnt
          
            import pandas as pd
            dtm=[]
            dt=[]
            res = []
            makesetm14(epc)
            cursor.execute('select t.*,p."M14SPLT_CD",COALESCE(p."ALLOW_PERC",0) as allow_perc,COALESCE(p."SHOP_UT", %s) as shop_ut from public.dlw_tempm14expl t,public."PART" p where (t."PTC"= %s or t."PTC"= %s or t."PTC"= %s) and t."PART_NO"= p."PARTNO" and t."QTY" >0;',['0','P','L','B'])
            row = cursor.fetchall()
            dts = pd.DataFrame(list(row))
            sch = card[:1]
            if alt=='F' and sch=='M' and btype=='O':
                messages.error(request,'M14 is not generated as alternate is "False" and batch type is "O"')
                return render(request,'PPRODUCTION/CARDGENERATION/CardGeneration.html')
            for i in range(len(dts)):
                allowqty=0
                # kamlesh
                if (alt=='F' and len(M14M4new1.objects.filter(~Q(pm_no='XXALT'), part_no=dts[1][i],brn_no=brn,l_fr=l_fr).values('pm_no'))!=0):
                    continue
                
                pn = dts[1][i]
                totqty = float(dts[2][i]) * float(bqty)
                locoqty = float(dts[2][i]) * float(NASSLY)
                ptsplt = ""
                ptsp_ut = ""
                pt_alp = 0
                ptsplt = dts[7][i]
                ptsp_ut = dts[9][i]
                pt_alp = dts[8][i]
                if ptsplt == "5":
                    tosplit = True
                else:
                    tosplit = False
                docind = dts[3][i]
                cursor.execute('select coalesce("AUTH_QTY",0),"PM_NO" from public."PROGPART" where "PARTNO"=%s and "EPC"=%s and coalesce("DEL_FL",%s) !=%s order by "PARTNO", "EPC", "PM_NO";',[pn,epc,'@','Y'])
                row = cursor.fetchall()
                ds= pd.DataFrame(list(row))
                j = 0
                while totqty > 0 and j < len(ds) and alt == "F": 
                    pmqty=0
                    pmno=''                
                    if btype== "O":
                        if ds[0][j] <= totqty:
                            pmqty = ds[0][j] 
                        else:
                            pmqty = totqty
                        pmno = ds[1][j]
                    else:
                        pmqty = totqty
                        pmno = m14btdesc(btype)
                    import numpy as np
                    if float(ptsp_ut) < 10:
                        allowqty = round(float(pmqty) * float(pt_alp) / 100, 0)
                    else:
                        allowqty = round(float(pmqty) * float(pt_alp) / 100, 3)
                    if tosplit is False:
                        if btype=='O':
                            l=l_fr.zfill(4)
                            t=l_to.zfill(4)
                        else:
                            l=''
                            t=''
                        dtm=write_row_expl_m14(pmno, pn, (float(pmqty) + float(allowqty)), l, t, docind, ptsp_ut, dtm)
                        totqty = float(totqty) - float(pmqty)
                    else:
                        ii = 0
                        lfri=''
                        vLfri = l_fr.zfill(4)
                        if btype=='O':
                            lfri=l_fr.zfill(4)
                        while float(pmqty) > float(locoqty):
                            dtm=write_row_expl_m14(pmno, pn, float(locoqty), lfri, lfri, docind, ptsp_ut, dtm)
                            pmqty = float(pmqty) - float(locoqty)
                            totqty = float(totqty) - float(locoqty)
                            ii = ii + 1
                            if btype=='O' and ii < 5:
                                lfri=(str(int(vLfri)+1)).zfill(4)
                                lfri=lfri.zfill(4)
                            else:
                                lfri=''
                            vLfri = lfri.zfill(4)
                        vLfri = l_fr.zfill(4)
                        if float(pmqty) > 0:
                            dtm=write_row_expl_m14(pmno, pn, float(pmqty) + float(allowqty), lfri, lfri, docind, ptsp_ut, dtm)
                            totqty = float(totqty) - float(pmqty)
                    j = j + 1

                if float(totqty) > 0:
                    lfri = ""
                    if alt=='F':
                        if int(ptsp_ut) < 10:
                            allowqty = round(float(totqty) *float(pt_alp) / 100, 0)
                        else:
                            allowqty = round(float(totqty) * float(pt_alp) / 100, 3)
                        abc=float(totqty) + float(allowqty)
                        abc="{0:.4f}".format(abc)
                        dtm=write_row_expl_m14("XX999", pn, abc, l_fr, l_to, docind, ptsp_ut, dtm)
                    else:
                        lfri = l_fr.zfill(4)
                        while tosplit is True and float(totqty) > float(locoqty) and int(lfri) <= int(l_to.zfill(4)):
                            if float(ptsp_ut) < 10:
                                allowqty = round(float(locoqty) * float(pt_alp) / 100, 0)
                            else:
                                allowqty = round(float(locoqty) * float(pt_alp) / 100, 3)
                            dtm=write_row_expl_m14("XXALT", pn, float(locoqty) + float(allowqty), lfri, lfri, docind, ptsp_ut, dtm)
                            totqty = float(totqty) - float(locoqty)
                            lfri = (str(int(lfri) + 1)).zfill(4)

                        if (float(totqty) > 0 and int(lfri) <= int(l_to.zfill(4))):
                            if float(ptsp_ut) < 10:
                                allowqty = round(float(totqty) * float(pt_alp )/ 100, 0)
                            else:
                                allowqty = round(float(totqty) * float(pt_alp )/ 100, 3)
                            dtm=write_row_expl_m14("XXALT", pn, float(totqty) + float(allowqty), lfri, l_to.zfill(4), docind, ptsp_ut, dtm)

                    
            dtm=sorted(dtm, key = lambda i: i['part_no'])
            nm14 = len(dtm)
            print('kk',nm14 )
            nom14 = nm14
            _sn=updtcodem14(nm14,"21","M14","m14")
            if _sn != 0:
                sn = _sn
                for q in range(len(dtm)):
                        sn = sn + 1
                        if alt=='T':
                            ash=EP_PART
                        else:
                            ash=asmno
                        

                        if (float(dtm[q]['qty']) > 0) and  ( dtm[q]['l_to'] !=''  ):  
                            M14M4new1.objects.create(doc_code='89',doc_no=sn,pm_no=dtm[q]['pm_no'],part_no=dtm[q]['part_no'],qty=dtm[q]['qty'],l_fr=dtm[q]['l_fr'],l_to=dtm[q]['l_to'],bo_no=batch,assly_no=ash,seq=seq,due_wk=DUE_WK,brn_no=brn,doc_ind=dtm[q]['doc_ind'],unit=dtm[q]['unit'],epc=epc,prtdt=datetime.datetime.now().strftime ("%d-%m-%Y"))

                  
            if bval=="Generate Cards":
                dtm=[]
                dt=[]
                res = [] 
        messages.success(request, 'Card generated Successfully!')
    return render(request,'PPRODUCTION/CARDGENERATION/CardGeneration.html',context)



def nextshop(dso,j,pn):
    if (len(dso)== 0):
        return ""
    else:
        return dso[0][0]
def nextsn(sn):
    return (sn + 1)
    
def cardexpl(request,pn,wt,dt,tepc,tlr,tlt,tver):
    lfr='0'
    lto='0'

    srchqry=list(Nstr.objects.filter(pp_part=pn,epc=tepc).values('ptc','ref_ind','ref_no','qty','cp_part','l_fr','l_to','alt_ind',).order_by('cp_part','epc'))
    for i in range(len(srchqry)):
        if tlr is not None:
            lfr=tlr
        if tlt is not None:
            lto=tlt           
        if (not (srchqry[i]['l_fr'] <= lfr and lto <= srchqry[i]['l_to']) or ( srchqry[i]['alt_ind']  is not None) ):
            continue
        Eptc=srchqry[i]['ptc']
        Erefind=srchqry[i]['ref_ind']
        Erefno=srchqry[i]['ref_no']
        Cpprt=srchqry[i]['cp_part']
        qty=float(srchqry[i]['qty'])
        wt=int(wt)
        # if Eptc!='Q' and Eptc!='R':        
        vale=["Q","R"]  
        if ((Eptc not in vale)): 
            if (Eptc == "P" and Erefind == "S" and ((Erefno  is not None)  or (Erefno != "0"))):
                Cpprt = Erefno
            if ((tver == "0" or tver == "") or (not tepc) ):
                dt=write_row_expl(Cpprt, qty*wt, Eptc,"",0.0,"", dt)
        else:
            dt=write_row_expl_r(Cpprt,qty,Eptc, dt) 

        mcp_part=srchqry[i]['cp_part']
        mqty = float(qty)
        c =  Nstr.objects.filter(pp_part=mcp_part,epc=tepc).values('pp_part') 
        # print('pp_part',c)
        # print('pp_part',c[0]['pp_part'])
        valeptc=['M','Z']
        if ((Eptc in valeptc) and (len(c)!=0)) :
            if (tver == "0" or tver == ""):
                cardexpl(request,mcp_part, mqty * wt, dt,tepc,tlr,tlt,tver)
    return dt
    


def write_row_expl(one, two, three,four,  five,  six,  dt):
    dt.append({'part_no':one,'qty':two,'ptc':three,'rm_partno':four,'rm_qty':five,'rm_ptc':six})
    return dt

def write_row_expl_m14(one, two, three,four,  five,  six,seven, dtm):
    dtm.append({'pm_no':one,'part_no':two,'qty':three,'l_fr':four,'l_to':five,'doc_ind':six,'unit':seven})
    return dtm

def write_row( one, two, dt):
        dt.append({'part':one,'wt':two})
        return dt

def write_row_expl_r(four,  five, six, dt):
    indx= len(dt)
    dt[indx - 1]["rm_partno"] = four
    dt[indx - 1]["rm_qty"] = five
    dt[indx - 1]["rm_ptc"] = six
    return dt

from functools import reduce
from operator import itemgetter
def batchExplode(request,pn,wt, dt1,tepc,tlr,tlt,tver):
    dt2=write_row_expl(pn, 1.0, "M", "", 0.0, "", dt1)
    dt=cardexpl(request,pn,wt, dt2,tepc,tlr,tlt,tver)
    a=[]
    lst=[]
    Tempm14expl.objects.all().delete()
    print('kamlesh list1',len(dt))
    for i in range(len(dt)):
        if dt[i]['part_no'] not in a:
            a.append(dt[i]['part_no'])
            ls=list(filter(lambda x:str(x['part_no']) in str(dt[i]['part_no']),dt))
             
            if len(ls) > 1:
                ls1=list(map(itemgetter('qty'),ls))
                ls2=list(map(itemgetter('ptc'),ls))
                ls3=list(map(itemgetter('rm_partno'),ls))
                ls4=list(map(itemgetter('rm_qty'),ls))
                ls5=list(map(itemgetter('rm_ptc'),ls))
                qty="{0:.3f}".format(reduce(lambda x,y:x + y,ls1))
                ptc=max(ls2)
                rpa=max(ls3)
                rpt=max(ls5)
                rqt=max(ls4)
                rqt="{0:.3f}".format(rqt)
                Tempm14expl.objects.create(part_no=dt[i]['part_no'], qty=qty, ptc=ptc, rm_partno=rpa, rm_qty=rqt, rm_ptc=rpt)
                lst.append({'part_no':dt[i]['part_no'],'qty':qty,'ptc':ptc,'rm_partno':rpa,'rm_qty':rqt,'rm_ptc':rpt})
            else:
                Tempm14expl.objects.create(part_no=dt[i]['part_no'], qty="{0:.3f}".format(dt[i]['qty']), ptc=dt[i]['ptc'], rm_partno=dt[i]['rm_partno'], rm_qty="{0:.3f}".format(dt[i]['rm_qty']), rm_ptc=dt[i]['rm_ptc'])
                lst.append({'part_no':dt[i]['part_no'],'qty':"{0:.3f}".format(dt[i]['qty']),'ptc':dt[i]['ptc'],'rm_partno':dt[i]['rm_partno'],'rm_qty':"{0:.3f}".format(dt[i]['rm_qty']),'rm_ptc':dt[i]['rm_ptc']})
    lst=sorted(lst, key = lambda i: i['part_no'])
    return lst

def m14btdesc(bt):
    if bt=='O':
        return 'ORD'
    elif bt=='S':
        return 'STKS'
    elif bt=='R':
        return 'REPL'
    elif bt=='B':
        return 'BAL'
    elif bt=='N':
        return 'NRC'
    elif bt=='M':
        return 'MISC'
    else:
        return ''

def CPQm14( _pn, _ep, _epn, _lto):
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
            Dss=implm14(_pn, "1", _ep, dt, _epn,_lto)
            for i in range(len(Dss)):
                if str(Dss[i]["part"]) == _epn:
                    q1 = 0
                    if str(Dss[i]["wt"]) != "":
                        q1 = float(Dss[i]["wt"])
                    q = q + q1
        return q

def implm14( _pn,  wt, _ep, dt, _epn, _lt):
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
                    implm14(mpp_part, str(val), _ep, dt, _epn,_lt)
            return dt
        return dt

def makesetm14(tepc):
    date=datetime.datetime.now()
    ds=list(Setmast.objects.filter((Q(valid_upto__isnull=True)|Q(valid_upto__gte=date)),epc=tepc,rec_ind__isnull=True).values('part_no','qty','set_part').order_by('epc','set_part','part_no'))
    dst=[]
    for i in range(len(ds)):
            setpart1 = ds[i]["set_part"]
            setqty1 = float(ds[i]["qty"])
            dst = list(Setmast.objects.filter((Q(valid_upto__isnull=True)|Q(valid_upto__gte=date)),epc=tepc,rec_ind__isnull=True,set_part=setpart1).values('part_no','qty').order_by('epc','set_part','part_no'))
            if (print(makesetonem14("check", dst, setpart1, setqty1)) == True):
                makesetonem14("update", dst, setpart1, setqty1)
    return True
from django.db.models import F
def makesetonem14( act, DTF, msetpart1, msetqty1):
    ret = True
    rowid = ""
    for j in range(len(DTF)):
        rowid = list(Tempm14expl.objects.filter(part_no=DTF[j]['part_no']).values('id').order_by('part_no'))
        if len(rowid) ==0:
            return False
        else:
            rowid=rowid[0]['id']
        if act == "update":
            Tempm14expl.objects.filter(id=rowid).update(qty=F('qty') - DTF[j]['qty'])
    if act == "update":
        Tempm14expl.objects.create(part_no=msetpart1,qty=msetqty1,ptc='P')
    return True 
           
def updtcodem14( nm, cdt, cd, fname):
    num1 = list(Code.objects.filter(cd_type=cdt,code=cd).values('num_1').order_by('cd_type','code'))
    if len(num1) == 0:
        return 0

    num_1=int(num1[0]['num_1'])    
    new_num=int(num1[0]['num_1'])     
    new_num = new_num + nm
    if ((new_num + nm) > 899000):
        Code.objects.filter(cd_type=cdt,code=cd).update(num_1=100001) 
    
    Code.objects.filter(cd_type=cdt,code=cd).update(num_1=new_num) 
    old_num = list(Code.objects.filter(cd_type=cdt,code=cd).values('num_1').order_by('cd_type','code'))   
            
    if len(old_num)==0:
        old_num=0
    else:        
        old_num=old_num[0]['num_1']
        
    if new_num == old_num:
        if fname == "m14":
            m14fr = num_1 + 1
            m14to = new_num
        return  num_1
    else:
        updtcodem14(nm, cdt, cd,fname)
    return num_1

def scl_cl(ltd,alt,epc):
        if alt == "T":
            return "T"
        ls=["01","02","05","1A","1C","1F"]
        if epc in ls:
            if ltd>35:
                return "A"
            if ltd>25:
                return "B"
            return "C"
        else:
            if ltd>25:
                return "A"
            if ltd>15:
                return "B"
            return "C"
        return "C"



def m5cardgen_getbrn(request):
     if request.method == "GET" and request.is_ajax():
        batch = request.GET.get('batch')
        assly = request.GET.get('assly')
        obj=[{'check':'O'}]
        obj3=list(Batch.objects.filter(bo_no=batch,part_no=assly).values('brn_no'))
        if(len(obj3)!=0):
            obj[0]['check']='E'
            obj.append(obj3)
        if len(obj3)==0:
            print('hhhh')
            obj1=list(Batch.objects.filter(brn_no__isnull=False).values('brn_no').order_by('brn_no').reverse())
            obj1=obj1[0]['brn_no']+1
            obj2=list(Proddem.objects.filter(bo_no=batch,part_no=assly).values('l_fr','l_to','qty','batch_type','week_no','epc').exclude(part_no__isnull=True).distinct().order_by('part_no'))
            if len(obj2)!=0:
                obj[0]['check']='NE'
                obj[0].update({'brn':obj1,'l_fr':obj2[0]['l_fr'],'l_to':obj2[0]['l_to'],'qty':obj2[0]['qty'],'batch_type':obj2[0]['batch_type'],'week_no':obj2[0]['week_no'],'epc':obj2[0]['epc']})
        print(obj)
        return JsonResponse(obj, safe = False)
     return JsonResponse({"success":False}, status = 400)
def m5cardgen_getassembly(request):
     if request.method == "GET" and request.is_ajax():
        obj=list(Proddem.objects.all().values('part_no').exclude(part_no__isnull=True).distinct().order_by('part_no'))
        return JsonResponse(obj, safe = False)
     return JsonResponse({"success":False}, status = 400)
def cggetBatchNo(request):
     if request.method == "GET" and request.is_ajax():
        batch = request.GET.get('batch')
        mAsslyno = request.GET.get('mAsslyno')
        obj=list(Proddem.objects.filter(part_no=mAsslyno).values('bo_no').distinct())
        return JsonResponse(obj, safe = False)
     return JsonResponse({"success":False}, status = 400)




@login_required
@role_required(urlpass='/CardGenerationreport/')
def CardGenerationreport(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context = {
        'ip':get_client_ip(request),
        'nav':nav,
        'subnav':subnav,
    }
    if request.method=="POST":
        batch = request.POST.get('batchno')
        bval=request.POST.get('cardbutton')
        asmno=request.POST.get('asslyno')
        card = request.POST.get('cardno')
        bno1 = request.POST.get('brn_no')
        if bval=="Generate Cards" and card=="M2":
            ades=list(Part.objects.filter(partno = asmno).values('des').distinct()) 

            m2=list(M2Docnew1.objects.filter(assly_no=asmno,batch_no=batch,brn_no=bno1).values('m2sln','scl_cl','part_no','qty','f_shopsec','rc_st_wk','rm_partno','rm_qty','epc'))
            if len(m2)==0:
                messages.error(request,'Card is Not Generated Yet!')
                return render(request,"PPRODUCTION/CARDGENERATION/CardGenerationreport.html",context)

            for i in range(len(m2)):
                part=Part.objects.filter(partno=m2[i]['part_no']).values('des')
                m2[i].update({'des':part[0]['des']})
            ades=ades[0]['des']
            epc=m2[0]['epc']
            data ={
                'epc':epc,
                'asl':asmno,
                'ades':ades,
                'batch':batch,
                'brn':bno1,
                'm2':m2,
            }
            pdf = render_to_pdf('PPRODUCTION/CARDGENERATION/cardpdf.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        elif bval=="Generate Cards" and card=="M4":
            ades=list(Part.objects.filter(partno = asmno).values('des').distinct()) 
            m4=list(M14M4new1.objects.filter(assly_no=asmno,bo_no=batch,brn_no=bno1,doc_code='88').values('doc_no','pm_no','part_no','qty','l_fr','l_to','due_wk','doc_ind','epc'))
            if len(m4)==0:
                messages.error(request,'Card is Not Generated Yet!')
                return render(request,"PPRODUCTION/CARDGENERATION/CardGenerationreport.html",context)
            for i in range(len(m4)):
                part=Part.objects.filter(partno=m4[i]['part_no']).values('des')
                m4[i].update({'des':part[0]['des']})
            ades=ades[0]['des']
            epc=m4[0]['epc']
            data ={
                'epc':epc,
                'brn':bno1,
                'asl':asmno,
                'ades':ades,
                'batch':batch,
                'brn':bno1,
                'm4':m4,
            }
            pdf = render_to_pdf('PPRODUCTION/CARDGENERATION/m4cardpdf.html', data)
            return HttpResponse(pdf, content_type='application/pdf')

        elif bval=="Generate Cards" and card=="M14":
            ades=list(Part.objects.filter(partno = asmno).values('des').distinct()) 
            m14=list(M14M4new1.objects.filter(assly_no=asmno,bo_no=batch,brn_no=bno1,doc_code='89').values('doc_no','pm_no','part_no','qty','l_fr','l_to','due_wk','doc_ind','epc'))
            if len(m14)==0:
                messages.error(request,'Card is Not Generated Yet!')
                return render(request,"PPRODUCTION/CARDGENERATION/CardGenerationreport.html",context)
            for i in range(len(m14)):
                part=Part.objects.filter(partno=m14[i]['part_no']).values('des')
                m14[i].update({'des':part[0]['des']})
            ades=ades[0]['des']
            epc=m14[0]['epc']
            data ={
                'epc':epc,
                'brn':bno1,
                'asl':asmno,
                'ades':ades,
                'batch':batch,
                'brn':bno1,
                'm4':m14,
            }
            pdf = render_to_pdf('PPRODUCTION/CARDGENERATION/m14cardpdf.html', data)
            return HttpResponse(pdf, content_type='application/pdf')
        elif bval=="Generate Cards" and card=="M5":
            ades=list(Part.objects.filter(partno = asmno).values('des').distinct()) 
            m5=list(M5Docnew1.objects.filter(assly_no=asmno,batch_no=batch,brn_no=bno1).values('scl_cl','pr_shopsec','m2slno','part_no','shop_sec','m5_cd','opn','opn_desc','l_fr','l_to'))
            if len(m5)==0:
                messages.error(request,'Card is Not Generated Yet!')
                return render(request,"PPRODUCTION/CARDGENERATION/CardGenerationreport.html",context)
            for i in range(len(m5)):
                part=Part.objects.filter(partno=m5[i]['part_no']).values('des')
                m5[i].update({'des':part[0]['des']})
            ades=ades[0]['des']
            data ={
                'asl':asmno,
                'ades':ades,
                'batch':batch,
                'brn':bno1,
                'm5':m5,
                
            }
            return render(request,"PPRODUCTION/CARDGENERATION/m5cardpdf.html",data)
    return render(request,"PPRODUCTION/CARDGENERATION/CardGenerationreport.html",context)
