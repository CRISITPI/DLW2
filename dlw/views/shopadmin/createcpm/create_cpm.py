from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/createCpm/')
def createCpm(request):
    from django.db import connection
     
    prcs=[{}]
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    
    wo_nop = empmast.objects.none() 
    t = time.localtime()
    curTime = time.strftime("%H%M%S", t)
    tmpStr = Code.objects.filter(cd_type='11',num_1='10010014').values('code','num_1').order_by('1')
    aEpc = tmpStr
    
    

    TotAsslyKnt = aEpc.count()
    cursor=connection.cursor()
    cursor.execute('''select to_char("START_DT",'dd/mm/yyyy') "START_DT","START_TIME",to_char("END_DT",'dd/mm/yyyy')"END_DT","END_TIME","ASSLY_OVER", "CPM_START_TIME","CPM_END_TIME","UPDT_CPM"
                        ,"QPP_START_TIME","QPP_END_TIME","QPP_ASSLY_OVER","UPDT_QPP" from public."CPM_PROCESS" 
                        where "START_DT"=(select max("START_DT") from public."CPM_PROCESS") and 
                        "START_TIME"=(select max("START_TIME") from public."CPM_PROCESS" where 
                        "START_DT"=(select max("START_DT") from public."CPM_PROCESS" ) ) order by "START_DT";''')
    prcs=cursor.fetchall()
    print('prcs',prcs)

    for i in range(len(prcs)):
        prcs1=[{'START_DT':prcs[i][0],'START_TIME':prcs[i][1],'END_DT':prcs[i][2],'END_TIME':prcs[i][3],'ASSLY_OVER':prcs[i][4],'CPM_START_TIME':prcs[i][5],'CPM_END_TIME':prcs[i][6],'UPDT_CPM':prcs[i][7],'QPP_START_TIME':prcs[i][8],'QPP_END_TIME':prcs[i][9],'QPP_ASSLY_OVER':prcs[i][10],'UPDT_QPP':prcs[i][11]}]
    print(prcs1)
    if (len(prcs) > 0):
        if prcs[0][6] is None:
           vCPM_END_TIME = ''
           createcpm['vCPM_END_TIME'] =''
        else:
            vCPM_END_TIME = prcs[0][6]
            createcpm['vCPM_END_TIME'] = prcs[0][6]

        if prcs[0][7] is None:
           vUpdt_cpm = ''
           createcpm['vUpdt_cpm'] =''
        else:
            vUpdt_cpm = prcs[0][7]
            createcpm['vUpdt_cpm'] = prcs[0][7]

        if prcs[0][11] is None:
            vUpdt_qpp = ''
            createcpm['vUpdt_qpp'] =''
        else:
            vUpdt_qpp = prcs[0][11]
            createcpm['vUpdt_qpp'] = prcs[0][11]

        if prcs[0][2] is None:
           vEnd_dt = ''
           createcpm['vEnd_dt'] =''
        else:
            vEnd_dt = prcs[0][2]
            createcpm['vEnd_dt'] = prcs[0][2]

        if prcs[0][3] is None:
           vEnd_time = ''
           createcpm['vEnd_time'] =''
        else:
            vEnd_time = prcs[0][3]
            createcpm['vEnd_time'] = prcs[0][3]

        if prcs[0][9] is None:
           vQPP_END_TIME = ''
           createcpm['vQPP_END_TIME'] =''
        else:
            vQPP_END_TIME = prcs[0][9]
            createcpm['vQPP_END_TIME'] = prcs[0][9]

        if prcs[0][5] is None:
           vCPM_START_TIME = ''
           createcpm['vCPM_START_TIME'] =''
        else:
            vCPM_START_TIME = prcs[0][5]
            createcpm['vCPM_START_TIME'] = prcs[0][5]

        if prcs[0][8] is None:
           vQPP_START_TIME = ''
           createcpm['vQPP_START_TIME'] =''
        else:
            vQPP_START_TIME = prcs[0][8]
            createcpm['vQPP_START_TIME'] = prcs[0][8]


        vAssly_over = prcs[0][4]   
        createcpm['vAssly_over'] = prcs[0][4]   
        createcpm['curTime']=curTime
        print(createcpm)
        if ((vEnd_dt!= "" and vEnd_time!="")  and (vUpdt_cpm == "N" and vCPM_END_TIME=="") and (vUpdt_qpp == "N")):
            msg="btnUpdCPM"
         
        elif ((vEnd_dt != "" and vEnd_time != "") and (vUpdt_cpm == "Y") and (vUpdt_qpp == "N" and vQPP_END_TIME=="")):
            msg="btnUpdQPP"
        
        elif ((vEnd_dt != "" and vEnd_time != "") and (vUpdt_cpm == "Y") and (vUpdt_qpp == "Y")):
            msg="btnProcess"
          
        elif (vEnd_dt== "" and vEnd_time==""):
            msg = "CPM UPDATION IS IN PROGRESS, " + str(vAssly_over) + " ASSEMBLIES ARE PROCEESSED. SO WAIT TILL ALL ASSEMBLIES GETS OVER.."

    print(msg)
    tm=shop_section.objects.all()
    tmp=[]
    for on in tm:
            tmp.append(on.section_code)
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'subnav':g.subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'vAssly_over':vAssly_over,
            'vUpdt_cpm':vUpdt_cpm,
            'vUpdt_qpp':vUpdt_qpp,
            'vEnd_dt':vEnd_dt,
            'vEnd_time':vEnd_time,
            'vCPM_START_TIME':vCPM_START_TIME,
            'vCPM_END_TIME':vCPM_END_TIME,
            'vQPP_START_TIME':vQPP_START_TIME,
            'vQPP_END_TIME':vQPP_END_TIME,
            'msg':msg,
            'prcs':prcs,
            'prcs1':prcs1,
            'usermaster':usermaster,
        }
    if(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M13.objects.all().filter(shop=rolelist[i]).values('wo').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':g.subnav,
            'vAssly_over':vAssly_over,
            'vUpdt_cpm':vUpdt_cpm,
            'vUpdt_qpp':vUpdt_qpp,
            'vEnd_dt':vEnd_dt,
            'vEnd_time':vEnd_time,
            'vCPM_START_TIME':vCPM_START_TIME,
            'vCPM_END_TIME':vCPM_END_TIME,
            'vQPP_START_TIME':vQPP_START_TIME,
            'vQPP_END_TIME':vQPP_END_TIME,
            'msg':msg,
            'prcs':prcs,
            'prcs1':prcs1,

        }
        
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':g.nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':g.subnav,
            'vAssly_over':vAssly_over,
            'vUpdt_cpm':vUpdt_cpm,
            'vUpdt_qpp':vUpdt_qpp,
            'vEnd_dt':vEnd_dt,
            'vEnd_time':vEnd_time,
            'vCPM_START_TIME':vCPM_START_TIME,
            'vCPM_END_TIME':vCPM_END_TIME,
            'vQPP_START_TIME':vQPP_START_TIME,
            'vQPP_END_TIME':vQPP_END_TIME,
            'msg':msg,
            'prcs':prcs,
            'prcs1':prcs1
        }

    return render(request,'SHOPADMIN/CREATECPM/createCpm.html',context)
