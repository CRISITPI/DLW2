from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/mg18view/')
def mg18view(request):
      
    form=list(MG18.objects.all().values('id').distinct().order_by('-id'))

    if(form==[]):
        sno=1
    else:
        sno=form[0]['id']
        sno=int(sno)+1

    context={
        'sub':0,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'subnav':g.subnav,
        'sno':sno,
        'usermaster':g.usermaster
    }
    return render(request, "MGCARD/MG18CARD/mg18view.html",context) 

def mg18InfoSave(request):
    context={}
    if request.method == "GET" and request.is_ajax():
            s_no=request.GET.get('s_no')
            date=request.GET.get('date')
            occupier_name=request.GET.get('occupier_name')
            occupier_addr=request.GET.get('occupier_addr')   
            empcode_Id=request.GET.get('empcode_Id') 
            industry_id=request.GET.get('industry_id') 
            address_acc=request.GET.get('address_acc')  
            branch_Id=request.GET.get('branch_Id')
            injured_name=request.GET.get('injured_name')
            injured_addr=request.GET.get('injured_addr')
            insur_no=request.GET.get('insur_no')
            gender1=request.GET.get('gender1')  
            agebirth_Id=request.GET.get('agebirth_Id')
            occupation_id=request.GET.get('occupation_id')
            date_accident=request.GET.get('date_accident')
            time_accident=request.GET.get('time_accident')
            time2=request.GET.get('time2')  
            cause_Id=request.GET.get('cause_Id')
            yn_id=request.GET.get('yn_id')
            machine_name=request.GET.get('machine_name')
            movmachpwr_Id=request.GET.get('movmachpwr_Id')
            injdoin_Id=request.GET.get('injdoin_Id')  
            injury_nature=request.GET.get('injury_nature')
            offwrk_Id=request.GET.get('offwrk_Id')
            doct_name=request.GET.get('doct_name')
            evident_name=request.GET.get('evident_name')
            c1=request.GET.get('c1')
            c2=request.GET.get('c2')
            c3=request.GET.get('c3')
            howaccident=request.GET.get('howaccident')
            injury_loc=request.GET.get('injury_loc')
            injretrn_Id=request.GET.get('injretrn_Id')
            datertn_Id=request.GET.get('datertn_Id')
            timertn_Id=request.GET.get('timertn_Id')
            yn1_id=request.GET.get('yn1_id')
            date_death=request.GET.get('date_death')
            Insur_lo=request.GET.get('Insur_lo')
            Insur_dis=request.GET.get('Insur_dis')
            distrct_Id=request.GET.get('distrct_Id')
            receipt_date=request.GET.get('receipt_date')
            accident_no=request.GET.get('accident_no')
            industry_no=request.GET.get('industry_no')
            causno=request.GET.get('causno')
            gender2=request.GET.get('gender2')
            otherpart=request.GET.get('otherpart')
            invest_date=request.GET.get('invest_date')
            invest_result=request.GET.get('invest_result')
            if c1=='true':
                c1='Yes'
            else:
                c1='No'

            if c2=='true':
                c2='Yes'
            else:
                c2='No'
            if c3=='true':
                c3='Yes'  
            else:
                c3='No'  
            cuser=request.user
            now = datetime.datetime.now()
            temp =MG18.objects.filter(s_no=s_no).distinct()
            if len(temp) == 0:
                obj=MG18.objects.create( s_no=str( s_no),date=str(date),login_id=str(cuser),name_occupier=str(occupier_name),address_occupier=str(occupier_addr),empcode=str(empcode_Id),
                nature_of_industry=str(industry_id),address_accident =str( address_acc),branch_at_accident=str(branch_Id),name_injured=str(injured_name),
                address_injured=str(injured_addr),insurance_no=str(insur_no),gender=str(gender1),age_last_birth=str(agebirth_Id),occupation_of_injured=str(occupation_id),
                accident_date=str(date_accident),accident_time=str(time_accident),hour_of_startwork=str(time2),cause=str(cause_Id),cause_by_machine=str(yn_id),
                machine_part=str(machine_name),mach_mov_state=str(movmachpwr_Id),injured_doing=str(injdoin_Id),injury_nature=str(injury_nature),
                injured_dayoff=str(offwrk_Id),doctor_name=str(doct_name),name_evid=str(evident_name),inj_under_drink_drug=str(c1),wilful_disobedience=str(c2),
                wilful_removal=str(c3),how_accident=str(howaccident),injury_location=str(injury_loc),inj_return_to_work=str(injretrn_Id),return_date=str(datertn_Id),
                return_time=str(timertn_Id),injured_died=str(yn1_id),date_of_death=str(date_death),insur_localoffice_name=str(Insur_lo),insur_dispensary_name=str(Insur_dis),
                district=str(distrct_Id),receipt_date=str(receipt_date),accident_no=str(accident_no),industry_no=str(industry_no),causation_no=str(causno),gender_1=str(gender2),
                particulars=str(otherpart),investigation_date =str(invest_date),investigation_result=str(invest_result),last_modified=now)

            else:
                MG18.objects.filter(s_no=s_no).update(s_no=str(s_no),date=str(date),login_id=str(cuser),name_occupier=str(occupier_name),address_occupier=str(occupier_addr),empcode=str(empcode_Id),
                nature_of_industry=str(industry_id),address_accident =str( address_acc),branch_at_accident=str(branch_Id),name_injured=str(injured_name),
                address_injured=str(injured_addr),insurance_no=str(insur_no),gender=str(gender1),age_last_birth=str(agebirth_Id),occupation_of_injured=str(occupation_id),
                accident_date=str(date_accident),accident_time=str(time_accident),hour_of_startwork=str(time2),cause=str(cause_Id),cause_by_machine=str(yn_id),
                machine_part=str(machine_name),mach_mov_state=str(movmachpwr_Id),injured_doing=str(injdoin_Id),injury_nature=str(injury_nature),
                injured_dayoff=str(offwrk_Id),doctor_name=str(doct_name),name_evid=str(evident_name),inj_under_drink_drug=str(c1),wilful_disobedience=str(c2),
                wilful_removal=str(c3),how_accident=str(howaccident),injury_location=str(injury_loc),inj_return_to_work=str(injretrn_Id),return_date=str(datertn_Id),
                return_time=str(timertn_Id),injured_died=str(yn1_id),date_of_death=str(date_death),insur_localoffice_name=str(Insur_lo),insur_dispensary_name=str(Insur_dis),
                district=str(distrct_Id),receipt_date=str(receipt_date),accident_no=str(accident_no),industry_no=str(industry_no),causation_no=str(causno),gender_1=str(gender2),
                particulars=str(otherpart),investigation_date =str(invest_date),investigation_result=str(invest_result),last_modified=now)

            return JsonResponse(context,safe=False)
    return JsonResponse({"success":False}, status=400)

