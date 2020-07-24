from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/addAddtionview/')
def addAddtionview(request):
    cuser=request.user     
     
    context={
        'nav':g.nav,
        'ip':get_client_ip(request),
        'subnav':g.subnav,
        'usermaster':g.usermaster,
    }
    if request.method == "POST":
        submitvalue = request.POST.get('PrintPDF')   
        if submitvalue=='PrintPDF':
            id = request.POST.get('txtDiv3')
            DivType = ''
            DivType1 = ''
            bo_nos=[]
            if id=='E' :
                DivType = 'ENGINE DIVISION'
                DivType1 = 'STATEMENT OF RUNNING WORK ORDERS'
                for i in Batch.objects.raw('select "id",substr(trim(c."ALPHA_1"),1,4) as alpha,b."BO_NO",b."LOCO_FR",b."LOCO_TO",b."REL_DATE",b."REL_DT_BC",b."CLOS_DT_B",b."CLOS_DT_C",b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where c."CD_TYPE"=%s and b."DIV"=%s and c."CODE"=b."EP_TYPE" and b."STATUS"=%s and b."BATCH_TYPE"=%s',['11',id,'R','O']):                                                              
                    bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'REL_DT_BC':i.rel_dt_bc,'CLOS_DT_B':i.clos_dt_b,'CLOS_DT_C':i.clos_dt_c,'BRN_NO':i.brn_no,'REMARK':i.remark}) 

            if id=='V':
                DivType = 'VEHICLE DIVISION'
                DivType1 = 'STATEMENT OF RUNNING WORK ORDERS'
                for i in Batch.objects.raw('select "id",substr(trim(c."ALPHA_1"),1,4) as alpha,b."BO_NO",b."LOCO_FR",b."LOCO_TO",b."REL_DATE",b."REL_DT_BC",b."CLOS_DT_B",b."CLOS_DT_C",b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where c."CD_TYPE"=%s and b."DIV"=%s and c."CODE"=b."EP_TYPE" and b."STATUS"=%s and b."BATCH_TYPE"=%s',['11',id,'R','O']):                                                              
                    bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'REL_DT_BC':i.rel_dt_bc,'CLOS_DT_B':i.clos_dt_b,'CLOS_DT_C':i.clos_dt_c,'BRN_NO':i.brn_no,'REMARK':i.remark})
                    
            if id=='S' or id=='T':
                DivType = 'SPECIAL'
                DivType1 = 'STATEMENT OF RUNNING WORK ORDERS'
                for i in Batch.objects.raw('select "id",substr(trim(c."ALPHA_1"),1,4) as alpha,b."BO_NO",b."LOCO_FR",b."LOCO_TO",b."REL_DATE",b."REL_DT_BC",b."CLOS_DT_B",b."CLOS_DT_C",b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where c."CD_TYPE"=%s and b."DIV"=%s and c."CODE"=b."EP_TYPE" and b."STATUS"=%s and b."BATCH_TYPE"=%s',['11',id,'R','O']):                                                              
                    bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'REL_DT_BC':i.rel_dt_bc,'CLOS_DT_B':i.clos_dt_b,'CLOS_DT_C':i.clos_dt_c,'BRN_NO':i.brn_no,'REMARK':i.remark})
        
            context = {  
                    'pagesize':'A4',                  
                    'bo_nos': bo_nos,
                    'DivType':DivType, 
                    'DivType1':DivType1, 
                    }  
            pdf = render_to_pdf('PPRODUCTION/BATCHADDITION/rwopdf.html',context)
            return HttpResponse(pdf, content_type='application/pdf')
    if request.method == "POST":       
        submitvalue = request.POST.get('Print')  
        if submitvalue=='Print':
            id = request.POST.get('txtDiv4')
            txtDt41 = datetime.datetime.strptime(request.POST.get('txtDt41'),'%d-%m-%Y').date()
            txtDt42 = datetime.datetime.strptime(request.POST.get('txtDt42'),'%d-%m-%Y').date()
            DivType = ''
            DivType1 = ''
            bo_nos=[]
            if id=='S' or id=='T':
                DivType = 'SPECIAL'
                DivType1 = 'BATCHES RELEASED/CLOSED DURING PERIOD'
                for i in Batch.objects.raw('select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO",b."LOCO_FR",b."LOCO_TO",b."REL_DATE", null B_CLOSE_DT, b."BRN_NO" , b."REMARK" from "BATCH" b,"CODE" c where c."CD_TYPE"=%s and trim(c."CODE")=trim(b."EP_TYPE") and b."DIV" in (%s,%s,%s) and b."BATCH_TYPE" != %s and substr(b."BO_NO",1,2) in (%s,%s,%s,%s,%s,%s,%s,%s,%s) and b."REL_DATE" between %s and %s union all  select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO",b."LOCO_FR",b."LOCO_TO", b."REL_DATE",b."B_CLOSE_DT",b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where trim(c."CD_TYPE")=%s and trim(c."CODE")=trim(b."EP_TYPE") and trim(b."DIV") in (%s,%s,%s) and trim(b."BATCH_TYPE")!=%s and substr(b."BO_NO",1,2) in (%s,%s,%s,%s,%s,%s,%s,%s,%s) and b."B_CLOSE_DT" between %s and %s ',['11','E','V','T','O','07','10','12','13','18','21','24','25','69',txtDt41,txtDt42,'11','E','V','T','O','07','10','12','13','18','21','24','25','69',txtDt41,txtDt42]):
                    bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'B_CLOSE_DT':i.b_close_dt,'BRN_NO':i.brn_no,'REMARK':i.remark})

            if id=='E' :
                DivType = 'ENGINE DIVISION'
                DivType1 = 'BATCHES RELEASED/CLOSED DURING PERIOD'
                for i in Batch.objects.raw('select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO" ,b."LOCO_FR",b."LOCO_TO",b."REL_DATE", null b_close_dt, b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where trim(c."CD_TYPE")=%s and trim(c."CODE")=trim(b."EP_TYPE") and b."DIV"=%s and trim(b."BATCH_TYPE")=%s and b."REL_DATE" between %s and %s union all select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO" ,b."LOCO_FR",b."LOCO_TO",b."REL_DATE" ,b."B_CLOSE_DT" ,b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where trim(c."CD_TYPE")=%s and trim(c."CODE")=trim(b."EP_TYPE") and trim(b."DIV") = %s and trim(b."BATCH_TYPE")=%s and b."B_CLOSE_DT" between %s and %s ',['11',id,'O',txtDt41,txtDt42,'11',id,'O',txtDt41,txtDt42]):
                    bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'B_CLOSE_DT':i.b_close_dt,'BRN_NO':i.brn_no,'REMARK':i.remark}) 

            if id=='V':
                DivType = 'VEHICLE DIVISION'
                DivType1 = 'BATCHES RELEASED/CLOSED DURING PERIOD'
                for i in Batch.objects.raw('select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO" ,b."LOCO_FR",b."LOCO_TO",b."REL_DATE", null b_close_dt, b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where trim(c."CD_TYPE")=%s and trim(c."CODE")=trim(b."EP_TYPE") and b."DIV"=%s and trim(b."BATCH_TYPE")=%s and b."REL_DATE" between %s and %s union all select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO" ,b."LOCO_FR",b."LOCO_TO",b."REL_DATE" ,b."B_CLOSE_DT" ,b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where trim(c."CD_TYPE")=%s and trim(c."CODE")=trim(b."EP_TYPE") and trim(b."DIV") = %s and trim(b."BATCH_TYPE")=%s and b."B_CLOSE_DT" between %s and %s ',['11',id,'O',txtDt41,txtDt42,'11',id,'O',txtDt41,txtDt42]):
                    bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'B_CLOSE_DT':i.b_close_dt,'BRN_NO':i.brn_no,'REMARK':i.remark})
            
            context = {
                    'pagesize':'A4',
                    'bo_nos': bo_nos,
                    'DivType':DivType,
                    'DivType1':DivType1,  
                    }  
                
            pdf = render_to_pdf('PPRODUCTION/BATCHADDITION/batchRepdf.html',context)
            return HttpResponse(pdf, content_type='application/pdf')

    if request.method == "POST":       
        submitvalue = request.POST.get('PDF')  
        if submitvalue=='PDF':
            id = request.POST.get('txtDiv5')
            DivType = ''
            bo_nos=[]
            if id=='E' :
                DivType = 'ENGINE DIVISION' 
                DivType1 = 'NUMERICAL-CUM-FINANCIAL TALLY SHEET'
                for i in Batch.objects.raw('select distinct b."id",substr(c."ALPHA_1",1,4) alpha,t1."SL_NO" sl_no,t1."DESCR" descr,t2."PART_NO" part_no,b."SO_NO",b."BO_NO",b."REL_DATE",b."REL_DT_BC",n."QTY" as qty,b."BAL_QTY",b."PROGRESS",b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c,"NSTR" n ,"TALLY_1" t1,"TALLY_2" t2 where t1."SL_NO"=t2."SL_NO" and t2."PART_NO"=b."PART_NO" and b."PART_NO"=n."PP_PART" and trim(c."CODE")=trim(b."EP_TYPE") AND substr(t1."SL_NO",1,1)=%s',[id]):
                    bo_nos.append({'ALPHA_1':i.alpha,'SL_NO':i.sl_no,'DESCR':i.descr,'PART_NO':i.part_no,'SO_NO':i.so_no,'BO_NO':i.bo_no,'REL_DATE':i.rel_date,'REL_DT_BC':i.rel_dt_bc,'QTY':i.qty,'BAL_QTY':i.bal_qty,'PROGRESS':i.progress,'BRN_NO':i.brn_no,'REMARK':i.remark})

            if id=='V':
                DivType = 'VEHICLE DIVISION'
                DivType1 = 'NUMERICAL-CUM-FINANCIAL TALLY SHEET'
                for i in Batch.objects.raw('select distinct b."id",substr(c."ALPHA_1",1,4) alpha,t1."SL_NO" sl_no,t1."DESCR" descr,t2."PART_NO" part_no,b."SO_NO",b."BO_NO",b."REL_DATE",b."REL_DT_BC",n."QTY" as qty,b."BAL_QTY",b."PROGRESS",b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c,"NSTR" n ,"TALLY_1" t1,"TALLY_2" t2 where t1."SL_NO"=t2."SL_NO" and t2."PART_NO"=b."PART_NO" and b."PART_NO"=n."PP_PART" and trim(c."CODE")=trim(b."EP_TYPE") AND substr(t1."SL_NO",1,1)=%s',[id]):
                    bo_nos.append({'ALPHA_1':i.alpha,'SL_NO':i.sl_no,'DESCR':i.descr,'PART_NO':i.part_no,'SO_NO':i.so_no,'BO_NO':i.bo_no,'REL_DATE':i.rel_date,'REL_DT_BC':i.rel_dt_bc,'QTY':i.qty,'BAL_QTY':i.bal_qty,'PROGRESS':i.progress,'BRN_NO':i.brn_no,'REMARK':i.remark})
            
            if id=='S' or id=='T':
                DivType = 'SPECIAL'
                DivType1 = 'NUMERICAL-CUM-FINANCIAL TALLY SHEET'
                for i in Batch.objects.raw('select distinct b."id",substr(c."ALPHA_1",1,4) alpha,t1."SL_NO" sl_no,t1."DESCR" descr,t2."PART_NO" part_no,b."SO_NO",b."BO_NO",b."REL_DATE",b."REL_DT_BC",n."QTY" as qty,b."BAL_QTY",b."PROGRESS",b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c,"NSTR" n ,"TALLY_1" t1,"TALLY_2" t2 where t1."SL_NO"=t2."SL_NO" and t2."PART_NO"=b."PART_NO" and b."PART_NO"=n."PP_PART" and trim(c."CODE")=trim(b."EP_TYPE") AND substr(t1."SL_NO",1,1)=%s',[id]):
                    bo_nos.append({'ALPHA_1':i.alpha,'SL_NO':i.sl_no,'DESCR':i.descr,'PART_NO':i.part_no,'SO_NO':i.so_no,'BO_NO':i.bo_no,'REL_DATE':i.rel_date,'REL_DT_BC':i.rel_dt_bc,'QTY':i.qty,'BAL_QTY':i.bal_qty,'PROGRESS':i.progress,'BRN_NO':i.brn_no,'REMARK':i.remark})
            
            context = {

                    'pagesize':'A4',
                    'bo_nos': bo_nos,
                    'DivType':DivType,
                    'DivType1':DivType1,   
                    
                    }  
                
            pdf = render_to_pdf('PPRODUCTION/BATCHADDITION/BatchTallyPdf.html',context)
            return HttpResponse(pdf, content_type='application/pdf')

    return render(request,"PPRODUCTION/BATCHADDITION/batchAddition_view.html",context)

