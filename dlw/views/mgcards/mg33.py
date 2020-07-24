from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/MG33view/')
def MG33view(request):
    import datetime
    rolelist=(g.usermaster).role.split(", ")
    wo_nop = empmast.objects.none()
    empname = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').all()
    dictemper={}
    totindb=0
    examcode = []

    ex = exam_master.objects.all().values('exam_code',)
    for i in ex:
       examcode.append(i['exam_code']) 
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
            'lvdate':"dd-mm-yy",
            'examcode': examcode,
            'empname':empname,
        }
    if(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'lvdate':"dd-mm-yy",
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'lvdate':"dd-mm-yy",
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Add':
            rolelist=(g.usermaster).role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            lvdate=request.POST.get('updt_date')
            examcode = []
            ex = exam_master.objects.all().values('exam_code')
            for i in ex:
                examcode.append(i['exam_code']) 
           
           
            w1=Shemp.objects.filter(shopsec=shop_sec).values('name').distinct()
            wono=[]
            for w in range(len(w1)):
                wono.append(w1[w]['name'])
            w2 = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname')
            names=[]
            for w in range(len(w2)):
                names.append(w2[w]['empname'])
            
            alt_date="yyyy-mm-dd"
           
           
            if "Superuser" in rolelist:
                
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':names,
                    'names':wono,
                    'usermaster':g.usermaster,
                     'totindb':0,
                    'alt_date':alt_date,
                    'examcode': examcode
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname').distinct

                  
                context = {
                    'sub':1,
                    'subnav':g.subnav,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':names,
                    'names':wono,
                    'examcode': examcode
                   
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'usermaster':g.usermaster,
                    'roles' :tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':names,
                    'names':wono,
                    'examcode': examcode
                }
        
        if submitvalue=='Save':
            tot=request.POST.get('totmebs')
             
            place_exam = request.POST.get('place')
            prac_desc = request.POST.get('pracdesc')
            oral_desc = request.POST.get('oraldescr')
            sec_sup = request.POST.get('sec_sup')
            trade_test_officer= request.POST.get('trade_test_officer')
            foreman = request.POST.get('foreman')
            trade_test_admin = request.POST.get('trade_test_admin')
            examdate = request.POST.get('exam_date')
            shop_sec = request.POST.get('shop_sec')
            examcode = request.POST.get('exam_code')
            exam_sno=request.POST.get('exam_sno')
            orscore=request.POST.get('orscore')
            pscore=request.POST.get('prac')
            skills=request.POST.get('skillname')
            epname=request.POST.get('nameoname')
            stfno=request.POST.get('ticketfname')               
            pramedakno=request.POST.get('pramedakno')
            attachment=request.FILES['attachment']
            join_date=request.POST.get('updt_date')
            designation=request.POST.get('designation')
            department=request.POST.get('department')
            temp=float(orscore)+float(pscore)
            if temp >55:
              result='PASS'
            else:
              result='FAIL' 
            newdoc = MG33new(
                exam_sno=str(exam_sno),
                exam_date=str(examdate),
                updt_date =str(datetime.datetime.now().strftime ("%d-%m-%Y")),
                join_date =str(join_date),
                result=str(result),
                exam_code=str(examcode),
                shop_sec = str(shop_sec),
                name=str(epname), 
                skill=str(skills),
                staff_no=str(stfno),                 
                prac_score= str(pscore),
                oral_score= str(orscore),
                prac_desc= str(prac_desc),
                oral_desc= str(oral_desc),
                total_marks = str(temp), 
                sec_sup= str(sec_sup), 
                trade_test_officer = str(trade_test_officer),
                foreman= str(foreman),
                trade_test_admin= str(trade_test_admin), 
                place_of_exam=str(place_exam),
                pramedak_no=str(pramedakno),
                department=str(department),
                designation=str(designation),
                attachment=attachment,
                )
            newdoc.save()

            messages.success(request, 'Successfully Saved !!!, Select new values to update')
    return render(request, "MGCARD/MG33CARD/MG33view.html", context)
    
    
    
def mg33report(request):
    
    wo_nop = empmast.objects.none()
    stfno=set()
    ex=MG33new.objects.all().values('staff_no')
    for i in ex:
        if i['staff_no'] is not None:
            stfno.add(i['staff_no'])
    
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
        'obj':stfno,
    }
     
    if request.method=="POST":
        bval=request.POST.get('proceed')
        if bval=='Proceed':
            
            stfno=set()
            

            
            ex=MG33new.objects.all().values('staff_no')
            for i in ex:
                if i['staff_no'] is not None:
                    stfno.add(i['staff_no'])
            shpsec = request.POST.get('shop_sec')
            staffno=request.POST.get('staff_no')
            update=request.POST.get('updt_date')
            ex = MG33new.objects.filter(shop_sec=shpsec,staff_no=staffno,updt_date=update).all()
            if ex:
                print("if") 
                pscore=ex[0].prac_score
                oscore=ex[0].oral_score
                result=ex[0].result
                trdadmin=ex[0].trade_test_admin
                worker=ex[0].name
                secsup=ex[0].sec_sup
                trdoff=ex[0].trade_test_officer
                print(ex)
                excode=set()
                j=0
                for i in range(len(ex)):
                    excode.add(ex[i].exam_code)
                print(excode)
                for a in excode:
                    obj1=exam_master.objects.filter(exam_code=a)
             
                if(len(rolelist)==1):
                    for i in range(0,len(rolelist)):
                        w1 = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname').distinct
                    context = {
                        'sub':1,
                        'subnav':g.subnav,
                        'lenm' :len(rolelist),
                        'wo_nop':wo_nop,
                        'nav':g.nav,
                        'ip':get_client_ip(request),
                        'usermaster':g.usermaster,
                        'roles' :tmp,
                        'shopsec':shpsec,
                        'obj':stfno,
                        'obj2':ex,
                        'obj1':obj1,
                        'pscore':pscore,'oscore':oscore,'result':result,
                        'trdadmin':trdadmin,'worker':worker,'trdoff':trdoff,'secsup':secsup,
                    }
                elif(len(rolelist)>1):
                    context = {
                        'sub':1,
                        'lenm' :len(rolelist),
                        'nav':g.nav,
                        'subnav':g.subnav,
                        'ip':get_client_ip(request),
                        'usermaster':g.usermaster,
                        'roles' :tmp,
                        'shopsec':shpsec,
                        'obj':stfno,
                        'obj2':ex,
                        'obj1':obj1,
                        'pscore':pscore,'oscore':oscore,'result':result,
                        'trdadmin':trdadmin,'worker':worker,'trdoff':trdoff,'secsup':secsup,
                    }
            else:
                print("else") 
                messages.error(request,"Data Not found!")         
        
    return render(request,"MGCARD/MG33CARD/mg33report.html",context)


