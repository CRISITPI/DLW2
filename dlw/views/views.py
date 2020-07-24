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
from django.db.models import Avg, Max, Min, Sum
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.db import connection
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
from .rp import *
import pandas as pd
from django.db.models import Q
from dlw.views.utils import render_to_pdf 
from django.db.models.functions import Substr
from django.db.models import Subquery,Sum,Count
from django.db.models import Sum,Subquery
from django.utils import formats
from django.utils.dateformat import DateFormat
from decimal import *
from django.db.models import Sum,Subquery
from django.utils import formats
from django.db.models import Count
from django.db.models.functions import Substr
def viewsPermission(request):
    rolelist = roles.objects.all().values('role').order_by('role').distinct('role')
    urlfirst = navbar.objects.all().values('link').distinct('link')
    first = []
    for i in range(len(urlfirst)):
        if urlfirst[i]['link']!='#':
            first.append(urlfirst[i]['link'])
    urlsecond = subnavbar.objects.all().values('link').distinct('link')
    second = []
    for i in range(len(urlsecond)):
        if urlsecond[i]['link']!='#':
            second.append(urlsecond[i]['link'])
    urlprefinal = first + second
    urlmade1 = viewUrlPermission.objects.all().values('urlname').distinct('urlname')
    urlmade = []
    for i in range(len(urlmade1)):
        urlmade.append(urlmade1[i]['urlname'])
    urlnotmade = []
    for i in range(len(urlprefinal)):
        if urlprefinal[i] not in urlmade and urlprefinal[i]!='/password_reset_inside/':
            urlnotmade.append(urlprefinal[i])
    parentmenu = navbar.objects.all().values('navitem').distinct('navitem')
    parent = []
    for i in range(len(parentmenu)):
        if parentmenu[i]['navitem']!='Under Production' and parentmenu[i]['navitem']!='Not Authorized':
            parent.append(parentmenu[i]['navitem'])
    if request.method=="POST":
        inputurl = request.POST.get('inpurl')
        rolesassign = request.POST.getlist('rolesassign')
        navbarparent = request.POST.get('navbarparent')
        rolesassignlist= ", ".join(rolesassign)
        if inputurl and rolesassign and navbarparent:
            viewUrlPermission.objects.create(navitem=navbarparent,urlname=inputurl,rolespermission=rolesassignlist)
            messages.success(request,'Successful')
            return redirect('viewsPermission')
        else:
            messages.error(request,'error')
            return redirect('viewsPermission')
    context = {
        'ip':get_client_ip(request),
        'rolelist':rolelist,
        'urlnotmade' : urlnotmade,
        'parentmenu':parent,
    }
    return render(request,'ACCOUNT/viewsPermission.html',context)

def viewsPermissiondelete(request):
    urlmade = viewUrlPermission.objects.all().values('urlname').distinct('urlname')
    if request.method=="POST":
        inputurl = request.POST.get('inpurl')
        if inputurl:
            viewUrlPermission.objects.filter(urlname=inputurl).delete()
            messages.success(request,'Successful')
            return redirect('viewsPermissiondelete')
        else:
            messages.error(request,'error')
            return redirect('viewsPermissiondelete')
    context = {
        'ip':get_client_ip(request),
        'urlmade' : urlmade,
    }
    return render(request,'ACCOUNT/viewsPermissiondel.html',context)

def viewsPermissionUpdate(request):
    rolelist = roles.objects.all().values('role').order_by('role').distinct('role')
    urlmade = viewUrlPermission.objects.all().values('urlname').distinct('urlname')
    parentmenu = navbar.objects.all().values('navitem').distinct('navitem')
    parent = []
    for i in range(len(parentmenu)):
        if parentmenu[i]['navitem']!='Under Production' and parentmenu[i]['navitem']!='Not Authorized':
            parent.append(parentmenu[i]['navitem'])
    if request.method=="POST":
        inputurl = request.POST.get('inpurl')
        rolesassign = request.POST.getlist('rolesassign')
        navbarparent = request.POST.get('navbarparent')
        rolesassignlist= ", ".join(rolesassign)
        if inputurl and rolesassign and navbarparent:
            toupdate = viewUrlPermission.objects.filter(urlname=inputurl).first()
            toupdate.rolespermission = rolesassignlist
            toupdate.navitem = navbarparent
            toupdate.save()
            messages.success(request,'Successful')
            return redirect('viewsPermissionUpdate')
        else:
            messages.error(request,'error')
            return redirect('viewsPermissionUpdate')
    context = {
        'ip':get_client_ip(request),
        'rolelist':rolelist,
        'urlmade' : urlmade,
        'parentmenu':parent,
    }
    return render(request,'ACCOUNT/viewsPermissionUpdate.html',context)

from collections import defaultdict 
nav=defaultdict()
subnav=defaultdict()
# usermaster=defaultdict()
#rolelist = []
import dlw.views.globals as g
def login_request(request):
    if request.method=='POST':
        u_id = request.POST.get('user_id')
        pwd=request.POST.get('password') 
        #global usermaster
        global rolelist  
        user = authenticate(username=u_id, password=pwd)

        if user is not None:
            g.usermaster=empmast.objects.filter(empno=user).first()
            g.rolelist=(g.usermaster).role.split(", ")
            get_navbar(user)
    
            login(request, user) 
            if "Superuser" in g.rolelist:
                return redirect('homeadmin')
            else:
                return redirect('homeuser')
        else:
            messages.error(request,"Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'MAIN/login.html', {"form": form})

def get_navbar(user):          
    g.nav=dynamicnavbarNew()    
    menulist=set()
    for ob in g.nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)    
    g.subnav=subnavbar.objects.filter(parentmenu__in=menulist).order_by('childmenu')
   
def dynamicnavbarNew():
    if("Superuser" in g.rolelist):
        nav=navbar.objects.filter(role="Superuser")
        return nav
    else:       
        nav=navbar.objects.filter(role__in=g.rolelist).distinct('navmenu','navitem')        
        return nav
 


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def logout_request(request):
    if request.method=='POST':
        logout(request)
        data={}
        return JsonResponse(data)
    return HttpResponseRedirect('login')

@login_required
@role_required(urlpass='/homeadmin/')
def homeadmin(request):
    
    context={
        'nav':g.nav,
        'subnav':g.subnav,
        'usermaster':g.usermaster,
        'ip':get_client_ip(request),
    }
    return render(request,'MAIN/homeadmin.html',context)




