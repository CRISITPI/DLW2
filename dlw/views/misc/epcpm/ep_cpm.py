from dlw.views import *
import dlw.views.globals as g


@login_required
@role_required(urlpass='/EpCpm/')
def EpCpm(request):
    
    wo_nop = empmast.objects.none()

    my_date=Cpm.objects.all().values('updt_dt').distinct()
    my=[]
    for i in my_date:
        my.append(i['updt_dt'])
    my.sort(reverse= True)
    my1=my[0]
    my=str(my[0])
    mydate=my[8:10]+'-'+my[5:7]+'-'+my[0:4]
     
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
        'lblDt': mydate,
        'lblDt1': my1,
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
            'lblDt': mydate,
            'lblDt1': my1,

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
            'lblDt': mydate,
            'lblDt1': my1,

        } 

    return render(request,'MISC/EPCPM/EpCpm.html',context)
      

def unbound(request):
    if request.method == "GET" and request.is_ajax():
        Unbound = Code.objects.filter(cd_type='11').values('code').distinct()
        un=[]
        for j in Unbound:
            un.append(j['code'])
        un.sort()
        data =  {
            'un': un
        }
        return JsonResponse(un, safe=False)
    return JsonResponse({"success": False}, status=400)



def btnViewCPM_Click(request):
    import datetime
    lblDt= request.GET.get('lblDt')
    dtEpc= request.GET.get('dtEpc')
    dtPtc= request.GET.get('dtPtc')
    EpcAll= request.GET.get('EpcAll')
    PtcAll= request.GET.get('PtcAll')
  
    p=Cpm.objects.values_list('part_no')
    
    monthTemp=lblDt.split(' ')[0]
    dateTemp=lblDt.split(' ')[1]
    final1=monthTemp[0:3]+' '+dateTemp.split(',')[0]+' '+lblDt.split(' ')[2]
    date_time_str=final1
    date_time_obj=datetime.datetime.strptime(date_time_str,'%b %d %Y')
    date_1=date_time_obj.date()
    
    len1=len(dtEpc)
    len2=len(dtPtc)

    
    e=[]
    for k in range(0,len1):
        if(dtEpc[k]==" " or dtEpc[k]==","):
            pass
        else:
            e.append(dtEpc[k])

    pt=[]
    for k in range(0,len2):
        if(dtPtc[k]==","):
            pass
        else:
            pt.append(dtPtc[k])
            

    
    elen=len(e)
    plen=len(pt)
    p=[]

    for m in range(0,elen,2):
        epc=str(e[m])+str(e[m+1])

        for j in range(0,plen):

            if(EpcAll=='B' and PtcAll=='B'):
                c=Cpm.objects.filter(epc=epc,ptc=pt[j],qty__gt=0).values('epc','shop_ut','part_no','ptc','qty').order_by('part_no').distinct()
                p.extend(c)
            
            else:
                c=Cpm.objects.filter(epc=epc,ptc=pt[j]).values('epc','shop_ut','part_no','ptc','qty').order_by('part_no').distinct()
                p.extend(c)

    
    seen = set()
    new_l = []
    for d in p:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    

    ptdes=[]
    epc = [] 
    ptc = [] 
    shop_ut = [] 
    part_no=[]
    part=[]
    qty=[]
    
    for x in p:
        epc.append(x['epc'])
        unit=Code.objects.filter(cd_type='51',code=x['shop_ut']).values('alpha_1')
        if len(unit)>0:
            unit=unit[0]['alpha_1']
        else:
            unit=''

        shop_ut.append(unit)
        if x['part_no'] not in part:
            part.append(x['part_no'])
        ptc.append(x['ptc'])
        qty.append(x['qty'])
    for x in part:    
        ptdes.append({'part_no':x})
    
        

    for i in range(0,len(ptdes)):
        a =list(Part.objects.filter(partno=ptdes[i]['part_no']).values('des'))
        ptdes[i].update({'sl':(i+1)})
        ptdes[i].update({'ptc':ptc[i]})   
        ptdes[i].update({'des':a[0]['des']})
        ptdes[i].update({'epc':epc[i]})
        ptdes[i].update({'part_no':ptdes[i]['part_no']})
        ptdes[i].update({'shop_ut':shop_ut[i]})
        ptdes[i].update({'qty':"{0:.2f}".format(float(qty[i]))})

    if EpcAll=='B':
        EpcAll=dtEpc
    if PtcAll=='B':
        PtcAll=dtPtc

    today=datetime.datetime.today().strftime('%d/%m/%Y')
 
    context={
        'today':today,
        'ptdes':ptdes,  
        'EpcAll':EpcAll,
        'PtcAll':PtcAll,
    }

    pdf=render_to_pdf('MISC/EPCPM/epcpmreport.html',context)
    return HttpResponse(pdf,content_type='application/pdf')

def btnClear_Click(request):
    return render(request,'MISC/EPCPM/EpCpm.html')