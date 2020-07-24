from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/sectionJobListingview/')
def sectionJobListingview(request):
     
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'subnav':g.subnav,
        'usermaster':g.usermaster,
    }       
    if request.method == "POST":       
        SubmitMultipleRowData = request.POST.get('SubmitMultipleRowData')
        dataForm = request.POST.get('dataForm')
        if SubmitMultipleRowData=="Submit":
            dataFormTemp  = request.POST.get('dataForm')
            context={
                'nav':g.nav,
                'ip':get_client_ip(request),           
                'subnav':g.subnav,
                'epc':dataFormTemp.split(',')[0],
                'bo_no':dataFormTemp.split(',')[1],
                'loco_fr':dataFormTemp.split(',')[2],
                'loco_to':dataFormTemp.split(',')[3],
                'batch_qty' : dataFormTemp.split(',')[4],
                'asslypart1' : dataFormTemp.split(',')[5],
                'reldate' : dataFormTemp.split(',')[6], 
                'a':'P',   
                }         
    return render(request,'SHOPADMIN/SECJOBLISTING/sectionJobListingview.html',context)
	
def secJobEpcDesc(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        epc=request.GET.get('epc')
        obj=list(Code.objects.filter(code=epc,cd_type='11').values('alpha_1').distinct())
        obj1=Batch.objects.filter(~Q(bo_no__startswith='13'),ep_type=epc,batch_type='O').values('ep_type','bo_no','loco_fr','loco_to','batch_qty','part_no','rel_date').distinct()
        obj2=Batch.objects.filter(bo_no__startswith='13',ep_type=epc,batch_type='O',status='R').values('ep_type','bo_no','loco_fr','loco_to','batch_qty','part_no','rel_date').distinct()
        obj3=obj1.union(obj2)
        obj4=list(obj3)
        l.append(obj)
        l.append(obj4)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)
def secJobBackClick(request):
    
    wo_nop = empmast.objects.none()
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'subnav':g.subnav,
        }  
    return render(request,'homeadmin.html',context)

def secJobPartNoDesc(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        part_no=request.GET.get('part_no')
        obj=list(Part.objects.filter(partno=part_no).values('des').distinct())
        l.append(obj)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)

def secJobViewCode(request):
    if request.method == "GET" and request.is_ajax():  
        part_no=request.GET.get('part_no')
        epc=request.GET.get('epc')
        loco_from=request.GET.get('loco_from')
        loco_to=request.GET.get('loco_to')
        p=explodem(part_no,epc,loco_from,loco_to)
        return JsonResponse(p,safe=False) 
    return JsonResponse({"success:False"},status=400) 
assly_ptc=None

def explodem(assly,ep,lf,lt):
    global assly_ptc
    assly_ptc=''
    assly_des=''
    obj=list(Part.objects.filter(partno=assly).values('ptc','des').distinct())
    for i in range(len(obj)):
        assly_ptc = str(obj[i].get('ptc'))
        assly_des = str(obj[i].get('des'))
    return obj

def secJobViewCodeII(request):
    if request.method == "GET" and request.is_ajax():  
        part_no=request.GET.get('part_no')
        cur_time=datetime.datetime.now().strftime("%H%M%S")
        epc=request.GET.get('epc')
        loco_from=request.GET.get('loco_from')
        loco_to=request.GET.get('loco_to')
        global assly_ptc
        q=explodemII(part_no,epc,loco_from,loco_to,assly_ptc,cur_time)
        lst=[]
        lst.append(cur_time)
        lst.append(q)
        return JsonResponse(lst,safe=False) 
    return JsonResponse({"success:False"},status=400) 

