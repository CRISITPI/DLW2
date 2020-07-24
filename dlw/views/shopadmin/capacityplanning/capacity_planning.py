from dlw.views import *
import dlw.views.globals as g
def CapacityPlanLoadBookGetPartDes(request):
    if request.method == "GET" and request.is_ajax():
        obj=[]
        partno=request.GET.get('partno')
        obj=list(Part.objects.filter(partno=partno).values('des').distinct())
        return JsonResponse(obj,safe=False) 
    return JsonResponse({"success:False"},status=400) 

def CapacityPlanLoadBookGetEpc(request):
    if request.method == "GET" and request.is_ajax():
        partno=request.GET.get('partno')
        epc=request.GET.get('epc')
        obj=list(Nstr.objects.filter(cp_part=partno,epc=epc,l_to = '9999').values('epc').distinct())
        if len(obj) == 0:
            return JsonResponse(obj,safe=False)
        obj1=list(Code.objects.filter(cd_type='11',code=epc).values('num_1').distinct())
        return JsonResponse(obj1,safe=False) 
    return JsonResponse({"success:False"},status=400) 

def CapacityPlanLoadBookGetQty(request):
    if request.method == "GET" and request.is_ajax():
        obj=[]
        partno=request.GET.get('partno')
        epc=request.GET.get('epc')
        eppartno=request.GET.get('eppartno')
        p = cpq(partno,epc,eppartno)
        return JsonResponse(p,safe=False) 
    return JsonResponse({"success:False"},status=400) 


@login_required
@role_required(urlpass='/capacityplanningandloadbook/')
def capacityplanningandloadbook(request):     
    context={
        'nav' : g.nav,
        'ip' : get_client_ip(request),
        'subnav' : g.subnav,
        'usermaste':g.usermaster,
    }
    return render(request, "SHOPADMIN/CAPACITYPLANNING/capacityplanningandloadbook.html",context) 
