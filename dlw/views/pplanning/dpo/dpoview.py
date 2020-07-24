from dlw.views import *
import dlw.views.globals as g

@login_required
def dpo(request):
    from dlw.models import annual_production

    tod = date.today()
    ft=int(tod.strftime("%Y"))
    ft2=ft+1
    ctp=str(ft)+'-'+str(ft2)

    locos=[]

    obj=annual_production.objects.filter(financial_year=ctp)

    for i in range(0,len(obj)):
        locos.append(obj[i].loco_type)
    


    context={
        'nav':g.nav,
        'ip':get_client_ip(request),
        'Role':g.rolelist[0],
        'cyear':ctp,
        'add':0,
        'locolist':locos,
        'subnav':g.subnav,
        'usermaster':g.usermaster,
    }

    if request.method=="POST":
        submit=request.POST.get('submit')
        locos=[]
        obj=annual_production.objects.filter(financial_year=ctp)
        for i in range(0,len(obj)):
            locos.append(obj[i].loco_type)
        if submit=='Proceed':
            b1=0
            flag=0
            locos=[]
            obj=annual_production.objects.filter(financial_year=ctp)
            for i in range(0,len(obj)):
                locos.append(obj[i].loco_type)
            loco=request.POST.get('loco')
            b2=request.POST.get('barl2')
            tc=request.POST.get('tc')
            num=(int(tc)-1) // 5
            mod=(int(tc)-1) % 5
            if(num>9):
                flag=1
            if loco=='WAP10' or loco=='WAP11' or loco=='WAP-7 ELECTRIC LOCO' or loco=='WAP-9 ELECTRIC LOCO':
                b1=33
            bno=str(b1)+'/'+str(b2)+'/'


            context={
            'nav':g.nav,
            'ip':get_client_ip(request),
            'Role':g.rolelist[0],
            'cyear':ctp,
            'b1':b1,
            'b2':b2,
            'tc':tc,
            'bno':bno,
            'ranl9':range(2,num+2),
            'ran':range(2,10),
            'ran2':range(10,num+2),
            'flag':flag,
            'num':num,
            'mod':mod,
            'two':num+2,
            'cm':225,
            'lcname':loco,
            'add':1,
            'locolist':locos,
            'subnav':g.subnav,
            'usermaster':g.usermaster,

        } 

        if submit=='Save':
            context={
            'nav':g.nav,
            'ip':get_client_ip(request),
            'Role':g.rolelist[0],
            'locolist':locos,
            'cyear':ctp,
            'subnav':g.subnav,
            'usermaster':g.usermaster,
        } 
    return render(request, 'PPRODUCTION/DPO/dpo.html', context)