@login_required
@role_required(urlpass='/homeuser/')
def homeuser(request):

    context={
        'nav':g.nav,
        'usermaster':g.usermaster,
        'ip':get_client_ip(request),
        'subnav':g.subnav
    }
    return render(request,'MAIN/homeuser.html',context)

@login_required
def dynamicnavbar(request,rolelist=[]):
    if("Superuser" in rolelist):
        nav=navbar.objects.filter(role="Superuser")
        return nav
    else:
        nav=navbar.objects.filter(role__in=rolelist).distinct('navmenu','navitem')
        return nav


@login_required
@role_required(urlpass='/createuser/')
def create(request):     
    # emp=empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL') | empmast.objects.filter(role__isnull=True,dept_desc='CRIS_MU')
    emp=empmast.objects.filter(role__isnull=True,dept_desc=(g.usermaster).dept_desc) 
    availableroles=roles.objects.all().values('parent').distinct()
    if request.method == "POST":
        emp_id=request.POST.get('emp_id')
        email=request.POST.get('email')
        role=request.POST.get('role')
        read=request.POST.get('read')
        create=request.POST.get('create')
        update=request.POST.get('update')
        delete=request.POST.get('delete')
        if read=='on':
           read=True 
        else:
           read=False

        if create=='on':
           create=True 
        else:
           create=False

        if update=='on':
           update=True 
        else:
           update=False

        if delete=='on':
           delete=True 
        else:
           delete=False

        sublevelrole=request.POST.getlist('sublevel')
        sublevelrolelist= ", ".join(sublevelrole)
        password="dlw@123"
        if "Superuser" in sublevelrole and emp_id and role and sublevelrole:
            employee=empmast.objects.filter(empno=emp_id).first()
            employee.role=sublevelrolelist
            employee.parent=role
            employee.op_read=read
            employee.op_create=create
            employee.op_update=update
            employee.op_delete=delete

            newuser = User.objects.create_user(username=emp_id, password=password,email=email)
            employee.save()
            newuser.is_staff= True
            newuser.is_superuser=True
            newuser.save()
            messages.success(request, 'Successfully Created!')
            return redirect('create')
        elif "Superuser" not in sublevelrole and emp_id and role and sublevelrole:
            employee=empmast.objects.filter(empno=emp_id).first()
            employee.role=sublevelrolelist
            employee.parent=role
            employee.op_read=read
            employee.op_create=create
            employee.op_update=update
            employee.op_delete=delete
            newuser = User.objects.create_user(username=emp_id, password=password,email=email)
            employee.save()
            newuser.is_staff= True
            newuser.is_superuser=False
            newuser.save()
            messages.success(request, 'Successfully Created!')
            return redirect('create')
        else:
            messages.error(request, 'Error, Try Again!')
    context={
        'nav':g.nav,
        'usermaster':g.usermaster,
        'emp':emp,
        'ip':get_client_ip(request),
        'roles':availableroles,
        'subnav':g.subnav,
    }

    return render(request,'ACCOUNT/createuser.html',context)
 
@login_required
@role_required(urlpass='/update_permission/')
def update_permission(request):
     
    users=User.objects.all()
    availableroles=roles.objects.all().values('parent').distinct() 
    if request.method == "POST":
        updateuser=request.POST.get('emp_id')
        sublevelrole=request.POST.getlist('sublevel')
        read=request.POST.get('read')
        create=request.POST.get('create')
        update=request.POST.get('update')
        delete=request.POST.get('delete')
        if read=='on':
           read=True 
        else:
           read=False

        if create=='on':
           create=True 
        else:
           create=False

        if update=='on':
           update=True 
        else:
           update=False

        if delete=='on':
           delete=True 
        else:
           delete=False
 
        role=request.POST.get('role')
        sublevelrolelist= ", ".join(sublevelrole)
        if updateuser and sublevelrole:
            usermasterupdate=empmast.objects.filter(empno=updateuser).first()
            usermasterupdate.role=sublevelrolelist
            usermasterupdate.parent=role
            usermasterupdate.op_read=read
            usermasterupdate.op_create=create
            usermasterupdate.op_update=update
            usermasterupdate.op_delete=delete
            usermasterupdate.save()
            messages.success(request, 'Successfully Updated!')
            return redirect('update_permission')
        else:
            messages.error(request,"Error!")
            return redirect('update_permission')

    context={
        'users':users,
        'nav':g.nav,
        'usermaster':g.usermaster,
        'ip':get_client_ip(request),
        'roles':availableroles,
        'subnav':g.subnav,
    }
    return render(request,'ACCOUNT/update_permission.html',context)



