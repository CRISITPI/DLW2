from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/m5hwview/')
def m5hwview(request):
    
    tempLength = 0
    cuser=(g.usermaster).empno
    tm=shop_section.objects.all()
    tmp=[]
    for on in tm:
        tmp.append(on.section_code)
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'roles':tmp,
        'subnav':g.subnav,
        'cuser':cuser,
        'usermaster':g.usermaster,
    }
        
    if request.method=="POST":
        submit = request.POST.get('userNameGo')  
        submitSelectOPN = request.POST.get('selectOPN')  
        submitproceed = request.POST.get('proceed')  
        submitSelectOPNBack = request.POST.get('selectFianlBack')  
        submitbackSelectOPN = request.POST.get('backSelectOPN')  
        submitBackMultiplaRowData = request.POST.get('backMultiplaRowData')  
        SubmitMultipleRowData = request.POST.get('SubmitMultipleRowData') 
        SubmitSaveAndUpdate = request.POST.get('saveAndUpdate') 
        submitInbox = request.POST.get('submitInbox')  
        backSubmitMultipleRowData =request.POST.get('backSubmitMultipleRowData')          
        SubmitMultipleRowDataInbox = request.POST.get('SubmitMultipleRowDataInbox')  
        SubmitMultipleRowDatadecision = request.POST.get('SubmitMultipleRowDatadecision')  
        SubmitSelectDocs = request.POST.get('selectDocs')  
        SubmitCreateM5M18 = request.POST.get('createM5M18')  
        printApprovalList = request.POST.get('printApprovalList')  

        if SubmitCreateM5M18=="Create M5/M18":
            context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'usermaster':g.usermaster,
            'cuser':cuser        
           
            }
            return render(request,"MCARD/M5HWCARD/m5hwviewFinal.html",context) 


        if SubmitSelectDocs=="Select Docs":
            batchQty=request.POST.get('batchQty') 
            batchNo=request.POST.get('batchNo')  
            temp=list(Hwm5Inbox.objects.all().filter(sel_sw='Y').exclude(cardstatus='Y'))
            context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'cuser':cuser,
            'temp':temp,
            'usermaster':g.usermaster,
            'batchQty':batchQty,
            'batchNo':batchNo
            }
            return render(request,"MCARD/M5HWCARD/m5hwviewInboxDecision.html",context) 


        if submitInbox=="Submit":
            batchQty=request.POST.get('batchQty')
            batchNo=request.POST.get('batchNo')  
            temp=list(Hwm5Inbox.objects.all().filter(sel_sw='Y').exclude(cardstatus='Y'))
            context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'cuser':cuser,
            'usermaster':g.usermaster,
            'temp':temp,
            'batchQty':batchQty,
            'batchNo':batchNo
            }
            return render(request,"MCARD/M5HWCARD/m5hwviewInboxDecision.html",context) 

        if backSubmitMultipleRowData=="back": 
            return render(request,"MCARD/M5HWCARD/m5hwview.html",context) 

        if submit=="GO":   
            context={
            'sub':0,
            'lenm' :2,
            'usermaster':g.usermaster,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'cuser':cuser
        }         
            return render(request,"MCARD/M5HWCARD/m5hwviewFinal.html",context)
        if submitbackSelectOPN=="back":
            context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'usermaster':g.usermaster,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'cuser':cuser
        }
            return render(request,"MCARD/M5HWCARD/m5hwviewFinal.html",context)     
        if submitSelectOPN=="Select OPN":
            context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'usermaster':g.usermaster,
            'cuser':cuser
        }
            return render(request,"MCARD/M5HWCARD/m5hwViewSelectOPN.html",context)              
        if submitBackMultiplaRowData=="back":
            context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'usermaster':g.usermaster,
            'cuser':cuser
        }
            return render(request,"MCARD/M5HWCARD/m5hwViewSelectOPN.html",context)   
        if submitSelectOPNBack=="back":
            context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'usermaster':g.usermaster,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'cuser':cuser
        }
            return render(request,"MCARD/M5HWCARD/m5hwview.html",context)  

        if submitproceed=="Proceed":
            partNo  = request.POST.get('partNo')
            batchNo = request.POST.get('batchNo')
            batchQty= request.POST.get('batchQty')
            locoFrom= request.POST.get('locoFrom')
            locoTo  = request.POST.get('locoTo')
            m4Req   = request.POST.get('m4Req')
            selectOPNForm= request.POST.get('selectOPNForm')
            totDetails = list(Hwm5.objects.filter(part_no = partNo,batch_no=batchNo).values('hw_cd','part_no','des','sel_sw','opn','opn_desc','shop_sec','lc_no','pa','at','time_pcpls','tot_hrspls','batch_no','org_batch','epc','seq','l_fr','l_to','m13_no','m13_date','brn_no','org_brnno','m5_cd','ncp_jbs','okmrq','rm_partno','rm_desc','rm_qty','rm_ut','sn','plregno','pr_shopsec','n_shopsec','usr_cd'))           
            context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'cuser':cuser,
            'usermaster':g.usermaster,
            'totDetails':totDetails,
            'batchQty':batchQty,
            'batchNo':batchNo
            }
            return render(request,"MCARD/M5HWCARD/m5hwViewMultipelRowData.html",context)  
        
        
        if printApprovalList=="View/Print Approval List":       
            temp=list(Hwm5Inbox.objects.all().filter(cardstatus='Y'))
            countemp=Hwm5Inbox.objects.all().filter(cardstatus='Y').count()
            userNameTemp  = request.POST.get('userName')
            context={  
            'nav':g.nav,
            'usermaster':g.usermaster,
            'ip':get_client_ip(request),           
            'subnav':g.subnav,
            'temp':temp,
            'userNameTemp':userNameTemp,
            'countemp':countemp            
            }                     
            return render(request,"MCARD/M5HWCARD/m5hwViewPrint.html",context) 


        if SubmitMultipleRowDatadecision=="Submit":             
            dataFormTemp  = request.POST.get('dataForm')
            mID1          = request.POST.get('id')
            batchQty      = request.POST.get('batchQty')
            batchNo       = request.POST.get('batchNo')
            tempID        = dataFormTemp.split(',')[35]
            
            Hwm5Inbox.objects.filter(id=tempID).update(cardstatus=str("Y"))  
            temp=list(Hwm5Inbox.objects.all().filter(sel_sw='Y').exclude(cardstatus='Y'))

            context={
            'mID1':mID1,   
            'nav':g.nav,
            'ip':get_client_ip(request),           
            'subnav':g.subnav,
            'batchQty' : batchQty,
            'hwcdTemp' : dataFormTemp.split(',')[0],
            'partNoTemp' : dataFormTemp.split(',')[1],
            'desTemp' : dataFormTemp.split(',')[2],
            'selTemp' : dataFormTemp.split(',')[3],
            'opnNoTemp' : dataFormTemp.split(',')[4],
            'opn_descTemp' : dataFormTemp.split(',')[5],
            'shop_secTemp' : dataFormTemp.split(',')[6],
            'lc_noTemp' : dataFormTemp.split(',')[7],
            'paTemp' : dataFormTemp.split(',')[8],
            'atTemp' : dataFormTemp.split(',')[9],
            'time_pcplsTemp' : dataFormTemp.split(',')[10],
            'tot_hrsplsTemp' : dataFormTemp.split(',')[11],
            'batchNo' : dataFormTemp.split(',')[13],
            'org_batchTemp' : dataFormTemp.split(',')[12],
            'epcTemp' : dataFormTemp.split(',')[14],
            'seqTemp' : dataFormTemp.split(',')[17],
            'l_frTemp' : dataFormTemp.split(',')[18],
            'l_toTemp' : dataFormTemp.split(',')[19],
            'm13_noTemp' : dataFormTemp.split(',')[16],
            'm13_dateTemp' : dataFormTemp.split(',')[15],
            'brn_noTemp' : dataFormTemp.split(',')[20],
            'org_brnnoTemp' : dataFormTemp.split(',')[21],
            'm5_cdTemp' : dataFormTemp.split(',')[22],
            'ncp_jbsTemp' : dataFormTemp.split(',')[23],
            'okmrqTemp' : dataFormTemp.split(',')[26],
            'rm_partnoTemp' : dataFormTemp.split(',')[28],
            'rm_descTemp' : dataFormTemp.split(',')[24],
            'rm_qtyTemp' : dataFormTemp.split(',')[29],
            'rm_utTemp' : dataFormTemp.split(',')[30],
            'snTemp' : dataFormTemp.split(',')[27],
            'plregnoTemp' : dataFormTemp.split(',')[25],
            'pr_shopsecTemp' : dataFormTemp.split(',')[31],
            'n_shopsecTemp' : dataFormTemp.split(',')[32],
            'temp':temp,
            'usermaster':g.usermaster,
            'testTemp':1
            }       
                    
            return render(request,"MCARD/M5HWCARD/m5hwviewInboxDecision.html",context) 

        if SubmitMultipleRowDataInbox=="Submit":             
            dataFormTemp  = request.POST.get('dataForm')
            mID1          = request.POST.get('id')
            batchQty      = request.POST.get('batchQty')
            batchNo       = request.POST.get('batchNo')
            context={
            'mID1':mID1,   
            'nav':g.nav,
            'ip':get_client_ip(request),           
            'subnav':g.subnav,
            'batchQty' : batchQty,
            'batchNo' : batchNo,
            'hwcdTemp' : dataFormTemp.split(',')[0],
            'partNoTemp' : dataFormTemp.split(',')[1],
            'desTemp' : dataFormTemp.split(',')[2],
            'selTemp' : dataFormTemp.split(',')[3],
            'opnNoTemp' : dataFormTemp.split(',')[4],
            'opn_descTemp' : dataFormTemp.split(',')[5],
            'shop_secTemp' : dataFormTemp.split(',')[6],
            'lc_noTemp' : dataFormTemp.split(',')[7],
            'paTemp' : dataFormTemp.split(',')[8],
            'atTemp' : dataFormTemp.split(',')[9],
            'time_pcplsTemp' : dataFormTemp.split(',')[10],
            'tot_hrsplsTemp' : dataFormTemp.split(',')[11],
            'org_batchTemp' : dataFormTemp.split(',')[12],
            'epcTemp' : dataFormTemp.split(',')[14],
            'seqTemp' : dataFormTemp.split(',')[17],
            'l_frTemp' : dataFormTemp.split(',')[18],
            'l_toTemp' : dataFormTemp.split(',')[19],
            'm13_noTemp' : dataFormTemp.split(',')[16],
            'm13_dateTemp' : dataFormTemp.split(',')[15],
            'brn_noTemp' : dataFormTemp.split(',')[20],
            'org_brnnoTemp' : dataFormTemp.split(',')[21],
            'm5_cdTemp' : dataFormTemp.split(',')[22],
            'ncp_jbsTemp' : dataFormTemp.split(',')[23],
            'okmrqTemp' : dataFormTemp.split(',')[26],
            'rm_partnoTemp' : dataFormTemp.split(',')[28],
            'rm_descTemp' : dataFormTemp.split(',')[24],
            'rm_qtyTemp' : dataFormTemp.split(',')[29],
            'rm_utTemp' : dataFormTemp.split(',')[30],
            'snTemp' : dataFormTemp.split(',')[27],
            'plregnoTemp' : dataFormTemp.split(',')[25],
            'pr_shopsecTemp' : dataFormTemp.split(',')[31],
            'n_shopsecTemp' : dataFormTemp.split(',')[32],
            'id' : dataFormTemp.split(',')[37],
            'usermaster':g.usermaster,
            }           
            return render(request,"MCARD/M5HWCARD/m5hwviewFinal.html",context) 

        if SubmitMultipleRowData=="Submit":             
            dataFormTemp  = request.POST.get('dataForm')
            mID1          = request.POST.get('id')
            batchQty      = request.POST.get('batchQty')
            batchNo      = request.POST.get('batchNo')
            context={
            'mID1':mID1,   
            'nav':g.nav,
            'ip':get_client_ip(request),           
            'subnav':g.subnav,
            'batchQty' : batchQty,
            'usermaster':g.usermaster,
            'batchNo' :batchNo,
            'hwcdTemp' : dataFormTemp.split(',')[0],
            'partNoTemp' : dataFormTemp.split(',')[1],
            'desTemp' : dataFormTemp.split(',')[2],
            'selTemp' : dataFormTemp.split(',')[3],
            'opnNoTemp' : dataFormTemp.split(',')[4],
            'opn_descTemp' : dataFormTemp.split(',')[5],
            'shop_secTemp' : dataFormTemp.split(',')[6],
            'lc_noTemp' : dataFormTemp.split(',')[7],
            'paTemp' : dataFormTemp.split(',')[8],
            'atTemp' : dataFormTemp.split(',')[9],
            'time_pcplsTemp' : dataFormTemp.split(',')[10],
            'tot_hrsplsTemp' : dataFormTemp.split(',')[11],
            'org_batchTemp' : dataFormTemp.split(',')[12],
            'epcTemp' : dataFormTemp.split(',')[14],
            'seqTemp' : dataFormTemp.split(',')[17],
            'l_frTemp' : dataFormTemp.split(',')[18],
            'l_toTemp' : dataFormTemp.split(',')[19],
            'm13_noTemp' : dataFormTemp.split(',')[16],
            'm13_dateTemp' : dataFormTemp.split(',')[15],
            'brn_noTemp' : dataFormTemp.split(',')[20],
            'org_brnnoTemp' : dataFormTemp.split(',')[21],
            'm5_cdTemp' : dataFormTemp.split(',')[22],
            'ncp_jbsTemp' : dataFormTemp.split(',')[23],
            'okmrqTemp' : dataFormTemp.split(',')[26],
            'rm_partnoTemp' : dataFormTemp.split(',')[28],
            'rm_descTemp' : dataFormTemp.split(',')[24],
            'rm_qtyTemp' : dataFormTemp.split(',')[29],
            'rm_utTemp' : dataFormTemp.split(',')[30],
            'snTemp' : dataFormTemp.split(',')[27],
            'plregnoTemp' : dataFormTemp.split(',')[25],
            'pr_shopsecTemp' : dataFormTemp.split(',')[31],
            'n_shopsecTemp' : dataFormTemp.split(',')[32]
            }           
            return render(request,"MCARD/M5HWCARD/m5hwviewFinal.html",context) 

        if SubmitSaveAndUpdate=="Save/Update":          
                                             
            hwcd            = request.POST.get('hwcd')
            partNoTemp      = request.POST.get('partNoTemp')
            desTemp         = request.POST.get('desTemp')
            if(hwcd == ''):
                sel         = ''
            else:
                sel         = 'Y'
            opnNoTemp       = request.POST.get('opnNoTemp')
            opn_descTemp    = request.POST.get('opn_descTemp')
            shop_secTemp    = request.POST.get('shop_secTemp')
            lc_noTemp       = request.POST.get('lc_noTemp')
            paTemp          = request.POST.get('paTemp')
            atTemp          = request.POST.get('atTemp')
            noOff           = request.POST.get('noOff')
            time_pcplsTemp  = request.POST.get('time_pcplsTemp')
            tot_hrsplsTemp  = request.POST.get('tot_hrsplsTemp')
            batchNo         = request.POST.get('batchNo')
            org_batchTemp   = request.POST.get('org_batchTemp')
            epcTemp         = request.POST.get('epcTemp')
            seq             = request.POST.get('seq')
            qtyOrder        = request.POST.get('qtyOrder')
            locoFrom        = request.POST.get('locoFrom')
            locoTo          = request.POST.get('locoTo')
            m13_noTemp      = request.POST.get('m13_noTemp')
            m13_dateTemp    = request.POST.get('m13_dateTemp')
            brn_noTemp      = request.POST.get('brn_noTemp')
            org_brnnoTemp   = request.POST.get('org_brnnoTemp')
            pShop           = request.POST.get('pShop')               
            nShop           = request.POST.get('nShop')
            m5cd            = request.POST.get('m5cd')
            ncp_jbsTemp     = request.POST.get('ncp_jbsTemp')
            okmrq           = request.POST.get('okmrq')
            snTemp          = request.POST.get('snTemp')            
            rm_partnoTemp   = request.POST.get('rm_partnoTemp')
            rm_qtyTemp      = request.POST.get('rm_qtyTemp')
            rm_utTemp       = request.POST.get('rm_utTemp')
            pr_shopsecTemp  = request.POST.get('pr_shopsecTemp')
            n_shopsecTemp   = request.POST.get('n_shopsecTemp')
            remarkM5CD      = request.POST.get('remarkM5CD')
            mID1           = request.POST.get('mID1')
            id           = request.POST.get('id')

            if id!="":
                if m5cd=="5":
                    qtyOrder = qtyOrder
                    for i in range(0, int(qtyOrder)):   
                        locoTo=locoFrom                               
                        Hwm5Inbox.objects.filter(id=id).update(hw_cd=str(hwcd), part_no=str(partNoTemp),  des=str(desTemp),  sel_sw=str(sel),  opn=str(opnNoTemp),  opn_desc=str(opn_descTemp), shop_sec=str(shop_secTemp),  lc_no=str(lc_noTemp), pa=str(paTemp),  at=str(atTemp),  no_off=str(noOff), time_pcpls=str(time_pcplsTemp), tot_hrspls=str(tot_hrsplsTemp), batch_no=str(batchNo), org_batch=str(org_batchTemp), epc=str(epcTemp),  seq=str(seq),  qty_ord=str(qtyOrder),  l_fr=str(locoFrom), l_to=str(locoTo), m13_no=str(m13_noTemp), brn_no=str(brn_noTemp), org_brnno=str(org_brnnoTemp), pr_shopsec=str(pShop), n_shopsec=str(nShop), m5_cd=str(m5cd), ncp_jbs=str(ncp_jbsTemp), okmrq=str(okmrq), sn=str(snTemp), rm_partno=str(rm_partnoTemp), rm_qty=str(rm_qtyTemp), rm_ut=str(rm_utTemp), remarks=str(remarkM5CD))
                        locoFrom=int(locoFrom)+1 
                else:
                    Hwm5Inbox.objects.filter(id=id).update(hw_cd=str(hwcd), part_no=str(partNoTemp),  des=str(desTemp),  sel_sw=str(sel),  opn=str(opnNoTemp),  opn_desc=str(opn_descTemp), shop_sec=str(shop_secTemp),  lc_no=str(lc_noTemp), pa=str(paTemp),  at=str(atTemp),  no_off=str(noOff), time_pcpls=str(time_pcplsTemp), tot_hrspls=str(tot_hrsplsTemp), batch_no=str(batchNo), org_batch=str(org_batchTemp), epc=str(epcTemp),  seq=str(seq),  qty_ord=str(qtyOrder),  l_fr=str(locoFrom), l_to=str(locoTo), m13_no=str(m13_noTemp), brn_no=str(brn_noTemp), org_brnno=str(org_brnnoTemp), pr_shopsec=str(pShop), n_shopsec=str(nShop), m5_cd=str(m5cd), ncp_jbs=str(ncp_jbsTemp), okmrq=str(okmrq), sn=str(snTemp), rm_partno=str(rm_partnoTemp), rm_qty=str(rm_qtyTemp), rm_ut=str(rm_utTemp), remarks=str(remarkM5CD))
            else:               
                if m5cd=="5":
                    qtyOrder = qtyOrder
                    for i in range(0, int(qtyOrder)):   
                        locoTo=locoFrom                               
                        Hwm5Inbox.objects.create(hw_cd=str(hwcd), part_no=str(partNoTemp),  des=str(desTemp),  sel_sw=str(sel),  opn=str(opnNoTemp),  opn_desc=str(opn_descTemp), shop_sec=str(shop_secTemp),  lc_no=str(lc_noTemp), pa=str(paTemp),  at=str(atTemp),  no_off=str(noOff), time_pcpls=str(time_pcplsTemp), tot_hrspls=str(tot_hrsplsTemp), batch_no=str(batchNo), org_batch=str(org_batchTemp), epc=str(epcTemp),  seq=str(seq),  qty_ord=str(qtyOrder),  l_fr=str(locoFrom), l_to=str(locoTo), m13_no=str(m13_noTemp), brn_no=str(brn_noTemp), org_brnno=str(org_brnnoTemp), pr_shopsec=str(pShop), n_shopsec=str(nShop), m5_cd=str(m5cd), ncp_jbs=str(ncp_jbsTemp), okmrq=str(okmrq), sn=str(snTemp), rm_partno=str(rm_partnoTemp), rm_qty=str(rm_qtyTemp), rm_ut=str(rm_utTemp), remarks=str(remarkM5CD))
                        locoFrom=int(locoFrom)+1 
                else:
                    Hwm5Inbox.objects.create(hw_cd=str(hwcd), part_no=str(partNoTemp),  des=str(desTemp),  sel_sw=str(sel),  opn=str(opnNoTemp),  opn_desc=str(opn_descTemp), shop_sec=str(shop_secTemp),  lc_no=str(lc_noTemp), pa=str(paTemp),  at=str(atTemp),  no_off=str(noOff), time_pcpls=str(time_pcplsTemp), tot_hrspls=str(tot_hrsplsTemp), batch_no=str(batchNo), org_batch=str(org_batchTemp), epc=str(epcTemp),  seq=str(seq),  qty_ord=str(qtyOrder),  l_fr=str(locoFrom), l_to=str(locoTo), m13_no=str(m13_noTemp), brn_no=str(brn_noTemp), org_brnno=str(org_brnnoTemp), pr_shopsec=str(pShop), n_shopsec=str(nShop), m5_cd=str(m5cd), ncp_jbs=str(ncp_jbsTemp), okmrq=str(okmrq), sn=str(snTemp), rm_partno=str(rm_partnoTemp), rm_qty=str(rm_qtyTemp), rm_ut=str(rm_utTemp), remarks=str(remarkM5CD))
            temp = Hwm5Inbox.objects.all()
                           
            context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':g.subnav,
            'cuser':cuser,
            'temp':temp,
            'tempLength':tempLength,
            'batchQty':qtyOrder,
            'usermaster':g.usermaster,
            'batchNo' : batchNo
            }
            return render(request,"MCARD/M5HWCARD/m5hwviewInbox.html",context)        
            
    return render(request,"MCARD/M5HWCARD/m5hwview.html",context)


