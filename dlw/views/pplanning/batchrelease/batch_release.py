from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/batchrelease/')
def batchrelease(request):
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'usermaster':g.usermaster,
    }
    if request.method == "POST":       
            Submit = request.POST.get('releasebatch')
            dataForm = request.POST.get('dataForm')
            if Submit=="Release Batch":
                asslyno = request.POST.get('asslyno')
                batchno = request.POST.get('batchno')
                date = request.POST.get('date')
                brn = request.POST.get('brn')
                epc = request.POST.get('epc')
                qty = request.POST.get('qty')
                locofr = request.POST.get('locofr')
                locoto = request.POST.get('locoto')
                date=date[6:10]+'-'+date[3:5]+'-'+date[0:2]
                date=datetime.datetime.strptime(date, "%Y-%m-%d")
                try:
                    Batch.objects.filter(bo_no=batchno,part_no=asslyno,ep_type=epc,loco_fr=locofr,loco_to=locoto,batch_qty=qty,brn_no=brn).update(rel_date=date,status='R')
                    messages.success(request, 'Batch Released!!!')
                except:
                    messages.error(request, ' Some Error Occured!!!')
    return render(request,'PPRODUCTION/BATCHRELEASE/batchrelease.html',context)
def Batchreleasestatus(request):
    if request.method=="GET" and request.is_ajax():
        batch=request.GET.get('batch')
        lst=list(M2Docnew1.objects.filter(batch_no=batch).values('batch_no'))
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success:False"},status=400)
def batchreleasegetbatch(request):
    if request.method=="GET" and request.is_ajax():
        lst=list(dpoloco.objects.values('batchordno').order_by('batchordno').distinct())
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success:False"},status=400)
def Batchreleasedetails(request):
    if request.method=="GET" and request.is_ajax():
        batch=request.GET.get('batch')
        if batch is not None:
            lst=list(Batch.objects.filter(bo_no=batch).values('id','part_no','brn_no','loco_fr','loco_to','batch_qty','ep_type','bo_no'))  
        else:
            lst=list(Batch.objects.values('id','part_no','brn_no','loco_fr','loco_to','batch_qty','ep_type','bo_no'))  
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success:False"},status=400)