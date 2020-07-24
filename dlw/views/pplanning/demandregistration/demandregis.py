from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/demandRegistrationview/')

@login_required
@role_required(urlpass='/demandRegistrationview/')
def demandRegistrationview(request):    
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'subnav':g.subnav,
        } 
    if request.method == "POST":       
        SubmitMultipleRowData = request.POST.get('SubmitMultipleRowData')
        dataForm = request.POST.get('dataForm')
        submitvalue = request.POST.get('Edit')

        if SubmitMultipleRowData=="Submit":
            dataFormTemp  = request.POST.get('dataForm')
            context={
            'nav':g.nav,
            'ip':get_client_ip(request),           
            'subnav':g.subnav,
            'staff_no':dataFormTemp.split(',')[0],
            'name':dataFormTemp.split(',')[1],
            'dep':dataFormTemp.split(',')[2],
            'dem_date':dataFormTemp.split(',')[3],
            'dem_RegNo' : dataFormTemp.split(',')[4],
            'sl_no' : dataFormTemp.split(',')[5],
            'part_no' : dataFormTemp.split(',')[6],
            'epc' : dataFormTemp.split(',')[7],
            'Qty' : dataFormTemp.split(',')[8],
            'wo_no' : dataFormTemp.split(',')[9],
            'wo_type' : dataFormTemp.split(',')[10],
            'l_fr' : dataFormTemp.split(',')[11],
            'l_to' : dataFormTemp.split(',')[12],
            'Seq' : dataFormTemp.split(',')[13],
            'week_no' : dataFormTemp.split(',')[14],
            'm2' : dataFormTemp.split(',')[15],
            'm4' : dataFormTemp.split(',')[16],
            'm5' : dataFormTemp.split(',')[17],
            'm14' : dataFormTemp.split(',')[18],
            'check':'1',
            }
            return render(request,"PPRODUCTION/DEMANDREGISTRATION/demandRegistration.html",context)     
        if submitvalue=='Edit':
            staff_no = request.POST.get('staff_no')
            obj=list(Proddem.objects.filter(~Q(status='L') & ~Q(status='E'),staff_no=staff_no).values('staff_no','name','dep','dem_date','dem_regno','slno','part_no','epc','qty','bo_no','batch_type','l_fr','l_to','seq','week_no','m2','m4','m5','m14').distinct())
                    
            for i in range(len(obj)):
                date=obj[i]['dem_date']
                newdate=date.strftime('%d-%m-%Y')
                obj[i].update({'dem_date':newdate})
           
            context={
                'nav':g.nav,
                'ip':get_client_ip(request),           
                'subnav':g.subnav,
                'obj':obj
                }
        return render(request,'PPRODUCTION/DEMANDREGISTRATION/demandRegisEditInfo.html',context)
    return render(request,'PPRODUCTION/DEMANDREGISTRATION/demandRegistration.html',context)

def DemandRegisSave(request):
    if request.method == "GET" and request.is_ajax():
            staff_no = request.GET.get('staff_no')
            name= request.GET.get('name')
            dep = request.GET.get('dep')
            dem_RegNo = request.GET.get('dem_RegNo')
            doc_type = request.GET.get('doc_type')       
            sl_no = request.GET.get('sl_no')
            part_no = request.GET.get('part_no')
            epc = request.GET.get('epc')
            wo_no = request.GET.get('wo_no')
            wo_type = request.GET.get('wo_type')
            loco_from = request.GET.get('loco_from')
            loco_to = request.GET.get('loco_to')
            Qty = request.GET.get('Qty')
            Seq = request.GET.get('Seq') 
            week_no = request.GET.get('week_no')       
            m2 = request.GET.get('m2')        
            m4 = request.GET.get('m4')          
            m5 = request.GET.get('m5')          
            m14 = request.GET.get('m14')          
            dem_others = request.GET.get('dem_others')         
            remark = request.GET.get('remark')          
            status = request.GET.get('status')           
            obj=[]
            d1=date.today()
            OBJ=Proddem.objects.create(staff_no=str(staff_no),name=str(name),dep=str(dep),dem_regno=str(dem_RegNo),dem_date=d1,ddoc_type=str(doc_type),slno=str(sl_no), part_no=str(part_no),epc=str(epc),bo_no=str(wo_no),batch_type=str(wo_type),l_fr=str(loco_from), l_to=str(loco_to),qty=Qty,seq=Seq,week_no=week_no,m2=str(m2),m4=str(m4),m5=str(m5),m14=str(m14),dem_others=str(dem_others),process_dt=d1,loading_dt=d1, print_dt=d1,issue_dt=d1,remark=str(remark),status=str(status)) 
            return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status=400)
