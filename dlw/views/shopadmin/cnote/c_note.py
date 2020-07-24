from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/cnote/')
def cnote(request): 
    obj = list(Cnote.objects.values('chg_ind').distinct()) 
    context={
        'sub':0,
        'lenm' :len(rolelist),
        'nav':g.nav,
        'obj':obj,
        'ip':get_client_ip(request),
        'usermaster' : g.usermaster,
        'subnav':g.subnav,
    }

    return render(request,'SHOPADMIN/CNOTE/cnote.html',context)

def cnote_get_details(request):
    if request.method == "GET" and request.is_ajax():
        cno = request.GET.get('cn')
        cind = request.GET.get('chng_ind')
        obj = list(Cnote.objects.filter(chg_ind = cind, ppl_cn_no = cno).values('reg_no','reg_dt','ref_1','ref_1_dt','cn_reg_dt','cn_dt','status','file_no','page_no','lett_no','assly_no', 'assly_desc').distinct())
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)

def cnote_getcn(request):
    if request.method == "GET" and request.is_ajax():
        cind = request.GET.get('cnind')
        obj = list(Cnote.objects.filter(chg_ind = cind,status='Y').values('ppl_cn_no').distinct().order_by('ppl_cn_no'))
         
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)

def assly_validation(request):
    if request.method == "GET" and request.is_ajax():
        asno = request.GET.get('an')
        obj = list(Part.objects.filter(partno = asno).values('partno','des').distinct())
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status = 400)


def allot_update(request):
    import datetime
    if request.method == "GET" and request.is_ajax():
        cn_no = request.GET.get('cn_no')
        chng_ind = request.GET.get('chng_ind')
        num = list(Code.objects.filter(cd_type = '21', code = 'MRG').values('num_1').order_by('cd_type','code').distinct())
        num = num[0]['num_1'] +1
        
        edp_reg_no = request.GET.get('edp_reg_no')
        edp_reg_dt = request.GET.get('edp_reg_dt')
        if(edp_reg_dt=='' or edp_reg_dt=='undefined' or edp_reg_dt==None):
            edp_reg_dt=datetime.datetime.now()
        else:
            edp_reg_dt= datetime.datetime.strptime(edp_reg_dt,'%d-%m-%Y').date()
        page_no = request.GET.get('page_no')
        file_no = request.GET.get('file_no')
        
        up_dt = request.GET.get('up_dt')
        up_dt =datetime.datetime.strptime(up_dt,'%d-%m-%Y').date()
        sts = request.GET.get('sts')
        
        if(edp_reg_no=='' or edp_reg_no==None ):
            Code.objects.filter(cd_type = '21' , code = 'MRG').update(num_1 = num, lupd_date = up_dt)
            edp_reg_no=num
            if(chng_ind =='STM' or chng_ind == 'STE'):
                Cpart.objects.filter(ppl_cn_no = cn_no, reg_no = None).update(reg_no = edp_reg_no)
                Cstr.objects.filter(pp_part = None , cp_part = None).delete()
                Cstr.objects.filter(chg_ind = chng_ind, cn_no = cn_no, reg_no = None).update(reg_no = edp_reg_no)
            elif(chng_ind == 'OPN'):
                Copn.objects.filter(part_no = None).delete()
                Copn.objects.filter(cn_no = cn_no, reg_no = None).update(reg_no = edp_reg_no)
        Cnote.objects.filter(chg_ind = chng_ind, ppl_cn_no = cn_no).update(reg_no = edp_reg_no, reg_dt = edp_reg_dt, file_no = file_no, page_no= page_no, updt_dt = up_dt, status = sts)
        return JsonResponse(num, safe = False)
    return JsonResponse({"success":False}, status = 400)