createcpm={'tmpStr':"", 'mAssly':"", 'ep': "", 'vStart_dt':"",'vStart_time':"",
            'vAssly_over':"", 'vUpdt_cpm':"", 'vUpdt_qpp':"", 'vEnd_dt':"", 'vEnd_time':"", 
            'vCPM_START_TIME':"", 'vCPM_END_TIME':"", 'vQPP_START_TIME':"", 'vQPP_END_TIME':"",'curTime':"",'DT_RUN':'','CURRTIME':''}

def expolde():     
        ds=[]
        cursor=connection.cursor()
        cursor.execute('''select exists(select * from public."CPM1")''')
        exists = cursor.fetchone()[0]
        
        if (exists):
            delCPM1()
        else:
            createCPM1()
        cursor=connection.cursor()
        cursor.execute('''select distinct substr("CODE",1,2), "NUM_1" from public."CODE" where "CD_TYPE"='11' order by 1;''')
        aEpc=list(cursor.fetchall())
        t = time.localtime()
        current_time = time.strftime("%H%M%S", t)
        if (len(aEpc) > 0):
            for i in range(len(aEpc)):
                ep=createcpm['ep'] = aEpc[i][0]
                mAssly=createcpm['mAssly'] = aEpc[i][1]
                print(ep,mAssly)
                ret=sumexpl(mAssly,ep)
                msg=ret[0]['msg']
                status=ret[0]['status']
                if ( status==0):
                    continue
                tmpStr = CpmProcess.objects.filter(start_dt=createcpm['DT_RUN'],start_time=createcpm['CURRTIME']).update(assly_over=i+1)
                break
            t = time.localtime()
            current_time = time.strftime("%H%M%S", t)
            edate=datetime.datetime.today().strftime('%Y-%m-%d')
            tmpStr = CpmProcess.objects.filter(start_dt=createcpm['DT_RUN'],start_time=createcpm['CURRTIME']).update(end_dt=edate,end_time=current_time)
        status=1
        msg = "Explode successfully. Now Update CPM."
        btnUpdCPM=1
        msg = "Unable to Explode successfully. Process not over!!"
        status=0
        lst=[{'status':status,'msg':msg,'btn':btnUpdCPM}]
        return lst