@login_required
@role_required(urlpass='/MG33view/')
def exam_detail(request):    
    rolelist=usermaster.role.split(", ")     
    context={
            'totindb':0,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'subnav':g.subnav,
        }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='View':
            ecode=request.POST.get('ecode')
            ex=exam_master.objects.all().order_by('id')
            leng=len(ex)
            context={
                'sub':1,
                'obj':ex,
                'totindb':0,
                'leng':leng,
                'nav':g.nav,
            'ip':get_client_ip(request),
            'subnav':g.subnav,
            }
        if bval=='Save':
            tot=request.POST.get('total')
            if tot=='':
                tot=0
            else:
                tot=int(tot)+1
                for i in range(1,int(tot)):
                    if (request.POST.get("ecode"+str(i))):
                        ecode=request.POST.get("ecode"+str(i))
                        etype=request.POST.get("etype"+str(i))                         
                        prcmarks=request.POST.get("pracmax"+str(i))                       
                        oralmarks=request.POST.get("orlmax"+str(i))
                        edate=request.POST.get("edate"+str(i))
                        department = request.POST.get("department"+str(i))
                        designation =request.POST.get("designation"+str(i))
                        exam_master.objects.create(exam_code=ecode,exam_type=etype,department=department,prac_max=prcmarks,designation=designation,oral_max=oralmarks)
            ex1=request.POST.get('length')
            print("exist",ex1)
            for j in range(1,len(ex1)+1):
                print(j)
                if (request.POST.get("code"+str(j))):
                    ecode=request.POST.get("code"+str(j))
                    etype=request.POST.get("type"+str(j))
                    prctd=request.POST.get("prc"+str(j))
                    prcmrk=request.POST.get("pmax"+str(j))
                    orald=request.POST.get("orl"+str(j))
                    orlmrk=request.POST.get("omax"+str(j))
                    edt=request.POST.get("date"+str(j))
                    exam_master.objects.filter(exam_code=ecode).update(exam_type=etype,prac_desc=prctd,prac_max=prcmrk,oral_desc=orald,oral_max=orlmrk,exam_date=edt)
            messages.success(request,'Successfully Saved!!')
    return render(request,"MGCARD/MG33CARD/examdetail.html",context)

def mg33getstaffno(request):
    if request.method == "GET" and request.is_ajax():  
        from.models import Batch      
        shop_sec = request.GET.get('shop_sec')
        name=request.GET.get('name')
        desgn=request.GET.get('desgn')
        w1=Shemp.objects.filter(shopsec=shop_sec,name=name, ).values('staff_no','desgn').distinct()

        wono = w1[0]['staff_no']
        cont ={
            "wono":wono,
        }
        return JsonResponse({"cont":cont}, safe = False)

    return JsonResponse({"success":False}, status=400)
def mg33getstaffdetails(request):
    if request.method == "GET" and request.is_ajax():  
        from.models import Batch      
        shop_sec = request.GET.get('shop_sec')        
        shop=list(Shemp.objects.filter(shopsec=shop_sec).values('updt_date','staff_no','name').distinct()) 
         
        return JsonResponse({'data':shop}, safe = False)

    return JsonResponse({"success":False}, status=400)