def explodemII(assly,ep,lf,lt,assly_ptc,cur_time): 
    global g_curTime
    cur_time=cur_time
    g_curTime=cur_time 
    global system_date
    system_date=datetime.date.today()
    if (assly!="" and ep!="" and lf!="" and lt !=""):
        obj1=list(Nstr.objects.filter(pp_part=assly,epc=ep,l_fr__lte=lf,l_to__gte=lt).values('pp_part','cp_part','l_fr','l_to','ptc','epc','qty','updt_dt','ref_ind','ref_no','alt_ind','alt_link','lead_time','reg_no','slno','del_fl','epc_old','id').order_by('pp_part','cp_part','epc','l_to').distinct())
    elif(assly != "" and ep != "" and lf != ""):
        obj1=list(Nstr.objects.filter(pp_part=assly,epc=ep,l_fr__lte=lf,l_to__gte=lt,l_to='9999').values('pp_part','cp_part','l_fr','l_to','ptc','epc','qty','updt_dt','ref_ind','ref_no','alt_ind','alt_link','lead_time','reg_no','slno','del_fl','epc_old','id').order_by('pp_part','cp_part','epc','l_to').distinct())
    elif (assly != "" and ep != ""):
        obj1=list(Nstr.objects.filter(pp_part=assly,epc=ep,l_fr='0000',l_to='9999').values('pp_part','cp_part','l_fr','l_to','ptc','epc','qty','updt_dt','ref_ind','ref_no','alt_ind','alt_link','lead_time','reg_no','slno','del_fl','epc_old','id').order_by('pp_part','cp_part','epc','l_to').distinct())

    qty=1.000
    delQtySum_Temp1()
    insertQtySum_temp1(assly,assly_ptc,qty, "01", lf, lt)
    explm(assly,1,ep,lf,lt)
    delQtySum_Temp2()
    appendQtySum_Temp2()
    return obj1

def explm(parent,wt,ep,lf,lt):
    mcp_part=''
    mqty=''
    shop_ut=''
    v_ptc=''
    wt1=0
    mqty1=0
    cursor = connection.cursor()
    if (parent!="" and ep!="" and lf!="" and lt !=""):
        cursor.execute('select distinct n."PP_PART", n."CP_PART",n."PTC",n."QTY",p."SHOP_UT",n."L_FR",n."L_TO", COALESCE("ALT_IND",%s) from "NSTR" as n,"PART" as p where p."PARTNO" = n."CP_PART" and n."PP_PART"=%s and "EPC"=%s and "L_FR"<=%s and "L_TO">=%s  order by n."PP_PART",n."CP_PART";',['0',parent,ep,lf,lt])
    elif(parent != "" and ep != "" and lf != ""):
        cursor.execute('select distinct n."PP_PART", n."CP_PART",n."PTC",n."QTY",p."SHOP_UT",n."L_FR",n."L_TO", COALESCE("ALT_IND",%s) from "NSTR" as n,"PART" as p where p."PARTNO" = n."CP_PART" and n."PP_PART"=%s and "EPC"=%s and "L_FR"<=%s and "L_TO">=%s and "L_TO"=%s order by n."PP_PART",n."CP_PART";',['0',parent,ep,lf,lt,'9999'])
    elif (parent != "" and ep != ""):
        cursor.execute('select distinct n."PP_PART", n."CP_PART",n."PTC",n."QTY",p."SHOP_UT",n."L_FR",n."L_TO", COALESCE("ALT_IND",%s) from "NSTR" as n,"PART" as p where p."PARTNO" = n."CP_PART" and n."PP_PART"=%s and "EPC"=%s and "L_FR"=%s and "L_TO"=%s   order by n."PP_PART",n."CP_PART";',['0',parent,ep,'0000','9999'])
   
    row = cursor.fetchall()
    dts = pandas.DataFrame(list(row))
    
    if(dts.shape[0]>0):
        for i in range(dts.shape[0]):
            l_fr=dts[5][i]
            l_to=dts[6][i]
            v_ptc=dts[2][i]
            mcp_part=dts[1][i]
            shop_ut=dts[4][i]
            mqty=dts[3][i]
            mqt=wt*mqty

            if v_ptc in ["Q","R"]:
                UpdateQtySum_temp1(mcp_part, v_ptc,mqty, shop_ut, l_fr, l_to, parent)
            else:
                insertQtySum_temp1(mcp_part, v_ptc, mqt, shop_ut, l_fr, l_to)
            if (parent!="" and ep!="" and lf!="" and lt !=""):
                ds1=list(Nstr.objects.filter(pp_part=mcp_part,epc=ep,l_fr__lte=lf,l_to__gte=lt).values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by("pp_part","epc","cp_part","l_to"))        
            elif(parent != "" and ep != "" and lf != ""):
                ds1=list(Nstr.objects.filter(pp_part=mcp_part,epc=ep,l_fr__lte=lf,l_to__gte=lt,l_to='9999').values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by("pp_part","epc","cp_part","l_to"))        
            elif (parent != "" and ep != ""):
                ds1=list(Nstr.objects.filter(pp_part=mcp_part,epc=ep,l_fr='0000',l_to='9999').values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by("pp_part","epc","cp_part","l_to"))
                       
            if v_ptc in ["M","Z","L","B"] and len(ds1)>0:
                explm(mcp_part,mqt,ep,lf,lt) 
    return        
        
