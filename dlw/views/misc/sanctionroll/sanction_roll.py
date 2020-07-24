from dlw.views import *
import dlw.views.globals as g


@login_required
@role_required(urlpass='/sanction_rollview/')

def sanction_rollview(request):
    import datetime
     
    tm=Shemp.objects.all().values('shopsec').distinct()
    tmp=[]
    for on in tm:
        tmp.append(on['shopsec'])
    context={
    'sub':0,
    'lenm' :2,
    'nav':g.nav,
    'ip':get_client_ip(request),
    'roles':tmp,
    'subnav':g.subnav,
    'usermaster':g.usermaster,
    }

    if(len(g.rolelist)==1):
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'ip':get_client_ip(request),                                                                                  
            'roles' :tmp,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'usermaster':g.usermaster,
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec= request.POST.get('shop_sec')
            reqf=list(sanctionSSE.objects.filter(shopsec=shop_sec).values('shopsec','desig','sanc'))
            shopname=list(Shop.objects.filter(shop=shop_sec).values('sh_desc').distinct())
            sub=empmast.objects.annotate(emp=Substr("empno",7,5)).distinct() 
            for i in range(0,len(reqf)):
                c=0
                for j in Shemp.objects.filter(staff_no__in=Subquery(sub.values('emp')),shopsec='2303',desgn__startswith=reqf[i]['desig']).values('name','staff_no').distinct():
                    c=c+1
                reqf[i].update({'roll':c})
             
            tm=Shemp.objects.all().values('shopsec').distinct()  
            tmp=[]
            for on in tm:
                tmp.append(on['shopsec'])
            context={
                'sub':1,
                'reqf':reqf,
                'nav':g.nav,
                'shop_sec':shop_sec,
                'lenm' :2,
                'roles':tmp,
                'ip':get_client_ip(request),
                'subnav':g.subnav,
                'shopname':shopname,
                'usermaster':g.usermaster,

                
            }
            if(len(g.rolelist)==1):
                context = {
                    'sub':1,
                    'reqf':reqf,
                    'nav':g.nav,
                    'shop_sec':shop_sec,
                    'lenm' :2,
                    'roles':tmp,
                    'ip':get_client_ip(request),
                    'subnav':g.subnav,
                    'shopname':shopname,
                    'usermaster':g.usermaster,
                }
            elif(len(g.rolelist)>1):
                context = {
                    'sub':1,
                    'reqf':reqf,
                    'nav':g.nav,
                    'shop_sec':shop_sec,
                    'lenm' :2,
                    'roles':tmp,
                    'ip':get_client_ip(request),
                    'subnav':g.subnav,
                    'shopname':shopname,
                    'usermaster':g.usermaster,
                }
            
            
        if submitvalue=='Proceed2':
            val2 = request.POST.get('updt_date')
            p=val2.split('-')
            year1=int(p[0])-60
            year=str(year1)
            year=year[2:]
            month=p[1]
            day=p[2]
            dat=day+"-"+month+"-"+year
            s = list(val2)
            date='' . join(map(str,s))
            date = date[8:10] + "-" + date[5:7] + "-" + date[0:4]
            pre_date_time=str(datetime.datetime.now())
            pre_date_time1=pre_date_time.split(' ')
            pre_date=pre_date_time1[0]
            pre=pre_date.split('-')
            pre_day=pre[2]
            pre_mon=pre[1]
            pre_year1=int(pre[0])-60
            pre_year=str(pre_year1)
            pre_year=pre_year[2:]
            pre_date_be_60=pre_day+"-"+pre_mon+"-"+pre_year
            shop_sec= request.POST.get('shop_sec')
            reqf=list(sanctionSSE.objects.filter(shopsec=shop_sec).values('shopsec','desig','sanc'))
            sub=empmast.objects.annotate(emp=Substr("empno",7,5)).distinct()
            for i in range(0,len(reqf)):
                c=0
                for j in Shemp.objects.filter(staff_no__in=Subquery(sub.values('emp')),shopsec='2303',desgn__startswith=reqf[i]['desig']).values('name','staff_no').distinct():
                    c=c+1
                reqf[i].update({'roll':c})
            k=empmast.objects.filter(birthdate__contains="-"+month+"-").filter(birthdate__contains="-"+year).values('empno','empname','birthdate','desig_longdesc')
            shopname=list(Shop.objects.filter(shop=shop_sec).values('sh_desc').distinct())
            context = {
                    'sub':1,
                    'k':k,
                    'nav':g.nav,
                    'lenm' :2,
                    'roles':tmp,
                    'ip':get_client_ip(request),
                    'subnav':g.subnav,
                    'shop_sec':shop_sec,
                    'reqf':reqf,
                    'date':date,
                    'shopname':shopname,
                    'usermaster':g.usermaster,

                }
    return render(request,"MISC/SANCTIONROLL/sanction_rollview.html",context)  


@login_required
@role_required(urlpass='/sanction_formview/')

def sanction_formview(request): 
    import datetime
    tm=Shemp.objects.all().values('shopsec').distinct()
    tmp=[]
    for on in tm:
        tmp.append(on['shopsec'])
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
        context = {
            'sub':0,
            'subnav':g.subnav,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'usermaster':g.usermaster,
        }
    elif(len(g.rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(g.rolelist),
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles' :tmp,
            'usermaster':g.usermaster,
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='submit':
            shop_sec= request.POST.get('shop_sec')
            totindb=request.POST.get('totmebs')
            now = datetime.datetime.now()
            user=request.user
            for tb in range(1,int(totindb)+1):
                desig=request.POST.get('desig1'+str(tb))
                san_no=request.POST.get('san_no'+str(tb))
                pre=list(sanctionSSE.objects.filter(shopsec=shop_sec,desig=desig).values('id'))
                if(shop_sec==None or desig==None or san_no==None or now==None or user==None):
                    pass
                else:
                    if len(pre)>0:
                        sanctionSSE.objects.filter(shopsec=shop_sec,desig=desig).update(sanc=str(san_no),login_id=str(user), last_modified=str(now))
                    else:
                        sanctionSSE.objects.create(shopsec=str(shop_sec), desig=str(desig), sanc=str(san_no),login_id=str(user), last_modified=str(now))          
    return render(request,"MISC/SANCTIONROLL/sanction_formview.html",context) 
