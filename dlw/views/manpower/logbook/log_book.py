from dlw.views import *
import dlw.views.globals as g


@login_required
@role_required(urlpass='/logbook_record/')
def logbook_record(request):
    from dlw.models import logbook_record
    rolelist=(g.usermaster).role.split(", ")
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    shop_sec=[]
    for on in tm:
        shop_sec.append(on.section_code)
    #shop_sec=shop_section.objects.all().order_by('section_code')
    context={         
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'shop_sec':shop_sec,
        'usermaster':g.usermaster, 
        }

    if request.method=="POST":
        save=request.POST.get('save')
        if save=='save':
            shop_sec=request.POST.get('shop_sec')
            date=request.POST.get('date')
            tolen=request.POST.get('tolen') 
            for i in range(int(tolen)):      
                obj=logbook_record.objects.create()           
                obj.shop_sec=shop_sec
                obj.date=date
                obj.shift=request.POST.get('shift'+str(i))             
                obj.staff_no=request.POST.get('staff_no'+str(i))
                obj.staffname=request.POST.get('staffname'+str(i))
                obj.attandance=request.POST.get('attandance'+str(i))
                obj.stafftype=request.POST.get('stafftype'+str(i)) 
                obj.flag=0            
                obj.save()    
        else:
            shop_sec=request.POST.get('shop_sec')
            date=request.POST.get('date')
            tolen=request.POST.get('tolen')             
            for i in range(int(tolen)): 
                staff_no=request.POST.get('staff_no'+str(i))                 
                attandance=request.POST.get('attandance'+str(i))                 
                logbook_record.objects.filter(shop_sec=shop_sec,date=date,staff_no=staff_no).update(attandance=attandance )

        messages.success(request, 'Successfully Done!')
    return render(request,"MANPOWER/LOGBOOK/logbook.html",context)

@login_required
@role_required(urlpass='/logbook_record/')
def logbook_assign(request):
    from dlw.models import logbook_record
    rolelist=(g.usermaster).role.split(", ")
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    shop_sec=[]
    for on in tm:
        shop_sec.append(on.section_code)
    context={         
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'shop_sec':shop_sec ,
        'usermaster':g.usermaster,
        
        }

    if request.method=="POST":         
       
        m_w_no=request.POST.get('mwno')
        pid=request.POST.get('id')
        shop_sec=request.POST.get('shop_sec')
        date=request.POST.get('date')
        opnno=request.POST.get('opn')            
        m5glsno=request.POST.get('m5glno')            
        staff_no=request.POST.get('staffno')
        staffname=request.POST.get('staffname')  
        out_turn=request.POST.get('outturn')
        opn_desc=request.POST.get('asswork') 
        flag=1
        logbook_record.objects.filter(id=pid).update( m_w_no=m_w_no, m5glsno=m5glsno, opnno=opnno,out_turn=out_turn,opn_desc=opn_desc,flag=flag)
       
    return render(request,"MANPOWER/LOGBOOK/logbook_assign.html",context)
 
def logbook_attendence(request):
    from dlw.models import logbook_record
    
    rolelist=(g.usermaster).role.split(", ")
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    shop_sec=[]
    for on in tm:
        shop_sec.append(on.section_code)
         
    context={         
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'shop_sec':shop_sec ,
        'usermaster':g.usermaster,
        
        }

    if request.method=="POST":         
       
        m_w_no=request.POST.get('mwno')
        pid=request.POST.get('id')
        shop_sec=request.POST.get('shop_sec')
        date=request.POST.get('date')
        opnno=request.POST.get('opn')            
        m5glsno=request.POST.get('m5glno')            
        staff_no=request.POST.get('staffno')
        staffname=request.POST.get('staffname')  
        out_turn=request.POST.get('outturn')
        opn_desc=request.POST.get('asswork') 
        flag=1
        logbook_record.objects.filter(id=pid).update( m_w_no=m_w_no, m5glsno=m5glsno, opnno=opnno,out_turn=out_turn,opn_desc=opn_desc,flag=flag)
       
    return render(request,"MANPOWER/LOGBOOK/logbook_attendence.html",context)

