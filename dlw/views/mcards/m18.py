from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/m18view/')
def m18view(request):
    rolelist=(g.usermaster).role.split(", ")
    wo_nop = empmast.objects.none()
    tm=shop_section.objects.filter(shop_id=(g.usermaster).shopno).all()
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
    if(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'usermaster':g.usermaster,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'usermaster':g.usermaster,
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Print/Save':
            shopIncharge    = request.POST.get('shopIncharge')
            shop_sec        = request.POST.get('shop_sec')
            wo_no           = request.POST.get('wo_no')
            part_nop        = request.POST.get('part_nop')
            refNo           = request.POST.get('refNo')
            extraTimePartNo = request.POST.get('extraTimePartNo')
            reasonSpecialAllowance = request.POST.get('reasonSpecialAllowance')
            forSpecialAllowance    = request.POST.get('forSpecialAllowance')
            totalExtraTime        = request.POST.get('totalExtraTime')
            opno            = request.POST.get('opno')
            opdesc          = request.POST.get('opdesc')
            discription     = request.POST.get('discription')
            quantity        = request.POST.get('quantity')
            setExtraTime    = request.POST.get('setExtraTime')    
            setno           = request.POST.get('setno')  
            proReason           = request.POST.get('proReason')  

            m18.objects.create(shopIncharge=str(shopIncharge),shop_sec=str(shop_sec),wo_no=str(wo_no),part_nop=str(part_nop), refNo=str(refNo), extraTimePartNo=str(extraTimePartNo), reasonSpecialAllowance=str(reasonSpecialAllowance), forSpecialAllowance=str(forSpecialAllowance), totalExtraTime=str(totalExtraTime),opno=str(opno),opdesc=str(opdesc), discription=str(discription), quantity=str(quantity), setExtraTime=str(setExtraTime), setno=str(setno), proReason=str(proReason))
           
            emp_detail= emp_details.objects.filter(card_details='M26').values('email_id','mobileno')
            mob_temp=[]            
            for i in emp_detail:
                mob_temp.append(i['mobileno'])
            for j in range(len(mob_temp)):
                smsM18(mob_temp[j],"Dear Employee Extra Time Card(M18) has been created. Your Ref No.- "+refNo+".")                

            messages.success(request, 'Successfully Saved ! Your ref No is :'+refNo)
    return render(request,"MCARD/M18CARD/m18view.html",context)
