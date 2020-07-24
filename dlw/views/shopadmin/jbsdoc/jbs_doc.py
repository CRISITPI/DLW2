from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/jbs_doc/')
def jbs_doc(request):
    
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
    return render(request,'SHOPADMIN/JBSDOC/jbs.html',context)
txtepc=''   
drpdwn='' 
BROWKEY=''
bonum=''
a=''
dt=[]
ALTLINK=0
ASSLY=''
LFR=''
LTO=''
CASE=''
CURTYM=''
ALTPT=''
cnt=1
fg=[]
def epc_changed(request):
    if request.method == "GET" and request.is_ajax():
        global txtepc
        lst=[]
        b=[]
        txtepc = request.GET.get('txtepc')
        global drpdwn
        drpdwn = request.GET.get('drpdwn')
        global a
        a=epc()
        if(a!=False):
            b.append(a[0]['alpha_1'])
            lst=get_batch() 
            b.append(lst)
        return JsonResponse(b,safe = False)
    return JsonResponse({"success":False}, status = 400)   


def epc():
        alpha1_list=list(Code.objects.filter(code = txtepc,cd_type = "11").values('alpha_1'))
        global BROWKEY
        if alpha1_list != "":
            if drpdwn == "ENG":
                epc = ["01","02","05","1A","1C","1E","1Y","21"]
                if  txtepc in epc:
                    BROWKEY = "04"
                    return alpha1_list
                else :
                    return False
            if drpdwn == "VEH":
                epc = ["03","04","06","07","08","09","1B","1D","1N","1F","1R","1Q","14","20","22","11","28","1W","1L","35","40","50"]
                if txtepc in epc:
                    BROWKEY = "05"
                    return alpha1_list
                else :
                    return False
            if drpdwn == "TRA":
                epc =["1G","1H","1J","1K","1L","1M","1P","1T","12","22","11","36"]
                if txtepc in epc:
                    BROWKEY = "05"
                    return alpha1_list
                else :
                    return False
        else :
            return False
        
def get_batch():
    global BROWKEY
    if drpdwn == "ENG":
        BROWKEY="04"
    if drpdwn == "VEH":
        BROWKEY="05"
    if drpdwn == "TRA":
        BROWKEY="05"
    cursor = connection.cursor()
    cursor.execute('select "BO_NO", "PART_NO", "EP_TYPE","BATCH_TYPE","LOCO_FR", "LOCO_TO","B_EXPL_DT","REL_DATE" FROM public."BATCH" where (trim(substr("BO_NO", 1, 2))=%s or trim(substr("BO_NO", 1, 2))=%s or trim(substr("BO_NO", 1, 2))=%s) and trim("BATCH_TYPE")=%s and trim("EP_TYPE")=%s  and ("B_EXPL_DT"::text is not null or "B_EXPL_DT" :: text !=%s)  order by "B_EXPL_DT" desc;',[BROWKEY,'13','33','O',txtepc,''])    
    row = cursor.fetchall()
    lst=list(row)
    return lst

def listselected_index(request):
    if request.method == "GET" and request.is_ajax():
        global bonum
        bonum = request.GET.get('bonum')
        global dt
        dt=v_batch()
        return JsonResponse(dt,safe = False)
    return JsonResponse({"success":False}, status = 400)  

def v_batch():
    dt1=[]
    f=0
    dt1.append(list(Batch.objects.filter(bo_no=bonum,ep_type=txtepc).values('bo_no','batch_type','ep_type','part_no','loco_fr','loco_to','batch_qty','uot_wk_f','b_expl_dt','rel_date').order_by('bo_no','ep_type')))
    if len(dt1) == 0:
        return False
    dt2 = list(Docjbs.objects.filter(epc=txtepc,batch_no=bonum).values('epc','batch_no'))
    if len(dt2) !=0:
        f=1
    dt1.append(f)
    return dt1
    
                                                                    
