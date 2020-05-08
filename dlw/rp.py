from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date,datetime,timedelta,time
import time
import datetime,calendar
from calendar import monthrange
from array import array
from django.contrib.sessions.models import Session
from django.views.generic import View
from dlw.models import *
from dlw.serializers import testSerializer
import re,uuid,copy
from copy import deepcopy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import password_reset,password_reset_done
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from dlw.forms import UserRegisterForm
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from dlw.decorators import role_required
from django.db.models import Max
from django.http import HttpResponseRedirect
import math,random
from random import randint
import datetime
import smtplib 
from django.apps import apps
import json
import pandas
from django.db.models import Subquery
from django.db.models import Avg
from django.db.models import Sum
from django.db.models import Max
import numpy as np

session_ep1=''
session_meppart=0
session_ptc=''
session_outfile=pandas.DataFrame()
session_ep=''
session_epn=''
session_aimpl=None
session_curTime=''
session_lt=''
system_date=datetime.date.today()
outfile=pandas.DataFrame()
Ldbk=pandas.DataFrame()
aimpl=pandas.DataFrame()



def process():
    data_list4=list(Ptld.objects.values('part_no','ptc','p_desc','qty','epc','rem','drgno'))
    df=pandas.DataFrame(data_list4)    
    global Ldbk
    if(Ldbk.empty):
        Ldbk=CreateDataTableLdBk()

    assly = ""
    ep = ""
    ptc = ""
    qtya = ""
    mep_part = ""
    mcpq=""
    locofrom=""
    locoto="" 
    ls1=["P","Q","R"]   
    if(len(data_list4)>0):
        for i in range(len(data_list4)):
            assly=data_list4[i].get('part_no')
            ds1=list(Nstr.objects.filter(cp_part=assly,l_to='9999').values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by('cp_part','epc','pp_part'))
            if(len(ds1)>0):
                ep=data_list4[i].get('epc')
                global session_ep1
                session_ep1=ep
                tmpstr=list(Code.objects.filter(cd_type='11',code=ep).values('num_1'))
                if(len(tmpstr)>0):
                    mep_part=tmpstr[0].get('num_1')
                global session_meppart
                session_meppart=mep_part
                   
            qtya =str(data_list4[i].get('qty'))
            if (assly != mep_part):    
                mcpq = cpq(assly, ep, mep_part)
                ds5=list(Nstr.objects.filter(cp_part=assly,l_to='9999').values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by('cp_part','epc','pp_part'))
                if(len(ds5)<=0):
                    if(mcpq=="0"):
                        Ptld.objects.create(rem="Part Not in Structure for this End Product")
                        continue
                    else:
                        if session_ptc in ls1:
                            Ptld.objects.create(rem="Part is purchase/Raw material")
                            continue
            
            locofrom = "9999"
            locoto = "9999"
            sumexpl(assly, locofrom, locoto)
            club_assly_qty(qtya)
    global outfile       
    outfile=session_outfile
    if(outfile.empty):
        outfile=CreateDataTableFn()
       
    for i in range(len(data_list4)):
        mPartNo=''
        mDesc=''
        mQty=''
        mEpc=''
        mPtc=''
        mPtc=data_list4[i].get('ptc')
        ls= ['P','Q','R'] 
        if mPtc not in ls:
            continue
        mPartNo=df['part_no']
        mDesc=df['p_desc']
        mQty=df['qty']
        mEpc=df['epc']
        mPtc=df['ptc']
        AddDataToTableFn(mPartNo[i], mEpc[i],mDesc[i], mQty[i], "", "", "", "", "", "", "", mPtc[i])
    
    
    Ldbk=outfile.groupby("PART_NO").agg({'DESC':'max','QTY':'sum','PTC':'max'})
    return Ldbk

def club_assly_qty(qtya):
    partno=''
    desc=''
    qty=''
    epc=''
    ptc=''
    ds1=list(QtysumTemp.objects.filter(dt_run=system_date,cur_time=session_curTime).values('partno','ptc','qty','shop_ut','ptlf','ptlt','rm_part','rm_ptc','rm_qty','rm_ut','rmlf','rmlt','remark','qty_loco','dt_run','cur_time'))
    for i in range(len(ds1)):
        partno=ds1[i].get('partno')
        epc=session_ep1
        ds2=list(Part.objects.filter(partno=partno).values('des'))
        if(len(ds2)>0):
            desc=str(ds2[0].get('des'))
        qty=str(ds1[i].get('qty'))
        qty=str(float(qty)*float(qtya))
        ptc=str(ds1[i].get('ptc'))
        global outfile
        if(outfile.empty):
            outfile = CreateDataTableFn()
        AddDataToTableFn(partno, epc, desc, qty, "", "", "", "", "", "", "", ptc)    
    global session_outfile
    session_outfile = outfile
    

