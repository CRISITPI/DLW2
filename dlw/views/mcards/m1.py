from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/m1view/')
def m1view(request):
    pa_no = empmast.objects.none()
    
    part11=''
    
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = Oprn.objects.all().filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            pa_no =pa_no | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'pa_no':pa_no,
            'roles' :g.rolelist,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
            
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'ip':get_client_ip(request),
            'roles' :g.rolelist,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'usermaster':g.usermaster,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        shop_sec = request.POST.get('shop_sec')
        part_no = request.POST.get('part_nop')
        part11=part_no
        obj  = Oprn.objects.filter(part_no=part_no).values('opn', 'shop_sec', 'lc_no', 'des','pa','at','ncp_jbs',).order_by('opn','shop_sec')
        leng = obj.count()
        epcv=0
        ptcv=0
        rmpart=0
        obj3=Nstr.objects.filter(pp_part=part_no).values('epc','ptc','cp_part').distinct()
        if len(obj3):
            epcv=obj3[0]['epc']
            ptcv=obj3[0]['ptc']
            rmpart=obj3[0]['cp_part']
        if submitvalue=='Proceed':
            if "Superuser" in g.rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub': 1,
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'len': leng,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'obj': obj,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                    'part':part11,
                    'usermaster':g.usermaster,
                }
            elif(len(g.rolelist)==1):
                lent=len(g.rolelist)
                for i in range(0,len(g.rolelist)):
                    req = Oprn.objects.all().filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                    pa_no =pa_no | req
                context = {
                    'sub': 1,
                    'lenm' :len(g.rolelist),
                    'pa_no':pa_no,
                    'roles' :g.rolelist,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'len': leng,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'obj': obj,'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                    'part':part11,
                    'usermaster':g.usermaster,
                }
            elif(len(g.rolelist)>1):
                context = {
                   'sub': 1,
                    'lenm' :len(g.rolelist),
                    'ip':get_client_ip(request),
                    'roles' :g.rolelist,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'len': leng,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'obj': obj,'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                    'part':part11,
                    'usermaster':g.usermaster,
                }
        
        if submitvalue=='Generate Report':
            part11=request.POST.get('h1')
            context = {
                    'lenm' :'',
                  
                    'roles' :'',
                    'nav':'',
                    'subnav':'',
                    'ip':'',
                    'sub': '',
                    'part_no': '',
                    'obj1':'',
                    'dtl':'',
                    'obj3':'',
                    'pttl':'',
                    'attl':'',
                    'dt':'d1',
                    'epcv':'',
                    'ptcv':'',
                    'rmpart':'',
                    'part':part11,
                }
            
            return render(request,"MCARD/M1CARD/M1report.html",context)
    return render(request,"MCARD/M1CARD/m1view.html",context)


def m1getpano(request):
    if request.method == "GET" and request.is_ajax():
        pano = list(Oprn.objects.filter(part_no__isnull=False).values('part_no').distinct())
        return JsonResponse(pano, safe = False)
    return JsonResponse({"success":False}, status=400)
    
def m1getshopsec(request):
    if request.method == "GET" and request.is_ajax():
        pano = list(shop_section.objects.values('section_code').distinct())
        return JsonResponse(pano, safe = False)
    return JsonResponse({"success":False}, status=400)