def CapacityPlanLoadBookexplode(request, *args, **kwargs):
    
    yes=request.GET.get('r1')
    no=request.GET.get('r2')
    lfr=request.GET.get('lfr')
    pn=request.GET.get('partno')
    epc=request.GET.get('epc')
    epc=epc.upper()
    qtyloco=request.GET.get('qtyloco')
    partdes =request.GET.get('partdes')
    today = date.today()
    fdate = date.today().strftime('%d/%m/%Y')
    if yes == "true":
        if lfr != "":
            locofrom=lfr
        else:
            locofrom=0000
        locoto=9999
        if sumexpl(pn,epc,locofrom,locoto,qtyloco):
            delLOADBK()
            insertLOADBK()
            UpdateLOADBK()
            dss1=list(Loadbk.objects.filter(cur_time=g_curTime).values("part_no","ptdes","qty", "sh_sec","lc_no","m5_cd","lc_des","pa",
            "at_hrs", "loco_load_hrs", "no_mc", "cap_mnth_hrs","prod_cap_mnth").order_by("sh_sec","lc_no","part_no"))
            
            lst1=[]
            i=0
            total=0
            l=0
            while(i<len(dss1)):
                sum=dss1[i]['loco_load_hrs']
                k=0
                for j in range(i+1,len(dss1)):
                    if dss1[i]['sh_sec']==dss1[j]['sh_sec'] and dss1[i]['lc_no']==dss1[j]['lc_no']:
                        sum = sum + dss1[j]['loco_load_hrs']
                        k=k+1
                        l+=1
                l+=1
                lst1.append({'shopsec':dss1[i]['sh_sec'],'lcno': dss1[i]['lc_no'],'sum':sum,'k':k,'l':l})
                i=i+k+1
                total=total + sum
            
            v=0
            for i in range(len(dss1)):
                dss1[i].update({'sl':i+1})
            

        data={
            'obj':dss1,
            'pn' : pn,
            'epc' :epc,
            'date' :fdate,
            'partdes':partdes,
            'a':"Y",
            'total':total,
            'lst1':lst1
            }
        pdf = render_to_pdf('SHOPADMIN/CAPACITYPLANNING/CapacityPLanLoadBookreport.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
        
    else:
        cursor = connection.cursor()
        cursor.execute('''select "OPRN"."PART_NO",(select "DES" from public."PART" where "OPRN"."PART_NO"= "PART"."PARTNO") ptdes,%s qty, "OPRN"."SHOP_SEC", "LC_NO","M5_CD", mp1.lc_des lc_desc, 
                (case when (coalesce(trim("OPRN"."M5_CD"),'9')='1') then (sum("OPRN"."PA_HRS")/5) else sum("OPRN"."PA_HRS") end) pa,
                sum("OPRN"."AT_HRS" / "OPRN"."LOT") at1, 
                round(((case when (coalesce(trim("M5_CD"),'9')='1') then (sum("PA_HRS")/5) else sum( "PA_HRS") end)+ (%s::int) * sum("AT_HRS"/"LOT")),2) loco_load, 
                sum(mp1.no_mc), sum(mp1.no_mc)*480 cap_month,
                round(mp1.no_mc*480/round(((case when (coalesce(trim("OPRN"."M5_CD"),'9')='1') then (sum("OPRN"."PA_HRS")/5)
                else sum("OPRN"."PA_HRS") end) + (1::int)*sum("OPRN"."AT_HRS"/"OPRN"."LOT")),2),2) prod_cap_month
                from (select "SHOP_SEC", "LCNO",(select "DES" from public."LC1" where "LC1"."SHOP_SEC"= "MP"."SHOP_SEC" and "LC1"."LCNO"= "MP"."LCNO" 
                and coalesce(trim("LC1"."DEL_FL"),'#')!='Y' limit 1) lc_des,count(1) no_mc from public."MP" group by "SHOP_SEC", "LCNO", "DES") 
                mp1  full OUTER JOIN public."OPRN" on
				mp1."SHOP_SEC"="OPRN"."SHOP_SEC" and mp1."LCNO"="OPRN"."LC_NO" WHERE 
                trim("PART_NO")=%s and coalesce(trim("NCP_JBS"),'#')<>'1'     
                group by "OPRN"."PART_NO",1,"OPRN"."SHOP_SEC", "LC_NO","M5_CD", mp1.no_mc, mp1.lc_des
                order by "OPRN"."SHOP_SEC", "OPRN"."LC_NO";''',[qtyloco,qtyloco,pn])
        row = cursor.fetchall()
        dts = list(row)
        lst=[]
        for i in range(len(dts)):
                lst.append({"sl":i+1,"part_no":dts[i][0],"ptdes":dts[i][1],"qty":dts[i][2], "sh_sec":dts[i][3],"lc_no":dts[i][4],"m5_cd":dts[i][5],"lc_des":dts[i][6],"pa":dts[i][7],
                "at_hrs":dts[i][8], "loco_load_hrs":dts[i][9], "no_mc":dts[i][10], "cap_mnth_hrs":dts[i][11],"prod_cap_mnth":dts[i][12]})
        

        lst1=[]
        i=0
        total=0
        l=0
        while(i<len(lst)):
            sum=lst[i]['loco_load_hrs']
            k=0
            for j in range(i+1,len(lst)):
                if lst[i]['sh_sec']==lst[j]['sh_sec'] and lst[i]['lc_no']==lst[j]['lc_no']:
                    sum = sum + lst[j]['loco_load_hrs']
                    k=k+1
                    l+=1
            l+=1
            lst1.append({'shopsec':lst[i]['sh_sec'],'lcno': lst[i]['lc_no'],'sum':sum,'k':k,'l':l})
            i=i+k+1
            total=total + sum
        

        v=0
        for i in range(len(lst)):
            v= v+lst[0]['loco_load_hrs']
        
        data={
            'pagesize':'A4',
            'obj':lst,
            'pn' : pn,
            'epc' :epc,
            'date' :fdate,
            'partdes':partdes,
            'a':"N",
            'total':total,
            'lst1':lst1
            }
        pdf = render_to_pdf('SHOPADMIN/CAPACITYPLANNING/CapacityPLanLoadBookreport.html', data)
        return HttpResponse(pdf, content_type='application/pdf')