from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/qtysum/')

def qtysum(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first() 
    tm=shop_section.objects.filter(shop_id=usermaster.shopno).all()
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
        'usermaster':g.usermaster
    }
    Ptld.objects.all().delete()   
    return render(request,"SHOPADMIN/QTYSUM/qtysum.html",context)
def report1(request): 
    data_list4=list(Ptld.objects.values('part_no','ptc','p_desc','qty','epc','rem','drgno'))
    df=pandas.DataFrame(data_list4)
    pn=[]
    pd=[]
    qt=[]
    ep=[]
    rm=[]
    drg=[]
    dt_length=len(data_list4)    
    for i in range(len(data_list4)):
        pn.append(data_list4[i].get('part_no'))
        pd.append(data_list4[i].get('p_desc'))
        qt1=str(data_list4[i].get('qty'))
        qt.append(qt1)
        ep.append(data_list4[i].get('epc')) 
        rm.append(data_list4[i].get('rem'))
        drg.append(data_list4[i].get('drgno'))
    data=process()
    a=data['DESC']
    partno=list(a.keys())
    desc=data["DESC"].values.tolist()
    qty=data["QTY"].values.tolist()
    ptc=data["PTC"].values.tolist()
    context={
     'val1':pn,
     'val2':pd,
     'val3':qt,
     'val4':ep,
     'val5':rm,
     'val6':drg,
     'count':dt_length,
     'l1':len(pn),
     'l2':len(pd),
     'l3':len(qt),
     'l4':len(ep),
     'l6':len(rm),
     'd':partno,
     'd1':desc,
     'd2':qty,
     'd3':ptc,
     'count1':len(desc),
    }
    return render(request,'SHOPADMIN/QTYSUM/report1.html',context)


    
def qtysum1(request):
    if request.method == 'GET' and request.is_ajax():  
        part= request.GET.get('asslyno')
        data_list=list(Part.objects.filter(partno=part).values('des').distinct())       
        if(len(data_list)>0):
            return JsonResponse(data_list,safe = False)                                  
    return JsonResponse({"success":False},status=400)           

def qtysum2(request):
    if request.method == 'GET' and request.is_ajax():  
        part = request.GET.get('asslyno')
        part1 = request.GET.get('Txtpartno')
        val = request.GET.get('qty')
        drg_no=list(Part.objects.filter(partno=part).values('drgno').distinct())
        drg=drg_no[0].get('drgno')

        Ptld.objects.create(part_no=part, p_desc=part1,qty=val  ,epc='',ptc='',rem='',drgno=drg)
        data_list2=list(Ptld.objects.values('part_no','p_desc','qty','epc','ptc','rem').distinct())
        return JsonResponse(data_list2,safe = False)                                               
    return JsonResponse({"success":False},status=400)
