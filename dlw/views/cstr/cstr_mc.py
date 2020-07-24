from dlw.views import *
import dlw.views.globals as g
def cstrmc_getRegno(request):
    if request.method=="GET" and request.is_ajax():
        chind = request.GET.get('c')
        myval=list(Cnote.objects.filter(chg_ind=chind).values('ppl_cn_no','reg_no').order_by('-ppl_cn_no'))[:1]
        
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def cstrmc_getslno(request):
    if request.method=="GET" and request.is_ajax():
        chind = request.GET.get('c')
        
        pplno = request.GET.get('p')
        
        myval=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind).values('slno').order_by('-slno'))
        
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def cstrmc_getepc(request):
    if request.method=="GET" and request.is_ajax():
        epc = request.GET.get('epc')
        
        myval=list(Code.objects.filter(code=epc).values('cd_type','code','alpha_1','num_1'))
        
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)


def cstrmc_getcompo(request):
    if request.method=="GET" and request.is_ajax():
        compo = request.GET.get('compo')
        
        myval=list(Part.objects.filter(partno=compo).values('des','ptc','shop_ut','drgno','m14splt_cd','allow_perc'))
        
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def cstrmc_explo(request):
    if request.method=="GET" and request.is_ajax():
        epart = request.GET.get('epart')
        
        myval=list(Nstr.objects.filter(pp_part=epart).values('pp_part','cp_part','ptc','l_fr','l_to','epc','qty'))
        
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)


def cstrmc_implo(request):
    if request.method=="GET" and request.is_ajax():
        ipart = request.GET.get('ipart')
        
        myval=list(Nstr.objects.filter(cp_part=ipart).values('pp_part','cp_part','ptc','l_fr','l_to','epc','qty'))
        
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)


def cstrmc_getAblyno(request):
    if request.method=="GET" and request.is_ajax():
        aslno= request.GET.get('c')
        
        myval=list(Part.objects.filter(partno=aslno).values('partno','des'))
        
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)


def cstrmc_deldata(request):
    if request.method=="GET" and request.is_ajax():
        chind = request.GET.get('cnind')
        
        pplno = request.GET.get('pplno')
        slno = request.GET.get('slno')
        
        Cstr.objects.filter(slno=slno,cn_no=pplno,chg_ind=chind).update(del_fl='Y')
        print("UPDATE")                                                                                             
        cnlist=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind).exclude(del_fl='Y').values('slno','chg_ind','reg_no','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','ref_ind','status','ref_no','cutdia_no','cn_no','cn_date','acd','updt_dt').order_by('slno'))
        
        return JsonResponse(cnlist, safe = False)
    return JsonResponse({"success":False}, status=400)

def cstrmc_Rep_PSE(request):
    if request.method=="GET" and request.is_ajax():
        chind = request.GET.get('cind')
        
        pplno = request.GET.get('pplno')
        status = request.GET.get('status')
        cnlist=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind).exclude(del_fl='Y').values('slno','chg_ind','reg_no','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','ref_ind','status','ref_no','cutdia_no','cn_no','cn_date','acd','updt_dt').order_by('slno'))
        
        data={
                'cnlists':cnlist, 
            }
            
        pdf = render_to_pdf('cstrmc_rep_pse.html',data)
        return HttpResponse(pdf, content_type='application/pdf')
        
    return JsonResponse({"success":False}, status=400)


def cstrmc_getdata(request):
    if request.method=="GET" and request.is_ajax():
        chind = request.GET.get('cnind')
        
        pplno = request.GET.get('pplno')
        slno = request.GET.get('slno')
        
        cnlist=list(Cstr.objects.filter(slno=slno,cn_no=pplno,chg_ind=chind).values('slno','chg_ind','reg_no','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','ref_ind','status','ref_no','cutdia_no','cn_no','cn_date','acd','updt_dt').order_by('slno'))
        partno=cnlist[0]['cp_part'].strip()
        mypart=list(Part.objects.filter(partno=partno).values('des'))
        if len(mypart)==0:
            mypart=list(Cpart.objects.filter(partno=partno).values('des'))
        data = {
            'cnlist':cnlist,
            'des':mypart[0]['des'].strip(),
        }
        
        return JsonResponse({'data':data}, safe = False)
    return JsonResponse({"success":False}, status=400)