def UpdateQtySum_temp1(partno,ptc,qty,shop_ut,l_fr,l_to,parent):  
    print("UPDATE") 
    try:
        QtysumTemp1.objects.filter(partno=parent,cur_time=g_curTime).update(rm_part=str(partno),rm_ptc=str(ptc),rm_qty=qty,
        rm_ut=str(shop_ut),rm_lf=str(l_fr),rm_lt=str(l_to)) 
        return  
    except:
        print("Updation not successful : QtysumTemp1")
        return 
def insertQtySum_temp1(part_n,pt,qt,shop_u,l_f,l_t): 
    try:
        print("INSERTION")
        QtysumTemp1.objects.create(partno=str(part_n),ptc=str(pt),qty=qt,shop_ut=str(shop_u),l_fr=str(l_f),l_to=str(l_t),
        rm_part='',rm_ptc='',rm_qty=0.00,rm_ut='',rm_lf='',rm_lt='',dt_run=system_date,cur_time=str(g_curTime))                
        return 
    except:
        print("Insertion not successful : QTYSUM_TEMP1") 
        return 
        
def delQtySum_Temp1():
    print("Delete qtysum_temp1")
    try:
        QtysumTemp1.objects.filter(dt_run__lt= system_date).delete()
        return
    except:
        print("Data not deleted : QTYSUM_TEMP1") 
        return 

def delQtySum_Temp2():
    print("delete qtysum_temp2")
    try:
        QtysumTemp2.objects.filter(dt_run__lt=system_date).delete()
        return
    except:
        print("Data not deleted : QTYSUM_TEMP2")  
        return  

def appendQtySum_Temp2():
    tmpstr=list(QtysumTemp1.objects.filter(cur_time=g_curTime).values("partno" ,"ptc" ,"qty" ,"shop_ut","l_fr","l_to","rm_part","rm_ptc","rm_qty","rm_ut","rm_lf","rm_lt","dt_run","cur_time"))
    for i in range(len(tmpstr)):
        QtysumTemp2.objects.create(partno=tmpstr[i].get('partno') ,ptc=tmpstr[i].get('ptc') ,qty=tmpstr[i].get('qty') ,shop_ut=tmpstr[i].get('shop_ut'),pt_lf=tmpstr[i].get('l_fr'),pt_lt=tmpstr[i].get('l_to'),rm_part=tmpstr[i].get('rm_part'),rm_ptc=tmpstr[i].get('rm_ptc'),rm_qty=tmpstr[i].get('rm_qty'),rm_ut=tmpstr[i].get('rm_ut'),rm_lf=tmpstr[i].get('rm_lf'),rm_lt=tmpstr[i].get('rm_lt'),dt_run=tmpstr[i].get('dt_run'),cur_time=tmpstr[i].get('cur_time'))
    return

def delQtySum_Temp():
    print("delete qtysum_temp")
    try:
        QtysumTemp.objects.filter(dt_run__lt=system_date).delete()
        return
    except:
        print("Data not deleted : QTYSUM_TEMP")   
        return 