@login_required
def update_permission_incharge(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    parentrole=roles.objects.all().filter(role__in=rolelist).first()
    available=roles.objects.all().filter(parent=parentrole.parent).values('role').exclude(role__in=rolelist)
    users=empmast.objects.all().filter(parent=parentrole.parent).values('empno').exclude(role__in=rolelist)
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    if request.method == "POST":
        updateuser=request.POST.get('emp_id')
        sublevelrole=request.POST.getlist('sublevel')
        sublevelrolelist= ", ".join(sublevelrole)
        if updateuser and sublevelrole:
            usermasterupdate=empmast.objects.filter(empno=updateuser).first()
            usermasterupdate.role=sublevelrolelist
            usermasterupdate.save()
            messages.success(request, 'Successfully Updated!')
            return redirect('update_permission_incharge')
        else:
            messages.error(request,"Error!")
            return redirect('update_permission_incharge')

    context={
        'users':users,
        'nav':nav,
        'usermaster':usermaster,
        'ip':get_client_ip(request),
        'roles':available,
        'subnav':subnav,
    }
    return render(request,'ACCOUNT/update_permission_incharge.html',context)



@login_required
def update_emp_shift(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    parentrole=roles.objects.all().filter(role__in=rolelist).first()
    users=empmast.objects.all().filter(parent=parentrole.parent).exclude(role__in=rolelist)
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    now=datetime.datetime.now() + datetime.timedelta(days=7)
    stringdate=str(now.date())
    movetohistory=shift.objects.all().filter(validity_from__lt=date.today())
    movecount=movetohistory.count()
    yesterday=datetime.datetime.now() - datetime.timedelta(days=1)
    for i in range(movecount):
        shiftcount=shift.objects.get(emp_id=movetohistory[i].emp_id).count()
        if shiftcount>1:
            newhistory=shift_history.objects.create()
            newhistory.emp_id=movetohistory[i].emp_id
            newhistory.shift_id=movetohistory[i].shift_id
            newhistory.validity_from=movetohistory[i].validity_from
            newhistory.validity_to=yesterday
            newhistory.save()
            movetohistory[i].delete()
    context={
        'users':users,
        'nav':nav,
        'subnav':subnav,
        'ip':get_client_ip(request),
        'future':stringdate,
    }
    return render(request,'ACCOUNT/update_emp_shift.html',context)






def shiftsave(request):
    if request.method=="GET" and request.is_ajax():
        shiftemp=request.GET.get('shift')
        emp_id=request.GET.get('emp')
        datetosave=request.GET.get('seldate')
        datetosaveformatdate = datetime.datetime.strptime(datetosave, "%Y-%m-%d") 
        if datetosaveformatdate.date() == date.today():
            if emp_id and shiftemp and datetosave:
                updateuser=shift.objects.filter(emp_id=emp_id).count()
                if updateuser==0:
                    update=shift.objects.create()
                    update.emp_id=emp_id
                    update.shift_id=shiftemp
                    update.validity_from=datetosave
                    update.save()
                else:
                    up=shift.objects.filter(emp_id=emp_id).update(shift_id=shiftemp,validity_from=datetosave)
        elif datetosaveformatdate.date() < date.today():
            if emp_id and shiftemp and datetosave:
                updateuser=shift.objects.filter(emp_id=emp_id).count()
                

    data={}
    return JsonResponse(data)






@login_required
def update_emp_shift_admin(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    parentshops=roles.objects.all().distinct().values('parent').exclude(parent='Superuser')
    if request.method=="POST":
        emp_shiftupdate=request.POST.get('emp_id')
        shift=request.POST.get('shift')
        if emp_shiftupdate and shift:
            updateuser=empmast.objects.get(empno=emp_shiftupdate)
            if updateuser.shift_id is None:
                updateuser.shift_id=shift
                updateuser.validity_from=date.today()
                updateuser.save()
                messages.success(request, 'Successfully Updated!')
                return redirect('update_emp_shift_admin')
            else:
                newhistory=shift_history.objects.create()
                newhistory.emp_id=updateuser.emp_id
                newhistory.shift_id=updateuser.shift_id
                newhistory.validity_from=updateuser.validity_from
                newhistory.validity_to=date.today()
                newhistory.save()
                updateuser.shift_id=shift
                updateuser.validity_from=date.today()
                updateuser.save()
                messages.success(request, 'Successfully Updated!')
                return redirect('update_emp_shift_admin')
        else:
            messages.error(request,"Error!")
            return redirect('update_emp_shift_admin')
    context={
        'nav':nav,
        'subnav':subnav,
        'ip':get_client_ip(request),
        'parentshops':parentshops,
    }
    return render(request,'ACCOUNT/update_emp_shift_admin.html',context)

def getEmpInfo(request):
    if request.method == "GET" and request.is_ajax():
        emp_id=request.GET.get('username')
        try:
            emp=empmast.objects.filter(empno=emp_id).first()
            if(emp.parentshop is None):
                uniqparent = list(roles.objects.all().values('parent').distinct())
            else:
                uniqparent = list(roles.objects.all().values('parent').filter(parent = emp.parentshop).distinct())
        except:
            return JsonResponse({"success":False}, status=400)
        emp_info={
            "name":emp.empname,
            "designation":emp.desig_longdesc,
            "department":emp.dept_desc,
            "email":emp.email,
            "contactno":emp.contactno,
            "uniqparent" : uniqparent
        }
        return JsonResponse({"emp_info":emp_info}, status=200)

    return JsonResponse({"success":False}, status=400)

def getauthempInfo(request):
    if request.method == "GET" and request.is_ajax():
        emp_id=request.GET.get('username')
        emp=User.objects.filter(username=emp_id).first()
        if emp:
            usermaster=empmast.objects.filter(empno=emp).first()
            auth_info={
                "name":usermaster.empname,
                "designation":usermaster.desig_longdesc,
                "department":usermaster.dept_desc,
                "contactno":usermaster.contactno
            }
            return JsonResponse({"auth_info":auth_info}, status=200)
        else:
            auth_info={
                "name":"No User Found",
                "designation":"",
                "department":"",
                "contactno":""
            }
            return JsonResponse({"auth_info":auth_info}, status=200)
    return JsonResponse({"success":False}, status=400)

def getPermissionInfo(request):
    if request.method == "GET" and request.is_ajax():
        selectrole=request.GET.get('username')
        subshop=roles.objects.filter(parent=selectrole).values('role')
        sub=list(subshop.values('role'))
        permission_info={
            "sub":sub,
        }
        return JsonResponse({"permission_info":permission_info}, status=200)
    return JsonResponse({"success":False}, status=400)

def getshopempinfo(request):
    if request.method == "GET" and request.is_ajax():
        shop=request.GET.get('username')
        usermaster=empmast.objects.filter(parent=shop).values('empno')
        neededusers=list(usermaster.values('empno'))
        shopemp_info={
            "neededusers":neededusers,
            }
        return JsonResponse({"shopemp_info":shopemp_info}, status=200)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/delete_user/')
def delete_user(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    users=User.objects.all()
    if not users:
        messages.success(request, 'No User Exist!')
    elif request.method == "POST":
        deleteuser=request.POST.get('emp_id')
        delete=User.objects.filter(username=deleteuser).first()
        if not delete:
            messages.error(request,"Error, No user selected!")
            return redirect('delete_user')
        usermasterupdate=empmast.objects.filter(empno=delete.username).first()
        usermasterupdate.role=None
        usermasterupdate.parent=None
        delete.delete()
        usermasterupdate.save()
        messages.success(request, 'Successfully Deleted!')
        return redirect('delete_user')
    context={
        'users':users,
        'nav':nav,
        'usermaster':usermaster,
        'ip':get_client_ip(request),
        'subnav':subnav,
    }
    return render(request,'ACCOUNT/delete_user.html',context)


@login_required
@role_required(urlpass='/forget_password/')
def forget_password(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    if request.method == "POST":
        emp=request.POST.get('emp_id')
        forgetuser=User.objects.filter(username=emp).first()
        password=request.POST.get('password')
        conpassword=request.POST.get('conpassword')
        if forgetuser and password==conpassword:
            forgetuser.set_password(password)
            forgetuser.save()
            messages.info(request, 'Successfully Changed Password!')
            return redirect('forget_password')
        else:
            messages.info(request, 'Error, Try Again!')
            return redirect('forget_password')
    context={
        'nav':nav,
        'usermaster':usermaster,
        'ip':get_client_ip(request),
        'subnav':subnav,
    }
    return render(request,'MAIN/forget_password.html',context)

def forget_path(request):
    if request.method == "POST":
        option=request.POST.get('forget')
        if option=="Email":
            return redirect('password_reset')
        else:
            return redirect('forget_password_path')
    return render(request,'MAIN/forget_password_path.html',{})



class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self,request):
        obj= testc.objects.all()
        serializer=testSerializer(obj,many=True)
        return Response(serializer.data)







def getYrDgp(request):
    from .models import jpo
    if request.method == "GET" and request.is_ajax():
        num=0
        dgp=0
       
        typec=request.GET.get('username')
        if typec=='ind-rail' or typec=='nrc' or typec=='export' or typec=='nrcdgset' or typec=='zr' or typec=='zrover' or typec=='zrasstn':
            jpot='main'
        else:
            jpot='rsp'
        try:
            rev=request.GET.get('revex')
            emp=jpo.objects.filter(jpo=jpot,revisionid=rev).first()


        except:
            return JsonResponse({"success":False}, status=400)
       
        if emp is not None:
            num=emp.numyrs
            dgp=emp.numdgp
        
        jpo_info={
             "numfy":num,
             "dgp":dgp
         }
        
        return JsonResponse({"jpo_info":jpo_info}, status=200)

    return JsonResponse({"success":False}, status=400)

def checktotal(request):
    from dlw.models import jpo,annual_production,Dpo
    if request.method == "GET" and request.is_ajax():
        loco=request.GET.get('loconame')
        b2=request.GET.get('barl2')
        
        total=0
        try:
            obj=Dpo.objects.filter(loco_type=loco,order_no=b2)
            if(len(obj)):
                total=obj[0].total_count
            
        except:
            return JsonResponse({"success":False}, status=400)
   
        dpo_info={
            "total":total,
        }
        return JsonResponse({"dpo_info":dpo_info}, status=200)

    return JsonResponse({"success":False}, status=400)



def checkloco(request):
    from .models import jpo,annual_production
    if request.method == "GET" and request.is_ajax():
        lcname=request.GET.get('vdp')
        flag=0
        try:
            emp=annual_production.objects.filter(loco_type=lcname).exists()
            if emp is True:
                flag=1
        except:
            return JsonResponse({"success":False}, status=400)
        jpo_info={
            "flag":flag,
        }
        return JsonResponse({"jpo_info":jpo_info}, status=200)

    return JsonResponse({"success":False}, status=400)

def findthis(request,temp):
    templist=[]
    asci=temp
    ascil=[ord(cc) for cc in asci]
    thr=[]
    for i in range(len(ascil)):
        if ascil[i]==13:
            thr.append(i)
    k=0
    for i in range(len(thr)):
        s=''.join(chr(ascil[d]) for d in range(k,thr[i]))
        lis=[13,10]
        if len(s)>0 and s!=''.join(chr(i) for i in lis):
            k=thr[i]+2
            templist.append(s)
    s=''.join(chr(ascil[d]) for d in range(k,len(ascil)))
    if len(s)>0:
        templist.append(s)
    return templist
def getcumino(request):
    from dlw.models import Dpo,dpoloco
    l=[]
    b=[]
    if request.method == "GET" and request.is_ajax():
        cmno=0
        bnothr=0
       
        loco=request.GET.get('loco')
        locot=request.GET.get('locot')
        ordno=request.GET.get('ordno')
        try:
            emp=dpoloco.objects.filter(loconame=loco,locotype=locot,orderno=ordno)
        except:
            return JsonResponse({"success":False}, status=400)
        if emp is not None  and len(emp):
            cmno=412
            for i in range(len(emp)):
                p=emp[i].cumino
                l.append(int(p.split('-')[1]))
                
                bn=emp[i].batchordno
                b.append(bn)
            
            bnothr=str(max(b))
            bnothr=bnothr[5:8]
                
            cmno=max(l)+1
            
        else:
            if loco=='WAP-7':
                cmno=161
            elif loco=='WAG-9':
                cmno='001'
        
        dpo_info={
            "cumino":cmno,
            "bnothr":bnothr,
         }
        
        return JsonResponse({"dpo_info":dpo_info}, status=200)

    return JsonResponse({"success":False}, status=400)


def email1(sender_email_id,sender_email_id_password,receiver_email_id,message):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.ehlo()
    s.starttls()
    s.login(sender_email_id,sender_email_id_password)  
    s.sendmail(sender_email_id,receiver_email_id, message) 
    s.quit()
def sms(phoneno,message):
    url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to=91"+str(phoneno)+"&msg="+message+" &msg_type=TEXT&userid=2000184632&auth_scheme=plain&password=pWK3H5&v=1.1&format=text"
    
    response = requests.request("POST", url)




def smsM18(phoneno,message):
    url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to=91"+str(phoneno)+"&msg="+message+" &msg_type=TEXT&userid=2000184632&auth_scheme=plain&password=pWK3H5&v=1.1&format=text"
    
    response = requests.request("POST", url)



@login_required
@role_required(urlpass='/demandreg/')
def wogen(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context={
        'nav':nav,
        'subnav':subnav,
        'usermaster':usermaster,
        'ip':get_client_ip(request),
    }
    return render(request,'wogeneration.html',context)


def smsM13(phoneno,message):
    url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to=91"+str(phoneno)+"&msg="+message+" &msg_type=TEXT&userid=2000184632&auth_scheme=plain&password=pWK3H5&v=1.1&format=text"
    
    response = requests.request("POST", url)

@login_required
@role_required(urlpass='/RoleGeneration/')
def RoleGeneration(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    rolemenulist = roleMenu.objects.all().values('navitem').order_by('navitem').distinct()
    originalitems = navbar.objects.all().values('navitem').order_by('navitem').distinct()
    originalmenu = navbar.objects.all().values('navmenu').order_by('navmenu').distinct()
    originalnavitem = []
    originalnavmenu = []
    for i in range(len(originalitems)):
        originalnavitem.append(originalitems[i]['navitem'])
    for i in range(len(originalmenu)):
        originalnavmenu.append(originalmenu[i]['navmenu'])
    originalnavitem.remove('Under Production')
    originalnavitem.remove('Not Authorized')
    originalnavitem.remove('Update Permission Incharge')
    notpresent = []
    present = []
    if request.method=='POST':
        rolename = request.POST.get('rolename')
        perlist = request.POST.getlist('permissions')
        viewper = viewUrlPermission.objects.filter(navitem__in=perlist).values('rolespermission','id')
        if rolename and perlist:
            roles.objects.create(role=rolename,parent=rolename)
            for i in range(len(perlist)):
                toinsert = roleMenu.objects.all().filter(navitem=perlist[i]).first()
                present.append(toinsert.navmenu)
                navbar.objects.create(role=rolename,navmenu=toinsert.navmenu,navitem=toinsert.navitem,link=toinsert.link)
            for j in range(len(originalnavmenu)):
                if originalnavmenu[j] not in present:
                    notpresent.append(originalnavmenu[j])
            for i in range(len(notpresent)):
                navbar.objects.create(role=rolename,navmenu=notpresent[i],navitem='Not Authorized',link='#')
            for i in range(len(viewper)):
                tempper = viewper[i]['rolespermission']
                restemp = tempper.split(",")
                restemp.append(rolename)
                final = ", ".join(restemp)
                toupdate=viewUrlPermission.objects.get(id=viewper[i]['id'])
                toupdate.rolespermission = final
                toupdate.save()
            present.clear()
            notpresent.clear()
            originalnavmenu.clear()
            originalnavitem.clear()
            messages.success(request, 'Successfully Created!')
        else:
            messages.error(request,"Error")
    context = {
        'ip':get_client_ip(request),
        'nav':nav,
        'subnav':subnav,
        'rolemenulist':rolemenulist,
    }
    return render(request,'ACCOUNT/RoleGeneration.html',context)






@login_required
@role_required(urlpass='/RoleDelete/')
def RoleDelete(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    role = roles.objects.all().values('role').order_by('role').distinct()
    users = []
    if request.method=="POST":
        rolename = request.POST.get('roldel')
        if rolename:
            perlist = navbar.objects.filter(role=rolename).values('navitem').distinct()
            viewper = viewUrlPermission.objects.filter(navitem__in=perlist).values('rolespermission','id')
            for i in range(len(viewper)):
                tempper = viewper[i]['rolespermission']
                restemp = tempper.split(", ")
                restemp.remove(rolename)
                final = ", ".join(restemp)
                toupdate=viewUrlPermission.objects.get(id=viewper[i]['id'])
                toupdate.rolespermission = final
                toupdate.save()
            navbar.objects.all().filter(role=rolename).delete()
            roles.objects.all().filter(role=rolename).delete()
            userremove = empmast.objects.all().values('empno').filter(role=rolename)
            for i in range(len(userremove)):
                users.append(userremove[i]['empno'])
                empmast.objects.filter(empno=userremove[i]['empno']).update(role=None,parent=None)
            User.objects.filter(username__in=users).delete()
            messages.success(request, 'Successfully Deleted!')
        else:
            messages.error(request,"Error")
    context = {
        'ip':get_client_ip(request),
        'nav':nav,
        'subnav':subnav,
        'roles' : role,
    }
    return render(request,'ACCOUNT/RoleDelete.html',context)


def m3a(request):
    return render(request,"m3a.html")

def performaA(request):
    return render(request,"performaA.html")


def tooling_submit(request):
    context={}
    if request.method == "GET" and request.is_ajax():
        form_no=request.GET.get('tool_form')
        dname=request.GET.get('dname')
        d_date=request.GET.get('d_date')
        gname=request.GET.get('gname')
        g_date=request.GET.get('g_date')
        c_date=request.GET.get('c_date')
        l_date=request.GET.get('l_date')
        ref_date=request.GET.get('ref_date')
        comment1=request.GET.get('comment1')
        comment2=request.GET.get('comment2')
        l_no=request.GET.get('l_no1')
        obj=list(machine_tools.objects.filter(letter_no=l_no).values('letter_no').distinct())
        
        if len(obj)>0:
            tooling1.objects.create( name_designer=str(dname),date_designer=str(d_date),name_guide=str(gname),date_guide=str(g_date),date_completion=str(c_date),date_loading=str(l_date),sno_loading=str(ref_date),commment1=str(comment1),commment2=str(comment2),lno=str(l_no))
        return JsonResponse(context,safe=False)
    return JsonResponse({"success":False}, status=400)    



def toolPdf(request, *args, **kwargs):
    l_no = request.GET.get('l_no1')
    obj=mdescription.objects.filter(lno=l_no).values('description','quantity').distinct()
    obj2=list(machine_tools.objects.filter(letter_no=l_no).values('shop_no','shop_desc','date','new_requirement','modification','additional','existing_drawing','component_drawing','machine_no','machine_description','wsm_id','sse_id','wsm_name','wsm_mobile','sse_name','sse_mobile','name_supervisor','desig_supervisor','mobile_supervisor').distinct())
    dname=request.GET.get('dname')
    d_date=request.GET.get('d_date')
    gname=request.GET.get('gname')
    g_date=request.GET.get('g_date')
    c_date=request.GET.get('c_date')
    l_date=request.GET.get('l_date')
    ref_date=request.GET.get('ref_date')
    comment1=request.GET.get('comment1')
    comment2=request.GET.get('comment2')
    data={
        'l_no':l_no,
        'obj':obj,
        'obj2':obj2,
        'dname':dname,
        'gname':gname,
        'd_date':d_date,
        'g_date':g_date,
        'c_date':c_date,
        'l_date':l_date,
        'ref_date':ref_date,
        'comment1':comment1,
        'comment2':comment2
    }
    pdf = render_to_pdf('toolreport.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def fetchdetails_tools(request):
    l=[]
    if request.method == "GET" and request.is_ajax():
        no= request.GET.get('l_no')
        obj=list(machine_tools.objects.filter(letter_no=no).values('letter_no','shop_no','shop_desc','date','new_requirement','modification','additional','existing_drawing','component_drawing','machine_no','machine_description','wsm_id','sse_id','wsm_name','wsm_mobile','sse_name','sse_mobile','name_supervisor','desig_supervisor','mobile_supervisor').distinct())
        obj1=list(mdescription.objects.filter(lno=no).values('description','quantity','lno').distinct())
        l.append(obj)
        l.append(obj1)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)




def  getShopDesc(request):
    if request.method == "GET" and request.is_ajax():
        shopdesc = request.GET.get('tr_location')
        sd = list(Shop.objects.filter(shop =shopdesc).values('sh_desc').distinct())
        return JsonResponse(sd, safe = False)
    return JsonResponse({"success":False}, status=400)

def addInfo(request):
    if request.method == "GET" and request.is_ajax():
        tr_toolnum = request.GET.get('tr_toolnum')
        tr_dgnum = request.GET.get('tr_dgnum')
        tr_tooldesc = request.GET.get('tr_tooldesc')
        tr_plnum = request.GET.get('tr_plnum')
        sh_locn=request.GET.get('tr_location')
        doe = request.GET.get('doe')
        po_no = request.GET.get('po_no')
        make = request.GET.get('make')
        model = request.GET.get('model')
        cost = request.GET.get('cost')
        rangee = request.GET.get('rangee')
        uom = request.GET.get('uom')
        cal_freq = request.GET.get('cal_freq')
        acc_cri = request.GET.get('acc_cri')
        cali_link = request.GET.get('cali_link')
        pro_tol = request.GET.get('pro_tol')
        perror = request.GET.get('perror')
        merror = request.GET.get('merror')
        refstdno = request.GET.get('refstdno')
        win = request.GET.get('win')
        tr_shopdesc=request.GET.get('tr_shopdesc')
        today = str(date.today().strftime('%d-%m-%y'))
        cuser=request.user
        toolmdata.objects.create(TOOL_NUM=tr_toolnum,uom=uom,dg_num=tr_dgnum,tl_desc=tr_tooldesc,pl_num=tr_plnum,doe=doe,make=make,model=model,cost=cost,cal_freq=cal_freq,rangee=rangee,perror=perror,merror=merror,rsn=refstdno,win=win,acc_cri=acc_cri,cal_link=cali_link,pro_tol=pro_tol,po_no=po_no,sh_locn=sh_locn,tr_shopdesc=tr_shopdesc,flag='y',lastupddate=today,user=cuser)
        a=[]
        return JsonResponse(a, safe = False)
    return JsonResponse({"success":False}, status=400)


def delInfo(request):
    if request.method == "GET" and request.is_ajax():
        tr_toolnum = request.GET.get('tr_toolnum')
        toolmdata.objects.filter(TOOL_NUM=tr_toolnum).update(flag='n')
        a=[]
        return JsonResponse(a, safe = False)
    return JsonResponse({"success":False}, status=400)

def updateInfo(request):
    if request.method == "GET" and request.is_ajax():
        tr_toolnum = request.GET.get('tr_toolnum')
        a=list(toolmdata.objects.filter(TOOL_NUM=tr_toolnum).values())
        return JsonResponse(a, safe = False)
    return JsonResponse({"success":False}, status=400)

def updatetool(request):
    cuser=request.user
    if request.method == "GET" and request.is_ajax():
        tr_toolnum = request.GET.get('tr_toolnum')
        tr_dgnum = request.GET.get('tr_dgnum')
        tr_tooldesc = request.GET.get('tr_tooldesc')
        tr_plnum = request.GET.get('tr_plnum')
        sh_locn=request.GET.get('tr_location')
        doe = request.GET.get('doe')
        po_no = request.GET.get('po_no')
        make = request.GET.get('make')
        model = request.GET.get('model')
        cost = request.GET.get('cost')
        rangee = request.GET.get('rangee')
        uom = request.GET.get('uom')
        cal_freq = request.GET.get('cal_freq')
        acc_cri = request.GET.get('acc_cri')
        cali_link = request.GET.get('cali_link')
        pro_tol = request.GET.get('pro_tol')
        perror = request.GET.get('perror')
        merror = request.GET.get('merror')
        refstdno = request.GET.get('refstdno')
        win = request.GET.get('win')
        tr_shopdesc=request.GET.get('tr_shopdesc')
        today = str(date.today().strftime('%d-%m-%y'))
        b=list(toolmdata.objects.filter(TOOL_NUM=tr_toolnum).values('flag'))
        if(b[0]['flag']=='n'):
            toolmdata.objects.filter(TOOL_NUM=tr_toolnum).update(TOOL_NUM=tr_toolnum,uom=uom,dg_num=tr_dgnum,tl_desc=tr_tooldesc,pl_num=tr_plnum,doe=doe,make=make,model=model,cost=cost,cal_freq=cal_freq,rangee=rangee,perror=perror,merror=merror,rsn=refstdno,win=win,acc_cri=acc_cri,cal_link=cali_link,pro_tol=pro_tol,po_no=po_no,sh_locn=sh_locn,tr_shopdesc=tr_shopdesc,flag='y',lastupddate=today,user=str(cuser))
        elif(b[0]['flag']=='y'):
            toolmdata.objects.filter(TOOL_NUM=tr_toolnum).update(TOOL_NUM=tr_toolnum,dg_num=tr_dgnum,tl_desc=tr_tooldesc,pl_num=tr_plnum,doe=doe,make=make,model=model,cost=cost,cal_freq=cal_freq,rangee=rangee,perror=perror,merror=merror,rsn=refstdno,win=win,acc_cri=acc_cri,cal_link=cali_link,pro_tol=pro_tol,po_no=po_no,sh_locn=sh_locn,tr_shopdesc=tr_shopdesc,flag='y',uom=uom,lastupddate=today,user=str(cuser))
        a=[]
        return JsonResponse(a, safe = False)
    return JsonResponse({"success":False}, status=400)

def caldata(request):
    if request.method=="GET" and request.is_ajax():
        cy = request.GET.get('btnyear')
        myval=list(holidaylist.objects.filter(holiday_year=cy).values('holiday_year','holiday_name', 'holiday_date','holiday_type','remark').order_by('id'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)
def email(sender_email_id,sender_email_id_password,receiver_email_id,message):
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.ehlo()
    s.starttls()
    s.login(sender_email_id,sender_email_id_password)  
    s.sendmail(sender_email_id,receiver_email_id, message) 
    s.quit()

aimpl=pandas.DataFrame()
g_ep=''
g_epn = ''
session_aimpl=None
Ldbk=pandas.DataFrame()
def cpq(pn,ep,epn):
    q=0
    if pn == epn:
        return 1
    if(aimpl.empty==False):
        aimpl.drop(aimpl.index, inplace=True)
    ds=list(Nstr.objects.filter(cp_part=pn,epc=ep).values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt",
    "ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old"))
    if len(ds) == 0:
        return 0
    global g_ep
    global g_epn
    g_ep=ep
    g_epn=epn
    impl(pn,1)
    for i in range(len(aimpl)): 
        a=aimpl['0'].iloc[i]
        b=aimpl['1'].iloc[i]
        if(a==epn):
            q=q+int(b)   
    return str(q)

def impl(pn,wt):
    pp_part=''
    mpp_part=''
    ptc =''
    _epn=''
    qty=''
    try:
        dss=list(Nstr.objects.filter(cp_part=pn,epc=g_ep,).values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty","updt_dt",
        "ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by("cp_part","epc").distinct())
        global session_aimpl
        global aimpl

        if(aimpl.empty==True):
            aimpl=CreateDataTableaImpl(2)
            session_aimpl=aimpl   
        _epn=str(g_epn) 
        for i in range(len(dss)):
            pp_part = ""
            qty = 0
            
            l_fr = str(dss[i].get('l_fr'))
            l_to = str(dss[i].get('l_to'))
            lt = 9999
            lfr = int(l_fr)
            lto = int(l_to)

            if (not((lfr <= lt) and (lt <= lto))):
                continue
            
            pp_part=str(dss[i].get('pp_part'))
            qty=float(dss[i].get('qty'))
            ptc=str(dss[i].get('ptc'))
            
            if(pp_part==_epn):
                AddDataToTable1(pp_part,(qty*wt)) 
            mpp_part=pp_part

            dss1=list(Nstr.objects.filter(cp_part=mpp_part,epc=g_ep,).values("pp_part","cp_part","l_fr","l_to","ptc","epc",
            "qty","updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by("cp_part",
            "epc"))
            ln=["M","Z","L","B"]
            if((len(dss1)>0) and (ptc in ln)):
                impl(mpp_part,qty*wt) 
        return
    except:
        print("Implosion not done")
        return



def CreateDataTableaImpl(cols):
    data_table=pandas.DataFrame(columns=["0","1"])
    return data_table

def AddDataToTable1(a,b):
    global aimpl
    aimpl=aimpl.append({"0":a,"1":b},ignore_index=True)
        


        
g_curTime=''
system_date=datetime.date.today()

def sumexpl(assly,ep,lf,lt,qtyloco):
    global system_date
    system_date=datetime.date.today()
    global g_curTime
    cur_time=datetime.datetime.now().strftime("%H%M%S")
    
    g_curTime=cur_time
    delQtySum_Temp1()
    qty=1.000
    insertQtySum_temp1(assly, "M",qty, "01", lf, lt)
    expl(assly, 1, ep)
    delQtySum_Temp2()
    appendQtySum_Temp2()
    delQtySum_Temp()
    summarizeQtySum_Temp(qtyloco)
    return True

def expl(parent, wt, ep):
    mcp_part=''
    mqty=''
    shop_ut1=''
    v_ptc=''
    wt1=0
    mqty1=0
        
    cursor = connection.cursor()
    cursor.execute('select distinct n."PP_PART", n."CP_PART",n."PTC",n."QTY",p."SHOP_UT",n."L_FR",n."L_TO",COALESCE("ALT_IND",%s) from "NSTR" as n,"PART" as p where p."PARTNO" = n."CP_PART" and n."L_TO"=%s and n."PP_PART"=%s and  n."EPC"=%s order by n."PP_PART",n."CP_PART";',['0','9999',parent,ep])
    row = cursor.fetchall()
    dts = pandas.DataFrame(list(row))
        
    if(dts.shape[0]>0):
        for i in range(dts.shape[0]):
            l_fr=dts[5][i]
            l_to=dts[6][i]
            v_ptc=dts[2][i]
            mcp_part=dts[1][i]
            shop_ut=dts[4][i]
            mqty=dts[3][i]
            
            mqt=wt*mqty
            if v_ptc in ["Q","R"]:
                UpdateQtySum_temp1(mcp_part, v_ptc,mqty, shop_ut, l_fr, l_to, parent)
            else:
                insertQtySum_temp1(mcp_part, v_ptc, mqt, shop_ut, l_fr, l_to)
            ds1=list(Nstr.objects.filter(pp_part=mcp_part,epc=ep,l_to='9999').values("pp_part","cp_part","l_fr","l_to","ptc","epc","qty",
            "updt_dt","ref_ind","ref_no","alt_ind","alt_link","lead_time","reg_no","slno","del_fl","epc_old").order_by("pp_part",
            "epc","cp_part"))        
            if v_ptc in ["M","Z","L","B"] and len(ds1)>0:
                expl(mcp_part, mqt, ep) 
    return        

def delQtySum_Temp():
    try:
        QtysumTemp.objects.filter(dt_run__lt=system_date).delete()
        return
    except:
        print("Data not deleted : QTYSUM_TEMP")   
        return 


def delQtySum_Temp2():
    try:
        QtysumTemp2.objects.filter(dt_run__lt=system_date).delete()
        return
    except:
        print("Data not deleted : QTYSUM_TEMP2")  
        return  
    
def appendQtySum_Temp2():
    try:
        tmpstr=list(QtysumTemp1.objects.filter(cur_time=g_curTime).values("partno" ,"ptc" ,"qty" ,"shop_ut","l_fr","l_to","rm_part","rm_ptc","rm_qty","rm_ut","rm_lf","rm_lt","dt_run","cur_time"))
        for i in range(len(tmpstr)):
            QtysumTemp2.objects.create(partno=tmpstr[i].get('partno') ,ptc=tmpstr[i].get('ptc') ,qty=tmpstr[i].get('qty') ,shop_ut=tmpstr[i].get('shop_ut'),pt_lf=tmpstr[i].get('l_fr'),pt_lt=tmpstr[i].get('l_to'),rm_part=tmpstr[i].get('rm_part'),rm_ptc=tmpstr[i].get('rm_ptc'),rm_qty=tmpstr[i].get('rm_qty'),rm_ut=tmpstr[i].get('rm_ut'),rm_lf=tmpstr[i].get('rm_lf'),rm_lt=tmpstr[i].get('rm_lt'),dt_run=tmpstr[i].get('dt_run'),cur_time=tmpstr[i].get('cur_time'))
        return
    except:
        print("Insertion not successful : QTYSUM_TEMP2") 
        return 

   
def insertQtySum_temp1(part_n,pt,qt,shop_u,l_f,l_t): 
    try: 
        QtysumTemp1.objects.create(partno=str(part_n),ptc=str(pt),qty=qt,shop_ut=str(shop_u),l_fr=str(l_f),l_to=str(l_t),
        rm_part='',rm_ptc='',rm_qty=0.00,rm_ut='',rm_lf='',rm_lt='',dt_run=system_date,cur_time=str(g_curTime))         
        return 
    except:
        print("Insertion not successful : QTYSUM_TEMP1") 
        return 

        

def summarizeQtySum_Temp(qtyloco):
    cursor = connection.cursor()
    cursor.execute('select "PARTNO" ,max(coalesce("PTC"::text,%s)) ptc ,sum(coalesce("QTY" :: float,%s)) * (%s::int) qty ,max(coalesce("SHOP_UT"::text,%s)) shop_ut,max(coalesce("PT_LF"::text,%s)) pt_lf,max(coalesce("PT_LT"::text,%s)) pt_lt,max(coalesce("RM_PART"::text,%s)) rm_part ,max(coalesce("RM_PTC",%s)) rm_ptc ,max(coalesce("RM_QTY"::float,%s)) rm_qty ,max(coalesce("RM_UT"::text,%s)) rm_ut from public."QTYSUM_TEMP2" where "CUR_TIME"=%s and  "PTC" IN (%s,%s,%s,%s)  group by "PARTNO" order by "PARTNO";',['0','0',qtyloco,'0','0','0','0','0','0','0',g_curTime,'M','Z','L','B'])
    row = cursor.fetchall()
    dts = pandas.DataFrame(list(row))
    if(dts.shape[0]>0):
        for i in range(dts.shape[0]):
            partno=dts[0][i]
            ptc=dts[1][i]
            qty=dts[2][i]
            shop_ut=dts[3][i]
            pt_lf=dts[4][i]
            pt_lt=dts[5][i]
            rm_part=dts[6][i]
            rm_ptc=dts[7][i]
            rm_qty=dts[8][i]
            rm_ut=dts[9][i]
        
            QtysumTemp.objects.create(partno=str(partno),ptc=str(ptc),qty=qty,shop_ut=str(shop_ut),ptlf=str(pt_lf),ptlt=str(pt_lt),
            rm_part=str(rm_part),rm_ptc=str(rm_ptc),rm_qty=rm_qty,rm_ut=str(rm_ut),rmlf='',rmlt='',remark = '',qty_loco='',dt_run=system_date,cur_time=str(g_curTime)) 
                
    return

def delQtySum_Temp1():
    try:
        QtysumTemp1.objects.filter(dt_run__lt= system_date).delete()
        return
    except:
        print("Data not deleted : QTYSUM_TEMP1") 
        return 

def delLOADBK():
    try:
        Loadbk.objects.filter(dt_run__lt=system_date).delete()
        return
    except:
        print("Data not deleted : Loadbk")  
        return  

def insertLOADBK():
    try:
        cursor = connection.cursor()
        cursor.execute('''insert into public."LOADBK"("SH_SEC","LC_NO", "PART_NO", "QTY", "NO_MC","PTDES", "M5_CD","LC_DES","PA", "AT_HRS", "LOT","DT_RUN","CUR_TIME") (select x."SHOP_SEC", x."LC_NO", x."PART_NO",y."QTY", mp1.no_mc, (select "DES" from public."PART" where x."PART_NO"= "PART"."PARTNO") ptdes, x."M5_CD", mp1.lc_des,(case when (coalesce(trim(x."M5_CD"),'9')='1') then (sum(x."PA_HRS")/5) else sum(x."PA_HRS") end) pa,sum(x."AT_HRS") at_hrs,x."LOT",CURRENT_DATE, %s from public."QTYSUM_TEMP" y,(select "SHOP_SEC", "LCNO",(select "DES" from public."LC1" where public."LC1"."SHOP_SEC"= public."MP"."SHOP_SEC" and public."LC1"."LCNO"= public."MP"."LCNO" and coalesce(trim(public."LC1"."DEL_FL"),'#')<>'Y' limit 1) lc_des, (count(1)/2) no_mc from public."MP" group by "SHOP_SEC", "LCNO") mp1 FULL OUTER JOIN public."OPRN" x on mp1."SHOP_SEC"=x."SHOP_SEC" and mp1."LCNO"=x."LC_NO" where trim(x."PART_NO")= trim(y."PARTNO") and coalesce(trim(x."NCP_JBS"),'#') !='1' and y."CUR_TIME"=%s group by x."PART_NO",y."QTY",x."SHOP_SEC", x."LC_NO",x."M5_CD", x."LOT",mp1.no_mc,lc_des,CURRENT_DATE);''',[g_curTime,g_curTime])
        return
    except:
        print("Insertion not successful : loadbk")
        return

def UpdateLOADBK():
    try:
        cursor = connection.cursor()
        cursor.execute('update  "LOADBK" set "LOCO_LOAD_HRS"= round(("PA"+"AT_HRS"/"LOT"*"QTY"),2), "CAP_MNTH_HRS"=  "NO_MC"*480')
        cursor.execute('update "LOADBK" set "PROD_CAP_MNTH"= round("CAP_MNTH_HRS"/ "LOCO_LOAD_HRS",0) where "LOCO_LOAD_HRS">0')
        return
    except:
        print("Updation not successful : Loadbk")
        return
       
def UpdateQtySum_temp1(partno,ptc,qty,shop_ut,l_fr,l_to,parent):
    try:
        QtysumTemp1.objects.filter(partno=parent,cur_time=g_curTime).update(rm_part=str(partno),rm_ptc=str(ptc),rm_qty=qty,
        rm_ut=str(shop_ut),rm_lf=str(l_fr),rm_lt=str(l_to)) 
        return  
    except:
        print("Updation not successful : QtysumTemp1")
        return 

def secJobEpcDesc(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        epc=request.GET.get('epc')
        obj=list(Code.objects.filter(code=epc,cd_type='11').values('alpha_1').distinct())
        obj1=Batch.objects.filter(~Q(bo_no__startswith='13'),ep_type=epc,batch_type='O').values('ep_type','bo_no','loco_fr','loco_to','batch_qty','part_no','rel_date').distinct()
        obj2=Batch.objects.filter(bo_no__startswith='13',ep_type=epc,batch_type='O',status='R').values('ep_type','bo_no','loco_fr','loco_to','batch_qty','part_no','rel_date').distinct()
        obj3=obj1.union(obj2)
        obj4=list(obj3)
        l.append(obj)
        l.append(obj4)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)
def secJobBackClick(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = empmast.objects.none()
    if "Superuser" in rolelist:    
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'subnav':subnav,
        }  
    return render(request,'homeadmin.html',context)

def secJobPartNoDesc(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        part_no=request.GET.get('part_no')
        obj=list(Part.objects.filter(partno=part_no).values('des').distinct())
        l.append(obj)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)

def secJobViewCode(request):
    if request.method == "GET" and request.is_ajax():  
        part_no=request.GET.get('part_no')
        epc=request.GET.get('epc')
        loco_from=request.GET.get('loco_from')
        loco_to=request.GET.get('loco_to')
        p=explodem(part_no,epc,loco_from,loco_to)
        return JsonResponse(p,safe=False) 
    return JsonResponse({"success:False"},status=400) 