def addBatchwono(request):
    if request.method == "GET" and request.is_ajax():
        sno = request.GET.get('id')
        wo_no=''
        obj1=list(Batch.objects.filter(bo_no=sno).values('bo_no','part_no','ep_type','brn_no','status','b_expl_dt','loco_fr','loco_to').distinct())
        if len(obj1)!=0:
            wo_no=obj1[0]['part_no'].strip()
        wo_no = list(Part.objects.filter(partno = wo_no).values('des').distinct())
        context={
            'obj1':obj1,
            'wo_no':wo_no,             
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)

def getepc(request):
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get('id')
        obj1=list(Code.objects.filter(code=id ,cd_type='11').values('alpha_1').distinct())
        context={
            'obj1':obj1,             
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)

def repRWOReport(request):
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get('id')
        epc=''
        bo_nos=[]
        if id=='E':
            for i in Batch.objects.raw('select "id",substr(trim(c."ALPHA_1"),1,4) as alpha,b."BO_NO",b."LOCO_FR",b."LOCO_TO",b."REL_DATE",b."REL_DT_BC",b."CLOS_DT_B",b."CLOS_DT_C",b."BRN_NO",COALESCE(b."REMARK",%s) as remark  from "BATCH" b,"CODE" c where c."CD_TYPE"=%s and b."DIV"=%s and c."CODE"=b."EP_TYPE" and b."STATUS"=%s and b."BATCH_TYPE"=%s',['','11',id,'R','O']):                                                              
                bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'REL_DT_BC':i.rel_dt_bc,'CLOS_DT_B':i.clos_dt_b,'CLOS_DT_C':i.clos_dt_c,'BRN_NO':i.brn_no,'REMARK':i.remark})
        
        if id=='V':
            for i in Batch.objects.raw('select "id",substr(trim(c."ALPHA_1"),1,4) as alpha,b."BO_NO",b."LOCO_FR",b."LOCO_TO",b."REL_DATE",b."REL_DT_BC",b."CLOS_DT_B",b."CLOS_DT_C",b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where c."CD_TYPE"=%s and b."DIV"=%s and c."CODE"=b."EP_TYPE" and b."STATUS"=%s and b."BATCH_TYPE"=%s',['11',id,'R','O']):                                                              
                bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'REL_DT_BC':i.rel_dt_bc,'CLOS_DT_B':i.clos_dt_b,'CLOS_DT_C':i.clos_dt_c,'BRN_NO':i.brn_no,'REMARK':i.remark})

        if id=='S' or id=='T':
            for i in Batch.objects.raw('select "id",substr(trim(c."ALPHA_1"),1,4) as alpha,b."BO_NO",b."LOCO_FR",b."LOCO_TO",b."REL_DATE",b."REL_DT_BC",b."CLOS_DT_B",b."CLOS_DT_C",b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where c."CD_TYPE"=%s and b."DIV"=%s and c."CODE"=b."EP_TYPE" and b."STATUS"=%s and b."BATCH_TYPE"=%s',['11',id,'R','O']):                                                              
                bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'REL_DT_BC':i.rel_dt_bc,'CLOS_DT_B':i.clos_dt_b,'CLOS_DT_C':i.clos_dt_c,'BRN_NO':i.brn_no,'REMARK':i.remark})

        return JsonResponse(bo_nos, safe = False)
    return JsonResponse({"success":False}, status=400)