def cstrmc_savecpart(request):
    if request.method=="POST" and request.is_ajax():
        
        pplno = request.POST.get('p')
        cpart = request.POST.get('spart')
        sm14 = request.POST.get('sm14')
        sdrgno = request.POST.get('sdrgno')
        sshop_ut = request.POST.get('sshop_ut')
        ptc = request.POST.get('sptc')
        sdes = request.POST.get('sdes')
        salperc = request.POST.get('salperc')
        
        cpartlist=list(Cpart.objects.filter(ppl_cn_no=pplno,partno=cpart).values('slno','reg_no','partno','ppl_cn_no'))
        if len(cpartlist)==0:
            print("no record")
            cpartlist1=list(Cpart.objects.filter(ppl_cn_no=pplno).values('slno').order_by('-slno'))
            if len(cpartlist1)!=0:
                
                sn=len(cpartlist1)
                sn=sn+1
            else:
                sn=1
            
            
            Cpart.objects.create(slno=sn,ppl_cn_no=pplno,partno=cpart,m14splt_cd=sm14,drgno=sdrgno,shop_ut=sshop_ut,ptc=ptc,des=sdes,allow_perc=salperc,updt_dt=datetime.datetime.now())
            
            return JsonResponse("save", safe = False)
    return JsonResponse({"success":False}, status=400)


def cstrmc_savenewReg(request):
    if request.method=="POST" and request.is_ajax():
        cnind=request.POST.get('cind')
        ppl_no=request.POST.get('ppl_no')

        if (request.POST.get('Reg_date') !=''):
            Reg_date=datetime.datetime.strptime(request.POST.get('Reg_date'),'%d-%m-%Y').date()
        else:
            Reg_date=''
        Ref1=request.POST.get('Ref1')
        if(request.POST.get('ref_date1')!=''):
            ref_date1=datetime.datetime.strptime(request.POST.get('ref_date1'),'%d-%m-%Y').date()
        else:
            ref_date1=''
        Ref2=request.POST.get('Ref2')
        if(request.POST.get('ref_date2')!=''):
            ref_date2=datetime.datetime.strptime(request.POST.get('ref_date2'),'%d-%m-%Y').date()
        else:
            ref_date2=''
        
        assly_no=request.POST.get('assly_no')
        desc=request.POST.get('desc')
        lett_no=request.POST.get('lett_no')
        if(request.POST.get('L_date')!=''):
            L_date=datetime.datetime.strptime(request.POST.get('L_date'),'%d-%m-%Y').date()
        else:
            L_date=''
        fd=request.POST.get('fd')
        std=request.POST.get('std')
        name=request.POST.get('name')
        
        status='U'
        copy1=request.POST.get('copy1')
        copy2=request.POST.get('copy2')
        copy3=request.POST.get('copy3')
        encl=request.POST.get('encl')
        matter=request.POST.get('matter')
        
        Cnote.objects.create(chg_ind=cnind,reg_dt=Reg_date,ref_1=Ref1,ref_2=Ref2,ppl_cn_no=ppl_no,lett_no=lett_no,status=status,lett_matt=matter,cn_dt=L_date,from_name=name,from_desig=fd,to_desig=std,copyto_1=copy1,copyto_2=copy2,copyto_3=copy3,encl=encl,assly_no=assly_no,assly_desc=desc)
        return JsonResponse("save", safe = False)
    return JsonResponse({"success":False}, status=400)    