Session={'mAltind':'','mAltlink':'','assly':''}
def sumexpl(assly,EP):   
        #try:
        ep=""
        ep_ptc = ""
        mAltind=""
        mAltlink = 0
        
        Session["mAltind"] = mAltind
        Session["mAltlink"] = mAltlink
        Session["assly"] = assly
        ep = EP
        r=1
        msg=''
        tmpStr = Part.objects.filter(partno=assly).values('ptc').order_by('ptc')
        if len(tmpStr)>0:
            ep_ptc = tmpStr[0]['ptc']
        if ep_ptc=='':
            msg = assly + "(" + ep + "):Assembly not in PART MASTER!"
            r=0
        if r!=0:
            cursor=connection.cursor()
            cursor.execute('''select p."PARTNO" from public."NSTR" n,PUBLIC."PART" p where trim("L_TO")='9999' and coalesce(trim(n."DEL_FL"),'*')='*' and trim("PP_PART")=%s::text and trim("EPC")=%s::text and trim(n."CP_PART")=trim(p."PARTNO") order by "PP_PART","EPC","CP_PART";''',[assly,ep])
            tmpStr=cursor.fetchall()
            if len(tmpStr)==0:
                msg = str(assly)+ "(" + str(ep) + "):Assembly not in STRUCTURE!"
                r=0
            if r!=0:
                cp1 = []
                cp1=expl(assly, "1", ep,cp1)
                print('expl',cp1)
                cnt = len(cp1)
                cp2 = []
                cp3=[]
                cp2=AddDataToTable1(assly, ep_ptc, "1.000", "01", ep, None, None, createcpm['DT_RUN'], cp2)
                for k in range(len(cp1)):
                    cp2.append(cp1[k])
                cnt = len(cp2)
                cp3=appendConsPart2(cp2)
                cnt = len(cp3)
                summarizeConsPart(cp3,cp2)
                r= 1
                msg='Successfully Exploded , Now Update CPM !!!'    
        lst=[{'status':r,'msg':msg}]
        return lst


def expl(parent, wt,ep, cp1):
        ds=[]
        ds1=[]
        mcp_part=''
        mqty =''
        shop_ut=''
        ptc=''
        mAltind=None
        mAltlink=''
        assly=''
        wt1=0.0
        mqty1=0.0
        mAltind = Session["mAltind"]
        mAltlink = Session["mAltlink"]
        assly = Session["assly"]
        r=1
        msg=''
        cursor=connection.cursor()
        cursor.execute('''select distinct "CP_PART",nstr."PTC" ptc,coalesce("QTY",0) qty,"SHOP_UT",nstr."ALT_LINK" alt_link,
            COALESCE("ALT_IND",'0') alt_ind from public."NSTR" nstr,public."PART" part where trim(nstr."CP_PART")=trim(part."PARTNO") and  
            trim("PP_PART")= %s ::text and trim("EPC")= %s  and trim("L_TO")='9999'  order by "CP_PART"''',[parent,ep])
        tmpStr=list(cursor.fetchall())
        ds=tmpStr
        if len(ds) > 0:
            for i in range(len(ds)):
                alt_ind=''
                alt_link=''
                mqt=''
                alt_ind = ds[i][5]
                alt_link = ds[i][4]
                if (parent == assly):
                    if ((alt_link != mAltlink) or (alt_ind != mAltind)):
                        mAltlink = alt_link
                        mAltind = alt_ind
                        Session["mAltind"] = mAltind
                        Session["mAltlink"] = mAltlink
                mcp_part = ds[i][0]
                PTC = ds[i][1]
                shop_ut = ds[i][3]
                mqty = ds[i][2]
                wt1 = float(wt)
                mqty1 = float(mqty)
                mqt = str(wt1 * mqty1)
                cp1=AddDataToTable1(mcp_part, PTC, mqt, shop_ut, ep, mAltlink, mAltind,createcpm['DT_RUN'], cp1)
                lst=["M", "Z", "L", "B"]
                cursor.execute('''select "PARTNO" from public."NSTR" nstr,public."PART" part where trim(nstr."CP_PART")=trim(part."PARTNO") and  
                trim("PP_PART")= %s  and trim("EPC")= %s  and trim("L_TO")='9999' limit 1''',[mcp_part,ep])
                obj=list(cursor.fetchall())
                if (PTC in lst and len(obj)>0):
                    cp1=expl(mcp_part, mqt, ep,cp1)
        return cp1