def BatchRelReport(request):
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get('id')
        txtDt41 = datetime.datetime.strptime(request.GET.get('txtDt41'),'%d-%m-%Y').date()
        txtDt42 = datetime.datetime.strptime(request.GET.get('txtDt42'),'%d-%m-%Y').date()
        bo_nos=[]
        if id=='S' or id=='T':
            for i in Batch.objects.raw('select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO",b."LOCO_FR",b."LOCO_TO",b."REL_DATE", null B_CLOSE_DT, b."BRN_NO" , COALESCE(b."REMARK",%s) as remark from "BATCH" b,"CODE" c where c."CD_TYPE"=%s and trim(c."CODE")=trim(b."EP_TYPE") and b."DIV" in (%s,%s,%s) and b."BATCH_TYPE" != %s and substr(b."BO_NO",1,2) in (%s,%s,%s,%s,%s,%s,%s,%s,%s) and b."REL_DATE" between %s and %s union all  select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO",b."LOCO_FR",b."LOCO_TO", b."REL_DATE",b."B_CLOSE_DT",b."BRN_NO",COALESCE(b."REMARK",%s) as remark from "BATCH" b,"CODE" c where trim(c."CD_TYPE")=%s and trim(c."CODE")=trim(b."EP_TYPE") and trim(b."DIV") in (%s,%s,%s) and trim(b."BATCH_TYPE")!=%s and substr(b."BO_NO",1,2) in (%s,%s,%s,%s,%s,%s,%s,%s,%s) and b."B_CLOSE_DT" between %s and %s ',['','11','E','V','T','O','07','10','12','13','18','21','24','25','69',txtDt41,txtDt42,'','11','E','V','T','O','07','10','12','13','18','21','24','25','69',txtDt41,txtDt42]):
                bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'B_CLOSE_DT':i.b_close_dt,'BRN_NO':i.brn_no,'REMARK':i.remark})
                
        if id=='E':
            for i in Batch.objects.raw('select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO" ,b."LOCO_FR",b."LOCO_TO",b."REL_DATE", null b_close_dt, b."BRN_NO",COALESCE(b."REMARK",%s) as remark from "BATCH" b,"CODE" c where trim(c."CD_TYPE")=%s and trim(c."CODE")=trim(b."EP_TYPE") and b."DIV"=%s and trim(b."BATCH_TYPE")=%s and b."REL_DATE" between %s and %s union all select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO" ,b."LOCO_FR",b."LOCO_TO",b."REL_DATE" ,b."B_CLOSE_DT" ,b."BRN_NO",COALESCE(b."REMARK",%s) as remark from "BATCH" b,"CODE" c where trim(c."CD_TYPE")=%s and trim(c."CODE")=trim(b."EP_TYPE") and trim(b."DIV") = %s and trim(b."BATCH_TYPE")=%s and b."B_CLOSE_DT" between %s and %s ',['','11',id,'O',txtDt41,txtDt42,'','11',id,'O',txtDt41,txtDt42]):
                bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date, 'B_CLOSE_DT':i.b_close_dt,'BRN_NO':i.brn_no,'REMARK':i.remark}) 
        if id=='V':
            for i in Batch.objects.raw('select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO" ,b."LOCO_FR",b."LOCO_TO",b."REL_DATE", null b_close_dt, b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where trim(c."CD_TYPE")=%s and trim(c."CODE")=trim(b."EP_TYPE") and b."DIV"=%s and trim(b."BATCH_TYPE")=%s and b."REL_DATE" between %s and %s union all select "id",substr(c."ALPHA_1",1,4) alpha,b."BO_NO" ,b."LOCO_FR",b."LOCO_TO",b."REL_DATE" ,b."B_CLOSE_DT" ,b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c where trim(c."CD_TYPE")=%s and trim(c."CODE")=trim(b."EP_TYPE") and trim(b."DIV") = %s and trim(b."BATCH_TYPE")=%s and b."B_CLOSE_DT" between %s and %s ',['11',id,'O',txtDt41,txtDt42,'11',id,'O',txtDt41,txtDt42]):
                bo_nos.append({'ALPHA_1':i.alpha,'BO_NO':i.bo_no,'LOCO_FR':i.loco_fr,'LOCO_TO':i.loco_to,'REL_DATE':i.rel_date,'B_CLOSE_DT':i.b_close_dt,'BRN_NO':i.brn_no,'REMARK':i.remark})
        
        return JsonResponse(bo_nos, safe = False)
    return JsonResponse({"success":False}, status=400)


