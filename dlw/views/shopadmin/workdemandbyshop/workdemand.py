from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/workdemandbyshop/')
def workdemandbyshop(request):
    cuser=request.user
    desg=empmast.objects.filter(empno=cuser).values('desig_longdesc')[0]
    ch='ne'
    match = re.search(r'SENIOR SECTION ENGINEER', desg['desig_longdesc'])
    if match:
         ch='sse'
    match = re.search(r'WORKSHOP  MANAGER', desg['desig_longdesc'])
    if match:
         ch='wmm'
    match = re.search(r'PROGRESS MAN', desg['desig_longdesc'])
    if match:
         ch='prm'
    
    lst=''
    if ch=='sse':
        lst=list(workdemandbyshopmain.objects.filter(Q(flag=0)).all().order_by('flag','recordno'))
    if ch=='wmm':
        lst=list(workdemandbyshopmain.objects.filter(flag=1).all().order_by('flag','recordno'))
    if ch=='prm':
        lst=list(workdemandbyshopmain.objects.filter(flag=3).all().order_by('flag','recordno'))
    context = {
        'main':'s',
        'ip':get_client_ip(request),
        'nav':g.nav,
        'subnav':g.subnav,
        'desg':ch,
        'lst':lst,
    }
    if request.method == "POST":
           submitvalue = request.POST.get('Add Demand')
           submitvalue1 = request.POST.get('Search2')
           submitvalue2 = request.POST.get('Details')
           submitvalue3 = request.POST.get('View')
           locono=request.POST.get('locono')
           workorder=request.POST.get('workorder')
           date=request.POST.get('date')
           detailsdocno=request.POST.get('detailsdocno')
           code=request.POST.get('code')
           if(code=='m4' or code=='M4'):
               code=88
           else:
               code=89
           if submitvalue=='Add Demand':
               cdate=str(datetime.datetime.now().strftime ("%d-%m-%Y"))
               check=cdate[3:5]+cdate[6:10]
               date=str(date)
               docno=workdemandbyshopmain.objects.values('recordno').order_by('-recordno')
               print(check,docno)
               if docno.count()>0:
                   if(docno[0]['recordno']=='999999'):
                        docno= '100001'
                   else:
                        docno=str(int(docno[0]['recordno'])+1)
               else:
                    docno= '100001'
               workdemandbyshopmain.objects.create(recordno=docno,workorder =workorder,locono=locono,flag='0',status='Inbox',remarks='Not Yet Forwarded',sseid=str(cuser),dreleasedate=date,date=cdate,doccode=code) 
               context = {
                        'ip':get_client_ip(request),
                        'nav':nav,
                        'subnav':subnav,
                        'desg':ch,
                        'demandno':docno,
                        'locono':locono,
                        'workorder':workorder,
                        'date':date,
                        'code':code,
                        'flag':'0',
                        'd':'A',
                        
                }
               return render(request,'SHOPADMIN/WORKDEMANDBYSHOP/workdemandbyshopadd.html',context)
           if submitvalue3=='View':
                lst=list(workdemandbyshopmain.objects.filter(~Q(flag=4)).all().order_by('flag','recordno'))
                context = {
                    'main':'n',
                    'ip':get_client_ip(request),
                    'nav':nav,
                    'subnav':subnav,
                    'desg':ch,
                    'lst':lst,
                }
                return render(request,'SHOPADMIN/WORKDEMANDBYSHOP/workdemandbyshop.html',context)

           if submitvalue1=='Search2':
                detailsdocno=request.POST.get('searchdoc')
                doc=list(workdemandbyshopmain.objects.filter(recordno=detailsdocno).values('recordno','workorder','locono','dreleasedate','status','doccode','flag'))
                lst=list(workdemandbyshopsecondary.objects.filter(recordno=detailsdocno).values('id','partno','desc','unit','quantity','locofrom','locoto','shopno').order_by('id'))
                j=1
                for i in range(len(lst)):
                    lst[i].update({'sl':j})
                    j+=1
                context = {
                        'ip':get_client_ip(request),
                        'nav':nav,
                        'subnav':subnav,
                        'desg':ch,
                        'demandno':doc[0]['recordno'],
                        'locono':doc[0]['locono'],
                        'workorder':doc[0]['workorder'],
                        'date':doc[0]['dreleasedate'],
                        'status':doc[0]['status'],
                        'code':doc[0]['doccode'],
                        'lst':lst,
                        'flag':doc[0]['flag'],
                        'd':'B',
                }
                return render(request,'SHOPADMIN/WORKDEMANDBYSHOP/workdemandbyshopadd.html',context)
           if submitvalue2=='Details':
                doc=list(workdemandbyshopmain.objects.filter(recordno=detailsdocno).values('recordno','workorder','locono','dreleasedate','status','doccode','flag'))
                lst=list(workdemandbyshopsecondary.objects.filter(recordno=detailsdocno).values('id','partno','desc','unit','quantity','locofrom','locoto','shopno').order_by('id'))
                j=1
                for i in range(len(lst)):
                    lst[i].update({'sl':j})
                    j+=1
                context = {
                        'ip':get_client_ip(request),
                        'nav':nav,
                        'subnav':subnav,
                        'desg':ch,
                        'demandno':doc[0]['recordno'],
                        'locono':doc[0]['locono'],
                        'workorder':doc[0]['workorder'],
                        'date':doc[0]['dreleasedate'],
                        'status':doc[0]['status'],
                        'code':doc[0]['doccode'],
                        'flag':doc[0]['flag'],
                        'lst':lst,
                        'd':'B',
                }
                return render(request,'SHOPADMIN/WORKDEMANDBYSHOP/workdemandbyshopadd.html',context)
    return render(request,'SHOPADMIN/WORKDEMANDBYSHOP/workdemandbyshop.html',context)