def btncrtjbsdoc(request):
    if request.method == "GET" and request.is_ajax():
        txtqty = request.GET.get('txtqty')
        txtloco_fr = request.GET.get('txtloco_fr')
        txtloco_to = request.GET.get('txtloco_to')
        txtpart_no = request.GET.get('txtpart_no')
        txtbatch_type = request.GET.get('txtbatch_type')
        if a == False and dt == False:
            return JsonResponse({"success":False}, status = 400)
        dt1 = list(Docjbs.objects.filter(epc=txtepc,batch_no=bonum).values('epc','batch_no'))
        if len(dt1) > 0 :
            f=[1]
            return JsonResponse(f,safe = False)
        sysdte = datetime.date.today()
        systemdte = sysdte - timedelta(days=1)
        del1 = TempJbs.objects.filter(dttym=systemdte).delete()
        global CURTYM
        CURTYM = datetime.datetime.today().strftime("%d%m%Y%H%M%S")
        global ALTLINK
        ALTLINK="0"
        qt=1
        if txtqty!="":
            qt = txtqty
        x=explodem(txtpart_no,txtepc,txtloco_fr,txtloco_to,txtbatch_type)
        if x == True:
            cursor = connection.cursor()
            cursor.execute('''insert into public."DOCJBS" select  %s epc,%s batch_no, s.part_no,s.ptc,s.qty*%s qty_ord, o."SHOP_SEC", o."LC_NO",
            o."OPN", o."AT", o."LOT", o."NCP_JBS",' ' as n_shop, null brn_no,%s updt_dt,s.alt_link,
            s.alt_ind,s.a_part alt_part,null as epc_old from 
            (select "CP" part_no,max("PTC") ptc , sum("QTY") qty, "A_IND" alt_ind, "A_LINK" alt_link, "A_PART" a_part from public."TEMP_JBS"
            where trim("CURTYM")=%s GROUP by "CP", "A_LINK", "A_IND", "A_PART" ) s,public."OPRN" o where trim(s.part_no)=trim(o."PART_NO")
            and trim(s.ptc) in('M','Z','L','B') and trim(o."NCP_JBS")='2' and  coalesce(trim(o."DEL_FL"),'*')<>'Y';''',[txtepc, bonum, qt , sysdte,CURTYM])
            print("inserted in docjbs")
        dsj = list(Docjbs.objects.filter(batch_no=bonum,epc=txtepc).values('part_no','opn','id').order_by('shop_sec','lc_no','part_no','opn'))
        for i in range(len(dsj)):
            dso = list(Oprn.objects.filter(part_no=dsj[i]['part_no'],opn=dsj[i]['opn']).values('shop_sec','part_no').order_by('part_no','opn'))
            if len(dso) > 0 :
                if len(dso) > 1 :
                    re = Docjbs.objects.filter(id=dsj[i]['id']).update(n_shop=dso[1][shop_sec])
                    if re == 0:
                        return JsonResponse({"success":False}, status = 400)  
                else:
                    nxtpart = list(Oprn.objects.filter(part_no=dsj[i]['part_no'],opn__gt=dsj[i]['opn']).values('part_no').order_by('part_no'))
                    if len(nxtpart) != 0 :
                        nxtshop = list(Oprn.objects.filter(part_no=nxtpart[0]['part_no'],opn__gt=dsj[i]['opn']).values('shop_sec').order_by('part_no','opn'))
                        if len(nxtshop) > 0:
                            s = Docjbs.objects.filter(id=dsj[i]['id']).update(n_shop=nxtshop[0]['shop_sec'])
                            if s == 0:
                                return JsonResponse({"success":False}, status = 400)  
        if len(fg) == 0:
          d=[4]
          return JsonResponse(d,safe = False)
        elif len(fg) != 0:
            return JsonResponse(fg,safe = False)
    return JsonResponse({"success":False}, status = 400)  