def logbook_editdata(request):
    from dlw.models import logbook_record
    if request.method == "GET" and request.is_ajax():
        shop_sec=request.GET.get('shop_sec') 
        pid=request.GET.get('pid') 
        
        date=request.GET.get('date')       
        record = list(logbook_record.objects.filter(id=pid).values('id','workorderno','staff_no' ,'staffname','date','m_w_no','opn_desc','m5glsno','attandance','opnno','shop_sec','out_turn','timein','timeout','shift','stafftype'))
        
        workorderno=record[0]['workorderno'] 
        if workorderno=='tyo' or workorderno=='mis' :
           m5doc=list(logbook_work_desc.objects.filter(work_type=workorderno).values('Work_desc'))
        else:  
           m5doc=list(M5Docnew1.objects.filter(shop_sec=shop_sec,batch_no=workorderno).values('shop_sec','opn_desc','opn','batch_no','m5glsn'))
        
        context={
          'data':record, 
          'm5doc' :m5doc ,
          
               
        }

        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)
def logbook_submitf(request):
    from dlw.models import logbook_record
    if request.method == "GET" and request.is_ajax():
        shop_sec=request.GET.get('shop_sec')
        date=request.GET.get('date')
        pid=request.GET.get('pid') 
        staffno=request.GET.get('staffno')
        staffname=request.GET.get('staffname')
        stafftype=request.GET.get('stafftype')
        shift=request.GET.get('shift')
        m_w_no=request.GET.get('m_w_no')               
        workorderno=request.GET.get('workorderno')            
        m5glsno=request.GET.get('m5glsno')
        timein=request.GET.get('timein')
        timeout=request.GET.get('timeout')
        out_turn=request.GET.get('outturn')
        opnno=request.GET.get('opnno')   
        opn_desc=request.GET.get('opn_desc') 
        flag=1
        if pid == '0':
            logbook_record.objects.create(attandance='P',staff_no=str(staffno),staffname=str(staffname) ,stafftype=str(stafftype),shift=str(shift),shop_sec=str(shop_sec),date=str(date), m_w_no=str(m_w_no),workorderno=str(workorderno),m5glsno=str(m5glsno), opnno=str(opnno),out_turn=str(out_turn),opn_desc=str(opn_desc),timein=str(timein),timeout=str(timeout),flag=str(flag))
        else :
            logbook_record.objects.filter(id=pid).update(m_w_no=m_w_no,workorderno=workorderno,m5glsno=m5glsno, opnno=opnno,out_turn=out_turn,opn_desc=opn_desc,timein=timein,timeout=timeout,flag=flag)
           
        staff_no = list(logbook_record.objects.filter(shop_sec=shop_sec,date=date,attandance='P').values('id','staff_no' ,'staffname','date','shift','stafftype').distinct('staff_no'))
        staffListP = list(logbook_record.objects.filter(shop_sec=shop_sec,date=date,attandance='P',flag=1).values('id','workorderno','staff_no' ,'staffname','date','m_w_no','opn_desc','m5glsno','attandance','opnno','shop_sec','out_turn','timein','timeout','shift','stafftype').order_by('id'))    
        m5docdet=list(M5Docnew1.objects.filter(shop_sec=shop_sec).values('shop_sec','opn_desc','opn','batch_no','m5glsn').distinct('batch_no'))
       
        context={
          'staffListP':staffListP,
          'data':staff_no,
          'm5docdet':m5docdet
        }
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)
def logbook_getstaff(request):
    from dlw.models import logbook_record
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        date = request.GET.get('date')
        shift = request.GET.get('shift')
        listss = logbook_record.objects.filter(shop_sec=shop_sec,date=date,shift=shift).all()
        if len(listss)==0:
          staff_no = list(roster1.objects.filter(shop_sec=shop_sec,date=date,shift=shift).values('staffNo','staffName', 'shift' ,'date','stafftype').order_by('staffNo').distinct('staffNo'))       
          rt= len(listss)
        else:
           staff_no = list(logbook_record.objects.filter(shop_sec=shop_sec,date=date,shift=shift).values('id','staff_no','staffname', 'shift' ,'attandance').order_by('staff_no').distinct('staff_no'))
           rt= len(listss)
        return JsonResponse({'data':staff_no,'rt':rt}, safe = False)
    return JsonResponse({"success":False}, status=400)

def logbook_getatten(request):
    from dlw.models import logbook_record
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        date = request.GET.get('date')
        shift = request.GET.get('shift')         
        staff_pres= list(logbook_record.objects.filter(shop_sec=shop_sec,date=date,shift=shift ,attandance='P').values('id','staff_no','staffname', 'shift' ,'attandance').order_by('staff_no').distinct('staff_no'))
           
        staff_abs = list(logbook_record.objects.filter(shop_sec=shop_sec,date=date,shift=shift,attandance='A').values('id','staff_no','staffname', 'shift' ,'attandance').order_by('staff_no').distinct('staff_no'))
         
        return JsonResponse({'data':staff_pres,'absent':staff_abs}, safe = False)
    return JsonResponse({"success":False}, status=400)


