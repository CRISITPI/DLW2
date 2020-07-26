
from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/wheelmachining_section/')
def wheelmachining_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    dd3=[]
    obj2=list(WheelMachining.objects.all().filter(Q(dispatch_status=False)).values('sno','bo_no','pt_no','bo_qty','bo_date','loco_type','date','wheel_no','wheelp_no','wheel_make','wheel_heatcaseno','in_qty','out_qty','dispatch_to','datewhl').order_by('sno'))
    obj3=list(WheelMachining.objects.all().filter(Q(dispatch_status=False)).values('datewhl','in_qty','out_qty').order_by('sno'))
    ll=len(obj3)
    for i in range(0,ll):
        dd=obj3[i]['datewhl']
        indate=obj3[i]['in_qty']
        outdate=obj3[i]['out_qty']
        if dd!=None :
            s = dd.split('-')
            month1 = s[1]
            day1 = s[2]
            year1 = s[0]
            dd2 =  day1 + "-" + month1 + "-" + year1
            obj2[i].update({'datewhl':dd2})
        else :
            obj2[i].update({'datewhl':None})
        if indate!=None :
            s1 = indate.split('-')
            newmonth1 = s1[1]
            newday1 = s1[2]
            newyear1 = s1[0]
            newindate =  newday1 + "-" + newmonth1 + "-" + newyear1
            obj2[i].update({'in_qty':newindate})
        else :
            obj2[i].update({'in_qty':None}) 

        if outdate!=None :
            s2 = outdate.split('-')
            newmonth2 = s2[1]
            newday2 = s2[2]
            newyear2 = s2[0]
            newoutdate =  newday2 + "-" + newmonth2 + "-" + newyear2
            obj2[i].update({'out_qty':newoutdate})
        else :
            obj2[i].update({'out_qty':None})
    mybo=Batch.objects.all().values('bo_no')
    mysno=(WheelMachining.objects.filter(dispatch_status=False).values('wheel_no')).order_by('wheel_no')
    mysno0=(WheelMachining.objects.filter(dispatch_status=False).filter(wheelinspection_status=True).values('wheel_no')).order_by('wheel_no')
    mysno1=(WheelMachining.objects.filter(dispatch_status=False).filter(wheelinspection_status=False).values('wheel_no')).order_by('wheel_no')
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mysno':mysno,
       'mysno0':mysno0,
       'mysno1':mysno1,
       }
    if request.method=="POST":
        once=request.POST.get('once')
        print(once)
        submit=request.POST.get('submit')
        if submit=='Save':
        
            first=request.POST.get('bo_no')
            second=request.POST.get('bo_date')
            third=request.POST.get('date')
            fourth=request.POST.get('wheel_no')
            fifth=request.POST.get('wheel_make')
            sixth=request.POST.get('loco_type')
            seventh=request.POST.get('wheel_heatcaseno')
            eighth=request.POST.get('wheelp_no')
            eleven=request.POST.get('pt_no')
            twelve=request.POST.get('bo_qty')
            indate=request.POST.get('in_qty')
            outdate=request.POST.get('out_qty')
            s1 = indate.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            newindate =  year1 + "-" + month1 + "-" + day1
            s2 = outdate.split('-')
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            newoutdate =  year2 + "-" + month2 + "-" + day2
            if first and second and third and fourth and fifth and sixth and seventh and eighth and eleven and twelve and indate and outdate :
                obj=WheelMachining.objects.create()
                obj.bo_no=first
                obj.bo_date=second
                obj.date=third
                obj.wheel_no=fourth
                obj.wheel_make=fifth
                obj.loco_type=sixth
                obj.wheel_heatcaseno=seventh
                obj.wheelp_no=eighth
                obj.wheelinspection_status=False
                obj.pt_no=eleven
                obj.bo_qty=twelve
                obj.in_qty=newindate
                obj.out_qty=newoutdate
                obj.save()
                messages.success(request, 'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=WheelMachining.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='save':

            sno=request.POST.get('editsno')
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            bo_qty=request.POST.get('editbo_qty')
            pt_no=request.POST.get('editpt_no')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            wheelp_no=request.POST.get('editwheelp_no')
            wheel_no=request.POST.get('editwheel_no')
            wheel_make=request.POST.get('editwheel_make')
            wheel_heatcaseno=request.POST.get('editwheel_heatcaseno')
            indate=request.POST.get('editin_qty')
            outdate=request.POST.get('editout_qty')
            s1 = indate.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            newindate =  year1 + "-" + month1 + "-" + day1
            s2 = outdate.split('-')
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            newoutdate =  year2 + "-" + month2 + "-" + day2
            if bo_no and bo_date and date and loco_type and wheel_make and wheel_no and wheel_heatcaseno and wheelp_no and pt_no and bo_qty and indate and outdate:
                WheelMachining.objects.filter(wheel_no=sno).update(bo_no=bo_no,bo_date=bo_date,pt_no=pt_no,bo_qty=bo_qty,in_qty=newindate,out_qty=newoutdate,date=date,wheel_no=wheel_no,wheel_make=wheel_make,loco_type=loco_type,wheel_heatcaseno=wheel_heatcaseno,wheelp_no=wheelp_no)
                messages.success(request, 'Successfully Edited!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            sno=request.POST.get('delsno')
            if sno:
                w=list(WheelMachining.objects.filter(wheel_no=sno).values('wheel_no'))
                l=len(w)
                if l>0 :
                    WheelMachining.objects.filter(wheel_no=sno).delete()
                    messages.success(request, 'Successfully Deleted!')
                else:
                    messages.error(request,"Please Enter Valid Wheel Number!")
            else:
                messages.error(request,"Please Enter S.No.!")

        if submit=='InspectWheel':
    
            sno=request.POST.get('snowheel')
            oustwhl=request.POST.get('ustwhl')
            oustwhl_date=request.POST.get('ustwhl_date')
            oustwhl_status=request.POST.get('ustwhl_status')
            ohub_lengthwhl=request.POST.get('hub_lengthwhl')
            otread_diawhl=request.POST.get('tread_diawhl')
            orim_thicknesswhl=request.POST.get('rim_thicknesswhl')
            obore_diawhl=request.POST.get('bore_diawhl')
            oinspector_namewhl=request.POST.get('inspector_namewhl')
            odatewhl=request.POST.get('datewhl')
            s = odatewhl.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]
            newodatewhl =  year1 + "-" + month1 + "-" + day1
            if oustwhl_status and oustwhl_date and oustwhl and ohub_lengthwhl and otread_diawhl and orim_thicknesswhl and obore_diawhl and oinspector_namewhl and odatewhl:
                WheelMachining.objects.filter(wheel_no=sno).update(ustwhl_status=oustwhl_status,ustwhl_date=oustwhl_date,ustwhl=oustwhl,hub_lengthwhl=ohub_lengthwhl,tread_diawhl=otread_diawhl,rim_thicknesswhl=orim_thicknesswhl,bore_diawhl=obore_diawhl,inspector_namewhl=oinspector_namewhl,datewhl=newodatewhl,wheelinspection_status=True,dispatch_to="Inspected")
                messages.success(request, 'Wheel Successfully Inspected!')
            else:
                messages.error(request,"Please Select S.No.!")
   
        return HttpResponseRedirect("/wheelmachining_section/")

    return render(request,"TMS/wheelmachining_section.html",my_context)




@login_required
@role_required(urlpass='/axlemachining_section/')
def axlemachining_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    dd3=[]
    obj2=list(AxleMachining.objects.all().filter(Q(dispatch_status=False)).values('sno','bo_no','pt_no','axle_no','dateaxle','bo_qty','bo_date','loco_type','date','axle_no','axlep_no','axle_make','axle_heatcaseno','in_qty','out_qty','dispatch_to').order_by('sno'))
    obj3=list(AxleMachining.objects.all().filter(Q(dispatch_status=False)).values('dateaxle','in_qty','out_qty').order_by('sno'))
    ll=len(obj3)
    for i in range(0,ll):
        dd=obj3[i]['dateaxle']
        indate=obj3[i]['in_qty']
        outdate=obj3[i]['out_qty']
        if dd!=None :
            s = dd.split('-')
            month1 = s[1]
            day1 = s[2]
            year1 = s[0]
            dd2 =  day1 + "-" + month1 + "-" + year1
            obj2[i].update({'dateaxle':dd2})
        else :
            obj2[i].update({'dateaxle':None})
        if indate!=None :
            s1 = indate.split('-')
            newmonth1 = s1[1]
            newday1 = s1[2]
            newyear1 = s1[0]
            newindate =  newday1 + "-" + newmonth1 + "-" + newyear1
            obj2[i].update({'in_qty':newindate})
        else :
            obj2[i].update({'in_qty':None}) 

        if outdate!=None :
            s2 = outdate.split('-')
            newmonth2 = s2[1]
            newday2 = s2[2]
            newyear2 = s2[0]
            newoutdate =  newday2 + "-" + newmonth2 + "-" + newyear2
            obj2[i].update({'out_qty':newoutdate})
        else :
            obj2[i].update({'out_qty':None})     

    mybo=Batch.objects.all().values('bo_no')
    mysno=(AxleMachining.objects.filter(dispatch_status=False).values('axle_no')).order_by('axle_no')
    mysno0=(AxleMachining.objects.filter(dispatch_status=False).filter(axleinspection_status=True).values('axle_no')).order_by('axle_no')
    mysno1=(AxleMachining.objects.filter(dispatch_status=False).filter(axleinspection_status=False).values('axle_no')).order_by('axle_no')
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mysno':mysno,
       'mysno0':mysno0,
       'mysno1':mysno1,
       'obj3':obj3,
       }
    if request.method=="POST":
        once=request.POST.get('once')
        print(once)
        submit=request.POST.get('submit')
        if submit=='Save':
        
            first=request.POST.get('bo_no')
            second=request.POST.get('bo_date')
            third=request.POST.get('date')
            fourth=request.POST.get('axlep_no')
            sixth=request.POST.get('loco_type')
            eighth=request.POST.get('axle_no')
            ninth=request.POST.get('axle_make')
            tenth=request.POST.get('axle_heatcaseno')
            eleven=request.POST.get('pt_no')
            twelve=request.POST.get('bo_qty')
            indate=request.POST.get('in_qty')
            outdate=request.POST.get('out_qty')
            s1 = indate.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            newindate =  year1 + "-" + month1 + "-" + day1
            s2 = outdate.split('-')
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            newoutdate =  year2 + "-" + month2 + "-" + day2
            if first and second and third and fourth and sixth and eighth and ninth and tenth and eleven and twelve and indate and outdate:
                obj=AxleMachining.objects.create()
                obj.bo_no=first
                obj.bo_date=second
                obj.date=third
                obj.axlep_no=fourth
                obj.loco_type=sixth
                obj.axle_no=eighth
                obj.axle_make=ninth
                obj.axle_heatcaseno=tenth
                obj.axleinspection_status=False
                obj.pt_no=eleven
                obj.bo_qty=twelve
                obj.in_qty=newindate
                obj.out_qty=newoutdate
                obj.save()
                messages.success(request, 'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=AxleMachining.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='save':

            sno=request.POST.get('editsno')
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            bo_qty=request.POST.get('editbo_qty')
            pt_no=request.POST.get('editpt_no')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            axlep_no=request.POST.get('editaxlep_no')
            axle_no=request.POST.get('editaxle_no')
            axle_make=request.POST.get('editaxle_make')
            axle_heatcaseno=request.POST.get('editaxle_heatcaseno')
            indate=request.POST.get('editin_qty')
            outdate=request.POST.get('editout_qty')
            s1 = indate.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            newindate =  year1 + "-" + month1 + "-" + day1
            s2 = outdate.split('-')
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            newoutdate =  year2 + "-" + month2 + "-" + day2
            if bo_no and bo_date and date and loco_type and axlep_no and axle_no and axle_make and axle_heatcaseno and pt_no and bo_qty and indate and outdate:
                AxleMachining.objects.filter(axle_no=sno).update(bo_no=bo_no,bo_date=bo_date,pt_no=pt_no,bo_qty=bo_qty,in_qty=newindate,out_qty=newoutdate,date=date,axlep_no=axlep_no,loco_type=loco_type,axle_no=axle_no,axle_make=axle_make,axle_heatcaseno=axle_heatcaseno)
                messages.success(request, 'Successfully Edited!')
            else:
                messages.error(request,"Please Enter S.No.!")
                
        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            dispatchdate=request.POST.get('dispatch_date')
            if sno and dislocos:
                AxleMachining.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_status=True,dispatch_date=dispatchdate)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            sno=request.POST.get('delsno')
            
            if sno:
                w=list(AxleMachining.objects.filter(axle_no=sno).values('axle_no'))
                l=len(w)
                if l>0 :
                    AxleMachining.objects.filter(axle_no=sno).delete()
                    messages.success(request, 'Successfully Deleted!')
                else:
                    messages.error(request,"Please Enter Valid Axle Number!")
            else:
                messages.error(request,"Please Enter S.No.!")

        if submit=='InspectAxle':
            
            sno=request.POST.get('snoaxle')
            ustaxle=request.POST.get('ustaxle')
            ustaxle_date=request.POST.get('ustaxle_date')
            ustaxle_status=request.POST.get('ustaxle_status')
            axlelength=request.POST.get('axlelength')
            journalaxle=request.POST.get('journalaxle')
            throweraxle=request.POST.get('throweraxle')
            wheelseataxle=request.POST.get('wheelseataxle')
            gearseataxle=request.POST.get('gearseataxle')
            collaraxle=request.POST.get('collaraxle')
            journalaxlende=request.POST.get('journalaxlende')
            throweraxlende=request.POST.get('throweraxlende')
            wheelseataxlende=request.POST.get('wheelseataxlende')
            collaraxlende=request.POST.get('collaraxlende')
            dateaxle=request.POST.get('dateaxle')
            bearingaxle=request.POST.get('bearingaxle')
            abutmentaxle=request.POST.get('abutmentaxle')
            inspector_nameaxle=request.POST.get('inspector_nameaxle')
            journal_surfacefinishGE=request.POST.get('journal_surfacefinishGE')
            wheelseat_surfacefinishGE=request.POST.get('wheelseat_surfacefinishGE')
            gearseat_surfacefinishGE=request.POST.get('gearseat_surfacefinishGE')
            journal_surfacefinishFE=request.POST.get('journal_surfacefinishFE')
            wheelseat_surfacefinishFE=request.POST.get('wheelseat_surfacefinishFE')
            gearseat_surfacefinishFE=request.POST.get('gearseat_surfacefinishFE')
            s = dateaxle.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]
            newdateaxle =  year1 + "-" + month1 + "-" + day1
           
            if ustaxle_date and ustaxle_status and ustaxle and axlelength and journalaxle and throweraxle and wheelseataxle and gearseataxle and collaraxle and dateaxle and bearingaxle and abutmentaxle and inspector_nameaxle and journal_surfacefinishGE and wheelseat_surfacefinishGE and gearseat_surfacefinishGE and journal_surfacefinishFE and wheelseat_surfacefinishFE and gearseat_surfacefinishFE and journalaxlende and throweraxlende and wheelseataxlende and collaraxlende:
                AxleMachining.objects.filter(axle_no=sno).update(ustaxle_date=ustaxle_date,ustaxle_status=ustaxle_status,ustaxle=ustaxle,axlelength=axlelength,journalaxle=journalaxle,throweraxle=throweraxle,wheelseataxle=wheelseataxle,gearseataxle=gearseataxle,collaraxle=collaraxle,dateaxle=newdateaxle,bearingaxle=bearingaxle,abutmentaxle=abutmentaxle,inspector_nameaxle=inspector_nameaxle,journal_surfacefinishGE=journal_surfacefinishGE,wheelseat_surfacefinishGE=wheelseat_surfacefinishGE,gearseat_surfacefinishGE=gearseat_surfacefinishGE,journal_surfacefinishFE=journal_surfacefinishFE,wheelseat_surfacefinishFE=wheelseat_surfacefinishFE,gearseat_surfacefinishFE=gearseat_surfacefinishFE,journalaxlende=journalaxlende,throweraxlende=throweraxlende,wheelseataxlende=wheelseataxlende,collaraxlende=collaraxlende,axleinspection_status=True,dispatch_to="Inspected")
                messages.success(request, 'Axle Successfully Inspected!')
            else:
                messages.error(request,"Please Enter all records!")

        
        return HttpResponseRedirect("/axlemachining_section/")

    return render(request,"TMS/axlemachining_section.html",my_context)

def aw_getaxleno(request):
    obj=[]
    if request.method == "GET" and request.is_ajax():
        obj=list(AxleMachining.objects.filter(axlefitting_status=False,axleinspection_status=True).values('axle_no'))
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)