def explodem(assly,ep,lfr,lto,bt):
    global ASSLY
    global CASE
    ASSLY = assly
    lst = list(Part.objects.filter(partno=assly).values('partno','des','ptc').order_by('partno'))
    if len(lst) <= 0 :
        return True
    assly_desc = lst[0]['des']
    assly_ptc = lst[0]['ptc']
    if assly != "" and ep != "" and lfr != "" and lto != "":
        CASE = "1"
        SrchQry = list(Nstr.objects.filter(Q(l_fr__lte = lfr) | Q(l_to__gte = lto),Q(pp_part=assly),Q(epc=ep),Q(l_to='9999')).values('pp_part','cp_part','epc','alt_link','alt_ind','ptc','qty','l_fr','l_to').order_by('pp_part','epc','cp_part'))
    if assly != "" and ep != "" and lfr != "" and lto == "":
        CASE = "2"
        SrchQry = list(Nstr.objects.filter(pp_part=assly,epc=ep,l_to='9999',l_fr__lte = lfr,l_to__gte=lfr).values('pp_part','cp_part','epc','alt_link','alt_ind','ptc','qty','l_fr','l_to').order_by('pp_part','epc','cp_part'))
    if assly != "" and ep != "" and lfr == "" and lto == "":
        CASE = "3"
        SrchQry = list(Nstr.objects.filter(pp_part=assly,epc=ep,l_fr='0000',l_to='9999').values('pp_part','cp_part','epc','alt_link','alt_ind','ptc','qty','l_fr','l_to').order_by('pp_part','epc','cp_part'))
    if assly != "" and ep == "" and lfr == "" and lto == "":
        return True
    global LFR
    global LTO
    LFR = lfr
    LTO = lto
    global f1
    if len(SrchQry) == 0 :
        global fg
        fg=[10]
        return True
    sysdte = datetime.date.today().strftime("%Y-%m-%d")
    InsrtQry = TempJbs.objects.create(cp=assly,l_fr=lfr,l_to=lto,ptc=assly_ptc,epc=ep,qty=00001.000,a_ind="",a_part="",dttym=sysdte,curtym=CURTYM,sl=1)
    if InsrtQry == 0:
        return False
    global cnt
    cnt=cnt+1
    explm(assly, "1", bt, ep,SrchQry,lfr,lto)
    return True

def explm(parent,wt,bt,ep,srchqry,lfr,lto):
    sysdte = datetime.date.today().strftime("%Y-%m-%d")
    global ALTPT
    global ALTLINK
    global cnt
    ALTIND=None
    check2=0
    check3=len(srchqry)
    if len(srchqry) > 0:
        for i in range(len(srchqry)):
            if ASSLY == parent:
                if str(srchqry[i]['alt_link']) != ALTLINK or srchqry[i]['alt_ind'] != ALTIND :
                    ALTLINK = srchqry[i]['alt_link']
                    ALTIND = srchqry[i]['alt_ind']
                    ALTPT = srchqry[i]['cp_part']
            WT=1
            if srchqry[i]['qty'] != "":
                WT = srchqry[i]['qty']
            mqty1 = Decimal(WT*Decimal(wt))
            alpt=""
            if ALTLINK != "0" and ALTLINK != "":
                alpt = ALTPT
            x = ['M','Z','L','B']
            if srchqry[i]['ptc'] in x :
                InsrtQry = TempJbs.objects.create(pp=srchqry[i]['pp_part'],cp=srchqry[i]['cp_part'],l_fr=srchqry[i]['l_fr'],l_to=srchqry[i]['l_to'],ptc=srchqry[i]['ptc'],epc=srchqry[i]['epc'],qty=mqty1,a_ind=ALTIND,a_link=ALTLINK,a_part=alpt,dttym=sysdte,curtym=CURTYM,sl=cnt)
                if InsrtQry == 0:
                    return False
                cnt=cnt+1
            if srchqry[i]['ptc'] in x :
                if CASE == "1":
                    Qry=list(Nstr.objects.filter(Q(pp_part=srchqry[i]['cp_part']),Q(epc=ep),Q(l_to='9999'),Q(l_fr__lte=LFR) | Q(l_to__gte=LTO)).values('pp_part','cp_part','epc','alt_link','alt_ind','ptc','qty','l_fr','l_to').order_by('pp_part','epc','cp_part'))
                if CASE == "2":
                    Qry=list(Nstr.objects.filter(pp_part=srchqry[i]['cp_part'],epc=ep,l_to='9999',l_fr__lte=LFR,l_to__gte=LFR).values('pp_part','cp_part','epc','alt_link','alt_ind','ptc','qty','l_fr','l_to').order_by('pp_part','epc','cp_part'))
                if CASE == "3":
                    Qry=list(Nstr.objects.filter(pp_part=srchqry[i]['cp_part'],epc=ep,l_to='9999',l_fr='0000').values('pp_part','cp_part','epc','alt_link','alt_ind','ptc','qty','l_fr','l_to').order_by('pp_part','epc','cp_part'))
                if len(Qry) !=0 :
                    check2=check2+1
                    explm(srchqry[i]['cp_part'], mqty1,bt,ep,Qry,lfr,lto)
    return True