def BatchTallyReport(request):
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get('id')
        bo_nos=[]
        for i in Batch.objects.raw('select distinct b."id",substr(c."ALPHA_1",1,4) alpha,t1."SL_NO" sl_no,t1."DESCR" descr,t2."PART_NO" part_no,b."SO_NO",b."BO_NO",b."REL_DATE",b."REL_DT_BC",n."QTY" as qty,b."BAL_QTY",b."PROGRESS",b."BRN_NO",b."REMARK" from "BATCH" b,"CODE" c,"NSTR" n ,"TALLY_1" t1,"TALLY_2" t2 where t1."SL_NO"=t2."SL_NO" and t2."PART_NO"=b."PART_NO" and b."PART_NO"=n."PP_PART" and trim(c."CODE")=trim(b."EP_TYPE") AND substr(t1."SL_NO",1,1)=%s',[id]):
            bo_nos.append({'ALPHA_1':i.alpha,'SL_NO':i.sl_no,'DESCR':i.descr,'PART_NO':i.part_no,'SO_NO':i.so_no,'BO_NO':i.bo_no,'REL_DATE':i.rel_date,'REL_DT_BC':i.rel_dt_bc,'QTY':i.qty,'BAL_QTY':i.bal_qty,'PROGRESS':i.progress,'BRN_NO':i.brn_no,'REMARK':i.remark})
           
        return JsonResponse(bo_nos, safe = False)
    return JsonResponse({"success":False}, status=400)


