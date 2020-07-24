from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/NearMissIncidentInvestigation/')
def NearMissIncidentInvestigation(request):
    wo_nop = empmast.objects.none()
    cuser= (g.usermaster).empno
    desig=list(empmast.objects.filter(empno=cuser).values('desig_longdesc').distinct())

    tmp1=''
    for on in desig:
        tmp1=on['desig_longdesc']  
    shopno = list(empmast.objects.filter(empno=cuser).values('shopno').distinct())  
    tmp2=''
    for on in shopno:
        tmp2=on['shopno']

    shop =list(shop_section.objects.filter(shop_id=tmp2).values('shop_code').distinct()) 
    
    tm = ''
    
    for on in shop:
        tm= on['shop_code']
    tm=tm[:-2]
    ssename= list(empmast.objects.filter(empno=cuser).values('empname').distinct()) 
    tmp3=[]
    for on in ssename:
        tmp3=on['empname']

    form=list(NearMissIncident.objects.all().values('sno').distinct().order_by('-sno'))
        
    if(form==[]):
        formid=1
    else:
        formid=form[0]['sno']
        formid=int(formid)+1
    
    context={
            'nav' : g.nav,
            'ip' : get_client_ip(request),
            'subnav' : g.subnav,
            'sno' : formid,
            'shopno' : tm,
            'ssedesig' :tmp1,
            'ssename' : tmp3,
            'usermaster':g.usermaster,
        }
    if request.method == "POST": 
            submitvalue = request.POST.get('Save')
            if submitvalue=='Save':
                sno = request.POST.get('sno')
                date = request.POST.get('date')
                doi=request.POST.get('doi')
                toi=request.POST.get('toi')
                loc=request.POST.get('location')
                unit = request.POST.get('unit')
                ssename=request.POST.get('ssename')
                ssedesig=request.POST.get('ssedesig')
                fire_exp=request.POST.get('fire_exp').strip()
                fire_exp=fire_exp[:200]
                emp_involve=request.POST.get('emp_involve')
                emp_inname=request.POST.get('emp_inname')
                emp_indesig=request.POST.get('emp_indesig')
                otherinvolve=request.POST.get('otherinvolve').strip()
                otherinvolve=otherinvolve[:200]
                briefdes=request.POST.get('briefdes').strip()
                briefdes=briefdes[:200]
                damage_detail=request.POST.get('damage_detail').strip()
                damage_detail=damage_detail[:500]
                yes = request.POST.get('hide2')
                
                if(yes == "0"):
                    attachment=""
                else:
                    attachment=request.FILES['site_sketch']
                sec_bay=request.POST.get('sec_bay')
                machine=request.POST.get('machine')
                
                work_en=request.POST.get('work_en').strip()
                work_en=work_en[:200]
                otherwork_en=request.POST.get('otherwork_en').strip()
                work_en=work_en[:300]
                fail_analysis=request.POST.get('fail_analysis').strip()
                fail_analysis=fail_analysis[:500]
                responsibility=request.POST.get('responsibility').strip()
                responsibility=responsibility[:500]
                corr_action=request.POST.get('corr_action').strip()
                corr_action=corr_action[:500]
                aucomment=request.POST.get('aucomment').strip()
                aucomment=aucomment[:200]

                auinid=request.POST.get('auinid')
                auinname=request.POST.get('auinname')
                auindesig=request.POST.get('auindesig')
                
                now = datetime.datetime.now()
                newdoc= NearMissIncident(sno=str(sno),date=str(date),site_sketch=attachment,incident_date=str(doi),incident_time=str(toi),
                incident_location=str(loc),unit_section=str(unit),sse_id =str(ssename),sse_name=str(ssename), 
                sse_designation=str(ssedesig),fire_explosion=str(fire_exp),employee_involve_id=str(emp_involve),
                employee_involve_name=str(emp_inname),employee_involve_designation=str(emp_indesig),otherinvolve=str(otherinvolve),
                incident_description=str(briefdes),login_id=str(cuser),last_modified=now,
                details_of_damages_to_infrastructure=str(damage_detail),
                section_bay = str(sec_bay),plant_machine_tools = str(machine), condition_of_work_environment = str(work_en),
                others=str(otherwork_en),details_of_analysis_of_incident=str(fail_analysis), responsibility=str(responsibility),
                prevention_and_corrective_action =str(corr_action),comments_of_au_incharge =str(aucomment),
                au_incharge_id = str(auinid),au_incharge_name =str(auinname) ,au_incharge_designation=str(auindesig))
                
                temp= NearMissIncident.objects.filter(sno=str(sno),incident_location=str(loc)).values('sno').distinct()
                if len(temp) == 0:
                    newdoc.save()
                temp = list(NearMissIncident.objects.filter(sno=str(sno),incident_location=str(loc)).values('site_sketch').filter())
                for on in temp:
                    attachment=on['site_sketch'] 
                attachment = attachment.replace("investigationdoc/", "")
                data={
                    'sno' : sno,
                    'date' : date,
                    'doi' : doi,
                    'toi' : toi,
                    'loc' : loc,
                    'unit' : unit,
                    'ssename' : ssename,
                    'ssedesig' : ssedesig,
                    'fire_exp' : fire_exp,
                    'emp_involve' : emp_involve,
                    'emp_inname' :  emp_inname,
                    'emp_indesig' : emp_indesig,
                    'otherinvolve' : otherinvolve,
                    'briefdes' : briefdes,
                    'damage_detail' : damage_detail,
                    'attachment' : attachment,
                    'sec_bay' : sec_bay,
                    'machine' : machine,
                    'work_en' : work_en,
                    'otherwork_en' : otherwork_en,
                    'fail_analysis' : fail_analysis,
                    'responsibility' : responsibility,
                    'corr_action' : corr_action,
                    'aucomment' : aucomment,
                    'auinid' : auinid,
                    'auinname' :auinname,
                    'auindesig' : auindesig,

                }


                pdf = render_to_pdf('NEARMISS/NearMissIncidentInvestReport.html',data)
                return HttpResponse(pdf, content_type='application/pdf')

    if request.method == "POST": 
            submitvalue = request.POST.get('Update')
            if submitvalue=='Update':
                sno = request.POST.get('sno')
                date = request.POST.get('date')
                doi=request.POST.get('doi')
                toi=request.POST.get('toi')
                loc=request.POST.get('location')
                unit = request.POST.get('unit')
                ssename=request.POST.get('ssename')
                ssedesig=request.POST.get('ssedesig')
                fire_exp=request.POST.get('fire_exp').strip()
                emp_involve=request.POST.get('emp_involve')
                emp_inname=request.POST.get('emp_inname')
                emp_indesig=request.POST.get('emp_indesig')
                otherinvolve=request.POST.get('otherinvolve').strip()
                briefdes=request.POST.get('briefdes').strip()
                damage_detail=request.POST.get('damage_detail').strip()
                yes = request.POST.get('hide2')
                if(yes == "0"):
                    attachment=""
                else:
                    attachment=request.FILES['site_sketch']
                sec_bay=request.POST.get('sec_bay')
                machine=request.POST.get('machine')
                work_en=request.POST.get('work_en').strip()
                otherwork_en=request.POST.get('otherwork_en').strip()
                fail_analysis=request.POST.get('fail_analysis').strip()
                responsibility=request.POST.get('responsibility').strip()
                responsibility=responsibility[:500]
                corr_action=request.POST.get('corr_action').strip()                                                                                                                                     
                aucomment=request.POST.get('aucomment').strip()
                auinid=request.POST.get('auinid')
                auinname=request.POST.get('auinname')
                auindesig=request.POST.get('auindesig')
                now = datetime.datetime.now()
                temp = list(NearMissIncident.objects.filter(sno=str(sno),incident_location=str(loc)).values('site_sketch').filter())
                img1=''
                for on in temp:
                    tmp1=on['site_sketch'] 
                NearMissIncident.objects.filter(sno=str(sno),incident_location=str(loc)).delete()
                if(attachment == ""):
                    newdoc= NearMissIncident(sno=str(sno),date=str(date),site_sketch=tmp1,incident_date=str(doi),incident_time=
                    str(toi),incident_location=str(loc),unit_section=str(unit),sse_id =str(ssename),sse_name=str(ssename), 
                    sse_designation=str(ssedesig),fire_explosion=str(fire_exp),employee_involve_id=str(emp_involve),
                    employee_involve_name=str(emp_inname),employee_involve_designation=str(emp_indesig),otherinvolve=str(otherinvolve),
                    incident_description=str(briefdes),login_id=str(cuser),last_modified=now,
                    details_of_damages_to_infrastructure=str(damage_detail),
                    section_bay = str(sec_bay),plant_machine_tools = str(machine), condition_of_work_environment = str(work_en),
                    others=str(otherwork_en),details_of_analysis_of_incident=str(fail_analysis), responsibility=str(responsibility),
                    prevention_and_corrective_action =str(corr_action),comments_of_au_incharge =str(aucomment),
                    au_incharge_id = str(auinid),au_incharge_name =str(auinname) ,au_incharge_designation=str(auindesig))
                    
                else :
                    newdoc= NearMissIncident(sno=str(sno),date=str(date),site_sketch=attachment,incident_date=str(doi),incident_time=
                    str(toi),incident_location=str(loc),unit_section=str(unit),sse_id =str(ssename),sse_name=str(ssename), 
                    sse_designation=str(ssedesig),fire_explosion=str(fire_exp),employee_involve_id=str(emp_involve),
                    employee_involve_name=str(emp_inname),employee_involve_designation=str(emp_indesig),otherinvolve=str(otherinvolve),
                    incident_description=str(briefdes),login_id=str(cuser),last_modified=now,
                    details_of_damages_to_infrastructure=str(damage_detail),
                    section_bay = str(sec_bay),plant_machine_tools = str(machine), condition_of_work_environment = str(work_en),
                    others=str(otherwork_en),details_of_analysis_of_incident=str(fail_analysis), responsibility=str(responsibility),
                    prevention_and_corrective_action =str(corr_action),comments_of_au_incharge =str(aucomment),
                    au_incharge_id = str(auinid),au_incharge_name =str(auinname) ,au_incharge_designation=str(auindesig))
                    
                newdoc.save()
                temp = list(NearMissIncident.objects.filter(sno=str(sno),incident_location=str(loc)).values('site_sketch').filter())
                for on in temp:
                    attachment=on['site_sketch'] 
                attachment = attachment.replace("investigationdoc/", "")
                data={
                    'sno' : sno,
                    'date' : date,
                    'doi' : doi,
                    'toi' : toi,
                    'loc' : loc,
                    'unit' : unit,
                    'ssename' : ssename,
                    'ssedesig' : ssedesig,
                    'fire_exp' : fire_exp,
                    'emp_involve' : emp_involve,
                    'emp_inname' :  emp_inname,
                    'emp_indesig' : emp_indesig,
                    'otherinvolve' : otherinvolve,
                    'briefdes' : briefdes,
                    'damage_detail' : damage_detail,
                    'attachment' : attachment,
                    'sec_bay' : sec_bay,
                    'machine' : machine,
                    'work_en' : work_en,
                    'otherwork_en' : otherwork_en,
                    'fail_analysis' : fail_analysis,
                    'responsibility' : responsibility,
                    'corr_action' : corr_action,
                    'aucomment' : aucomment,
                    'auinid' : auinid,
                    'auinname' :auinname,
                    'auindesig' : auindesig,

                }
               
                pdf = render_to_pdf('NEARMISS/NearMissIncidentInvestReport.html',data)
                return HttpResponse(pdf, content_type='application/pdf')

    if request.method == "POST": 
            submitvalue = request.POST.get('Report')
            if submitvalue=='Report':
                sno = request.POST.get('sno')
                
                date = request.POST.get('date')
                doi=request.POST.get('doi')
                toi=request.POST.get('toi')
                loc=request.POST.get('location')
                unit = request.POST.get('unit')
                ssename=request.POST.get('ssename')
                ssedesig=request.POST.get('ssedesig')
                fire_exp=request.POST.get('fire_exp').strip()
                emp_involve=request.POST.get('emp_involve')
                emp_inname=request.POST.get('emp_inname')
                emp_indesig=request.POST.get('emp_indesig')
                otherinvolve=request.POST.get('otherinvolve').strip()
                briefdes=request.POST.get('briefdes').strip()
                damage_detail=request.POST.get('damage_detail').strip()
                yes = request.POST.get('hide2')
                attachment=request.POST.get('pic')
                sec_bay=request.POST.get('sec_bay')
                machine=request.POST.get('machine')
                work_en=request.POST.get('work_en').strip()
                otherwork_en=request.POST.get('otherwork_en').strip()
                fail_analysis=request.POST.get('fail_analysis').strip()
                responsibility=request.POST.get('responsibility').strip().strip()
                responsibility=responsibility[:500]
                corr_action=request.POST.get('corr_action').strip()
                aucomment=request.POST.get('aucomment').strip()
                auinid=request.POST.get('auinid')
                auinname=request.POST.get('auinname')
                auindesig=request.POST.get('auindesig')
                
                data={
                    'sno' : sno,
                    'date' : date,
                    'doi' : doi,
                    'toi' : toi,
                    'loc' : loc,
                    'unit' : unit,
                    'ssename' : ssename,
                    'ssedesig' : ssedesig,
                    'fire_exp' : fire_exp,
                    'emp_involve' : emp_involve,
                    'emp_inname' :  emp_inname,
                    'emp_indesig' : emp_indesig,
                    'otherinvolve' : otherinvolve,
                    'briefdes' : briefdes,
                    'damage_detail' : damage_detail,
                    'attachment' : attachment,
                    'sec_bay' : sec_bay,
                    'machine' : machine,
                    'work_en' : work_en,
                    'otherwork_en' : otherwork_en,
                    'fail_analysis' : fail_analysis,
                    'responsibility' : responsibility,
                    'corr_action' : corr_action,
                    'aucomment' : aucomment,
                    'auinid' : auinid,
                    'auinname' :auinname,
                    'auindesig' : auindesig,

                }
               
                pdf = render_to_pdf('NEARMISS/NearMissIncidentInvestReport.html',data)
                return HttpResponse(pdf, content_type='application/pdf')
    return render(request, "NEARMISS/NearMissIncidentInvestigation.html",context) 

  

def NearMissIncidentInvestigationDetails(request):
    if request.method == "GET" and request.is_ajax():
        emp_involve = request.GET.get('emp_involve')
        obj1=[]   
        obj1=list(empmast.objects.filter(empno=emp_involve).values('empname','desig_longdesc').distinct())
        return JsonResponse(obj1,safe=False)
    return JsonResponse({"success:False"},status=400)

def NearMissInvestigationGetAllDetails(request):
    if request.method == "GET" and request.is_ajax():
        sno = request.GET.get('sno')
        loc = request.GET.get('loc')
        obj=list(NearMissIncident.objects.filter(sno=sno,incident_location=loc).values('sno','date','incident_date','incident_time',
        'incident_location','unit_section','sse_id','sse_name','sse_designation','fire_explosion','employee_involve_id',
        'employee_involve_name','employee_involve_designation','otherinvolve','incident_description',
        'details_of_damages_to_infrastructure','site_sketch','section_bay','plant_machine_tools',
        'condition_of_work_environment','others','details_of_analysis_of_incident','responsibility','prevention_and_corrective_action',
        'comments_of_au_incharge','au_incharge_id','au_incharge_name','au_incharge_designation').distinct()) 
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success:False"},status=400)   