def mg33getexam(request):
    if request.method == "GET" and request.is_ajax():  
        examcode= request.GET.get('two')
        
        ex = exam_master.objects.filter(exam_code= examcode).all()    
     
        exam ={

            "exam_type":ex[0].exam_type,
            "exam_date":ex[0].exam_date,
            "department":ex[0].department,
            "designation":ex[0].designation,
        }
        
        return JsonResponse({"exam":exam}, safe = False)

    return JsonResponse({"success":False}, status=400)
	


def mg33getexamdata(request):
    if request.method == "GET" and request.is_ajax():  
       
        id= request.GET.get('id')
        ex = MG33new.objects.filter(staff_no=id).all()
        officer= ex[0].trade_test_officer
        admin= ex[0].trade_test_admin
        foreman= ex[0].foreman
        sec_sup= ex[0].sec_sup
        
        empsec_supdet= empmast.objects.filter(empno=sec_sup,dept_desc='MECHANICAL').all()        
        empadmindet= empmast.objects.filter(empno=admin,dept_desc='MECHANICAL').all()       
        empforemandet=empmast.objects.filter(empno=foreman,dept_desc='MECHANICAL').all()  
        empofficerdet=empmast.objects.filter(empno=officer,dept_desc='MECHANICAL').all()
         
        data ={
        "sno":ex[0].exam_sno,
        "updt_date":ex[0].updt_date,
        "join_date":ex[0].join_date,
        "shop_sec":ex[0].shop_sec,
        "name":ex[0].name,
        "staff_no":ex[0].staff_no,
        "skill":ex[0].skill,
        "exam_code":ex[0].exam_code,
        "exam_date":ex[0].exam_date,
        "prac_desc":ex[0].prac_desc,
        "prac_score":ex[0].prac_score,
        "oral_desc":ex[0].oral_desc,
        "oral_score":ex[0].oral_score,
        "total_marks":ex[0].total_marks,
        "result":ex[0].result,
        "place_of_exam":ex[0].place_of_exam, 
        "sec_sup_no":empsec_supdet[0].empno,
        "sec_sup_name":empsec_supdet[0].empname,
        "sec_sup_design":empsec_supdet[0].desig_longdesc,
        
        "foreman_no":empforemandet[0].empno,
        "foreman_name":empforemandet[0].empname,
        "foreman_design":empforemandet[0].desig_longdesc,
        "officer_no":empofficerdet[0].empno,
        "officer_name":empofficerdet[0].empname,
        "officer_design":empofficerdet[0].desig_longdesc,
        "admin_no":empadmindet[0].empno,
        "admin_name":empadmindet[0].empname,
        "admin_design":empadmindet[0].desig_longdesc,          
        "department":ex[0].department,
        "designation":ex[0].designation,
        "pramedak_no":ex[0].pramedak_no,
        
        }
        
        return JsonResponse({"data":data}, safe = False)

    return JsonResponse({"success":False}, status=400)  


@login_required
@role_required(urlpass='/MG33view/')
def view_exam_data(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    ex=MG33new.objects.all().order_by('id')
    context={
            'totindb':0,
            'nav':nav,
            'ip':get_client_ip(request),
            'subnav':subnav,
            'obj':ex,
        }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='View Exam Detail':
            ecode=request.POST.get('ecode')
            ex=MG33new.objects.all().order_by('id')
            leng=len(ex)
            context={
                'sub':1,
                'obj':ex,
                'totindb':0,
                'leng':leng,
                'nav':nav,
            'ip':get_client_ip(request),
            'subnav':subnav,
            }
        if bval=='Save':
            tot=request.POST.get('total')
            if tot=='':
                tot=0
            else:
                tot=int(tot)+1
                for i in range(1,int(tot)):
                    if (request.POST.get("ecode"+str(i))):
                        ecode=request.POST.get("ecode"+str(i))
                        etype=request.POST.get("etype"+str(i))
                        prctd=request.POST.get("practical"+str(i))
                        prcmarks=request.POST.get("pracmax"+str(i))
                        orald=request.POST.get("oral"+str(i))
                        oralmarks=request.POST.get("orlmax"+str(i))
                        edate=request.POST.get("edate"+str(i))
                        exam_master.objects.create(exam_code=ecode,exam_type=etype,exam_date=edate,prac_desc=prctd,prac_max=prcmarks,oral_desc=orald,oral_max=oralmarks)
            ex1=request.POST.get('length')
            for j in range(1,len(ex1)+1):
                if (request.POST.get("code"+str(j))):
                    ecode=request.POST.get("code"+str(j))
                    etype=request.POST.get("type"+str(j))
                    prctd=request.POST.get("prc"+str(j))
                    prcmrk=request.POST.get("pmax"+str(j))
                    orald=request.POST.get("orl"+str(j))
                    orlmrk=request.POST.get("omax"+str(j))
                    edt=request.POST.get("date"+str(j))
                    exam_master.objects.filter(exam_code=ecode).update(exam_type=etype,prac_desc=prctd,prac_max=prcmrk,oral_desc=orald,oral_max=orlmrk,exam_date=edt)
            messages.success(request,'Successfully Saved!!')
    return render(request,"MGCARD/MG33CARD/mg33viewdata.html",context)