def PpncDemStaffNoDetails(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        staff_no=request.GET.get('staff_no')
        obj=list(Proddem.objects.filter(staff_no=staff_no).values('name','dep').distinct().order_by('staff_no','dem_regno','slno'))
        l.append(obj)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)
def PpncDemPartNoDetails(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        partno=request.GET.get('part_no')
        obj=list(Part.objects.filter(partno=partno).values('ptc','alt_link').distinct())
        l.append(obj)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)
def PpncDemEPCDetails(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        epc=request.GET.get('epc')
        part_no=request.GET.get('part_no')
        obj=list(Code.objects.filter(code=epc,cd_type='11').values('num_1').distinct())
        obj1=list(Nstr.objects.filter(pp_part=part_no,epc=epc).values('pp_part').distinct())
        obj2=list(Nstr.objects.filter(cp_part=part_no,epc=epc).values('cp_part').distinct())
        l.append(obj)
        l.append(obj1)
        l.append(obj2)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)
def PpncDemWODetails1(request):
    if request.method=="GET" and request.is_ajax():
        obj1=list(dpoloco.objects.values('batchordno'))      
        return JsonResponse(obj1,safe=False)
    return JsonResponse({"success":False}, status=400)

def PpncDemWODetails(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        wo_no=request.GET.get('wo_no')
        obj=list(Batch.objects.filter(bo_no=wo_no).values('batch_type').distinct())
        l.append(obj)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)
def PpncDemshopdetails(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        tb=request.GET.get('tb')
        obj=list(Shop.objects.filter(shop=tb).values('shop').distinct())
        l.append(obj)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)
def PpncDemGetNewDemno(request):
    l=[]
    d=date.today()
    if request.method=="GET" and request.is_ajax():
        obj=list(Code.objects.filter(cd_type='M2',code='DEMNO').values('num_1').distinct())
        l1=int(obj[0]['num_1'])+1
        l.append(obj)
        Code.objects.filter(cd_type='M2',code='DEMNO').update(num_1=l1,lupd_date=d)  
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)
def DemandRegisStatus(request):
    l=[]
    if request.method=="GET" and request.is_ajax():      
        dem_RegNo=request.GET.get('dem_RegNo')
        obj=list(Proddem.objects.filter(dem_regno=dem_RegNo).values('status','id').distinct())
        l.append(obj)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)

def DemandRegisAddNewDemand(request):
    if request.method == "GET" and request.is_ajax():
            staff_no = request.GET.get('staff_no') 
            name= request.GET.get('name')         
            dep = request.GET.get('dep')           
            dem_RegNo = request.GET.get('dem_RegNo')          
            doc_type = request.GET.get('doc_type')           
            sl_no = request.GET.get('sl_no')            
            part_no = request.GET.get('part_no')           
            epc = request.GET.get('epc')           
            wo_no = request.GET.get('wo_no')           
            wo_type = request.GET.get('wo_type')           
            loco_from = request.GET.get('loco_from')          
            loco_to = request.GET.get('loco_to')          
            Qty = request.GET.get('Qty')          
            Seq = request.GET.get('Seq')           
            week_no = request.GET.get('week_no')           
            m2 = request.GET.get('m2')          
            m4 = request.GET.get('m4')          
            m5 = request.GET.get('m5')
            m14 = request.GET.get('m14')
            dem_others = request.GET.get('dem_others')
            remark = request.GET.get('remark')
            status = request.GET.get('status')
            obj1=[]
            d2=date.today()
            OBJ1=Proddem.objects.create(staff_no=str(staff_no),name=str(name),dep=str(dep),dem_regno=str(dem_RegNo),dem_date=d2,ddoc_type=str(doc_type),slno=str(sl_no), part_no=str(part_no),epc=str(epc),bo_no=str(wo_no),batch_type=str(wo_type),l_fr=str(loco_from), l_to=str(loco_to),qty=Qty,seq=Seq,week_no=week_no,m2=str(m2),m4=str(m4),m5=str(m5),m14=str(m14),dem_others=str(dem_others),process_dt=d2,loading_dt=d2, print_dt=d2,issue_dt=d2,remark=str(remark),status=str(status)) 
            return JsonResponse(obj1,safe = False)
    return JsonResponse({"success":False}, status=400)