def workdemandbyshoppdf(request, *args, **kwargs):
    docno = request.GET.get('docno')
    main=list(workdemandbyshopmain.objects.filter(recordno=docno).values('recordno','workorder','locono','dreleasedate','doccode','sseid','wmmid','pmid','date','wmmdate','prmdate'))
    sec=list(workdemandbyshopsecondary.objects.filter(recordno=docno).values('id','partno','desc','unit','quantity','locofrom','locoto','shopno').order_by('id'))
    for i in range(len(sec)):
        sec[i].update({'sl':i+1})
    data={
        'main':main,
        'sec':sec,
    }
    pdf = render_to_pdf('SHOPADMIN/WORKDEMANDBYSHOP/workdemandbyshoppdf.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def getcode(request):
    if request.method == "GET" and request.is_ajax():
        unit=list(Code.objects.filter(cd_type='51').values('alpha_1').distinct())       
        return JsonResponse(unit, safe = False)
    return JsonResponse({"success":False}, status=400)

def getworkorderno(request):
    if request.method == "GET" and request.is_ajax():
        bono=list(Batch.objects.values('bo_no').distinct())       
        return JsonResponse(bono, safe = False)
    return JsonResponse({"success":False}, status=400)

def addworkorderdetails(request):
    if request.method=="GET" and request.is_ajax():
        partno=request.GET.get('partno')
        desc=request.GET.get('desc')
        quantity=request.GET.get('quantity')
        unit=request.GET.get('unit')
        locofrom=request.GET.get('locofrom')
        locoto=request.GET.get('locoto')
        docno=request.GET.get('docno')
        shopsec=request.GET.get('shopsec')
        a=request.GET.get('a')
        if a=='0':
            workdemandbyshopsecondary.objects.create(recordno=docno,partno=partno,quantity=quantity,desc=desc,unit=unit,locofrom=locofrom,locoto=locoto,shopno=shopsec)
        else:
            workdemandbyshopsecondary.objects.filter(id=a).update(recordno=docno,partno=partno,quantity=quantity,desc=desc,unit=unit,locofrom=locofrom,locoto=locoto,shopno=shopsec)
        return JsonResponse(partno, safe = False)
    return JsonResponse({"success":False}, status=400)

def getworkdemandpart(request):
    if request.method=='GET' and request.is_ajax():
        docno=request.GET.get('docno')
        lst=list(workdemandbyshopsecondary.objects.filter(recordno=docno).values('id','partno','desc','unit','quantity','locofrom','locoto','shopno').order_by('id'))
        j=1
        for i in range(len(lst)):
            lst[i].update({'sl':j})
            j+=1
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success":False},status=400)
def getpartno(request):
    if request.method=='GET' and request.is_ajax():
        lst=[]
        part=list(Part.objects.filter(partno__isnull=False).values('partno').distinct())
        shop=list(Shop.objects.filter(shop__isnull=False).values('shop').distinct())
        lst.append(list(part))
        lst.append(list(shop))
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success":False},status=400)

def changestatus(request):
    cuser=request.user
    if request.method=='GET' and request.is_ajax():
        docno=request.GET.get('docno')
        status=request.GET.get('flag')
        cdate=str(datetime.datetime.now().strftime ("%d-%m-%Y"))
        if status == '0':
            workdemandbyshopmain.objects.filter(recordno=docno).update(flag='1',status='Progress',remarks='Forwarded To WMM')
        if status == '1':
            workdemandbyshopmain.objects.filter(recordno=docno).update(flag='3',status='Progress',remarks='Forwarded To PRM',wmmid=str(cuser),wmmdate=cdate)
        
        if status == '2':
            workdemandbyshopmain.objects.filter(recordno=docno).update(flag='0',status='Progress',remarks='Returned By Wmm',wmmid=str(cuser),wmmdate=cdate)
        
        if status == '3':
            workdemandbyshopmain.objects.filter(recordno=docno).update(flag='4',status='Completed',remarks='Work Order Generated',pmid=str(cuser),prmdate=cdate)
        a=[]
        return JsonResponse(a,safe=False)
    return JsonResponse({"success":False},status=400)


def getdocumentno(request):
    if request.method=='GET' and request.is_ajax():
        lst=list(workdemandbyshopmain.objects.values('recordno'))
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success":False},status=400)