def cpq(pn,ep,epn):
    q=0
    if(aimpl.empty==False):
        aimpl.drop(aimpl.index, inplace=True)
    ds=list(Nstr.objects.filter(cp_part=pn,epc=ep,l_to='9999').values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by("cp_part","epc","pp_part"))
    if(len(ds)<=0):
        return "0"
    global session_ep
    global session_epn
    session_ep = ep
    session_epn = epn
    impl(pn,1)
    for i in range(len(aimpl)): 
        a=aimpl[i].get('0')
        b=aimpl[i].get('1')
        if(a==epn):
            q=q+int(b)       
    return str(q)



def impl(pn,wt):
    pp_part=''
    mpp_part=''
    ptc =''
    _epn=''
    qty=0
    dss=list(Nstr.objects.filter(cp_part=pn,epc=session_ep,l_to='9999').values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by("cp_part","epc","pp_part"))
    global session_aimpl
    global aimpl
    aimpl=session_aimpl
    if(aimpl==None):
        aimpl=CreateDataTableaImpl(2)
        session_aimpl=aimpl   
    _epn=str(session_epn) 
    for i in range(len(dss)):
        pp_part = ""
        qty = 0
        pp_part=str(dss[i].get('pp_part'))
        qty=float(dss[i].get('qty'))
        ptc=str(dss[i].get('ptc'))
        if(pp_part==_epn):
           AddDataToTable1(pp_part,(qty*wt),aimpl)  
        mpp_part=pp_part
        dss1=list(Nstr.objects.filter(cp_part=mpp_part,epc=session_ep,l_to='9999').values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by("cp_part","epc","pp_part"))
        ln=["M","Z","L","B"]
        if((len(dss1)>0) and (ptc in ln)):
            impl(mpp_part,qty*wt)
    return  



def sumexpl(assly, lf, lt):
    ep=""
    ds=list(Nstr.objects.filter(pp_part=assly).values("epc").order_by("pp_part","cp_part","epc","l_to"))
    df=pandas.DataFrame(ds)
    if(len(ds)<=0):
        return False   
    ep=df.at[0,'epc']
    session_ep=ep
    global system_date
    system_date=datetime.date.today()
    global session_curTime
    cur_time=datetime.datetime.now().strftime("%H%M%S")
    session_curTime=cur_time
    delQtySum_Temp1()
    global session_lt
    session_lt = "9999"
    insertQtySum_temp1(assly, "M", "1.000", "01", lf, lt)
    expl(assly, 1, ep)
    delQtySum_Temp2()
    appendQtySum_Temp2()
    delQtySum_Temp()
    summarizeQtySum_Temp(ep,session_meppart)
    return True


def qloco(partno):
    try:
        mcpq="0"
        ds3=list(Nstr.objects.filter(cp_part=partno,epc=str(session_ep),l_to='9999').values('pp_part','cp_part','l_fr','l_to','ptc','epc','qty','updt_dt','ref_ind','ref_no','alt_ind','alt_link','lead_time','reg_no','slno','del_fl','epc_old').order_by('cp_part','epc','pp_part'))
        if(len(ds3)>0):
            for i in range(len(ds3)):
                mcpq=str(float(mcpq)+float(cpq(partno,str(session_ep),str(session_meppart))))        
        return mcpq        

    except:
        return "0"   