@login_required
@role_required(urlpass='/dpoinput/')
def dpoinput(request):
    from dlw.models import annual_production,barrelfirst,Dpo,dpoloco,jpo
    tod = date.today()
    ft=int(tod.strftime("%Y"))
    ft2=ft+1
    ctp=str(ft)+'-'+str(ft2)
    locos=[]
    locoindb=[]
    annulloco=[]
    obj=barrelfirst.objects.all()
    for i in range(0,len(obj)):
        locos.append(obj[i].locotype)
    context={
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'Role':g.rolelist[0],
        'cyear':ctp,
        'add':0,
        'locolist':locos,
        'locoindb':locoindb,
        'annualloco':annulloco,
        'usermaster':g.usermaster,
    }
    if request.method=="POST":
        subject=None
        reference=None
        copyto=None
        summary=None
        dat=None
        locoindb=[]
        dictemper={}
        dataext=0
        submit=request.POST.get('submit')
        if submit=='Proceed':
            b1=0
            loco=request.POST.get('loco')
            b2=request.POST.get('barl2')
            cm=225
            cm2=300
            obj1=barrelfirst.objects.filter(locotype=loco)
            b1=obj1[0].code
            
            args = jpo.objects.filter(financial_year=ctp,jpo='main') 
            ar=args.aggregate(Max('revisionid'))
            revisionidmax=ar['revisionid__max']
            annualobj=annual_production.objects.filter(financial_year=ctp,revisionid=revisionidmax)
            for l in range(len(annualobj)):
                annulloco.append(annualobj[l].loco_type)
            
            obj=Dpo.objects.filter(locotype=loco,orderno=b2,procedureno=0)
            if (obj is not None) and len(obj):
                subject=obj[0].subject
                reference=obj[0].reference
                copyto=obj[0].copyto
                summary=obj[0].summary
                dat=obj[0].date
            objloco=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=0).values('loconame').distinct()
            if (objloco is not None) and len(objloco):
                for l in range(len(objloco)):
                    locoindb.append(objloco[l]['loconame'])

                objlocobt=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=0)
                if (objlocobt is not None) and len(objlocobt):
                    for l in range(len(objlocobt)):
                        bnoo=objlocobt[l].batchordno
                        ss=bnoo[0:2]+'/'+bnoo[2:5]+'/'+bnoo[5:8]
                        temper = {str(l):{"bno":ss,
                                           "qty":objlocobt[l].qtybatch,
                                           "cumino":objlocobt[l].cumino,
                                           "loconame":objlocobt[l].loconame,
                                           }}
                        dataext=dataext+1

                        dictemper.update(copy.deepcopy(temper))
                   
            context={
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'Role':g.rolelist[0],
            'cyear':ctp,
            'b1':b1,
            'b2':b2,
            'cm':cm,
            'cm2':cm2,
            'lcname':loco,
            'add':1,
            'locolist':locos,
            'locoindb':locoindb,
            'subject':subject,
            'reference':reference,
            'copyto':copyto,
            'summary':summary,
            'date':dat,
            'dictemper':dictemper,
            'dataext':dataext,
            'annualloco':annulloco,
            'usermaster':g.usermaster,
        } 

        if submit=='Save':
            sub=request.POST.get('sub')
            refn=request.POST.get('refn')
            summary=request.POST.get('summary')
            copyto=request.POST.get('copyto')
            datee=request.POST.get('xTime')
            
            locot=request.POST.get('loco')
            ordno=request.POST.get('barl2')
            dataext=request.POST.get('dataext')
            totbaches=request.POST.get('totbaches')
            args = jpo.objects.filter(financial_year=ctp,jpo='main') 
            ar=args.aggregate(Max('revisionid'))
            revisionidmax=ar['revisionid__max']
            annualobj=annual_production.objects.filter(financial_year=ctp,revisionid=revisionidmax)
            for l in range(len(annualobj)):
                annulloco.append(annualobj[l].loco_type)
            dpopb=Dpo.objects.filter(procedureno=0,locotype=locot,orderno=ordno)
            if dpopb is not None and len(dpopb):
                obj=Dpo.objects.filter(procedureno=0,locotype=locot,orderno=ordno).update(subject=sub,reference=refn,date=datee,copyto=copyto,summary=summary)
                
            else:
                obj=Dpo.objects.create()
                obj.subject=sub
                obj.reference=refn
                obj.date=datee
                obj.copyto=copyto
                obj.summary=summary
                obj.orderno=ordno
                obj.locotype=locot
                obj.save()
            temp1="loconame"
            idname=[]
            lcname=[]
            ttlcnt=request.POST.get('cm2')
            
            for i in range(1,int(dataext)+1):
                bno=request.POST.get("bno"+str(i))
           
                a=bno.split('/')
                s=""
                for ad in a:
                    s=s+ad
                qty=request.POST.get("qty"+str(i))
                typ=request.POST.get("typ"+str(i))               
                cumino=request.POST.get("cumino"+str(i))
                dpoloco.objects.filter(procedureno=0,locotype=locot,orderno=ordno,batchordno=s,loconame=typ).update(qtybatch=qty,cumino=cumino)
            
            
            for i in range(int(dataext)+1,int(totbaches)+1):
                 
                bno=request.POST.get("bno"+str(i))
         
                a=bno.split('/')
                s=""
                for ad in a:
                    s=s+ad
                qty=request.POST.get("qty"+str(i))
                typ=request.POST.get("typ"+str(i))               
                cumino=request.POST.get("cumino"+str(i))
                obj=dpoloco.objects.create()
                obj.loconame=typ
                obj.batchordno=s
                obj.qtybatch=qty
                obj.cumino=cumino
                obj.orderno=ordno
                obj.locotype=locot
                obj.save()
               
            context={
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'Role':g.rolelist[0],
            'cyear':ctp,
            'locolist':locos,
            'annualloco':annulloco,
            'usermaster':g.usermaster,
        } 

    return render(request, 'PPRODUCTION/DPO/dpof.html', context)


