from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date,timedelta,time
import time
import re
import datetime,calendar
from calendar import monthrange
from array import array
from django.contrib.sessions.models import Session
from rest_framework.views import APIView
from rest_framework.response import Response
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
from authy.api import AuthyApiClient
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from dlw.decorators import role_required
from django.db.models import Max
from django.http import HttpResponseRedirect
import math,random
from random import randint
import datetime
import smtplib 
import pandas
import requests
from django.db.models import Q
from dlw.views.utils import render_to_pdf 
from django.db.models.functions import Substr
from django.db.models import Subquery,Sum,Count
from django.db.models import Sum,Subquery
from django.utils import formats
from django.utils.dateformat import DateFormat
from decimal import *
from dlw.views import *
import dlw.views.globals as g
def GeneratePdf(request, *args, **kwargs):
    m13_no = request.GET.get('m13_no')
    m13_date = request.GET.get('m13_date')
    char_wo = request.GET.get('char_wo')
    sl_no = request.GET.get('sl_no')
    batch_no = request.GET.get('batch_no')
    epc = request.GET.get('epc')
    brn_no = request.GET.get('brn_no')
    loco_from = request.GET.get('loco_from')
    loco_to = request.GET.get('loco_to')
    assly_no = request.GET.get('assly_no')
    assly_desc = request.GET.get('assly_desc')
    part_no = request.GET.get('part_no')
    part_desc = request.GET.get('part_desc')
    quantity = request.GET.get('quantity')
    unit = request.GET.get('unit')
    pm_no = request.GET.get('pm_no')
    m14_no = request.GET.get('m14_no')
    rforhw = request.GET.get('rforhw')
    m14_date=datetime.datetime.now().strftime ("%d-%m-%Y")
    data = {
        'm14_date':m14_date,
        'rforhw':rforhw,
        'm14_no':m14_no,
        'pm_no':pm_no,
        'unit':unit,
        'quantity':quantity,
        'part_desc':part_desc,
        'part_no':part_no,
        'assly_desc':assly_desc,
        'assly_no':assly_no,
        'loco_to':loco_to,
        'loco_from':loco_from,
        'brn_no':brn_no,
        'epc':epc,
        'batch_no':batch_no,
        'sl_no':sl_no,
        'char_wo':char_wo,
        'm13_date':m13_date,
        'm13_no':m13_no,    
        }
    if str(m13_no)==str(0):
        pdf = render_to_pdf('MCARD/M14hw/m14genpdf2.html', data)
    else:
        pdf = render_to_pdf('MCARD/M14hw/m14genpdf1.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
@login_required
@role_required(urlpass='/m14hwview/')
def m14hwview(request):
    batch1 = list(Batch.objects.filter(status = 'R' , rel_date__isnull=False).values('bo_no').distinct())
    m13ref = list(M13.objects.filter(rej_cat='M14').values('slno').order_by('slno').distinct())
    context={
        'sub':0,
        'lenm' :2,
        'nav':g.nav,
        'ip':get_client_ip(request),
        'subnav':g.subnav,
        'm13ref' :m13ref,
        'batch1' :batch1, 
        'usermaster':g.usermaster,
                
    }
    return render(request,'MCARD/M14hw/m14hwview.html', context)

# @login_required
# @role_required(urlpass='/m14hwview/')
# def m14hwview(request):   
#     cuser=request.user
#     usermaster=empmast.objects.filter(empno=cuser).first()
#     rolelist=usermaster.role.split(", ")
#     nav=dynamicnavbar(request,rolelist)
#     menulist=set()
#     for ob in nav:
#         menulist.add(ob.navitem)
#     menulist=list(menulist)
#     subnav=subnavbar.objects.filter(parentmenu__in=menulist) 
#     batch1 = list(Batch.objects.filter(status = 'R' , rel_date__isnull=False).values('bo_no').distinct())
#     m13ref = list(M13.objects.filter(rej_cat='M14').values('slno').order_by('slno').distinct())
#     if "Superuser" in rolelist:
#         tm=shop_section.objects.all()
#         tmp=[]
#         for on in tm:
#             tmp.append(on.section_code)

#         context={
#             'sub':0,
#             'lenm' :2,
#             'nav':nav,
#             'ip':get_client_ip(request),
#             'roles':tmp,
#             'subnav':subnav,
#             'm13ref' :m13ref,
#             'batch1' :batch1, 
                   
#         }
#     return render(request,'m14hwview.html', context)

def m14getdate(request):
    if request.method == 'GET' and request.is_ajax():  
        partno_temp = request.GET.get('partno_temp')
        partnew = list(M13.objects.filter(slno = partno_temp ).values('epc','m13_date','m13_no','wo','wo_rep','reason','part_no','qty_rej','brn_no').distinct())
        s = list(partnew[0]['m13_date'])
        date='' . join(map(str,s))
        date = date[8:10] + "-" + date[5:7] + "-" + date[0:4]
        partnew[0]['m13_date'] = date
        return JsonResponse(partnew, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14hwpart(request):
    if request.method == 'GET' and request.is_ajax():  
        partno_temp = request.GET.get('partno_temp')
        partnew=list(Part.objects.filter(partno = partno_temp).values('des').distinct())
        if str(partno_temp)=='':
            partnew.insert(0,'A')      
        else:
            if len(partnew)<=0:
                partnew.insert(0,'Z')
            elif len(partnew)>0:
                partnew.insert(0,'ZR')
        return JsonResponse(partnew, safe = False)
    return JsonResponse({"success":False}, status=400)



def m14hwbatch_no(request):
    if request.method == 'GET' and request.is_ajax():  
        batch_temp = request.GET.get('batch')
        batchnew=list(Batch.objects.filter(bo_no = batch_temp, status = 'R' , rel_date__isnull=False).values('part_no','ep_type','brn_no','loco_to','loco_fr','rel_date','status','batch_qty').distinct())
        if len(batchnew)<=0:
                batchnew.insert(0,'Z')
        elif len(batchnew)>0:
                batchnew.insert(0,'ZR')
        return JsonResponse(batchnew, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14hwbatch_no1(request):
    if request.method == 'GET' and request.is_ajax():  
        batch_temp = request.GET.get('batch')
        part_temp = request.GET.get('part')
        batchnew=list(M14M4.objects.filter(bo_no = batch_temp,part_no=part_temp).values('assly_no','l_to','l_fr').distinct())
        if len(batchnew)<=0:
                batchnew.insert(0,'Z')
        elif len(batchnew)>0:
                batchnew.insert(0,'ZR')
        return JsonResponse(batchnew, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14hwpm1(request):
    if request.method == 'GET' and request.is_ajax():  
        batch_temp = request.GET.get('batch')
        qty=request.GET.get('qty')
        lt=request.GET.get('lt')
        lf=request.GET.get('lf')
        batchnew=list(M14M4.objects.filter(bo_no = batch_temp,assly_no=qty,l_to=lt,l_fr=lf).values('unit','pm_no','brn_no','qty','epc').distinct())
        return JsonResponse(batchnew, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14hwassly(request):
    if request.method == 'GET' and request.is_ajax():  
        temp = request.GET.get('temp')
        partnew = list(Part.objects.filter(partno = temp ).values('des').distinct())
        return JsonResponse(partnew, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14hwasslyno(request):
    if request.method == 'GET' and request.is_ajax():  
        temp = request.GET.get('part')
        partnew = list(M14M4.objects.filter(bo_no = temp ).values('part_no').distinct())
        return JsonResponse(partnew, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14hwsave(request):
    response_data = {}
    if request.method == 'GET' and request.is_ajax():
        m13_no = request.GET.get('sl_no')
        m13_date = request.GET.get('m13_date')
        char_wo = request.GET.get('char_wo')
        sl_no = request.GET.get('m13_no')
        batch_no = request.GET.get('batch_no')
        epc = request.GET.get('epc')
        brn_no = request.GET.get('brn_no')
        loco_from = request.GET.get('loco_from')
        loco_to = request.GET.get('loco_to')
        assly_no = request.GET.get('assly_no')
        assly_desc = request.GET.get('assly_desc')
        part_no = request.GET.get('part_no')
        part_desc = request.GET.get('part_desc')
        quantity = request.GET.get('quantity')
        unit = request.GET.get('unit')
        pm_no = request.GET.get('pm_no')
        m14_no = request.GET.get('m14_no')
        rforhw = request.GET.get('rforhw')
        loco_no = request.GET.get('loco_no')
        m14_date=datetime.datetime.now().strftime ("%d-%m-%Y")
        
        response_data=m14_no                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        M14HW11.objects.create(doc_code='89',m14_no=str(m14_no),m14_date=str(m14_date),m13_no=str(m13_no),m13_date=str(m13_date),char_wo=str(char_wo),sl_no=str(sl_no),batch_no=str(batch_no),brn_no=brn_no,epc=str(epc),l_fr=str(loco_from),l_to=str(loco_to),pm_no=str(pm_no),part_no=str(part_no),part_desc=str(part_desc),qty=quantity,reason=str(rforhw),assly_no=str(assly_no),assly_desc=str(assly_desc),unit=unit,epc_old=str(''),loco_no=str(loco_no))
        Code.objects.filter(cd_type='21',code = 'M14' ).update(num_1=int(m14_no))
        return JsonResponse(response_data, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14getdoc_no(request):
    if request.method == 'GET' and request.is_ajax():  
        temp = request.GET.get('temp')
        c_date = datetime.datetime.now().strftime ("%d-%m-%Y")
        docno = list(Code.objects.filter(cd_type='21',code = 'M14' ).values('num_1').order_by('-num_1').distinct())
        docno.insert(1,c_date)
        return JsonResponse(docno, safe = False)
    return JsonResponse({"success":False}, status=400)