def logbook_getm5doc(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        batch_no = request.GET.get('batch_no')
        m5glsn   = request.GET.get('m5glsn')
        
        m5doc=list(M5Docnew1.objects.filter(shop_sec=shop_sec,batch_no=batch_no,m5glsn=m5glsn).values('shop_sec','opn_desc','opn','batch_no','m5glsn','scl_cl','part_no', 'm2slno','rm_qty','pa','at','no_off','m5_cd','pr_shopsec','n_shopsec','qty_ord','tot_rm_qty','l_fr','l_to','m5prtdt','brn_no','assly_no','rm_partno','rm_ut','cut_shear','lc_no','seq','mark','del_fl','status','qty_insp' ,'inspector','date','remarks','worker','rej_qty','rev_qty','acc_qty','rej_mat'))
        context={
            'data':m5doc,             
        }
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)
    

def logbook_getworkdetail(request):
    from dlw.models import logbook_record
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        date = request.GET.get('date')         
        staffListP = list(logbook_record.objects.filter(shop_sec=shop_sec,date=date,attandance='P',flag=1).values('id','workorderno','staff_no' ,'staffname','date','m_w_no','opn_desc','m5glsno','attandance','opnno','shop_sec','out_turn','timein','timeout','shift','stafftype'))      
        staff_no = list(logbook_record.objects.filter(shop_sec=shop_sec,date=date,attandance='P').values('id','staff_no' ,'staffname','date','shift','stafftype').order_by('staff_no').distinct('staff_no'))
        m5docdet=list(M5Docnew1.objects.filter(shop_sec=shop_sec).values('shop_sec','opn_desc','opn','batch_no','m5glsn').order_by('batch_no').distinct('batch_no'))

        context={
            'data':staff_no,
            'm5docdet':m5docdet,
            'staffListP':staffListP,
            
        }
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)
    

def logbook_getm5glno(request):
    from dlw.models import logbook_record
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        work_no = request.GET.get('workorderno')
         
        if work_no=='tyo' or work_no=='mis' :
           m5doc=list(logbook_work_desc.objects.filter(work_type=work_no).values('Work_desc').distinct('Work_desc'))
        else:
           m5doc=list(M5Docnew1.objects.filter(shop_sec=shop_sec,batch_no=work_no).values('shop_sec','opn_desc','opn','batch_no','m5glsn'))

        context={             
            'm5doc':m5doc,
             
        }
        return JsonResponse(context, safe = False)
    return JsonResponse({"success":False}, status=400)

def logbook_desc(request):
    if request.method == "GET" and request.is_ajax():
        workad = request.GET.get('workad')
        work_no = request.GET.get('workorderno')
        Shop_code=request.GET.get('Shop_code')
        logbook_work_desc.objects.create(work_type =str(work_no),Work_desc=str(workad),Shop_code=str(Shop_code))
        data=list(logbook_work_desc.objects.filter(work_type=work_no).values('Work_desc').distinct('Work_desc'))

        return JsonResponse({'data':data}, safe = False)
    return JsonResponse({"success":False}, status=400)
@login_required
@role_required(urlpass='/logbook_delete/')
def logbook_delete(request):
    from dlw.models import logbook_record

    if request.method=="POST":
        var=request.POST.get('del1')
        obj=logbook_record.objects.filter(m_w_no=var)
        obj.delete()
    return render(request,"MANPOWER/LOGBOOK/logbook_delete.html",{}) 

@role_required(urlpass='/logbook_update/')
def logbook_update(request):

    if request.method=="POST":
        
        obj=logbook_record.objects.create()
        obj.m_w_no=request.POST.get('m_w_no')
        obj.job_booked=request.POST.get('job_booked')
        obj.staff_no=request.POST.get('staff_no')
        obj.attandance=request.POST.get('attandance')
        obj.out_turn=request.POST.get('out_turn')
        obj.remarks=request.POST.get('remarks')
        obj.save()        
        logbook_record.objects.filter(m_w_no=obj.m_w_no).update(job_booked=obj.job_booked,staff_no=obj.staff_no,attandance=obj.attandance,out_turn=obj.out_turn,remarks=obj.remarks)
        context = {
                
                'auth':auth,
                'nav':g.nav,
                'subnav':g.subnav,
                'ip':get_client_ip(request),
                'roles' :rolelist,
                'usermaster':g.usermaster,
                
            }

    return render(request,"MANPOWER/LOGBOOK/logbook_update.html",{})
