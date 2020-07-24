
from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/aprodplan/')
def bprodplan(request):
    from dlw.models import annual_production,jpo,namedgn,loconame,materialname
    existlen=0
    context={}
    dictemper={}
    yearlist=[]
    indrwspan=0
    years={}
    flagg=1
    diiict={}
    dct={}
    tod = date.today()
    ft=int(tod.strftime("%Y"))
    ft2=ft+1
    ctp=str(ft)+'-'+str(ft2)
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=(g.usermaster).role.split(", ")
    
    context={
        'nav':g.nav,
        'subnav':g.subnav,
        'usermaster':g.usermaster,
        'ip':get_client_ip(request),
    }
    year=None
    cuser=request.user
    ruser=True
    num=0
    numfy=0
    objj=None
    objx=None
    dgp=0
    flag=0
    rcnt=0
    dt=None
    rmlist=[]
    reflist=[]
    dictt=jpo.objects.all().aggregate(Max('revisionid'))
    revex=dictt['revisionid__max']
    if revex is None:
            revex=0
    else:
        objx=jpo.objects.filter(revisionid=revex,jpo='main').exists()
        if objx is True:
            objx1=jpo.objects.filter(revisionid=revex,jpo='main',finalval=1).exists()
            objx2=jpo.objects.filter(revisionid=revex,jpo='rsp',finalval=1).exists()
            if objx1 is True or objx2 is True:
                revex=revex+1
    formno=0
    number=0
    mjalt=None
    headalt=None
    remk=None
    sub=None
    ref=None
    context={
              'nav':g.nav,
              'revex':revex,
              'usermaster':g.usermaster,
              'ip':get_client_ip(request),
              'ruser':ruser,'ref':ref,
              'yup':True,
              'Manpower':"Manpower",
              'Account':"Account",
              'Add':"Add",
              'Role':rolelist[0],
              'cyear':ctp,
              'numfy':'-','dgp':'-','flag':flag,'existlen':0,
              'subnav':g.subnav,
            }
    lcname=loco(request)
    mtname=material(request)
    if request.method=="POST":
        flag=0
        dicn={}
        bval=request.POST.get('proceed')
        save=request.POST.get('save')
        typec=request.POST.get('type')
        if (bval==None and save==None):
            save="Save"
        dgp=request.POST.get('dgp')
        if dgp is None:
            cnt=0
        else:
            cnt=int(dgp)
        typenew=typec
        if(typec== "ind-rail" ):
            typenew="Indian Railway Loco"
        elif(typec == "zrover"):
            typenew="ZR Overhauling"
        elif(typec=="rspitm"):
            typenew="RSP Items"
        elif(typec=="rspm"):
            typenew="RSP Manufacturing"
        elif(typec == "zr"):
            typenew="ZR"
        elif(typec=="export"):
            typenew="Export"
        elif(typec=="nrc"):
            typenew="NRC"
        
        if typec=='ind-rail' or typec=='nrc' or typec=='export' or typec=='nrcdgset' or typec=='zr' or typec=='zrover' or typec=='zrasstn':
            jpot='main'
            iammain=1
        else:
            jpot='rsp'
            iammain=0
        if revex==0:
            revf=0
        else:
            pp=jpo.objects.filter(revisionid=revex,jpo=jpot).exists()
            if pp:
                revf=revex
            else:
                revf=revex-1
        objc=jpo.objects.filter(revisionid=revf,jpo=jpot).exists()
        if objc is True:
            objp=jpo.objects.filter(revisionid=revf,jpo=jpot)
            if len(objp):
                formno=objp[0].formno
                number=objp[0].number
                sub=objp[0].subject
                ref=objp[0].reference
                mjalt=objp[0].majoralt
                headalt=objp[0].headmjr
                remk=objp[0].remark
                dt=objp[0].date
        cnt=0
        if bval == "Proceed" :
            numfy1=0
            typec=request.POST.get('type')
            lcname2=set()
            abc=annual_production.objects.filter(revisionid=revf,customer=typec)
            for a in abc:
                lcname2.add(a.loco_type)
            lcname2=(list(lcname2))
            dt=request.POST.get('xTime')
            tod = date.today()
            ft=int(tod.strftime("%Y"))
            ft2=ft+1
            ctp=str(ft)+'-'+str(ft2)
            yr=ctp
            jpoobj=jpo.objects.filter(financial_year=yr,revisionid=revf,jpo=jpot)
            if len(jpoobj):
                numfy1=int(jpoobj[0].numyrs)
                cspan=numfy1
                dt=jpoobj[0].date
                sub=jpoobj[0].subject

            if numfy1==0 or numfy1 >= num:
                numfy1=int(num)
            numfy=request.POST.get("numfy")
            cspan=numfy
            tod = date.today()
            ft=int(tod.strftime("%Y"))
            ft2=ft+1
            for lol in range(int(numfy)):
                yearlist.append(str(ft)+'-'+str(ft2))
                ft=ft+1
                ft2=ft2+1

            for lol in range(int(numfy1)):
                indo=annual_production.objects.filter(financial_year=yearlist[lol],revisionid=revf,customer=typec)
                if len(indo)==0:
                    flagg=0

                elif len(indo)!=0 and indrwspan==0:
                    indrwspan=len(indo)+1

            for yrs in range(int(numfy)):

                temr = {str(yrs):{"yrs":yearlist[yrs],}}

                years.update(copy.deepcopy(temr))

            if flagg:
                indobj=annual_production.objects.filter(financial_year=yearlist[0],revisionid=revf,customer=typec)
                dell=0

                for j in range(len(indobj)):
                    
                    for kill in range(int(numfy)):
                        dct={}
                        inobj=annual_production.objects.filter(financial_year=yearlist[kill],revisionid=revf,customer=typec,loco_type=indobj[j].loco_type)
                        if len(inobj)!=0:
                        
                            v=inobj[0].target_quantity
                            bq=inobj[0].buffer_quantity

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

                    dictname="dict"
                    temper = {str(j):{"loty":indobj[j].loco_type,
                                    "dict":diiict,}}
                    

                    dictemper.update(copy.deepcopy(temper))
                    j=j+1

            objn=namedgn.objects.filter(revision=revf)
            namedg={}
            k=0
            diff=int(dgp)-len(objn)
            if diff>0:
                for j in range(len(objn)):
                    k=j
                    temp={str(j):{"name":objn[j].namep,
                                "dgn":objn[j].design,}}
                    namedg.update(copy.deepcopy(temp))
                k=k+1
                for j in range(k,(k+diff)):
                    temp1={str(j):{"name":"","dgn":"",}}
                    namedg.update(copy.deepcopy(temp1))
            elif diff==0:
                for j in range(len(objn)):
                    temp={str(j):{"name":objn[j].namep,
                                "dgn":objn[j].design,}}
                    namedg.update(copy.deepcopy(temp))
            else:
                for j in range(int(dgp)):
                    temp={str(j):{"name":objn[j].namep,
                                "dgn":objn[j].design,}}
                    namedg.update(copy.deepcopy(temp))
            flag=1
            existlen=(len(dictemper))
            context={
                        'user':cuser,
                        'ruser':ruser,
                        'yup':True,
                        'Manpower':"Manpower",
                        'Account':"Account",
                        'Add':"Add",
                        'nav':g.nav,
                        'subnav':g.subnav,
                        'Role':rolelist[0],
                        'value': range(5),
                        'typec':typec,
                        'typed':typenew,'numfy':numfy,'dgp':dgp,
                        'cyear':ctp,'ref':ref,'mjalt':mjalt,'remk':remk,'headalt':headalt,
                        'val':range(3),'iammain':iammain,
                        'revex':revex,
                        'usermaster':g.usermaster,'cnt':range(cnt),
                        'ip':get_client_ip(request),
                        'loconame':lcname,'matrname':mtname,'flag':flag,
                        'delcname':lcname2,'existlen':existlen,
                        'rcnt':rcnt,'dictemper':dictemper,'rev':revex,
                        'formno':formno,'number':number,'sub':sub,'dt':dt,'namedg':namedg,
                        "years":years,"cspan":int(cspan)+1,"bufcspan":cspan,
                    }
        elif(save=="Save"):
            nmdgn={}
            dgp=request.POST.get('dgp')
            cnt=int(dgp)+1
            temp1="namep"
            temp2="desig"
            temp3="remk"
            namelist=[]
            desiglist=[]
            rnamelist=[]
            for i in range(1,cnt):
                temp1=temp1+str(i)
                temp2=temp2+str(i)
                namelist.append(temp1)
                desiglist.append(temp2)
                temp1="namep"
                temp2="desig"
            for key in request.POST:
                for (a,b) in zip(namelist,desiglist):
                    if key==a or key==b:
                        nmdgn[request.POST[a]]=request.POST[b]
            new=0
            rem=0
            num=0
            rem_num=0
            ref_num=0
            remlist=[]
            reflist=[]
            rev=request.POST.get("rev")
            typ=request.POST.get("typec")
            num=request.POST.get("num")
            ref=request.POST.get("ref")
            formno=request.POST.get('formno')
            number=request.POST.get('number')
            dt=request.POST.get('xTime')
            remk=request.POST.get('remk')
            mjalt=request.POST.get('mjalt')
            headalt=request.POST.get('headalt')
            ob=namedgn.objects.filter(revision=rev)
            indx=len(ob)
            if indx==0:
                for k,v in nmdgn.items():
                    obj1=namedgn.objects.create()
                    obj1.namep=k
                    obj1.design=v
                    obj1.revision=rev
                    obj1.save()
            elif len(ob)==int(dgp):
                i=0
                for k,v in nmdgn.items():
                    ob[i].namep=k
                    ob[i].design=v
                    ob[i].revision=rev
                    ob[i].save()
                    i=i+1
            else:
                ob=namedgn.objects.filter(revision=rev).delete()
                i=0
                for k,v in nmdgn.items():
                    obj1=namedgn.objects.create()
                    obj1.namep=k
                    obj1.design=v
                    obj1.revision=rev
                    obj1.save()

            obj1=None
            if num!='THE OUTPUT OF PRODUCT FUNCTION' or num is None:
                new=int(num)

            nfy=int(request.POST.get("numfy"))
            sub=request.POST.get("sub")
            ref=request.POST.get('refrn')


            delm=request.POST.get("num_del")
            del_num=0
            if delm!='THE OUTPUT OF DEL FUNCTION' and delm!=None:
                del_num=int(request.POST.get("num_del"))     

            tod = date.today()
            ft=int(tod.strftime("%Y"))
            ft2=ft+1
            ctp=str(ft)+'-'+str(ft2)
            if typ=='ind-rail' or typ=='nrc' or typ=='export' or typ=='nrcdgset' or typ=='zr' or typ=='zrover' or typ=='zrasstn':

                nl=request.POST.get('num_of_loco')
                num_loco=0
                if(nl is not None):
                    num_loco=nl
                nf=request.POST.get('num_of_numfy')
                num_fy=0
                if(nf is not None):
                    num_fy=nfy
                tod = date.today()
                ft=int(tod.strftime("%Y"))
                ft2=ft+1

                yearr=[]
                for dq in range(1,int(num_fy)+1):
                    ctp=str(ft)+'-'+str(ft2)
                    yearr.append(ctp)
                    ft=ft+1
                    ft2=ft2+1
                deledit=annual_production.objects.filter(customer=typ,revisionid=rev).delete()
                for lo in range(0,int(num_loco)):

                    for nf in range(1,int(num_fy)+1):
                        if(request.POST.get("edit"+str(lo)+str(1))!=None):
                            if len(request.POST.get("edit"+str(lo)+str(1))) and (request.POST.get("edit"+str(lo)+str(1))) is not None:
                                credit=annual_production.objects.create()
                                credit.financial_year=yearr[nf-1]
                                credit.revisionid=rev
                                credit.customer=typ
                                credit.loco_type=request.POST.get("editloconame"+str(lo+1))
                                credit.target_quantity=request.POST.get("edit"+str(lo)+str(nf))
                                credit.buffer_quantity=request.POST.get("editbf"+str(lo)+str(nf))
                                credit.save()


                loconame="delname"
                
                for k in range(1,del_num+1):
                    for j in range(1,nfy+1):
                        o=annual_production.objects.filter(financial_year=yearr[j-1],revisionid=rev,customer=typ,loco_type=request.POST.get(loconame+str(k)))
                        if len(o)!=0:
                            o.delete()


                tod = date.today()
                ft=int(tod.strftime("%Y"))
                ft2=ft+1
                ctp=str(ft)+'-'+str(ft2)
                subobj=jpo.objects.filter(financial_year=ctp,revisionid=rev,jpo='main')
                indx=len(subobj)
                if len(subobj)==0 and (sub is not None) and (ref is not None):
                    sobj=jpo.objects.create()
                    sobj.financial_year=ctp
                    sobj.revisionid=rev
                    sobj.jpo='main'
                    if "Dy_CME/Plg" in rolelist:
                        sobj.subject=sub
                        sobj.reference=ref
                    sobj.date=dt
                    sobj.numyrs=nfy
                    sobj.numdgp=dgp
                    sobj.formno=formno
                    sobj.number=number
                    sobj.remark=remk
                    sobj.majoralt=mjalt
                    sobj.headmjr=headalt
                    sobj.save()
                else:
                    if "Dy_CME/Plg" in rolelist:
                        subobj[0].subject=sub
                        subobj[0].reference=ref
                    subobj[0].date=dt
                    subobj[0].numyrs=nfy
                    subobj[0].numdgp=dgp
                    subobj[0].formno=formno
                    subobj[0].number=number
                    subobj[0].remark=remk
                    subobj[0].headmjr=headalt
                    subobj[0].majoralt=mjalt
                    subobj[0].save()


            elif typ=='rspm' or typ=='rspitm':

                num_loco=request.POST.get('num_of_loco')
                num_fy=request.POST.get('numfy')
                tod = date.today()
                ft=int(tod.strftime("%Y"))
                ft2=ft+1

                yearr=[]
                for dq in range(1,int(num_fy)+1):
                    ctp=str(ft)+'-'+str(ft2)
                    yearr.append(ctp)
                    ft=ft+1
                    ft2=ft2+1

                deledit=annual_production.objects.filter(customer=typ,revisionid=rev).delete()
                

                for lo in range(0,int(num_loco)):
                    for nf in range(1,int(num_fy)+1):
                        if(request.POST.get("edit"+str(lo)+str(1))!=None):
                            if len(request.POST.get("edit"+str(lo)+str(1))) and (request.POST.get("edit"+str(lo)+str(1))) is not None:
               
                                credit=annual_production.objects.create()
                                credit.financial_year=yearr[nf-1]
                                credit.revisionid=rev
                                credit.customer=typ
                                credit.loco_type=request.POST.get("editloconame"+str(lo+1))
                                
                                if(request.POST.get("edit"+str(lo)+str(nf))==None):
                                    credit.target_quantity='-'
                                else:
                                    credit.target_quantity=request.POST.get("edit"+str(lo)+str(nf))
                                credit.buffer_quantity='-'
                                

                                credit.save()
           



                loconame="delname"
                
                for k in range(1,del_num+1):
                    for j in range(1,nfy+1):
                        o=annual_production.objects.filter(financial_year=yearr[j-1],revisionid=rev,customer=typ,loco_type=request.POST.get(loconame+str(k)))
                        if len(o)!=0:
                            o.delete()


                tod = date.today()
                ft=int(tod.strftime("%Y"))
                ft2=ft+1
                ctp=str(ft)+'-'+str(ft2)
                subobj=jpo.objects.filter(financial_year=ctp,revisionid=rev,jpo='rsp')
                if len(subobj)==0 and (sub is not None):
                    sobj=jpo.objects.create()
                    sobj.financial_year=ctp
                    sobj.revisionid=rev
                    sobj.jpo='rsp'
                    if "Dy_CME/Plg" in rolelist:
                        sobj.subject=sub
                        sobj.reference=ref
                    sobj.date=dt
                    sobj.numyrs=nfy
                    sobj.numdgp=dgp
                    sobj.remark=remk
                    sobj.majoralt=mjalt
                    sobj.formno=formno
                    sobj.number=number
                    sobj.save()
                else:
                    if "Dy_CME/Plg" in rolelist:
                        subobj[0].subject=sub
                        subobj[0].reference=ref
                    subobj[0].date=dt
                    subobj[0].numyrs=nfy
                    subobj[0].numdgp=dgp
                    subobj[0].formno=formno
                    subobj[0].number=number
                    subobj[0].remark=remk
                    subobj[0].majoralt=mjalt
                    subobj[0].save()

            
            nl=[]
            rma=[]

            qunat=[]
            qunatb=[]
            qt="quantity"
            qtb="quantityb"
            loconame="name"

            tod = date.today()
            ft=int(tod.strftime("%Y"))
            ft2=ft+1

            yearr=[]
            for dq in range(1,nfy+1):
                ctp=str(ft)+'-'+str(ft2)
                yearr.append(ctp)
                ft=ft+1
                ft2=ft2+1



            for k in range(1,new+1):
                for j in range(1,nfy+1):


                    qtname=qt+str(k)+str(j)
                    qtbuffname=qtb+str(k)+str(j)
                    if(request.POST.get(loconame+str(k))!=None):
                        if len(request.POST.get(loconame+str(k))) and (request.POST.get(loconame+str(k))) is not None:

                            o=annual_production.objects.create()
                            o.financial_year=yearr[j-1]
                            o.target_quantity=request.POST.get(qtname)
                            if request.POST.get("typec")=='rspitm' or request.POST.get("typec")=='rspm':
                                o.buffer_quantity='-'
                            else:
                                o.buffer_quantity=request.POST.get(qtbuffname)
                            temp=request.POST.get(loconame+str(k))
                            o.loco_type=temp.upper()
                            o.revisionid=int(request.POST.get("rev"))
                            o.customer=request.POST.get("typec")
                            o.save()
                            messages.success(request, 'Successfully Created!')
                            o=None
    return render(request,'PPRODUCTION/ANNUALPRODUCTION/newaprodplan.html',context)

def loco(request):
    from dlw.models import loconame
    lcname=[]
    objy=loconame.objects.all()
    for o in objy:
        if (o.loconame):
            lcname.append(o.loconame)
    return lcname

def material(request):
    from dlw.models import materialname
    lcname=[]
    objy=materialname.objects.all()
    for o in objy:
        if (o.matrname):
            lcname.append(o.matrname)
    return lcname