def getBatchAdditionno(request):
    if request.method == "GET" and request.is_ajax():
        sno = request.GET.get('id')
        BO_No = request.GET.get('BO_No')
        wo_no=''
        epc=''
        div=''
        obj1=list(Batch.objects.filter(brn_no=sno,bo_no=BO_No).values('bo_no','part_no','ep_type','brn_no','status','b_expl_dt','loco_fr','loco_to','div','seq','batch_type','rel_date','b_close_dt','rel_dt_bc','clos_dt_b','clos_dt_c','so_no','batch_qty','bal_qty','progress','remark','scno','uot_wk_f').distinct())
        if len(obj1)!=0:
            wo_no=obj1[0]['part_no'].strip()
            div=obj1[0]['div'].strip()
        wo_no = list(Part.objects.filter(partno = wo_no).values('des').distinct())
        if len(obj1)!=0:
            epc=obj1[0]['ep_type'].strip()
        epc=list(Code.objects.filter(code=epc ,cd_type='11').values('alpha_1').distinct())
        context={
            'obj1':obj1, 
            'wo_no':wo_no,
            'epc':epc,            
        }         
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)

def getAsslyNo(request):
    if request.method == "GET" and request.is_ajax():
        id = request.GET.get('id')
        sno = request.GET.get('ec')
        shop_section.objects.all()
        obj1=list(Part.objects.filter(partno=id ).values('des','partno'))
        if len(obj1)>0:
            context={
                'obj1':obj1
            }
        else:
            obj1=list(Schdesc.objects.filter(brn_no=sno).values('des','brn_no').distinct())
            context={
                'obj1':obj1
            }       
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)