def mg18GenerateReport(request, *args, **kwargs):
    s_no=request.GET.get('s_no')
    date=request.GET.get('date')
    occupier_name=request.GET.get('occupier_name')
    occupier_addr=request.GET.get('occupier_addr')   
    empcode_Id=request.GET.get('empcode_Id') 
    industry_id=request.GET.get('industry_id') 
    address_acc=request.GET.get('address_acc')  
    branch_Id=request.GET.get('branch_Id')
    injured_name=request.GET.get('injured_name')
    injured_addr=request.GET.get('injured_addr')
    insur_no=request.GET.get('insur_no')
    gender1=request.GET.get('gender1')  
    agebirth_Id=request.GET.get('agebirth_Id')  
    occupation_id=request.GET.get('occupation_id')
    date_accident=request.GET.get('date_accident')
    time_accident=request.GET.get('time_accident')
    time2=request.GET.get('time2')  
    cause_Id=request.GET.get('cause_Id')
    yn_id=request.GET.get('yn_id')
    machine_name=request.GET.get('machine_name')
    movmachpwr_Id=request.GET.get('movmachpwr_Id')
    injdoin_Id=request.GET.get('injdoin_Id')  
    injury_nature=request.GET.get('injury_nature')
    offwrk_Id=request.GET.get('offwrk_Id')
    doct_name=request.GET.get('doct_name')
    evident_name=request.GET.get('evident_name')
    c1=request.GET.get('c1')
    c2=request.GET.get('c2')
    c3=request.GET.get('c3')
    howaccident=request.GET.get('howaccident')
    injury_loc=request.GET.get('injury_loc')
    injretrn_Id=request.GET.get('injretrn_Id')
    datertn_Id=request.GET.get('datertn_Id')
    timertn_Id=request.GET.get('timertn_Id')
    yn1_id=request.GET.get('yn1_id')
    date_death=request.GET.get('date_death')
    Insur_lo=request.GET.get('Insur_lo')
    Insur_dis=request.GET.get('Insur_dis')
    distrct_Id=request.GET.get('distrct_Id')
    receipt_date=request.GET.get('receipt_date')
    accident_no=request.GET.get('accident_no')
    industry_no=request.GET.get('industry_no')
    causno=request.GET.get('causno')
    gender2=request.GET.get('gender2')
    otherpart=request.GET.get('otherpart')
    invest_date=request.GET.get('invest_date')
    invest_result=request.GET.get('invest_result') 
    if c1=='true':
        c1='Yes'
    else:
        c1='No'
    if c2=='true':
        c2='Yes'
    else:
        c2='No'
    if c3=='true':
        c3='Yes'
    else:
        c3='No'

    data = {
        's_no':s_no,
        'date':date,
        'occupier_name':occupier_name,
        'occupier_addr':occupier_addr,
        'empcode_Id':empcode_Id,
        'industry_id':industry_id,
        'address_acc':address_acc,
        'branch_Id':branch_Id,
        'injured_name':injured_name,
        'injured_addr':injured_addr,
        'insur_no':insur_no,
        'gender1': gender1,
        'agebirth_Id':agebirth_Id,
        'occupation_id':occupation_id,
        'date_accident':date_accident,
        'time_accident':time_accident, 
        'time2':time2,

        'cause_Id':cause_Id,
        'yn_id':yn_id,
        'machine_name':machine_name,
        'movmachpwr_Id':movmachpwr_Id,
        'injdoin_Id':injdoin_Id,
        'injury_nature':injury_nature,
        'offwrk_Id':offwrk_Id,
        'doct_name':doct_name,
        'evident_name':evident_name,
        'c1':c1,
        'c2':c2,
        'c3':c3,
        'howaccident':howaccident,
        'injury_loc': injury_loc,
        'injretrn_Id':injretrn_Id,
        'datertn_Id':datertn_Id,
        'timertn_Id':timertn_Id,
        'yn1_id':yn1_id, 
        'date_death':date_death,

        'Insur_lo':Insur_lo,
        'Insur_dis':Insur_dis,
        'distrct_Id':distrct_Id,
        'receipt_date':receipt_date,
        'accident_no':accident_no,
        'industry_no':industry_no,
        'causno':causno,
        'gender2':gender2,
        'otherpart':otherpart,
        'invest_date':invest_date,
        'invest_result': invest_result,
         
        }
    pdf = render_to_pdf('MGCARD/MG18CARD/mg18report.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def mg18Details(request):
    if request.method == "GET" and request.is_ajax():  
        s_no = request.GET.get('s_no') 
        obj =list(MG18.objects.filter(s_no = s_no).values('date','name_occupier','address_occupier','empcode','nature_of_industry',
        'address_accident','branch_at_accident','name_injured','address_injured','insurance_no','gender','age_last_birth',
        'occupation_of_injured','accident_date','accident_time','hour_of_startwork','cause','cause_by_machine','machine_part',
        'mach_mov_state','injured_doing','injury_nature','injured_dayoff','doctor_name','name_evid','inj_under_drink_drug',
        'wilful_disobedience','wilful_removal','how_accident','injury_location','inj_return_to_work','return_date',
        'return_time','injured_died','date_of_death','insur_localoffice_name','insur_dispensary_name','district',
        'receipt_date','accident_no','industry_no','causation_no','gender_1','particulars','investigation_date',
        'investigation_result').distinct())
        return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status=400)    