def cstrmc_savedata(request):
    if request.method=="GET" and request.is_ajax():
        chind = request.GET.get('c')
        
        pplno = request.GET.get('p')
        slno = request.GET.get('slno')
        acd = request.GET.get('acd')
        epc = request.GET.get('epc')
        ptc = request.GET.get('ptc')
        locofr = request.GET.get('locofr')
        locoto = request.GET.get('locoto')
        pp_part = request.GET.get('pp')
        cp_part = request.GET.get('compo')
        qty = request.GET.get('qty')
        cutno = request.GET.get('cutno')
        partlst=list(Part.objects.filter(partno=cp_part).values('partno','des'))
        if len(partlst)>0:
            myval=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind,acd=acd,l_fr=locofr,l_to=locoto,pp_part=pp_part,cp_part=cp_part).exclude(del_fl='Y').values('slno','cp_part','pp_part'))
            if len(myval)==0:
                Cstr.objects.create(cn_no=pplno,chg_ind=chind,slno=slno,acd=acd,ptc=ptc,l_fr=locofr,l_to=locoto,pp_part=pp_part,cp_part=cp_part,qty=qty,cutdia_no=cutno,epc=epc)
                
                cnlist=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind).exclude(del_fl='Y').values('slno','chg_ind','reg_no','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','ref_ind','status','ref_no','cutdia_no','cn_no','cn_date','acd','updt_dt').order_by('slno'))
                
                return JsonResponse(cnlist, safe = False)
            else:
                print('already')
                return JsonResponse({"success":False}, status=400)
        else:
            cpartlst=list(Cpart.objects.filter(ppl_cn_no=pplno,partno=cp_part).values('partno','des'))
            if len(cpartlst)>0:
                myval=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind,acd=acd,l_fr=locofr,l_to=locoto,pp_part=pp_part,cp_part=cp_part).exclude(del_fl='Y').values('slno','cp_part','pp_part'))
                if len(myval)==0:
                    Cstr.objects.create(cn_no=pplno,chg_ind=chind,slno=slno,acd=acd,ptc=ptc,l_fr=locofr,l_to=locoto,pp_part=pp_part,cp_part=cp_part,qty=qty,cutdia_no=cutno,epc=epc)
                    Cpart.objects.filter(ppl_cn_no=pplno,partno=cp_part).exclude(del_fl='Y').update(acd=acd)
                    print("update data cpart")
                    cnlist=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind).exclude(del_fl='Y').values('slno','chg_ind','reg_no','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','ref_ind','status','ref_no','cutdia_no','cn_no','cn_date','acd','updt_dt').order_by('slno'))
                    
                    return JsonResponse(cnlist, safe = False)

    return JsonResponse({"success":False}, status=400)

def cstrmc_editdata(request):
    if request.method=="GET" and request.is_ajax():
        chind = request.GET.get('c')
        
        pplno = request.GET.get('p')
        slno = request.GET.get('slno')
        acd = request.GET.get('acd')
        epc = request.GET.get('epc')
        ptc = request.GET.get('ptc')
        locofr = request.GET.get('locofr')
        locoto = request.GET.get('locoto')
        pp_part = request.GET.get('pp')
        cp_part = request.GET.get('compo')
        qty = request.GET.get('qty')
        cutno = request.GET.get('cutno')
        d1 = datetime.date.today()
        
        partlst=list(Part.objects.filter(partno=cp_part).values('partno','des'))
        if len(partlst)>0:
            Cstr.objects.filter(cn_no=pplno,chg_ind=chind,slno=slno).update(acd=acd,ptc=ptc,l_fr=locofr,l_to=locoto,pp_part=pp_part,cp_part=cp_part,qty=qty,cutdia_no=cutno,epc=epc,updt_dt=d1)
            print("update data")
            cnlist=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind).exclude(del_fl='Y').values('slno','chg_ind','reg_no','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','ref_ind','status','ref_no','cutdia_no','cn_no','cn_date','acd','updt_dt').order_by('slno'))
            
            return JsonResponse(cnlist, safe = False)
        else:
            cpartlst=list(Cpart.objects.filter(ppl_cn_no=pplno,partno=cp_part).values('partno','des'))
            if len(cpartlst)>0:
                Cstr.objects.filter(cn_no=pplno,chg_ind=chind,slno=slno).update(acd=acd,ptc=ptc,l_fr=locofr,l_to=locoto,pp_part=pp_part,cp_part=cp_part,qty=qty,cutdia_no=cutno,epc=epc,updt_dt=d1)
                Cpart.objects.filter(ppl_cn_no=pplno,partno=cp_part).exclude(del_fl='Y').update(acd=acd,updt_dt=d1)
                print("update data cpart")
                cnlist=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind).exclude(del_fl='Y').values('slno','chg_ind','reg_no','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','ref_ind','status','ref_no','cutdia_no','cn_no','cn_date','acd','updt_dt').order_by('slno'))
                
                return JsonResponse(cnlist, safe = False)

    return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/cstrmc/')