def expl(parent, wt, ep):
    mcp_part=''
    mqty=''
    shop_ut1=''
    v_ptc=''
    wt1=0
    mqty1=0
    cp_part=[]
    ptc=[]
    qty=[]
    shop_ut=[]
    l_fr1=[]
    l_to1=[]
    alt_ind=[]
    

    for i in Nstr.objects.raw('select n."id_pk", n."CP_PART",n."ALT_IND",p."PTC",n."QTY",p."SHOP_UT",n."L_FR",n."L_TO" from "NSTR" as n,"PART" as p where p."PARTNO" = n."CP_PART" and  n."PP_PART"=%s and  n."EPC"=%s order by n."PP_PART",n."CP_PART",n."EPC",n."L_TO";',[parent,ep]):
        cp_part.append(i.cp_part)
        qty.append(i.qty)     
        l_fr1.append(i.l_fr)
        l_to1.append(i.l_to)
        alt_ind.append(i.alt_ind)
    
    for i in Part.objects.raw('select p.id, n."CP_PART",p."PTC",n."QTY",p."SHOP_UT",n."L_FR",n."L_TO" from "NSTR" as n,"PART" as p where p."PARTNO" = n."CP_PART" and  n."PP_PART"=%s and  n."EPC"=%s order by n."PP_PART",n."CP_PART",n."EPC",n."L_TO";',[parent,ep]):
        ptc.append(i.ptc)
        shop_ut.append(i.shop_ut)  

    
    df=pandas.DataFrame({'cp_part':cp_part,'ptc':ptc,'qty':qty,'shop_ut':shop_ut,'l_fr':l_fr1,'l_to':l_to1})
    if(df.shape[0]>0):
        for i in range(df.shape[0]) :
            l_fr=''
            l_to=''
            v_alt_ind=''
            mqt=''
            lt=0
            lto=0
            lfr=0
            valtind=0
            l_fr=str(l_fr1[i])
            l_to=str(l_to1[i])
            v_alt_ind = str(0)
            lt=int(str(session_lt))
            lfr=int(l_fr)
            lto=int(l_to)
            valtind=int(v_alt_ind)
            if((((lfr<=lt) and (lt<=lto)) or valtind>1)==False):
                continue 
            mcp_part=str(cp_part[i])
            shop_ut1=str(shop_ut[i])
            v_ptc=str(ptc[i])   
            mqty=str(qty[i])
            wt1 = 0
            mqty1 =0    
            wt1 =float(wt)
            mqty1 =float(mqty)
            mqt=str(wt1*mqty1)
            insertQtySum_temp1(mcp_part, v_ptc, mqt, shop_ut1, l_fr, l_to)
            ds1=list(Nstr.objects.filter(pp_part=mcp_part,epc=ep).values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by("pp_part","cp_part","epc","l_to"))        
            if v_ptc in ["M","Z","L","B"] and len(ds1)>0:
                expl(mcp_part, mqt, ep)     
    
    return        


def summarizeQtySum_Temp(ep,mep_part):
    v_qty=""
    v_partno="" 
        
    ds2=list(QtysumTemp2.objects.filter(cur_time=session_curTime).values('partno').annotate(Max('ptc'),Sum("qty"),Max("shop_ut"),Max("pt_lf"),Max("pt_lt"),Max("rm_part"),Max("rm_ptc"),Max("rm_qty"),Max("rm_ut"),Max("rm_lf"),Max("rm_lt")))
    if(len(ds2)>0):
        for i in range(len(ds2)): 
            v_partno=str(ds2[i].get('partno'))
            v_qty=qloco(v_partno)
            AddDataToTable(v_partno,str(ds2[i].get('ptc__max')),ds2[i].get('qty__sum'),str(ds2[i].get('shop_ut__max')),str(ds2[i].get('pt_lf__max')),str(ds2[i].get('pt_lt_max')),str(ds2[i].get('rm_part__max')),str(ds2[i].get('rm_ptc__max')),ds2[i].get('rm_qty__max'),str(ds2[i].get('rm_ut__max')),str(ds2[i].get('rm_lf__max')),str(ds2[i].get('rm_lt__max')),'0',v_qty)
               
       
    ds3=list(Wrap_table.objects.values('partno','rem','v_qty').annotate(Max('ptc'),Sum("qty"),Max("shop_ut"),Max("pt_lf"),Max("pt_lt"),Max("rm_part"),Max("rm_ptc"),Sum("rm_qty"),Max("rm_ut"),Max("rm_lf"),Max("rm_lt")))
    
    
    ti=Wrap_table.objects.all().delete()
    for i in range(len(ds3)):
        QtysumTemp.objects.create(partno=str(ds3[i].get('partno')),ptc=str(ds3[i].get('ptc__max')),qty=str(ds3[i].get('qty__sum')),shop_ut=str(ds3[i].get('shop_ut__max')),ptlf=str(ds3[i].get('pt_lf__max')),ptlt=str(ds3[i].get('pt_lt__max')),rm_part=str(ds3[i].get('rm_part__max')),rm_ptc=str(ds3[i].get('rm_ptc__max')),rm_qty=ds3[i].get('rm_qty__sum'),rm_ut=str(ds3[i].get('rm_ut__max')),rmlf=str(ds3[i].get('rm_lf__max')),rmlt=str(ds3[i].get('rm_lt__max')),remark=str(ds3[i].get('rem')),qty_loco=ds3[i].get('v_qty'),dt_run=system_date,cur_time=session_curTime) 
        


