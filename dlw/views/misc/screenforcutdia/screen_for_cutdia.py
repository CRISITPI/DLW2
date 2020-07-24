from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/screenforcutdiagramupdation/')
def screenforcutdiagramupdation(request):
     
     
    context={
        'nav' : g.nav,
        'ip' : get_client_ip(request),
        'subnav' : g.subnav,
        'usermaster':g.usermaster
    }
    return render(request,'MISC/SCREENFORCUTDIA/screenforcutdiagramupdation.html',context)


def ScreenCutGetAllDetails(request):
    if request.method == "GET" and request.is_ajax():
        cno=request.GET.get('cutno')
        temp=list(Part.objects.filter(partno=cno).values('partno').distinct())
        if(len(temp)==0):
            return JsonResponse(temp,safe=False)
        else:

            obj=list(Cutdia.objects.filter(cutdia_no=cno,del_fl__isnull=True).values('ep_part','epc','l_fr','l_to','rm_part','rm_desc','thick_rm','rm_width',
            'rm_len','rm_spec','wt_rm','rm_unit','batch_size','rm_unit').distinct())
            obj1=list(Part.objects.filter(partno=cno).values('des','ptc').distinct())
            i=[]
            v=''
            v1=''
            if len(obj)!=0:
                v=obj[0]['epc']
                v1=obj[0]['rm_part']
            obj2=[]
            obj3=[]
            
            if v != "":
                obj2=list(Code.objects.filter(code=v,cd_type='11').values('alpha_1').distinct())
               
            if v1 != "":
                obj3=list(Part.objects.filter(partno=v1).values('ptc').distinct())
                   
            i.append(obj)
            i.append(obj1)
            i.append(obj2)
            i.append(obj3)
            return JsonResponse(i,safe=False)
    return JsonResponse({"success:False"},status=400)

def ScreenCutDiaValidateEpc(request):
    if request.method == "GET" and request.is_ajax():
        epc=request.GET.get('epc')
        
        obj=list(Code.objects.filter(code=epc,cd_type='11').values('alpha_1','code').distinct())
        if len(obj)==0:
            i=[]
            return JsonResponse(i,safe=False)
        else:    
            return JsonResponse(obj,safe=False)
    return JsonResponse({"success:False"},status=400)

def ScreenCutDiaValidateEpPartNo(request):
    if request.method == "GET" and request.is_ajax():
        eppartno = request.GET.get('eppartno')
        obj=list(Part.objects.filter(partno=eppartno).values('partno').distinct())
        if len(obj)==0:
            i=[]
            return JsonResponse(i,safe=False)
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success:False"},status=400)

def ScreenCutDiaValidateRmPartNo(request):
    if request.method == "GET" and request.is_ajax():
        rmpartno = request.GET.get('rmpartno')
        obj=list(Part.objects.filter(partno=rmpartno).values('ptc','partno').distinct())
        if len(obj)==0:
            i=[]
            return JsonResponse(i,safe=False)
        else:   
            return JsonResponse(obj,safe=False)
    return JsonResponse({"success:False"},status=400)  

def ScreenCutDiaSave(request):
    if request.method == "GET" and request.is_ajax():
        obj=[]
        cutdiano=request.GET.get('cutdiano') 
        epc=request.GET.get('epc')  
        eppartno=request.GET.get('eppartno')
        rmpartno=request.GET.get('rmpartno')
        rmdesc=request.GET.get('rmdesc')
        rmunit=request.GET.get('rmunit')
        rmthick=request.GET.get('rmthick') 
        rmwidth=request.GET.get('rmwidth')
        rmlength=request.GET.get('rmlength')
        rmspec=request.GET.get('rmspec')
        rmweight=request.GET.get('rmweight')
        batchsize=request.GET.get('batchsize')  
        locofr=request.GET.get('locofr')
        locoto=request.GET.get('locoto')
        d1 = date.today()

        temp=Cutdia.objects.values('cutdia_no','del_fl').filter(cutdia_no=cutdiano).distinct()
        if len(temp) == 0:
            temp=Cutdia.objects.create(cutdia_no=str(cutdiano),ep_part=str(eppartno),epc=str(epc),l_fr=str(locofr),
            l_to=str(locoto),rm_part=str(rmpartno),rm_desc=str(rmdesc),thick_rm=rmthick,rm_width=rmwidth,rm_len=rmlength,
            rm_spec=str(rmspec),wt_rm = rmweight,rm_unit=str(rmunit),batch_size=str(batchsize),updt_dt=d1)
        elif temp[0]['del_fl']== 'Y' and len(temp) != 0:
            Cutdia.objects.filter(cutdia_no=cutdiano).update(cutdia_no=str(cutdiano),ep_part=str(eppartno),epc=str(epc),l_fr=str(locofr),
            l_to=str(locoto),rm_part=str(rmpartno),rm_desc=str(rmdesc),thick_rm=rmthick,rm_width=rmwidth,rm_len=rmlength,
            rm_spec=str(rmspec),wt_rm = rmweight,rm_unit=str(rmunit),batch_size=str(batchsize),updt_dt=d1,del_fl=None)
        
        else:
            obj=[1]
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success:False"},status=400) 

def ScreenCutDiaUpdateYes(request):
    if request.method == "GET" and request.is_ajax():
        obj=[]
        cutdiano=request.GET.get('cutdiano') 
        epc=request.GET.get('epc')  
        eppartno=request.GET.get('eppartno')
        rmpartno=request.GET.get('rmpartno')
        rmdesc=request.GET.get('rmdesc')
        rmunit=request.GET.get('rmunit')
        rmthick=request.GET.get('rmthick') 
        rmwidth=request.GET.get('rmwidth')
        rmlength=request.GET.get('rmlength')
        rmspec=request.GET.get('rmspec')
        rmweight=request.GET.get('rmweight')
        batchsize=request.GET.get('batchsize')  
        locofr=request.GET.get('locofr')
        locoto=request.GET.get('locoto')
        d1 = date.today()
        Cutdia.objects.filter(cutdia_no=cutdiano).update(cutdia_no=str(cutdiano),ep_part=str(eppartno),epc=str(epc),l_fr=str(locofr),
            l_to=str(locoto),rm_part=str(rmpartno),rm_desc=str(rmdesc),thick_rm=rmthick,rm_width=rmwidth,rm_len=rmlength,
            rm_spec=str(rmspec),wt_rm = rmweight,rm_unit=str(rmunit),batch_size=str(batchsize),updt_dt=d1)

        return JsonResponse(obj,safe=False)
    return JsonResponse({"success:False"},status=400) 

def ScreenCutDiaDeleteYes(request):
    if request.method == "GET" and request.is_ajax():
        obj=[]
        cutdiano=request.GET.get('cutdiano') 
        d1 = date.today()
        Cutdia.objects.filter(cutdia_no=cutdiano).update(del_fl='Y',updt_dt=d1)

        return JsonResponse(obj,safe=False)
    return JsonResponse({"success:False"},status=400) 