def DemandRegisGetSINo(request):
    if request.method == "GET" and request.is_ajax():
        staff_no = request.GET.get('staff_no')
        dem_regno= request.GET.get('dem_RegNo')
        obj=list(Proddem.objects.filter(staff_no=staff_no,dem_regno=dem_regno).values('slno'))
        val=obj[len(obj)-1].get("slno")
        return JsonResponse(val,safe = False)
    return JsonResponse({"success":False}, status=400)
def DemandRegisModifyDemand(request):
    if request.method == "GET" and request.is_ajax():
            staff_no = request.GET.get('staff_no')          
            name= request.GET.get('name')          
            dep = request.GET.get('dep')          
            dem_RegNo = request.GET.get('dem_RegNo')
            doc_type = request.GET.get('doc_type')
            sl_no = request.GET.get('sl_no')
            part_no = request.GET.get('part_no')
            epc = request.GET.get('epc')
            wo_no = request.GET.get('wo_no')          
            wo_type = request.GET.get('wo_type')          
            loco_from = request.GET.get('loco_from')
            loco_to = request.GET.get('loco_to')
            Qty = request.GET.get('Qty')
            Seq = request.GET.get('Seq')         
            week_no = request.GET.get('week_no')       
            m2 = request.GET.get('m2')          
            m4 = request.GET.get('m4')       
            m5 = request.GET.get('m5')
            m14 = request.GET.get('m14')
            dem_others = request.GET.get('dem_others')      
            remark = request.GET.get('remark')        
            status = request.GET.get('status')
            obj2=[]
            d3=date.today()
            OBJ2=Proddem.objects.filter(bo_no=wo_no).update(staff_no=str(staff_no),name=str(name),dep=str(dep),dem_regno=str(dem_RegNo),dem_date=d3,ddoc_type=str(doc_type),slno=str(sl_no), part_no=str(part_no),epc=str(epc),bo_no=str(wo_no),batch_type=str(wo_type),l_fr=str(loco_from), l_to=str(loco_to),qty=Qty,seq=Seq,week_no=week_no,m2=str(m2),m4=str(m4),m5=str(m5),m14=str(m14),dem_others=str(dem_others),process_dt=d3,loading_dt=d3, print_dt=d3,issue_dt=d3,remark=str(remark),status=str(status)) 
            return JsonResponse(obj2,safe = False)
    return JsonResponse({"success":False}, status=400)
def DemandRegisDelete(request):
    obj=[]
    if request.method == "GET" and request.is_ajax():
        staff_no = request.GET.get('staff_no')
        dem_regno= request.GET.get('dem_RegNo')
        Proddem.objects.filter(staff_no=staff_no,dem_regno=dem_regno).update(del_fl='Y')
        return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status=400)
def PpncdemViewInfo(request):
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'subnav':g.subnav,
        }  
    return render(request,'PPRODUCTION/DEMANDREGISTRATION/demandRegisViewInfo.html',context) 
def PpncdemEditInfo(request):
   
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'subnav':g.subnav,
        }  
    if request.method == "POST":
        submitvalue = request.POST.get('Edit')
        if submitvalue=='Edit':
            staff_no = request.POST.get('staff_no')
            obj=list(Proddem.objects.filter(staff_no=staff_no).values('dem_regno','slno','part_no','epc','qty','bo_no','bo_type','l_fr','l_to','seq','status').distinct())
            context1={
                'obj':obj
                }
        return render(request,'PPRODUCTION/DEMANDREGISTRATION/demandRegisEditInfo.html',context1)    
    return render(request,'PPRODUCTION/DEMANDREGISTRATION/demandRegisEditInfo.html',context) 
def PpncdemBackClick(request):
      
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'subnav':g.subnav,
        }  
    return render(request,'homeadmin.html',context)