def aw_getwhenode(request):
    obj=[]
    if request.method == "GET" and request.is_ajax():
        obj=list(WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no'))
        return JsonResponse(obj, safe = False)
    return JsonResponse({"success":False}, status=400)

def aw_getwhenonde(request):
    myval=[]
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('wde')  
        myval = list(WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no').exclude(wheel_no=mybo))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success": False}, status=400)

@login_required
@role_required(urlpass='/axlewheelpressing_section/')
def axlewheelpressing_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    obj2=list(AxleWheelPressing.objects.all().filter(Q(dispatch_status=False)).values('sno','bo_no','pt_no','axle_no','inspect_date','bo_qty','bo_date','loco_type','date','wheelno_de','wheelno_nde','bullgear_no','in_qty','out_qty','bullgear_make','dispatch_to').order_by('sno'))
    obj3=list(AxleWheelPressing.objects.all().filter(Q(dispatch_status=False)).values('inspect_date','in_qty','out_qty').order_by('sno'))
    ll=len(obj3)
    for i in range(0,ll):
        dd=obj3[i]['inspect_date']
        indate=obj3[i]['in_qty']
        outdate=obj3[i]['out_qty']
        if dd!=None :
            s = dd.split('-')
            month1 = s[1]
            day1 = s[2]
            year1 = s[0]
            dd2 =  day1 + "-" + month1 + "-" + year1
            obj2[i].update({'inspect_date':dd2})
        else :
            obj2[i].update({'inspect_date':None})
        if indate!=None :
            s1 = indate.split('-')
            newmonth1 = s1[1]
            newday1 = s1[2]
            newyear1 = s1[0]
            newindate =  newday1 + "-" + newmonth1 + "-" + newyear1
            obj2[i].update({'in_qty':newindate})
        else :
            obj2[i].update({'in_qty':None}) 

        if outdate!=None :
            s2 = outdate.split('-')
            newmonth2 = s2[1]
            newday2 = s2[2]
            newyear2 = s2[0]
            newoutdate =  newday2 + "-" + newmonth2 + "-" + newyear2
            obj2[i].update({'out_qty':newoutdate})
        else :
            obj2[i].update({'out_qty':None})
    mybo=Batch.objects.all().values('bo_no')
    hhpmysno=(AxleWheelPressing.objects.all().filter((Q(pt_no='17010019')|Q(pt_no='17010706')|Q(pt_no='17010639')|Q(pt_no='17010330')|Q(pt_no='17010421')|Q(pt_no='16010085')|Q(pt_no='16010206')|Q(pt_no='16010255')|Q(pt_no='17010019')|Q(pt_no='17010391')),dispatch_status=False).values('axle_no')).order_by('axle_no')
    hhpmysno0=(AxleWheelPressing.objects.all().filter((Q(pt_no='17010019')|Q(pt_no='17010706')|Q(pt_no='17010639')|Q(pt_no='17010330')|Q(pt_no='17010421')|Q(pt_no='16010085')|Q(pt_no='16010206')|Q(pt_no='16010255')|Q(pt_no='17010019')|Q(pt_no='17010391')),dispatch_status=False).filter(hhpinspection_status=True).values('axle_no')).order_by('axle_no')
    hhpmysno1=(AxleWheelPressing.objects.all().filter((Q(pt_no='17010019')|Q(pt_no='17010706')|Q(pt_no='17010639')|Q(pt_no='17010330')|Q(pt_no='17010421')|Q(pt_no='16010085')|Q(pt_no='16010206')|Q(pt_no='16010255')|Q(pt_no='17010019')|Q(pt_no='17010391')),dispatch_status=False).filter(hhpinspection_status=False).values('axle_no')).order_by('axle_no')
    mysno=(AxleWheelPressing.objects.all().filter(dispatch_status=False).values('axle_no')).order_by('axle_no')
    mysno0=(AxleWheelPressing.objects.all().filter(dispatch_status=False).filter(inspectinspection_status=True).values('axle_no')).order_by('axle_no')
    mysno1=(AxleWheelPressing.objects.all().filter(dispatch_status=False).filter(inspectinspection_status=False).values('axle_no')).order_by('axle_no')
    axle=list(AxleMachining.objects.filter(axlefitting_status=False,axleinspection_status=True).values('axle_no'))
    wheelde=list(WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no'))
    wheelpressde=list(WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no'))
    wheelnde=list(WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no'))
    print(wheelnde)
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mywheel':wheelde,
       'mywheel1':wheelnde,
       'myaxle':axle,
       'mysno':mysno,
        'mysno0':mysno0,
        'mysno1':mysno1,
        'hhpmysno':hhpmysno,
        'hhpmysno0':hhpmysno0,
        'hhpmysno1':hhpmysno1
       }
    if request.method=="POST":
        
        once=request.POST.get('once')
        submit=request.POST.get('submit')
        if submit=='Save':

            bo_no=request.POST.get('bo_no')
            bo_date=request.POST.get('bo_date')
            pt_no=request.POST.get('pt_no')
            bo_qty=request.POST.get('bo_qty')
            indate=request.POST.get('in_qty')
            outdate=request.POST.get('out_qty')
            date=request.POST.get('date')
            loco_type=request.POST.get('locos')
            axle_no=request.POST.get('axle_no')
            wheelno_de=request.POST.get('wheelno_de')
            wheelno_nde=request.POST.get('wheelno_nde')
            bullgear_no=request.POST.get('bullgear_no')
            bullgear_make=request.POST.get('bullgear_make')
            chkinsp=request.POST.get('insp_supplier')
            s1 = indate.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            newindate =  year1 + "-" + month1 + "-" + day1
            s2 = outdate.split('-')
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            newoutdate =  year2 + "-" + month2 + "-" + day2
            if bo_no and bo_date and date and loco_type and axle_no and wheelno_de and wheelno_nde and bullgear_no and bullgear_make and pt_no and bo_qty and indate and outdate:
               obj=AxleWheelPressing.objects.create()
               obj.bo_no=bo_no
               obj.bo_date=bo_date
               obj.date=date
               obj.pt_no=pt_no
               obj.bo_qty=bo_qty
               obj.in_qty=newindate
               obj.out_qty=newoutdate
               obj.loco_type=loco_type
               obj.axle_no=axle_no
               obj.wheelno_de=wheelno_de
               obj.wheelno_nde=wheelno_nde
               obj.bullgear_no=bullgear_no
               obj.bullgear_make=bullgear_make
               obj.inspectinspection_status=False
               obj.hhpinspection_status=False
               if chkinsp:
                   dts=date[6:] + "-" + date[3:5] + "-" + date[:2]
                   obj.inspectinspection_status=True
                   obj.dispatch_to="Inspected"
                   obj.inspect_date=dts                
               obj.save()
               messages.success(request, 'Successfully Added!')
               AxleMachining.objects.filter(axle_no=axle_no).update(axlefitting_status=True,dispatch_status=True)
               WheelMachining.objects.filter(wheel_no=wheelno_de).update(wheelfitting_status=True,dispatch_status=True)
               WheelMachining.objects.filter(wheel_no=wheelno_nde).update(wheelfitting_status=True,dispatch_status=True)  
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=AxleWheelPressing.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='Edit':
            sno=request.POST.get('editsno')
            
            if sno is not None:
            
                bo_no=request.POST.get('editbo_no')
                bo_date=request.POST.get('editbo_date')
                bo_qty=request.POST.get('editbo_qty')
                indate=request.POST.get('editin_qty')
                outdate=request.POST.get('editout_qty')
                pt_no=request.POST.get('editpt_no')
                date=request.POST.get('editdate')
                loco_type=request.POST.get('editlocos')
                axle_no=request.POST.get('editaxle_no')
                wheelno_de=request.POST.get('editwheelno_de')
                wheelno_nde=request.POST.get('editwheelno_nde')
                bullgear_no=request.POST.get('editbullgear_no')
                bullgear_make=request.POST.get('editbullgear_make')
                in_qty=request.POST.get('editin_qty')
                out_qty=request.POST.get('editout_qty')
                s1 = in_qty.split('-')
                month1 = s1[1]
                day1 = s1[0]
                year1 = s1[2]
                newin_qty =  year1 + "-" + month1 + "-" + day1
                s2 = out_qty.split('-')
                month2 = s2[1]
                day2 = s2[0]
                year2 = s2[2]
                newout_qty =  year2 + "-" + month2 + "-" + day2
                if bo_no and bo_date and date and pt_no and bo_qty and indate and outdate and axle_no and wheelno_de and wheelno_nde and bullgear_no and bullgear_make and in_qty and out_qty:
                    AxleWheelPressing.objects.filter(axle_no=sno).update(bo_no=bo_no,bo_date=bo_date,edit_date=date,loco_type=loco_type,axle_no=axle_no,in_qty=newin_qty,out_qty=newout_qty,wheelno_de=wheelno_de,wheelno_nde=wheelno_nde,bullgear_no=bullgear_no,bullgear_make=bullgear_make,pt_no=pt_no,bo_qty=bo_qty)
                    AxleMachining.objects.filter(axle_no=axle_no).update(axlefitting_status=True,dispatch_status=True)
                    WheelMachining.objects.filter(wheel_no=wheelno_de).update(wheelfitting_status=True,dispatch_status=True)
                    WheelMachining.objects.filter(wheel_no=wheelno_nde).update(wheelfitting_status=True,dispatch_status=True)
                    messages.success(request, 'Successfully Edited!')
                else:
                    messages.error(request,"Please Enter S.No.!")

        if submit=='InspectHHP':
            sno=request.POST.get('sno')
            wheelno_de=request.POST.get('hhpwheelno_de')
            wheel_de_make=request.POST.get('hhpwheel_de_make')
            wheelno_nde=request.POST.get('hhpwheelno_nde')
            wheel_nde_make=request.POST.get('hhpwheel_nde_make')
            wheel_nde_pressure=request.POST.get('hhpwheel_nde_pressure')
            wheel_de_pressure=request.POST.get('hhpwheel_de_pressure')
            axle_no=request.POST.get('hhpaxle_no')
            axle_make=request.POST.get('hhpaxle_make')
            bullgear_no=request.POST.get('hhpbullgear_no')
            bullgear_make=request.POST.get('hhpbullgear_make')
            bullgear_pressure=request.POST.get('hhpbullgear_pressure')
            msu_unit_no=request.POST.get('hhpmsu_unit_no')
            msu_unit_make=request.POST.get('hhpmsu_unit_make')
            axle_box_node=request.POST.get('hhpaxle_box_node')
            axle_box_makede=request.POST.get('hhpaxle_box_makede')
            axle_box_clearancede=request.POST.get('hhpaxle_box_clearancede')
            axle_box_nonde=request.POST.get('hhpaxle_box_nonde')
            axle_box_makende=request.POST.get('hhpaxle_box_makende')
            axle_box_clearancende=request.POST.get('hhpaxle_box_clearancende')
            msu_bearing_de_make=request.POST.get('hhpmsu_bearing_de_make')
            msu_bearing_nde_make=request.POST.get('hhpmsu_bearing_nde_make')
            cru_bearing_no_de=request.POST.get('hhpcru_bearing_no_de')
            cru_bearing_make_de=request.POST.get('hhpcru_bearing_make_de')
            cru_bearing_pressure_de=request.POST.get('hhpcru_bearing_pressure_de')
            cru_bearing_no_nde=request.POST.get('hhpcru_bearing_no_nde')
            cru_bearing_make_nde=request.POST.get('hhpcru_bearing_make_nde')
            cru_bearing_pressure_nde=request.POST.get('hhpcru_bearing_pressure_nde')
            wheel_distance=request.POST.get('hhpwheel_distance')
            axialplay_de=request.POST.get('hhpaxialplay_de')
            axialplay_nde=request.POST.get('hhpaxialplay_nde')
            date=request.POST.get('hhpdate')
            inspector_name=request.POST.get('hhpinspector_name')
            journal_no_de=request.POST.get('hhpjournal_no_de')
            journal_make_de=request.POST.get('hhpjournal_make_de')
            journal_no_nde=request.POST.get('hhpjournal_no_nde')
            journal_make_nde=request.POST.get('hhpjournal_make_nde')
            s = date.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]
            newdate =  year1 + "-" + month1 + "-" + day1
            if wheel_distance and axialplay_de and axialplay_nde and wheel_de_pressure and cru_bearing_pressure_nde and cru_bearing_make_nde and wheelno_de and wheel_de_make and wheelno_nde and wheel_nde_make and wheel_nde_pressure and axle_no and axle_make and bullgear_no and bullgear_make and bullgear_pressure and msu_unit_no and msu_unit_make and axle_box_nonde and axle_box_makende and axle_box_clearancende and axle_box_node and axle_box_makede and axle_box_clearancede and msu_bearing_de_make and msu_bearing_nde_make and cru_bearing_no_de and cru_bearing_make_de and cru_bearing_pressure_de and date and inspector_name and cru_bearing_no_nde and journal_no_de and journal_make_de and journal_no_nde and journal_make_nde:
                
                AxleWheelPressing.objects.filter(axle_no=sno).update(wheel_distance=wheel_distance,axialplay_de=axialplay_de,axialplay_nde=axialplay_nde,wheel_de_pressure=wheel_de_pressure,wheelno_de=wheelno_de,wheel_de_make=wheel_de_make,wheel_nde_make=wheel_nde_make,wheelno_nde=wheelno_nde,wheel_nde_pressure=wheel_nde_pressure,axle_no=axle_no,axle_make=axle_make,bullgear_no=bullgear_no,bullgear_make=bullgear_make,bullgear_pressure=bullgear_pressure,msu_unit_no=msu_unit_no,msu_unit_make=msu_unit_make,axle_box_nonde=axle_box_nonde,axle_box_makende=axle_box_makende,axle_box_clearancende=axle_box_clearancende,axle_box_node=axle_box_node,axle_box_makede=axle_box_makede,axle_box_clearancede=axle_box_clearancede,msu_bearing_de_make=msu_bearing_de_make,msu_bearing_nde_make=msu_bearing_nde_make,cru_bearing_no_de=cru_bearing_no_de,cru_bearing_make_de=cru_bearing_make_de,cru_bearing_pressure_de=cru_bearing_pressure_de,inspect_date=newdate,inspector_name=inspector_name,cru_bearing_no_nde=cru_bearing_no_nde,cru_bearing_make_nde=cru_bearing_make_nde,cru_bearing_pressure_nde=cru_bearing_pressure_nde,hhpinspection_status=True,journal_no_de=journal_no_de,journal_make_de=journal_make_de,journal_no_nde=journal_no_nde,journal_make_nde=journal_make_nde,dispatch_to="HHP_Inspected")

                messages.success(request,'Successfully Inspected!')
            else:
                messages.error(request,"Please Enter the all the records!")    
        if submit=='Inspect':
            sno=request.POST.get('sno')
            wheelno_de=request.POST.get('inspectwheelno_de')
            wheel_de_make=request.POST.get('inspectwheel_de_make')
            wheelno_nde=request.POST.get('inspectwheelno_nde')
            wheel_nde_make=request.POST.get('inspectwheel_nde_make')
            wheel_nde_pressure=request.POST.get('inspectwheel_nde_pressure')
            wheel_de_pressure=request.POST.get('inspectwheel_de_pressure')
            axle_no=request.POST.get('inspectaxle_no')
            axle_make=request.POST.get('inspectaxle_make')
            bullgear_no=request.POST.get('inspectbullgear_no')
            bullgear_make=request.POST.get('inspectbullgear_make')
            bullgear_pressure=request.POST.get('inspectbullgear_pressure')
            msu_unit_no=request.POST.get('inspectmsu_unit_no')
            msu_unit_make=request.POST.get('inspectmsu_unit_make')
            axle_box_node=request.POST.get('inspectaxle_box_node')
            axle_box_makede=request.POST.get('inspectaxle_box_makede')
            axle_box_clearancede=request.POST.get('inspectaxle_box_clearancede')
            axle_box_nonde=request.POST.get('inspectaxle_box_nonde')
            axle_box_makende=request.POST.get('inspectaxle_box_makende')
            axle_box_clearancende=request.POST.get('inspectaxle_box_clearancende')
            msu_bearing_de_make=request.POST.get('inspectmsu_bearing_de_make')
            msu_bearing_nde_make=request.POST.get('inspectmsu_bearing_nde_make')
            cru_bearing_no_de=request.POST.get('inspectcru_bearing_no_de')
            cru_bearing_make_de=request.POST.get('inspectcru_bearing_make_de')
            cru_bearing_pressure_de=request.POST.get('inspectcru_bearing_pressure_de')
            cru_bearing_no_nde=request.POST.get('inspectcru_bearing_no_nde')
            cru_bearing_make_nde=request.POST.get('inspectcru_bearing_make_nde')
            cru_bearing_pressure_nde=request.POST.get('inspectcru_bearing_pressure_nde')
            date=request.POST.get('inspectdate')
            inspector_name=request.POST.get('inspectinspector_name')
            wheel_distance=request.POST.get('inspectwheel_distance')
            axialplay_de=request.POST.get('inspectaxialplay_de')
            axialplay_nde=request.POST.get('inspectaxialplay_nde')
            s = date.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]
            newdate =  year1 + "-" + month1 + "-" + day1
            if wheel_distance and axialplay_de and axialplay_nde and wheel_de_pressure and cru_bearing_pressure_nde and cru_bearing_make_nde and wheelno_de and wheel_de_make and wheelno_nde and wheel_nde_make and wheel_nde_pressure and axle_no and axle_make and bullgear_no and bullgear_make and bullgear_pressure and msu_unit_no and msu_unit_make and axle_box_nonde and axle_box_makende and axle_box_clearancende and axle_box_node and axle_box_makede and axle_box_clearancede and msu_bearing_de_make and msu_bearing_nde_make and cru_bearing_no_de and cru_bearing_make_de and cru_bearing_pressure_de and date and inspector_name and cru_bearing_no_nde:
                AxleWheelPressing.objects.filter(axle_no=sno).update(wheel_distance=wheel_distance,axialplay_de=axialplay_de,axialplay_nde=axialplay_nde,wheel_de_pressure=wheel_de_pressure,wheelno_de=wheelno_de,wheel_de_make=wheel_de_make,wheel_nde_make=wheel_nde_make,wheelno_nde=wheelno_nde,wheel_nde_pressure=wheel_nde_pressure,axle_no=axle_no,axle_make=axle_make,bullgear_no=bullgear_no,bullgear_make=bullgear_make,bullgear_pressure=bullgear_pressure,msu_unit_no=msu_unit_no,msu_unit_make=msu_unit_make,axle_box_nonde=axle_box_nonde,axle_box_makende=axle_box_makende,axle_box_clearancende=axle_box_clearancende,axle_box_node=axle_box_node,axle_box_makede=axle_box_makede,axle_box_clearancede=axle_box_clearancede,msu_bearing_de_make=msu_bearing_de_make,msu_bearing_nde_make=msu_bearing_nde_make,cru_bearing_no_de=cru_bearing_no_de,cru_bearing_make_de=cru_bearing_make_de,cru_bearing_pressure_de=cru_bearing_pressure_de,inspect_date=newdate,inspector_name=inspector_name,cru_bearing_no_nde=cru_bearing_no_nde,cru_bearing_make_nde=cru_bearing_make_nde,cru_bearing_pressure_nde=cru_bearing_pressure_nde,inspectinspection_status=True,dispatch_to="Inspected")
                messages.success(request,'Successfully Inspected!')
            else:
                messages.error(request,"Please Enter all the records!")

        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            disdate=request.POST.get('dispatch_date')
            if sno and dislocos and disdate:
                AxleWheelPressing.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_status=True,dispatch_date=disdate)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            sno=request.POST.get('delsno')
            if sno:
                AxleWheelPressing.objects.filter(axle_no=sno).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        return HttpResponseRedirect("/axlewheelpressing_section/")

    return render(request,"TMS/axlewheelpressing_section.html",my_context)

@login_required
@role_required(urlpass='/PinionPress/')
def pinionpressing_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    
    dd3=[]
    obj2=list(PinionPressing.objects.filter(Q(dispatch_status=False)).values('sno','bo_no','pt_no','bo_qty','bo_date','loco_type','date','in_qty','out_qty','tm_no','tm_make','axle_no','dispatch_to','inspect_date').order_by('sno'))
    obj3=list(PinionPressing.objects.filter(Q(dispatch_status=False)).values('inspect_date','in_qty','out_qty').order_by('sno'))
    ll=len(obj3)
    for i in range(0,ll):
        dd=obj3[i]['inspect_date']
        indate=obj3[i]['in_qty']
        outdate=obj3[i]['out_qty']
        if dd!=None :
            s = dd.split('-')
            month1 = s[1]
            day1 = s[2]
            year1 = s[0]
            dd2 =  day1 + "-" + month1 + "-" + year1
            obj2[i].update({'inspect_date':dd2})
        else :
            obj2[i].update({'inspect_date':None})
        if indate!=None :
            s1 = indate.split('-')
            newmonth1 = s1[1]
            newday1 = s1[2]
            newyear1 = s1[0]
            newindate =  newday1 + "-" + newmonth1 + "-" + newyear1
            obj2[i].update({'in_qty':newindate})
        else :
            obj2[i].update({'in_qty':None}) 

        if outdate!=None :
            s2 = outdate.split('-')
            newmonth2 = s2[1]
            newday2 = s2[2]
            newyear2 = s2[0]
            newoutdate =  newday2 + "-" + newmonth2 + "-" + newyear2
            obj2[i].update({'out_qty':newoutdate})
        else :
            obj2[i].update({'out_qty':None})
    
    mybo=(Batch.objects.all().values('bo_no')).order_by('bo_no')
    mysno=(PinionPressing.objects.filter(dispatch_status=False).values('axle_no')).order_by('axle_no')
    axleno=(AxleWheelPressing.objects.filter(inspectinspection_status=True).values('axle_no')).order_by('axle_no')
    mytm=(PinionPressing.objects.filter(dispatch_status=False).values('tm_no')).order_by('tm_no')
    mytm1=(PinionPressing.objects.filter(dispatch_status=False).filter(inspection_status=False).values('tm_no')).order_by('tm_no')
    mytm0=(PinionPressing.objects.filter(dispatch_status=False).filter(inspection_status=True).values('tm_no')).order_by('tm_no')
    
    my_context={
       'object':obj2,
       'nav':nav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mysno':mysno,
       'subnav':subnav,
       'axleno':axleno,
       'mytm':mytm,
       'mytm1':mytm1,
       'mytm0': mytm0,
        }
    
    
    if request.method=="POST":
        once=request.POST.get('once')
       
        submit=request.POST.get('submit')
        
        if submit=='Save':
            first=request.POST.get('bo_no')
            second=request.POST.get('bo_date')
            third=request.POST.get('date')
            fourth=request.POST.get('tm_make')
            fifth=request.POST.get('tm_no')
            sixth=request.POST.get('locos')
            pt_no=request.POST.get('pt_no')
            bo_qty=request.POST.get('bo_qty')
            indate=request.POST.get('in_qty')
            outdate=request.POST.get('out_qty')
            axle_no=request.POST.get('axle_no')
            s1 = indate.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            newindate =  year1 + "-" + month1 + "-" + day1
            s2 = outdate.split('-')
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            newoutdate =  year2 + "-" + month2 + "-" + day2
            if first and second and third and fourth and fifth and sixth and pt_no and bo_qty and indate and outdate and axle_no:
                obj=PinionPressing.objects.create()
                obj.bo_no=first
                obj.bo_date=second
                obj.pt_no=pt_no
                obj.bo_qty=bo_qty
                obj.date=third
                obj.tm_make=fourth
                obj.tm_no=fifth
                obj.loco_type=sixth
                obj.inspection_status=False
                obj.in_qty=newindate
                obj.out_qty=newoutdate
                obj.axle_no=axle_no
                obj.save()
                messages.success(request,'Successfully Added!')
                AxleWheelPressing.objects.filter(axle_no=axle_no).update(dispatch_status=True)
            else:
                messages.error(request,"Please Enter All Records!")    
        
        obj2=PinionPressing.objects.all().order_by('sno') 
        my_context={
            'object':obj2,
            }   

        if submit=='Edit':
            sno=request.POST.get('sno')
        
            if sno is not None:
           
                bo_no=request.POST.get('editbo_no')
                bo_date=request.POST.get('editbo_date')
                date=request.POST.get('editdate')
                tm_make=request.POST.get('edittm_make')
                tm_no=request.POST.get('edittm_no')
                bo_qty=request.POST.get('editbo_qty')
                pt_no=request.POST.get('editpt_no')
                indate=request.POST.get('editin_qty')
                outdate=request.POST.get('editout_qty')
                s1 = indate.split('-')
                month1 = s1[1]
                day1 = s1[0]
                year1 = s1[2]
                newindate =  year1 + "-" + month1 + "-" + day1
                s2 = outdate.split('-')
                month2 = s2[1]
                day2 = s2[0]
                year2 = s2[2]
                newoutdate =  year2 + "-" + month2 + "-" + day2
                if sno and bo_no and bo_date and date and tm_make and tm_no and pt_no and bo_qty and indate and outdate:
                    PinionPressing.objects.filter(tm_no=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,tm_make=tm_make,tm_no=tm_no,pt_no=pt_no,bo_qty=bo_qty,in_qty=newindate,out_qty=newoutdate)
                    messages.success(request, 'Successfully Edited!')
                else:
                    messages.error(request,"Please Enter S.No.!")        



        if submit=='Inspect':
            sno=request.POST.get('snowheel')
            pinion_no=request.POST.get('pinion_no')
            pinion_make=request.POST.get('pinion_make')
            pinion_travel=request.POST.get('pinion_travel')
            pinion_pressure_triangle_glycerin=request.POST.get('pinion_pressure_triangle_glycerin')
            pinion_pressure_square_ram=request.POST.get('pinion_pressure_square_ram')
            pinion_teeth_dist=request.POST.get('pinion_teeth_dist')
            blue_match=request.POST.get('blue_match')
            inspect_date=request.POST.get('inspect_date')
          
            s = inspect_date.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]
            newinspect_date =  year1 + "-" + month1 + "-" + day1
            
            if pinion_pressure_triangle_glycerin and pinion_pressure_square_ram and pinion_teeth_dist and pinion_no and pinion_make and pinion_travel and blue_match and inspect_date :
                PinionPressing.objects.filter(tm_no=sno).update(pinion_pressure_triangle_glycerin=pinion_pressure_triangle_glycerin,pinion_pressure_square_ram=pinion_pressure_square_ram,pinion_teeth_dist=pinion_teeth_dist,pinion_no=pinion_no,pinion_make=pinion_make,pinion_travel=pinion_travel,blue_match=blue_match,inspect_date=newinspect_date,inspection_status=True,dispatch_to="Inspected") 
                messages.success(request,'Successfully Inspected!')
            else:
                messages.error(request,"Please Enter All Records!")

        
        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            disdate=request.POST.get('dispatch_date')
            if sno and dislocos and disdate:
                PinionPressing.objects.filter(sno=sno).update(dispatch_date=disdate)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            sno=request.POST.get('delsno')
            if sno:
                PinionPressing.objects.filter(tm_no=sno).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")

        return HttpResponseRedirect("/PinionPress/")
    
    return render(request,"TMS/PinionPress.html",my_context)