def HWM5Validate(request):
    if request.method == "GET" and request.is_ajax():
        
        partNoTemp = request.GET.get('partNoTemp')   
        batchNo = request.GET.get('batchNo')       
        shop_secTemp = request.GET.get('shop_secTemp')          
    
        bono_Temp = list(M13.objects.filter(shop=shop_secTemp, part_no=partNoTemp,wo=batchNo).values('qty_rej').distinct())
        return JsonResponse(bono_Temp, safe = False)
    return JsonResponse({"success":False}, status=400)


def m5hwGetbatchNo(request):
    if request.method == "GET" and request.is_ajax():
        partNo = request.GET.get('partNo')
        msgSet = 'False'
        mob_temp=[]
        bono_Temp = Batch.objects.filter(part_no = partNo).values('bo_no').exclude(part_no__isnull=True).distinct()                  
        for i in bono_Temp: 
            mob_temp.append(i['bo_no'])
        for j in range(len(mob_temp)):
            if len(mob_temp[j]):
                msgSet = "True"
        return JsonResponse(msgSet, safe = False)
    return JsonResponse({"success":False}, status=400)

def m5hwGetbatchQtyDetails(request):
    if request.method == "GET" and request.is_ajax():
        partNo = request.GET.get('partNo')
        batchNo = request.GET.get('batchNo')             
        mob_temp=[]
        b_qty=0
        bono_Temp = Batch.objects.filter(part_no = partNo, bo_no = batchNo).values('loco_fr','loco_to').distinct() 
        qty=Batch.objects.filter(part_no = partNo, bo_no = batchNo).aggregate(Sum('batch_qty'))
        
        if len(qty)!=0:
            b_qty=qty['batch_qty__sum']
        for i in bono_Temp: 
            mob_temp.append(i['loco_fr'])
            mob_temp.append(i['loco_to'])
            mob_temp.append(b_qty)
            break
                      
        return JsonResponse(mob_temp, safe = False)
    return JsonResponse({"success":False}, status=400)