def secJobViewData(request):
    loco_from=request.GET.get('loco_from')
    loco_to=request.GET.get('loco_to')
    batch_qty=request.GET.get('batch_qty')
    part_no=request.GET.get('assly_part1')
    des=request.GET.get('assly_part2')
    cur_time1=request.GET.get('ctime')
    today=date.today().strftime('%d/%m/%Y')
    date1=str(today)
    date1=date1[0:2]+date1[3:5]+'rrrr'
    cursor = connection.cursor()
    cursor.execute('''select j.*,  CASE trim(o."NCP_JBS") WHEN '1' THEN 1 ELSE 0 END as ncp_ctr, CASE trim(o."NCP_JBS") WHEN '2' THEN 1 ELSE 0 END as jbs_ctr, 
                    (select "DES" from "LC1" where "SHOP_SEC"=j."SHOP_SEC" and "LCNO"=j."LC_NO" limit 1) lcdes, (select "DES" from "PART" 
                    where "PARTNO"=j.part_no limit 1) ptdes, (select "DRGNO" from "PART" where "PARTNO"=j.part_no limit 1) 
                    ptdrgno, o."DES" opdes, o."NCP_JBS", o."M5_CD",replace(to_char(o."PA",'9900.90'),'.','-') pa,  
                    replace(to_char(o."AT",'9900.90'),'.','-') as at, o."LOT" no_off, (case when (o."LOT" > 0) then 
                    TOT_TIME("AT","PA",qty,"LOT") else 0 end) tot_time,  (case when (o."LOT" > 0) then gt_hrs("AT","PA",qty,"LOT") else 0 end)
                    gt_hrs, (case when (o."LOT" > 0) then gt_min("AT","PA",qty,"LOT") else 0 end) gt_min from (select a.part_no part_no,a.ptc,
                    round(a.qty,2) as qty, b."SHOP_SEC", b."LC_NO", b."OPN" opn  from (select "PARTNO" part_no, max("PTC") ptc, CASE max("PTC") WHEN 'C' THEN sum("QTY") ELSE sum("QTY")*('1'::int) END as  qty  from "QTYSUM_TEMP2" where "CUR_TIME"=%s and to_char("DT_RUN",'ddmmrrrr')=
                    %s group by "PARTNO") a,"OPRN" b  where trim(a.part_no)=trim(b."PART_NO") and trim(a.ptc) in 
                    ('M','Z','L','B','C')) j, "OPRN" o where trim(j.part_no)=trim(o."PART_NO") and trim(j.opn)=trim(o."OPN") order by 
                    j."SHOP_SEC", j."LC_NO";''',[str(cur_time1),date1])
    row = cursor.fetchall()
    dts = list(row)
    lst=[]
    k=1
    for i in range(len(dts)):
        lst.append({'sl':k,"part_no":dts[i][0],"ptc":dts[i][1],"qty":dts[i][2],"shop_sec":dts[i][3], "lc_no":dts[i][4],"opn":dts[i][5],"ncp_ctr":dts[i][6],"jbs_ctr":dts[i][7],"lcdes":dts[i][8],
                   "ptdes":dts[i][9], "ptdrgno":dts[i][10], "opdes":dts[i][11],"ncp_jbs":dts[i][12],"m5_cd":dts[i][13],"pa":dts[i][14],"at":dts[i][15],"no_off":dts[i][16],"tot_time":dts[i][17],"gt_hrs":dts[i][18],"gt_min":dts[i][19]})
        k+=1

    i=0
    c=1
    total=0
    lst1=[]
    lst2=[]
    while(i<len(lst)):
        total=lst[i]['no_off']
        nj=0
        k=0
        if (lst[i]['m5_cd']) is not None:
                    nj=int(lst[i]['m5_cd'])
        lst2.append({'sl':c,'shopsec':lst[i]['shop_sec'],'lcno':lst[i]['lc_no'],'lcdes':lst[i]['lcdes'],})
        for j in range(i+1,len(lst)):
            if (lst[i]['shop_sec']==lst[j]['shop_sec'] and lst[i]['lc_no']==lst[j]['lc_no']):
                k+=1
                if (lst[j]['m5_cd']) is not None:
                    nj=int(lst[j]['m5_cd']) + nj
                total=total+lst[j]['no_off']
                c+=1
        c+=1
        lst1.append({'sl':c-1,'noo':k+1,'total':total,'nj':nj})
        i=i+k+1
   
    context={
        'loco_from':loco_from,
        'loco_to':loco_to,
        'batch_qty':batch_qty,
        'part_no':part_no,
        'des':des,
        'obj':lst,
        'today':today,
        'lst2':lst2,
        'lst1':lst1,
        'cur_time1':cur_time1
    }
    return render(request,'SHOPADMIN/SECJOBLISTING/SectionJobListingViewReport.html',context)