def batchAddBrn_no(request):
    if request.method == 'GET' and request.is_ajax():  
        sno= request.GET.get('id')
        obj1=list(Batch.objects.filter(brn_no=sno).values('brn_no').distinct())
        context={
            'obj1':obj1,
        }
        return JsonResponse({'data':context},safe = False)                         
    return JsonResponse({"success":False},status=400)



def batchAdditionsave(request):
    if request.method == 'GET' and request.is_ajax():
        txtB_Type= request.GET.get('txtB_Type')
        txtBO_No= request.GET.get('txtBO_No')
        txtEp_Type= request.GET.get('txtEp_Type')
        txtEp_Desc= request.GET.get('txtEp_Desc')
        txtBrn_No= request.GET.get('txtBrn_No')

        if request.GET.get('txtB_Expl_Dt')=='' or request.GET.get('txtB_Expl_Dt')==None :
            txtB_Expl_Dt=None
        else:
            txtB_Expl_Dt= datetime.datetime.strptime(request.GET.get('txtB_Expl_Dt'),'%d-%m-%Y').date()

        txtBatch_Qty= request.GET.get('txtBatch_Qty')
        txtStatus= request.GET.get('txtStatus')
        txtLoco_Fr= request.GET.get('txtLoco_Fr')
        txtLoco_To= request.GET.get('txtLoco_To')
        txtPart_No= request.GET.get('txtPart_No')
        txtDesc= request.GET.get('txtDesc')
        txtSCNNO= request.GET.get('txtSCNNO')
       
        if request.GET.get('txtRel_Date')=='' or request.GET.get('txtRel_Date')==None :
            txtRel_Date=None
        else:
            txtRel_Date= datetime.datetime.strptime(request.GET.get('txtRel_Date'),'%d-%m-%Y').date()
            
        if request.GET.get('txtRel_Dt_Bc')=='' or request.GET.get('txtRel_Dt_Bc')==None :
            txtRel_Dt_Bc=None
        else:
            txtRel_Dt_Bc= datetime.datetime.strptime(request.GET.get('txtRel_Dt_Bc'),'%d-%m-%Y').date()

        if request.GET.get('txtClos_Dt_B')=='' or request.GET.get('txtClos_Dt_B')==None :
            txtClos_Dt_B=None
        else:
            txtClos_Dt_B= datetime.datetime.strptime(request.GET.get('txtClos_Dt_B'),'%d-%m-%Y').date()

        if request.GET.get('txtClos_Dt_C')=='' or request.GET.get('txtClos_Dt_C')==None :
            txtClos_Dt_C=None
        else:
            txtClos_Dt_C= datetime.datetime.strptime(request.GET.get('txtClos_Dt_C'),'%d-%m-%Y').date()

        if request.GET.get('txtB_Close_dt')=='' or request.GET.get('txtB_Close_dt')==None :
            txtB_Close_dt=None
        else:
            txtB_Close_dt= datetime.datetime.strptime(request.GET.get('txtB_Close_dt'),'%d-%m-%Y').date()

        txtSo_No= request.GET.get('txtSo_No')
        txtBal_Qty= request.GET.get('txtBal_Qty')
        txtProgress= request.GET.get('txtProgress')
        txtRemark= request.GET.get('txtRemark')
        lblmDivsn= request.GET.get('lblmDivsn')
        mSeq= request.GET.get('mSeq')
        mUot_wk_f= request.GET.get('mUot_wk_f')

        Batch.objects.create(bo_no=txtBO_No,part_no=txtPart_No,ep_type=txtEp_Type,brn_no=float(txtBrn_No),status=txtStatus,b_expl_dt=txtB_Expl_Dt,loco_fr=txtLoco_Fr,loco_to=txtLoco_To,batch_type=txtB_Type,rel_date=txtRel_Date,b_close_dt=txtB_Close_dt,rel_dt_bc=txtRel_Dt_Bc,clos_dt_b=txtClos_Dt_B,clos_dt_c=txtClos_Dt_C,so_no=txtSo_No,batch_qty=float(txtBatch_Qty),bal_qty=float(txtBal_Qty),progress=txtProgress,remark=txtRemark,scno=float(txtSCNNO),div=lblmDivsn,seq=mSeq,uot_wk_f=mUot_wk_f)
        Schdesc.objects.create(brn_no=float(txtBrn_No),des=txtDesc)
        obj2=list(Schdesc.objects.filter(brn_no=float(txtBrn_No)).values('des','brn_no').distinct())
        obj1=list(Batch.objects.filter(brn_no=txtBrn_No,bo_no=txtBO_No).values('bo_no','part_no','ep_type','brn_no','status','b_expl_dt','loco_fr','loco_to','div','seq','batch_type','rel_date','b_close_dt','rel_dt_bc','clos_dt_b','clos_dt_c','so_no','batch_qty','bal_qty','progress','remark','scno','uot_wk_f').distinct())
        context={
            'obj1':obj1, 
            'obj2':obj2, 
            }   
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status = 400)