def demandRegistrationReportview(request, *args, **kwargs):
    tmpstr=[]
    rbtnquery= request.GET.get('rbtnquery')
    staffno= request.GET.get('staffno')
    dem_reg=request.GET.get('dem_reg')
    date_from=request.GET.get('date_from')
    date_to=request.GET.get('date_to')
    demReg=request.GET.get('demReg')
    today=date.today().strftime('%d-%m-%Y')
    if(rbtnquery=="1"):
        tmp=list(Proddem.objects.values('dem_date','dem_regno','staff_no','name','slno','part_no','l_fr','l_to','bo_no','qty','epc','batch_type','seq','week_no','m2','m4','m5','m14','ddoc_type','dem_others').filter(dem_regno=dem_reg).distinct().order_by('dem_regno'))
        tmpstr.append(tmp)
        print(tmpstr)     
    if(rbtnquery=="2"):
        tmp=[]
        s1=date_from.split('-')
        month1=s1[1]
        day1=s1[0]
        year1=s1[2]
        newdate_from=year1 + "-" + month1 + "-" + day1
        s2=date_to.split('-')
        month2=s2[1]
        day2=s2[0]
        year2=s2[2]
        newdate_to=year2 + "-" + month2 + "-" + day2
        for i in (Proddem.objects.raw('SELECT "id","DEM_DATE", "DEM_REGNO", "STAFF_NO", "NAME", "SLNO", "PART_NO", "L_FR", "L_TO","BO_NO","QTY","EPC","BATCH_TYPE","SEQ","WEEK_NO","DDOC_TYPE","DEM_OTHERS" FROM "PRODDEM" WHERE "DEM_DATE" >=%s and "DEM_DATE" <=%s order by "DEM_REGNO";',[newdate_from,newdate_to])):
            tmp.append({'dem_date':i.dem_date,'dem_regno':i.dem_regno,'staff_no':i.staff_no,'name':i.name,'slno':i.slno,'part_no':i.part_no,'l_fr':i.l_fr,'l_to':i.l_to,'bo_no':i.bo_no,'qty':i.qty,'epc':i.epc,'batch_type':i.batch_type,'seq':i.seq,'week_no':i.week_no,'m2':i.m2,'m4':i.m4,'m5':i.m5,'m14':i.m14,'ddoc_type':i.ddoc_type,'dem_others':i.dem_others})
        tmpstr.append(tmp)
    if(rbtnquery=="3"):
        tmp=list(Proddem.objects.values('dem_date','dem_regno','staff_no','name','slno','part_no','l_fr','l_to','bo_no','qty','epc','batch_type','seq','week_no','m2','m4','m5','m14','ddoc_type','dem_others').filter(staff_no=staffno).distinct().order_by('dem_regno'))
        tmpstr.append(tmp) 
    if(rbtnquery=="4"):
        tmp=list(Proddem.objects.values('dem_date','dem_regno','staff_no','name','slno','part_no','l_fr','l_to','bo_no','qty','epc','batch_type','seq','week_no','m2','m4','m5','m14','ddoc_type','dem_others').filter(dem_regno=demReg).distinct().order_by('dem_regno'))
        tmpstr.append(tmp)
    lst=[]
    dem=''
    k=0
    j=0
    for i in range(len(tmp)):
        if tmp[i]['dem_regno']==dem:
            tmp[i].update({'c':1})
            lst[k-1].insert(j,(tmp[i]))
            j=j+1
        else:
            j=1
            l=[]
            tmp[i].update({'c':0})
            l.append(tmp[i])
            lst.insert(k,l)
            dem=tmp[i]['dem_regno']
            k=k+1
    context={
        'tmpstr':lst,
        'today':today,
    }
    pdf = render_to_pdf('PPRODUCTION/DEMANDREGISTRATION/demandRegistrationReport.html',context)
    return HttpResponse(pdf, content_type='application/pdf')

def PpncdemGenerateReport(request):
    tmpstr=[]
    today=date.today().strftime('%d-%m-%Y')
    staffno= request.GET.get('staff_no')
    tmp=list(Proddem.objects.values('dem_date','dem_regno','staff_no','name','slno','part_no','l_fr','l_to','bo_no','qty','epc','batch_type','seq','week_no','m2','m4','m5','m14','ddoc_type','dem_others').filter(staff_no=staffno).distinct().order_by('dem_regno'))
    tmpstr.append(tmp)
    lst=[]
    dem=''
    k=0
    j=0
    for i in range(len(tmp)):
        if tmp[i]['dem_regno']==dem:
            tmp[i].update({'c':1})
            lst[k-1].insert(j,(tmp[i]))
            j=j+1
        else:
            j=1
            l=[]
            tmp[i].update({'c':0})
            l.append(tmp[i])
            lst.insert(k,l)
            dem=tmp[i]['dem_regno']
            k=k+1
    context={
        'tmpstr':lst,
        'today':today
    }
    return render(request,'PPRODUCTION/DEMANDREGISTRATION/demandRegistrationPrintReport.html',context)
