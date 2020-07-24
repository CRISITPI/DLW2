from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/jpo123/')
def jpo123(request):
    from dlw.models import annual_production,jpo,namedgn
    cuser=request.user
    rolelist=(g.usermaster).role.split(", ")
    dictt=jpo.objects.all().aggregate(Max('revisionid'))
    revex=dictt['revisionid__max']
    if revex is None:
        revex=0
    revcnt=revex+1    
    datadic={}
    context={
        'nav':g.nav,
        'subnav':g.subnav,
        'usermaster':g.usermaster,
        'ip':get_client_ip(request),
        'revcnt':range(revcnt),
    }
    spclremlist=[]
    reflist=[]
    remklist=[]
    nrmllist=[]
    altrlist=[]
    datadic={}
    nrc={}
    f=0
    nr=0 
    k=0
    j=0
    data=0
    e=0  
    exp={}  
    ex=0  

    d=0
    dgs={}
    dg=0

    r1=0
    rspm={}
    rm=0

    r2=0
    rspitm={}
    ri=0

    z=0
    zrzr={}
    zr=0

    z2=0
    zozo={}
    zo=0

    remark={}
    rma=0
    rmark=0

    ty1=0
    ty2=0
    ty3=0
    ty4=0

    yearlist=[]
    years={}



    flag=1
    dictemper={}
    diiict={}
    dct={}
    indrwspan=0


    nrcflag=1
    nrcdictemper={}
    nrcrwspan=0

    nrcdgflag=1
    nrcdgdictemper={}
    nrcdgrwspan=0

    cspan=0

    expflag=1
    expdictemper={}
    exprwspan=0

    zrflag=1
    zrdictemper={}
    zrrwspan=0

    zrasflag=1
    zrasdictemper={}
    zrasrwspan=0

    zroverflag=1
    zroverdictemper={}
    zroverrwspan=0

    rspflag=1
    rspdictemper={}
    rsprwspan=0

    rspitmflag=1
    rspitmdictemper={}
    rspitmrwspan=0

    total={}
    tottq=[]
    tot=0

    rev=None
    remk1=None
    remk2=None
    jpoo=None
    sub=None
    dt=None
    headalt=None

    finalvalue=0
    formno=0
    number=0
    cdgp=0

    if request.method == "POST":
        tod = date.today()
        ft=int(tod.strftime("%Y"))
        ft2=ft+1
        ctp=str(ft)+'-'+str(ft2)
        yr=ctp
        ree=request.POST.get('rev')
        if ree is not None:
            rev=int(ree)
        objm=jpo.objects.filter(jpo='main',revisionid=rev)
        if len(objm):
            cdgp=int(objm[0].numdgp)
        objnm=namedgn.objects.filter(revision=rev)
        namelist=[]
        desiglist=[]
        for o in objnm:
            namelist.append(o.namep)
            desiglist.append(o.design)
        
        jpoo=request.POST.get('jpotype')
        finalize=request.POST.get('finalize')
        Finalize=request.POST.get('Finalize')
        
        if (rev is None) and (finalize is not None):
            rev=int(request.POST.get('revh'))
        if (jpoo is None) and (finalize is not None):
            jpoo=request.POST.get('jpotypeh')
        reflist=[]
        remklist=[]
        altrlist=[]
        jpoobj=jpo.objects.filter(financial_year=yr,revisionid=rev)
        y1=[]
        y2=[]
        y3=[]
        y4=[]
        yint=[]
        y1=yr.split('-',2)
        

        yint.append(int(y1[0])+1)
        yint.append(int(y1[1])+1)
        

        y2.append(str(yint[0]))
        y2.append(str(yint[1]))
        yr2=y2[0]+'-'+y2[1]

        yint=[]

        yint.append(int(y2[0])+1)
        yint.append(int(y2[1])+1)
        

        y3.append(str(yint[0]))
        y3.append(str(yint[1]))
        yr3=y3[0]+'-'+y3[1]

        yint=[]

        yint.append(int(y3[0])+1)
        yint.append(int(y3[1])+1)
        

        y4.append(str(yint[0]))
        y4.append(str(yint[1]))
        yr4=y4[0]+'-'+y4[1]
        yl=[]
        yl.append(yr)
        yl.append(yr3)

        if jpoo=="main":


            listname=['loty','yr1','yr2','yr3','yr4']
            jpoobj=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='main')
            
            if len(jpoobj):
                sub=jpoobj[0].subject
                numfy=jpoobj[0].numyrs
                ref=jpoobj[0].reference
                mjalt=jpoobj[0].majoralt
                headalt=jpoobj[0].headmjr
                remk=jpoobj[0].remark
                dt=jpoobj[0].date
                formno=jpoobj[0].formno
                number=jpoobj[0].number
                if ref is not None:
                    reflist=findthis(request,ref)
                if mjalt is not None:
                    altrlist=findthis(request,mjalt)
                if remk is not None:
                    remklist=findthis(request,remk)
                spclremlist=[]
                nrmllist=[]
                for str2 in remklist:
                    if len(str2.split('$'))>1:
                        spclremlist.append(str2)
                    elif len(str2.split('*'))>1:
                        spclremlist.append(str2)
                    else:
                        nrmllist.append(str2)

                cspan=numfy

                tod = date.today()
                ft=int(tod.strftime("%Y"))
                ft2=ft+1
                for lol in range(int(numfy)):
                    yearlist.append(str(ft)+'-'+str(ft2))
                    ft=ft+1
                    ft2=ft2+1
                    indo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='ind-rail')
                    if len(indo)==0:
                        flag=0

                    elif len(indo)!=0 and indrwspan==0:
                        indrwspan=len(indo)+1
                        

                    nrco=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='nrc')
                    if len(nrco)==0:
                        nrcflag=0
                    elif len(nrco)!=0 and nrcrwspan==0:
                        nrcrwspan=len(nrco)+1
                        

                    expo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='export')
                    if len(expo)==0:
                        expflag=0

                    elif len(expo)!=0 and exprwspan==0:
                        exprwspan=len(expo)+1

                    zro=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='zr')
                    if len(zro)==0:
                        zrflag=0

                    elif len(zro)!=0 and zrrwspan==0:
                        zrrwspan=len(zro)+1


                    zrov=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='zrover')
                    if len(zrov)==0:
                        zroverflag=0

                    elif len(zrov)!=0 and zroverrwspan==0:
                        zroverrwspan=len(zrov)+1


                    zraso=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='zrasstn')
                    if len(zraso)==0:
                        zrasflag=0

                    elif len(zraso)!=0 and zrasrwspan==0:
                        zrasrwspan=len(zraso)+1

                    nrcdgo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='nrcdgset')
                    if len(nrcdgo)==0:
                        nrcdgflag=0
                    elif len(nrcdgo)!=0 and nrcdgrwspan==0:
                        nrcdgrwspan=len(nrcdgo)+1

                for yrs in range(int(numfy)):

                    temr = {str(yrs):{"yrs":yearlist[yrs],}}
                    years.update(copy.deepcopy(temr))

                if flag:
                    indobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='ind-rail')
                    dell=0

                    for j in range(len(indobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            inobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='ind-rail',loco_type=indobj[j].loco_type)
                            
                            v=inobj[0].target_quantity
                            bq=inobj[0].buffer_quantity

                            if len(v)==0:
                                v='-'

                            if len(bq)==0:
                                bq='-'

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            dct=None

                        dictname="dict"
                        temper = {str(j):{"loty":indobj[j].loco_type,
                                      "dict":diiict,}}
                       
                        dictemper.update(copy.deepcopy(temper))
                        j=j+1

                    for kill in range(int(numfy)):

                        for j in range(len(indobj)):
                            if(dictemper[str(j)]['dict'][str(kill)]['yrtq']!='-'):
                                art=dictemper[str(j)]['dict'][str(kill)]['yrtq']
                                artl=[ord(cc) for cc in art]
                                
                                tr=[]
                                l=[48,49,50,51,52,53,54,55,56,57]
                                for p in range(len(artl)):
                                    if artl[p] in l:
                                        tr.append(artl[p])
                               
                                s=''.join(chr(artl[d]) for d in range(len(tr)) )
                                tot=tot+int(s)
                        tottq.append(tot)
                        tot=0
                        tottemper = {str(kill):{"totq":tottq[kill],}}

                        total.update(copy.deepcopy(tottemper))

                    tottq=[]

                if nrcflag:
                    nrcdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='nrc')
                    dell=0

                    for j in range(len(nrcdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            nrcobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='nrc',loco_type=nrcdobj[j].loco_type)
                            
                            v=nrcobj[0].target_quantity
                            bq=nrcobj[0].buffer_quantity

                            if len(v)==0:
                                v='-'

                            if len(bq)==0:
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None

                        temper = {str(j):{"loty":nrcdobj[j].loco_type,
                                      "dict":diiict,}}

                       

                        j=j+1
                       
                        nrcdictemper.update(copy.deepcopy(temper))

                    for kill in range(int(numfy)):

                        for j in range(len(nrcdobj)):
                            if(nrcdictemper[str(j)]['dict'][str(kill)]['yrtq']!='-'):
                                if len(total.keys()) and j==0:
                                    tot=int(total[str(kill)]['totq'])
                                art=nrcdictemper[str(j)]['dict'][str(kill)]['yrtq']
                                artl=[ord(cc) for cc in art]
                                
                                tr=[]
                                l=[48,49,50,51,52,53,54,55,56,57]
                                for p in range(len(artl)):
                                    if artl[p] in l:
                                        tr.append(artl[p])
                                s=''.join(chr(artl[d]) for d in range(len(tr)) )
                                tot=tot+int(s)
                            else:
                                tot=int(total[str(kill)]['totq'])
                        tottq.append(tot)
                        tot=0
                        tottemper = {str(kill):{"totq":tottq[kill],
                                      
                                        }}

                        total.update(copy.deepcopy(tottemper))

                    tottq=[]

                if nrcdgflag:
                    nrcdgdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='nrcdgset')
                    dell=0

                    for j in range(len(nrcdgdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            nrcdgobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='nrcdgset',loco_type=nrcdgdobj[j].loco_type)
                            
                            v=nrcdgobj[0].target_quantity
                            bq=nrcdgobj[0].buffer_quantity

                            if len(v)==0:
                                v='-'

                            if len(bq)==0:
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None

                        temper = {str(j):{"loty":nrcdgdobj[j].loco_type,
                                      "dict":diiict,}}

                       

                        j=j+1
                       
                        nrcdgdictemper.update(copy.deepcopy(temper))


                if expflag:
                    expdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='export')
                    dell=0

                    for j in range(len(expdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            expobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='export',loco_type=expdobj[j].loco_type)
                            
                            v=expobj[0].target_quantity
                            bq=expobj[0].buffer_quantity

                            if len(v)==0:
                                v='-'

                            if len(bq)==0:
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None

                        temper = {str(j):{"loty":expdobj[j].loco_type,
                                      "dict":diiict,
                                  
                                        }}                 

                        j=j+1
                       
                        expdictemper.update(copy.deepcopy(temper))


                    for kill in range(int(numfy)):

                        for j in range(len(expdobj)):
                            if(expdictemper[str(j)]['dict'][str(kill)]['yrtq']!='-'):
                                if len(total.keys()) and j==0:
                                    tot=int(total[str(kill)]['totq'])
                                art=expdictemper[str(j)]['dict'][str(kill)]['yrtq']
                                artl=[ord(cc) for cc in art]
                                
                                tr=[]
                                l=[48,49,50,51,52,53,54,55,56,57]
                                for p in range(len(artl)):
                                    if artl[p] in l:
                                        tr.append(artl[p])
                               
                                s=''.join(chr(artl[d]) for d in range(len(tr)) )
                                tot=tot+int(s)
                            else:
                                tot=int(total[str(kill)]['totq'])
                                
                        tottq.append(tot)
                        tot=0
                        tottemper = {str(kill):{"totq":tottq[kill],
                                      
                                        }}

                        total.update(copy.deepcopy(tottemper))

                    tottq=[]


                if zrflag:
                    zrdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='zr')
                    dell=0

                    for j in range(len(zrdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            zrobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='zr',loco_type=zrdobj[j].loco_type)
                            
                            v=zrobj[0].target_quantity
                            bq=zrobj[0].buffer_quantity

                            if len(v)==0:
                                v='-'

                            if len(bq)==0:
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            dct=None

                        temper = {str(j):{"loty":zrdobj[j].loco_type,
                                      "dict":diiict,}}                 

                        j=j+1
                       
                        zrdictemper.update(copy.deepcopy(temper))



                if zroverflag:
                    zrovdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='zrover')
                    dell=0

                    for j in range(len(zrovdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            zrovobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='zrover',loco_type=zrovdobj[j].loco_type)
                            
                            v=zrovobj[0].target_quantity
                            bq=zrovobj[0].buffer_quantity

                            if len(v)==0:
                                v='-'

                            if len(bq)==0:
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None

                        temper = {str(j):{"loty":zrovdobj[j].loco_type,
                                      "dict":diiict,}}                 

                        j=j+1
                       
                        zroverdictemper.update(copy.deepcopy(temper))
                
                if zrasflag:
                    zrasdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='zrasstn')
                    dell=0

                    for j in range(len(zrasdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            zrasobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='zrasstn',loco_type=zrasdobj[j].loco_type)
                            
                            v=zrasobj[0].target_quantity
                            bq=zrasobj[0].buffer_quantity

                            if len(v)==0:
                                v='-'

                            if len(bq)==0:
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            dct=None

                        temper = {str(j):{"loty":zrasdobj[j].loco_type,
                                      "dict":diiict,}}                 

                        j=j+1
                       
                        zrasdictemper.update(copy.deepcopy(temper))



            if flag or nrcflag or expflag or zrflag or zroverflag or nrcdgflag or zrasflag:
                data=1

            lidict={0:'loty',1:'yr1',2:'yr3',3:'yr4'}
            colsapn=int(cspan)+2
            if rev==0:
                heading="Production Programme for "
            else:
                heading="Revised Production Programme for "
            for kt,v in years.items():
                heading=heading+str(v['yrs'])+" ,"
            heading=heading+" is indicated below :"

            context={'data':data,
            "data2":datadic,"data3":nrc,"data4":exp,"data5":dgs,"data8":zrzr,"data9":zozo,"jpo":1,
            "listname":listname,"lidict":lidict,
            "years":years,"dictemper":dictemper,"nrcdictemper":nrcdictemper,"expdictemper":expdictemper,"zrdictemper":zrdictemper,"zroverdictemper":zroverdictemper,
            "nrcflag":nrcflag,"flag":flag,"expflag":expflag,"zrflag":zrflag,"zroverflag":zroverflag,
            'nrcdgflag':nrcdgflag,'zrasflag':zrasflag,"nrcdgdictemper":nrcdgdictemper,"zrasdictemper":zrasdictemper,
            "colsapn":colsapn,"bufcspan":int(cspan),
            "nrcrwspan":nrcrwspan,"nrcdgrwspan":nrcdgrwspan,"indrwspan":indrwspan,"exprwspan":exprwspan,"zrrwspan":zrrwspan,"zroverrwspan":zroverrwspan,"zrasrwspan":zrasrwspan,
            "year1":yr,"year2":yr2,"year3":yr3,"year4":yr4,
            "toty1":ty1,"toty2":ty2,"toty3":ty3,"toty4":ty4,'jpoo':jpoo,'rev':rev,
            "pre":f,"n":j+1,'headalt':headalt,
            "pre2":nr,"n2":k+1,
            "pre3":ex,"n3":e+1,
            "pre4":dg,"n4":d+1,
            "pre7":zr,"n7":z+1,
            "pre8":zo,"n8":z2+1,
            'nav':g.nav,'rev':rev,'heading':heading,
            'usermaster':g.usermaster,
            'ip':get_client_ip(request),
            'total':total,'subnav':g.subnav,
            'namelist':namelist,'desiglist':desiglist,'cdgp':range(cdgp),
            'number':number,'formno':formno,'subject':sub,'dt':dt,
            'reflist':reflist,'altrlist':altrlist,'remklist':remklist,'spclremlist':spclremlist,
            'nrmllist':nrmllist,'revcnt':range(revcnt),
            }

        elif jpoo=="rsp":

            jpoobj=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='rsp')
            if len(jpoobj):
                numfy=jpoobj[0].numyrs
                cspan=numfy
                dt=jpoobj[0].date
                sub=jpoobj[0].subject
                numfy=jpoobj[0].numyrs
                remk=jpoobj[0].remark
                number=jpoobj[0].number
                remklist=findthis(request,remk)
                spclremlist=[]
                nrmllist=[]
                for str2 in remklist:
                    if len(str2.split('$'))>1:
                        spclremlist.append(str2)
                    elif len(str2.split('*'))>1:
                        spclremlist.append(str2)
                    else:
                        nrmllist.append(str2)

                tod = date.today()
                ft=int(tod.strftime("%Y"))
                ft2=ft+1
                for lol in range(int(numfy)):
                    yearlist.append(str(ft)+'-'+str(ft2))
                    ft=ft+1
                    ft2=ft2+1
                    rspo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='rspm')
                    if len(rspo)==0:
                        rspflag=0

                    elif len(rspo)!=0 and rsprwspan==0:
                        rsprwspan=len(rspo)+1
                        

                    rspitmo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='rspitm')
                    if len(rspitmo)==0:
                        rspitmflag=0
                    elif len(rspitmo)!=0 and rspitmrwspan==0:
                        rspitmrwspan=len(rspitmo)+1
                        



                for yrs in range(int(numfy)):

                    temr = {str(yrs):{"yrs":yearlist[yrs],}}


                    years.update(copy.deepcopy(temr))

                myvar=0


                if rspflag:
                    rspdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='rspm')
                    dell=0

                    for j in range(len(rspdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            rspobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='rspm',loco_type=rspdobj[j].loco_type)
                        
                            v=rspobj[0].target_quantity
                            bq=rspobj[0].buffer_quantity

                            if len(v)==0:
                                v='-'

                            if len(bq)==0:
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None


                        dictname="dict"
                        temper = {str(j):{"loty":rspdobj[j].loco_type,
                                      "dict":diiict,}}

                        j=j+1
                        myvar=j
                       
                        rspdictemper.update(copy.deepcopy(temper))


                if rspitmflag:
                    rspitmdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='rspitm')
                    dell=0

                    for j in range(len(rspitmdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            rspitmobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='rspitm',loco_type=rspitmdobj[j].loco_type)
                            
                            v=rspitmobj[0].target_quantity
                            bq=rspitmobj[0].buffer_quantity

                            if len(v)==0:
                                v='-'

                            if len(bq)==0:
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None


                        dictname="dict"
                        myvar=myvar+1
                        temper = {str(myvar):{"loty":rspitmdobj[j].loco_type,
                                      "dict":diiict,
                                  
                                        }}

                        j=j+1
                        rspdictemper.update(copy.deepcopy(temper))


                if rspflag or rspitmflag :
                    data=1
            colsapn=int(cspan)+2

            context={"data":data,"data6":rspm,"data7":rspitm,"jpo":0,
              "years":years,"rspdictemper":rspdictemper,
            "rspflag":rspflag,"rspitmflag":rspitmflag,
            "colsapn":colsapn,"bufcspan":int(cspan),
            "rsprwspan":rsprwspan,"rspitmrwspan":rspitmrwspan,'jpoo':jpoo,'rev':rev,
            "year1":yr,"year2":yr2,"year3":yr3,"year4":yr4,
            "pre5":rm,"n5":r1+1,
            "pre6":ri,"n6":r2+1,
            'nav':g.nav,'rev':rev,
            'usermaster':g.usermaster,
            'ip':get_client_ip(request),
            'dt':dt,'subject':sub,
            'total':total,'subnav':g.subnav,
            'namelist':namelist,'desiglist':desiglist,'cdgp':range(cdgp),
            'number':number,'subject':sub,'dt':dt,'remklist':remklist,
            'nrmllist':nrmllist,'revcnt':range(revcnt),
            }

        elif jpoo=="combined":
            

            if (finalize == "Submit") and (Finalize == "yes"):
                
                mainjp=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='main').update(finalval=1)
                
               
                rspjp=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='rsp').update(finalval=1)
            

            listname=['loty','yr1','yr2','yr3','yr4']



            jpoobj=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='main')
            jprsp=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='rsp')
            mainnumfy=0
            rspnumfy=0
            if len(jprsp):
                rspnumfy=int(jprsp[0].numyrs)
            if len(jpoobj):
                mainnumfy=int(jpoobj[0].numyrs)
                if mainnumfy>rspnumfy:
                    numfy=mainnumfy
                else:
                    numfy=rspnumfy
                cspan=numfy
                
                tod = date.today()
                ft=int(tod.strftime("%Y"))
                ft2=ft+1
                for lol in range(int(mainnumfy)):
                    yearlist.append(str(ft)+'-'+str(ft2))
                    ft=ft+1
                    ft2=ft2+1
                    indo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='ind-rail')
                    if len(indo)==0:
                        flag=0

                    elif len(indo)!=0 and indrwspan==0:
                        indrwspan=len(indo)+1
                        

                    nrco=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='nrc')
                    if len(nrco)==0:
                        nrcflag=0
                    elif len(nrco)!=0 and nrcrwspan==0:
                        nrcrwspan=len(nrco)+1
                        

                    expo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='export')
                    if len(expo)==0:
                        expflag=0

                    elif len(expo)!=0 and exprwspan==0:
                        exprwspan=len(expo)+1

                    zro=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='zr')
                    if len(zro)==0:
                        zrflag=0

                    elif len(zro)!=0 and zrrwspan==0:
                        zrrwspan=len(zro)+1


                    zrov=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='zrover')
                    if len(zrov)==0:
                        zroverflag=0

                    elif len(zrov)!=0 and zroverrwspan==0:
                        zroverrwspan=len(zrov)+1

                    zraso=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='zrasstn')
                    if len(zraso)==0:
                        zrasflag=0

                    elif len(zraso)!=0 and zrasrwspan==0:
                        zrasrwspan=len(zraso)+1

                    nrcdgo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='nrcdgset')
                    if len(nrcdgo)==0:
                        nrcdgflag=0
                    elif len(nrcdgo)!=0 and nrcdgrwspan==0:
                        nrcdgrwspan=len(nrcdgo)+1
                for yrs in range(int(numfy)):

                    temr = {str(yrs):{"yrs":yearlist[yrs],}}

                    years.update(copy.deepcopy(temr))




                if flag:
                    indobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='ind-rail')
                    dell=0

                    for j in range(len(indobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            inobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='ind-rail',loco_type=indobj[j].loco_type)
                            
                            if len(inobj)==0:
                                v='-'
                                bq='-'
                            else:
                                v=inobj[0].target_quantity
                                bq=inobj[0].buffer_quantity

                                if len(v)==0:
                                    v='-'

                                if len(bq)==0:
                                    bq='-'


                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None

                        dictname="dict"
                        temper = {str(j):{"loty":indobj[j].loco_type,"dict":diiict,}}
                       
                       
                        dictemper.update(copy.deepcopy(temper))
                        j=j+1

                    for kill in range(int(numfy)):

                        for j in range(len(indobj)):
                            if(dictemper[str(j)]['dict'][str(kill)]['yrtq']!='-'):
                                art=dictemper[str(j)]['dict'][str(kill)]['yrtq']
                                artl=[ord(cc) for cc in art]
                                
                                tr=[]
                                l=[48,49,50,51,52,53,54,55,56,57]
                                for p in range(len(artl)):
                                    if artl[p] in l:
                                        tr.append(artl[p])
                                s=''.join(chr(artl[d]) for d in range(len(tr)) )
                                tot=tot+int(s)
                        tottq.append(tot)
                        tot=0
                        tottemper = {str(kill):{"totq":tottq[kill],
                                      
                                        }}

                        total.update(copy.deepcopy(tottemper))

                    tottq=[]



                if nrcflag:
                    nrcdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='nrc')
                    dell=0

                    for j in range(len(nrcdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            nrcobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='nrc',loco_type=nrcdobj[j].loco_type)
                            if len(nrcobj)!=0:
                                v=nrcobj[0].target_quantity
                                bq=nrcobj[0].buffer_quantity

                                if len(v)==0:
                                    v='-'

                                if len(bq)==0:
                                    bq='-'
                            else:
                                v='-'
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None

                        temper = {str(j):{"loty":nrcdobj[j].loco_type,
                                      "dict":diiict,
                                  
                                        }}

                       

                        j=j+1
                       
                        nrcdictemper.update(copy.deepcopy(temper))

                    for kill in range(int(numfy)):

                        for j in range(len(nrcdobj)):
                            if(nrcdictemper[str(j)]['dict'][str(kill)]['yrtq']!='-'):
                                if len(total.keys()) and j==0:
                                    tot=int(total[str(kill)]['totq'])
                                art=nrcdictemper[str(j)]['dict'][str(kill)]['yrtq']
                                artl=[ord(cc) for cc in art]
                                
                                tr=[]
                                l=[48,49,50,51,52,53,54,55,56,57]
                                for p in range(len(artl)):
                                    if artl[p] in l:
                                        tr.append(artl[p])
                                s=''.join(chr(artl[d]) for d in range(len(tr)) )
                                tot=tot+int(s)
                            else:
                                tot=int(total[str(kill)]['totq'])
                        tottq.append(tot)
                        tot=0
                        tottemper = {str(kill):{"totq":tottq[kill],
                                      
                                        }}

                        total.update(copy.deepcopy(tottemper))

                    tottq=[]
                    




                if expflag:
                    expdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='export')
                    dell=0

                    for j in range(len(expdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            expobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='export',loco_type=expdobj[j].loco_type)
                            
                            if len(expobj)!=0:
                                v=expobj[0].target_quantity
                                bq=expobj[0].buffer_quantity

                                if len(v)==0:
                                    v='-'

                                if len(bq)==0:
                                    bq='-'
                            else:
                                v='-'
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None

                        temper = {str(j):{"loty":expdobj[j].loco_type,
                                      "dict":diiict,}}                 

                        j=j+1
                       
                        expdictemper.update(copy.deepcopy(temper))


                    for kill in range(int(numfy)):

                        for j in range(len(expdobj)):
                            if(expdictemper[str(j)]['dict'][str(kill)]['yrtq']!='-'):
                                if len(total.keys()) and j==0:
                                    tot=int(total[str(kill)]['totq'])
                                art=expdictemper[str(j)]['dict'][str(kill)]['yrtq']
                                artl=[ord(cc) for cc in art]
                                
                                tr=[]
                                l=[48,49,50,51,52,53,54,55,56,57]
                                for p in range(len(artl)):
                                    if artl[p] in l:
                                        tr.append(artl[p])
                                s=''.join(chr(artl[d]) for d in range(len(tr)) )
                                tot=tot+int(s)
                            else:
                                tot=int(total[str(kill)]['totq'])
                        tottq.append(tot)
                        tot=0
                        tottemper = {str(kill):{"totq":tottq[kill],
                                      
                                        }}

                        total.update(copy.deepcopy(tottemper))

                    tottq=[]
                if nrcdgflag:
                    nrcdgdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='nrcdgset')
                    dell=0

                    for j in range(len(nrcdgdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            nrcdgobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='nrcdgset',loco_type=nrcdgdobj[j].loco_type)
                            
                            if len(nrcdgdobj)!=0:
                                v=nrcdgobj[0].target_quantity
                                bq=nrcdgobj[0].buffer_quantity

                                if len(v)==0:
                                    v='-'

                                if len(bq)==0:
                                    bq='-'
                            else:
                                v='-'
                                bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None

                        temper = {str(j):{"loty":nrcdgdobj[j].loco_type,
                                      "dict":diiict,}}

                       

                        j=j+1
                       
                        nrcdgdictemper.update(copy.deepcopy(temper))

                if zrflag:
                    zrdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='zr')
                    dell=0

                    for j in range(len(zrdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            zrobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='zr',loco_type=zrdobj[j].loco_type)
                            
                            if len(zrobj)==0:
                                v='-'
                                bq='-'
                            else:
                                v=zrobj[0].target_quantity
                                bq=zrobj[0].buffer_quantity

                                if len(v)==0:
                                    v='-'

                                if len(bq)==0:
                                    bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None

                        temper = {str(j):{"loty":zrdobj[j].loco_type,
                                      "dict":diiict,}}                 

                        j=j+1
                       
                        zrdictemper.update(copy.deepcopy(temper))



                if zroverflag:
                    zrovdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='zrover')
                    dell=0

                    for j in range(len(zrovdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            zrovobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='zrover',loco_type=zrovdobj[j].loco_type)
                            
                            if len(zrovdobj)==0:
                                v='-'
                                bq='-'
                            else:
                                v=zrovobj[0].target_quantity
                                bq=zrovobj[0].buffer_quantity

                                if len(v)==0:
                                    v='-'

                                if len(bq)==0:
                                    bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None

                        temper = {str(j):{"loty":zrovdobj[j].loco_type,
                                      "dict":diiict,
                                  
                                        }}                 

                        j=j+1
                       
                        zroverdictemper.update(copy.deepcopy(temper))

                if zrasflag:
                    zrasdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='zrasstn')
                    dell=0

                    for j in range(len(zrasdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            zrasobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='zrasstn',loco_type=zrasdobj[j].loco_type)
                            
                            if len(zrasobj)==0:
                                v='-'
                                bq='-'
                            else:
                                v=zrasobj[0].target_quantity
                                bq=zrasobj[0].buffer_quantity

                                if len(v)==0:
                                    v='-'

                                if len(bq)==0:
                                    bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            dct=None

                        temper = {str(j):{"loty":zrasdobj[j].loco_type,
                                      "dict":diiict,}}                 

                        j=j+1
                       
                        zrasdictemper.update(copy.deepcopy(temper))


                tod = date.today()
                ft=int(tod.strftime("%Y"))
                ft2=ft+1
                for lol in range(int(rspnumfy)):
                    yearlist.append(str(ft)+'-'+str(ft2))
                    ft=ft+1
                    ft2=ft2+1
                    rspo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='rspm')
                    if len(rspo)==0:
                        rspflag=0

                    elif len(rspo)!=0 and rsprwspan==0:
                        rsprwspan=len(rspo)+1
                        

                    rspitmo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=rev,customer='rspitm')
                    if len(rspitmo)==0:
                        rspitmflag=0
                    elif len(rspitmo)!=0 and rspitmrwspan==0:
                        rspitmrwspan=len(rspitmo)+1



                for yrs in range(int(numfy)):

                    temr = {str(yrs):{"yrs":yearlist[yrs],}}


                    years.update(copy.deepcopy(temr))





                if rspflag:
                    rspdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='rspm')
                    dell=0

                    for j in range(len(rspdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}
                            rspobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='rspm',loco_type=rspdobj[j].loco_type)
                            if len(rspobj)==0:
                                v='-'
                                bq='-'
                            else:
                                v=rspobj[0].target_quantity
                                bq=rspobj[0].buffer_quantity

                                if len(v)==0:
                                    v='-'

                                if len(bq)==0:
                                    bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None


                        dictname="dict"
                        temper = {str(j):{"loty":rspdobj[j].loco_type,
                                      "dict":diiict,}}
                       

                        j=j+1
                       
                        rspdictemper.update(copy.deepcopy(temper))


                if rspitmflag:
                    rspitmdobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=rev,customer='rspitm')
                    dell=0

                    for j in range(len(rspitmdobj)):
                        
                        for kill in range(int(numfy)):
                            dct={}

                            rspitmobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=rev,customer='rspitm',loco_type=rspitmdobj[j].loco_type)
                            if len(rspitmobj)==0:
                                v='-'
                                bq='-'
                            else:
                                v=rspitmobj[0].target_quantity
                                bq=rspitmobj[0].buffer_quantity

                                if len(v)==0:
                                    v='-'

                                if len(bq)==0:
                                    bq='-'
                            

                            dct["yrtq"]=v
                            dct["yrbq"]=bq
                            diiict[(str(kill))]=dct

                            

                            dct=None


                        dictname="dict"
                        temper = {str(j):{"loty":rspitmdobj[j].loco_type,
                                      "dict":diiict,}}

                        j=j+1
                       
                        rspitmdictemper.update(copy.deepcopy(temper))
            if flag or nrcflag or expflag or zrflag or zroverflag or rspflag or rspitmflag or nrcdgflag or zrasflag:
                data=1


            maijp=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='main')
            if len(maijp)!=0:
                finalvalue=maijp[0].finalval



            lidict={0:'loty',1:'yr1',2:'yr3',3:'yr4'}
            colsapn=int(cspan)+2
            if rev==0:
                heading="Production Programme for "
            else:
                heading="Revised Production Programme for "
            for kt,v in years.items():
                heading=heading+str(v['yrs'])+", "
            heading=heading+" is indicated below :"

            jpoobj=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='main')
            if len(jpoobj):
                numfy=jpoobj[0].numyrs
                cspan=numfy
                dt=jpoobj[0].date
                sub=jpoobj[0].subject
                numfy=jpoobj[0].numyrs
                ref=jpoobj[0].reference
                mjalt=jpoobj[0].majoralt
                formno=jpoobj[0].formno
                number=jpoobj[0].number
                headalt=jpoobj[0].headmjr
                if ref is not None:
                    reflist=findthis(request,ref)
                if mjalt is not None:
                    altrlist=findthis(request,mjalt)
            jpob=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='main')
            jpoc=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='rsp')
            if len(jpob):
                remk1=jpob[0].remark
            if len(jpoc):
                remk2=jpoc[0].remark
            spclremlist=[]
            nrmllist=[]
            if remk1 is not None:
                remklist=findthis(request,remk1)
            for str2 in remklist:
                if len(str2.split('$'))>1:
                    spclremlist.append(str2)
                elif len(str2.split('*'))>1:
                    spclremlist.append(str2)
                else:
                    nrmllist.append(str2)
            if remk2 is not None:
                remklist=findthis(request,remk2)
            for str2 in remklist:
                if len(str2.split('$'))>1:
                    spclremlist.append(str2)
                elif len(str2.split('*'))>1:
                    spclremlist.append(str2)
                else:
                    nrmllist.append(str2)

            context={
            "data":data,"data2":datadic,"data3":nrc,"data4":exp,"data5":dgs,"data8":zrzr,"data9":zozo,"jpo":2,"rev":rev,"jpoo":jpoo,"finalvalue":finalvalue,
            "listname":listname,"lidict":lidict,
            "years":years,"dictemper":dictemper,"nrcdictemper":nrcdictemper,"expdictemper":expdictemper,"zrdictemper":zrdictemper,"zroverdictemper":zroverdictemper,"zrasdictemper":zrasdictemper,
            "nrcdgdictemper":nrcdgdictemper,"nrcdgflag":nrcdgflag,"zrasflag":zrasflag,
            "nrcflag":nrcflag,"flag":flag,"expflag":expflag,"zrflag":zrflag,"zroverflag":zroverflag,

            "colsapn":colsapn,"bufcspan":int(cspan),
            "nrcrwspan":nrcrwspan,"nrcdgrwspan":nrcdgrwspan,"indrwspan":indrwspan,"exprwspan":exprwspan,"zrrwspan":zrrwspan,"zroverrwspan":zroverrwspan,"zrasrwspan":zrasrwspan,
            "total":total,
            "rspdictemper":rspdictemper,"rspitmdictemper":rspitmdictemper,
            "rspflag":rspflag,"rspitmflag":rspitmflag,
            "colsapn":colsapn,"bufcspan":int(cspan),
            "rsprwspan":rsprwspan,"rspitmrwspan":rspitmrwspan,'jpoo':jpoo,'rev':rev,
            "year1":yr,"year2":yr2,"year3":yr3,"year4":yr4,
            "toty1":ty1,"toty2":ty2,"toty3":ty3,"toty4":ty4,
            "pre":f,"n":j+1,'headalt':headalt,
            "pre2":nr,"n2":k+1,
            "pre3":ex,"n3":e+1,
            "pre4":dg,"n4":d+1,
            "pre7":zr,"n7":z+1,
            "pre8":zo,"n8":z2+1,
            'nav':g.nav,'dt':dt,'subject':sub,'rev':rev,
            'usermaster':g.usermaster,'ip':get_client_ip(request),
            'total':total,'subnav':g.subnav,
            'namelist':namelist,'desiglist':desiglist,'cdgp':range(cdgp),
            'number':number,'formno':formno,'subject':sub,'dt':dt,'heading':heading,
            'reflist':reflist,'altrlist':altrlist,'remklist':remklist,'spclremlist':spclremlist,
            'nrmllist':nrmllist,'revcnt':range(revcnt),
            }

        else:
            context={'nav':g.nav,'dt':dt,'subject':sub,'revcnt':range(revcnt),
            
        'usermaster':g.usermaster,'subnav':g.subnav,
        'ip':get_client_ip(request),
        'revision':rev,'namelist':namelist,'desiglist':desiglist,'cdgp':range(cdgp),}

 
    return render(request,"PPRODUCTION/JPO/jpoc.html",context)