@login_required
@role_required(urlpass='/dporeport/')
def dporeport(request):
    from dlw.models import annual_production,Dpo,barrelfirst,dpoloco,jpo
    from django.db.models import Max
    tod = date.today()
    ft=int(tod.strftime("%Y"))
    ft2=ft+1
    ctp=str(ft)+'-'+str(ft2)

    locos=[]
    reflist=[]

    obj=barrelfirst.objects.all()
    for i in range(0,len(obj)):
        locos.append(obj[i].locotype)
    


    context={
        'nav':g.nav,
        'ip':get_client_ip(request),
        'Role':g.rolelist[0],
        'cyear':ctp,
        'add':0,
        'locolist':locos,
        'subnav':g.subnav,
        'usermaster':g.usermaster,
       
    }

    if request.method=="POST":

        pno=None
        pnonum=None


        subject=None
        reference=None
        copyto=None
        summary=None
        dat=None
        data=0
        locodisp=""
        procedureno=None
        locoindb=[]
        dictemper={}
        dataext=0
        procedure=0
        
        totproduction=0
        balance=0
        totproduced=0
        
        

        submit=request.POST.get('submit')
        finalsubmit=request.POST.get('finalize')
        locos=[]
        obj=barrelfirst.objects.all()
        for i in range(0,len(obj)):
            locos.append(obj[i].locotype)
        if submit=='Proceed':
            pord=request.POST.get('pord')


            b1=0
            loco=request.POST.get('loco')
            b2=request.POST.get('barl2')
            cm=225
            cm2=300
            

            procedure=pord

            if(pord!=None and  len(pord)):
                dloco=Dpo.objects.filter(procedureno=pord)
                if(len(dloco) and dloco is not None):
                    loco=dloco[0].locotype
                    b2=dloco[0].orderno
                obj1=barrelfirst.objects.filter(locotype=loco)
                if (obj1 is not None) and len(obj1):
                    b1=obj1[0].code
                
                obj=Dpo.objects.filter(locotype=loco,orderno=b2,procedureno=pord)
                if (obj is not None) and len(obj):
                    subject=obj[0].subject
                    reference=obj[0].reference
                    copyto=obj[0].copyto
                    summary=obj[0].summary
                    dat=obj[0].date
                    if(obj[0].procedureno=='0'):
                        procedureno=0
                    else:
                        procedureno=1

                    reflist=findthis(request,reference)
                objloco=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=pord).values('loconame').distinct()
                if (objloco is not None) and len(objloco):
                    args = jpo.objects.filter(financial_year=ctp,jpo='main') 
                    ar=args.aggregate(Max('revisionid'))
                    revisionidmax=ar['revisionid__max']
                    lis=['WDM2','YDM4','G4D']
                    for l in range(len(objloco)):
                        locoindb.append(objloco[l]['loconame'])
                        annualobj=annual_production.objects.filter(financial_year=ctp,loco_type=locoindb[l]+" ELECTRIC LOCO",revisionid=revisionidmax)
                        if(annualobj is not None and len(annualobj)):
                            if annualobj[0].target_quantity=='-':
                                totproduction=totproduction+0
                            else:
                                
                                totproduction=totproduction+int(annualobj[0].target_quantity)
                   
                    objlocobt=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=pord).order_by('id')
                    if (objlocobt is not None) and len(objlocobt):
                        for l in range(len(objlocobt)):

                            bnoo=objlocobt[l].batchordno
                            ss=bnoo[0:2]+'/'+bnoo[2:5]+'/'+bnoo[5:8]
                            temper = {str(l):{"bno":ss,
                                               "qty":objlocobt[l].qtybatch,
                                               "cumino":objlocobt[l].cumino,
                                               "loconame":objlocobt[l].loconame,
                                               }}
                            totproduced=totproduced+int(objlocobt[l].qtybatch)
                            dataext=dataext+1
                            dictemper.update(copy.deepcopy(temper))
                        data=1

            elif((loco!=None and  len(loco)) and (b2!=None and  len(b2))):
                obj1=barrelfirst.objects.filter(locotype=loco)
                b1=obj1[0].code
                
                obj=Dpo.objects.filter(locotype=loco,orderno=b2,procedureno=0)
                if (obj is not None) and len(obj):
                    subject=obj[0].subject
                    reference=obj[0].reference
                    copyto=obj[0].copyto
                    summary=obj[0].summary
                    dat=obj[0].date
                    if(obj[0].procedureno=='0'):
                        procedureno=0
                    else:
                        procedureno=1

                    reflist=findthis(request,reference)
                objloco=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=0).values('loconame').distinct()
                if (objloco is not None) and len(objloco):
                    args = jpo.objects.filter(financial_year=ctp,jpo='main') 
                    ar=args.aggregate(Max('revisionid'))
                    revisionidmax=ar['revisionid__max']
                    lis=['WDM2','YDM4','G4D']
                    for l in range(len(objloco)):
                        locoindb.append(objloco[l]['loconame'])
                        annualobj=annual_production.objects.filter(financial_year=ctp,loco_type=locoindb[l]+" ELECTRIC LOCO",revisionid=revisionidmax)
                        if(annualobj is not None and len(annualobj)):
                            if annualobj[0].target_quantity=='-':
                                totproduction=totproduction+0
                            else:
                                
                                totproduction=totproduction+int(annualobj[0].target_quantity)
                
                    for n in locoindb:
                        obt=dpoloco.objects.filter(locotype=loco,orderno=b2,loconame=n)
                        if obt is not None and len(obt):
                            for nn in range(len(obt)):
                                totproduced=totproduced+int(obt[nn].qtybatch)

                    objlocobt=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=0).order_by('batchordno')
                    if (objlocobt is not None) and len(objlocobt):
                        for l in range(len(objlocobt)):

                            bnoo=objlocobt[l].batchordno
                            ss=bnoo[0:2]+'/'+bnoo[2:5]+'/'+bnoo[5:8]
                            temper = {str(l):{"bno":ss,
                                                   "qty":objlocobt[l].qtybatch,
                                                   "cumino":objlocobt[l].cumino,
                                                   "loconame":objlocobt[l].loconame,
                                                   }}
                          
                          
                          
                          
                          
                            dataext=dataext+1

                            dictemper.update(copy.deepcopy(temper))
                        data=1


            balance=totproduction-totproduced
            if balance==0:
                balance="NIL"
                
            context={
            'nav':g.nav,
            'ip':get_client_ip(request),
            'Role':g.rolelist[0],
            'cyear':ctp,
            'productionyear':ctp,
            'totproduction':totproduction,
            'balance':balance,
            'b1':b1,
            'b2':b2,
            'cm':cm,
            'cm2':cm2,
            'lcname':loco,
            'add':1,
            'locolist':locos,
            'subject':subject,
            'reference':reference,
            'copyto':copyto,
            'summary':summary,
            'date':dat,
            'dictemper':dictemper,
            'dataext':dataext,
            'data':data,
            'reflist':reflist,
            'finalvalue':procedureno,
            'procedure':procedure,
            'subnav':g.subnav,
            'usermaster':g.usermaster,

        } 



        if finalsubmit == "Submit":
            
            pnonum=0
            b1=0
            loco=request.POST.get('loco')
            b2=request.POST.get('barl2')
            cm=225
            cm2=300
            obj1=barrelfirst.objects.filter(locotype=loco)
            b1=obj1[0].code


            objlocobt=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=0)
            if (objlocobt is not None) and len(objlocobt):
                allobj = Dpo.objects.all()
                maxobj=Dpo.objects.aggregate(Max('procedureno'))
                if allobj is None or len(allobj)==0:
                    pnonum=547
                else:
                    pnonum=int(maxobj['procedureno__max'])+1



            
            obj=Dpo.objects.filter(locotype=loco,orderno=b2,procedureno=0)
            if (obj is not None) and len(obj):
                subject=obj[0].subject
                reference=obj[0].reference
                copyto=obj[0].copyto
                summary=obj[0].summary
                dat=obj[0].date
                if(obj[0].procedureno=='0'):
                    procedureno=0
                else:
                    procedureno=1
                reflist=findthis(request,reference)
            objloco=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=0).values('loconame').distinct()
            if (objloco is not None) and len(objloco):
                    args = jpo.objects.filter(financial_year=ctp,jpo='main') 
                    ar=args.aggregate(Max('revisionid'))
                    revisionidmax=ar['revisionid__max']
                    lis=['WDM2','YDM4','G4D']
                    for l in range(len(objloco)):
                        locoindb.append(objloco[l]['loconame'])
                        annualobj=annual_production.objects.filter(financial_year=ctp,loco_type=locoindb[l]+" ELECTRIC LOCO",revisionid=revisionidmax)
                        if(annualobj is not None and len(annualobj)):
                            if annualobj[0].target_quantity=='-':
                                totproduction=totproduction+0
                            else:
                                
                                totproduction=totproduction+int(annualobj[0].target_quantity)
                  
            if (objloco is not None) and len(objloco):
                for l in range(len(objloco)):
                    locoindb.append(objloco[l]['loconame'])

                objlocobt=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=0)
                if (objlocobt is not None) and len(objlocobt):
                    for l in range(len(objlocobt)):
                        bnoo=objlocobt[l].batchordno
                        ss=bnoo[0:2]+'/'+bnoo[2:5]+'/'+bnoo[5:8]
                        temper = {str(l):{"bno":ss,
                                           "qty":objlocobt[l].qtybatch,
                                           "cumino":objlocobt[l].cumino,
                                           "loconame":objlocobt[l].loconame,
                                           }}
                        dataext=dataext+1

                        dictemper.update(copy.deepcopy(temper))

                    data=1

                    dpp=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=0).update(procedureno=pnonum)
                    dpp=Dpo.objects.filter(locotype=loco,orderno=b2,procedureno=0).update(procedureno=pnonum)

                    dpoop=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=pnonum)
                    procedure=dpoop[0].procedureno
                


            balance=totproduction-totproduced
            if balance==0:
                balance="NIL"
            context={
                'dpono':1,
            
                'productionyear':ctp,
            'totproduction':totproduction,
            'balance':balance,
            
            'nav':g.nav,
            'ip':get_client_ip(request),
            'Role':g.rolelist[0],
            'cyear':ctp,
            'b1':b1,
            'b2':b2,
            'cm':cm,
            'cm2':cm2,
            'lcname':loco,
            'add':1,
            'locolist':locos,
            'subject':subject,
            'reference':reference,
            'copyto':copyto,
            'summary':summary,
            'date':dat,
            'dictemper':dictemper,
            'dataext':dataext,
            'data':data,
            'reflist':reflist,
            'finalvalue':procedureno,
            'procedure':procedure,
            'subnav':g.subnav,
            'usermaster':g.usermaster,
        }

    return render(request, 'PPRODUCTION/DPO/dporeport.html', context)