def PpncDemvalidation1(request):
    if request.method=="GET" and request.is_ajax():  
        dem_reg= request.GET.get('dem_reg')
        obj=list(Proddem.objects.values('dem_date','dem_regno','staff_no','name','slno','part_no','l_fr','l_to','bo_no','qty','epc','batch_type','seq','week_no','m2','m4','m5','m14','ddoc_type','dem_others').filter(dem_regno=dem_reg).distinct().order_by('dem_regno'))
        return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status=400)
def PpncDemvalidation2(request):
    if request.method=="GET" and request.is_ajax():  
        staffNo= request.GET.get('staffNo')
        obj=list(Proddem.objects.values('dem_date','dem_regno','staff_no','name','slno','part_no','l_fr','l_to','bo_no','qty','epc','batch_type','seq','week_no','m2','m4','m5','m14','ddoc_type','dem_others').filter(staff_no=staffNo).distinct().order_by('dem_regno'))
        return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status=400) 
def PpncDemvalidation3(request):
    if request.method=="GET" and request.is_ajax():  
        demReg= request.GET.get('demReg')
        obj=list(Proddem.objects.values('dem_date','dem_regno','staff_no','name','slno','part_no','l_fr','l_to','bo_no','qty','epc','batch_type','seq','week_no','m2','m4','m5','m14','ddoc_type','dem_others').filter(dem_regno=demReg).distinct().order_by('dem_regno'))
        return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status=400)
def PpncDemlocofunc(request):
    if request.method == "GET" and request.is_ajax():
        partno=request.GET.get('part_no')
        epc=request.GET.get('epc')
        eppartno=request.GET.get('ep_part')
        l_to=request.GET.get('l_to')
        p = cpq(partno,epc,eppartno,l_to)
        return JsonResponse(p,safe=False) 
    return JsonResponse({"success:False"},status=400)
assly_ptc=None
cumino=None
qty=None
def PpncDemLocoFromToValue(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        wo_no=request.GET.get('wo_no')
        obj1=list(dpoloco.objects.filter(batchordno=wo_no).values('cumino','qtybatch').distinct())
        for i in range(len(obj1)):
            cumino = str(obj1[i].get('cumino')) 
            qty=str(obj1[i].get('qtybatch'))
        st=cumino.split('-')
        loco_fr=st[0]
        loco_to=st[1]
        l.append(loco_fr)
        l.append(loco_to)
        l.append(qty)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)
def PpncDemlocofunc1(request):
    lst=[]
    if request.method == "GET" and request.is_ajax():
        partno=request.GET.get('part_no')
        epc=request.GET.get('epc')
        cursor = connection.cursor()
        cursor.execute('''select distinct "CP_PART" from "NSTR" where "CP_PART"=%s and "EPC"=%s  limit 1;''',[partno,epc])
        row = cursor.fetchall()
        dts = list(row)
        for i in range(len(dts)):
            lst.append({"cp_part":dts[i][0]})
        return JsonResponse(lst,safe=False) 
    return JsonResponse({"success:False"},status=400) 

def PpncDemlocofunc2(request):
    lst=[]
    if request.method == "GET" and request.is_ajax():
        partno=request.GET.get('part_no')
        epc=request.GET.get('epc')
        l_to=request.GET.get('l_to')
        l_fr=request.GET.get('l_fr')
        cursor = connection.cursor()
        cursor.execute('''select distinct "PTC" from "NSTR" where "CP_PART"=%s and "EPC"=%s and "L_TO" between %s and %s;''',[partno,epc,l_to,l_fr])
        row = cursor.fetchall()
        dts = list(row)
        for i in range(len(dts)):
            lst.append({"ptc":dts[i][0]})
        return JsonResponse(lst,safe=False) 
    return JsonResponse({"success:False"},status=400) 