def secJobPrintPDF(request, *args, **kwargs):
    loco_from=request.GET.get('loco_from')
    loco_to=request.GET.get('loco_to')
    batch_qty=request.GET.get('batch_qty')
    part_no=request.GET.get('assly_part1')
    des=request.GET.get('assly_part2')
    cur_time1=request.GET.get('ctime')
    today=date.today().strftime('%d/%m/%Y')
    date1=str(today)
    date1=date1[0:2]+date1[3:5]+'rrrr'
    cursor = connection.cursor()
    cursor.execute('''select j.*,  CASE trim(o."NCP_JBS") WHEN '1' THEN 1 ELSE 0 END as ncp_ctr, CASE trim(o."NCP_JBS") WHEN '2' THEN 1 ELSE 0 END as jbs_ctr, 
                    (select "DES" from "LC1" where "SHOP_SEC"=j."SHOP_SEC" and "LCNO"=j."LC_NO" limit 1) lcdes, (select "DES" from "PART" 
                    where "PARTNO"=j.part_no limit 1) ptdes, (select "DRGNO" from "PART" where "PARTNO"=j.part_no limit 1) 
                    ptdrgno, o."DES" opdes, o."NCP_JBS", o."M5_CD",replace(to_char(o."PA",'9900.90'),'.','-') pa,  
                    replace(to_char(o."AT",'9900.90'),'.','-') as at, o."LOT" no_off, (case when (o."LOT" > 0) then 
                    TOT_TIME("AT","PA",qty,"LOT") else 0 end) tot_time,  (case when (o."LOT" > 0) then gt_hrs("AT","PA",qty,"LOT") else 0 end)
                    gt_hrs, (case when (o."LOT" > 0) then gt_min("AT","PA",qty,"LOT") else 0 end) gt_min from (select a.part_no part_no,a.ptc,
                    round(a.qty,2) as qty, b."SHOP_SEC", b."LC_NO", b."OPN" opn  from (select "PARTNO" part_no, max("PTC") ptc, CASE max("PTC") WHEN 'C' THEN sum("QTY") ELSE sum("QTY")*('1'::int) END as  qty  from "QTYSUM_TEMP2" where "CUR_TIME"=%s and to_char("DT_RUN",'ddmmrrrr')=
                    %s group by "PARTNO") a,"OPRN" b  where trim(a.part_no)=trim(b."PART_NO") and trim(a.ptc) in 
                    ('M','Z','L','B','C')) j, "OPRN" o where trim(j.part_no)=trim(o."PART_NO") and trim(j.opn)=trim(o."OPN") order by 
                    j."SHOP_SEC", j."LC_NO";''',[str(cur_time1),date1])
    row = cursor.fetchall()
    dts = list(row)
    lst=[]
    k=1
    for i in range(len(dts)):
        lst.append({'sl':k,"part_no":dts[i][0],"ptc":dts[i][1],"qty":dts[i][2],"shop_sec":dts[i][3], "lc_no":dts[i][4],"opn":dts[i][5],"ncp_ctr":dts[i][6],"jbs_ctr":dts[i][7],"lcdes":dts[i][8],
                   "ptdes":dts[i][9], "ptdrgno":dts[i][10], "opdes":dts[i][11],"ncp_jbs":dts[i][12],"m5_cd":dts[i][13],"pa":dts[i][14],"at":dts[i][15],"no_off":dts[i][16],"tot_time":dts[i][17],"gt_hrs":dts[i][18],"gt_min":dts[i][19]})
        k+=1

    for i in range(len(lst)):
        opdes=lst[i]['opdes']
        opdes1=opdes[0:1500]
        lst[i].update({'opdes':opdes1})

    i=0
    c=1
    total=0
    lst1=[]
    lst2=[]
    while(i<len(lst)):
        total=lst[i]['no_off']
        nj=0
        k=0
        if (lst[i]['m5_cd']) is not None:
                    nj=int(lst[i]['m5_cd'])
        lst2.append({'sl':c,'shopsec':lst[i]['shop_sec'],'lcno':lst[i]['lc_no'],'lcdes':lst[i]['lcdes'],})
        for j in range(i+1,len(lst)):
            if (lst[i]['shop_sec']==lst[j]['shop_sec'] and lst[i]['lc_no']==lst[j]['lc_no']):
                k+=1
                if (lst[j]['m5_cd']) is not None:
                    nj=int(lst[j]['m5_cd']) + nj
                total=total+lst[j]['no_off']
                c+=1
        c+=1
        lst1.append({'sl':c-1,'noo':k+1,'total':total,'nj':nj})
        i=i+k+1
   
    context={
        'loco_from':loco_from,
        'loco_to':loco_to,
        'batch_qty':batch_qty,
        'part_no':part_no,
        'des':des,
        'obj':lst,
        'today':today,
        'lst2':lst2,
        'lst1':lst1,       
    }
    pdf = render_to_pdf('SHOPADMIN/SECJOBLISTING/SecJobListPDFReport.html',context)
    return HttpResponse(pdf, content_type='application/pdf')