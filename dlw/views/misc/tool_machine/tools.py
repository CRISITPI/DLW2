from dlw.views import *
import dlw.views.globals as g

def shop_section_tool(request):
    if request.method == "GET" and request.is_ajax():
        sh_no= request.GET.get('sh_no')
        obj=list(Shop.objects.filter(shop=str(sh_no)).values('sh_desc').distinct())
        return JsonResponse(obj,safe=False)
    
    return JsonResponse({"success":False}, status=400)
def tools1(request):
    if request.method == "GET" and request.is_ajax():
        emp= request.GET.get('wman')
        obj=list(empmast.objects.filter(empno=emp).values('empname','contactno').distinct())
        return JsonResponse(obj,safe=False)
    
    return JsonResponse({"success":False}, status=400)

def tools2(request):
    if request.method == "GET" and request.is_ajax():
        emp= request.GET.get('sse')
        obj=list(empmast.objects.filter(empno=emp).values('empname','contactno').distinct())
        return JsonResponse(obj,safe=False)    
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/Tools/')
def Tools(request):  
    tm=Shop.objects.all().values('shop').distinct() 
    tmp=[]
    for on in tm:
        tmp.append(on['shop'])

    tm1=list(empmast.objects.filter(Q(desig_longdesc__contains='WORKSHOP MANAGER')  | Q(desig_longdesc__contains='WORKSHOP  MANAGER')  ).values('empno').distinct())
    tmp1=[]
    for on in tm1:
        tmp1.append(on['empno'])
    tm2=list(empmast.objects.filter(desig_longdesc__contains='SECTION ENGINE').values('empno').distinct())
    
    tmp2=[]
    for on in tm2: 
        tmp2.append(on['empno'])
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'wm_shop':tmp1,
        'usermaster':g.usermaster,
        'shop':tmp2,
        'subnav':g.subnav,
    }
    if request.method =="POST":

        submitvalue = request.POST.get('submit')
     

        if submitvalue =='submit':
            form_no=request.POST.get('tool_form')
            sh_no=request.POST.get('sh_no')
            s_sec=request.POST.get('s_sec')
            date1=request.POST.get('date1')
            l_no=request.POST.get('l_no')
            new_req=request.POST.get('new_req')
            mod=request.POST.get('mod')
            add_req=request.POST.get('add_req')
            e_no=request.POST.get('e_no')
            d_no=request.POST.get('d_no')
            m_no=request.POST.get('m_no')
            des1=request.POST.get('des1')
            wm_name=request.POST.get('wm_name')
            wm_contact=request.POST.get('wm_contact')
            sse_name=request.POST.get('sse_name')
            sse_contact=request.POST.get('sse_contact')
            wman=request.POST.get('wman')
            sse=request.POST.get('sse')
            sup_name=request.POST.get('sup_name')
            sup_des=request.POST.get('sup_des')
            sup_mob=request.POST.get('sup_mob')
            obj=machine_tools.objects.filter(letter_no=l_no).distinct()
            b=obj
            if len(obj) == 0:
                machine_tools.objects.create(letter_no=str(l_no),shop_no=str(sh_no),shop_desc=str(s_sec),date=str(date1),new_requirement=str(new_req),modification=str(mod),additional=str(add_req),existing_drawing=e_no,component_drawing=str(d_no),machine_no=str(m_no),machine_description=str(des1),wsm_id=str(wman),sse_id=str(sse),wsm_name=str(wm_name),wsm_mobile=str(wm_contact),sse_name=str(sse_name),sse_mobile=str(sse_contact),name_supervisor=str(sup_name),desig_supervisor=str(sup_des),mobile_supervisor=str(sup_mob))
            else:
                machine_tools.objects.filter(letter_no=l_no).update(letter_no=str(l_no),shop_no=str(sh_no),shop_desc=str(s_sec),date=str(date1),new_requirement=str(new_req),modification=str(mod),additional=str(add_req),existing_drawing=e_no,component_drawing=str(d_no),machine_no=str(m_no),machine_description=str(des1),wsm_id=str(wman),sse_id=str(sse),wsm_name=str(wm_name),wsm_mobile=str(wm_contact),sse_name=str(sse_name),sse_mobile=str(sse_contact),name_supervisor=str(sup_name),desig_supervisor=str(sup_des),mobile_supervisor=str(sup_mob))
                
            hidtext=request.POST.get('hidtext')
            obj1 =list(mdescription.objects.values('id').filter(lno=l_no).distinct())
            if len(obj1) == 0:
                for i in range(2,int(hidtext)+1):                    
                    des=request.POST.get("des"+str(i))
                    quant=request.POST.get('quant'+str(i))
                    mdescription.objects.create(description=str(des),quantity=quant,lno=l_no)
            else:
                hidtext=request.POST.get('hidtext')
                for i in range(1,int(hidtext)):
                    des=request.POST.get('des'+str(i))
                    quant=request.POST.get('quant'+str(i))
                    mdescription.objects.filter(lno=l_no).update(description=str(des),quantity=quant)        
    
    return render(request,"MISC/TOOL&MACHINE/Tools.html",context)