def m1genrept1(request):
    from dlw.models import Part,Partalt,Nstr
    pa_no = empmast.objects.none()
    
    newob=list(Part.objects.all().values('partno').exclude(partno__isnull=True).distinct())
    if "Superuser" in g.rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'newob':newob,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)==1):
        for i in range(0,len(g.rolelist)):
            req = Oprn.objects.all().filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
            pa_no =pa_no | req
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'pa_no':pa_no,
            'roles' :g.rolelist,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'newob':newob,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'ip':get_client_ip(request),
            'roles' :g.rolelist,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'newob':newob,
            'usermaster':g.usermaster,
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        part_no = part_no
        if submitvalue=='Proceed':
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            epcv=0
            ptcv=0
            rmpart=0
            obj=Part.objects.filter(partno=part_no).values('des','drgno','drg_alt','size_m','spec','weight','des').distinct()
            obj3=Nstr.objects.filter(pp_part=part_no).values('epc','ptc','cp_part').distinct()
            if len(obj3):
                epcv=obj3[0]['epc']
                ptcv=obj3[0]['ptc']
                rmpart=obj3[0]['cp_part']
                obj11=Part.objects.filter(partno=rmpart).values('des').distinct()
                if len(obj11):
                    rdes=obj11[0]['des']
            obj2 = Oprn.objects.filter(part_no=part_no).values('opn','shop_sec','lc_no','des','pa','at','ncp_jbs','lot','m5_cd','updt_dt').order_by('opn')
            patotal=0
            attotal=0
            if len(obj2):
                for op in obj2:
                    patotal=patotal+op['pa']
                    attotal=attotal+op['at']
            lst=str(patotal).split('.',1)
            h=int(lst[0])*100
            patotal=int(lst[1])+h
            m=str(patotal % 60).zfill(2)
            patotal=(str(int(patotal/60))+":"+m)
            lst=str(attotal).split('.',1)
            h=int(lst[0])*100
            attotal=int(lst[1])+h
            m=str(attotal % 60).zfill(2)
            attotal=(str(int(attotal/60))+":"+m)          
            if "Superuser" in g.rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'subnav':g.subnav,
                    'part_no': part_no,
                    'obj1':obj,
                    'dtl':obj2,
                    'obj3':obj3,
                    'pttl':patotal,
                    'attl':attotal,
                    'dt':d1,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                    'rdes':rdes,
                    'prtno':part_no,
                    'usermaster':g.usermaster,
                }
            elif(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    req = Oprn.objects.all().filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                    pa_no =pa_no | req
                context = {
                    'lenm' :len(g.rolelist),
                    'pa_no':pa_no,
                    'roles' :g.rolelist,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'part_no': part_no,
                    'obj1':obj,
                    'dtl':obj2,
                    'obj3':obj3,
                    'pttl':patotal,
                    'attl':attotal,
                    'dt':d1,'sub': 1,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                    'rdes':rdes,
                    'prtno':part_no,
                    'usermaster':g.usermaster,
                }
            elif(len(g.rolelist)>1):
                context = {
                    'lenm' :len(g.rolelist),
                    'ip':get_client_ip(request),
                    'roles' :g.rolelist,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'sub': 1,
                    'part_no': part_no,
                    'obj1':obj,
                    'dtl':obj2,
                    'obj3':obj3,
                    'pttl':patotal,
                    'attl':attotal,
                    'dt':d1,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                    'rdes':rdes,
                    'prtno':part_no,
                    'usermaster':g.usermaster,
                }
        part_no = request.POST.get('hide1')
        printpdf = request.POST.get('print')
        if printpdf=='Print':
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            epcv=0
            ptcv=0
            rmpart=0
            obj=Part.objects.filter(partno=part_no).values('des','drgno','drg_alt','size_m','spec','weight','des').distinct()
            obj3=Nstr.objects.filter(pp_part=part_no).values('epc','ptc','cp_part').distinct()
            rdes=''
            if len(obj3):
                epcv=obj3[0]['epc']
                ptcv=obj3[0]['ptc']
                rmpart=obj3[0]['cp_part']
                obj11=Part.objects.filter(partno=rmpart).values('des').distinct()
                if len(obj11):
                    rdes=obj11[0]['des']
            obj2 = Oprn.objects.filter(part_no=part_no).values('opn','shop_sec','lc_no','des','pa','at','ncp_jbs','lot','m5_cd','updt_dt').order_by('opn')
            patotal=0
            attotal=0
            if len(obj2):
                for op in obj2:
                    patotal=patotal+op['pa']
                    attotal=attotal+op['at']
            lst=str(patotal).split('.',1)
            h=int(lst[0])*100
            patotal=int(lst[1])+h
            m=str(patotal % 60).zfill(2)
            patotal=(str(int(patotal/60))+":"+m)
            lst=str(attotal).split('.',1)
            h=int(lst[0])*100
            attotal=int(lst[1])+h
            m=str(attotal % 60).zfill(2)
            attotal=(str(int(attotal/60))+":"+m)          
            if "Superuser" in g.rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':g.nav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'subnav':g.subnav,
                    'part_no': part_no,
                    'obj1':obj,
                    'dtl':obj2,
                    'obj3':obj3,
                    'pttl':patotal,
                    'attl':attotal,
                    'dt':d1,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                    'rdes':rdes,
                    'prtno':part_no,
                    'usermaster':g.usermaster,
                }
            elif(len(g.rolelist)==1):
                for i in range(0,len(g.rolelist)):
                    req = Oprn.objects.all().filter(shop_sec=g.rolelist[i]).values('part_no').distinct()
                    pa_no =pa_no | req
                context = {
                    'lenm' :len(g.rolelist),
                    'pa_no':pa_no,
                    'roles' :g.rolelist,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'part_no': part_no,
                    'obj1':obj,
                    'dtl':obj2,
                    'obj3':obj3,
                    'pttl':patotal,
                    'attl':attotal,
                    'dt':d1,'sub': 1,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                    'rdes':rdes,
                    'prtno':part_no,
                    'usermaster':g.usermaster,
                }
            elif(len(g.rolelist)>1):
                context = {
                    'lenm' :len(g.rolelist),
                    'ip':get_client_ip(request),
                    'roles' :g.rolelist,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'sub': 1,
                    'part_no': part_no,
                    'obj1':obj,
                    'dtl':obj2,
                    'obj3':obj3,
                    'pttl':patotal,
                    'attl':attotal,
                    'dt':d1,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                    'rdes':rdes,
                    'prtno':part_no,
                    'usermaster':g.usermaster,
                }
            
            pdf = render_to_pdf('MCARD/M1CARD/m1pdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        bckbtn=request.POST.get('backbutton')
        if bckbtn=='Back':
            return render(request,"MCARD/M1CARD/m1view.html",{})
    return render(request,"MCARD/M1CARD/M1report.html",context)
