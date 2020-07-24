from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/m9view/')
def m9view(request):
    from dlw.models import m9
    wo_nop = empmast.objects.none()
    tmp=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'usermaster':g.usermaster,
    }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            part_no = request.POST.get('part_nop')
            op_no=request.POST.get('op_no')
            dt=date.today
            context = {
                'date':dt,
                'shop_sec': shop_sec,
                'wo_no': wo_no,
                'part_no': part_no,
                'op_no':op_no,
                'sub' : 1,
                'nav':g.nav,
                'user':g.usermaster,
                'ip':get_client_ip(request),  
                'subnav':g.subnav,
            } 
    
    return render(request,"MCARD/M9CARD/m9view.html",context)


def m9getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        
        part_no = list(Oprn.objects.filter(shop_sec = shop_sec,part_no__isnull=False).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)




def m9getopno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        part_no = request.GET.get('part_nop')
        op_no = list(Oprn.objects.filter(shop_sec = shop_sec,part_no=part_no).values('opn').distinct())
        return JsonResponse(op_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m9getwono(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = list(Batch.objects.filter(bo_no__isnull=False).values('bo_no').distinct())
        
        return JsonResponse(wo_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m9getmw(request):
    if request.method == "GET" and request.is_ajax():
        mwno = request.GET.get('mw')
        mw_no=list(MG9Initial.objects.filter(id=mwno).values('mw_no').distinct())
        return JsonResponse(mw_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m9getsbc(request):
    if request.method == "GET" and request.is_ajax():
        sbc = request.GET.get('sbc')
        sbc_no=list(M5DOCnew.objects.filter(m5glsn=sbc).values('m5glsn').distinct())
        if len(sbc_no)!=0:
            return JsonResponse(sbc_no, safe = False)
        else:
            i=[]
            return JsonResponse(i, safe = False)
    return JsonResponse({"success":False}, status=400)

def m9getrjc(request):
    if request.method == "GET" and request.is_ajax():
        rjc = request.GET.get('rjc')
        rjc_no=list(M5DOCnew.objects.filter(m5glsn=rjc).values('m5glsn').distinct())
        if len(rjc_no)!=0:
            return JsonResponse(rjc_no, safe = False)
        else:
            i=[]
            return JsonResponse(i, safe = False)
    return JsonResponse({"success":False}, status=400)

def m9getshop_name(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        shop_name = list(shop_section.objects.filter(section_code=shop_sec).values('section_desc').distinct())
        return JsonResponse(shop_name , safe = False)
    return JsonResponse({"success":False}, status=400)

    
def save_sm9(request):
    context={}
    if request.method == "GET" and request.is_ajax():
            date=request.GET.get('val1')
            idle_time_man_mac=request.GET.get('val2')
            wo_no=request.GET.get('val')
            part_no=request.GET.get('val3')
            sus_jbno=request.GET.get('val4')
            res_jno=request.GET.get('val5')
            mw_no=request.GET.get('val6')
            mg9_no=request.GET.get('val7')
            aff_opn=request.GET.get('val8')
            empno=request.GET.get('val9')
            empname=request.GET.get('val10')
            prev_empno=request.GET.get('val11')
            cat=request.GET.get('val12')
            remark=request.GET.get('val13')
            shop=request.GET.get('val15')
            on_off=request.GET.get('val14')

            m9obj=m9.objects.create()
            m9obj.empname=empname
            m9obj.sus_jbno=sus_jbno
            m9obj.res_jno=res_jno
            m9obj.cat=cat
            m9obj.mw_no=mw_no
            m9obj.mg9_no=mg9_no
            m9obj.empno=empno
            m9obj.prev_empno=prev_empno
            m9obj.remark=remark
            m9obj.idle_time_man_mac=idle_time_man_mac
            m9obj.date=date
            m9obj.shop_sec=shop
            m9obj.part_no=part_no
            m9obj.wo_no=wo_no
            m9obj.aff_opn=aff_opn
            m9obj.on_off=on_off
            m9obj.save()
            return JsonResponse(context,safe=False)
    return JsonResponse({"success":False}, status=400)
def get_value(request):
    if request.method == "GET" and request.is_ajax():
        date=request.GET.get('val1')
        idle_time_man_mac=request.GET.get('val2')
        wo_no=request.GET.get('val')
        part_no=request.GET.get('val3')
        sus_jbno=request.GET.get('val4')
        res_jno=request.GET.get('val5')
        mw_no=request.GET.get('val6')
        mg9_no=request.GET.get('val7')
        aff_opn=request.GET.get('val8')
        empno=request.GET.get('val9')
        empname=request.GET.get('val10')
        prev_empno=request.GET.get('val11')
        cat=request.GET.get('val12')
        remark=request.GET.get('val13')
        shop=request.GET.get('val15')
        lst=[]
        lst=list(m9.objects.filter(shop_sec=shop,wo_no=wo_no,part_no=part_no,aff_opn=aff_opn).values('date','idle_time_man_mac','wo_no','part_no','sus_jbno','res_jno','mw_no','mg9_no','aff_opn','empno','empname','prev_empno','cat','remark',).distinct())
        a={'date':date,'idle_time_man_mac':idle_time_man_mac,'wo_no':wo_no,'part_no':part_no,'sus_jbno':sus_jbno,'res_jno':res_jno,'mw_no':mw_no,'mg9_no':mg9_no,'aff_opn':aff_opn,'empno':empno,'empname':empname,'prev_empno':prev_empno,'cat':cat,'remark':remark}
        for key,value in a.items():
            if key in lst:
                lst.append(a)
        return JsonResponse(lst, safe = False)
    return JsonResponse({"success":False}, status=400)