from functools import reduce
def appendConsPart2(cp2):
    fnames1 = []
    fnames2=[]
    part=[{'partno':'','alt_link':'','alt_ind':''}]
    altlink=[]
    altind=[]
    r =1 
    for i in range(len(cp2)):
        if [{'partno':cp2[i]['partno'],'alt_link':cp2[i]["alt_link"],'alt_ind':cp2[i]["alt_ind"]}] not in part:
            part.append({'partno':cp2[i]['partno'],'alt_link':cp2[i]["alt_link"],'alt_ind':cp2[i]["alt_ind"]})
            ls=list(filter(lambda x:str(x['partno']) in str(cp2[i]['partno']) and str(x['alt_link']) in str(cp2[i]['alt_link']) and str(x['alt_ind']) in str(cp2[i]['alt_ind']),cp2))
            if len(ls) > 1:
                ls1=list(map(itemgetter('qty'),ls))
                ls2=list(map(itemgetter('ptc'),ls))
                ls3=list(map(itemgetter('shop_ut'),ls))
                ls4=list(map(itemgetter('ep'),ls))
                ls5=list(map(itemgetter('dt_run'),ls))
                qty_alt="{0:.3f}".format(reduce(lambda x,y:float(x) + float(y),ls1))
                ptc=max(ls2)
                shop_ut=max(ls3)
                dt_run=max(ls5)
                epc=max(ls4)
                fnames2.append({'partno':cp2[i]['partno'],'alt_link':cp2[i]['alt_link'],'alt_ind':cp2[i]['alt_ind'],'qty_alt':qty_alt,'ptc':ptc,'shop_ut':shop_ut,'dt_run':dt_run,'epc':epc})
            else:
                fnames2.append({'partno':cp2[i]['partno'],'alt_link':cp2[i]['alt_link'],'alt_ind':cp2[i]['alt_ind'],'qty_alt':cp2[i]['qty'],'ptc':cp2[i]['ptc'],'shop_ut':cp2[i]['shop_ut'],'dt_run':cp2[i]['dt_run'],'epc':cp2[i]['ep']})
    part=[{'partno':'','altlink':''}]
    altlink=[]
    altind=[]
    for i in range(len(fnames2)):
        if [{'partno':fnames2[i]['partno'],'altlink':fnames2[i]["alt_link"]}] not in part:
            part.append({'partno':fnames2[i]['partno'],'altlink':fnames2[i]["alt_link"]})
            ls=list(filter(lambda x:str(x['partno']) in str(fnames2[i]['partno']) and str(x['alt_link']) in str(fnames2[i]['alt_link']) ,fnames2))
            if len(ls) > 1:
                ls1=list(map(itemgetter('qty_alt'),ls))
                ls2=list(map(itemgetter('ptc'),ls))
                ls3=list(map(itemgetter('shop_ut'),ls))
                ls4=list(map(itemgetter('epc'),ls))
                ls6=list(map(itemgetter('alt_ind'),ls))
                ls5=list(map(itemgetter('dt_run'),ls))
                qty_alt="{0:.3f}".format(reduce(lambda x,y:float(x) + float(y),ls1))
                ptc=max(ls2)
                shop_ut=max(ls3)
                dt_run=max(ls5)
                epc=max(ls4)
                alt_ind=max(ls6)
                fnames1.append({'part_no':fnames2[i]['partno'],'alt_link':fnames2[i]['alt_link'],'alt_ind':alt_ind,'qty_alt':qty_alt,'ptc':ptc,'shop_ut':shop_ut,'dt_run':dt_run,'epc':epc})
            else:
                fnames1.append({'part_no':fnames2[i]['partno'],'alt_link':fnames2[i]['alt_link'],'alt_ind':fnames2[i]['alt_ind'],'qty_alt':fnames2[i]['qty_alt'],'ptc':fnames2[i]['ptc'],'shop_ut':fnames2[i]['shop_ut'],'dt_run':fnames2[i]['dt_run'],'epc':fnames2[i]['epc']})
    r= 1
    return fnames1
   
def createCPM1():
    cursor=connection.cursor()
    try:
            cursor.execute('''CREATE TABLE "CPM1"( "PART_NO" character(8), "EPC" character(2),"QTY" numeric(4), "SHOP_UT"   varchar(2),"PTC"   varchar(1),
                    "ALT_LINK" numeric(4) , "ALT_IND" varchar(1),     "QTY_ALT" numeric(9,3),  "UPDT_DT" date, "CUR_TIME" varchar(40))''')
            r = 1
            msg=''
    except:
            msg = "Table not created : CPM1"
            r = 0
    lst=[{'status':r,'msg':msg}]
    return msg

def delCPM1():
        try:
            cursor=connection.cursor()
            cursor.execute('''truncate table public."CPM1";''')
            msg=''
            r=1

        except:
            msg= "Data not deleted : CPM1"
            r=0
        lst=[{'status':r,'msg':msg}]
        return lst