def batchAddupdatedata(request):
    if request.method == "GET" and request.is_ajax():
        txtB_Type= request.GET.get('txtB_Type')
        txtBO_No= request.GET.get('txtBO_No')
        txtEp_Type= request.GET.get('txtEp_Type')
        txtEp_Desc= request.GET.get('txtEp_Desc')
        txtBrn_No= request.GET.get('txtBrn_No')

        if request.GET.get('txtB_Expl_Dt')=='' or request.GET.get('txtB_Expl_Dt')==None :
            txtB_Expl_Dt=None
        else:
            txtB_Expl_Dt= datetime.datetime.strptime(request.GET.get('txtB_Expl_Dt'),'%d-%m-%Y').date()

        txtBatch_Qty= request.GET.get('txtBatch_Qty')
        txtStatus= request.GET.get('txtStatus')
        txtLoco_Fr= request.GET.get('txtLoco_Fr')
        txtLoco_To= request.GET.get('txtLoco_To')
        txtPart_No= request.GET.get('txtPart_No')
        txtDesc= request.GET.get('txtDesc')
        txtSCNNO= request.GET.get('txtSCNNO')
        if request.GET.get('txtRel_Date')=='' or request.GET.get('txtRel_Date')==None :
            txtRel_Date=None
        else:
            txtRel_Date= datetime.datetime.strptime(request.GET.get('txtRel_Date'),'%d-%m-%Y').date()
            
        if request.GET.get('txtRel_Dt_Bc')=='' or request.GET.get('txtRel_Dt_Bc')==None :
            txtRel_Dt_Bc=None
        else:
            txtRel_Dt_Bc= datetime.datetime.strptime(request.GET.get('txtRel_Dt_Bc'),'%d-%m-%Y').date()

        if request.GET.get('txtClos_Dt_B')=='' or request.GET.get('txtClos_Dt_B')==None :
            txtClos_Dt_B=None
        else:
            txtClos_Dt_B= datetime.datetime.strptime(request.GET.get('txtClos_Dt_B'),'%d-%m-%Y').date()

        if request.GET.get('txtClos_Dt_C')=='' or request.GET.get('txtClos_Dt_C')==None :
            txtClos_Dt_C=None
        else:
            txtClos_Dt_C= datetime.datetime.strptime(request.GET.get('txtClos_Dt_C'),'%d-%m-%Y').date()

        if request.GET.get('txtB_Close_dt')=='' or request.GET.get('txtB_Close_dt')==None :
            txtB_Close_dt=None
        else:
            txtB_Close_dt= datetime.datetime.strptime(request.GET.get('txtB_Close_dt'),'%d-%m-%Y').date()
        txtSo_No= request.GET.get('txtSo_No')
        txtBal_Qty= request.GET.get('txtBal_Qty')
        txtProgress= request.GET.get('txtProgress')
        txtRemark= request.GET.get('txtRemark')
        lblmDivsn= request.GET.get('lblmDivsn')
        mSeq= request.GET.get('mSeq')
        mUot_wk_f= request.GET.get('mUot_wk_f')
        Batch.objects.filter(brn_no=float(txtBrn_No)).update(bo_no=txtBO_No,part_no=txtPart_No,ep_type=txtEp_Type,brn_no=float(txtBrn_No),status=txtStatus,b_expl_dt=txtB_Expl_Dt,loco_fr=txtLoco_Fr,loco_to=txtLoco_To,batch_type=txtB_Type,rel_date=txtRel_Date,b_close_dt=txtB_Close_dt,rel_dt_bc=txtRel_Dt_Bc,clos_dt_b=txtClos_Dt_B,clos_dt_c=txtClos_Dt_C,so_no=txtSo_No,batch_qty=float(txtBatch_Qty),bal_qty=float(txtBal_Qty),progress=txtProgress,remark=txtRemark,scno=float(txtSCNNO),div=lblmDivsn,uot_wk_f=mUot_wk_f)
        obj1=list(Batch.objects.filter(brn_no=txtBrn_No,bo_no=txtBO_No).values('bo_no','part_no','ep_type','brn_no','status','b_expl_dt','loco_fr','loco_to','div','seq','batch_type','rel_date','b_close_dt','rel_dt_bc','clos_dt_b','clos_dt_c','so_no','batch_qty','bal_qty','progress','remark','scno','uot_wk_f').distinct())
        context={
            'obj1':obj1,
            
        }       
        return JsonResponse({'data':context}, safe = False)
    return JsonResponse({"success":False}, status=400)