#report work of jbs starts from here
def jbsreport(request):
    shopsec=[]
    lc_no=[]
    partno=request.GET.get('partno')
    cursor = connection.cursor()
    cursor.execute('SELECT j."ALT_PART" FROM public."DOCJBS" j, public."OPRN" o, public."PART" p WHERE j."PART_NO" = o."PART_NO" and j."OPN" = o."OPN" and j."NCP_JBS" = %s and j."BATCH_NO"=%s and j."EPC"=%s and p."PARTNO" = j."PART_NO" ORDER BY j."PART_NO",j."OPN"',['2',bonum,txtepc])
    row = cursor.fetchall()
    lst=list(row)
    if len(lst) != 0 :
        part_des=''
        doc_no=0
        cd = list(Code.objects.filter(cd_type='11',code=txtepc).values('alpha_1').order_by('cd_type','code'))
        if len(cd) > 0:
            part_des = cd[0]['alpha_1']
            cursor = connection.cursor()
            cursor.execute('SELECT DISTINCT "SHOP_SEC","LC_NO" FROM (SELECT j."SHOP_SEC",j."LC_NO" from public."DOCJBS" j,public."OPRN" o, public."PART" p WHERE j."PART_NO"= o."PART_NO" and j."OPN"= o."OPN" and j."NCP_JBS"=%s and j."BATCH_NO"=%s and j."EPC"=%s and p."PARTNO"=j."PART_NO" order by j."SHOP_SEC",j."LC_NO",j."PART_NO",j."OPN") abc order by "SHOP_SEC","LC_NO"',['2',bonum,txtepc])
            row = cursor.fetchall()
            dt=list(row)  
            dt1=[]
            lst=[]
            b=1
            for i in range(len(dt)):
                shop_sec= dt[i][0]
                lc_no = dt[i][1]
                cursor.execute('''SELECT j."PART_NO", substr(p."DES",0,21) des, substr(trim(o."DES"),0,26) t_des, j."OPN",
                coalesce(o."AT",'0.00')as at , trim(o."LOT" :: text)as lot, trim(j."N_SHOP"), 
                trim(coalesce(j."QTY_ORD" :: text,'0'))as qty_ord, j."SHOP_SEC", j."LC_NO" FROM public."DOCJBS" j, 
                public."OPRN" o, public."PART" p WHERE j."PART_NO"= o."PART_NO" and j."OPN"= o."OPN" and j."NCP_JBS"=%s and 
                j."BATCH_NO"=%s and j."EPC"=%s and 
                p."PARTNO"=j."PART_NO" and j."SHOP_SEC" = %s and j."LC_NO"=%s ORDER BY j."OPN"''',['2',bonum,txtepc,shop_sec,lc_no])
                row = cursor.fetchall()
                dt1=(list(row))
                a=0
                lst.append([])
                for j in range(len(dt1)):
                    if a==0:
                        lst[i].append({'sno':j+1,'doc':b,'s':shop_sec,'l':lc_no,'a':dt1[j][0],'b':dt1[j][1],'c':dt1[j][2],'d':dt1[j][3],'e':dt1[j][4],'f':dt1[j][5],'g':dt1[j][6],'h':dt1[j][7],'i':dt1[j][8],'j':dt1[j][9]})
                        a=1
                        b=b+1
                    else:
                        lst[i].append({'sno':j+1,'doc':'','s':'','l':'','a':dt1[j][0],'b':dt1[j][1],'c':dt1[j][2],'d':dt1[j][3],'e':dt1[j][4],'f':dt1[j][5],'g':dt1[j][6],'h':dt1[j][7],'i':dt1[j][8],'j':dt1[j][9]})

            dte=datetime.datetime.today().strftime("%d-%m-%Y")
            print("my listt is",lst)
        context={
        'tdate':dte,  #today's date
        'pn':partno,     #assmbly no
        'des':part_des,  #assmbly design
        'head':dt,       #list of shop_sec and lc_no
        'lst':lst,      #list of lists
        'm':len(dt),     
        'n':len(dt1),
        }           
    pdf=render_to_pdf('SHOPADMIN/JBSDOC/jbs_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')