def CreateDataTableaImpl(cols):
    data_table=pandas.DataFrame(columns=["0","1"])
    return data_table



def CreateDataTableLdBk():
    global Ldbk
    Ldbk= pandas.DataFrame(columns=['PART_NO','DESC','QTY','PTC'])
    return Ldbk       

def AddDataToTableLdBk(a,b,c,d):
    global Ldbk
    Ldbk=Ldbk.append({'PART_NO':a,'DESC':b,'QTY':c,'PTC':d},ignore_index=True)
    return Ldbk



def delQtySum_Temp():
    try:
        QtysumTemp.objects.filter(dt_run__lt=system_date).delete()
        return
    except:
        return 


def delQtySum_Temp2():
    try:
        QtysumTemp2.objects.filter(dt_run__lt=system_date).delete()
        return
    except:
        return  
    


def appendQtySum_Temp2():
        tmpstr=list(TempQtysum.objects.filter(cur_time=session_curTime).values("partno" ,"ptc" ,"qty" ,"shop_ut","l_fr","l_to","rm_part","rm_ptc","rm_qty","rm_ut","rm_lf","rm_lt","dt_run","cur_time"))
        for i in range(len(tmpstr)):
            QtysumTemp2.objects.create(partno=tmpstr[i].get('partno') ,ptc=tmpstr[i].get('ptc') ,qty=tmpstr[i].get('qty') ,shop_ut=tmpstr[i].get('shop_ut'),pt_lf=tmpstr[i].get('l_fr'),pt_lt=tmpstr[i].get('l_to'),rm_part=tmpstr[i].get('rm_part'),rm_ptc=tmpstr[i].get('rm_ptc'),rm_qty=tmpstr[i].get('rm_qty'),rm_ut=tmpstr[i].get('rm_ut'),rm_lf=tmpstr[i].get('rm_lf'),rm_lt=tmpstr[i].get('rm_lt'),dt_run=tmpstr[i].get('dt_run'),cur_time=tmpstr[i].get('cur_time'))
        return
   





def delQtySum_Temp1():
    try:
        TempQtysum.objects.filter(dt_run__lt= system_date).delete()
        return
    except:
        return 



    
def insertQtySum_temp1(part_n,pt,qt,shop_u,l_f,l_t):  
        try:
            
            TempQtysum.objects.create(partno=part_n,ptc=pt,qty=qt,shop_ut=shop_u,l_fr=l_f,l_to=l_t,rm_part='',rm_ptc='',rm_qty=0.00,rm_ut='',rm_lf='',rm_lt='',dt_run=system_date,cur_time=session_curTime) 
            
            return   
        except:
            return
       



def AddDataToTable1(a,b,mytable):
    mytable=mytable.append({"0":a,"1":b})
    


def AddDataToTable(a,b,c,d,e,f,g,h,i,j,k,l,m,n):
    ls=[a,b,c,d,e,f,g,h,i,j,k,l,m,n]
    for i in range(len(ls)):
        if ls[i]=='None':
            ls[i]='0'
        elif(ls[i]==None):
            ls[i]=0.00    
    Wrap_table.objects.create(partno=ls[0],ptc=ls[1],qty=ls[2],shop_ut=ls[3],pt_lf=ls[4],pt_lt=ls[5],rm_part=ls[6],rm_ptc=ls[7],rm_qty=ls[8],rm_ut=ls[9],rm_lf=ls[10],rm_lt=ls[11],rem=ls[12],v_qty=ls[13])
    
    


def AddDataToTableFn(a,b,c,d,e,f,g,h,i,j,k,l):
    global outfile
    outfile=outfile.append({'PART_NO':a, 'EPC':b, 'DESC':c,'QTY':d,'OPN':e,'LCNO':f,'SHOP':g,'PA':h,'AT':i,'QTY_LOCO':j,'LOT':k,'PTC':l},ignore_index=True)
 


def CreateDataTableFn():
    dfObj = pandas.DataFrame(columns=['PART_NO', 'EPC', 'DESC','QTY','OPN','LCNO','SHOP','PA','AT','QTY_LOCO','LOT','PTC'])
    return dfObj    