def cstrmc(request):
    
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'subnav':g.subnav,
        'ip':get_client_ip(request),
        'usermaster':g.usermaster,
    } 
    if(request.method=="POST"):
        submitvalue = request.POST.get('btnpost')
        print("post val ", submitvalue) 
        if(submitvalue=="inputstr"):
            cnind=request.POST.get('cn_ind')
            pplno=request.POST.get('ppl')
            print("Fetch the data", cnind, pplno)
            cnlist=list(Cnote.objects.filter(chg_ind=cnind,ppl_cn_no=pplno).values('chg_ind','reg_no','reg_dt','ref_1','ref_1_dt','ref_2','ref_2_dt','ppl_cn_no','cn_reg_dt','cn_dt','lett_no','status','lett_matt','lett_no','from_name','from_desig','to_desig','copyto_1','copyto_2','copyto_3','encl','assly_no','assly_desc'))[:1]
            if len(cnlist)==0:
                print("no record")
            else:
                context={
                    'sub':0,
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'cnlists':cnlist,
                    'usermaster':g.usermaster,
                } 
                    
        elif(submitvalue=="process"):
            cnind=request.POST.get('pcind')
            
            pplno=request.POST.get('ppplno')
            status='Y'
            Cnote.objects.filter(chg_ind=cnind,ppl_cn_no=pplno).update(status=status)
        elif(submitvalue=="update"):
            cnind=request.POST.get('rcind')
            ppl_no=request.POST.get('rppl_no')

            print("val :",request.POST.get('rReg_date'))
            Reg_date=request.POST.get('rReg_date')

            
            if(Reg_date == '' or Reg_date is None):
                Reg_date=None
            else:
                Reg_date=datetime.datetime.strptime(Reg_date,'%d-%m-%Y').date()
                
            
            Ref1=request.POST.get('rRef1')
            ref_date1=request.POST.get('rref_date1')
            if(ref_date1 =='' or ref_date1 is None):
                ref_date1=None
            else:
                ref_date1=datetime.datetime.strptime(ref_date1,'%d-%m-%Y').date()
            print("test",ref_date1)
            Ref2=request.POST.get('rRef2')
            ref_date2=request.POST.get('rref_date2')
            if(ref_date2 =='' or ref_date2 is None):
                ref_date2=None
            else:
                ref_date2=datetime.datetime.strptime(ref_date2,'%d-%m-%Y').date()
            assly_no=request.POST.get('rassly_no')
            desc=request.POST.get('rdesc')
            lett_no=request.POST.get('rletno')
            lett_dt=request.POST.get('rletdt')
            print("lett_dt :",request.POST.get('rletdt'))
            print("value of  lett_dt: ",lett_dt)
            if(lett_dt =='' or lett_dt is None):
                lett_dt=None
            else:
                lett_dt=datetime.datetime.strptime(lett_dt,'%d-%m-%Y').date()
            fd=request.POST.get('rfd')
            std=request.POST.get('rstd')
            name=request.POST.get('rnn')
            status=request.POST.get('rstatus')
            copy1=request.POST.get('rcopy1')
            copy2=request.POST.get('rcopy2')
            copy3=request.POST.get('rcopy3')
            encl=request.POST.get('rencl')
            matter=request.POST.get('rmatter')
            Cnote.objects.filter(chg_ind=cnind,ppl_cn_no=ppl_no).update(reg_dt=Reg_date,ref_1=Ref1,ref_1_dt=ref_date1,ref_2=Ref2,ref_2_dt=ref_date2,ppl_cn_no=ppl_no,lett_no=lett_no,status=status,lett_matt=matter,cn_dt=lett_dt,from_name=name,from_desig=fd,to_desig=std,copyto_1=copy1,copyto_2=copy2,copyto_3=copy3,encl=encl,assly_no=assly_no,assly_desc=desc)
            print("Update the data into cnote table",cnind,ppl_no)
        elif(submitvalue=="detail"):
            cnind=request.POST.get('dcind')
            reg_no=request.POST.get('dreg_no')
            pplno=request.POST.get('dpplno')
            status=request.POST.get('dstatus')
            print("Fetch the data", cnind, pplno)
            cnlist=list(Cstr.objects.filter(cn_no=pplno,chg_ind=cnind).exclude(del_fl='Y').values('slno','chg_ind','reg_no','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','ref_ind','status','ref_no','cutdia_no','cn_no','cn_date','acd','updt_dt').order_by('slno'))
            if len(cnlist)==0:
                print("no record")
                context={
                    'sub':0,
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'cnind':cnind,
                    'reg_no':reg_no,
                    'pplno':pplno,
                    'status':status,
                    'usermaster':g.usermaster,
                } 
            else:
                context={
                    'sub':0,
                    'lenm' :2,
                    'nav':g.nav,
                    'subnav':g.subnav,
                    'ip':get_client_ip(request),
                    'cnlists':cnlist,
                    'cnind':cnind,
                    'reg_no':reg_no,
                    'pplno':pplno,
                    'status':status,
                    'usermaster':g.usermaster,
                } 
            
            return render(request, "CSTR/cstrmcdetail.html", context)
        elif(submitvalue=="RepPSE"):
            chind = request.POST.get('repcind')
            
            pplno = request.POST.get('reppplno')
            status = request.POST.get('repstatus')
            cnlist=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind).exclude(del_fl='Y').values('slno','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','status','cutdia_no','acd','updt_dt','errmsg').order_by('slno'))
            i=0
            while i<len(cnlist):
                cnlist[i]['l_fr']=cnlist[i]['l_fr'].strip().zfill(4)
                cnlist[i]['l_to']=cnlist[i]['l_to'].strip().zfill(4)
                i=i+1
            cnotelst=list(Cnote.objects.filter(chg_ind=chind,ppl_cn_no=pplno).values('chg_ind','reg_no','reg_dt','ref_1','ref_1_dt','ref_2','ref_2_dt','ppl_cn_no','cn_reg_dt','cn_dt','lett_no','status','lett_matt','lett_no','from_name','from_desig','to_desig','copyto_1','copyto_2','copyto_3','encl','assly_no','assly_desc'))
            
            data={
                    'cnlists':cnlist,
                    'cnotelist': cnotelst,
                }
                
            pdf = render_to_pdf('CSTR/cstrmc_rep_pse.html',data)
            return HttpResponse(pdf, content_type='application/pdf')
        elif(submitvalue=="RepPSI"):
            chind = request.POST.get('repcind')
            
            pplno = request.POST.get('reppplno')
            status = request.POST.get('repstatus')
            cnlist=list(Cstr.objects.filter(cn_no=pplno,chg_ind=chind).exclude(del_fl='Y').values('slno','pp_part','cp_part','l_fr','l_to','ptc','epc','qty','status','cutdia_no','acd','updt_dt',).order_by('slno'))
            i=0
            while i<len(cnlist):
                cnlist[i]['l_fr']=cnlist[i]['l_fr'].strip().zfill(4)
                cnlist[i]['l_to']=cnlist[i]['l_to'].strip().zfill(4)
                i=i+1
            cnotelst=list(Cnote.objects.filter(chg_ind=chind,ppl_cn_no=pplno).values('chg_ind','reg_no','reg_dt','ref_1','ref_1_dt','ref_2','ref_2_dt','ppl_cn_no','cn_reg_dt','cn_dt','lett_no','assly_no'))
            
            data={
                    'cnlists':cnlist,
                    'cnotelist': cnotelst,
                }
                
            pdf = render_to_pdf('CSTR/cstrmc_rep_psi.html',data)
            return HttpResponse(pdf, content_type='application/pdf')
        elif(submitvalue=="RepPME"):
            chind = request.POST.get('repcind')
            
            pplno = request.POST.get('reppplno')
            status = request.POST.get('repstatus')
            cnlist=list(Cpart.objects.filter(ppl_cn_no=pplno).exclude(del_fl='Y').values('slno','partno','des','drgno','spec','ptc','acd','shop_ut','status','errmsg','m14splt_cd','updt_dt').order_by('slno'))
            cnotelst=list(Cnote.objects.filter(chg_ind=chind,ppl_cn_no=pplno).values('chg_ind','reg_no','reg_dt','ref_1','ref_1_dt','ref_2','ref_2_dt','ppl_cn_no','cn_reg_dt','cn_dt','lett_no','assly_no'))
            
            data={
                    'cnlists':cnlist,
                    'cnotelist': cnotelst,
                }
                
            pdf = render_to_pdf('CETR/cstrmc_rep_pme.html',data)
            return HttpResponse(pdf, content_type='application/pdf')
        elif(submitvalue=="RepPMI"):
            chind = request.POST.get('repcind')
            
            pplno = request.POST.get('reppplno')
            status = request.POST.get('repstatus')
            cnlist=list(Cpart.objects.filter(ppl_cn_no=pplno).exclude(del_fl='Y').values('slno','partno','des','drgno','spec','ptc','acd','shop_ut','m14splt_cd','alt_link','allow_perc').order_by('slno'))
            cnotelst=list(Cnote.objects.filter(chg_ind=chind,ppl_cn_no=pplno).values('chg_ind','reg_no','reg_dt','ref_1','ref_1_dt','ref_2','ref_2_dt','ppl_cn_no','cn_reg_dt','cn_dt','lett_no','assly_no'))
            
            data={
                    'cnlists':cnlist,
                    'cnotelist': cnotelst,
                }
                
            pdf = render_to_pdf('CSTR/cstrmc_rep_pmi.html',data)
            return HttpResponse(pdf, content_type='application/pdf')
    return render(request, "CSTR/cstrmc.html", context)

