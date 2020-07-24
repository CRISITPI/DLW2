from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/M20view/')
def M20report(request):
    import datetime
    cyear = date.today().year
    
    hd1=list(holidaylist.objects.filter(holiday_year=cyear))
    tm=shop_section.objects.all().distinct('shop_code')
    tmp=[]
    for on in tm:
        tmp.append(on.shop_code)
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'hd':hd1,
        'lvdate':"dd-mm-yyyy",
        'usermaster': g.usermaster ,       
    }    
    if request.method == "POST":
            shop_sec = request.POST.get('shop_sec')
            lvdate=request.POST.get('lv_date') 
            sh_name=shop_section.objects.filter(shop_code=shop_sec).values('section_desc')
            shop_n=shop_sec[:-2]
            shop_sec = shop_sec[-2:] 
            m2=list(M20new.objects.filter(shop_sec__startswith=shop_sec,lv_date=datetime.datetime.strptime(lvdate,"%d-%m-%Y").date()).order_by('shop_sec'))
            data={
                'm2':m2,
                'shop_sec':shop_n,
                'lvdate':lvdate,
                'usermaster': g.usermaster ,
            }
            
            pdf = render_to_pdf('M20pdfc.html',data)
            return HttpResponse(pdf, content_type='application/pdf')
    return render(request, "MCARD/M20CARD/M20report.html", context)