@login_required
@role_required(urlpass='/bogieassembly/')
def bogieassembly_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    dd3=[]
    obj2=list(BogieAssembly.objects.filter(Q(dispatch_status=False)).values('sno','bo_no','pt_no','bo_qty','bo_date','loco_type','date','frameserial_no','frame_make','frame_type','in_date','out_qty','dispatch_to','inspect_date').order_by('sno'))
    obj3=list(BogieAssembly.objects.filter(Q(dispatch_status=False)).values('inspect_date','in_date','out_qty').order_by('sno'))
    ll=len(obj3)
    for i in range(0,ll):
        dd=obj3[i]['inspect_date']
        indate=obj3[i]['in_date']
        outdate=obj3[i]['out_qty']
        if dd!=None :
            s = dd.split('-')
            month1 = s[1]
            day1 = s[2]
            year1 = s[0]
            dd2 =  day1 + "-" + month1 + "-" + year1
            obj2[i].update({'inspect_date':dd2})
        else :
            obj2[i].update({'inspect_date':None})
        if indate!=None :
            s1 = indate.split('-')
            newmonth1 = s1[1]
            newday1 = s1[2]
            newyear1 = s1[0]
            newindate =  newday1 + "-" + newmonth1 + "-" + newyear1
            obj2[i].update({'in_date':newindate})
        else :
            obj2[i].update({'in_qty':None}) 

        if outdate!=None :
            s2 = outdate.split('-')
            newmonth2 = s2[1]
            newday2 = s2[2]
            newyear2 = s2[0]
            newoutdate =  newday2 + "-" + newmonth2 + "-" + newyear2
            obj2[i].update({'out_qty':newoutdate})
        else :
            obj2[i].update({'out_qty':None})
    mybo=Batch.objects.all().values('bo_no')
    hhpmysno=BogieAssembly.objects.all().filter((Q(pt_no='17010019')|Q(pt_no='17010706')|Q(pt_no='17010639')|Q(pt_no='17010330')|Q(pt_no='17010421')|Q(pt_no='16010085')|Q(pt_no='16010206')|Q(pt_no='16010255')|Q(pt_no='17010019')|Q(pt_no='17010391')),dispatch_status=False).values('frameserial_no','pt_no').order_by('frameserial_no')
    hhpmysno0=BogieAssembly.objects.all().filter((Q(pt_no='17010019')|Q(pt_no='17010706')|Q(pt_no='17010639')|Q(pt_no='17010330')|Q(pt_no='17010421')|Q(pt_no='16010085')|Q(pt_no='16010206')|Q(pt_no='16010255')|Q(pt_no='17010019')|Q(pt_no='17010391')),dispatch_status=False).values('frameserial_no','pt_no').filter(inspection_status=True).order_by('frameserial_no')
    hhpmysno1=BogieAssembly.objects.all().filter((Q(pt_no='17010019')|Q(pt_no='17010706')|Q(pt_no='17010639')|Q(pt_no='17010330')|Q(pt_no='17010421')|Q(pt_no='16010085')|Q(pt_no='16010206')|Q(pt_no='16010255')|Q(pt_no='17010019')|Q(pt_no='17010391')),dispatch_status=False).values('frameserial_no','pt_no').filter(inspection_status=False).order_by('frameserial_no')
    mysno=(BogieAssembly.objects.values('frameserial_no')).order_by('frameserial_no')
    mysno0=(BogieAssembly.objects.values('frameserial_no').filter(inspection_status=True)).order_by('frameserial_no')
    mysno1=(BogieAssembly.objects.values('frameserial_no').filter(inspection_status=False)).order_by('frameserial_no')
    
    myaxle=(PinionPressing.objects.all().filter(inspection_status=True,dispatch_status=False).values('axle_no')).order_by('axle_no')
    mytm=PinionPressing.objects.all().values('tm_no')
    mymsu=AxleWheelPressing.objects.all().values('msu_unit_no')
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'hhpmysno':hhpmysno,
       'hhpmysno0':hhpmysno0,
       'hhpmysno1':hhpmysno1,
       'mysno':mysno,
       'mysno0':mysno0,
       'mysno1':mysno1,
       'myaxle':myaxle,
       'mytm':mytm,
       'mymsu':mymsu,
    }

    if request.method=="POST":

        once=request.POST.get('once')
        print(once)
        submit=request.POST.get('submit')

        if submit=='Save':
            bo_no=request.POST.get('bo_no')
            bo_date=request.POST.get('bo_date')
            date=request.POST.get('date')
            pt_no=request.POST.get('pt_no')
            bo_qty=request.POST.get('bo_qty')
            loco_type=request.POST.get('locos')
            in_date=request.POST.get('in_date')
            outdate=request.POST.get('out_qty')
            frameserial_no=request.POST.get('frameserial_no')
            frame_make=request.POST.get('frame_make')
            frame_type=request.POST.get('frame_type')
            first_axle=request.POST.get('first_axle')
            second_axle=request.POST.get('second_axle')
            third_axle=request.POST.get('third_axle')
            first_axle_location=request.POST.get('first_axle_location')
            second_axle_location=request.POST.get('second_axle_location')
            third_axle_location=request.POST.get('third_axle_location')
            chkinsp=request.POST.get('insp_supplier')
            s1 = in_date.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            newindate =  year1 + "-" + month1 + "-" + day1
            s2 = outdate.split('-')
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            newoutdate =  year2 + "-" + month2 + "-" + day2
            

            if bo_no and bo_date and date and loco_type and frameserial_no and frame_make and frame_type and in_date and outdate and bo_qty and pt_no and first_axle and second_axle and third_axle and first_axle_location and second_axle_location and third_axle_location :
               obj=BogieAssembly.objects.create()
               obj.bo_no=bo_no
               obj.bo_date=bo_date
               obj.pt_no=pt_no
               obj.bo_qty=bo_qty
               obj.date=date
               obj.loco_type=loco_type
               obj.in_date=newindate
               obj.out_qty=newoutdate
               obj.frame_make=frame_make
               obj.frame_type=frame_type
               obj.frameserial_no=frameserial_no
               obj.inspection_status=False
               obj.first_axle=first_axle
               obj.second_axle=second_axle
               obj.third_axle=third_axle
               obj.first_axle_location=first_axle_location
               obj.second_axle_location=second_axle_location
               obj.third_axle_location=third_axle_location
               s = date.split('-')
               month1 = s[1]
               day1 = s[0]
               year1 = s[2]
               insp_date =  year1 + "-" + month1 + "-" + day1
               if (chkinsp):
                   obj.inspection_status=True
                   obj.dispatch_to="Inspected"
                   obj.inspect_date=insp_date
               obj.save()
               messages.success(request, 'Successfully Added!')
               PinionPressing.objects.filter(axle_no=first_axle).update(dispatch_status=True)
               PinionPressing.objects.filter(axle_no=second_axle).update(dispatch_status=True)
               PinionPressing.objects.filter(axle_no=third_axle).update(dispatch_status=True)
            else:
               messages.error(request,"Please Enter All Records!") 

            obj2=BogieAssembly.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            'mybo':mybo,
            'mysno':mysno,
            }

        if submit=='Edit':
            sno=request.POST.get('editsno')
           
            if sno is not None:
                
                bo_no=request.POST.get('editbo_no')
                bo_date=request.POST.get('editbo_date')
                date=request.POST.get('editdate')
                loco_type=request.POST.get('editlocos')
                in_date=request.POST.get('editin_date')
                outdate=request.POST.get('editout_qty')
                frameserial_no=request.POST.get('editframeserial_no')
                frame_make=request.POST.get('editframe_make')
                frame_type=request.POST.get('editframe_type')
                bo_qty=request.POST.get('editbo_qty')
                pt_no=request.POST.get('editpt_no')
                first_axle=request.POST.get('editfirst_axle')
                second_axle=request.POST.get('editsecond_axle')
                third_axle=request.POST.get('editthird_axle')
                first_axle_location=request.POST.get('editfirst_axle_location')
                second_axle_location=request.POST.get('editsecond_axle_location')
                third_axle_location=request.POST.get('editthird_axle_location')
                s1 = in_date.split('-')
                month1 = s1[1]
                day1 = s1[0]
                year1 = s1[2]
                newindate =  year1 + "-" + month1 + "-" + day1
                s2 = outdate.split('-')
                month2 = s2[1]
                day2 = s2[0]
                year2 = s2[2]
                newoutdate =  year2 + "-" + month2 + "-" + day2
            
                if bo_no and bo_date and date and loco_type and frameserial_no and frame_make and frame_type and in_date and outdate and pt_no and bo_qty and first_axle and second_axle and third_axle and first_axle_location and second_axle_location and third_axle_location:
                    BogieAssembly.objects.filter(frameserial_no=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,frameserial_no=frameserial_no,frame_make=frame_make,frame_type=frame_type,in_date=newindate,out_qty=newoutdate,pt_no=pt_no,bo_qty=bo_qty,first_axle=first_axle,second_axle=second_axle,third_axle=third_axle,first_axle_location=first_axle_location,second_axle_location=second_axle_location,third_axle_location=third_axle_location)
                    messages.success(request, 'Successfully Edited!')
                else:
                    messages.error(request,"Please Enter S.No.!")

                my_context={
                'object':obj2,
                'mybo':mybo,
                'mysno':mysno,
            }

        if submit=="Dispatch":
            sno=request.POST.get('dissno')
            dislocos=request.POST.get('dislocos')
            disdate=request.POST.get('dispatch_date')
            if sno and dislocos and disdate:
                BogieAssembly.objects.filter(frameserial_no=sno).update(dispatch_to=dislocos,dispatch_status=True,dispatch_date=disdate)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")

        if submit=='InspectHHP':
            sno=request.POST.get('hhpaddsno')
            h_plate=request.POST.get('h_plate')
            first_axle_location=request.POST.get('hhpfirst_location')
            first=request.POST.get('hhpfirst')
            first_coilspring_make=request.POST.get('hhpfirst_coilspring_make')
            first_secondary_coilspring_make=request.POST.get('hhpfirst_secondary_coilspring_make')
            first_gearcase_no=request.POST.get('hhpfirst_gearcase_no')
            first_gearcase_make=request.POST.get('hhpfirst_gearcase_make')
            first_back_lash=request.POST.get('hhpfirst_back_lash')
            first_vertical_r=request.POST.get('hhpfirst_vertical_r')
            first_vertical_l=request.POST.get('hhpfirst_vertical_l')
            first_horizontal_r=request.POST.get('hhpfirst_horizontal_r')
            first_horizontal_l=request.POST.get('hhpfirst_horizontal_l')
            second_axle_location=request.POST.get('hhpsecond_location')
            second=request.POST.get('hhpsecond')
            second_coilspring_make=request.POST.get('hhpsecond_coilspring_make')
            second_secondary_coilspring_make=request.POST.get('hhpsecond_secondary_coilspring_make')
            second_gearcase_no=request.POST.get('hhpsecond_gearcase_no')
            second_gearcase_make=request.POST.get('hhpsecond_gearcase_make')
            second_back_lash=request.POST.get('hhpsecond_back_lash')
            second_vertical_r=request.POST.get('hhpsecond_vertical_r')
            second_vertical_l=request.POST.get('hhpsecond_vertical_l')
            second_horizontal_r=request.POST.get('hhpsecond_horizontal_r')
            second_horizontal_l=request.POST.get('hhpsecond_horizontal_l')
            third_axle_location=request.POST.get('hhpthird_location')
            third=request.POST.get('hhpthird')
            third_coilspring_make=request.POST.get('hhpthird_coilspring_make')
            third_secondary_coilspring_make=request.POST.get('hhpthird_secondary_coilspring_make')
            third_gearcase_no=request.POST.get('hhpthird_gearcase_no')
            third_gearcase_make=request.POST.get('hhpthird_gearcase_make')
            third_back_lash=request.POST.get('hhpthird_back_lash')
            third_vertical_r=request.POST.get('hhpthird_vertical_r')
            third_vertical_l=request.POST.get('hhpthird_vertical_l')
            third_horizontal_r=request.POST.get('hhpthird_horizontal_r')
            third_horizontal_l=request.POST.get('hhpthird_horizontal_l')
            wheel_set_guide=request.POST.get('hhpwheel_set_guide')
            gear_case_oil=request.POST.get('hhpgear_case_oil')
            break_rigging_make=request.POST.get('hhpbreak_rigging_make')
            sand_box_make=request.POST.get('hhpsand_box_make')
            spheri_block_make=request.POST.get('hhpspheri_block_make')
            elastic_shop_make=request.POST.get('hhpelastic_shop_make')
            lateral_damper=request.POST.get('hhplateral_damper')
            thrust_pad_make=request.POST.get('hhpthrust_pad_make')
            break_cylinder_make=request.POST.get('hhpbreak_cylinder_make')
            inspect_date=request.POST.get('hhpdate')
            motor_check=request.POST.get('hhpmotor_check')
            motor_date=request.POST.get('hhpmotor_date')
            lowering_check=request.POST.get('hhplowering_check')
            lowering_date=request.POST.get('hhplowering_date')
            dispatch_check=request.POST.get('hhpdispatch_check')
            dispatch_check_date=request.POST.get('hhpdispatch_check_date')
            loco_paper=request.POST.get('hhploco_paper')
            locopaper_date=request.POST.get('hhplocopaper_date')
            s = inspect_date.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]
            newinspect_date =  year1 + "-" + month1 + "-" + day1
            if  motor_check and motor_date and lowering_check and lowering_date and dispatch_check and dispatch_check_date and loco_paper and locopaper_date and h_plate and first_axle_location and second_axle_location and third_axle_location and first and second and third and first_coilspring_make and first_secondary_coilspring_make and first_gearcase_make and first_back_lash and first_gearcase_no and first_horizontal_l and first_vertical_l and first_horizontal_r and first_vertical_r and second_back_lash and second_coilspring_make and second_secondary_coilspring_make and second_gearcase_make and second_gearcase_no and second_horizontal_l and second_horizontal_l and second_horizontal_r and second_vertical_l and second_vertical_r and third_back_lash and third_coilspring_make and third_secondary_coilspring_make and third_gearcase_make and third_gearcase_no and third_horizontal_l and third_horizontal_r and third_vertical_l and third_vertical_r  and wheel_set_guide and gear_case_oil and break_rigging_make and sand_box_make and spheri_block_make and elastic_shop_make and lateral_damper and wheel_set_guide and gear_case_oil and thrust_pad_make and inspect_date:
                BogieAssembly.objects.filter(frameserial_no=sno).update(locopaper_date=locopaper_date,loco_paper=loco_paper,dispatch_check_date=dispatch_check_date,dispatch_check=dispatch_check,lowering_date=lowering_date,lowering_check=lowering_check,motor_check=motor_check,motor_date=motor_date,h_plate=h_plate,inspection_status=True,first_axle_location=first_axle_location,second_axle_location=second_axle_location,third_axle_location=third_axle_location,first_axle=first,second_axle=second,third_axle=third,first_coilspring_make=first_coilspring_make,first_secondary_coilspring_make=first_secondary_coilspring_make,first_gearcase_make=first_gearcase_make,first_back_lash=first_back_lash,first_gearcase_no=first_gearcase_no,first_horizontal_l=first_horizontal_l,first_vertical_l=first_vertical_l,first_horizontal_r=first_horizontal_r,first_vertical_r=first_vertical_r,second_back_lash=second_back_lash,second_coilspring_make =second_coilspring_make,second_secondary_coilspring_make=second_secondary_coilspring_make,second_gearcase_make =second_gearcase_make ,second_gearcase_no =second_gearcase_no ,second_horizontal_l =second_horizontal_l ,second_horizontal_r =second_horizontal_r ,second_vertical_l =second_vertical_l ,second_vertical_r =second_vertical_r ,third_back_lash =third_back_lash ,third_coilspring_make =third_coilspring_make,third_secondary_coilspring_make=third_secondary_coilspring_make ,third_gearcase_make =third_gearcase_make ,third_gearcase_no =third_gearcase_no ,third_horizontal_l =third_horizontal_l ,third_horizontal_r =third_horizontal_r ,third_vertical_l =third_vertical_l ,third_vertical_r=third_vertical_r,wheel_set_guide=wheel_set_guide,gear_case_oil=gear_case_oil,break_rigging_make=break_rigging_make,sand_box_make=sand_box_make,spheri_block_make=spheri_block_make,elastic_shop_make=elastic_shop_make,lateral_damper=lateral_damper,thrust_pad_make=thrust_pad_make ,dispatch_to="HHP_Inspected",inspect_date=newinspect_date) 
                messages.success(request,'Successfully Inspected!')
            else:
                messages.error(request,"Please Enter All Records!")

        if submit=='Inspect':
            sno=request.POST.get('addsno')
            torque_support=request.POST.get('torque_support')
            first_axle_location=request.POST.get('first_location')
            first=request.POST.get('first')
            first_coilspring_make=request.POST.get('first_coilspring_make')
            first_gearcase_no=request.POST.get('first_gearcase_no')
            first_gearcase_make=request.POST.get('first_gearcase_make')
            first_back_lash=request.POST.get('first_back_lash')
            first_vertical_r=request.POST.get('first_vertical_r')
            first_vertical_l=request.POST.get('first_vertical_l')
            first_horizontal_r=request.POST.get('first_horizontal_r')
            first_horizontal_l=request.POST.get('first_horizontal_l')
            second_axle_location=request.POST.get('second_location')
            second=request.POST.get('second')
            second_coilspring_make=request.POST.get('second_coilspring_make')
            second_gearcase_no=request.POST.get('second_gearcase_no')
            second_gearcase_make=request.POST.get('second_gearcase_make')
            second_back_lash=request.POST.get('second_back_lash')
            second_vertical_r=request.POST.get('second_vertical_r')
            second_vertical_l=request.POST.get('second_vertical_l')
            second_horizontal_r=request.POST.get('second_horizontal_r')
            second_horizontal_l=request.POST.get('second_horizontal_l')
            third_axle_location=request.POST.get('third_location')
            third=request.POST.get('third')
            third_coilspring_make=request.POST.get('third_coilspring_make')
            third_gearcase_no=request.POST.get('third_gearcase_no')
            third_gearcase_make=request.POST.get('third_gearcase_make')
            third_back_lash=request.POST.get('third_back_lash')
            third_vertical_r=request.POST.get('third_vertical_r')
            third_vertical_l=request.POST.get('third_vertical_l')
            third_horizontal_r=request.POST.get('third_horizontal_r')
            third_horizontal_l=request.POST.get('third_horizontal_l')
            wheel_set_guide=request.POST.get('wheel_set_guide')
            gear_case_oil=request.POST.get('gear_case_oil')
            break_rigging_make=request.POST.get('break_rigging_make')
            sand_box_make=request.POST.get('sand_box_make')
            spheri_block_make=request.POST.get('spheri_block_make')
            elastic_shop_make=request.POST.get('elastic_shop_make')
            horizontal_damper=request.POST.get('horizontal_damper')
            inspect_date=request.POST.get('inspectdate')
            motor_check=request.POST.get('motor_check')
            motor_date=request.POST.get('motor_date')
            lowering_check=request.POST.get('lowering_check')
            lowering_date=request.POST.get('lowering_date')
            dispatch_check=request.POST.get('dispatch_check')
            dispatch_check_date=request.POST.get('dispatch_check_date')
            loco_paper=request.POST.get('loco_paper')
            locopaper_date=request.POST.get('locopaper_date')
            break_cylinder_make=request.POST.get('break_cylinder_make')
            s = inspect_date.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]
            newinspect_date =  year1 + "-" + month1 + "-" + day1
            if  break_cylinder_make and torque_support and locopaper_date and loco_paper and dispatch_check_date and dispatch_check and lowering_date and lowering_check and motor_date and motor_check and first_axle_location and second_axle_location and third_axle_location and first and second and third and first_coilspring_make and first_gearcase_make and first_back_lash and first_gearcase_no and first_horizontal_l and first_vertical_l and first_horizontal_r and first_vertical_r and second_back_lash and second_coilspring_make and second_gearcase_make and second_gearcase_no and second_horizontal_l and second_horizontal_l and second_horizontal_r and second_vertical_l and second_vertical_r and third_back_lash and third_coilspring_make and third_gearcase_make and third_gearcase_no and third_horizontal_l and third_horizontal_r and third_vertical_l and third_vertical_r  and wheel_set_guide and gear_case_oil and break_rigging_make and sand_box_make and spheri_block_make and elastic_shop_make and horizontal_damper and inspect_date:
                BogieAssembly.objects.filter(frameserial_no=sno).update(break_cylinder_make=break_cylinder_make,torque_support=torque_support,inspection_status=True,motor_check=motor_check,motor_date=motor_date,lowering_check=lowering_check,lowering_date=lowering_date,dispatch_check=dispatch_check,dispatch_check_date=dispatch_check_date,loco_paper=loco_paper,locopaper_date=locopaper_date,first_axle_location=first_axle_location,second_axle_location=second_axle_location,third_axle_location=third_axle_location,first_axle=first,second_axle=second,third_axle=third,first_coilspring_make=first_coilspring_make,first_gearcase_make=first_gearcase_make,first_back_lash=first_back_lash,first_gearcase_no=first_gearcase_no,first_horizontal_l=first_horizontal_l,first_vertical_l=first_vertical_l,first_horizontal_r=first_horizontal_r,first_vertical_r=first_vertical_r,second_back_lash=second_back_lash,second_coilspring_make =second_coilspring_make ,second_gearcase_make =second_gearcase_make ,second_gearcase_no =second_gearcase_no ,second_horizontal_l =second_horizontal_l ,second_horizontal_r =second_horizontal_r ,second_vertical_l =second_vertical_l ,second_vertical_r =second_vertical_r ,third_back_lash =third_back_lash ,third_coilspring_make =third_coilspring_make ,third_gearcase_make =third_gearcase_make ,third_gearcase_no =third_gearcase_no ,third_horizontal_l =third_horizontal_l ,third_horizontal_r =third_horizontal_r ,third_vertical_l =third_vertical_l ,third_vertical_r=third_vertical_r,wheel_set_guide=wheel_set_guide,gear_case_oil=gear_case_oil,break_rigging_make=break_rigging_make,sand_box_make=sand_box_make,spheri_block_make=spheri_block_make,elastic_shop_make=elastic_shop_make,horizontal_damper=horizontal_damper ,dispatch_to="Inspected",inspect_date=newinspect_date) 
                messages.success(request,'Successfully Inspected!')
            else:
                messages.error(request,"Please Enter All Records!")

        if submit=='Delete':

            sno=request.POST.get('delsno')
            if sno:
                BogieAssembly.objects.filter(frameserial_no=sno).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")
        

        
        return HttpResponseRedirect("/bogieassembly/")

    return render(request,"TMS/bogieassembly.html",my_context)



