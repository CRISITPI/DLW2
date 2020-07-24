
from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/tool_report/')
def tool_report(request):
     
    obj=Shop.objects.all().values('shop').distinct()
    temp=[]
    for i in obj:
            temp.append(i['shop'])
    
    context={
        'usermaster':g.usermaster,          
        'trlocation': temp,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'subnav':g.subnav,
        
    }
    return render(request,'MISC/TOOLREPORT/tool_report.html',context)


@login_required
@role_required(urlpass='/tool_reportedit/')
def tool_reportedit(request):
   
    wo_nop = empmast.objects.none()
    
    tool=list(toolmdata.objects.values())
    obj=Shop.objects.all().values('shop').distinct()
    temp=[]
    for i in obj:
            temp.append(i['shop'])
    context={
        'nav':g.nav,
        'ip':get_client_ip(request),
        'subnav':g.subnav,
        'tool':tool,
    }
    if request.method == "POST":       
        SubmitMultipleRowData = request.POST.get('SubmitMultipleRowData')
        dataForm = request.POST.get('dataForm')
        if SubmitMultipleRowData=="Submit":
            dataFormTemp  = request.POST.get('dataForm')
            TOOL_NUM=dataFormTemp.split(',')[0]
            context={
            'trlocation': temp,
            'nav':g.nav,
            'ip':get_client_ip(request),           
            'subnav':g.subnav,
            'TOOL_NUM' : TOOL_NUM,
            'dg_num':dataFormTemp.split(',')[1],
            'tl_desc':dataFormTemp.split(',')[2],
            'pl_num':dataFormTemp.split(',')[3],
            'sh_locn':dataFormTemp.split(',')[4],
            'tr_shopdesc':dataFormTemp.split(',')[5],
            'po_no':dataFormTemp.split(',')[7],
            'doe':dataFormTemp.split(',')[6],
            'make':dataFormTemp.split(',')[8],
            'model':dataFormTemp.split(',')[9],
            'cost':dataFormTemp.split(',')[10],
            'rangee':dataFormTemp.split(',')[11],
            'uom':dataFormTemp.split(',')[12],
            'cal_freq':dataFormTemp.split(',')[13],
            'acc_cri':dataFormTemp.split(',')[14],
            'cal_link':dataFormTemp.split(',')[15],
            'pro_tol':dataFormTemp.split(',')[16],
            'perror':dataFormTemp.split(',')[17],
            'merror':dataFormTemp.split(',')[18],
            'rsn':dataFormTemp.split(',')[19],
            'win':dataFormTemp.split(',')[21],
            'flag':dataFormTemp.split(',')[20],
            }
            return render(request,'MISC/TOOLREPORT/tool_report.html',context)
    return render(request,'MISC/TOOLREPORT/tool_reportedit.html',context)


