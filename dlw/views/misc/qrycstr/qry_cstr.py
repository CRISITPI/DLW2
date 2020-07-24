from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/qrycstr/')
def qrycstr(request):
    
    wo_nop = empmast.objects.none()
 
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
    if(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = M13.objects.all().filter(shop=g.rolelist[i]).values('wo').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'subnav':g.subnav,
        }
        
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            'roles' :tmp,
            'subnav':g.subnav,
        }
    return render(request,'MISC/PRODUCTSTRCNGQRY/qrycstr.html',context)


def qrycstr1(request):
    if request.method == "GET" and request.is_ajax():   
        part_no=request.GET.get('val')
        c=list(Part.objects.filter(partno=part_no).values('des'))
        return JsonResponse(c, safe = False)
    return JsonResponse({"success":False}, status=400)

def qrycstr_ddCn_fun(request):
    if request.method == "GET" and request.is_ajax():   
        ddCn=request.GET.get('val1')
        
        ds=list(Cnote.objects.filter(chg_ind=ddCn).values('reg_no','reg_dt','ppl_cn_no','assly_no','ref_1_dt','updt_dt').annotate(mysubstring1=Substr('assly_desc',1,14),mysubstring2=Substr('ref_1',1,14)).order_by('ppl_cn_no').distinct())
        return JsonResponse(ds, safe = False)
    return JsonResponse({"success":False}, status=400)



def qrycstr_viewstatus(request):
    ddCN= request.GET.get('ddCN')
    rbtnquery= request.GET.get('rbtnquery')
    formateDate= request.GET.get('formateDate')
    
    if(rbtnquery=='3'):
        tbox = datetime.datetime.strptime(formateDate, "%d-%m-%Y")
    else:
        tbox = formateDate
   
    if(rbtnquery=="1"):
        tmpstr=Cstr.objects.values('reg_no','slno','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','cutdia_no','cn_no','cn_date','acd','updt_dt','errmsg').filter(status='U',chg_ind=ddCN,cp_part=tbox).distinct().order_by('chg_ind','cp_part','reg_no')
    elif(rbtnquery=="2"):
        tmpstr=Cstr.objects.values('reg_no','slno','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','cutdia_no','cn_no','cn_date','acd','updt_dt','errmsg').filter(status='U',chg_ind=ddCN,cn_no=tbox).distinct().order_by('chg_ind','cp_part','reg_no')
    elif(rbtnquery=="3"):
        tmpstr=Cstr.objects.values('reg_no','slno','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','cutdia_no','cn_no','cn_date','acd','updt_dt','errmsg').filter(status='U',chg_ind=ddCN,updt_dt=tbox).distinct().order_by('chg_ind','cp_part','reg_no')

    cp_part=[]
    cn_no=[]
    for x in tmpstr:
        cp_part.append(x['cp_part'])
        cn_no.append(x['cn_no'])
    
    tmpstr1=Part.objects.filter(partno__in=cp_part).count()
    

    if tmpstr1 > 0:
        tmp=Part.objects.filter(partno__in=cp_part).values('des').distinct()
    else:
        tmp=[{'des':'null'}]
    
    desc=[]
    for y in tmp:
        desc.append(y['des'])

    

    tmpstr2=Cnote.objects.filter(chg_ind=ddCN,ppl_cn_no__in=cn_no).count()
    
    if tmpstr2 > 0:
        tmp1=Cnote.objects.filter(chg_ind=ddCN,ppl_cn_no__in=cn_no).values('ref_1').distinct()
    else:
        tmp1=[{'ref_1':'null'}]

    design=[]
    for z in tmp1:
        design.append(z['ref_1'])
    
    for j in range(len(tmpstr)):
        tmpstr[j].update({'des':desc[0]})
        if len(tmp1)==len(tmpstr):
            tmpstr[j].update({'design':design[j]})
        else:
            tmpstr[j].update({'design':design[0]})

    today = date.today()
    context={
        'today':today,
        'tmpstr':tmpstr,
    }
    pdf=render_to_pdf('MISC/PRODUCTSTRCNGQRY/qrycstrreport.html',context)
    return HttpResponse(pdf,content_type='application/pdf')