@login_required
@role_required(urlpass='/wheelreport/')
def wheelreport(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    a=0
    context={
        'a':a,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':88,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Wheel Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':5,
            }
        if bval=='No. of Wheel (date wise)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':6,
            }
        if bval=='No. of Wheel (date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':7,
            }
        if bval=='Month Wise Detail':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':10,
            }
        if bval=='Wheel Record of Loco Type (date wise)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':20,
            }
        if bval=='Wheel Record of Loco Type (date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':22,
            }
        if bval=='Proceed1':
            pt=[]
            pto=[]
            lt=[]
            lto=[]
            count=[]
            count1=[]
            myval=[]
            myval1=[]
            unique_myval=[]
            unique_myval1=[]
            c1=0
            c2=0
            dt=request.POST.get('datew')
            s = dt.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(WheelMachining.objects.filter(in_qty=date).values('pt_no','loco_type','wheel_no'))
            ob2=list(WheelMachining.objects.filter(out_qty=date).values('pt_no','loco_type','wheel_no'))   
            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                pt.append(ob1[i]['pt_no'])
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range (0,len(pt)):
                for j in range(0,len(pt)):
                    if(pt[i]==pt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(pt)):
                myval.append({'pt_no':pt[i], 'loco_type':lt[i], 'count1':count[i],'count2':'0'})

            for i in range(0,len(ob2)):
                pto.append(ob2[i]['pt_no'])
            
            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(pto)):
                for j in range(0,len(pto)):
                    if(pto[i]==pto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0

            for i in range (0,len(pto)):
                myval1.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['pt_no']==myval[j]['pt_no']:
                        final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['pt_no'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['pt_no'] not in id:
                    final.append({'pt_no':pt[j], 'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)
            
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'dt':dt,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            s1 = dt1.split('-')
            s2 = dt2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            date1 =  year1 + "-" + month1 + "-" + day1
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            date2 =  year2 + "-" + month2 + "-" + day2
            ob1=WheelMachining.objects.filter(in_qty__range=(date1,date2)).values('pt_no','loco_type')
            ob2=WheelMachining.objects.filter(out_qty__range=(date1,date2)).values('pt_no','loco_type')
            pt=[] 
            lt=[] 
            pto=[]
            lto=[]
            myval=[]
            myval1=[]
            final=[]
            unique_final=[]
            count=[]
            count1=[]
            c1=0
            c2=0

            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                pt.append(ob1[i]['pt_no'])
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range (0,len(pt)):
                for j in range(0,len(pt)):
                    if(pt[i]==pt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(pt)):
                myval.append({'pt_no':pt[i], 'loco_type':lt[i], 'count1':count[i],'count2':'0'})

            for i in range(0,len(ob2)):
                pto.append(ob2[i]['pt_no'])
            
            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(pto)):
                for j in range(0,len(pto)):
                    if(pto[i]==pto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0

            for i in range (0,len(pto)):
                myval1.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['pt_no']==myval[j]['pt_no']:
                        final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['pt_no'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['pt_no'] not in id:
                    final.append({'pt_no':pt[j], 'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'dt1':dt1,
            'dt2':dt2,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }
        if bval=='Proceed':
            wheel_no=request.POST.get('wheel_no')
            ob1=list(WheelMachining.objects.filter(wheel_no=wheel_no).values('wheel_no','loco_type','date','bo_no','wheel_heatcaseno','ustwhl','hub_lengthwhl','tread_diawhl','rim_thicknesswhl','bore_diawhl','inspector_namewhl','datewhl'))
            l=len(ob1)
            if l>0:
                for i in range(0,l):
                    dd=ob1[i]['datewhl']
                    if dd!=None:
                        s=dd.split('-')
                        month=s[1]
                        day=s[2]
                        year=s[0]
                        dd2=day + '-' + month + '-' + year
                        ob1[i].update({'datewhl':dd2})
                    else:
                        ob1[i].update({'datewhl':None})
            ob2=list(AxleWheelPressing.objects.filter(Q(wheelno_de=wheel_no)|Q(wheelno_nde=wheel_no)).values('axle_no','inspect_date','inspector_name'))
            l1=len(ob2)
            if l1>0:
                for i in range(0,l1):
                    dd3=ob2[i]['inspect_date']
                    if dd3!=None:
                        s1=dd3.split('-')
                        month1=s1[1]
                        day1=s1[2]
                        year1=s1[0]
                        dd4=day1 + '-' + month1 + '-' + year1
                        ob2[i].update({'inspect_date':dd4})
                    else:
                        ob2[i].update({'inspect_date':None})
            context={
                'nav':nav,
                'subnav':subnav,
                'usermaster':usermaster,
                'ip':get_client_ip(request),
                'sub':4,
                'ob1':ob1,
                'ob2':ob2,
                'l':l,
            }

        if bval=='Proceed6':
            dt1=request.POST.get('datea')
            ob1=WheelMachining.objects.filter(in_qty=dt1).values('sno','wheel_no','in_qty').order_by('in_qty')
            ob2=WheelMachining.objects.filter(out_qty=dt1).values('sno','wheel_no','out_qty').order_by('out_qty')
            l1=len(ob1)
            l2=len(ob2)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':8,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,
            'l1':l1,'l2':l2,
            }
        if bval=='Proceed7':
            dt1=request.POST.get('datea1')
            dt2=request.POST.get('datea2')
            ob1=WheelMachining.objects.filter(in_qty__range=(dt1,dt2)).values('sno','wheel_no','in_qty').order_by('in_qty')
            ob2=WheelMachining.objects.filter(out_qty__range=(dt1,dt2)).values('sno','wheel_no','out_qty').order_by('out_qty')
            l1=len(ob1)
            l2=len(ob2)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':9,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            'l1':l1,'l2':l2,
            }
        if bval=='Proceed10':
            mon=request.POST.get('month')
            ob1=WheelMachining.objects.filter(date__contains=mon).values('sno','wheel_no','in_qty','out_qty','pt_no','date').order_by('date')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':11,
            'ob1':ob1,
            'mon':mon,
            }
        if bval=='Proceed20':
            a=1
            datel=request.POST.get('datel')
            s = datel.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(WheelMachining.objects.filter(datewhl=date).values('wheel_no','wheel_heatcaseno','ustwhl','hub_lengthwhl','tread_diawhl','rim_thicknesswhl','bore_diawhl','inspector_namewhl','datewhl'))
            context={
            'a':a,
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':21,
            'ob1':ob1,
            'datel':datel,   
            }
        if bval=='Proceed22':
            datell1=request.POST.get('datell1')
            datell2=request.POST.get('datell2')
            s1 = datell1.split('-')
            s2 = datell2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            date1 =  year1 + "-" + month1 + "-" + day1
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            date2 =  year2 + "-" + month2 + "-" + day2
            ob1=list(WheelMachining.objects.filter(datewhl__range=(date1,date2)).values('wheel_no','wheel_heatcaseno','ustwhl','hub_lengthwhl','tread_diawhl','rim_thicknesswhl','bore_diawhl','inspector_namewhl','datewhl'))
            ll=len(ob1)
            if ll>0:
                for i in range(0,ll):
                    dd=ob1[i]['datewhl']
                    if dd!=None:
                        s=dd.split('-')
                        month=s[1]
                        day=s[2]
                        year=s[0]
                        dd2=day + '-' + month + '-' + year
                        ob1[i].update({'datewhl':dd2})
                    else:
                        ob1[i].update({'datewhl':None})
            context={
            'a':a,
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':23,
            'ob1':ob1,
            'datell1':datell1, 
            'datell2':datell2,  
            }
            

    return render(request,'TMS/wheelreport.html',context)


@login_required
@role_required(urlpass='/axlereport/')
def axlereport(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context={
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Axle Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':10,
            }
        if bval=='Axle Record of Loco Type (date wise)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':6,
            }
        if bval=='Axle Record of Loco Type (date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':7,
            }
        if bval=='Proceed1':
                    
            pt=[]
            pto=[]
            lt=[]
            lto=[]
            count=[]
            count1=[]
            myval=[]
            myval1=[]
            unique_myval=[]
            unique_myval1=[]
            c1=0
            c2=0
            dt=request.POST.get('datew')
            s = dt.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(AxleMachining.objects.filter(in_qty=date).values('pt_no','loco_type','axle_no'))
            ob2=list(AxleMachining.objects.filter(out_qty=date).values('pt_no','loco_type','axle_no'))   
            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                pt.append(ob1[i]['pt_no'])
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range (0,len(pt)):
                for j in range(0,len(pt)):
                    if(pt[i]==pt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(pt)):
                myval.append({'pt_no':pt[i], 'loco_type':lt[i], 'count1':count[i],'count2':'0'})


            for i in range(0,len(ob2)):
                pto.append(ob2[i]['pt_no'])
            
            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(pto)):
                for j in range(0,len(pto)):
                    if(pto[i]==pto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0

            for i in range (0,len(pto)):
                myval1.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['pt_no']==myval[j]['pt_no']:
                        final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['pt_no'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['pt_no'] not in id:
                    final.append({'pt_no':pt[j], 'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)
            
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'dt':dt,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }
            
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            s1 = dt1.split('-')
            s2 = dt2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            date1 =  year1 + "-" + month1 + "-" + day1
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            date2 =  year2 + "-" + month2 + "-" + day2
            ob1=AxleMachining.objects.filter(in_qty__range=(date1,date2)).values('pt_no','loco_type')
            ob2=AxleMachining.objects.filter(out_qty__range=(date1,date2)).values('pt_no','loco_type')
            pt=[] 
            lt=[] 
            pto=[]
            lto=[]
            myval=[]
            myval1=[]
            final=[]
            unique_final=[]
            count=[]
            count1=[]
            c1=0
            c2=0

            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                pt.append(ob1[i]['pt_no'])
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range (0,len(pt)):
                for j in range(0,len(pt)):
                    if(pt[i]==pt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(pt)):
                myval.append({'pt_no':pt[i], 'loco_type':lt[i], 'count1':count[i],'count2':'0'})
            
            for i in range(0,len(ob2)):
                pto.append(ob2[i]['pt_no'])
            
            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(pto)):
                for j in range(0,len(pto)):
                    if(pto[i]==pto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0

            for i in range (0,len(pto)):
                myval1.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['pt_no']==myval[j]['pt_no']:
                        final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['pt_no'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['pt_no'] not in id:
                    final.append({'pt_no':pt[j], 'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'dt1':dt1,
            'dt2':dt2,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }

        if bval=='Proceed3':
            dt1=request.POST.get('date3')
            dt2=request.POST.get('date4')
            ob1=AxleMachining.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','axle_no','ustaxle_status','in_qty').order_by('in_qty')
            ob2=AxleMachining.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','axle_no','ustaxle_status','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':4,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }
        if bval=='Proceed6':
            datel=request.POST.get('datea')
            s = datel.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(AxleMachining.objects.filter(dateaxle=date).values('axle_no','bo_no','date','loco_type','axle_heatcaseno','ustaxle','axlelength','journalaxle','throweraxle','wheelseataxle','gearseataxle','collaraxle','journal_surfacefinishGE','wheelseat_surfacefinishGE','gearseat_surfacefinishGE','journal_surfacefinishFE','wheelseat_surfacefinishFE','gearseat_surfacefinishFE','collaraxlende','wheelseataxlende','throweraxlende','journalaxlende','bearingaxle','abutmentaxle','dateaxle','inspector_nameaxle'))
            l=len(ob1)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':8,
            'ob1':ob1,
            'datel':datel,
            }
        if bval=='Proceed7':
            datea1=request.POST.get('datea1')
            datea2=request.POST.get('datea2')
            s1 = datea1.split('-')
            s2 = datea2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            datell1 =  year1 + "-" + month1 + "-" + day1
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            datell2 =  year2 + "-" + month2 + "-" + day2
            ob1=list(AxleMachining.objects.filter(dateaxle__range=(datell1,datell2)).values('axle_no','bo_no','date','loco_type','axle_heatcaseno','ustaxle','axlelength','journalaxle','throweraxle','wheelseataxle','gearseataxle','collaraxle','journal_surfacefinishGE','wheelseat_surfacefinishGE','gearseat_surfacefinishGE','journal_surfacefinishFE','wheelseat_surfacefinishFE','gearseat_surfacefinishFE','collaraxlende','wheelseataxlende','throweraxlende','journalaxlende','bearingaxle','abutmentaxle','dateaxle','inspector_nameaxle'))
            ll=len(ob1)
            if ll>0:
                for i in range(0,ll):
                    dd=ob1[i]['dateaxle']
                    if dd!=None:
                        s=dd.split('-')
                        month=s[1]
                        day=s[2]
                        year=s[0]
                        dd2=day + '-' + month + '-' + year
                        ob1[i].update({'dateaxle':dd2})
                    else:
                        ob1[i].update({'dateaxle':None})
            l=len(ob1)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':9,
            'ob1':ob1,
            'datea1':datea1, 
            'datea2':datea2,
            }
        if bval=='Proceed':
            axle_no=request.POST.get('axle_no')
            ob1=list(AxleMachining.objects.filter(axle_no=axle_no).values('axle_no','bo_no','date','loco_type','axle_heatcaseno','ustaxle','axlelength','journalaxle','throweraxle','wheelseataxle','gearseataxle','collaraxle','journal_surfacefinishGE','wheelseat_surfacefinishGE','gearseat_surfacefinishGE','journal_surfacefinishFE','wheelseat_surfacefinishFE','gearseat_surfacefinishFE','collaraxlende','wheelseataxlende','throweraxlende','journalaxlende','bearingaxle','abutmentaxle','dateaxle','inspector_nameaxle'))
            ax=ob1[0]['axle_no']
            l=len(ob1)
            if l>0:
                for i in range(0,l):
                    dd=ob1[i]['dateaxle']
                    if dd!=None:
                        s=dd.split('-')
                        month=s[1]
                        day=s[2]
                        year=s[0]
                        dd2=day + '-' + month + '-' + year
                        ob1[i].update({'dateaxle':dd2})
                    else:
                        ob1[i].update({'dateaxle':None})
            ob2=list(AxleWheelPressing.objects.filter(axle_no=axle_no).values('wheelno_de','wheelno_nde','inspect_date','inspector_name'))
            l1=len(ob2)
            if l1>0:
                for i in range(0,l1):
                    dd3=ob2[i]['inspect_date']
                    if dd3!=None:
                        s1=dd3.split('-')
                        month1=s1[1]
                        day1=s1[2]
                        year1=s1[0]
                        dd4=day1 + '-' + month1 + '-' + year1
                        ob2[i].update({'inspect_date':dd4})
                    else:
                        ob2[i].update({'inspect_date':None})
            context={
                'nav':nav,
                'subnav':subnav,
                'usermaster':usermaster,
                'ip':get_client_ip(request),
                'sub':4,
                'ob1':ob1,
                'ob2':ob2,
                'l':l,
                'ax':ax,
                'l1':l1
            }

    return render(request,'TMS/axlereport.html',context)


@login_required
@role_required(urlpass='/axlepressreport/')
def axlepressreport(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context={
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=="Axle Report":
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':4,
            }
        if bval=='Record of Loco Type (date wise)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':10,
            }
        if bval=='Record of Loco Type (date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':12,
            }
        if bval=='Proceed1':
            pt=[]
            pto=[]
            lt=[]
            lto=[]
            count=[]
            count1=[]
            myval=[]
            myval1=[]
            unique_myval=[]
            unique_myval1=[]
            c1=0
            c2=0
            dt=request.POST.get('datew')
            s = dt.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(AxleWheelPressing.objects.filter(in_qty=date).values('pt_no','loco_type','axle_no'))
            ob2=list(AxleWheelPressing.objects.filter(out_qty=date).values('pt_no','loco_type','axle_no'))   
            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                pt.append(ob1[i]['pt_no'])
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range (0,len(pt)):
                for j in range(0,len(pt)):
                    if(pt[i]==pt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(pt)):
                myval.append({'pt_no':pt[i], 'loco_type':lt[i], 'count1':count[i],'count2':'0'})


            for i in range(0,len(ob2)):
                pto.append(ob2[i]['pt_no'])
            
            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(pto)):
                for j in range(0,len(pto)):
                    if(pto[i]==pto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0

            for i in range (0,len(pto)):
                myval1.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['pt_no']==myval[j]['pt_no']:
                        final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['pt_no'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['pt_no'] not in id:
                    final.append({'pt_no':pt[j], 'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)
            
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'dt':dt,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            s1 = dt1.split('-')
            s2 = dt2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            date1 =  year1 + "-" + month1 + "-" + day1
            
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            date2 =  year2 + "-" + month2 + "-" + day2
            ob1=AxleWheelPressing.objects.filter(in_qty__range=(date1,date2)).values('pt_no','loco_type')
            ob2=AxleWheelPressing.objects.filter(out_qty__range=(date1,date2)).values('pt_no','loco_type')
            pt=[] 
            lt=[] 
            pto=[]
            lto=[]
            myval=[]
            myval1=[]
            final=[]
            unique_final=[]
            count=[]
            count1=[]
            c1=0
            c2=0

            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                pt.append(ob1[i]['pt_no'])
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range (0,len(pt)):
                for j in range(0,len(pt)):
                    if(pt[i]==pt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(pt)):
                myval.append({'pt_no':pt[i], 'loco_type':lt[i], 'count1':count[i],'count2':'0'})

            for i in range(0,len(ob2)):
                pto.append(ob2[i]['pt_no'])
            
            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(pto)):
                for j in range(0,len(pto)):
                    if(pto[i]==pto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0

            for i in range (0,len(pto)):
                myval1.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['pt_no']==myval[j]['pt_no']:
                        final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['pt_no'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['pt_no'] not in id:
                    final.append({'pt_no':pt[j], 'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'dt1':dt1,
            'dt2':dt2,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }
        if bval=='Proceed':
            axle_no=request.POST.get('axle_no')
            ob1=list(AxleWheelPressing.objects.filter(axle_no=axle_no).values('dispatch_to'))
            l=len(ob1)
            ob3=list(AxleWheelPressing.objects.filter(axle_no=axle_no).values('date','loco_type','axle_no','wheelno_de','wheelno_nde','axle_no','bo_no','inspect_date','inspector_name'))
            c=ob1[0]['dispatch_to']
           
            ob2=[]
            ll1=0
            ll2=0
            if l>0 and c=="Inspected" :
                ob2=list(AxleWheelPressing.objects.filter(axle_no=axle_no).values('loco_type','axle_no','wheelno_de','wheelno_nde','bullgear_make','bullgear_no','wheel_de_make','wheel_nde_make','wheel_nde_pressure','wheel_de_pressure','axle_make','msu_unit_no','bullgear_pressure','msu_unit_make','axle_box_node','axle_box_makede','axle_box_clearancede','axle_box_nonde','axle_box_makende','axle_box_clearancende','msu_bearing_de_make','msu_bearing_nde_make','cru_bearing_no_de','cru_bearing_make_de','cru_bearing_pressure_de','cru_bearing_no_nde','cru_bearing_make_nde','cru_bearing_pressure_nde','inspect_date','inspector_name'))
                ll1=len(ob2)
                ll2=0
                if ll1>0:
                    for i in range(0,ll1):
                        dd=ob2[i]['inspect_date']
                        if dd!=None:
                            s=dd.split('-')
                            month=s[1]
                            day=s[2]
                            year=s[0]
                            dd2=day + '-' + month + '-' + year
                            ob2[i].update({'inspect_date':dd2})
                        else:
                            ob2[i].update({'inspect_date':None})
               
            elif l>0 and c=="HHP_Inspected" :
                ob2=list(AxleWheelPressing.objects.filter(axle_no=axle_no).values('loco_type','axle_no','wheelno_de','wheelno_nde','bullgear_make','bullgear_no','wheel_de_make','wheel_nde_make','wheel_nde_pressure','wheel_de_pressure','axle_make','msu_unit_no','bullgear_pressure','msu_unit_make','axle_box_node','axle_box_makede','axle_box_clearancede','axle_box_nonde','axle_box_makende','axle_box_clearancende','msu_bearing_de_make','msu_bearing_nde_make','cru_bearing_no_de','cru_bearing_make_de','cru_bearing_pressure_de','cru_bearing_no_nde','cru_bearing_make_nde','cru_bearing_pressure_nde','journal_no_de','journal_make_de','journal_no_nde','journal_make_nde','inspect_date','inspector_name'))
                ll2=len(ob2)
                ll1=0
                if ll2>0:
                    for i in range(0,ll2):
                        dd=ob2[i]['inspect_date']
                        if dd!=None:
                            s=dd.split('-')
                            month=s[1]
                            day=s[2]
                            year=s[0]
                            dd2=day + '-' + month + '-' + year
                            ob2[i].update({'inspect_date':dd2})
                        else:
                            ob2[i].update({'inspect_date':None})
            context={
                'nav':nav,
                'subnav':subnav,
                'usermaster':usermaster,
                'ip':get_client_ip(request),
                'sub':11,
                'ob1':ob1,
                'ob2':ob2,
                'ob3':ob3,
                'l':l,
                'll1':ll1,
                'll2':ll2,
            }
        if bval=='Proceed3':
            dt1=request.POST.get('datel1')
            dt2=request.POST.get('datel2')
            s1 = dt1.split('-')
            s2 = dt2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            datell1 =  year1 + "-" + month1 + "-" + day1
           
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            datell2 =  year2 + "-" + month2 + "-" + day2
            ob1=AxleWheelPressing.objects.filter(inspect_date__range=(datell1,datell2)).values('loco_type','axle_no','wheelno_de','wheelno_nde','bullgear_make','bullgear_no','wheel_de_make','wheel_nde_make','wheel_nde_pressure','wheel_de_pressure','axle_make','msu_unit_no','bullgear_pressure','msu_unit_make','axle_box_node','axle_box_makede','axle_box_clearancede','axle_box_nonde','axle_box_makende','axle_box_clearancende','msu_bearing_de_make','msu_bearing_nde_make','cru_bearing_no_de','cru_bearing_make_de','cru_bearing_pressure_de','cru_bearing_no_nde','cru_bearing_make_nde','cru_bearing_pressure_nde','journal_no_de','journal_make_de','journal_no_nde','journal_make_nde','inspect_date','inspector_name')
            l=len(ob1)
            ll=len(ob1)
            if ll>0:
                for i in range(0,ll):
                    dd=ob1[i]['inspect_date']
                    if dd!=None:
                        s=dd.split('-')
                        month=s[1]
                        day=s[2]
                        year=s[0]
                        dd2=day + '-' + month + '-' + year
                        ob1[i].update({'inspect_date':dd2})
                    else:
                        ob1[i].update({'inspect_date':None})
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':5,
            'ob1':ob1,
            'dt1':dt1,
            'dt2':dt2,
            'l':l,
            }
        if bval=='Proceed10':
            dt1=request.POST.get('datea')
            s = dt1.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(AxleWheelPressing.objects.filter(inspect_date=date).values('loco_type','axle_no','wheelno_de','wheelno_nde','bullgear_make','bullgear_no','wheel_de_make','wheel_nde_make','wheel_nde_pressure','wheel_de_pressure','axle_make','msu_unit_no','bullgear_pressure','msu_unit_make','axle_box_node','axle_box_makede','axle_box_clearancede','axle_box_nonde','axle_box_makende','axle_box_clearancende','msu_bearing_de_make','msu_bearing_nde_make','cru_bearing_no_de','cru_bearing_make_de','cru_bearing_pressure_de','cru_bearing_no_nde','cru_bearing_make_nde','cru_bearing_pressure_nde','journal_no_de','journal_make_de','journal_no_nde','journal_make_nde','inspect_date','inspector_name'))
            l=len(ob1)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':8,
            'ob1':ob1,
            'dt1':dt1,
            'l':l,
            }
    return render(request,'TMS/axlepress.html',context)

@login_required
@role_required(urlpass='/pinionreport/')
def pinionreport(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context={
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=="Record of Loco Type (date wise)":
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':4,
            }
        if bval=='Record of Loco Type (date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':10,
            }
        if bval=='Pinion Pressing Detail':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':12,
            }
        if bval=='Proceed1':
            pt=[]
            pto=[]
            lt=[]
            lto=[]
            count=[]
            count1=[]
            myval=[]
            myval1=[]
            unique_myval=[]
            unique_myval1=[]
            c1=0
            c2=0
            dt=request.POST.get('datew')
            s = dt.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(PinionPressing.objects.filter(in_qty=date).values('loco_type'))
            ob2=list(PinionPressing.objects.filter(out_qty=date).values('loco_type'))   
            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range (0,len(lt)):
                for j in range(0,len(lt)):
                    if(lt[i]==lt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(lt)):
                myval.append({'loco_type':lt[i], 'count1':count[i],'count2':'0'})

            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(lto)):
                for j in range(0,len(lto)):
                    if(lto[i]==lto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0
            
            for i in range (0,len(lto)):
                 myval1.append({'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['loco_type']==myval[j]['loco_type']:
                        final.append({'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['loco_type'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['loco_type'] not in id:
                    final.append({'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)

            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'dt':dt,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }
        if bval=='Proceed2':
            pt=[]
            pto=[]
            lt=[]
            lto=[]
            count=[]
            count1=[]
            myval=[]
            myval1=[]
            unique_myval=[]
            unique_myval1=[]
            c1=0
            c2=0
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            s1 = dt1.split('-')
            s2 = dt2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            date1 =  year1 + "-" + month1 + "-" + day1
          
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            date2 =  year2 + "-" + month2 + "-" + day2
            ob1=list(PinionPressing.objects.filter(in_qty__range=(date1,date2)).values('loco_type'))
            ob2=list(PinionPressing.objects.filter(out_qty__range=(date1,date2)).values('loco_type'))
            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range (0,len(lt)):
                for j in range(0,len(lt)):
                    if(lt[i]==lt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(lt)):
                myval.append({'loco_type':lt[i], 'count1':count[i],'count2':'0'})

            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(lto)):
                for j in range(0,len(lto)):
                    if(lto[i]==lto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0
            
            for i in range (0,len(lto)):
                 myval1.append({'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['loco_type']==myval[j]['loco_type']:
                        final.append({'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['loco_type'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['loco_type'] not in id:
                    final.append({'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)

            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'dt1':dt1,
            'dt2':dt2,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }
        if bval=='Proceed3':
            dt=request.POST.get('datea')
            s1 = dt.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            datell1 =  year1 + "-" + month1 + "-" + day1
            ob1=list(PinionPressing.objects.filter(inspect_date=datell1).values('bo_no','pt_no','loco_type','date','axle_no','loco_type','tm_no','tm_make','pinion_no','pinion_make','pinion_travel','pinion_pressure_square_ram','pinion_pressure_triangle_glycerin','pinion_teeth_dist','blue_match','inspect_date'))
            l=len(ob1)
            ll=len(ob1)
            if ll>0:
                for i in range(0,ll):
                    dd=ob1[i]['inspect_date']
                    if dd!=None:
                        s=dd.split('-')
                        month=s[1]
                        day=s[2]
                        year=s[0]
                        dd2=day + '-' + month + '-' + year
                        ob1[i].update({'inspect_date':dd2})
                    else:
                        ob1[i].update({'inspect_date':None})
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':5,
            'ob1':ob1,
            'dt':dt,
            'l':l
            }
        if bval=='Proceed10':
            dt1=request.POST.get('datell1')
            dt2=request.POST.get('datell2')
            s1 = dt1.split('-')
            s2 = dt2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            datell1 =  year1 + "-" + month1 + "-" + day1
          
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            datell2 =  year2 + "-" + month2 + "-" + day2
            ob1=list(PinionPressing.objects.filter(inspect_date__range=(datell1,datell2)).values('bo_no','pt_no','loco_type','date','axle_no','loco_type','tm_no','tm_make','pinion_no','pinion_make','pinion_travel','pinion_pressure_square_ram','pinion_pressure_triangle_glycerin','pinion_teeth_dist','blue_match','inspect_date'))
            l=len(ob1)
            ll=len(ob1)
            if ll>0:
                for i in range(0,ll):
                    dd=ob1[i]['inspect_date']
                    if dd!=None:
                        s=dd.split('-')
                        month=s[1]
                        day=s[2]
                        year=s[0]
                        dd2=day + '-' + month + '-' + year
                        ob1[i].update({'inspect_date':dd2})
                    else:
                        ob1[i].update({'inspect_date':None})
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':11,
            'ob1':ob1,
            'dt1':dt1,
            'dt2':dt2,
            'l':l,
            }
        if bval=='Proceed':
            axle_no=request.POST.get('axle_no')
            ob1=list(PinionPressing.objects.filter(axle_no=axle_no,inspection_status=True).values('bo_no','pt_no','loco_type','date','axle_no','loco_type','tm_no','tm_make','pinion_no','pinion_make','pinion_travel','pinion_pressure_square_ram','pinion_pressure_triangle_glycerin','pinion_teeth_dist','blue_match','inspect_date'))
            l1=len(ob1)
            if l1>0:
                for i in range(0,l1):
                    dd=ob1[i]['inspect_date']
                    if dd!=None:
                        s=dd.split('-')
                        month=s[1]
                        day=s[2]
                        year=s[0]
                        dd2=day + '-' + month + '-' + year
                        ob1[i].update({'inspect_date':dd2})
                    else:
                        ob1[i].update({'inspect_date':None})
            ob2=list(PinionPressing.objects.filter(axle_no=axle_no,inspection_status=False).all())
            l2=len(ob2)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':13,
            'ob1':ob1,
            'ob2':ob2,
            'axle_no':axle_no,
            'l1':l1,
            'l2':l2
            }

    return render(request,'TMS/pinionreport.html',context)


@login_required
@role_required(urlpass='/bogiereport/')
def bogiereport(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context={
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Record of Loco Type (date wise)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':4,
            }
        if bval=='Record of Loco Type (date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':6,
            }
        if bval=='Consolidated Detail Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':8,
            }
        if bval=='Proceed1':
            pt=[]
            pto=[]
            lt=[]
            lto=[]
            fm=[]
            count=[]
            count1=[]
            myval=[]
            myval1=[]
            unique_myval=[]
            unique_myval1=[]
            c1=0
            c2=0
            dt=request.POST.get('datew')
            s = dt.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(BogieAssembly.objects.filter(in_date=date).values('pt_no','loco_type','frame_make'))
            ob2=list(BogieAssembly.objects.filter(out_qty=date).values('pt_no','loco_type','frame_make'))   
            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                pt.append(ob1[i]['pt_no'])
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range(0,len(ob1)):
                fm.append(ob1[i]['frame_make'])
            for i in range (0,len(pt)):
                for j in range(0,len(pt)):
                    if(pt[i]==pt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(pt)):
                myval.append({'pt_no':pt[i],'frame_make':fm[i],'loco_type':lt[i], 'count1':count[i],'count2':'0'})

            for i in range(0,len(ob2)):
                pto.append(ob2[i]['pt_no'])
            
            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(pto)):
                for j in range(0,len(pto)):
                    if(pto[i]==pto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0

            for i in range (0,len(pto)):
                myval1.append({'pt_no':pto[i],'frame_make':fm[i],'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['pt_no']==myval[j]['pt_no']:
                        final.append({'pt_no':pto[i],'frame_make':fm[i],'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['pt_no'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'pt_no':pto[i],'frame_make':fm[i],'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['pt_no'] not in id:
                    final.append({'pt_no':pt[j],'frame_make':fm[j],'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'ob1':ob1,
            'ob2':ob2,
            'dt':dt,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            s1 = dt1.split('-')
            s2 = dt2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            date1 =  year1 + "-" + month1 + "-" + day1
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            date2 =  year2 + "-" + month2 + "-" + day2
            ob1=BogieAssembly.objects.filter(in_date__range=(date1,date2)).values('pt_no','loco_type','frame_make')
            ob2=BogieAssembly.objects.filter(out_qty__range=(date1,date2)).values('pt_no','loco_type','frame_make')
            pt=[] 
            lt=[] 
            fm=[]
            pto=[]
            lto=[]
            myval=[]
            myval1=[]
            final=[]
            unique_final=[]
            count=[]
            count1=[]
            c1=0
            c2=0

            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                pt.append(ob1[i]['pt_no'])
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range(0,len(ob1)):
                fm.append(ob1[i]['frame_make'])
            for i in range (0,len(pt)):
                for j in range(0,len(pt)):
                    if(pt[i]==pt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(pt)):
                myval.append({'pt_no':pt[i],'frame_make':fm[i],'loco_type':lt[i], 'count1':count[i],'count2':'0'})
            
            for i in range(0,len(ob2)):
                pto.append(ob2[i]['pt_no'])
            
            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(pto)):
                for j in range(0,len(pto)):
                    if(pto[i]==pto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0

            for i in range (0,len(pto)):
                myval1.append({'pt_no':pto[i],'frame_make':fm[i],'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['pt_no']==myval[j]['pt_no']:
                        final.append({'pt_no':pto[i],'frame_make':fm[i],'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['pt_no'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'pt_no':pto[i],'frame_make':fm[i],'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['pt_no'] not in id:
                    final.append({'pt_no':pt[j],'frame_make':fm[j],'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'dt1':dt1,
            'dt2':dt2,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }
        if bval=='Proceed6':
            dt1=request.POST.get('datea')
            s = dt1.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(BogieAssembly.objects.filter(inspect_date=date).values('axle_no','axle_location','traction_motor_no','gear_case_no','gear_case_make','msu_unit_no','break_rigging_make','coil_spring_make','secondary_coil_make','sand_box_make','spheri_block_make','thrust_pad_make','break_cylinder_make','elastic_shop_make','horizontal_damper','lateral_damper','inspect_date'))
            l=len(ob1)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':5,
            'ob1':ob1,
            'dt1':dt1,
            'l':l,
            }
        if bval=='Proceed7':
            datea1=request.POST.get('datea1')
            datea2=request.POST.get('datea2')
            s1 = datea1.split('-')
            s2 = datea2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            datell1 =  year1 + "-" + month1 + "-" + day1
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            datell2 =  year2 + "-" + month2 + "-" + day2
            ob1=list(BogieAssembly.objects.filter(inspect_date__range=(datell1,datell2)).values('axle_no','axle_location','traction_motor_no','gear_case_no','gear_case_make','msu_unit_no','break_rigging_make','coil_spring_make','secondary_coil_make','sand_box_make','spheri_block_make','thrust_pad_make','break_cylinder_make','elastic_shop_make','horizontal_damper','lateral_damper','inspect_date'))
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':7,
            'ob1':ob1,
           
            'datea1':datea1, 
            'datea2':datea2,
            }
        if bval=='Proceed':
            bo_no=request.POST.get('bo_no')
            fs_no=request.POST.get('fs_no')
            ob1=list(BogieAssembly.objects.filter(bo_no=bo_no,frameserial_no=fs_no,dispatch_to='Inspected').values('break_cylinder_make','first_coilspring_make','break_rigging_make','motor_check','motor_date','lowering_check','lowering_date','dispatch_check','dispatch_check_date','loco_paper','locopaper_date','frameserial_no','pt_no','horizontal_damper','loco_type','first_axle','second_axle','third_axle','first_gearcase_no','second_gearcase_no','third_gearcase_no','first_back_lash','second_back_lash','third_back_lash','wheel_set_guide','gear_case_oil','lateral_damper','spheri_block_make','sand_box_make','elastic_shop_make','coil_spring_make','break_cylinder_make','date','first_vertical_r','first_vertical_l','first_horizontal_r','first_horizontal_l','second_vertical_r','second_vertical_l','second_horizontal_r','second_horizontal_l','third_vertical_r','third_vertical_l','third_horizontal_r','third_horizontal_l'))  
            l=len(ob1)
           
            if l>0 :
                ax1=ob1[0]['first_axle']
                ax2=ob1[0]['second_axle']
                ax3=ob1[0]['third_axle']
                tm1=list(PinionPressing.objects.filter(axle_no=ax1).values('tm_no','tm_make'))
                tm2=list(PinionPressing.objects.filter(axle_no=ax2).values('tm_no','tm_make'))
                tm3=list(PinionPressing.objects.filter(axle_no=ax3).values('tm_no','tm_make'))
                axle_box1=list(AxleWheelPressing.objects.filter(axle_no=ax1).values('axle_box_node'))
                tno1=tm1[0]['tm_no']
                tno2=tm2[0]['tm_no']
                tno3=tm3[0]['tm_no']
                tmake1=tm1[0]['tm_make']
                tmake2=tm2[0]['tm_make']
                tmake3=tm3[0]['tm_make']
                axle_box=axle_box1[0]['axle_box_node']
            ob2=list(BogieAssembly.objects.filter(bo_no=bo_no,frameserial_no=fs_no,dispatch_to='HHP_Inspected').values('first_coilspring_make','break_cylinder_make','motor_check','motor_date','lowering_check','lowering_date','dispatch_check','dispatch_check_date','loco_paper','locopaper_date','frameserial_no','pt_no','horizontal_damper','lateral_damper','loco_type','first_axle','second_axle','third_axle','first_gearcase_no','second_gearcase_no','third_gearcase_no','first_back_lash','second_back_lash','third_back_lash','wheel_set_guide','gear_case_oil','lateral_damper','spheri_block_make','sand_box_make','elastic_shop_make','coil_spring_make','break_cylinder_make','date','first_vertical_r','first_vertical_l','first_horizontal_r','first_horizontal_l','second_vertical_r','second_vertical_l','second_horizontal_r','second_horizontal_l','third_vertical_r','third_vertical_l','third_horizontal_r','third_horizontal_l'))  
            l2=len(ob2)
            if l2>0 :
                ax1=ob1[0]['first_axle']
                ax2=ob1[0]['second_axle']
                ax3=ob1[0]['third_axle']
                tm1=list(PinionPressing.objects.filter(axle_no=ax1).values('tm_no','tm_make'))
                tm2=list(PinionPressing.objects.filter(axle_no=ax2).values('tm_no','tm_make'))
                tm3=list(PinionPressing.objects.filter(axle_no=ax3).values('tm_no','tm_make'))
                axle_box1=list(AxleWheelPressing.objects.filter(axle_no=ax1).values('axle_box_node'))
                tno1=tm1[0]['tm_no']
                tno2=tm2[0]['tm_no']
                tno3=tm3[0]['tm_no']
                tmake1=tm1[0]['tm_make']
                tmake2=tm2[0]['tm_make']
                tmake3=tm3[0]['tm_make']
                axle_box=axle_box1[0]['axle_box_node']
            
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':9,
            'ob1':ob1,
            'l':l,
            'l2':l2,
           'ob2':ob2,
            'bo_no':bo_no,
            'fs_no':fs_no,
            'tno1':tno1,
            'tno2':tno2,
            'tno3':tno3,
            'tmake1':tmake1,
            'tmake2':tmake2,
            'tmake3':tmake3,
            'axle_box':axle_box
            }
    return render(request,'TMS/bogiereport.html',context)



def fetchloco(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('sels_no')
        myval1=list(WheelMachining.objects.filter(wheel_no=mysno).values('bo_no').distinct())
        myval2 = list(Batch.objects.filter(bo_no=myval1[0]['bo_no']).values('ep_type').distinct())
        myval3 = list(Code.objects.filter(code=myval2[0]['ep_type'],cd_type='11').values('alpha_1').distinct())
        return JsonResponse(myval3, safe = False)
    return JsonResponse({"success":False}, status=400)

def fetchaxleloco(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('sels_no')
        myval1=list(AxleMachining.objects.filter(axle_no=mysno).values('bo_no').distinct())
        myval2 = list(Batch.objects.filter(bo_no=myval1[0]['bo_no']).values('ep_type').distinct())
        myval3 = list(Code.objects.filter(code=myval2[0]['ep_type'],cd_type='11').values('alpha_1').distinct())
        return JsonResponse(myval3, safe = False)
    return JsonResponse({"success":False}, status=400)

def fetchwheelpartno(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('b_no')
        myval1=list(M2Doc.objects.filter(batch_no=mysno,f_shopsec='2304').values('rm_partno').distinct())
        myval2=''
        l=[]
        if len(myval1)>0:
                for i in range(0,len(myval1)):
                    l.append(myval1[i]['rm_partno'])
        if len(l)!=0:
            myval2 = list(Part.objects.filter(partno__in=l,des__startswith='WHEE').values('partno').distinct())
            msg=myval2[0]['partno']
        else:
             msg="false"
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def fetchaxlepartno(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('b_no')
        myval1=list(M2Doc.objects.filter(batch_no=mysno,f_shopsec='2304').values('rm_partno').distinct())
        myval2=''
        l=[]
        if len(myval1)>0:
                for i in range(0,len(myval1)):
                    l.append(myval1[i]['rm_partno'])
        if len(l)!=0:
            myval2 = list(Part.objects.filter(partno__in=l,des__startswith='AXL').values('partno').distinct())
            ll=len(myval2)
            if ll>0:
                msg=myval2[0]['partno']
            else :
                msg="false"
        else:
             msg="false"
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def fetchwheeleditpartno(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('b_no')
        myval1=list(WheelMachining.objects.filter(wheel_no=mysno).values('wheelp_no').distinct())
        myval2=myval1[0]['wheelp_no']
        return JsonResponse(myval1, safe = False)
    return JsonResponse({"success":False}, status=400)

def fetchaxleeditpartno(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('b_no')
        myval1=list(AxleMachining.objects.filter(axle_no=mysno).values('axlep_no').distinct())
        myval2=myval1[0]['axlep_no']
        return JsonResponse(myval1, safe = False)
    return JsonResponse({"success":False}, status=400)

def FetchWheelInspectDetail(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('sels_no')
        myval1=list(WheelMachining.objects.filter(wheel_no=mysno,dispatch_to="Inspected").values('ustwhl','ustwhl_date','ustwhl_status','hub_lengthwhl','tread_diawhl','rim_thicknesswhl','bore_diawhl','inspector_namewhl','datewhl').distinct())
        l=len(myval1)
        if l>0 :
            msg=myval1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def FetchAxleInspectDetail(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('sels_no')
        myval1=list(AxleMachining.objects.filter(axle_no=mysno,dispatch_to="Inspected").values('ustaxle','ustaxle_date','ustaxle_status','axlelength','journalaxle','throweraxle','wheelseataxle','gearseataxle','collaraxle','dateaxle','bearingaxle','abutmentaxle','inspector_nameaxle','journal_surfacefinishGE','wheelseat_surfacefinishGE','gearseat_surfacefinishGE','journal_surfacefinishFE','wheelseat_surfacefinishFE','gearseat_surfacefinishFE','journalaxlende','throweraxlende','wheelseataxlende','collaraxlende').distinct())
        l=len(myval1)
        if l>0 :
            msg=myval1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def FetchPressInspectDetail(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('sels_no')
        myval1=list(AxleWheelPressing.objects.filter(axle_no=mysno,dispatch_to="Inspected").values('wheel_distance','axialplay_de','axialplay_nde','wheel_de_pressure','wheelno_de','wheelno_nde','bullgear_make','bullgear_no','inspector_name','wheel_de_make','wheel_nde_make','wheel_nde_pressure','axle_make','msu_unit_no','bullgear_pressure','msu_unit_make','axle_box_node','axle_box_makede','axle_box_clearancede','axle_box_nonde','axle_box_makende','axle_box_clearancende','msu_bearing_de_make','msu_bearing_nde_make','cru_bearing_no_de','cru_bearing_make_de','cru_bearing_pressure_de','cru_bearing_no_nde','cru_bearing_make_nde','cru_bearing_pressure_nde','inspect_date','wheel_nde_pressure').distinct())
        l=len(myval1)
        if l>0 :
            msg=myval1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def chkaw(request):
    if request.method=="GET" and request.is_ajax():
        myax = request.GET.get('axle_no')
        whl_de = request.GET.get('whlde')
        whl_nde = request.GET.get('whlnde')
        axle=list(AxleMachining.objects.filter(axlefitting_status=False,axleinspection_status=True,axle_no=myax).values('axle_no'))
        whlde=list(WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True,wheel_no=whl_de).values('wheel_no'))
        whlnde=list(WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True,wheel_no=whl_nde).values('wheel_no'))
        if (len(axle)<1):
            msg=["wrongaxle"]
        elif (len(whlde)<1):
            msg=["wrongwheelde"]
        elif (len(whlnde)<1):
            msg=["wrongwheelnde"]
        else:
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def wheelpress_inspectsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(AxleWheelPressing.objects.filter(axle_no=mysno).values('wheelno_de','wheelno_nde','axle_no','bullgear_no','bullgear_make'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def FetchPressInspectHHPDetail(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('sels_no')
        myval2=list(AxleWheelPressing.objects.filter(axle_no=mysno,dispatch_to="HHP_Inspected").values('wheel_de_pressure','wheel_distance','axialplay_de','axialplay_nde','wheel_de_pressure','wheelno_de','wheelno_nde','bullgear_make','bullgear_no','inspector_name','wheel_de_make','wheel_nde_make','wheel_nde_pressure','axle_make','msu_unit_no','bullgear_pressure','msu_unit_make','axle_box_node','axle_box_makede','axle_box_clearancede','axle_box_nonde','axle_box_makende','axle_box_clearancende','msu_bearing_de_make','msu_bearing_nde_make','cru_bearing_no_de','cru_bearing_make_de','cru_bearing_pressure_de','cru_bearing_no_nde','cru_bearing_make_nde','cru_bearing_pressure_nde','inspect_date','wheel_nde_pressure','journal_no_de','journal_make_de','journal_no_nde','journal_make_nde').distinct())
        l1=len(myval2)
        if l1>0 :
            msg=myval2
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def FetchPinionInspectDetail(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('sels_no')
        myval2=list(PinionPressing.objects.filter(axle_no=mysno,dispatch_to="Inspected").values('pinion_pressure_triangle_glycerin','pinion_pressure_square_ram','pinion_teeth_dist','pinion_no','pinion_make','pinion_pressure_triangle_glycerin','pinion_travel','blue_match','inspect_date').distinct())
        l1=len(myval2)
        if l1>0 :
            msg=myval2
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)


def FetchTmnoBogie(request):
    if request.method=="GET" and request.is_ajax():
        tm01=request.GET.get('f')
        tm02=request.GET.get('s')
        tm03=request.GET.get('t')
        myval1=(PinionPressing.objects.filter(axle_no=tm01).values('tm_no'))
        myval2=(PinionPressing.objects.filter(axle_no=tm02).values('tm_no'))
        myval3=(PinionPressing.objects.filter(axle_no=tm03).values('tm_no'))
        # myval=[{myval1},{myval2},{myval3}]
        myval=[]
        myval.append(myval1[0]["tm_no"])
        myval.append(myval2[0]["tm_no"])
        myval.append(myval3[0]["tm_no"])
        if (len(myval)>0) :
            msg=myval            
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def FetchBogieInspectDetail(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('sels_no')
        myval=list(BogieAssembly.objects.filter(frameserial_no=mysno,inspection_status=False).values('first_axle','second_axle','third_axle','loco_type').distinct())
        myval2=list(BogieAssembly.objects.filter(frameserial_no=mysno,dispatch_to="Inspected",inspection_status=True).values('torque_support','break_cylinder_make','inspect_date','first_axle','first_coilspring_make','first_gearcase_no','first_gearcase_make','first_back_lash','first_vertical_r','first_vertical_l','first_horizontal_r','first_horizontal_l','second_axle','second_coilspring_make','second_gearcase_no','second_gearcase_make','second_back_lash','second_vertical_r','second_vertical_l','second_horizontal_r','second_horizontal_l','third_axle','third_coilspring_make','third_gearcase_no','third_gearcase_make','third_back_lash','third_vertical_r','third_vertical_l','third_horizontal_r','third_horizontal_l','wheel_set_guide','gear_case_oil','break_rigging_make','sand_box_make','spheri_block_make','elastic_shop_make','horizontal_damper','inspect_date','motor_check','motor_date','lowering_check','lowering_date','dispatch_check','dispatch_check_date','loco_paper','locopaper_date','first_axle','second_axle','third_axle','loco_type').distinct())
        if (len(myval)>0) :
            msg=myval
        elif (len(myval2)>0) :
            msg=myval2
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def FetchBogieInspectHHPDetail(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('sels_no')
        myval2=list(BogieAssembly.objects.filter(frameserial_no=mysno,dispatch_to="HHP_Inspected").values('first_secondary_coilspring_make','second_secondary_coilspring_make','third_secondary_coilspring_make','h_plate','first_axle','first_coilspring_make','first_gearcase_no','first_gearcase_make','first_back_lash','first_vertical_r','first_vertical_l','first_horizontal_r','first_horizontal_l','second_axle','second_coilspring_make','second_gearcase_no','second_gearcase_make','second_back_lash','second_vertical_r','second_vertical_l','second_horizontal_r','second_horizontal_l','third_axle','third_coilspring_make','third_gearcase_no','third_gearcase_make','third_back_lash','third_vertical_r','third_vertical_l','third_horizontal_r','third_horizontal_l','wheel_set_guide','gear_case_oil','break_cylinder_make','break_rigging_make','sand_box_make','spheri_block_make','elastic_shop_make','lateral_damper','inspect_date','motor_check','motor_date','lowering_check','lowering_date','dispatch_check','dispatch_check_date','loco_paper','locopaper_date','first_axle','second_axle','third_axle').distinct())
        l1=len(myval2)
        if l1>0 :
            msg=myval2
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def wheelreport_validate(request):
    if request.method=="GET" and request.is_ajax():
        wheel_no = request.GET.get('wheel_no')
        ob1=list(WheelMachining.objects.filter(wheel_no=wheel_no).values('wheel_no','loco_type','date','bo_no','wheel_heatcaseno','ustwhl','hub_lengthwhl','tread_diawhl','rim_thicknesswhl','bore_diawhl','inspector_namewhl','datewhl'))
        l=len(ob1)
        if l>0 :
            msg=ob1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)  

def axlereport_validate(request):
    if request.method=="GET" and request.is_ajax():
        axle_no = request.GET.get('axle_no')
        ob1=list(AxleMachining.objects.filter(axle_no=axle_no).values('axle_no'))
        l=len(ob1)
        if l>0 :
            msg=ob1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400) 


def axlepressreport_validate(request):
    if request.method=="GET" and request.is_ajax():
        axle_no = request.GET.get('axle_no')
        ob1=list(AxleWheelPressing.objects.filter(axle_no=axle_no).values('axle_no'))
        l=len(ob1)
        if l>0 :
            msg=ob1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def pinionaxle_validate(request):
    if request.method=="GET" and request.is_ajax():
        axle_no = request.GET.get('axle_no')
        ob1=list(PinionPressing.objects.filter(axle_no=axle_no).values('axle_no'))
        l=len(ob1)
        if l>0 :
            msg=ob1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def bogiereportbono_validate(request):
    if request.method=="GET" and request.is_ajax():
        bo_no = request.GET.get('bo_no')
        ob1=list(BogieAssembly.objects.filter(bo_no=bo_no).values('bo_no'))
        l=len(ob1)
        if l>0 :
            msg=ob1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400) 

def bogiereportfsno_validate(request):
    if request.method=="GET" and request.is_ajax():
        fs_no = request.GET.get('fs_no')
        ob1=list(BogieAssembly.objects.filter(frameserial_no=fs_no).values('frameserial_no'))
        l=len(ob1)
        if l>0 :
            msg=ob1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400) 

def firstaxle(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('first_axle')
        myval = list(PinionPressing.objects.filter(inspection_status=True).values('axle_no').exclude(axle_no=mybo))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def secondaxle(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('first_axle')
        mybb = request.GET.get('second_axle')
        myval = list(PinionPressing.objects.filter(inspection_status=True).values('axle_no').exclude(Q(axle_no=mybo)|Q(axle_no=mybb)))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def FetchBogieDetail(request):
    if request.method=="GET" and request.is_ajax():
        mysno = request.GET.get('sels_no')
        myval2=list(BogieAssembly.objects.filter(frameserial_no=mysno).values('first_axle','second_axle','third_axle','loco_type').distinct())
        msg=myval2
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def uniquewheel(request):
    if request.method=="GET" and request.is_ajax():
        wheel_no = request.GET.get('wheel_no')
        ob1=list(WheelMachining.objects.filter(wheel_no=wheel_no).values('bo_no'))
        l=len(ob1)
        if l==0 :
            msg=["true"]
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def uniqueaxle(request):
    if request.method=="GET" and request.is_ajax():
        axle_no = request.GET.get('axle_no')
        ob1=list(AxleMachining.objects.filter(axle_no=axle_no).values('bo_no'))
        l=len(ob1)
        if l==0 :
            msg=["true"]
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def uniquebullgear(request):
    if request.method=="GET" and request.is_ajax():
        bullgear_no = request.GET.get('bullgear_no')
        ob1=list(AxleWheelPressing.objects.filter(bullgear_no=bullgear_no).values('bo_no'))
        l=len(ob1)
        if l==0 :
            msg=["true"]
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def uniquetm(request):
    if request.method=="GET" and request.is_ajax():
        tm_no = request.GET.get('tm_no')
        ob1=list(PinionPressing.objects.filter(tm_no=tm_no).values('bo_no'))
        l=len(ob1)
        if l==0 :
            msg=["true"]
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def uniquepinion(request):
    if request.method=="GET" and request.is_ajax():
        pinion_no = request.GET.get('pinion_no')
        ob1=list(PinionPressing.objects.filter(pinion_no=pinion_no).values('bo_no'))
        l=len(ob1)
        if l==0 :
            msg=["true"]
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def uniqueframeserial(request):
    if request.method=="GET" and request.is_ajax():
        frameserial_no = request.GET.get('frameserial_no')
        ob1=list(BogieAssembly.objects.filter(frameserial_no=frameserial_no).values('bo_no'))
        l=len(ob1)
        if l==0 :
            msg=["true"]
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def validate_axlepress_inspect(request):
    if request.method=="GET" and request.is_ajax():
        sels_no = request.GET.get('sels_no')
        ob1=list(AxleWheelPressing.objects.filter(axle_no=sels_no).values('loco_type'))
       
        return JsonResponse(ob1, safe = False)
    return JsonResponse({"success":False}, status=400)

def validate_pinionpress_inspect(request):
    if request.method=="GET" and request.is_ajax():
        sels_no = request.GET.get('sels_no')
        ob1=list(PinionPressing.objects.filter(axle_no=sels_no).values('loco_type'))
        
        return JsonResponse(ob1, safe = False)
    return JsonResponse({"success":False}, status=400)

def fetch_axlemake(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        ax_make=list(AxleMachining.objects.filter(axle_no=mysno).values('axle_make'))
        
        return JsonResponse(ax_make, safe = False)
    return JsonResponse({"success":False}, status=400)


    
@login_required
@role_required(urlpass='/machining_of_air_box/')
def insert_machining_of_air_box(request):
    
    rolelist=(g.usermaster).role.split(", ")
    
    obj2=MachiningAirBox.objects.all().filter(dispatch_status=False).order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=MachiningAirBox.objects.filter(dispatch_status=False).values('sno')
    my_context={
       'object':obj2,
       'nav':g.nav,
       'subnav':g.subnav,
       'usermaster':g.usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mysno':mysno,
       }
    if request.method=="POST":
        
        once=request.POST.get('once')
    
        submit=request.POST.get('submit')
        if submit=='Save':
        
            bo_no=request.POST.get('bo_no')
            bo_date=request.POST.get('bo_date')
            pt_no=request.POST.get('pt_no')
            bo_qty=request.POST.get('bo_qty')
            date=request.POST.get('date')
            loco_type=request.POST.get('locos')
            airbox_sno=request.POST.get('airbox_sno')
            airbox_make=request.POST.get('airbox_make')
            in_qty=request.POST.get('in_qty')
            out_qty=request.POST.get('out_qty')
            if bo_no and bo_date and pt_no and bo_qty and date and loco_type and airbox_sno and airbox_make and in_qty and out_qty:
               obj=MachiningAirBox.objects.create()
               obj.bo_no=bo_no
               obj.bo_date=bo_date
               obj.bo_qty=bo_qty
               obj.pt_no=pt_no
               obj.date=date
               obj.loco_type=loco_type
               obj.airbox_sno=airbox_sno
               obj.airbox_make=airbox_make
               obj.in_qty=in_qty
               obj.out_qty=out_qty
               obj.save()
               messages.success(request, 'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=MachiningAirBox.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='save':
    
            sno=int(request.POST.get('editsno'))
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            pt_no=request.POST.get('editpt_no')
            bo_qty=request.POST.get('editbo_qty')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            airbox_sno=request.POST.get('editairbox_sno')
            airbox_make=request.POST.get('editairbox_make')
            in_qty=request.POST.get('editin_qty')
            out_qty=request.POST.get('editout_qty')
            if bo_no and bo_date and pt_no and bo_qty and date and loco_type and airbox_sno and airbox_make and in_qty and out_qty:
               MachiningAirBox.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,pt_no=pt_no,bo_qty=bo_qty,date=date,loco_type=loco_type,airbox_sno=airbox_sno,airbox_make=airbox_make,in_qty=in_qty,out_qty=out_qty)
               messages.success(request, 'Successfully Edited!')
            else:
               messages.error(request,"Please Enter S.No.!")

        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dispatch_date=request.POST.get('dispatch_date')
            dislocos=request.POST.get('dislocos')
            if sno and dispatch_date and dislocos:
                MachiningAirBox.objects.filter(sno=sno).update(dispatch_date=dispatch_date,dispatch_to=dislocos,dispatch_status=True)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            first=int(request.POST.get('delsno'))
            if first:
                MachiningAirBox.objects.filter(sno=first).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        return HttpResponseRedirect("/machining_of_air_box/")

    return render(request,"TMS/machining_of_air_box.html",my_context)

def airbox_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)





@login_required
@role_required(urlpass='/miscellaneous_section/')
def miscellaneous_section(request):
   
    rolelist=(g.usermaster).role.split(", ")
    nav=dynamicnavbar(request,rolelist)
   
    obj2=MiscellSection.objects.all().filter(dispatch_status=False).order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=MiscellSection.objects.filter(dispatch_status=False).values('sno')
    my_context={
       'object':obj2,
       'nav':g.nav,
       'subnav':g.subnav,
        'usermaster':g.usermaster,
        'ip':get_client_ip(request),
        'mybo':mybo,
        'mysno':mysno,
       }
    if request.method=="POST":
        
        once=request.POST.get('once')
        submit=request.POST.get('submit')
        if submit=='Save':
        
            first=request.POST.get('bo_no')
            second=request.POST.get('bo_date')
            pt_no=request.POST.get('pt_no')
            bo_qty=request.POST.get('bo_qty')
            third=request.POST.get('date')
            fourth=request.POST.get('locos')
            fifth=request.POST.get('shaft_m')
            sixth=request.POST.get('in_qty')
            seventh=request.POST.get('out_qty')
            if first and second and pt_no and bo_qty and third and fourth and fifth and sixth and seventh:
                obj=MiscellSection.objects.create()
                obj.bo_no=first
                obj.bo_date=second
                obj.bo_qty=bo_qty
                obj.pt_no=pt_no
                obj.date=third
                obj.loco_type=fourth
                obj.shaft_m=fifth
                obj.in_qty=sixth
                obj.out_qty=seventh
                obj.save()
                messages.success(request, 'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=MiscellSection.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='save':
        
            sno=int(request.POST.get('editsno'))
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            pt_no=request.POST.get('editpt_no')
            bo_qty=request.POST.get('editbo_qty')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            shaft_m=request.POST.get('editshaft_m')
            in_qty=request.POST.get('editin_qty')
            out_qty=request.POST.get('editout_qty')
            if sno and bo_no and pt_no and bo_qty and bo_date and date and loco_type and shaft_m and in_qty and out_qty:
                MiscellSection.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,shaft_m=shaft_m,in_qty=in_qty,out_qty=out_qty)
                messages.success(request, 'Successfully Edited!')
            else:
               messages.error(request,"Please Enter S.No.!")
        
        if submit=="Dispatch":
            
            first=int(request.POST.get('dissno'))
            second=request.POST.get('dislocos')
            dispatch_date=request.POST.get('dispatch_date')
            if first and dispatch_date and second:
               MiscellSection.objects.filter(sno=first).update(dispatch_date=dispatch_date,dispatch_to=second,dispatch_status=True)
               messages.success(request, 'Successfully Dispatched!')
            else:
               messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            first=int(request.POST.get('delsno'))
            if first:
                MiscellSection.objects.filter(sno=first).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        return HttpResponseRedirect("/miscellaneous_section/")

    return render(request,"TMS/miscellaneous_section.html",my_context)



def miscell_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def miscell_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(MiscellSection.objects.filter(sno=mysno).values('bo_no','bo_date','pt_no','bo_qty','shaft_m','in_qty','out_qty','date','loco_type'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400) 


def pinion_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','batch_qty','part_no'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)
        
def pinion_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(PinionPressing.objects.filter(tm_no=mysno).values('bo_no','bo_date','loco_type','date','tm_make','tm_no','pt_no','bo_qty','in_qty','out_qty'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400) 
    
def airbox_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(MachiningAirBox.objects.filter(sno=mysno).values('bo_no','bo_date','airbox_sno','airbox_make','in_qty','out_qty','date','loco_type','pt_no','bo_qty'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400) 


def axlepress_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(AxleWheelPressing.objects.filter(axle_no=mysno).values('bo_no','bo_date','loco_type','date','axle_no','wheelno_de','wheelno_nde','bullgear_no','bullgear_make','pt_no','bo_qty','in_qty','out_qty'))
        AxleMachining.objects.filter(axle_no=myval[0]['axle_no']).update(axlefitting_status=False)
        WheelMachining.objects.filter(wheel_no=myval[0]['wheelno_de']).update(wheelfitting_status=False)
        WheelMachining.objects.filter(wheel_no=myval[0]['wheelno_nde']).update(wheelfitting_status=False)
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)  

def wheelnde(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('wheel_no')
        myval = list(WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no').exclude(wheel_no=mybo))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)



def uniqueframeserial(request):
    if request.method=="GET" and request.is_ajax():
        frameserial_no = request.GET.get('frameserial_no')
        ob1=list(BogieAssembly.objects.filter(frameserial_no=frameserial_no).values('bo_no'))
        l=len(ob1)
        if l==0 :
            msg=["true"]
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)


def bogieassemb_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def bogieassemb_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(BogieAssembly.objects.filter(frameserial_no=mysno).values('bo_no','bo_date','pt_no','bo_qty','loco_type','date','frameserial_no','frame_make','frame_type','in_date','out_qty','first_axle','second_axle','third_axle','first_axle_location','second_axle_location','third_axle_location'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)
def axlepress_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def axle_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def axle_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(AxleMachining.objects.filter(axle_no=mysno).values('bo_no','bo_date','pt_no','bo_qty','in_qty','out_qty','date','axlep_no','loco_type','axle_no','axle_make','axle_heatcaseno'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)
 

def whl_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def whl_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(WheelMachining.objects.filter(wheel_no=mysno).values('bo_no','bo_date','pt_no','bo_qty','in_qty','out_qty','date','wheel_no','wheel_make','loco_type','wheel_heatcaseno','wheelp_no'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(urlpass='/airboxreport/')
def airboxreport(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context={
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Proceed1':
            dt=request.POST.get('datew')
            ob1=MachiningAirBox.objects.filter(in_qty=dt).values('sno','pt_no')
            ob2=MachiningAirBox.objects.filter(out_qty=dt).values('sno','pt_no')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'ob1':ob1,
            'ob2':ob2,
            'dt':dt,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            ob1=MachiningAirBox.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','in_qty').order_by('in_qty')
            ob2=MachiningAirBox.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }

    return render(request,'TMS/airboxreport.html',context)

@login_required
@role_required(urlpass='/miscreport/')
def miscreport(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context={
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Proceed1':
            dt=request.POST.get('datew')
            ob1=MiscellSection.objects.filter(in_qty=dt).values('sno','pt_no')
            ob2=MiscellSection.objects.filter(out_qty=dt).values('sno','pt_no')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'ob1':ob1,
            'ob2':ob2,
            'dt':dt,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            ob1=MiscellSection.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','in_qty').order_by('in_qty')
            ob2=MiscellSection.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }

    return render(request,'TMS/miscreport.html',context)



@login_required
@role_required(urlpass='/axlereport/')
def axlereport(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context={
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Axle Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':10,
            }
        if bval=='Axle Record of Loco Type (date wise)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':6,
            }
        if bval=='Axle Record of Loco Type (date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':7,
            }
        if bval=='Proceed1':
                    
            pt=[]
            pto=[]
            lt=[]
            lto=[]
            count=[]
            count1=[]
            myval=[]
            myval1=[]
            unique_myval=[]
            unique_myval1=[]
            c1=0
            c2=0
            dt=request.POST.get('datew')
            s = dt.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(AxleMachining.objects.filter(in_qty=date).values('pt_no','loco_type','axle_no'))
            ob2=list(AxleMachining.objects.filter(out_qty=date).values('pt_no','loco_type','axle_no'))   
            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                pt.append(ob1[i]['pt_no'])
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range (0,len(pt)):
                for j in range(0,len(pt)):
                    if(pt[i]==pt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(pt)):
                myval.append({'pt_no':pt[i], 'loco_type':lt[i], 'count1':count[i],'count2':'0'})


            for i in range(0,len(ob2)):
                pto.append(ob2[i]['pt_no'])
            
            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(pto)):
                for j in range(0,len(pto)):
                    if(pto[i]==pto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0

            for i in range (0,len(pto)):
                myval1.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['pt_no']==myval[j]['pt_no']:
                        final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['pt_no'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['pt_no'] not in id:
                    final.append({'pt_no':pt[j], 'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)
            
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'dt':dt,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }
            
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            s1 = dt1.split('-')
            s2 = dt2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            date1 =  year1 + "-" + month1 + "-" + day1
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            date2 =  year2 + "-" + month2 + "-" + day2
            ob1=AxleMachining.objects.filter(in_qty__range=(date1,date2)).values('pt_no','loco_type')
            ob2=AxleMachining.objects.filter(out_qty__range=(date1,date2)).values('pt_no','loco_type')
            pt=[] 
            lt=[] 
            pto=[]
            lto=[]
            myval=[]
            myval1=[]
            final=[]
            unique_final=[]
            count=[]
            count1=[]
            c1=0
            c2=0

            len2=len(ob2)
            len1=len(ob1)
            for i in range(0,len(ob1)):
                pt.append(ob1[i]['pt_no'])
            for i in range(0,len(ob1)):
                lt.append(ob1[i]['loco_type'])
            for i in range (0,len(pt)):
                for j in range(0,len(pt)):
                    if(pt[i]==pt[j]):
                        c1=c1+1
                count.append(c1)
                c1=0
            for i in range (0,len(pt)):
                myval.append({'pt_no':pt[i], 'loco_type':lt[i], 'count1':count[i],'count2':'0'})
            
            for i in range(0,len(ob2)):
                pto.append(ob2[i]['pt_no'])
            
            for i in range(0,len(ob2)):
                lto.append(ob2[i]['loco_type'])
            
            for i in range (0,len(pto)):
                for j in range(0,len(pto)):
                    if(pto[i]==pto[j]):
                        c2=c2+1
                count1.append(c2)
                c2=0

            for i in range (0,len(pto)):
                myval1.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            id=[]
            final=[]
            unique_final=[]
            c=0
            for i in range(len(myval1)):
                for j in range(len(myval)):
                    if myval1[i]['pt_no']==myval[j]['pt_no']:
                        final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':myval[j]['count1'], 'count2':count1[i]})
                        id.append(myval1[i]['pt_no'])
                        c=1
                        break
                if c==1:
                    c=0
                    continue
                else:
                    final.append({'pt_no':pto[i], 'loco_type':lto[i],'count1':'0', 'count2':count1[i]})
            
            for j in range(len(myval)):
                if  myval[j]['pt_no'] not in id:
                    final.append({'pt_no':pt[j], 'loco_type':lt[j], 'count1':count[j],'count2':'0'})

            for x in final:  
                if x not in unique_final: 
                    unique_final.append(x)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'dt1':dt1,
            'dt2':dt2,
            'len1':len1,
            'len2':len2,
            'unique_final':unique_final,
            }

        if bval=='Proceed3':
            dt1=request.POST.get('date3')
            dt2=request.POST.get('date4')
            ob1=AxleMachining.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','axle_no','ustaxle_status','in_qty').order_by('in_qty')
            ob2=AxleMachining.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','axle_no','ustaxle_status','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':4,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }
        if bval=='Proceed6':
            datel=request.POST.get('datea')
            s = datel.split('-')
            month = s[1]
            day = s[0]
            year = s[2]
            date =  year + "-" + month + "-" + day
            ob1=list(AxleMachining.objects.filter(dateaxle=date).values('axle_no','bo_no','date','loco_type','axle_heatcaseno','ustaxle','axlelength','journalaxle','throweraxle','wheelseataxle','gearseataxle','collaraxle','journal_surfacefinishGE','wheelseat_surfacefinishGE','gearseat_surfacefinishGE','journal_surfacefinishFE','wheelseat_surfacefinishFE','gearseat_surfacefinishFE','collaraxlende','wheelseataxlende','throweraxlende','journalaxlende','bearingaxle','abutmentaxle','dateaxle','inspector_nameaxle'))
            l=len(ob1)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':8,
            'ob1':ob1,
            'datel':datel,
            }
        if bval=='Proceed7':
            datea1=request.POST.get('datea1')
            datea2=request.POST.get('datea2')
            s1 = datea1.split('-')
            s2 = datea2.split('-')
            month1 = s1[1]
            day1 = s1[0]
            year1 = s1[2]
            datell1 =  year1 + "-" + month1 + "-" + day1
            month2 = s2[1]
            day2 = s2[0]
            year2 = s2[2]
            datell2 =  year2 + "-" + month2 + "-" + day2
            ob1=list(AxleMachining.objects.filter(dateaxle__range=(datell1,datell2)).values('axle_no','bo_no','date','loco_type','axle_heatcaseno','ustaxle','axlelength','journalaxle','throweraxle','wheelseataxle','gearseataxle','collaraxle','journal_surfacefinishGE','wheelseat_surfacefinishGE','gearseat_surfacefinishGE','journal_surfacefinishFE','wheelseat_surfacefinishFE','gearseat_surfacefinishFE','collaraxlende','wheelseataxlende','throweraxlende','journalaxlende','bearingaxle','abutmentaxle','dateaxle','inspector_nameaxle'))
            ll=len(ob1)
            if ll>0:
                for i in range(0,ll):
                    dd=ob1[i]['dateaxle']
                    if dd!=None:
                        s=dd.split('-')
                        month=s[1]
                        day=s[2]
                        year=s[0]
                        dd2=day + '-' + month + '-' + year
                        ob1[i].update({'dateaxle':dd2})
                    else:
                        ob1[i].update({'dateaxle':None})
            l=len(ob1)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':9,
            'ob1':ob1,
            'datea1':datea1, 
            'datea2':datea2,
            }
        if bval=='Proceed':
            axle_no=request.POST.get('axle_no')
            ob1=list(AxleMachining.objects.filter(axle_no=axle_no).values('axle_no','bo_no','date','loco_type','axle_heatcaseno','ustaxle','axlelength','journalaxle','throweraxle','wheelseataxle','gearseataxle','collaraxle','journal_surfacefinishGE','wheelseat_surfacefinishGE','gearseat_surfacefinishGE','journal_surfacefinishFE','wheelseat_surfacefinishFE','gearseat_surfacefinishFE','collaraxlende','wheelseataxlende','throweraxlende','journalaxlende','bearingaxle','abutmentaxle','dateaxle','inspector_nameaxle'))
            ax=ob1[0]['axle_no']
            l=len(ob1)
            if l>0:
                for i in range(0,l):
                    dd=ob1[i]['dateaxle']
                    if dd!=None:
                        s=dd.split('-')
                        month=s[1]
                        day=s[2]
                        year=s[0]
                        dd2=day + '-' + month + '-' + year
                        ob1[i].update({'dateaxle':dd2})
                    else:
                        ob1[i].update({'dateaxle':None})
            ob2=list(AxleWheelPressing.objects.filter(axle_no=axle_no).values('wheelno_de','wheelno_nde','inspect_date','inspector_name'))
            l1=len(ob2)
            if l1>0:
                for i in range(0,l1):
                    dd3=ob2[i]['inspect_date']
                    if dd3!=None:
                        s1=dd3.split('-')
                        month1=s1[1]
                        day1=s1[2]
                        year1=s1[0]
                        dd4=day1 + '-' + month1 + '-' + year1
                        ob2[i].update({'inspect_date':dd4})
                    else:
                        ob2[i].update({'inspect_date':None})
            context={
                'nav':nav,
                'subnav':subnav,
                'usermaster':usermaster,
                'ip':get_client_ip(request),
                'sub':4,
                'ob1':ob1,
                'ob2':ob2,
                'l':l,
                'ax':ax,
                'l1':l1
            }

    return render(request,'TMS/axlereport.html',context)

  
def airbox_addloco(request):
    
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval=list(Batch.objects.filter(bo_no=mybo).values('ep_type').distinct())
        myvalue = list(Code.objects.filter(code=myval[0]['ep_type'],cd_type='11').values('alpha_1'))
        return JsonResponse(myvalue, safe = False)
    return JsonResponse({"success":False}, status=400)

def airbox_addeditloco(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('batchNo')
        myval=list(Batch.objects.filter(bo_no=mybo).values('ep_type').distinct())
        myvalue=[{'alpha_1':''}]
        if len(myval)!=0:
            myvalue = list(Code.objects.filter(code=myval[0]['ep_type'],cd_type='11').values('alpha_1'))
        return JsonResponse(myvalue, safe = False)
    return JsonResponse({"success":False}, status=400)











def validate_axleno(request):
    if request.method=="GET" and request.is_ajax():
        w=request.GET.get('x')
        axle_no = request.GET.get('axle_no')
        ob1=list(AxleMachining.objects.filter(axle_no=axle_no,axleinspection_status=True).values('axle_no'))
        l=len(ob1)
        if l>0 :
            msg=ob1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def validate_wheelnode(request):
    if request.method=="GET" and request.is_ajax():
        wheelno_de = request.GET.get('wheelno_de')
        w=request.GET.get('x')
        ob1=list(WheelMachining.objects.filter(wheel_no=wheelno_de,wheelinspection_status=True).values('wheel_no'))
        l=len(ob1)
        if l>0 and wheelno_de!=w:
            msg=ob1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)

def validate_wheelnonde(request):
    if request.method=="GET" and request.is_ajax():
        wheelno_nde = request.GET.get('wheelno_nde')
        w=request.GET.get('x')
        ob1=list(WheelMachining.objects.filter(wheel_no=wheelno_nde,wheelinspection_status=True).values('wheel_no'))
        l=len(ob1)
        if l>0 and wheelno_nde!=w:
            msg=ob1
        else :
            msg=["false"]
        return JsonResponse(msg, safe = False)
    return JsonResponse({"success":False}, status=400)