from operator import itemgetter
def summarizeConsPart(fnames1,fname2):         
    fnames = []
    part=[{'partno':'','alt_ind':''}]

    cursor=connection.cursor()
    for i in range(len(fnames1)):
       if [{'partno':fnames1[i]['part_no'],'alt_link':fnames1[i]["alt_link"]}] not in part:
            part.append({'partno':fnames1[i]['part_no'],'alt_link':fnames1[i]["alt_link"]})
            if fnames1[i]['part_no']!='':    
                ls=list(filter(lambda x:str(x['part_no']) in str(fnames1[i]['part_no']),fnames1))
                if len(ls) > 1:
                    ls2=list(map(itemgetter('ptc'),ls))
                    ls7=list(map(itemgetter('qty_alt'),ls))
                    ls3=list(map(itemgetter('shop_ut'),ls))
                    ls4=list(map(itemgetter('epc'),ls))
                    ls5=list(map(itemgetter('dt_run'),ls))
                    qty_alt=0
                    qty=max(ls7)
                    ptc=max(ls2)
                    shop_ut=max(ls3)
                    dt_run=max(ls5)
                    epc=max(ls4)
                    alt_ind=None
                    alt_link=0
                    fnames.append({'part_no':fnames1[i]['part_no'],'qty':qty,'alt_link':alt_link,'alt_ind':alt_ind,'qty_alt':qty_alt,'ptc':ptc,'shop_ut':shop_ut,'dt_run':dt_run,'epc':epc})
                else:
                    fnames.append({'part_no':fnames1[i]['part_no'],'qty':fnames1[i]['qty_alt'],'alt_link':0,'alt_ind':None,'qty_alt':0,'ptc':fnames1[i]['ptc'],'shop_ut':fnames1[i]['shop_ut'],'dt_run':fnames1[i]['dt_run'],'epc':fnames1[i]['epc']})
    part=[{'partno':'','alt_link':'','alt_ind':''}]
    altlink=[]
    altind=[]
    for i in range(len(fname2)):
         if [{'partno':fname2[i]['partno'],'alt_link':fname2[i]["alt_link"],'alt_ind':fname2[i]["alt_ind"]}] not in part:
            part.append({'partno':fname2[i]['partno'],'alt_link':fname2[i]["alt_link"],'alt_ind':fname2[i]["alt_ind"]})
            if fname2[i]['partno']!='':
                ls=list(filter(lambda x:str(x['partno']) in str(fname2[i]['partno']) and str(x['alt_link']) in str(fname2[i]['alt_link']) and str(x['alt_ind']) in str(fname2[i]['alt_ind']),fname2))
                if len(ls) > 1:
                    ls1=list(map(itemgetter('qty'),ls))
                    ls2=list(map(itemgetter('ptc'),ls))
                    ls3=list(map(itemgetter('shop_ut'),ls))
                    ls4=list(map(itemgetter('ep'),ls))
                    ls5=list(map(itemgetter('dt_run'),ls))
                    qty_alt="{0:.3f}".format(reduce(lambda x,y:float(x) + float(y),ls1))
                    qty=0
                    ptc=max(ls2)
                    shop_ut=max(ls3)
                    dt_run=max(ls5)
                    epc=max(ls4)
                    fnames.append({'part_no':fname2[i]['partno'],'qty':qty,'alt_link':fname2[i]['alt_link'],'alt_ind':fname2[i]['alt_ind'],'qty_alt':qty_alt,'ptc':ptc,'shop_ut':shop_ut,'dt_run':dt_run,'epc':epc})
                else:
                    fnames.append({'part_no':fname2[i]['partno'],'qty':0,'alt_link':fname2[i]['alt_link'],'alt_ind':fname2[i]['alt_ind'],'qty_alt':fname2[i]['qty'],'ptc':fname2[i]['ptc'],'shop_ut':fname2[i]['shop_ut'],'dt_run':fname2[i]['dt_run'],'epc':fname2[i]['ep']})
    fname = fnames
    if len(fname)> 0:
        for i in range(len(fname)):
            cursor.execute('''INSERT INTO public."CPM1"("PART_NO", "EPC", "QTY", "SHOP_UT", "PTC", "ALT_LINK", "ALT_IND", "QTY_ALT", "UPDT_DT", "CUR_TIME")
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',[fname[i]["part_no"],fname[i]["epc"],fname[i]["qty"],fname[i]["shop_ut"], 
                            fname[i]["ptc"], fname[i]["alt_link"],fname[i]["alt_ind"],fname[i]["qty_alt"],
                            datetime.datetime.strptime(fname[i]["dt_run"],"%Y-%m-%d").date(), createcpm['CURRTIME']])
                
   
       



def AddDataToTable1(a,b,c,d,e,f,g,h,myTable):
        num = len(myTable) + 1
        myTable.append({"partno":a, "ptc":b, "qty":c, "shop_ut":d, "ep":e, "alt_link":f, "alt_ind":g,"dt_run":h})
        return myTable
     
def AddDataToTable( a,  b,  c,  d,  e,  f,  g,  h, i, myTable):
        num = len(myTable)+ 1
        myTable.append({"partno":a, "ptc":b, "qty":c, "shop_ut":d, "ep":e, "alt_link":f, "alt_ind":g,"dt_run":h})
        return myTable

def MyLongRunningTask1():
    ret=expolde()
    status=ret[0]['status']
    msg=ret[0]['msg']
    btn=ret[0]['btn']
    
import time
def MyLongRunningTask2():
    t = time.localtime()
    current_time = time.strftime("%H%M%S", t)
    cursor=connection.cursor()
    r=1
    msg=''
    btn=''
    cursor.execute('''select "START_DT","CPM_START_TIME" cpm_start_time,"CPM_END_TIME" cpm_end_time from public."CPM_PROCESS" where ("START_DT", "START_TIME") in (select "START_DT",max("START_TIME") from public."CPM_PROCESS" where "START_DT"=(select max("START_DT") from public."CPM_PROCESS") group by "START_DT");''')
    ds=list(cursor.fetchall())
    if len(ds) > 0:
        CURRTIME = ds[0][1]
        createcpm['vEnd_time'] = ds[0][2]
        t = time.localtime()
        current_time = time.strftime("%H%M%S", t)
        if (CURRTIME is not None and createcpm['vEnd_time'] is None):
            msg="CPM UPDATION IS IN PROGRESS, SO WAIT TILL IT GETS OVER.."
            r = 0
   
        elif (CURRTIME is None and createcpm['vEnd_time'] is None):
            cursor.execute('''update public."CPM_PROCESS" set "CPM_START_TIME"=%s where ("START_DT", "START_TIME") in 
                (select "START_DT",max("START_TIME") from public."CPM_PROCESS" where "START_DT"= 
                (select max("START_DT") from public."CPM_PROCESS") group by "START_DT")''',[current_time])
    if r != 0:
        
        cursor.execute('''delete from public."CPM1" where coalesce("QTY"::text,'0')='0' and coalesce("ALT_LINK"::text,'0')='0';''')
        cursor.execute('''delete from public."CPM" where "EPC"='21'and (trim("PART_NO"),trim("EPC"),coalesce("ALT_LINK"::text,'0'),coalesce(trim("ALT_IND"),'#')) in (
                        select trim("PART_NO"),trim( "EPC"),coalesce("ALT_LINK"::text,'0'),coalesce(trim("ALT_IND"),'#') from public."CPM" 
                        except select trim("PART_NO"),trim( "EPC"),coalesce("ALT_LINK"::text,'0'),coalesce(trim("ALT_IND"),'#') from public."CPM1");''')
        cursor.execute('''select "PART_NO", "EPC", "QTY", "SHOP_UT", "PTC", "ALT_LINK", "ALT_IND","QTY_ALT", "UPDT_DT", "CUR_TIME" from public."CPM1";''')
        ds=(cursor.fetchall())
        for i in range(len(ds)):
            cursor.execute('''update public."CPM" set "PTC"=%s,"QTY_OLD" = (SELECT "QTY" FROM public."CPM" where trim("PART_NO") = trim(%s) and trim("EPC")= trim(%s) and COALESCE("ALT_LINK"::TEXT,'0')=COALESCE(%s::text,'0') and COALESCE("ALT_IND",'#')=COALESCE(%s,'#') limit 1), "SHOP_UT" =%s, "QTY"=%s, "UPDT_DT"= %s  
                where trim("PART_NO") = trim(%s) and trim("EPC")= trim(%s) and COALESCE("ALT_LINK"::TEXT,'0')=COALESCE(%s::text,'0') and COALESCE("ALT_IND",'#')=COALESCE(%s,'#');
		        ''',[ds[i][4],ds[i][0],ds[i][1],ds[i][5],ds[i][6],ds[i][3],ds[i][2],ds[i][8],ds[i][0],ds[i][1],ds[i][5],ds[i][6]])
        
        cursor.execute('''insert into public."CPM" ( select b."PART_NO",b."EPC",b."QTY",b."SHOP_UT",b."PTC",b."QTY",coalesce(b."ALT_LINK",0),b."ALT_IND",b."QTY_ALT", b."UPDT_DT",null from 
        (select trim("PART_NO") part_no,trim("EPC") epc,coalesce("ALT_LINK",0) alt_link,coalesce(trim("ALT_IND"),'#') alt_ind from public."CPM1"
        except select trim("PART_NO") part_no,trim("EPC") epc,coalesce("ALT_LINK",0) alt_link,coalesce(trim("ALT_IND"),'#') alt_ind from public."CPM") a, public."CPM1" b 
        where trim(a.part_no)=trim(b."PART_NO") and trim(a.epc)=trim(b."EPC") and 
        coalesce(a.alt_link,0)=coalesce(b."ALT_LINK",0) and coalesce(trim(a.alt_ind),'#')=coalesce(trim(b."ALT_IND"),'#'));''')
        t = time.localtime()
        current_time = time.strftime("%H%M%S", t)
        cursor.execute('''update public."CPM_PROCESS" set "CPM_END_TIME"=%s, "UPDT_CPM"='Y' where ("START_DT", "START_TIME") in
        (select "START_DT",max("START_TIME") from public."CPM_PROCESS" where "START_DT"= 
        (select max("START_DT") from public."CPM_PROCESS") group by "START_DT")''',[current_time])
            
        
        msg= "CPM Updated successfully. Now update QPP"
        r=2
    if r!=0 and r!=2:
        r=0
        msg="Unable to Update CPM successfully. Process not over yet!!"
    lst=[{'status':r,'msg':msg,'CURRTIME':createcpm['CURRTIME']}]
   

import threading
def btnUpdCPM_Click(request):
    if request.method=='GET' and request.is_ajax():
        t=threading.Thread(target=MyLongRunningTask2)
        t.start()
        t.join()
        r=1
        msg=''
        
        lst=[{'status':r,'msg':msg}]
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success:False"},status=400)

def btnUpdQPP_Click(request):
    if request.method=='GET' and request.is_ajax():
        cursor=connection.cursor()
        
        r=1
        msg=''
        cursor.execute('''select "START_DT","QPP_START_TIME" qpp_start_time, "QPP_END_TIME" qpp_end_time from public."CPM_PROCESS" where ("START_DT", "START_TIME") in 
        (select "START_DT",max("START_TIME") from public."CPM_PROCESS" where "START_DT"= 
        (select max("START_DT") from public."CPM_PROCESS") group by "START_DT")''')
        ds=list(cursor.fetchall())
            
        if len(ds) > 0:
            vQPP_START_TIME = createcpm['vQPP_START_TIME'] = ds[0][1]
            vQPP_END_TIME = createcpm['vQPP_END_TIME'] = ds[0][2]

            if (vQPP_START_TIME is not None and vQPP_END_TIME is None):
                msg= "QPP UPDATION IS IN PROGRESS, SO WAIT TILL IT GETS OVER.."
                r= 0
            elif (vQPP_START_TIME is None and vQPP_END_TIME is None):
                t = time.localtime()
                current_time = time.strftime("%H%M%S", t)
                cursor.execute('''update public."CPM_PROCESS" set "QPP_START_TIME"=%s where ("START_DT", "START_TIME") in 
                (select "START_DT",max("START_TIME") from public."CPM_PROCESS" where "START_DT"= 
                (select max("START_DT") from public."CPM_PROCESS") group by "START_DT");''',[current_time])
                r = 1 
                msg='QPP Updated Successfully!!!'  

                t = time.localtime()
                current_time = time.strftime("%H%M%S", t)
                cursor.execute('''update public."CPM_PROCESS" set "QPP_END_TIME"=%s ,"UPDT_QPP"='Y' where ("START_DT", "START_TIME") in 
                (select "START_DT",max("START_TIME") from public."CPM_PROCESS" where "START_DT"= 
                (select max("START_DT") from public."CPM_PROCESS") group by "START_DT");''',[current_time])
        else: 
            r = 0           
            msg="Unable to Update QPP successfully. Process Not over yet!!"
        lst=[{'status':r,'msg':msg}]
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success:False"},status=400)

def Reset_Click(request):
    if request.method=='GET' and request.is_ajax():
        cursor=connection.cursor()
        cursor.execute('''select "START_DT" ::text, "START_TIME", "ASSLY_OVER","UPDT_CPM", "CPM_START_TIME", "CPM_END_TIME", "UPDT_QPP", 
            "QPP_START_TIME","QPP_END_TIME","END_DT" ::text, "END_TIME" from public."CPM_PROCESS" where "START_DT"=(select
            max("START_DT") from public."CPM_PROCESS") and "START_TIME"=(select max("START_TIME") from public."CPM_PROCESS"
            where "START_DT"=(select max("START_DT") from public."CPM_PROCESS"))''')
        ds=list(cursor.fetchall())
        if len(ds) > 0:
            t = time.localtime()
            current_time = time.strftime("%H%M%S", t)
            CURRENT_DATE=datetime.datetime.today().strftime('%Y-%m-%d')
            dtTime = str(ds[0][0]).split(' ')
            createcpm['vStart_dt'] = dtTime[0]
            createcpm['vStart_time'] = ds[0][1]
            da=datetime.datetime.strptime(createcpm['vStart_dt'],'%Y-%m-%d')
            cursor.execute('''update  public."CPM_PROCESS" set "END_DT"=%s, "END_TIME"=
            %s,"UPDT_CPM"='Y',"UPDT_QPP"='Y',"CPM_START_TIME"= %s, "CPM_END_TIME"=%s,"QPP_START_TIME"= %s,"QPP_END_TIME"=%s,
            "QPP_ASSLY_OVER"=0  where  "START_TIME"=%s;''',[CURRENT_DATE,current_time,current_time,current_time,current_time,current_time,createcpm['vStart_time']])
            msg= "Reset Successful. Now Open Again"
        return JsonResponse(msg,safe=False)
    return JsonResponse({"success:False"},status=400)       
       
def btnRefresh_Click(request):
    if request.method=='GET' and request.is_ajax():
        cursor=connection.cursor()
        cursor.execute('''select to_char("START_DT",'dd/mm/yyyy'),"START_TIME",to_char("END_DT",'dd/mm/yyyy'),
        "END_TIME","ASSLY_OVER", "CPM_START_TIME","CPM_END_TIME","UPDT_CPM","QPP_START_TIME","QPP_END_TIME",
        "QPP_ASSLY_OVER","UPDT_QPP" from public."CPM_PROCESS" where "START_DT"=(select max("START_DT") 
        from public."CPM_PROCESS") and "START_TIME"=(select max("START_TIME") from public."CPM_PROCESS" 
        where "START_DT"=(select max("START_DT") from public."CPM_PROCESS" ) ) order by "START_DT";''')
        prcs=list(cursor.fetchall())
        return JsonResponse(prcs,safe=False)
    return JsonResponse({"success:False"},status=400) 
        
def btnAllJobs_Click(request):
    if request.method=="GET" and request.is_ajax():
        cursor=connection.cursor()
        cursor.execute('''select to_char("START_DT",'dd/mm/yyyy'),"START_TIME",to_char("END_DT",'dd/mm/yyyy'),
        "END_TIME","ASSLY_OVER", "CPM_START_TIME","CPM_END_TIME","UPDT_CPM","QPP_START_TIME","QPP_END_TIME",
        "QPP_ASSLY_OVER","UPDT_QPP" from public."CPM_PROCESS" order by "START_DT";''')
        prcs=list(cursor.fetchall())
        return JsonResponse(prcs,safe=False)
    return JsonResponse({"success:False"},status=400)

def btnProcess_Click(request):
    if request.method=="GET" and request.is_ajax():
        
        t = threading.Thread(target=MyLongRunningTask1)
        cursor=connection.cursor()
        msg=''
        r=1
        cursor.execute('''select "ASSLY_OVER","UPDT_CPM","UPDT_QPP","END_DT"::text, "END_TIME" from public."CPM_PROCESS" where "START_DT"=(select max("START_DT") 
            from public."CPM_PROCESS") and "START_TIME"=(select max("START_TIME") from public."CPM_PROCESS" where "START_DT"=
            (select max("START_DT") from public."CPM_PROCESS"))''')
        ds=cursor.fetchall()
        if len(ds) > 0:
            createcpm['vAssly_over'] = ds[0][0]
            createcpm['vUpdt_cpm'] = ds[0][1]
            createcpm['vUpdt_qpp'] = ds[0][2]
            createcpm['vEnd_dt'] = ds[0][3]
            createcpm['vEnd_time'] = ds[0][4]

            if createcpm['vEnd_dt'] == "" and createcpm['vEnd_time'] == "":
                msg= "CPM UPDATION IS IN PROGRESS, " + createcpm['vAssly_over'] + " ASSEMBLIES ARE PROCEESSED. SO WAIT TILL ALL ASSEMBLIES GETS OVER.."
                r=0
            elif ((createcpm['vEnd_dt'] != "" and createcpm['vEnd_time'] != "") and (createcpm['vUpdt_cpm'] == "Y") and (createcpm['vUpdt_qpp']  == "Y")):
                dtTime = createcpm['curTime']    
                createcpm['DT_RUN']= datetime.datetime.today().strftime('%Y-%m-%d')
                t1 = time.localtime()
                current_time = time.strftime("%H%M%S", t1)
                createcpm['CURRTIME']= current_time
                cursor.execute('''insert into public."CPM_PROCESS" ("START_DT", "START_TIME") values (%s,%s);''',[ createcpm['DT_RUN'],createcpm['CURRTIME']])
                print('start')
                t.start()
                print('end')
                t.join()
        else:
            dtTime = createcpm['curTime']    
            createcpm['DT_RUN']= datetime.datetime.today().strftime('%Y-%m-%d')
            t = time.localtime()
            current_time = time.strftime("%H%M%S", t)
            createcpm['CURRTIME']= current_time
            
            cursor.execute('''insert into public."CPM_PROCESS" ("START_DT", "START_TIME") values (%s,%s);''',[ createcpm['DT_RUN'],createcpm['CURRTIME']])
            ret=expolde()
            status=ret[0]['status']
            msg=ret[0]['msg']
            btn=ret[0]['btn'] 
        if r!=0 and msg !='':          
            msg= "Explode Aborted"
            r=0
        print(msg)
        lst=[{'status':r,'msg':msg}]
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success:False"},status=400)