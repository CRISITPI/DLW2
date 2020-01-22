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
import requests
from datetime import datetime,date

# Create your views here.
#
#
#
#
#
#
#

from django.db.models import Q
from .utils import render_to_pdf 
from django.db.models.functions import Substr
from django.db.models import Subquery

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
        pdf = render_to_pdf('m14genpdf2.html', data)
    else:
        pdf = render_to_pdf('m14genpdf1.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
# END PRINT


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
    return render(request,'viewsPermission.html',context)





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
    return render(request,'viewsPermissiondel.html',context)





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
    return render(request,'viewsPermissionUpdate.html',context)





def login_request(request):
    if request.method=='POST':
        u_id = request.POST.get('user_id')
        pwd=request.POST.get('password')
        user = authenticate(username=u_id, password=pwd)
        if user is not None:
            login(request, user)
            currentuser=empmast.objects.filter(empno=user).first()
            rolelist=currentuser.role.split(", ")
            if "Superuser" in rolelist:
                return redirect('homeadmin')
            else:
                return redirect('homeuser')
        else:
            messages.error(request,"Invalid username or password")
    form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})







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
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist).order_by('childmenu')
    context={
        'nav':nav,
        'subnav':subnav,
        'usermaster':usermaster,
        'ip':get_client_ip(request),
    }
    return render(request,'homeadmin.html',context)




@login_required
@role_required(urlpass='/homeuser/')
def homeuser(request):
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
        'usermaster':usermaster,
        'ip':get_client_ip(request),
        'subnav':subnav
    }
    return render(request,'homeuser.html',context)










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
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    emp=empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL') | empmast.objects.filter(role__isnull=True,dept_desc='CRIS_MU')
    availableroles=roles.objects.all().values('parent').distinct()
    if request.method == "POST":
        emp_id=request.POST.get('emp_id')
        email=request.POST.get('email')
        role=request.POST.get('role')
        sublevelrole=request.POST.getlist('sublevel')
        sublevelrolelist= ", ".join(sublevelrole)
        password="dlw@123"
        if "Superuser" in sublevelrole and emp_id and role and sublevelrole:
            employee=empmast.objects.filter(empno=emp_id).first()
            employee.role=sublevelrolelist
            employee.parent=role
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
        'nav':nav,
        'usermaster':usermaster,
        'emp':emp,
        'ip':get_client_ip(request),
        'roles':availableroles,
        'subnav':subnav,
    }

    return render(request,'createuser.html',context)





    




@login_required
@role_required(urlpass='/update_permission/')
def update_permission(request):
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
    availableroles=roles.objects.all().values('parent').distinct() 
    if request.method == "POST":
        updateuser=request.POST.get('emp_id')
        sublevelrole=request.POST.getlist('sublevel')
        role=request.POST.get('role')
        sublevelrolelist= ", ".join(sublevelrole)
        if updateuser and sublevelrole:
            usermasterupdate=empmast.objects.filter(empno=updateuser).first()
            usermasterupdate.role=sublevelrolelist
            usermasterupdate.parent=role
            usermasterupdate.save()
            messages.success(request, 'Successfully Updated!')
            return redirect('update_permission')
        else:
            messages.error(request,"Error!")
            return redirect('update_permission')

    context={
        'users':users,
        'nav':nav,
        'usermaster':usermaster,
        'ip':get_client_ip(request),
        'roles':availableroles,
        'subnav':subnav,
    }
    return render(request,'update_permission.html',context)



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
    return render(request,'update_permission_incharge.html',context)



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
    return render(request,'update_emp_shift.html',context)






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
    return render(request,'update_emp_shift_admin.html',context)

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
    return render(request,'delete_user.html',context)


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
    return render(request,'forget_password.html',context)

def forget_path(request):
    if request.method == "POST":
        option=request.POST.get('forget')
        if option=="Email":
            return redirect('password_reset')
        else:
            return redirect('forget_password_path')
    return render(request,'forget_password_path.html',{})



class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self,request):
        obj= testc.objects.all()
        serializer=testSerializer(obj,many=True)
        return Response(serializer.data)


@login_required
@role_required(urlpass='/m2view/')
def m2view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            brn_no = request.POST.get('br_no')
            assembly_no = request.POST.get('assm_no')
            doc_no = request.POST.get('doc_no')
            kkk=Oprn.objects.all()
            obj1 = Part.objects.filter(partno=part_no).values('des', 'drgno').distinct()
            obj2 = Part.objects.filter(partno=assembly_no).values('des').distinct()
            # print(obj2)
            obj3 = Batch.objects.filter(bo_no=wo_no,brn_no=brn_no,part_no=assembly_no).values('batch_type')
            check_obj=Oprn.objects.all().filter(shop_sec=shop_sec)
            # obgg = Oprn.objects.filter(part_no=part_no, shop_sec=shop_sec).values('shop_sec').distinct()
            # obggg = Oprn.objects.filter(part_no=part_no).values('shop_sec').distinct()
            # obgggg = obggg.union(obgg)
            # if obgg.count() != 0:
            obj = Oprn.objects.filter(part_no=part_no).values('opn', 'shop_sec', 'lc_no', 'des','pa','at','lot','mat_rej','qtr_accep', 'qty_prod','work_rej').order_by('opn')
            date = M2Doc.objects.filter(m2sln=doc_no).values('m2prtdt','qty').distinct()
            leng = obj.count()
            datel= date.count()


            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'len': leng,
                        'date': date,
                        'datel': datel,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'brn_no': brn_no,
                        'assembly_no': assembly_no,
                        'doc_no': doc_no,
                        'subnav':subnav
                  }
            elif(len(rolelist)==1):
                  for i in range(0,len(rolelist)):
                        # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
                        # wo_nop =wo_nop | req

                        w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                        req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                        wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'len': leng,
                        'date': date,
                        'datel': datel,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'brn_no': brn_no,
                        'assembly_no': assembly_no,
                        'doc_no': doc_no,
                        'subnav':subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'len': leng,
                        'date': date,
                        'datel': datel,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'brn_no': brn_no,
                        'assembly_no': assembly_no,
                        'doc_no': doc_no,
                        'subnav':subnav
                  }
            # else:
            #     messages.error(request,'Corresponding Data For Shop-Section and PartNumber Not Found!, Select other values to check')
        if submitvalue=='Save':
            leng=request.POST.get('len')
            shopsec= request.POST.get('shopsec')
            partno= request.POST.get('partno')
            for i in range(1, int(leng)+1):
                qtypr=request.POST.get('qtypr'+str(i))
                qtyac = request.POST.get('qtyac'+str(i))
                wrrej = request.POST.get('wrrej'+str(i))
                matrej = request.POST.get('matrej'+str(i))
                opn=request.POST.get('opn'+str(i))
                print(shopsec)

                Oprn.objects.filter(shop_sec=shopsec, part_no=partno, opn=opn).update(qty_prod=qtypr, qtr_accep=qtyac, work_rej=wrrej, mat_rej=matrej)
                wo_no=M2Doc.objects.all().values('batch_no').distinct()
            messages.success(request, 'Successfully Updated!, Select new values to update')
    return render(request, "m2view.html", context)


def m2getwono(request):
    if request.method == "GET" and request.is_ajax():
        from.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2=M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m2getbr(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        br_no = list(M2Doc.objects.filter(batch_no =wo_no).values('brn_no').distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m2getassly(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        w2=M2Doc.objects.filter(batch_no=wo_no).values('assly_no').distinct()
        w1=Oprn.objects.filter(part_no__in=w2).values('shop_sec', 'part_no').distinct()
        print(w1)
        w3=w1.filter(shop_sec=shop_sec).values('part_no').distinct()
        w4=M2Doc.objects.filter(batch_no=wo_no, f_shopsec=shop_sec, brn_no=br_no).values('assly_no').distinct()
        w5=w3.union(w4)
        w6=w5.distinct()
        print(w6)
        assm_no = list(w6)
        return JsonResponse(assm_no, safe=False)
    return JsonResponse({"success":False}, status=400)



def m2getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        w2 = M2Doc.objects.filter(batch_no=wo_no).values('part_no').distinct()
        w1 = Oprn.objects.filter(part_no__in=w2).all().distinct()
        w3= w1.filter(shop_sec=shop_sec).values('part_no').distinct()
        w4 = M2Doc.objects.filter(batch_no=wo_no, f_shopsec=shop_sec, brn_no=br_no,assly_no=assembly_no).values('part_no').distinct()
        w5=w3.union(w4)
        w6=w5.distinct()
        part_no = list(w6)
        return JsonResponse(part_no, safe=False)
    return JsonResponse({"success":False}, status=400)



def m2getdoc_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        # br_no = request.GET.get('brn_no')
        # shop_sec = request.GET.get('shop_sec')
        # assembly_no = request.GET.get('assm_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M2Doc.objects.filter(batch_no=wo_no,part_no=part_no).values('m2sln').distinct())

        return JsonResponse(doc_no, safe=False)
    return JsonResponse({"success": False}, status=400)







@login_required
@role_required(urlpass='/m4view/')
def m4view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = M14M4.objects.filter(assly_no__in=w1).values('bo_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            brn_no = request.POST.get('br_no')
            assembly_no = request.POST.get('assm_no')
            doc_no = request.POST.get('doc_no')
            kkk=Oprn.objects.all()
            obj1 = Part.objects.filter(partno=part_no).values('des', 'drgno').distinct()
            obj2 = Part.objects.filter(partno=assembly_no).values('des').distinct()
            obj3 = Batch.objects.filter(bo_no=wo_no,brn_no=brn_no,part_no=assembly_no).values('batch_type')
            check_obj=Oprn.objects.all().filter(shop_sec=shop_sec)
            obj = M14M4.objects.filter(doc_no=doc_no,assly_no=assembly_no,brn_no=brn_no,part_no=part_no).values('received_mat', 'issued_qty', 'received_qty', 'laser_pst', 'line', 'closing_bal', 'remarks', 'posted_date', 'wardkp_date', 'shopsup_date', 'posted1_date')
            print("hh")
            print(obj)
            if len(obj) == 0:
                obj = range(0,1)
            date = M14M4.objects.filter(doc_no=doc_no,assly_no=assembly_no,brn_no=brn_no,part_no=part_no).values('prtdt','qty').distinct()
            leng = obj.count()
            datel = date.count()
            print(datel)
            # print(obj1)
            # print(obj2.count())
            # print(obj1.count())
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context = {
                    'roles':tmp,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
                    # wo_nop =wo_nop | req

                    w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    req = M14M4.objects.filter(assly_no__in=w1).values('bo_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'wo_nop':wo_nop,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'usermaster':usermaster,
                    'lenm' :len(rolelist),
                    'nav': nav,
                    'ip': get_client_ip(request),
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }
            elif(len(rolelist)>1):
                context = {
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }

        # if submitvalue=='Print':
        #     ppp=1
        #     context={
        #         'ppp': ppp
        #     }

        if submitvalue=='Save':
            doc_no= request.POST.get('doc_no1')
            part_no= request.POST.get('part_no1')
            wo_no=request.POST.get('wo_no1')
            brn_no=request.POST.get('brn_no1')
            # print("hh")
            print(doc_no)
            # print(part_no)
            # print(wo_no)
            # print(brn_no)
            # print("hhhh")
            received_mat = request.POST.get('received_mat')
            issued_qty = request.POST.get('issued_qty')
            received_qty = request.POST.get('received_qty')
            laser_pst = request.POST.get('laser_pst')
            line= request.POST.get('line')
            closing_bal = request.POST.get('closing_bal')
            remarks = request.POST.get('remarks')
            posted_date = request.POST.get('posted_date')
            wardkp_date = request.POST.get('wardkp_date')
            shopsup_date = request.POST.get('shopsup_date')

            # print(laser_pst)
            # temp_date = time.strptime(laser_pst, "%Y-%m-%d")
            # print(temp_date)

            posted1_date = request.POST.get('posted1_date')
            M14M4.objects.filter(part_no=part_no,doc_no=doc_no,brn_no=brn_no,bo_no=wo_no).update(received_mat=str(received_mat), issued_qty=int(issued_qty), received_qty=int(received_qty), laser_pst=str(laser_pst), line=str(line), closing_bal=int(closing_bal), remarks=str(remarks), posted_date=str(posted_date), wardkp_date=str(wardkp_date), shopsup_date=str(shopsup_date), posted1_date=str(posted1_date))
            wo_no=M14M4.objects.all().values('bo_no').distinct()
            messages.success(request, 'Successfully Updated!, Select new values to update')
    return render(request, "m4view.html", context)




def m4getwono(request):
    if request.method == "GET" and request.is_ajax():
        from.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1 = Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2 = M14M4.objects.filter(assly_no__in=w1).values('bo_no').exclude(bo_no__isnull=True).distinct()
        # print(w2)
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m4getbr(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = list(M14M4.objects.filter(bo_no =wo_no).values('brn_no').exclude(brn_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m4getassly(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assm_no = list(M14M4.objects.filter(bo_no =wo_no,brn_no=br_no).values('assly_no').exclude(assly_no__isnull=True).distinct())
        return JsonResponse(assm_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m4getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assembly_no = request.GET.get('assm_no')
        part_no = list(M14M4.objects.filter(brn_no=br_no,assly_no=assembly_no,bo_no=wo_no).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m4getdoc_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M14M4.objects.filter(bo_no =wo_no,brn_no=br_no,assly_no=assembly_no,part_no=part_no).values('doc_no').exclude(doc_no__isnull=True).distinct())
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)








@login_required
@role_required(urlpass='/m14view/')
def m14view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = M14M4.objects.filter(assly_no__in=w1).values('bo_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            brn_no = request.POST.get('br_no')
            assembly_no = request.POST.get('assm_no')
            doc_no = request.POST.get('doc_no')
            kkk=Oprn.objects.all()
            obj1 = Part.objects.filter(partno=part_no).values('des', 'drgno').distinct()
            obj2 = Part.objects.filter(partno=assembly_no).values('des').distinct()
            obj3 = Batch.objects.filter(bo_no=wo_no,brn_no=brn_no,part_no=assembly_no).values('batch_type')
            check_obj=Oprn.objects.all().filter(shop_sec=shop_sec)
            obj = M14M4.objects.filter(doc_no=doc_no,brn_no=brn_no,assly_no=assembly_no,bo_no=wo_no,part_no=part_no).values('received_mat14', 'issued_qty14', 'received_qty14', 'laser_pst14', 'line14', 'closing_bal14', 'remarks14', 'posted_date14', 'wardkp_date14', 'shopsup_date14', 'posted1_date14')
            print(doc_no)
            if len(obj) == 0:
                obj = range(0, 1)
            print("HH")
            # print(assembly_no)
            date = M14M4.objects.filter(doc_no=doc_no,brn_no=brn_no,assly_no=assembly_no,bo_no=wo_no).values('prtdt','qty').distinct()
            leng = obj.count()
            datel= date.count()
            print(obj)
            print(date)
            # print(obj1)
            # print(obj2.count())
            # print(obj1.count())
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context = {
                    'roles':tmp,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
                    # wo_nop =wo_nop | req

                    w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    req = M14M4.objects.filter(assly_no__in=w1).values('bo_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'wo_nop':wo_nop,
                    'roles' :rolelist,
                    'usermaster':usermaster,
                    'lenm' :len(rolelist),
                    'nav': nav,
                    'subnav':subnav,
                    'ip': get_client_ip(request),
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }
            elif(len(rolelist)>1):
                context = {
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }
        if submitvalue=='Save':
            doc_no= request.POST.get('doc_no1')
            part_no= request.POST.get('part_no1')
            wo_no=request.POST.get('wo_no1')
            brn_no=request.POST.get('brn_no1')
            # print("hh")
            print(doc_no)
            # print(part_no)
            # print(wo_no)
            # print(brn_no)
            # print("hhhh")
            received_mat = request.POST.get('received_mat')
            issued_qty = request.POST.get('issued_qty')
            received_qty = request.POST.get('received_qty')
            laser_pst = request.POST.get('laser_pst')
            line= request.POST.get('line')
            closing_bal = request.POST.get('closing_bal')
            remarks = request.POST.get('remarks')
            posted_date = request.POST.get('posted_date')
            wardkp_date = request.POST.get('wardkp_date')
            shopsup_date = request.POST.get('shopsup_date')

            # print(laser_pst)
            # temp_date = time.strptime(laser_pst, "%Y-%m-%d")
            # print(temp_date)

            posted1_date = request.POST.get('posted1_date')
            M14M4.objects.filter(part_no=part_no,doc_no=doc_no,brn_no=brn_no,bo_no=wo_no).update(received_mat14=str(received_mat), issued_qty14=int(issued_qty), received_qty14=int(received_qty), laser_pst14=str(laser_pst), line14=str(line), closing_bal14=int(closing_bal), remarks14=str(remarks), posted_date14=str(posted_date), wardkp_date14=str(wardkp_date), shopsup_date14=str(shopsup_date), posted1_date14=str(posted1_date))
            wo_no=M14M4.objects.all().values('bo_no').distinct()
            messages.success(request, 'Successfully Updated!, Select new values to update')
    return render(request, "m14view.html", context)




def m14getwono(request):
    if request.method == "GET" and request.is_ajax():
        from.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1 = Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2 = M14M4.objects.filter(assly_no__in=w1).values('bo_no').exclude(bo_no__isnull=True).distinct()
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14getbr(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = list(M14M4.objects.filter(bo_no =wo_no).values('brn_no').exclude(brn_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m14getassly(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assm_no = list(M14M4.objects.filter(bo_no =wo_no,brn_no=br_no).values('assly_no').exclude(assly_no__isnull=True).distinct())
        return JsonResponse(assm_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m14getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assembly_no = request.GET.get('assm_no')
        part_no = list(M14M4.objects.filter(brn_no=br_no,assly_no=assembly_no,bo_no=wo_no).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m14getdoc_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M14M4.objects.filter(bo_no =wo_no,brn_no=br_no,assly_no=assembly_no,part_no=part_no).values('doc_no').exclude(doc_no__isnull=True).distinct())
        print(doc_no)
        print("h")
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)










@login_required
@role_required(urlpass='/aprodplan/')
def bprodplan(request):
    from .models import annual_production,jpo,namedgn,loconame,materialname
    from datetime import date
    existlen=0
    context={}
    dictemper={}
    yearlist=[]
    indrwspan=0
    years={}
    flagg=1
    # dictemper={}
    diiict={}
    dct={}
    tod = date.today()
    ft=int(tod.strftime("%Y"))
    ft2=ft+1
    ctp=str(ft)+'-'+str(ft2)
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
    print("revex",revex)
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
              'nav':nav,
              'revex':revex,
              'usermaster':usermaster,
              'ip':get_client_ip(request),
              'ruser':ruser,'ref':ref,
              'yup':True,
              'Manpower':"Manpower",
              'Account':"Account",
              'Add':"Add",
              'Role':rolelist[0],
              'cyear':ctp,
              'numfy':'-','dgp':'-','flag':flag,'existlen':0,
              'subnav':subnav,
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
        # num=request.POST.get('numfy')
        print(bval,save)
        dgp=request.POST.get('dgp')
        if dgp is None:
            cnt=0
        else:
            cnt=int(dgp)
        print(dgp)
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
                print(indo)
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
            print(diff)
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
            print("existlen",existlen)
            context={
                        'user':cuser,
                        'ruser':ruser,
                        'yup':True,
                        'Manpower':"Manpower",
                        'Account':"Account",
                        'Add':"Add",
                        'nav':nav,
                        'subnav':subnav,
                        'Role':rolelist[0],
                        'value': range(5),
                        'typec':typec,
                        'typed':typenew,'numfy':numfy,'dgp':dgp,
                        'cyear':ctp,'ref':ref,'mjalt':mjalt,'remk':remk,'headalt':headalt,
                        'val':range(3),'iammain':iammain,
                        'revex':revex,
                        'usermaster':usermaster,'cnt':range(cnt),
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
            print("new dgp",dgp)
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
            # print("new names",nmdgn)
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
            print("altr",mjalt)
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
            print("num is",num)
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
                # print("num of loco = "+num_loco)
                nf=request.POST.get('num_of_numfy')
                num_fy=0
                if(nf is not None):
                    num_fy=nfy

                # print("num_fy = "+num_fy)


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
                    # deledit=annual_production.objects.filter(customer=typ,loco_type=request.POST.get("editloco"+str(lo+1)),revisionid=rev).delete()
                    # print(" For Loco: "+request.POST.get("editloconame"+str(lo+1)))

                    for nf in range(1,int(num_fy)+1):
                        if(request.POST.get("edit"+str(lo)+str(1))!=None):
                            if len(request.POST.get("edit"+str(lo)+str(1))) and (request.POST.get("edit"+str(lo)+str(1))) is not None:
                                # print("target_quantity for "+yearr[nf-1]+" = "+request.POST.get("edit"+str(lo)+str(nf)))
                                # print("buffer_quantity for "+yearr[nf-1]+" = "+request.POST.get("editbf"+str(lo)+str(nf)))
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
                print(indx)
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
                # print("num of loco = "+num_loco)
                # num_fy=request.POST.get('num_of_numfy')
                num_fy=request.POST.get('numfy')
                print("num_fy",num_fy)
                # print("num_fy = "+num_fy)


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
                    # print(" For Loco: "+request.POST.get("editloco"+str(lo+1)))
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
                # print(subobj)

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
                    print(qtname)
                    qtbuffname=qtb+str(k)+str(j)
                    print(qtbuffname)
                    # print(len(request.POST.get(loconame+str(k))),request.POST.get(loconame+str(k)))
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
    return render(request,'newaprodplan.html',context)








@login_required
@role_required(urlpass='/jpo/')
def jpo(request):
    from .models import annual_production,jpo,namedgn
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    dictt=jpo.objects.all().aggregate(Max('revisionid'))
    revex=dictt['revisionid__max']
    if revex is None:
        revex=0
    revcnt=revex+1    
    datadic={}
    context={
        'nav':nav,
        'subnav':subnav,
        'usermaster':usermaster,
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
    finalvalue=0
    formno=0
    number=0
    cdgp=0

    if request.method == "POST":
        
        # yr=request.POST.get('financial-year')
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
        # if len(jpoobj):
        #     formno=jpoobj[0].formno
        #     number=jpoobj[0].number
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
                    print(years)

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
                        # print(dictemper[str(j)]['dict']['0']['yrtq'])
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
                                print(tr)
                               
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
                                # print(tr)
                               
                                s=''.join(chr(artl[d]) for d in range(len(tr)) )
                                tot=tot+int(s)
                                # tot=tot+int(nrcdictemper[str(j)]['dict'][str(kill)]['yrtq'])
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
                                # print(tr)
                               
                                s=''.join(chr(artl[d]) for d in range(len(tr)) )
                                tot=tot+int(s)
                                # tot=tot+int(expdictemper[str(j)]['dict'][str(kill)]['yrtq'])
                            else:
                                tot=int(total[str(kill)]['totq'])
                                
                        tottq.append(tot)
                        tot=0
                        tottemper = {str(kill):{"totq":tottq[kill],
                                      
                                        }}

                        total.update(copy.deepcopy(tottemper))

                    tottq=[]
                    # print(total)


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
            # print("cspan=="+cspan)
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
            'nav':nav,'rev':rev,'heading':heading,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'total':total,'subnav':subnav,
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
                    # print(years)

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
                       
                        # rspitmdictemper.update(copy.deepcopy(temper))
                        rspdictemper.update(copy.deepcopy(temper))
                # print("finaldict",rspdictemper)


                if rspflag or rspitmflag :
                    data=1
            # totalcnt=len(rspitmdictemper)+len(rspdictemper)
            # print("in rsp:",totalcnt)

            colsapn=int(cspan)+2

            context={"data":data,"data6":rspm,"data7":rspitm,"jpo":0,
              "years":years,"rspdictemper":rspdictemper,
            #   "rspitmdictemper":rspitmdictemper,
            "rspflag":rspflag,"rspitmflag":rspitmflag,
            "colsapn":colsapn,"bufcspan":int(cspan),
            "rsprwspan":rsprwspan,"rspitmrwspan":rspitmrwspan,'jpoo':jpoo,'rev':rev,
            "year1":yr,"year2":yr2,"year3":yr3,"year4":yr4,
            "pre5":rm,"n5":r1+1,
            "pre6":ri,"n6":r2+1,
            'nav':nav,'rev':rev,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'dt':dt,'subject':sub,
            'total':total,'subnav':subnav,
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
                print(mainnumfy,rspnumfy)
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


                print("error",numfy)
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
                        print(dictemper[str(j)]['dict']['0']['yrtq'])
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
                                # print(tr)
                               
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
                                # print(tr)
                               
                                s=''.join(chr(artl[d]) for d in range(len(tr)) )
                                tot=tot+int(s)
                                # tot=tot+int(nrcdictemper[str(j)]['dict'][str(kill)]['yrtq'])
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
                                # print(tr)
                               
                                s=''.join(chr(artl[d]) for d in range(len(tr)) )
                                tot=tot+int(s)
                                # tot=tot+int(expdictemper[str(j)]['dict'][str(kill)]['yrtq'])
                            else:
                                tot=int(total[str(kill)]['totq'])
                        tottq.append(tot)
                        tot=0
                        tottemper = {str(kill):{"totq":tottq[kill],
                                      
                                        }}

                        total.update(copy.deepcopy(tottemper))

                    tottq=[]
                    # print(total)
                
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
                    print("rsp years",years)





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
                        # print(rspitmdictemper)


                


            if flag or nrcflag or expflag or zrflag or zroverflag or rspflag or rspitmflag or nrcdgflag or zrasflag:
                data=1

            print(Finalize,finalize)

            maijp=jpo.objects.filter(financial_year=yr,revisionid=rev,jpo='main')
            if len(maijp)!=0:
                finalvalue=maijp[0].finalval
                print(finalvalue)



            lidict={0:'loty',1:'yr1',2:'yr3',3:'yr4'}
            # print("cspan=="+cspan)
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
                # print("main remark",remk1)
            if len(jpoc):
                remk2=jpoc[0].remark
                # print("rsp remark",remk1)
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
            'nav':nav,'dt':dt,'subject':sub,'rev':rev,
            'usermaster':usermaster,'ip':get_client_ip(request),
            'total':total,'subnav':subnav,
            'namelist':namelist,'desiglist':desiglist,'cdgp':range(cdgp),
            'number':number,'formno':formno,'subject':sub,'dt':dt,'heading':heading,
            'reflist':reflist,'altrlist':altrlist,'remklist':remklist,'spclremlist':spclremlist,
            'nrmllist':nrmllist,'revcnt':range(revcnt),
            }

        else:
            context={'nav':nav,'dt':dt,'subject':sub,'revcnt':range(revcnt),
            # 'refr':ref,
        'usermaster':usermaster,'subnav':subnav,
        'ip':get_client_ip(request),
        'revision':rev,'namelist':namelist,'desiglist':desiglist,'cdgp':range(cdgp),}

 
    return render(request,"jpoc.html",context)


def loco(request):
    from .models import loconame
    lcname=[]
    objy=loconame.objects.all()
    for o in objy:
        if (o.loconame):
            lcname.append(o.loconame)
    return lcname

def material(request):
    from .models import materialname
    lcname=[]
    objy=materialname.objects.all()
    for o in objy:
        if (o.matrname):
            lcname.append(o.matrname)
    # print(lcname)
    return lcname

def findthis(request,temp):
    templist=[]
    asci=temp
    ascil=[ord(cc) for cc in asci]
    # print(ascil,len(ascil))
    thr=[]
    for i in range(len(ascil)):
        if ascil[i]==13:
            thr.append(i)
    # print("enter list:",thr)
    k=0
    for i in range(len(thr)):
        s=''.join(chr(ascil[d]) for d in range(k,thr[i]))
        # print(len(s),s)
        lis=[13,10]
        if len(s)>0 and s!=''.join(chr(i) for i in lis):
            # print(s)
            k=thr[i]+2
            templist.append(s)
    s=''.join(chr(ascil[d]) for d in range(k,len(ascil)))
    # print(len(s),s)
    if len(s)>0:
        # print(s)
        templist.append(s)
    return templist



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
    from .models import jpo,annual_production,dpo
    if request.method == "GET" and request.is_ajax():
        loco=request.GET.get('loconame')
        b2=request.GET.get('barl2')
        
        total=0
        try:
            obj=dpo.objects.filter(loco_type=loco,order_no=b2)
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
        # print(lcname)
        flag=0
        try:
            emp=annual_production.objects.filter(loco_type=lcname).exists()
            if emp is True:
                flag=1
        except:
            return JsonResponse({"success":False}, status=400)
        print("flag",flag)
        jpo_info={
            "flag":flag,
        }
        return JsonResponse({"jpo_info":jpo_info}, status=200)

    return JsonResponse({"success":False}, status=400)


def test(request):
    if request.method == "POST":
        obj = testing_purpose.objects.create()
        obj.first = request.POST.get('firstinp')
        obj.second = request.POST.get('secondinp')
        obj.save()
    return render(request,'test.html',{})






@login_required
def dpo(request):
    from .models import annual_production
    # locodpo,barrelfirst

    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)

     

    tod = date.today()
    ft=int(tod.strftime("%Y"))
    ft2=ft+1
    ctp=str(ft)+'-'+str(ft2)

    locos=[]

    obj=annual_production.objects.filter(financial_year=ctp)

    for i in range(0,len(obj)):
        locos.append(obj[i].loco_type)
    


    context={
        'nav':nav,
        'ip':get_client_ip(request),
        'Role':rolelist[0],
        'cyear':ctp,
        'add':0,
        'locolist':locos,
        'subnav':subnav,
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
            # obj=dpo.objects.filter(loco_type=loco,order_no=b2)
            # if(len(obj))
            tc=request.POST.get('tc')
            num=(int(tc)-1) // 5
            mod=(int(tc)-1) % 5
            if(num>9):
                flag=1
            if loco=='WAP10' or loco=='WAP11' or loco=='WAP-7 ELECTRIC LOCO' or loco=='WAP-9 ELECTRIC LOCO':
                b1=33
            bno=str(b1)+'/'+str(b2)+'/'


            context={
            'nav':nav,
            'ip':get_client_ip(request),
            'Role':rolelist[0],
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
            'subnav':subnav,

        } 

        if submit=='Save':
            context={
            'nav':nav,
            'ip':get_client_ip(request),
            'Role':rolelist[0],
            'locolist':locos,
            'cyear':ctp,
            'subnav':subnav,

            

        } 



    return render(request, 'dpo.html', context)









@login_required
@role_required(urlpass='/dpoinput/')
def dpoinput(request):
    from datetime import date
    
    from .models import annual_production,barrelfirst,dpo,dpoloco,jpo
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    # cuser=request.user
    # usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
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

    # print("locolist:",locos)
    context={
        'nav':nav,
        'subnav':subnav,
        'ip':get_client_ip(request),
        'Role':rolelist[0],
        'cyear':ctp,
        'add':0,
        'locolist':locos,
        'locoindb':locoindb,
        'annualloco':annulloco,
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
            
            obj=dpo.objects.filter(locotype=loco,orderno=b2,procedureno=0)
            if (obj is not None) and len(obj):
                print(obj)
                subject=obj[0].subject
                reference=obj[0].reference
                copyto=obj[0].copyto
                summary=obj[0].summary
                dat=obj[0].date
                print(subject,reference,copyto,summary,dat)
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
                    print(dictemper)
                    print("j=",dataext)


            print(locoindb,"locoindb")  
            print("annualloco",annulloco)
            context={
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'Role':rolelist[0],
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
            print("dataext",dataext,"totbaches",totbaches)
            # totbaches=int(tbaches)-int(dataext)
            
            args = jpo.objects.filter(financial_year=ctp,jpo='main') 
            ar=args.aggregate(Max('revisionid'))
            revisionidmax=ar['revisionid__max']
            annualobj=annual_production.objects.filter(financial_year=ctp,revisionid=revisionidmax)
            for l in range(len(annualobj)):
                annulloco.append(annualobj[l].loco_type)
                
                # '<td><input type="text" name="'+idname+'" placeholder="loconame" id="'+idname+'" onkeyup="findcm(this)" /></td>'+
            
            dpopb=dpo.objects.filter(procedureno=0,locotype=locot,orderno=ordno)
            if dpopb is not None and len(dpopb):
                print("already exists")
                obj=dpo.objects.filter(procedureno=0,locotype=locot,orderno=ordno).update(subject=sub,reference=refn,date=datee,copyto=copyto,summary=summary)
                
            else:
                obj=dpo.objects.create()
                obj.subject=sub
                obj.reference=refn
                obj.date=datee
                obj.copyto=copyto
                obj.summary=summary
                obj.orderno=ordno
                obj.locotype=locot
                obj.save()
               
            print("locot",locot)
            print("ordno",ordno)
            temp1="loconame"
            idname=[]
            lcname=[]
            ttlcnt=request.POST.get('cm2')
            # for i in range(1,int(ttlcnt)+1):
            #     temp1=temp1+str(i)
            #     idname.append(temp1)
            #     temp1="loconame"
            # for key in request.POST:
            #     for temp1 in idname:
            #         if key==temp1:
            #             lcname.append(request.POST[key])
            
            print("lcname",lcname)
            
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
               
               
            
            print("annualloco",annulloco)
            
            context={
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'Role':rolelist[0],
            'cyear':ctp,
            'locolist':locos,
            'annualloco':annulloco,
            
        } 

    return render(request, 'dpof.html', context)










@login_required
@role_required(urlpass='/dporeport/')
def dporeport(request):
    from .models import annual_production,dpo,barrelfirst,dpoloco,jpo
    from django.db.models import Max
    
    # locodpo,barrelfirst
    
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)

     

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
        'nav':nav,
        'ip':get_client_ip(request),
        'Role':rolelist[0],
        'cyear':ctp,
        'add':0,
        'locolist':locos,
        'subnav':subnav,
       
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
        # obj=annual_production.objects.filter(financial_year=ctp)
        # for i in range(0,len(obj)):
        #     locos.append(obj[i].loco_type)
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
                dloco=dpo.objects.filter(procedureno=pord)
                if(len(dloco) and dloco is not None):
                    loco=dloco[0].locotype
                    b2=dloco[0].orderno
                    # print("loco",loco,"b2",b2)

                obj1=barrelfirst.objects.filter(locotype=loco)
                if (obj1 is not None) and len(obj1):
                    b1=obj1[0].code
                
                obj=dpo.objects.filter(locotype=loco,orderno=b2,procedureno=pord)
                if (obj is not None) and len(obj):
                    print(obj)
                    subject=obj[0].subject
                    reference=obj[0].reference
                    copyto=obj[0].copyto
                    summary=obj[0].summary
                    dat=obj[0].date
                    if(obj[0].procedureno=='0'):
                        procedureno=0
                    else:
                        procedureno=1

                    print(subject,reference,copyto,summary,dat)
                    reflist=findthis(request,reference)
                objloco=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=pord).values('loconame').distinct()
                if (objloco is not None) and len(objloco):
                    # for l in range(len(objloco)):
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
                    print("locoindb",locoindb)
                    print("totproduction",totproduction)
                    
                    
                
                    
                    


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
                            print("totproduced",totproduced)
                            dataext=dataext+1

                            dictemper.update(copy.deepcopy(temper))
                        print(dictemper)
                        data=1

            elif((loco!=None and  len(loco)) and (b2!=None and  len(b2))):
                obj1=barrelfirst.objects.filter(locotype=loco)
                b1=obj1[0].code
                
                obj=dpo.objects.filter(locotype=loco,orderno=b2,procedureno=0)
                if (obj is not None) and len(obj):
                    print(obj)
                    subject=obj[0].subject
                    reference=obj[0].reference
                    copyto=obj[0].copyto
                    summary=obj[0].summary
                    dat=obj[0].date
                    if(obj[0].procedureno=='0'):
                        procedureno=0
                    else:
                        procedureno=1

                    print(subject,reference,copyto,summary,dat)
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
                    # print("locoindb",locoindb)
                    # print("totproduction",totproduction)
                    
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
                            # if objlocobt[l].loconame!=locodisp:

                            #     temper = {str(l):{"bno":objlocobt[l].batchordno,
                            #                        "qty":objlocobt[l].qtybatch,
                            #                        "cumino":objlocobt[l].cumino,
                            #                        "loconame":objlocobt[l].loconame,
                            #                        }}
                            #     locodisp=objlocobt[l].loconame
                            # else:

                            #     temper = {str(l):{"bno":objlocobt[l].batchordno,
                            #                        "qty":objlocobt[l].qtybatch,
                            #                        "cumino":objlocobt[l].cumino,
                            #                        "loconame":"-DO-",
                            #                        }}

                            dataext=dataext+1
                            # totproduced=totproduced+int(objlocobt[l].qtybatch)

                            dictemper.update(copy.deepcopy(temper))
                        print(dictemper)
                        data=1


            # if loco is None:
            balance=totproduction-totproduced
            if balance==0:
                balance="NIL"
                
            print("dataext",dataext)
            context={
            'nav':nav,
            # 'subnav':subnav,
            'ip':get_client_ip(request),
            'Role':rolelist[0],
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
            'subnav':subnav,
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
            # print("pnoo")
            if (objlocobt is not None) and len(objlocobt):
                # args = dpo.objects.filter(locotype=loco,orderno=b2) # or whatever arbitrary queryset
                allobj = dpo.objects.all()
                # pno=args.aggregate(Max('procedureno'))
                # print("pno",pno['procedureno__max'])
                maxobj=dpo.objects.aggregate(Max('procedureno'))
                print("Maximum",maxobj['procedureno__max'])
                if allobj is None or len(allobj)==0:
                    pnonum=547
                else:
                    pnonum=int(maxobj['procedureno__max'])+1



            
            obj=dpo.objects.filter(locotype=loco,orderno=b2,procedureno=0)
            if (obj is not None) and len(obj):
                print(obj)
                subject=obj[0].subject
                reference=obj[0].reference
                copyto=obj[0].copyto
                summary=obj[0].summary
                dat=obj[0].date
                if(obj[0].procedureno=='0'):
                    procedureno=0
                else:
                    procedureno=1

                print(subject,reference,copyto,summary,dat)
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
                    # print("locoindb",locoindb)
                    # print("totproduction",totproduction)
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
                    print(dictemper)

                    data=1

                    dpp=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=0).update(procedureno=pnonum)
                    dpp=dpo.objects.filter(locotype=loco,orderno=b2,procedureno=0).update(procedureno=pnonum)

                    dpoop=dpoloco.objects.filter(locotype=loco,orderno=b2,procedureno=pnonum)
                    print(dpoop[0].procedureno,"procedureno")
                    procedure=dpoop[0].procedureno
                


            balance=totproduction-totproduced
            if balance==0:
                balance="NIL"
            print("dataext",dataext)
            context={
                'dpono':1,
            
                'productionyear':ctp,
            'totproduction':totproduction,
            'balance':balance,
            
            'nav':nav,
            # 'subnav':subnav,
            'ip':get_client_ip(request),
            'Role':rolelist[0],
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
            'subnav':subnav,
        }





    return render(request, 'dporeport.html', context)



def getcumino(request):
    from .models import dpo,dpoloco
    print("dpogetcumi")
    l=[]
    b=[]
    if request.method == "GET" and request.is_ajax():
        print("in")
        cmno=0
        bnothr=0
       
        loco=request.GET.get('loco')
        locot=request.GET.get('locot')
        ordno=request.GET.get('ordno')
        try:
            print("hell")
            emp=dpoloco.objects.filter(loconame=loco,locotype=locot,orderno=ordno)
            print("emp",emp)
            
            
        except:
            print("hello")
            return JsonResponse({"success":False}, status=400)
       
        if emp is not None  and len(emp):
            print(emp)
            cmno=412
            for i in range(len(emp)):
                p=emp[i].cumino
                l.append(int(p.split('-')[1]))
                
                bn=emp[i].batchordno
                b.append(bn)
            
            bnothr=str(max(b))
            bnothr=bnothr[5:8]
            print(bnothr,"bnothr")
                
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







@login_required
@role_required(urlpass='/m1view/')
def m1view(request):
    pa_no = empmast.objects.none()
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav
        }
    elif(len(rolelist)==1):
        # print("in else")
        for i in range(0,len(rolelist)):
            req = Oprn.objects.all().filter(shop_sec=rolelist[i]).values('part_no').distinct()
            pa_no =pa_no | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'pa_no':pa_no,
            'roles' :rolelist,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
        }
    if request.method == "POST":
        print("hi")
        submitvalue = request.POST.get('proceed')
        shop_sec = request.POST.get('shop_sec')
        part_no = request.POST.get('part_nop')
        obj  = Oprn.objects.filter(part_no=part_no).values('opn', 'shop_sec', 'lc_no', 'des','pa','at','ncp_jbs',).order_by('shop_sec','opn')
        leng = obj.count()
        epcv=0
        ptcv=0
        rmpart=0
        obj3=Nstr.objects.filter(pp_part=part_no).values('epc','ptc','cp_part').distinct()
        # print(obj3[0])
        if len(obj3):
            epcv=obj3[0]['epc']
            ptcv=obj3[0]['ptc']
            rmpart=obj3[0]['cp_part']
        if submitvalue=='Proceed':
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub': 1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'len': leng,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'obj': obj,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                }
            elif(len(rolelist)==1):
                lent=len(rolelist)
                for i in range(0,len(rolelist)):
                    req = Oprn.objects.all().filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    pa_no =pa_no | req
                context = {
                    'sub': 1,
                    'lenm' :len(rolelist),
                    'pa_no':pa_no,
                    'roles' :rolelist,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'len': leng,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'obj': obj,'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                }
            elif(len(rolelist)>1):
                context = {
                   'sub': 1,
                    'lenm' :len(rolelist),
                    'ip':get_client_ip(request),
                    'roles' :rolelist,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'len': leng,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'obj': obj,'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                }
        if submitvalue=='Generate Report':
            return m1genrept1(request)
    

    return render(request,"m1view.html",context)


def m1getpano(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        print(shop_sec)
        pano = list(Oprn.objects.filter(shop_sec = shop_sec).values('part_no').distinct())
        # print(pano)
        return JsonResponse(pano, safe = False)
    return JsonResponse({"success":False}, status=400)





@login_required
@role_required(urlpass='/m1view/')
def m1genrept1(request):
    from .models import Part,Partalt,Nstr
    pa_no = empmast.objects.none()
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    newob=list(Part.objects.all().values('partno').exclude(partno__isnull=True).distinct())
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
            'newob':newob,
        }
    elif(len(rolelist)==1):
        # print("in else")
        for i in range(0,len(rolelist)):
            req = Oprn.objects.all().filter(shop_sec=rolelist[i]).values('part_no').distinct()
            pa_no =pa_no | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'pa_no':pa_no,
            'roles' :rolelist,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'newob':newob,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'newob':newob,
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        part_no = request.POST.get('part_nop')
        print("prtno",part_no)
        if submitvalue=='Proceed':
            print("in report proceed")
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            epcv=0
            ptcv=0
            rmpart=0
            obj=Part.objects.filter(partno=part_no).values('des','drgno','drg_alt','size_m','spec','weight').distinct()
            print(obj)
            obj3=Nstr.objects.filter(pp_part=part_no).values('epc','ptc','cp_part').distinct()
            # print(obj3[0])
            if len(obj3):
                epcv=obj3[0]['epc']
                ptcv=obj3[0]['ptc']
                rmpart=obj3[0]['cp_part']
            obj2 = Oprn.objects.filter(part_no=part_no).values('opn','shop_sec','lc_no','des','pa','at','ncp_jbs','lot','m5_cd','updt_dt').order_by('shop_sec','opn')
            patotal=0
            attotal=0
            if len(obj2):
                for op in obj2:
                    patotal=patotal+op['pa']
                    attotal=attotal+op['at']
            print(obj)
            print(d1)
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'subnav':subnav,
                    'part_no': part_no,
                    'obj1':obj,
                    'dtl':obj2,
                    'obj3':obj3,
                    'pttl':patotal,
                    'attl':attotal,
                    'dt':d1,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                }
            elif(len(rolelist)==1):
                # print("in else")
                for i in range(0,len(rolelist)):
                    req = Oprn.objects.all().filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    pa_no =pa_no | req
                context = {
                    'lenm' :len(rolelist),
                    'pa_no':pa_no,
                    'roles' :rolelist,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'part_no': part_no,
                    'obj1':obj,
                    'dtl':obj2,
                    'obj3':obj3,
                    'pttl':patotal,
                    'attl':attotal,
                    'dt':d1,'sub': 1,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                }
            elif(len(rolelist)>1):
                context = {
                    'lenm' :len(rolelist),
                    'ip':get_client_ip(request),
                    'roles' :rolelist,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'sub': 1,
                    'part_no': part_no,
                    'obj1':obj,
                    'dtl':obj2,
                    'obj3':obj3,
                    'pttl':patotal,
                    'attl':attotal,
                    'dt':d1,
                    'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
                }

        bckbtn=request.POST.get('backbutton')
        if bckbtn=='Back':
            return render(request,"m1view.html",{})
    return render(request,"M1report.html",context)








@login_required
@role_required(urlpass='/m5view/')
def m5view(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)

    wo_nop = user_master.objects.none()
  
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            
            'ip':get_client_ip(request),
            'roles' :rolelist
        }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            brn_no = request.POST.get('br_no')
            doc_no = request.POST.get('doc_no')
            staff_no = request.POST.get('staff_no')
            ticket_no = request.POST.get('ticket_no')
            name = request.POST.get('name')
            doc_no =request.POST.get('doc_no')
            current_yr=int(datetime.datetime.now().year)


            print("Current year",current_yr)
            print("shop_sec",shop_sec)
       

            
           # print(doc_no)
            res = [int(x) for x in str(wo_no)] 
            print("WORK",str(res))
            # workorder=np.trim_zeros(res)

            s = [str(i) for i in res] 
            workorder = int("".join(s)) 
            print("wo_no",workorder)
            obj1 = M5DOCnew.objects.filter(batch_no=wo_no,shop_sec=shop_sec, part_no=part_no,brn_no=brn_no,m5glsn=doc_no).values('opn','n_shopsec','rm_partno','cut_shear','pr_shopsec','n_shopsec','l_fr','l_to','qty_insp','inspector','date','remarks','worker','m2slno','qty_ord','m5prtdt','rm_ut','rm_qty','tot_rm_qty','rej_qty','rev_qty','lc_no','pa','at','opn_desc').distinct()
            obj2 = Part.objects.filter(partno=part_no).values('drgno','des','partno').order_by('partno').distinct()
            obj3 = Batch.objects.filter(bo_no=workorder,brn_no=brn_no,b_close_dt__isnull=True).values('part_no').distinct()
            obj4 = M5SHEMP1.objects.filter(shopsec=shop_sec).values('shopsec','staff_no','in_date','flag','name','cat','in1','out','ticket_no','month_hrs','total_time_taken','out_date','in_date','shift_typename').distinct()
            obj5 = M5SHEMP1.objects.filter(shopsec=shop_sec).values('shopsec','staff_no','name','ticket_no','flag').distinct()
            obj6  = Oprn.objects.filter(shop_sec=shop_sec,part_no=part_no).values('qtr_accep','mat_rej').exclude(qtr_accep=None,mat_rej=None).distinct()
            obj10= Batch.objects.filter(bo_no=workorder).values('batch_type','loco_fr','loco_to')[0]
            print(obj3)
            leng=0
            leng5=0
            leng9=0
            obj=0
            obj7=0
            obj9=0
            if len(obj1):
                raw_mat= obj1[0]['rm_partno']
                opn= obj1[0]['opn']
                obj7 = Part.objects.filter(partno=raw_mat).values('des').distinct()
                obj  = Oprn.objects.filter(part_no=part_no,opn=opn).values('ncp_jbs').distinct()
                leng = obj.count()
                print(raw_mat,opn)
                print(obj)
                print(obj7)
                leng5=obj7.count()
            if len(obj3):
                end_part=obj3[0]['part_no']
                obj9 = Part.objects.filter(partno=end_part).values('des').distinct()
                leng9=obj9.count()

            print("OBJ",obj)
            print("OBJ1",obj1)
            print("OBJ2",obj2)
            print("OBJ3",obj3)
            print("OBJ4",obj4)
            print("OBJ5",obj5)
            print("OBJ6",obj6)
            print("OBJ7",obj7)
            # print("OBJ8",obj8)
            print("OBJ9",obj9)

            
            
           

        
           
            obj8 = M5SHEMP1.objects.filter(shopsec=shop_sec).values('flag').distinct()
            print("OBJ8",obj8)
            # obj9 = empmast.objects.filter()
            staff=5548
            rr=0

           
            # # print("OBJ!0",obj10)
            # print("obj7",obj7)
            # print("ibj",obj6)
            # print("OBJ5",obj5)
            # print("OBJ!",obj8)

            staff=M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
           
            prtstaff=[]
            for i in staff:
              prtstaff.append(i['staff_no'])
            # print(prtstaff)  
    #    .    print(prtlist) 
            # print("obj4",obj4)
            # print("oj4 len",len(obj4))
            ticket= randint(1111,9999)
           
            leng1=obj1.count()
            leng2=obj2.count()
            leng3=obj3.count()
            leng4=obj4.count()
           
            leng7=obj5.count()
            leng6=obj6.count()
           
            leng8=obj8.count()
            #print("lengg4",leng4)
            
            
            if obj != None:
                if "Superuser" in rolelist:
                    tm=M5SHEMP.objects.all().values('shopsec').distinct()
                    tmp=[]
                    for on in tm:
                        tmp.append(on['shopsec'])
                    context={
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'obj': obj,
                        'obj1':obj1,
                        'obj2':obj2,
                        'obj3':obj3,
                        'obj4':obj4,
                        'obj7':obj7,
                        'obj5':obj5,
                        'obj6' :obj6,
                        'obj8':obj8,
                        'obj9':obj9,
                        'obj10':obj10,
                        'len9':leng9,
                        'len8':leng8,
                        'ticket1':ticket,
                        'rr':rr,
                        'sub': 1,
                        'len': leng,
                        'len1':leng1,
                        'len2':leng2,
                        'len3':leng3,
                        'len4':leng4,
                        'len5':leng5,
                        'len6':leng6,
                        'len7':leng7,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'cyear':current_yr,
                        #'assm_no':assm_no,
                        'brn_no': brn_no,
                        'doc_no': doc_no,
                        'prtstaff':prtstaff,
                        'staff_no':staff_no,
                        'subnav':subnav,
                    }
                elif(len(rolelist)==1):
                    # print("in m5 else")
                    for i in range(0,len(rolelist)):
                        req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
                        wo_nop =wo_nop | req
                    context = {
                        'lenm' :len(rolelist),
                        'wo_nop':wo_nop,
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1':obj1,
                        'obj2':obj2,
                        'obj3':obj3,
                        'obj4':obj4,
                        'obj5':obj5,
                        'obj6':obj6,
                        'obj7':obj7,
                        'obj8':obj8,
                        'obj9':obj9,
                        'obj10':obj10,
                        'rr':rr,
                        'len9':leng9,
                        'len8':leng8,
                        'sub': 1,
                        'len': leng,
                        'len1':leng1,
                        'len2':leng2,
                        'len3':leng3,
                        'len4':leng4,
                        'len5':leng5,
                        'len6':leng6,
                        'len7':leng7,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'cyear':current_yr,
                        #'assm_no':assm_no,
                        'brn_no': brn_no,
                        'doc_no': doc_no,
                        'prtstaff':prtstaff,
                        'staff_no':staff_no,
                        'subnav':subnav
                    }
                elif(len(rolelist)>1):
                    context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1':obj1,
                        'obj2':obj2,
                        'obj3':obj3,
                        'obj4':obj4,
                        'obj5':obj5,
                        'obj6':obj6,
                        'obj7':obj7,
                        'obj8':obj8,
                        'obj9':obj9,
                        'obj10':obj10,
                        'rr':rr,
                        'len9':leng9,
                        'len8':leng8,
                        'sub': 1,
                        'len': leng,
                        'len1':leng1,
                        'len2':leng2,
                        'len3':leng3,
                        'len4':leng4,
                        'len5':leng5,
                        'len6':leng6,
                        'len7':leng7,
                        'cyear':current_yr,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        #'assm_no':assm_no,
                        'brn_no': brn_no,
                        'doc_no': doc_no,
                        'prtstaff':prtstaff,
                        'staff_no':staff_no,
                        'subnav':subnav
                    }    
        if submitvalue=='submit':
            print("M%n")
            leng=request.POST.get('len')
            shopsec= request.POST.get('shop_sec')
            partno= request.POST.get('partno')
            brn_no = request.POST.get('brn_no')
            inoutnum=request.POST.get("inoutnum")
            #name = request.Post.get('name')

            len4=request.POST.get('len4')

            qty_insp = request.POST.get('qty_insp')
            inspector = request.POST.get('inspector')
            date = request.POST.get('date')
            remarks = request.POST.get('remarks')
            rev_qty=request.POST.get('rev_qty')
            rej_qty=request.POST.get('rej_qty')
            worker=request.POST.get('worker')
            #worker = request.POST.get('worker')
            
            # in1 = request.POST.get('in1')
            # out = request.POST.get('out')
            # #lc_no = request.POST.get('lc_no'+str(i))
            # # brn_no = request.POST.get('brn_no'+str(i))
            # cat = request.POST.get('cat')
            # staff_no = request.POST.get('staff_no')
            # ticket_no = request.POST.get('ticket_no')
            # month_hrs = request.POST.get('month_hrs')
            # total_time_taken = request.POST.get('total_time_taken')
            # in_date =  request.POST.get('in_date')
            # out_date= request.POST.get('out_date')
            # rm_ut =  request.POST.get('rm_ut')


           # print(remarks)
           # print(qty_insp)



           # print(inspector)
           # print(worker)
            print(date)

            print("@")
            print(shopsec)
            print(partno)
            print(brn_no)
            print(inspector)
            print(worker)
            print(date)
            print(remarks)
            print(qty_insp)
            print(rev_qty)
            print(rej_qty)
            #print(in1)
            #print(out)
           # print(date)

            M5DOCnew.objects.filter(shop_sec=shopsec,part_no=partno,brn_no=brn_no).update(qty_insp=str(qty_insp),inspector=str(inspector),date=str(date),remarks=str(remarks),rev_qty=str(rev_qty),rej_qty=str(rej_qty),worker=str(worker))             
            
            # staff_no = request.POST.get('staff_nohid')
            # name = request.POST.get('namehid')
            # ticket_no = request.POST.get('ticket_nohid')
            # cat = request.POST.get('cat1')
            # m5upd=M5SHEMP.objects.filter(shopsec=shopsec,staff_no=staff_no,cat=cat)
            # print("m5upd",m5upd)
            
        #     for i in range(1, int(len4)+1):

        #         print("i",i)
        #         in1 = request.POST.get('in1'+str(i))

                

        #         out = request.POST.get('out'+str(i))
        #         lc_no = request.POST.get('lc_no'+str(i))
        #        # brn_no = request.POST.get('brn_no'+str(i))
        #         cat = request.POST.get('cat'+str(i))
        #         # staff_no = request.POST.get('staff_no'+str(i))
        #         # ticket_no = request.POST.get('ticket_no'+str(i))
        #         month_hrs = request.POST.get('month_hrs'+str(i))
        #         total_time_taken = request.POST.get('total_time_taken'+str(i))
        #         # name = request.POST.get('name'+str(i))
        #         in_date = request.POST.get('in_date'+str(i))
        #         out_date = request.POST.get('out_date'+str(i))


        #         # M5SHEMP.objects.filter(shopsec=shopsec,staff_no=staff_no,cat=cat).update(in1=str(in1),out=str(out),month_hrs=int(month_hrs),total_time_taken=str(total_time_taken),date=str(date),ticket_no=int(ticket_no))

        #    # print(worker)
           # print(date)
            print("leng",leng)
            len4=request.POST.get('len4')
            
            for i in range(1, int(leng)+1):
                qtyac = request.POST.get('qtyac')
                matrej = request.POST.get('mat_rej')
                lc_no = request.POST.get('lc_no')
                pa = request.POST.get('pa')
                at = request.POST.get('at')
                shopsec = request.POST.get('shop_sec')
                # partno = request.POST.get('part_no')
                
               
                print("staff No")
                print(shopsec)
                print(partno)
                print(lc_no)
                print(qtyac)
                print(matrej)
                print(at)
                print(pa)
                Oprn.objects.filter(shop_sec=shopsec).update(qtr_accep=int(qtyac),mat_rej=int(matrej))
               
                 

                print("len4",len4,"inoutnum",inoutnum)
                len4=request.POST.get('len4')
            for i in range(int(len4)+1, int(inoutnum)+1):
                in1 = request.POST.get('in1add'+str(i))
                out = request.POST.get('outadd'+str(i))
                lc_no = request.POST.get('lc_no'+str(i))
                # brn_no = request.POST.get('brn_no'+str(i))
                cat = request.POST.get('catadd'+str(i))
                staff_no = request.POST.get('staff_noadd'+str(i))
                staff_name = request.POST.get('staff_nameadd'+str(i))
                ticket_no = request.POST.get('ticket_noadd'+str(i))
                month_hrs = request.POST.get('month_hrsadd'+str(i))
                total_time_taken = request.POST.get('total_time_takenadd'+str(i))
                # name = request.POST.get('name'+str(i))
                in_date = request.POST.get('in_dateadd'+str(i))
                out_date = request.POST.get('out_dateadd'+str(i))
                shift = request.POST.get('shiftadd'+str(i))
                
                print("j",i)
                print("shift",shift)
                
                if len(cat)==1:
                    cat="0"+cat
                print("stf no",staff_no) 

                print("name",staff_name)
                print("in_time",in1)
                print("in_date",in_date)
                print("out",out)
                print("Out_date",out_date) 
                print("month_hrs",month_hrs)   
                print("cat",cat)
                print("ticket_no",ticket_no)
                print("total time",total_time_taken)
                print("Create new row")
                M5SHEMP1.objects.create(shopsec=shopsec,staff_no=str(staff_no),name=str(staff_name),in1=str(in1),out=str(out),month_hrs=int(month_hrs),total_time_taken=str(total_time_taken),cat=str(cat),in_date=str(in_date),out_date=str(out_date),ticket_no=int(ticket_no),shift_typename=str(shift))
                
                
            wo_no=M5DOCnew.objects.all().values('batch_no').distinct()

    return render(request,"m5view.html",context)

def m5getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        # print(shop_sec)
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').exclude(batch_no__isnull=True).distinct())
        # print(wono)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m5getbr(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        br_no = list(M5DOCnew.objects.filter(batch_no =wo_no,shop_sec=shop_sec).values('brn_no').exclude(brn_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

   

def m5getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        part_no = list(M5DOCnew.objects.filter(batch_no =wo_no,brn_no=br_no,shop_sec=shop_sec).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m5getdoc_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        part_no = request.GET.get('part_no')
        doc_no = list(M5DOCnew.objects.filter(batch_no =wo_no,brn_no=br_no,shop_sec=shop_sec,part_no=part_no).values('m5glsn').distinct())
        print(doc_no)
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m5getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        # staff_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        br_no = list(M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m5getempname(request):
   if request.method == "GET" and request.is_ajax():  
        examcode= request.GET.get('two')
        x =512000
        y=15719
        a = math.floor(math.log10(y))
        hello= int(x*10**(1+a)+y)
        print(hello)
        ex = M5SHEMP.objects.filter(staff_no= examcode).all()  
        # print(ex[0].get("name"))
        obj10= empmast.objects.filter(empno__contains=examcode).all()
        # print("ONKJJ",obj10[0]['ticket_no'])
        # print(obj10[0].get("ticket_no"))
        ticket=0
        if len(obj10):
            ticket=obj10[0].ticket_no
            print("ticket",ticket)
        
        # print(obj10)
        exam ={
            "exam_type":ex[0].name,
            "ticket":ticket,
             
           
           
        }
    
        

        return JsonResponse({"exam":exam}, safe = False)
        return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/m12view/')
def m12view(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_no = empmast.objects.none()
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'len' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
            wo_no =wo_no | req
        context = {
            'sub':0,
            'len' :len(rolelist),
            'wo_no':wo_no,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'lent':0,
        }
        # return render(request,"m2view.html",context)
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'len' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'lent':0,
        }
    if request.method == "POST":
        #print("hi")
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            from decimal import Decimal
            #print("ii")
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            month = request.POST.get('month')
            wo_no = request.POST.get('wo_no')
            print(month)
            #obj3 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('month')[0]
            obj1 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('cat','time_hrs','date','in1','out','reasons_for_idle_time','total_time','idle_time','month').distinct() 
            print(obj1)
           # print(obj1[0]['total_time'])
            obj2='None'
            obj3='None'
            leng=0
            leng1=0
            rr='None'
            amt=0
            patotal=0
            a=0
            b=0
            if len(obj1):
                t=obj1[0]['cat']
                print(t)
                print(obj1[0]['total_time'])
                if t != 'None':
                    obj2 = Rates.objects.filter(cat=t).values('avg_rate').distinct()
                    obj3 = M12DOC.objects.filter(shopsec=shop_sec,staff_no=staff_no,month=month).values('month','cat')[0]
                   
           
                for op in range(len(obj1)):
                    patotal=obj1[op]['total_time']
                    p=patotal.split(':')
                    a=a+Decimal(p[0])
                    b=b+Decimal(p[1])
                    if (b>=60):
                        a=a+1
                        b=b%60
                          
                    rr=str(a)+':'+str(b)     
                    print(rr)
                
           
                    print("a",a)
                    print("b",b)
                print("object1",obj1)
                tmhr=rr
                if len(obj2):    
                    avgrt=obj2[0]['avg_rate']
                    if tmhr == 'None': 
                        tmhr=0
                        avgrt=0
                    else:
                        tmhr1=tmhr.split(':')
                        tmhr=Decimal(tmhr1[0])+(Decimal(tmhr1[1])/60)
                                
                        
                    amt=tmhr*avgrt
                leng = obj1.count()
                leng1 = obj2.count()
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'len' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,
                    'sub':1,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                    wo_no =wo_no | req
                context = {
                    'len' :len(rolelist),
                    'wo_no':wo_no,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles' :rolelist,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,
                    'sub':1,
                }
            elif(len(rolelist)>1):
                context = {
                    'len' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles' :rolelist,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,
                    'sub':1,
                }

        if submitvalue=='submit':
            leng=request.POST.get('len')
            shopsec= request.POST.get('shopsec')
            staff_no = request.POST.get('staff_no')
            month = request.POST.get('month')
            inoutnum=request.POST.get("inoutnum")
            amt = request.POST.get('amt')
            for i in range(1, int(leng)+1):
                in1 = request.POST.get('in1'+str(i))
                out = request.POST.get('out'+str(i))
                date = request.POST.get('date'+str(i))
                month = request.POST.get('month'+str(i))
               
                total_time = request.POST.get('total_time'+str(i))
                time_hrs = request.POST.get('total_time'+str(i))
                idle_time = request.POST.get('idle_time'+str(i))
                reasons_for_idle_time = request.POST.get('reasons_for_idle_time'+str(i))
                M12DOC.objects.filter(shopsec=shopsec,staff_no=staff_no,date=date,month=month).update(date=str(date),in1=str(in1),out=str(out),month=str(month),total_time=str(total_time),idle_time=str(idle_time),reasons_for_idle_time=str(reasons_for_idle_time),time_hrs=str(time_hrs),amt=str(amt))
               

            for i in range(1, int(inoutnum)+1):
                in1 = request.POST.get('in1add'+str(i))
                out = request.POST.get('outadd'+str(i))
                month = request.POST.get('month_add'+str(i))
                total_time = request.POST.get('total_time_add'+str(i))
                date = request.POST.get('dateadd'+str(i))
                cat = request.POST.get('catadd'+str(i))
                time_hrs = request.POST.get('total_time_add'+str(i))
                idle_time = request.POST.get('idle_time_add'+str(i))
                reasons_for_idle_time = request.POST.get('reasons_for_idle_timeadd'+str(i))
               
              
                M12DOC.objects.create(shopsec=shopsec,staff_no=staff_no,in1=str(in1),out=str(out),month=str(month),total_time=str(total_time),date=str(date),idle_time=str(idle_time),reasons_for_idle_time=str(reasons_for_idle_time),cat=str(cat),time_hrs=str(time_hrs))
               
                
                

                wo_no=Batch.objects.all().values('bo_no').distinct()
    return render(request,"m12view.html",context)
                   
def m12getwono(request):
    if request.method == "GET" and request.is_ajax():
        #from.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2=Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
        wono = list(w2)
        
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)



def m12getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
       # staff_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        staff_no = list(M12DOC.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m12getempname(request):
   if request.method == "GET" and request.is_ajax():  
        examcode= request.GET.get('two')
        ex = M5SHEMP.objects.filter(staff_no= examcode).all()  
        exam ={
            "exam_type":ex[0].name,
        }
        return JsonResponse({"exam":exam}, safe = False)
        return JsonResponse({"success":False}, status=400)















@login_required
@role_required(urlpass='/machining_of_air_box/')
def insert_machining_of_air_box(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    obj2=MachiningAirBox.objects.all().filter(dispatch_status=False).order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=MachiningAirBox.objects.filter(dispatch_status=False).values('sno')
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mysno':mysno,
       }
    if request.method=="POST":
        
        once=request.POST.get('once')
        print(once)
    
        submit=request.POST.get('submit')
        if submit=='Save':
        
            bo_no=request.POST.get('bo_no')
            bo_date=request.POST.get('bo_date')
            pt_no=request.POST.get('pt_no')
            bo_qty=request.POST.get('bo_qty')
            date=request.POST.get('date')
            loco_type=request.POST.get('locos')
            airbox_sno=request.POST.get('airbox_sno')
            airbox_make=request.POST.get('airbox_make')
            in_qty=request.POST.get('in_qty')
            out_qty=request.POST.get('out_qty')
            if bo_no and bo_date and pt_no and bo_qty and date and loco_type and airbox_sno and airbox_make and in_qty and out_qty:
               obj=MachiningAirBox.objects.create()
               obj.bo_no=bo_no
               obj.bo_date=bo_date
               obj.bo_qty=bo_qty
               obj.pt_no=pt_no
               obj.date=date
               obj.loco_type=loco_type
               obj.airbox_sno=airbox_sno
               obj.airbox_make=airbox_make
               obj.in_qty=in_qty
               obj.out_qty=out_qty
               obj.save()
               messages.success(request, 'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=MachiningAirBox.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='save':
    
            sno=int(request.POST.get('editsno'))
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            pt_no=request.POST.get('editpt_no')
            bo_qty=request.POST.get('editbo_qty')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            airbox_sno=request.POST.get('editairbox_sno')
            airbox_make=request.POST.get('editairbox_make')
            in_qty=request.POST.get('editin_qty')
            out_qty=request.POST.get('editout_qty')
            if bo_no and bo_date and pt_no and bo_qty and date and loco_type and airbox_sno and airbox_make and in_qty and out_qty:
               MachiningAirBox.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,pt_no=pt_no,bo_qty=bo_qty,date=date,loco_type=loco_type,airbox_sno=airbox_sno,airbox_make=airbox_make,in_qty=in_qty,out_qty=out_qty)
               messages.success(request, 'Successfully Edited!')
            else:
               messages.error(request,"Please Enter S.No.!")

        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dispatch_date=request.POST.get('dispatch_date')
            dislocos=request.POST.get('dislocos')
            if sno and dispatch_date and dislocos:
                MachiningAirBox.objects.filter(sno=sno).update(dispatch_date=dispatch_date,dispatch_to=dislocos,dispatch_status=True)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            first=int(request.POST.get('delsno'))
            if first:
                MachiningAirBox.objects.filter(sno=first).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        return HttpResponseRedirect("/machining_of_air_box/")

    return render(request,"machining_of_air_box.html",my_context)


def airbox_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)










@login_required
@role_required(urlpass='/miscellaneous_section/')
def miscellaneous_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    obj2=MiscellSection.objects.all().filter(dispatch_status=False).order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=MiscellSection.objects.filter(dispatch_status=False).values('sno')
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
        'usermaster':usermaster,
        'ip':get_client_ip(request),
        'mybo':mybo,
        'mysno':mysno,
       }
    if request.method=="POST":
        
        once=request.POST.get('once')
        print(once)
        submit=request.POST.get('submit')
        if submit=='Save':
        
            first=request.POST.get('bo_no')
            second=request.POST.get('bo_date')
            pt_no=request.POST.get('pt_no')
            bo_qty=request.POST.get('bo_qty')
            third=request.POST.get('date')
            fourth=request.POST.get('locos')
            fifth=request.POST.get('shaft_m')
            sixth=request.POST.get('in_qty')
            seventh=request.POST.get('out_qty')
            if first and second and pt_no and bo_qty and third and fourth and fifth and sixth and seventh:
                obj=MiscellSection.objects.create()
                obj.bo_no=first
                obj.bo_date=second
                obj.bo_qty=bo_qty
                obj.pt_no=pt_no
                obj.date=third
                obj.loco_type=fourth
                obj.shaft_m=fifth
                obj.in_qty=sixth
                obj.out_qty=seventh
                obj.save()
                messages.success(request, 'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=MiscellSection.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='save':
        
            sno=int(request.POST.get('editsno'))
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            pt_no=request.POST.get('editpt_no')
            bo_qty=request.POST.get('editbo_qty')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            shaft_m=request.POST.get('editshaft_m')
            in_qty=request.POST.get('editin_qty')
            out_qty=request.POST.get('editout_qty')
            if sno and bo_no and pt_no and bo_qty and bo_date and date and loco_type and shaft_m and in_qty and out_qty:
                MiscellSection.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,shaft_m=shaft_m,in_qty=in_qty,out_qty=out_qty)
                messages.success(request, 'Successfully Edited!')
            else:
               messages.error(request,"Please Enter S.No.!")
        
        if submit=="Dispatch":
            
            first=int(request.POST.get('dissno'))
            second=request.POST.get('dislocos')
            dispatch_date=request.POST.get('dispatch_date')
            if first and dispatch_date and second:
               MiscellSection.objects.filter(sno=first).update(dispatch_date=dispatch_date,dispatch_to=second,dispatch_status=True)
               messages.success(request, 'Successfully Dispatched!')
            else:
               messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            first=int(request.POST.get('delsno'))
            if first:
                MiscellSection.objects.filter(sno=first).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        return HttpResponseRedirect("/miscellaneous_section/")

    return render(request,"miscellaneous_section.html",my_context)


def miscell_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def miscell_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(MiscellSection.objects.filter(sno=mysno).values('bo_no','bo_date','pt_no','bo_qty','shaft_m','in_qty','out_qty','date','loco_type'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400) 


@login_required
@role_required(urlpass='/m3view/')
def m3view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'roles' :rolelist,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'roles' :rolelist,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
        }
    if request.method == "POST":
        print("hi")
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            print("ii")
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            brn_no = request.POST.get('br_no')
            assembly_no = request.POST.get('assm_no')
            doc_no = request.POST.get('doc_no')
            obj = Part.objects.filter(partno=part_no).values('drgno','des')
            objj = M2Doc.objects.filter(m2sln=doc_no,f_shopsec=shop_sec).values('qty','rm_partno','m4_no','scl_cl').distinct()
            obj1 = empmast.objects.filter(role=shop_sec).values('empname','dept_desc')
            print(obj1)
            date = M2Doc.objects.filter(m2sln=doc_no).values('m2prtdt').distinct()
            leng = obj.count()
            leng1 = obj1.count()
            leng2 = objj.count()
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj': obj,
                    'objj': objj,
                    'obj1': obj1,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'date': date,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                    'sub':1,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
                    wo_nop =wo_nop | req
                context = {
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'roles' :rolelist,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'obj': obj,
                    'objj': objj,
                    'obj1': obj1,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'date': date,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                    'sub':1,
                }
            elif(len(rolelist)>1):
                context = {
                    'lenm' :len(rolelist),
                    'roles' :rolelist,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'obj': obj,
                    'objj': objj,
                    'obj1': obj1,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'date': date,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                    'sub':1,
                }

            # context = {
            #             'obj': obj,
            #             'objj': objj,
            #             'obj1': obj1,
            #             'len': leng,
            #             'len1':leng1,
            #             'len2':leng2,
            #             'date': date,
            #             'shop_sec': shop_sec,
            #             'part_no': part_no,
            #             'wo_no': wo_no,
            #             'brn_no': brn_no,
            #             'assembly_no': assembly_no,
            #             'doc_no': doc_no,
            #             'sub':1,
            #             'nav':nav,
            #             'subnav':subnav,
            # 'ip':get_client_ip(request),
            #         }
    return render(request,"m3view.html",context)


def m3getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        print(shop_sec)
        wo_no = list(M2Doc.objects.filter(f_shopsec = shop_sec).values('batch_no').distinct())
        # print(wo_no)
        return JsonResponse(wo_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m3getbr(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = list(M2Doc.objects.filter(batch_no =wo_no).values('brn_no').distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m3shopsec(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = list(M2Doc.objects.filter(batch_no =wo_no,brn_no=br_no).values('f_shopsec').distinct())
        return JsonResponse(shop_sec, safe = False)
    return JsonResponse({"success":False}, status=400)

def m3getassly(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = list(M2Doc.objects.filter(batch_no =wo_no,brn_no=br_no,f_shopsec=shop_sec).values('assly_no').distinct())
        return JsonResponse(assembly_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m3getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        part_no = list(M2Doc.objects.filter(batch_no =wo_no,brn_no=br_no,f_shopsec=shop_sec,assly_no=assembly_no).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m3getdoc_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M2Doc.objects.filter(batch_no =wo_no,brn_no=br_no,f_shopsec=shop_sec,assly_no=assembly_no,part_no=part_no).values('m2sln').distinct())
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m3sub(request):
    if request.method == "POST":

        shop_sec = request.POST.get('shop_sec')
        part_no = request.POST.get('part_nop')
        wo_no = request.POST.get('wo_no')
        brn_no = request.POST.get('br_no')
        assembly_no = request.POST.get('assm_no')
        doc_no = request.POST.get('doc_no')
        obj = Part.objects.filter(partno=part_no).values('drgno','des')
        objj = M2Doc.objects.filter(m2sln=doc_no,f_shopsec=shop_sec).values('qty','m4_no','scl_cl','rm_partno')
        obj1 = empmast.objects.filter(role=shop_sec).values('empname','dept_desc')
        date = M2Doc.objects.filter(m2sln=doc_no).values('m2prtdt').distinct()
        leng = obj.count()
        leng1 = obj1.count()
        leng2 = objj.count()

        context = {
                    'obj': obj,
                    'objj': objj,
                    'obj1': obj1,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    #'len3':leng3,
                    'date': date,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                    #'rm_partno': rm_partno,
    }

    return render(request, "m3view.html", context)






@login_required
@role_required(urlpass='/m7view/')
def m7view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
        # return render(request,"m2view.html",context)
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
            
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mon = request.POST.get('mon')
            wo_no = request.POST.get('wo_no')
            staff_no = request.POST.get('staff_no')
            part_no = request.POST.get('part_no')
            obj1 = M7.objects.filter(staff_no=staff_no).values('month','date','in1','out')
            obj2 = Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name','cat').distinct()
            leng = obj1.count()
            leng2 = obj2.count()
            print(obj1,"obj1")
            print(obj2,"obj2")
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':0,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj1': obj1,
                    'obj2': obj2,
                    'ran':range(1,2),
                    'len': 31,
                    'len2': leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no': staff_no,
                    'part_no': part_no, 
                    'mon': mon,
                    'sub':1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav, 
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                    wo_nop =wo_nop | req
                context = {
                    'sub':0,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj1': obj1,
                    'obj2': obj2,
                    'ran':range(1,2),
                    'len': 31,
                    'len2': leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no': staff_no,
                    'part_no': part_no, 
                    'mon': mon,
                    'sub':1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav, 
                }
        # return render(request,"m2view.html",context)
            elif(len(rolelist)>1):
                context = {
                    'sub':0,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj1': obj1,
                    'obj2': obj2,
                    'ran':range(1,2),
                    'len': 31,
                    'len2': leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no': staff_no,
                    'part_no': part_no, 
                    'mon': mon,
                    'sub':1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav, 
                }

        if submitvalue =='Submit':
                leng=request.POST.get('len')
                shop_sec= request.POST.get('shopsec')
                staff_no = request.POST.get('staffno')
                wo_no = request.POST.get('wono')
                part_no = request.POST.get('partno')
                inoutnum=request.POST.get("inoutnum")
                print(shop_sec,staff_no,wo_no,part_no)

                m7obj = M7.objects.filter(shop_sec=shop_sec,staff_no=staff_no,part_no=part_no).distinct()
                print(m7obj)
                if((m7obj)):
                    m7obj.delete()
                
                for i in range(1, int(leng)+1):
                    in1 = request.POST.get('in1'+str(i))
                    out = request.POST.get('out'+str(i))
                    date = request.POST.get('date'+str(i))
                    mon = request.POST.get('mon'+str(i))
                
                    print(in1,out,date,mon)
                    
                    # objjj=M7.objects.create(shop_sec=shop_sec,staff_no=staff_no,part_no=part_no,in1=in1,out=out,month=mon,date=date)
                    if in1 and out and date and mon :
                        objjj=M7.objects.create()
                        objjj.shop_sec=shop_sec
                        objjj.staff_no=staff_no
                        objjj.part_no=part_no
                        objjj.in1=in1
                        objjj.out=out
                        objjj.mon=mon
                        objjj.date=date
                        objjj.save()
                    #print(objjj)

                for i in range(1, int(inoutnum)+1):
                    in1 = request.POST.get('in1add'+str(i))
                    out = request.POST.get('outadd'+str(i))
                    month = request.POST.get('month_add'+str(i))
                    #total_time = request.POST.get('total_time_add'+str(i))
                    #name = request.POST.get('name'+str(i))
                    date = request.POST.get('dateadd'+str(i))

                    if in1 and out and date and mon :
                        obj5=M7.objects.create()
                        obj5.shop_sec=shop_sec
                        obj5.staff_no=staff_no
                        obj5.part_no=part_no
                        obj5.in1=in1
                        obj5.out=out
                        obj5.mon=mon
                        obj5.date=date
                        obj5.save()

                    
                wo_nop=Batch.objects.all().values('bo_no').distinct()
 
    return render(request,"m7view.html",context)
                        
def m7getwono(request):
    if request.method == "GET" and request.is_ajax():
        #from.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2=Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)


def m7getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        staff_no=list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m7getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        
        wo_no = request.GET.get('wo_no')
        
        part_no = list(Batch.objects.filter(bo_no=wo_no).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)








@login_required
@role_required(urlpass='/PinionPress/')
def pinionpressing_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    obj2=PinionPressing.objects.all().order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=PinionPressing.objects.all().values('sno')
    my_context={
       'object':obj2,
       'nav':nav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mysno':mysno,
       'subnav':subnav,
        }
    
    
    if request.method=="POST":
        once=request.POST.get('once')
        print(once)
        submit=request.POST.get('submit')
        
        if submit=='Save':
            first=request.POST.get('bo_no')
            second=request.POST.get('bo_date')
            third=request.POST.get('date')
            fourth=request.POST.get('tm_make')
            fifth=request.POST.get('tm_no')
            sixth=request.POST.get('locos')
            pt_no=request.POST.get('pt_no')
            bo_qty=request.POST.get('bo_qty')
            indate=request.POST.get('in_qty')
            outdate=request.POST.get('out_qty')
            if first and second and third and fourth and fifth and sixth and pt_no and bo_qty and indate and outdate:
                obj=PinionPressing.objects.create()
                obj.bo_no=first
                obj.bo_date=second
                obj.pt_no=pt_no
                obj.bo_qty=bo_qty
                obj.date=third
                obj.tm_make=fourth
                obj.tm_no=fifth
                obj.loco_type=sixth
                obj.inspection_status=False
                obj.in_qty=indate
                obj.out_qty=outdate
                obj.save()
                messages.success(request,'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")    
        
        obj2=PinionPressing.objects.all().order_by('sno') 
        my_context={
            'object':obj2,
            }   

        if submit=='Edit':
            temp=request.POST.get('sno')
            print(temp)
            if temp is not None:
                sno=int(temp)
            else:
                sno=None
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            date=request.POST.get('editdate')
            tm_make=request.POST.get('edittm_make')
            tm_no=request.POST.get('edittm_no')
            bo_qty=request.POST.get('editbo_qty')
            pt_no=request.POST.get('editpt_no')
            indate=request.POST.get('editin_qty')
            outdate=request.POST.get('editout_qty')
            if sno and bo_no and bo_date and date and tm_make and tm_no and pt_no and bo_qty and indate and outdate:
                PinionPressing.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,tm_make=tm_make,tm_no=tm_no,pt_no=pt_no,bo_qty=bo_qty,in_qty=indate,out_qty=outdate)
                messages.success(request, 'Successfully Edited!')
            else:
                messages.error(request,"Please Enter S.No.!")        



        if submit=='Inspect':
            sno=int(request.POST.get('snowheel'))
            # print(sno)
            pinion_no=request.POST.get('pinion_no')
            pinion_make=request.POST.get('pinion_make')
            pinion_travel=request.POST.get('pinion_travel')
            pinion_pressure=request.POST.get('pinion_pressure')
            blue_match=request.POST.get('blue_match')
            # loco_type=request.POST.get('locos')
            if pinion_no and pinion_make and pinion_travel and pinion_pressure and blue_match :
                PinionPressing.objects.filter(sno=sno).update(pinion_no=pinion_no,pinion_make=pinion_make,pinion_travel=pinion_travel,pinion_pressure=pinion_pressure,blue_match=blue_match,inspection_status=True) 
                messages.success(request,'Successfully Inspected!')
            else:
                messages.error(request,"Please Enter All Records!")

        
        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            disdate=request.POST.get('dispatch_date')
            if sno and dislocos and disdate:
                PinionPressing.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_date=disdate)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            sno=int(request.POST.get('delsno'))
            if sno:
                PinionPressing.objects.filter(sno=sno).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")

        return HttpResponseRedirect("/PinionPress/")
    
    return render(request,"PinionPress.html",my_context)

def pinion_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','batch_qty','part_no'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)
        
def pinion_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(PinionPressing.objects.filter(sno=mysno).values('bo_no','bo_date','loco_type','date','tm_make','tm_no','pt_no','bo_qty','in_qty','out_qty'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)  

def airbox_editsno(request):
    if request.method=="GET" and request.is_ajax():
        print("in ajax call")
        mysno=request.GET.get('sels_no')
        print("sno",mysno)
        myval=list(MachiningAirBox.objects.filter(sno=mysno).values('bo_no','bo_date','airbox_sno','airbox_make','in_qty','out_qty','date','loco_type','pt_no','bo_qty'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400) 


def axlepress_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(AxleWheelPressing.objects.filter(sno=mysno).values('bo_no','bo_date','loco_type','date','axle_no','wheelno_de','wheelno_nde','bullgear_no','bullgear_make','pt_no','bo_qty','in_qty','out_qty'))
        AxleMachining.objects.filter(axle_no=myval[0]['axle_no']).update(axlefitting_status=False)
        WheelMachining.objects.filter(wheel_no=myval[0]['wheelno_de']).update(wheelfitting_status=False)
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)  

def wheelnde(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('wheel_no')
        print("wheel no:",mybo)
        myval = list(WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no').exclude(wheel_no=mybo))
        print(myval)
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)




@login_required
@role_required(urlpass='/M20view/')
def M20view(request):
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
    dictemper={}
    totindb=0
    
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'lvdate':"yyyy-mm-dd",
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"yyyy-mm-dd",
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"yyyy-mm-dd",
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Add':
            rolelist=usermaster.role.split(", ")

            wo_nop = empmast.objects.none()

            shop_sec = request.POST.get('shop_sec')
            #staffno=request.POST.get('staff_no')

            lvdate=request.POST.get('lv_date')
            print("lvdate",lvdate)
            

            # lv_date_temp1 = lv_date.split("-")[0]
            # print("month---->",month_temp1)

            # lv_date_temp2 = lv_date.split("-")[1]
            # print("days---->",month_temp2)

            # lv_date_temp3 = lv_date.split("-")[2]
            # print("year---->",month_temp3)

            # lvdate = month_temp1+"-"+month_temp_2+"-"+month_temp3

            # print("final date after formating",lvdate)
            # # name=request.P




            m2=M20new.objects.filter(shop_sec=shop_sec,lv_date=lvdate)
            # print(m2)
            if m2 is not None and len(m2):
                for mm in range(len(m2)):
                    temper = {str(mm):{"name":m2[mm].name,
                                               "ticketno":m2[mm].ticketno,
                                               "date":m2[mm].alt_date,
                                               }}


                    totindb=totindb+1

                    dictemper.update(copy.deepcopy(temper))
                    print(dictemper)

            w1=M5SHEMP.objects.filter(shopsec=shop_sec).values('name').distinct()
            # print("w1",w1)
            wono=[]
            for w in range(len(w1)):
                wono.append(w1[w]['name'])
                # print(w1[w]['name'])
            # print("wono",wono)
            # w1=M5SHEMP.objects.filter(staff_no=staffno).values('staff_no','name').distinct()
            # wono = list(w1)
            # ename=wono[0]['name']
            # obj1=M20new.objects.filter(shop_sec=shop_sec,staff_no=staffno).first()
            # print(obj1)
            
            alt_date="yy-mm-dd"
            # if obj1 is not None:
            #     ename=obj1[0].name
            #     alt_date=obj1[0].alt_date
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    # 'obj1':obj1,
                    # 'empname':ename,
                    # 'ticketno':staffno,
                    'names':wono,
                    'dictemper':dictemper,
                    'totindb':totindb,
                    'alt_date':alt_date,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
                    req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'sub':1,
                    'subnav':subnav,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                    # 'ticket':wono[0]['staff_no'],
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                    # 'ticket':wono[0]['staff_no'],
                }
        
        if submitvalue=='Save':
            print("data saved")
            shop_sec= request.POST.get('shop_sec')
            # staff_no=request.POST.get('stffno')
            lv_date= request.POST.get('lv_date')


            # print("test : --------------",lv_date)
            # lv_date_temp1 = lv_date.split("-")[0]
            # print("month---->",month_temp1)

            # lv_date_temp2 = lv_date.split("-")[1]
            # print("days---->",month_temp2)

            # lv_date_temp3 = lv_date.split("-")[2]
            # print("year---->",month_temp3)

            # lv_date = month_temp1+"-"+month_temp_2+"-"+month_temp3

           
            # name=request.POST.get('empname')
            # ticketno = request.POST.get('stffno')
            # alt_date = request.POST.get('alt_date')
            # M20new.objects.create(shop_sec=str(shop_sec),staff_no=str(staff_no), lv_date=str(lv_date), name=str(name), ticketno=str(ticketno), alt_date=str(alt_date))
            tot=0
            tot=request.POST.get('totmebs')
            print("total members",tot)


            totindb=request.POST.get('totindb')
            for tb in range(1,int(totindb)+1):
                namedb=request.POST.get('namedb'+str(tb))
                ticketnodb=request.POST.get('ticketnodb'+str(tb))
                datedb=request.POST.get('datedb'+str(tb))
                print("Dateindb"+str(tb),datedb)
                M20new.objects.filter(shop_sec=str(shop_sec),staff_no=str(ticketnodb), lv_date=str(lv_date) ).update(alt_date=str(datedb))

            for t in range(1,int(tot)+1):
                name=request.POST.get('name'+str(t))
                ticketno=request.POST.get('ticket'+str(t))
                date=request.POST.get('date'+str(t))
                print(name,ticketno,date)

                M20new.objects.create(shop_sec=str(shop_sec),staff_no=str(ticketno), lv_date=str(lv_date), name=str(name), ticketno=str(ticketno), alt_date=str(date))
                emp_detail= emp_details.objects.filter(shopsec=shop_sec, empno=ticketno).values('email_id','mobileno')
                # email("erpdlw@gmail.com", "erpdlw@123", emp_detail[0]['email_id']," M20 Card Saved")
                sms(emp_detail[0]['mobileno'],"Leave alloted on"+date+" for sunday booking, m20 card saved ")
                print(shop_sec,lv_date,name,ticketno,date)
                print("check----->>",emp_detail[0]['email_id'])
            messages.success(request, 'Successfully Saved !!!, Select new values to update')
    return render(request, "M20view.html", context)



def email(sender_email_id,sender_email_id_password,receiver_email_id,message):
    print(sender_email_id)
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls()
    s.login(sender_email_id,sender_email_id_password)  
    s.sendmail(sender_email_id,receiver_email_id, message) 
    s.quit()

def sms(phoneno,message):
    url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to=91"+str(phoneno)+"&msg="+message+" &msg_type=TEXT&userid=2000184632&auth_scheme=plain&password=pWK3H5&v=1.1&format=text"
    
    print("Message ---->>",message)
    response = requests.request("POST", url)
    print(response.text)

def m20getstaffno(request):
    if request.method == "GET" and request.is_ajax():  
        from.models import Batch      
        shop_sec = request.GET.get('shop_sec')
        name=request.GET.get('name')
        # print("ths is",shop_sec)
        w1=M5SHEMP.objects.filter(shopsec=shop_sec,name=name).values('staff_no').distinct()
        wono = w1[0]['staff_no']
        cont ={
            "wono":wono,
        }
        # print("ths is",shop_sec)
        return JsonResponse({"cont":cont}, safe = False)

    return JsonResponse({"success":False}, status=400)

def m20getstaffName(request):
    if request.method == "GET" and request.is_ajax():  
        from.models import Batch     
        shop_sec = request.GET.get('shop_sec')
        staff_no = request.GET.get('staff_no')
        # print(staff_no)
        w1=M5SHEMP.objects.filter(staff_no=staff_no).values('staff_no','name').distinct()
        wono = list(w1)
        # print("ths is",shop_sec)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(urlpass='/MG33view/')
def MG33view(request):
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
    dictemper={}
    totindb=0
    
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'lvdate':"dd-mm-yy",
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"dd-mm-yy",
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"dd-mm-yy",
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Add':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            #staffno=request.POST.get('staff_no')
            lvdate=request.POST.get('updt_date')
            examcode = []
            ex = exam_master.objects.all().values('exam_code')
            for i in ex:
                examcode.append(i['exam_code']) 
            # m2=M20new.objects.filter(shop_sec=shop_sec,lv_date=lvdate)
            # # print(m2)
            # if m2 is not None and len(m2):
            #     for mm in range(len(m2)):
            #         temper = {str(mm):{"name":m2[mm].name,
            #                                    "ticketno":m2[mm].ticketno,
            #                                    "date":m2[mm].alt_date,
            #                                    }}


            #         totindb=totindb+1

            #         dictemper.update(copy.deepcopy(temper))
            #         print(dictemper)

            w1=Shemp.objects.filter(shopsec=shop_sec).values('name').distinct()
            # print("w1",w1)
            wono=[]
            for w in range(len(w1)):
                wono.append(w1[w]['name'])
                

            # w2=Shemp.objects.filter(shopsec=shop_sec).values('name').distinct()
            w2 = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname')
            # print("w1",w1)
            names=[]
            for w in range(len(w2)):
                names.append(w2[w]['empname'])
                # print(w1[w]['name'])
            # print("wono",wono)
            # w1=M5SHEMP.objects.filter(staff_no=staffno).values('staff_no','name').distinct()
            # wono = list(w1)
            # ename=wono[0]['name']
            # obj1=M20new.objects.filter(shop_sec=shop_sec,staff_no=staffno).first()
            # print(obj1)
            
            alt_date="yyyy-mm-dd"
            # if obj1 is not None:
            #     ename=obj1[0].name
            #     alt_date=obj1[0].alt_date
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':names,
                    'names':wono,
                    # 'dictemper':dictemper,
                    # 'totindb':totindb,
                     'totindb':0,
                    'alt_date':alt_date,
                    'examcode': examcode
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname').distinct

                    # req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                    # wo_nop = wo_nop | req

                context = {
                    'sub':1,
                    'subnav':subnav,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':names,
                    'names':wono,
                    'examcode': examcode
                    # 'ticket':wono[0]['staff_no'],
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':names,
                    'names':wono,
                    'examcode': examcode
                    # 'ticket':wono[0]['staff_no'],
                }
        
        if submitvalue=='Save':
            print("data saved")
            tot=request.POST.get('totmebs')
            print("tot",tot)
            tot=int(tot)+1
            pract="prac"
            oral="oral"
            ttl="total"
            ename="name"
            stffn="ticket"
            skill="skill"
            remkr="remk"
            for i in range(1,int(tot)):
                pscore=request.POST.get(pract+str(i))
                orscore=request.POST.get(oral+str(i))
                tscore=request.POST.get(ttl+str(i))
                skills=request.POST.get(skill+str(i))
                epname=request.POST.get(ename+str(i))
                stfno=request.POST.get(stffn+str(i))
                remk=request.POST.get(remkr+str(i))
                place_exam = request.POST.get('place')
                prac_desc = request.POST.get('prac_desc')
                oral_desc = request.POST.get('oral_desc')
                sec_sup = request.POST.get('sec_sup')
                trade_test_officer= request.POST.get('trade_test_officer')
                foreman = request.POST.get('foreman')
                trade_test_admin = request.POST.get('trade_test_admin')
                examdate = request.POST.get('exam_date')
                shop_sec = request.POST.get('shop_sec')
                acc_date = request.POST.get('updt_date')
                examcode = request.POST.get('exam_code')
            
                MG33new.objects.create(exam_date=str(examdate),result=str(remk),exam_code=str(examcode),shop_sec = str(shop_sec),name=str(epname), skill=str(skills),staff_no=str(stfno), updt_date =str(acc_date),prac_score= str(pscore),oral_score= str(orscore), total_marks = str(tscore),  sec_sup= str(sec_sup), trade_test_officer = str(trade_test_officer),  foreman= str(foreman), trade_test_admin= str(trade_test_admin), place_of_exam=str(place_exam))
        
            # print(updt_date, shop_sec, name, staff_no, ticketno, acc_Date, cause, reason_neg, reason_y_neg, equip_check, suggestions, bgc, bgc2, sec_sup, chargeman, mistry, c1, c2, c3, c4, a1, a2, a3, SSFO)

            messages.success(request, 'Successfully Saved !!!, Select new values to update')
    return render(request, "MG33view.html", context)

def mg33getstaffno(request):
    if request.method == "GET" and request.is_ajax():  
        from.models import Batch      
        shop_sec = request.GET.get('shop_sec')
        name=request.GET.get('name')
        desgn=request.GET.get('desgn')
        # print("ths is",shop_sec)
        w1=Shemp.objects.filter(shopsec=shop_sec,name=name, ).values('staff_no','desgn').distinct()

        wono = w1[0]['staff_no']
        cont ={
            "wono":wono,
        }
        # print("ths is",shop_sec)
        return JsonResponse({"cont":cont}, safe = False)

    return JsonResponse({"success":False}, status=400)


def mg33getexam(request):
    if request.method == "GET" and request.is_ajax():  
        examcode= request.GET.get('two')

        ex = exam_master.objects.filter(exam_code= examcode).all()    
     
        exam ={

            "exam_type":ex[0].exam_type,
            "exam_date":ex[0].exam_date,
            "prac_exam":ex[0].prac_desc,
            "oral_exam":ex[0].oral_desc,
        }
        
        return JsonResponse({"exam":exam}, safe = False)

    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/m26view/')
def m26view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    return render(request,'m26view.html',context)


@login_required
@role_required(urlpass='/m27view/')
def m27view(request):
    pa_no = empmast.objects.none()
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    mon="dd-mm-yyyy"
    stfrate="staff rate"
    stfname="staff name"
    stfdesg="staff designation"
    if "Superuser" in rolelist: 
        shop_sec_temp = request.POST.get('shop_sec')
        stfno_temp = request.POST.get('staffNo')
        getDateList = list(M21DOCNEW1.objects.filter(shop_sec=shop_sec_temp,staff_no=stfno_temp).values('date').exclude(date__isnull=True)) 
        print("getDateList : ",getDateList)
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
            'stfname': stfname,
            'stfdesg': stfdesg,
            'stfrate': stfrate,
            'getDateList':getDateList,
        }
    elif(len(rolelist)==1):
        # print("in else")
        for i in range(0,len(rolelist)):
            req = Oprn.objects.all().filter(shop_sec=rolelist[i]).values('part_no').distinct()
            pa_no =pa_no | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'pa_no':pa_no,
            'roles' :rolelist,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'getDateList':getDateList,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'getDateList':getDateList,
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            mon=request.POST.get('date1')
            shop_sec = request.POST.get('shop_sec')
            stfno = request.POST.get('staffNo')
            stfname = request.POST.get('staffName')
            stfdesg = request.POST.get('staffDesg')
            stfrate = request.POST.get('staffRate')
            wono=[]
            ex=list(Batch.objects.all().values('bo_no').exclude(bo_no__isnull=True).distinct())
            for i in ex:
                wono.append(i['bo_no'])
            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'sub': 1,
                        'mon':mon,
                        'stfno':stfno,
                        'shopsec': shop_sec,
                        'stfname': stfname,
                        'stfdesg': stfdesg,
                        'stfrate': stfrate,
                        'subnav':subnav,
                        'totindb':0,
                        'batch_no':wono,
                        'getDateList':getDateList,
                  }
            elif(len(rolelist)==1):
                  for i in range(0,len(rolelist)):
                        # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
                        # wo_nop =wo_nop | req

                        w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                        req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                        wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'sub': 1,
                        'mon':mon,
                        'stfno':stfno,
                        'shopsec': shop_sec,
                        'stfname': stfname,
                        'stfdesg': stfdesg,
                        'subnav':subnav,
                        'getDateList':getDateList,
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'sub': 1,
                        'mon':mon,
                        'stfno':stfno,
                        'shopsec': shop_sec,
                        'stfname': stfname,
                        'stfdesg': stfdesg,
                        'subnav':subnav,
                        'getDateList':getDateList,
                  }

        if submitvalue=='Save':
            date1=request.POST.get('date1')
            shop_sec=request.POST.get('shopsec')
            staffNo=request.POST.get('stfno')
            staffName=request.POST.get('stfname')
            staffDesg =request.POST.get('stfdesg')
            staffRate=request.POST.get('staffRate')
            tot = request.POST.get('total')
            print(tot)
            tot=int(tot)+1
            for i in range(1,int(tot)):    
                wono = request.POST.get("wono"+str(i))
                wodate = request.POST.get("wodate"+str(i))
                ofcdate = request.POST.get("ofcdate"+str(i))
                tothrs = request.POST.get("tothrs"+str(i))
                print(wono,wodate,ofcdate,tothrs)
                M27TimeSheet.objects.create(shop_sec=shop_sec, staff_no=staffNo, rate=staffRate, month=date1, tot_hrs=tothrs, ofc_date=ofcdate, wo_date=wodate, wo_no=wono, desg=staffDesg, name=staffName)
                print("data saved ",i)

            emp_detail= emp_details.objects.filter(empno='12136').values('email_id','mobileno')                  
            smsM18(emp_detail[0]['mobileno'],"Dear Employee thank you for summit Timesheet, for dates are : "+wodate)
            messages.success(request, 'Successfully Saved !')     
    return render(request,'m27view1.html',context)      




def m27getStaffNo(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        date = request.GET.get('date')
        print(shop_sec)
        staff_no = list(M5SHEMP.objects.filter(shopsec = shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m27getDetails(request):
    if request.method == "GET" and request.is_ajax():
        staffNo = request.GET.get('staffNo')        
        getdetail = list(M5SHEMP.objects.filter(staff_no = staffNo).values('name','desgn').exclude(name__isnull=True).distinct())
        return JsonResponse(getdetail, safe = False)
    return JsonResponse({"success":False}, status=400)


def m27getDesignation(request): 
    if request.method == "GET" and request.is_ajax():
        staffNo = request.GET.get('staffNo')    
        staffName = request.GET.get('staffName')      
        getdetaildesgn = list(M5SHEMP.objects.filter(staff_no = staffNo, name = staffName).values('desgn').exclude(staff_no__isnull=True).distinct())
        print("getdetaildesgn ---: ",getdetaildesgn)
        return JsonResponse(getdetaildesgn, safe = False)
    return JsonResponse({"success":False}, status=400)

def m27getWorkOrder(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        print(shop_sec)
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m27getWorkOrderDate(request):
    if request.method == "GET" and request.is_ajax():
        wono = request.GET.get('wo')
        wono1 = list(Batch.objects.filter(bo_no = wono).values('b_expl_dt').exclude(bo_no__isnull=True).exclude(b_expl_dt__isnull=True).distinct())
        print(wono1)
        return JsonResponse(wono1, safe = False)
    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(urlpass='/m18view/')
def m18view(request):
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
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Print/Save':
            print("data saved")            
            shopIncharge    = request.POST.get('shopIncharge')
            shop_sec        = request.POST.get('shop_sec')
            wo_no           = request.POST.get('wo_no')
            part_nop        = request.POST.get('part_nop')
            refNo           = request.POST.get('refNo')
            extraTimePartNo = request.POST.get('extraTimePartNo')
            reasonSpecialAllowance = request.POST.get('reasonSpecialAllowance')
            forSpecialAllowance    = request.POST.get('forSpecialAllowance')
            totalExtraTime        = request.POST.get('totalExtraTime')
            opno            = request.POST.get('opno')
            opdesc          = request.POST.get('opdesc')
            discription     = request.POST.get('discription')
            quantity        = request.POST.get('quantity')
            setExtraTime    = request.POST.get('setExtraTime')    
            setno           = request.POST.get('setno')  

            M18.objects.create(shopIncharge=str(shopIncharge),shop_sec=str(shop_sec),wo_no=str(wo_no),part_nop=str(part_nop), refNo=str(refNo), extraTimePartNo=str(extraTimePartNo), reasonSpecialAllowance=str(reasonSpecialAllowance), forSpecialAllowance=str(forSpecialAllowance), totalExtraTime=str(totalExtraTime),opno=str(opno),opdesc=str(opdesc), discription=str(discription), quantity=str(quantity), setExtraTime=str(setExtraTime), setno=str(setno), proReason=str(proReason))
            emp_detail= emp_details.objects.filter(empno='12136').values('email_id','mobileno')                  
            smsM18(emp_detail[0]['mobileno'],"Dear Employee Extra Time Card(M18) has been created. Your Ref No.- "+refNo+".")
            #email("erpdlw@gmail.com", "erpdlw@123", emp_detail[0]['email_id']," M20 Card Saved")
            messages.success(request, 'Successfully Saved ! Your ref No is :'+refNo) 

    return render(request,"m18view.html",context)


def m26getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(M5DOCnew.objects.all().filter(shop_sec=shop_sec).values('batch_no').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)


def m26getStaffCatWorkHrs(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        w_no     = request.GET.get('wno')
        date     = request.GET.get('date')
        print(date)
        if shop_sec and w_no and date:
            wono = list(M5SHEMP.objects.filter(shopsec=shop_sec,date__contains=date).values('staff_no','cat','total_time_taken').exclude(staff_no__isnull=True).exclude(total_time_taken__isnull=True).distinct('staff_no'))
        else:
            wono = "NO"
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)









@login_required
@role_required(urlpass='/m22view/')
def m22view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            wo_no1 = request.POST.get('wo_no1')
            staff_no = request.POST.get('staff_no')
            mon = request.POST.get('mon')
            mm=int(mon)
            month=calendar.month_name[mm]
            cy=int(date.today().year)
            cm=int(date.today().month)
            mtt = monthrange(cy, mm)[1]
            mt=int(mtt)
            # if mt  == 30:
            #     mt2 =14
            # elif mt == 31:
            #     mt2 = 15
            # elif mt == 28:
            #     mt2 = 12
            # else:
            #     mt2 = 13

            obj=Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('name').distinct()
            obj1=M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).values('datelw', 'datecc', 'daterw', 'briefdd').distinct()
            datel=len(obj)
            if len(obj1) == 0:
                obj1=range(0, 1)
            obj2=M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).values('no_hrs')[:mt+1]
            # obj5 = M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).values('no_hrs')[16:31]

            # print(obj2)
            # print(obj5)
            # print(len(obj5))
            obj3=[]
            # obj4=[]
            if len(obj2) == 0:
                for i in range(1, mt+1):
                    obj3.append(0)
                   # no_hrs = 'no_hrs' + str(i)
                   # obj3[no_hrs] = 0
                # for i in range(int((mt/2+1)+1), mt+1):
                #     obj4.append(0)
            else:
                    obj3=M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).values('no_hrs')[:mt+1]
                    # obj4=M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).values('no_hrs')[16:]
            # print(obj3)
            # print(obj4)
            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles': tmp,
                        'lenm': 2,
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'mt': range(1, mt+1),
                        'mtt': range(1, mt + 1),
                        # 'mmt': range(int((mt/2+1)+1), mt+1),
                        'mt1': mt,
                        # 'mt2': mt2,
                        'sub': 1,
                        'wo_no': wo_no,
                        'wo_no1': wo_no1,
                        'shop_sec':shop_sec,
                        'staff_no':staff_no,
                        'obj': obj,
                        'obj1': obj1,
                        'obj3':obj3,
                        # 'obj4':obj4,
                        'month': month,
                        'datel': datel,
                        'subnav':subnav
                  }
            elif(len(rolelist)==1):
                  for i in range(0,len(rolelist)):
                        # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
                        # wo_nop =wo_nop | req

                        w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                        req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                        wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'mt': range(1, mt+1),
                        'mtt': range(1, mt + 1),
                        # 'mmt': range(int((mt/2+1)+1), mt+1),
                        'mt1': mt,
                        # 'mt2': mt2,
                        'sub': 1,
                        'wo_no': wo_no,
                        'wo_no1': wo_no1,
                        'shop_sec': shop_sec,
                        'staff_no': staff_no,
                        'obj': obj,
                        'obj1': obj1,
                        'obj3': obj3,
                        # 'obj4': obj4,
                        'month': month,
                        'datel': datel,
                        'subnav':subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'mt': range(1, mt+1),
                        'mtt': range(1, mt + 1),
                        # 'mmt': range(int((mt/2+1)+1), mt+1),
                        'mt1': mt,
                        # 'mt2': mt2,
                        'sub': 1,
                        'wo_no': wo_no,
                        'wo_no1': wo_no1,
                        'shop_sec': shop_sec,
                        'staff_no': staff_no,
                        'obj': obj,
                        'obj1': obj1,
                        'obj3': obj3,
                        # 'obj4': obj4,
                        'datel': datel,
                        'month': month,
                        'subnav':subnav
                  }
        if submitvalue=='Save':
            leng=request.POST.get('mt1')
            # leng1=request.POST.get('mt2')
            print(leng)
            # print(leng1)
            datelw = request.POST.get('datelw')
            datecc = request.POST.get('datecc')
            daterw = request.POST.get('daterw')
            briefdd = request.POST.get('briefdd')
            shop_sec = request.POST.get('shop__sec')
            wo_no = request.POST.get('wo__no')
            wo_no1 = request.POST.get('wo__no1')
            staff_no = request.POST.get('staff__no')
            month = request.POST.get('month')
            print(month)
            print(shop_sec)
            print(wo_no)
            print(wo_no1)
            print(staff_no)
            print(datelw)
            print(datecc)
            print(daterw)
            print(briefdd)
            # print(staff_no)
            obj2 = M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).values('no_hrs').distinct()
            print(len(obj2))
            print(obj2)
            print(leng)
            # print(leng1)
            if len(obj2) == 0:
                for i in range(1, int(leng) + 1):
                    datee = request.POST.get('datee' + str(i))
                    print(datee)
                    # print(i)
                    M22.objects.create(datelw=str(datelw), datecc=str(datecc), daterw=str(daterw), briefdd=str(briefdd), no_hrs=str(datee), shop_sec=str(shop_sec), wo_no=str(wo_no), wo_no1=str(wo_no1), staff_no=str(staff_no), month=str(month))
                # for i in range(1, int(leng1) + 1):
                #
                #     datee1 = request.POST.get('datee1' + str(i))
                #     # print(datee1)
                #     print(i)
                #     M22.objects.create(datelw=str(datelw), datecc=str(datecc), daterw=str(daterw), briefdd=str(briefdd), no_hrs=str(datee1), shop_sec=str(shop_sec), wo_no=str(wo_no), wo_no1=str(wo_no1), staff_no=str(staff_no), month=str(month))

            if len(obj2) != 0:
                M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).delete()
                for i in range(1, int(leng) + 1):
                    # print("j")
                    # rr='1'
                    no_hrs=request.POST.get('datee' + str(i))
                    print(no_hrs)
                    M22.objects.create(datelw=str(datelw), datecc=str(datecc), daterw=str(daterw), briefdd=str(briefdd), no_hrs=str(no_hrs), shop_sec=str(shop_sec), wo_no=str(wo_no), wo_no1=str(wo_no1), staff_no=str(staff_no), month=str(month))
                    # M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).update(no_hrs=str(no_hrs), datelw=str(datelw), datecc=str(datecc), daterw=str(daterw), briefdd=str(briefdd))
                # for i in range(1, int(leng1) + 1):
                #     print("jj")
                #     datee1 = request.POST.get('datee1' + str(i))
                #     print(datee1)
                #     M22.objects.filter(shop_sec=shop_sec, staff_no=staff_no, month=month, wo_no=wo_no, wo_no1=wo_no1).update(no_hrs=str(datee1), datelw=str(datelw), datecc=str(datecc), daterw=str(daterw), briefdd=str(briefdd))


            wo_no=M22.objects.all().values('wo_no').distinct()
            messages.success(request, 'Successfully Updated!, Select new values to update')
    return render(request, "m22view.html", context)


def m22getwono(request):
    if request.method == "GET" and request.is_ajax():
        from.models import Batch

        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2=Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m22getstaff(request):
    if request.method == "GET" and request.is_ajax():
        # wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        staff_no = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)







@login_required
@role_required(urlpass='/m15view/')
def m15view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M13.objects.all().filter(shop=rolelist[i]).values('wo').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
        
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            print(request.user)
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            part_no = request.POST.get('part_no')
            obj = M13.objects.filter(shop=shop_sec,part_no=part_no,wo=wo_no).values('m13_no','rate','allocation').distinct()
            obj1 = Part.objects.filter(partno=part_no).values('des')
            obj2 = M15.objects.filter(shop=shop_sec,wo=wo_no,part_no=part_no).values('doc_no','c_d_no','unit','metric_ton_returned','qty_ret','metric_ton_received','qty_rec_inward','rupees','paise','allocation','rate','mat_ret_date','mat_rec_date','posted_date')
            noprint=0
            #obj2 = M2Doc.objects.filter(f_shopsec=shop_sec,part_no=part_no,batch_no=wo_no).values('m2sln').distinct()
            leng = obj.count()
            leng1 = obj1.count()
            leng2 = obj2.count()
            if len(obj2) == 0:
                noprint=1
            #leng2 = obj2.count()

            context = {
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'len': leng,
                        'len1':leng1,
                        'len2':leng2,
                        'shop_sec': shop_sec,
                        'wo_no': wo_no,
                        'part_no': part_no,
                        'noprint':noprint,
                        'sub' : 1,
                        'nav':nav,
                        'ip':get_client_ip(request),  
                        'subnav':subnav,
            }
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':0,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                    'noprint':noprint,
                    'sub' : 1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    req = M13.objects.all().filter(shop=rolelist[i]).values('wo').distinct()
                    wo_nop =wo_nop | req
                context = {
                    'sub':0,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                    'noprint':noprint,
                    'sub' : 1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
        
            elif(len(rolelist)>1):
                context = {
                    'sub':0,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                    'noprint':noprint,
                    'sub' : 1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
        if submitvalue =='Submit':
                #print("hi")
                leng=request.POST.get('len')
                #login_id = request.POST.get('login_id')
                #last_modified = request.POST.get('last_modified')
                shop_sec= request.POST.get('shop_sec')
                wo_no = request.POST.get('wo_no')
                part_no = request.POST.get('part_no')
                unit = request.POST.get('unit')
                allocation = request.POST.get('allocation')
                rate = request.POST.get('rate')
                rupees = request.POST.get('rupees')
                paise = request.POST.get('paise')
                mat_ret_date = request.POST.get('mat_ret_date')
                mat_rec_date = request.POST.get('mat_rec_date')
                m13_no = request.POST.get('m13_no')
                #m13_prtdt = request.POST.get('m13_prtdt')
                des = request.POST.get('des')
                posted_date = request.POST.get('posted_date')
                doc_no = request.POST.get('doc_no')
                c_d_no = request.POST.get('c_d_no')
                #date = request.POST.get('date')
                qty_ret = request.POST.get('qty_ret')
                qty_rec_inward = request.POST.get('qty_rec_inward')
                metric_ton_returned = request.POST.get('metric_ton_returned')
                metric_ton_received = request.POST.get('metric_ton_received')
                now = datetime.datetime.now()

                m15obj = M15.objects.filter(shop=shop_sec,wo=wo_no).distinct()
                if len(m15obj) == 0:
                    
                    M15.objects.create(login_id=request.user,shop=str(shop_sec),wo=str(wo_no),part_no=str(part_no),last_modified=str(now),unit=str(unit),allocation=str(allocation),rate=str(rate),rupees=str(rupees),paise=str(paise),mat_ret_date=str(mat_ret_date),
                    mat_rec_date=str(mat_rec_date),m13_no=str(m13_no),metric_ton_returned=str(metric_ton_returned),metric_ton_received=str(metric_ton_received),des=str(des),posted_date=str(posted_date),doc_no=str(doc_no),c_d_no=str(c_d_no),qty_ret=str(qty_ret),qty_rec_inward=str(qty_rec_inward))
                    
                

                else:
                    M15.objects.filter(shop=shop_sec,wo=wo_no,part_no=str(part_no)).update(unit=str(unit),allocation=str(allocation),rate=str(rate),rupees=str(rupees),paise=str(paise),mat_ret_date=str(mat_ret_date),
                    mat_rec_date=str(mat_rec_date),last_modified=str(now),login_id=request.user.username,posted_date=str(posted_date),metric_ton_returned=str(metric_ton_returned),metric_ton_received=str(metric_ton_received),m13_no=str(m13_no),des=str(des),doc_no=str(doc_no),c_d_no=str(c_d_no),qty_ret=str(qty_ret),qty_rec_inward=str(qty_rec_inward))
            
                wo_nop=M13.objects.all().values('wo').distinct()

    
 
    
    return render(request,"m15view.html",context)

def m15getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = list(M13.objects.filter(shop = shop_sec).values('wo').distinct())
        return JsonResponse(wo_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m15getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        part_no = list(M13.objects.filter(shop = shop_sec,wo=wo_no).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m18getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)    

def m18getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        part_no = list(M5DOCnew.objects.filter(batch_no =wo_no,shop_sec=shop_sec).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)    

def m18getoperation_no(request):
    if request.method == "GET" and request.is_ajax():
        part_nop = request.GET.get('part_nop')
        shop_sec = request.GET.get('shop_sec')
        #print(part_nop)
        #print(shop_sec)
        opnno = list(Oprn.objects.filter(part_no =part_nop,shop_sec=shop_sec).values('opn').exclude(part_no__isnull=True).distinct())
        #print(opnno)
        return JsonResponse(opnno, safe = False)
    return JsonResponse({"success":False}, status=400) 

def m18getoperation_desc(request):
    if request.method == "GET" and request.is_ajax():
        part_nop = request.GET.get('part_nop')
        shop_sec = request.GET.get('shop_sec')
        opno = request.GET.get('opno')
        print(part_nop)
        print(shop_sec)
        print(opno)
        opndesc = list(Oprn.objects.filter(part_no=part_nop,shop_sec=shop_sec,opn=opno).values('des').exclude(part_no__isnull=True).distinct())
        print(opndesc)
        return JsonResponse(opndesc, safe = False)
    return JsonResponse({"success":False}, status=400) 

def m18getRef_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        part_nop = request.GET.get('part_nop')
        refno = list(M5DOCnew.objects.filter(batch_no =wo_no,shop_sec=shop_sec,part_no =part_nop).values('m5glsn').exclude(part_no__isnull=True).distinct())
        return JsonResponse(refno, safe = False)
    return JsonResponse({"success":False}, status=400) 






@login_required
@role_required(urlpass='/m13view/')
def m13view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M13.objects.all().filter(shop=rolelist[i]).values('wo').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
        
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            part_no = request.POST.get('part_nop')
            obj = M13.objects.filter(shop=shop_sec,part_no=part_no,wo=wo_no).values('m13_no','qty_tot','qty_ins','qty_pas','qty_rej','opn','vendor_cd','fault_cd','reason','slno','m13_sn','wo_rep','m15_no','epc','rej_cat','job_no').distinct()
            obj1 = Part.objects.filter(partno=part_no).values('des','drgno').distinct()
            #obj2 = M2Doc.objects.filter(f_shopsec=shop_sec,part_no=part_no,batch_no=wo_no).values('m2sln').distinct()
            leng = obj.count()
            leng1 = obj1.count()
            #leng2 = obj2.count()
            # print(obj)
            # print(obj1)
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj': obj,
                    'obj1': obj1,
                    #'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    #'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    req = M13.objects.all().filter(shop=rolelist[i]).values('wo').distinct()
                    wo_nop =wo_nop | req
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    #'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    #'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                }
                
            elif(len(rolelist)>1):
                context = {
                    'sub': 1,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    #'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    #'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                }

        if submitvalue=='Save':
                slno= request.POST.get('slno')
                m13_sn = request.POST.get('m13_sn')
                epc = request.POST.get('epc')
                qty_tot = request.POST.get('qty_tot')
                qty_ins = request.POST.get('qty_ins')
                qty_pas = request.POST.get('qty_pas')
                qty_rej = request.POST.get('qty_rej')
                vendor_cd = request.POST.get('vendor_cd')
                opn = request.POST.get('opn')
                job_no = request.POST.get('job_no')
                fault_cd = request.POST.get('fault_cd')
                wo_rep = request.POST.get('wo_rep')
                m13no = request.POST.get('m13no')
                m15_no = request.POST.get('m15_no')
                rej_cat = request.POST.get('rej_cat')
                reason = request.POST.get('reason')
                print(reason)

                M13.objects.filter(m13_no=m13no).update(slno=slno,m13_sn=m13_sn,epc=epc,qty_tot=qty_tot,qty_ins=qty_ins,qty_pas=qty_pas,qty_rej=qty_rej,vendor_cd=vendor_cd,opn=opn,job_no=job_no,fault_cd=fault_cd,wo_rep=wo_rep,m13_no=m13no,m15_no=m15_no,rej_cat=rej_cat,reason=reason)

    return render(request,"m13view.html",context)

def m13getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = list(M13.objects.filter(shop = shop_sec).values('wo').distinct())
        return JsonResponse(wo_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m13getpano(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        part_no = list(M13.objects.filter(shop = shop_sec,wo=wo_no).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m13getno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        part_no = request.GET.get('part_nop')
        # print(wo_no)
        # print(shop_sec)
        # print(part_no)
        pp = list(M13.objects.filter(shop=shop_sec,part_no=part_no,wo=wo_no).values('m13_no').distinct())
        # print(pp)
        return JsonResponse(pp, safe = False)
    return JsonResponse({"success":False}, status=400)





def Childnode(request,part,res,code):
    arr=[]
    obj = Nstr.objects.filter(pp_part=part).filter(cp_part__isnull=False,ptc=code,l_to='9999').values('cp_part').distinct()
    for i in range(0,len(obj)):
        arr.append(obj[i]['cp_part'])
    for i in arr:   
        obj1=Nstr.objects.filter(pp_part=i,cp_part__isnull=False,ptc=code,l_to='9999').values('cp_part').distinct() 
      
        if len(obj1):
            for i in range(len(obj1)):
                if obj1[i]['cp_part'] not in arr:
                    arr.append(obj1[i]['cp_part'])
    print(arr)
    return arr

    





@login_required
@role_required(urlpass='/CardGeneration/')
def CardGeneration(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    #assmno = EpcCode.objects.all().values('num_1').distinct()
    assmno = Batch.objects.all().values('part_no').exclude(part_no__isnull=True).distinct().order_by('part_no')
    context = {
        'ip':get_client_ip(request),
        'nav':nav,
        'subnav':subnav,
        'assmno':assmno,
    }
    if request.method=="POST":
        batch = request.POST.get('batchno')
        bval=request.POST.get('cardbutton')
        asmno=request.POST.get('asslyno')
        card = request.POST.get('cardno')
        if batch and bval and asmno and card:
            if bval=="Generate Cards" and card=="M2":
                res = []
                first = []
                second = []
                third = []
                obj1 = Childnode(request,asmno,res,'M')
                print("obj1 :  = ",len(obj1),batch,bval,asmno,card)
                getShopSecDetails = list(Oprn.objects.filter(part_no=asmno).values('shop_sec').distinct())
                print(getShopSecDetails)
                for i in range(len(getShopSecDetails)):            
                    first.append(getShopSecDetails[i]['shop_sec'])  
                print(first)
                #getNstrDetails = list(Nstr.objects.filter(pp_part=asmno,ptc='M',l_to='9999').values('cp_part','ptc','qty','epc','del_fl','epc_old').exclude(pp_part__isnull=True).distinct())
                #for i in range(len(getNstrDetails)):            
                    #second.append(getNstrDetails[i]['cp_part'],getNstrDetails[i]['ptc'],getNstrDetails[i]['qty'],getNstrDetails[i]['epc'],getNstrDetails[i]['del_fl'],getNstrDetails[i]['epc_old'],)  

                #getBatchDetails = list(Batch.objects.filter(part_no=asmno,loco_to='9999').values('mark','status','brn_no'))
                #for i in range(len(getBatchDetails)):            
                    #third.append(getBatchDetails[i]['mark'],getBatchDetails[i]['status'],getBatchDetails[i]['brn_no'])  


                #for i in range(len(obj1)):
                    
                    # obj2=Tempexplsum.objects.filter(part_no=obj1[i]).values('qty','ptc','rm_partno','rm_qty','rm_ptc').distinct()
                    # obj3=Wgrptable.objects.filter(part_no=obj1[i]).values('scl_cl','f_shopsec','rc_st_wk','cut_shear','seq','brn_no','del_fl','version','status','epc','mark').distinct()
                    # epcold=Code.objects.filter(num_1=asmno).values('epc_old').distinct()
                    #  obj2=M2Doc.objects.filter(part_no=obj1[i]).values('qty','ptc','rm_partno','rm_qty','rm_ptc','scl_cl','f_shopsec','rc_st_wk','cut_shear','seq','brn_no','del_fl','version','status','epc','mark','epc_old').distinct()
                    #  if len(obj2):
                     #   print("len1----",len(obj2))  
                        #print("tset ----------",len(obj2))
                    #print(i)
                    #M2Docnew1.objects.create(part_no=obj1[i],assly_no=asmno,ptc='M',batch_no=batch)

                # try:
                #     for j in range(len(obj1)):
                #         cstr_buffer.objects.create(pp_part=asmno,cp_part=obj1[j])
                #     messages.success(request, 'Successfully Done!')
                # except:
                #     messages.error(request,'Some Error Occurred')
            elif bval=="Generate Cards" and card=="M4":
                res = []
                obj1 = ShowLeaf(request,asmno,res,'R')
                print("len = ",obj1)
                for i in range(len(obj1)):
                    # obj2=Tempexplsum.objects.filter(part_no=obj1[i]).values('qty','ptc','rm_partno','rm_qty','rm_ptc').distinct()
                    # obj3=Wgrptable.objects.filter(part_no=obj1[i]).values('scl_cl','f_shopsec','rc_st_wk','cut_shear','seq','brn_no','del_fl','version','status','epc','mark').distinct()
                    # epcold=Code.objects.filter(num_1=asmno).values('epc_old').distinct()
                    # obj2=M2Doc.objects.filter(part_no=obj1[i]).values('qty','ptc','rm_partno','rm_qty','rm_ptc','scl_cl','f_shopsec','rc_st_wk','cut_shear','seq','brn_no','del_fl','version','status','epc','mark','epc_old').distinct()
                    # if len(obj2):
                    #     print(obj2[0])
                    print(i)
                    M14M4new1.objects.create(part_no=obj1[i],assly_no=asmno,ptc='R',batch_no=batch)
                # try:
                #     for j in range(len(obj1)):
                #         cstr_buffer.objects.create(pp_part=asmno,cp_part=obj1[j])
                #     messages.success(request, 'Successfully Done!')
                # except:
                #     messages.error(request,'Some Error Occurred')
            elif bval=="Generate Cards" and card=="M5":
                res = []
                obj1 = ShowLeaf(request,asmno,res,'M')
                print("len = ",obj1)
                for i in range(len(obj1)):
                    # obj2=Tempexplsum.objects.filter(part_no=obj1[i]).values('qty','ptc','rm_partno','rm_qty','rm_ptc').distinct()
                    # obj3=Wgrptable.objects.filter(part_no=obj1[i]).values('scl_cl','f_shopsec','rc_st_wk','cut_shear','seq','brn_no','del_fl','version','status','epc','mark').distinct()
                    # epcold=Code.objects.filter(num_1=asmno).values('epc_old').distinct()
                    # obj2=M2Doc.objects.filter(part_no=obj1[i]).values('qty','ptc','rm_partno','rm_qty','rm_ptc','scl_cl','f_shopsec','rc_st_wk','cut_shear','seq','brn_no','del_fl','version','status','epc','mark','epc_old').distinct()
                    # if len(obj2):
                    #     print(obj2[0])
                    print(i)
                    M5Docnew1.objects.create(part_no=obj1[i],assly_no=asmno,ptc='M',batch_no=batch)
                # try:
                #     for j in range(len(obj1)):
                #         cstr_buffer.objects.create(pp_part=asmno,cp_part=obj1[j])
                #     messages.success(request, 'Successfully Done!')
                # except:
                #     messages.error(request,'Some Error Occurred')
            elif bval=="Generate Cards" and card=="M14":
                res = []
                obj1 = ShowLeaf(request,asmno,res,'P')
                print("len = ",obj1)
                for i in range(len(obj1)):
                    # obj2=Tempexplsum.objects.filter(part_no=obj1[i]).values('qty','ptc','rm_partno','rm_qty','rm_ptc').distinct()
                    # obj3=Wgrptable.objects.filter(part_no=obj1[i]).values('scl_cl','f_shopsec','rc_st_wk','cut_shear','seq','brn_no','del_fl','version','status','epc','mark').distinct()
                    # epcold=Code.objects.filter(num_1=asmno).values('epc_old').distinct()
                    # obj2=M2Doc.objects.filter(part_no=obj1[i]).values('qty','ptc','rm_partno','rm_qty','rm_ptc','scl_cl','f_shopsec','rc_st_wk','cut_shear','seq','brn_no','del_fl','version','status','epc','mark','epc_old').distinct()
                    # if len(obj2):
                    #     print(obj2[0])
                    print(i)
                    M14M4new1.objects.create(part_no=obj1[i],assly_no=asmno,ptc='P',batch_no=batch)
                # try:
                #     for j in range(len(obj1)):
                #         cstr_buffer.objects.create(pp_part=asmno,cp_part=obj1[j])
                #     messages.success(request, 'Successfully Done!')
                # except:
                #     messages.error(request,'Some Error Occurred')
            else:
                messages.error(request,'Enter all values!')
    return render(request,'CardGeneration.html',context)


def m27getBatchNo(request):
    if request.method == "GET" and request.is_ajax():
        mAsslyno = request.GET.get('mAsslyno')
        bo_no=Batch.objects.filter(part_no=mAsslyno).values('bo_no').distinct()
        bo_no_temp = list(bo_no)
        return JsonResponse(bo_no_temp, safe = False)
    return JsonResponse({"success": False}, status=400)


def smsM18(phoneno,message):
    url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to=91"+str(phoneno)+"&msg="+message+" &msg_type=TEXT&userid=2000184632&auth_scheme=plain&password=pWK3H5&v=1.1&format=text"
    
    print("Message ---->>",message)
    response = requests.request("POST", url)
    print(response.text)

def email(sender_email_id,sender_email_id_password,receiver_email_id,message):
    print(sender_email_id)
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls()
    s.login(sender_email_id,sender_email_id_password)  
    s.sendmail(sender_email_id,receiver_email_id, message) 
    s.quit()
	


@login_required
@role_required(urlpass='/mg7view/')
def mg7view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').exclude(batch_no__isnull=True).distinct()
            wo_nop =wo_nop | req



        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            shop_sec1 = request.POST.get('shop_sec1')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            m5no = request.POST.get('job_no')
            # print(m5no)
            obj = Part.objects.filter(partno=part_no).values('des').distinct()
            obj1 = M5DOCnew.objects.filter(batch_no=wo_no, pr_shopsec=shop_sec, n_shopsec=shop_sec1, part_no=part_no).values('m5glsn').distinct()
            obj2 = M13.objects.filter(shop=shop_sec, part_no=part_no, wo=wo_no).values('m13_no').distinct()
            if len(obj2) > 0:
                obj2 = M13.objects.filter(shop=shop_sec, part_no=part_no, wo=wo_no).values('m13_no').distinct()[:1]
            date=len(obj2)
            # print(obj2)
            obj3 = MG7.objects.filter(wo_no=wo_no, fromshop=shop_sec, toshop=shop_sec1, part_no=part_no, m5glsn=m5no).values('date','qty_ord','qty_rej','qty_req','reason').distinct()
            print(obj3)
            if len(obj3) == 0:
                obj3=range(0, 1)


            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,


                        'sub': 1,

                        'date': date,

                        'shop_sec': shop_sec,
                        'shop_sec1': shop_sec1,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'm5no': m5no,

                        'subnav':subnav
                  }
            elif(len(rolelist)==1):
                  for i in range(0,len(rolelist)):
                      req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').exclude(batch_no__isnull=True).distinct()
                      wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,

                        'date': date,

                        'shop_sec': shop_sec,
                        'shop_sec1': shop_sec1,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'm5no': m5no,
                        'subnav':subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,

                        'sub': 1,

                        'date': date,

                        'shop_sec': shop_sec,
                        'shop_sec1': shop_sec1,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'm5no': m5no,

                        'subnav':subnav
                  }

        if submitvalue=='Save':

                shop_sec= request.POST.get('shop_sec11')
                shop_sec1 = request.POST.get('shop_sec12')
                part_no= request.POST.get('part_no1')
                wo_no = request.POST.get('wo_no1')
                m5no = request.POST.get('m5no11')
                des = request.POST.get('des1')
                m13_no = request.POST.get('m13_no11')
                print(wo_no)
                print(shop_sec)
                print(part_no)
                print(shop_sec1)
                print(m5no)
                print(m13_no)
                qty_ord =request.POST.get('qty_ord')
                qty_req = request.POST.get('qty_req')
                qty_rej = request.POST.get('qty_rej')
                date = request.POST.get('date')
                reason =request.POST.get('reason')

                obj4 = MG7.objects.filter(wo_no=wo_no, fromshop=shop_sec, toshop=shop_sec1, part_no=part_no, m5glsn=m5no).distinct()
                print(len(obj4))
                if len(obj4) == 0:
                    MG7.objects.create(wo_no=str(wo_no), m13_no=str(m13_no), des=str(des), fromshop=str(shop_sec), toshop=str(shop_sec1), part_no=str(part_no), m5glsn=str(m5no), qty_ord=int(qty_ord),qty_req=int(qty_req),qty_rej=int(qty_rej),date=str(date),reason=str(reason))

                else:
                    MG7.objects.filter(wo_no=wo_no, fromshop=shop_sec, toshop=shop_sec1, part_no=part_no, m5glsn=m5no).update(qty_ord=int(qty_ord), qty_req=int(qty_req), qty_rej=int(qty_rej), date=str(date), reason=str(reason))

                wo_no=MG7.objects.all().values('wo_no').distinct()
                messages.success(request, 'Successfully Done!, Select new values to proceed')
    return render(request, "mg7view.html", context)



def mg7getshop(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')
        shop = M5DOCnew.objects.filter(pr_shopsec=shop_sec).values('n_shopsec').exclude(n_shopsec__isnull=True).distinct()
        shop_sec1 = list(shop)
        return JsonResponse(shop_sec1, safe=False)
    return JsonResponse({"success": False}, status=400)

def mg7getjob(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')
        wo_no = request.GET.get('wo_no')
        shop_sec1 = request.GET.get('shop_sec1')
        part_nop = request.GET.get('part_nop')
        # print(wo_no)
        # print(part_nop)
        job = M5DOCnew.objects.filter(pr_shopsec=shop_sec, n_shopsec=shop_sec1, batch_no=wo_no,  part_no=part_nop).values('m5glsn').distinct()
        jobno = list(job)
        # print(job)
        return JsonResponse(jobno, safe=False)
    return JsonResponse({"success": False}, status=400)

def mg7getwono(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')
        shop_sec1 = request.GET.get('shop_sec1')
        wo = M5DOCnew.objects.filter(pr_shopsec=shop_sec, n_shopsec=shop_sec1).values('batch_no').exclude(batch_no__isnull=True).distinct()
        wono = list(wo)
        return JsonResponse(wono, safe=False)
    return JsonResponse({"success": False}, status=400)




def mg7getpartno(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        # print(wo_no)
        shop_sec1 = request.GET.get('shop_sec1')
        pa = M5DOCnew.objects.filter(pr_shopsec=shop_sec,n_shopsec=shop_sec1, batch_no=wo_no).values('part_no').exclude(part_no__isnull=True).distinct()
        part_no = list(pa)
        return JsonResponse(part_no, safe=False)
    return JsonResponse({"success": False}, status=400)







@login_required
@role_required(urlpass='/m23view/')
def m23view(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    print("kj",usermaster)
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)

    wo_nop = empmast.objects.none()
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            w1 = M5SHEMP.objects.filter(shopsec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            from datetime import date
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            ddate = request.POST.get('ddate')
            obj1 =  M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name').distinct()
            # obj2=m23doc.objects.filter(emp_no=staff_no,shop_no=shop_sec).values('date','purpose','from_time','to_time')[0]
            noprint=0
            tod = date.today()
            # current_date=date.today()
            # print(current_date)
            # if len(obj2) == 0:
            #     obj2=range(1,2)
            #     noprint=1
           # obj2 = Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name','cat').distinct()
            # leng = obj1.count()
            # print(obj2)
            #leng2 = obj2.count()
           # print(obj1,"obj1")
            #print(obj2,"obj2")
            context = {
                'obj1': obj1,
                # 'obj2': obj2,
                'ran':range(1,32),
                'len': 31,
                #'len2': leng2,
                'shop_sec': shop_sec,
                 'noprint':noprint,
                #'wo_no': wo_no,
                'staff_no': staff_no,
                #'part_no': part_no, 
                #'mon': mon,
                'curdate':tod,
                'sub':1,
                'nav':nav,
                'ddate': ddate,
                'ip':get_client_ip(request),  
                'subnav':subnav,     
            }
        if submitvalue =='Save':
                    leng=request.POST.get('len')
                    print("HH")
                    
                    from_time = request.POST.get('from_time')
                    to_time = request.POST.get('to_time')
                    purpose = request.POST.get('pur')
                    shops=request.POST.get('shopsec')
                    staffn=request.POST.get('staffno')
                    date=request.POST.get('dddate')
                    name=request.POST.get('employeename')
                    print(date)
                    now = time.localtime()
                    current_time = time.strftime("%H:%M:%S",now)
                    if to_time > from_time and from_time > current_time or from_time == current_time  :
                        m23obj1 = m23doc.objects.filter(shop_no=shops,emp_no=staffn, date=date).values('to_time')
                        if len(m23obj1)>0 :
                            if (m23obj1[0]['to_time'] <= str(from_time) and str(from_time) <= str(to_time) ) :
                                 m23doc.objects.create(shop_no=str(shops),emp_no=str(staffn),emp_name=str(name), from_time=str(from_time), to_time=str(to_time), purpose=str(purpose), date=str(date))
                                 messages.success(request,'New gate pass created')
                            else :
                                 messages.success(request,'From-time and to-time of new gate pass should be greater than issued time of previous gate pass')
                        else:
                           m23doc.objects.create(shop_no=str(shops),emp_no=str(staffn),emp_name=str(name), from_time=str(from_time), to_time=str(to_time), purpose=str(purpose), date=str(date))
                           messages.success(request,'First gate pass created')
                    else :
                        messages.success(request,'To_time should be greater than From_time  and from time should be greater than current time')
                        
        if submitvalue=='Generate report':
            return m23report(request)
    # else :
    #     return m23report(request)
    
    return render(request,"m23view.html",context)
                        

def m23getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        #wo_no = request.GET.get('wo_no')
        staff_no=list(M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def getm23date(request):
    from .models import m23doc
    if request.method == "GET" and request.is_ajax():
        shopsec = request.GET.get('shpsec')
        stfno=request.GET.get('stfno')
        cdate=request.GET.get('insertdate')
        print("in ajax")
        #wo_no = request.GET.get('wo_no')
        cddate=list(m23doc.objects.filter(shop_no=shopsec,emp_no=stfno).values('date').order_by('-id'))
        print("list")
        print(cddate)
        return JsonResponse(cddate, safe = False)
    return JsonResponse({"success":False}, status=400)
  
@login_required
#@role_required(allowed_roles=["Superuser"])
def m23report(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    # print("kj",usermaster)
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)

    # wo_nop = empmast.objects.none()
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            w1 = M5SHEMP.objects.filter(shopsec=rolelist[i]).values('empno').distinct()
            # req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            # wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            # 'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            ddate = request.POST.get('ddate')
            print(shop_sec,staff_no,ddate)
            # obj1 =  M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name').distinct()
            obj1 = m23doc.objects.filter(shop_no=shop_sec,emp_no=staff_no,date=ddate).values('purpose','from_time','to_time').distinct()
            obj2 = m23doc.objects.filter(shop_no=shop_sec,emp_no=staff_no,date=ddate).values('emp_name').distinct()
            leng = obj1.count()
            print("obj1",obj1)
            context = {
                'obj1': obj1,
                'obj2': obj2,
                'ran':range(1,32),
                'len': 31,
                #'len2': leng2,
                'shop_sec': shop_sec,
                #'wo_no': wo_no,
                'staff_no': staff_no,
                #'part_no': part_no, 
                #'mon': mon,
                'sub':1,
                'nav':nav,
                'ip':get_client_ip(request),  
                'subnav':subnav,  
                'date': ddate,   
            }
        if submitvalue =='Submit':
                leng=request.POST.get('len')
                shop_sec= request.POST.get('s_spass')
                staff_no = request.POST.get('s_fpass')
            
                m23obj = M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).distinct()
                print(m23obj)
                if((m23obj)):
                    m23obj.delete()
                
                # for i in range(1, int(leng)+1):
                from_time = request.POST.get('from_time')
                to_time = request.POST.get('to_time')
                purpose = request.POST.get('pur')
                shops=request.POST.get('shopsec')
                staffn=request.POST.get('staffno')
  
                # reasons_for_idle_time = request.POST.get('reasons_for_idle_time'+str(i))
                    #print(shopsec)
                    # objjj=M7.objects.create(shop_sec=shop_sec,staff_no=staff_no,part_no=part_no,in1=in1,out=out,month=mon,date=date)
                if from_time and to_time and purpose :
                    print("jj")
                    objjj=m23doc.objects.create()
                    objjj.shop_no=shops
                    objjj.emp_no=staffn
                    objjj.emp_name=request.POST.get('employeename')
                    objjj.from_time=from_time
                    objjj.to_time=to_time
                    objjj.purpose=purpose
                    objjj.save()
                    #print(in1)
                    #print(date)
                    
                wo_nop=M5SHEMP.objects.all().values('staff_no').distinct()
 

    return render(request,"m23report.html",context)







@login_required
@role_required(urlpass='/bogieassembly/')
def bogieassembly_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    obj2=BogieAssembly.objects.all().filter(dispatch_status=False).order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=BogieAssembly.objects.filter(dispatch_status=False).values('sno')
    myaxle=AxleMachining.objects.all().values('axle_no')
    mytm=PinionPressing.objects.all().values('tm_no')
    mymsu=AxleWheelPressing.objects.all().values('msu_unit_no')
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mysno':mysno,
       'myaxle':myaxle,
       'mytm':mytm,
        'mymsu':mymsu,
    }

    if request.method=="POST":

        once=request.POST.get('once')
        print(once)
        submit=request.POST.get('submit')

        if submit=='Save':
            bo_no=request.POST.get('bo_no')
            bo_date=request.POST.get('bo_date')
            date=request.POST.get('date')
            pt_no=request.POST.get('pt_no')
            bo_qty=request.POST.get('bo_qty')
            loco_type=request.POST.get('locos')
            in_date=request.POST.get('in_date')
            outdate=request.POST.get('out_qty')
            frameserial_no=request.POST.get('frameserial_no')
            frame_make=request.POST.get('frame_make')
            frame_type=request.POST.get('frame_type')
            print(bo_no,bo_date,date,loco_type,in_date,frame_make,frame_type,frameserial_no)
            

            if bo_no and bo_date and date and loco_type and frameserial_no and frame_make and frame_type and in_date and outdate and bo_qty and pt_no:
               obj=BogieAssembly.objects.create()
               obj.bo_no=bo_no
               obj.bo_date=bo_date
               obj.pt_no=pt_no
               obj.bo_qty=bo_qty
               obj.date=date
               obj.loco_type=loco_type
               obj.in_date=in_date
               obj.out_qty=outdate
               obj.frame_make=frame_make
               obj.frame_type=frame_type
               obj.frameserial_no=frameserial_no
               obj.inspection_status=False
               obj.save()
               messages.success(request, 'Successfully Added!')
            else:
               messages.error(request,"Please Enter All Records!") 

            obj2=BogieAssembly.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            'mybo':mybo,
            'mysno':mysno,
            }

        if submit=='Edit':
            temp=request.POST.get('editsno')
            if temp is not None:
                sno=int(temp)
            else:
                sno=None
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            in_date=request.POST.get('editin_date')
            outdate=request.POST.get('editout_date')
            frameserial_no=request.POST.get('editframeserial_no')
            frame_make=request.POST.get('editframe_make')
            frame_type=request.POST.get('editframe_type')
            bo_qty=request.POST.get('editbo_qty')
            pt_no=request.POST.get('editpt_no')
            print(bo_no,bo_date,date,loco_type,in_date,frame_make,frame_type,frameserial_no)
        
            if bo_no and bo_date and date and loco_type and frameserial_no and frame_make and frame_type and in_date and outdate and pt_no and bo_qty:
               BogieAssembly.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,frameserial_no=frameserial_no,frame_make=frame_make,frame_type=frame_type,in_date=in_date,out_qty=outdate,pt_no=pt_no,bo_qty=bo_qty)
               messages.success(request, 'Successfully Edited!')
            else:
               messages.error(request,"Please Enter S.No.!")

            my_context={
            'object':obj2,
            'mybo':mybo,
            'mysno':mysno,
            }

        if submit=="Dispatch":
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            disdate=request.POST.get('dispatch_date')
            if sno and dislocos and disdate:
                BogieAssembly.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_status=True,dispatch_date=disdate)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")

        if submit=='InspectHHP':
            sno=int(request.POST.get('sno'))
            print(sno)
            axle_no=request.POST.get('axle_no')
            axle_location=request.POST.get('axle_location')
            gear_case_no=request.POST.get('gear_case_no')
            tm_no=request.POST.get('tm_no')
            gear_case_make=request.POST.get('gear_case_make')
            msu_unit_no=request.POST.get('msu_unit_no')
            break_rigging_make=request.POST.get('break_rigging_make')
            coil_spring_make=request.POST.get('coil_spring_make')
            sand_box_make=request.POST.get('sand_box_make')
            spheri_block_make=request.POST.get('spheri_block_make')
            elastic_shop_make=request.POST.get('elastic_shop_make')
            secondary_coil_make=request.POST.get('secondary_coil_make')
            thrust_pad_make=request.POST.get('thrust_pad_make')
            break_cylinder_make=request.POST.get('break_cylinder_make')
            lateral_damper=request.POST.get('lateral_damper')
            if axle_no and axle_location and gear_case_no and tm_no and gear_case_make and msu_unit_no and break_rigging_make and coil_spring_make and sand_box_make and spheri_block_make and elastic_shop_make and secondary_coil_make and thrust_pad_make and break_cylinder_make and lateral_damper :
                BogieAssembly.objects.filter(sno=sno).update(axle_no=axle_no,axle_location=axle_location,gear_case_no=gear_case_no,traction_motor_no=tm_no,gear_case_make=gear_case_make,msu_unit_no=msu_unit_no,break_rigging_make=break_rigging_make,coil_spring_make=coil_spring_make,sand_box_make=sand_box_make,spheri_block_make=spheri_block_make,elastic_shop_make=elastic_shop_make,secondary_coil_make=secondary_coil_make,thrust_pad_make=thrust_pad_make,break_cylinder_make=break_cylinder_make,lateral_damper=lateral_damper) 
                messages.success(request,'Successfully Inspected!')
            else:
                messages.error(request,"Please Enter All Records!")

        if submit=='Inspect':
            sno=int(request.POST.get('sno'))
            print(sno)
            axle_no=request.POST.get('axle_no')
            axle_location=request.POST.get('axle_location')
            gear_case_no=request.POST.get('gear_case_no')
            tm_no=request.POST.get('tm_no')
            gear_case_make=request.POST.get('gear_case_make')
            msu_unit_no=request.POST.get('msu_unit_no')
            break_rigging_make=request.POST.get('break_rigging_make')
            coil_spring_make=request.POST.get('coil_spring_make')
            sand_box_make=request.POST.get('sand_box_make')
            spheri_block_make=request.POST.get('spheri_block_make')
            elastic_shop_make=request.POST.get('elastic_shop_make')
            horizontal_damper=request.POST.get('horizontal_damper')
            # secondary_coil_make=request.POST.get('secondary_coil_make')
            # thrust_pad_make=request.POST.get('thrust_pad_make')
            # break_cylinder_make=request.POST.get('break_cylinder_make')
            # lateral_damper=request.POST.get('lateral_damper')
            if axle_no and axle_location and gear_case_no and tm_no and gear_case_make and msu_unit_no and break_rigging_make and coil_spring_make and sand_box_make and spheri_block_make and elastic_shop_make and horizontal_damper:
                BogieAssembly.objects.filter(sno=sno).update(axle_no=axle_no,axle_location=axle_location,gear_case_no=gear_case_no,traction_motor_no=tm_no,gear_case_make=gear_case_make,msu_unit_no=msu_unit_no,break_rigging_make=break_rigging_make,coil_spring_make=coil_spring_make,sand_box_make=sand_box_make,spheri_block_make=spheri_block_make,elastic_shop_make=elastic_shop_make,horizontal_damper=horizontal_damper) 
                messages.success(request,'Successfully Inspected!')
            else:
                messages.error(request,"Please Enter All Records!")

        if submit=='Delete':

            sno=int(request.POST.get('delsno'))
            if sno:
                myval=list(BogieAssembly.objects.filter(sno=sno))
                print(myval) 
                BogieAssembly.objects.filter(sno=sno).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")
        

        
        return HttpResponseRedirect("/bogieassembly/")

    return render(request,"bogieassembly.html",my_context)

def bogieassemb_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        # print(mybo)
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def bogieassemb_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(BogieAssembly.objects.filter(sno=mysno).values('bo_no','bo_date','pt_no','bo_qty','loco_type','date','frameserial_no','frame_make','frame_type','in_date','out_qty'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/homeadmin/')
def mg22report(request):
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
    dictemper={}
    totindb=0
    emp=[]
    empname = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname')
    if empname is not None and len(empname):
        for i in range(len(empname)):
            emp.append(empname[i]['empname'])

    w1=M5SHEMP.objects.all().values('name').distinct().exclude(name__isnull=True)
    wono=[]
    for w in range(len(w1)):
        wono.append(w1[w]['name'])
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'names':wono,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'lvdate':"yyyy-mm-dd",
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"yyyy-mm-dd",
            'names':wono,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"yyyy-mm-dd",
            'names':wono,
        }
    if request.method=="POST":
        bvalue=request.POST.get('proceed')
        shop_sec=request.POST.get('shop_sec')
        lvdate=request.POST.get('updt_date')
        empname=request.POST.get('emp_name')
        accdate=request.POST.get('accdate')
        if bvalue=='Proceed':
            m2=MG22new.objects.filter(shop_sec=shop_sec,updt_date=lvdate,name=empname,acc_Date=accdate).first()
            nocertf=0
            mm=0
            # print(m2)
            if m2 is not None:
                if m2.c1 or m2.c2 or m2.c3 or m2.c4 is not None:
                    nocertf=1
                temper = {str(mm):{"name":m2.name,
                                               "ticketno":m2.ticketno,"cause":m2.cause,"bgc2":m2.bgc2,
                        "acdate":m2.acc_Date,"superv":m2.sec_sup,"mistry":m2.mistry,"chargeman":m2.chargeman,"ssfoname":m2.ssfo,
                        "reasonneg":m2.reason_neg,"epchck":m2.equip_check,"sugg":m2.suggestions,
                        "cert1":m2.c1,"cert2":m2.c2,"cert3":m2.c3,"cert4":m2.c4,"firstacc":m2.bgc,
                        "anex1":m2.a1,"anex2":m2.a2,"anex3":m2.a3,
                                               }}
                           
                totindb=1
                dictemper.update(copy.deepcopy(temper))
                # print("dictionary")
                # print(dictemper)
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'names':wono,
                    'dictemper':dictemper,
                    'totindb':totindb,
                    'empname':emp,
                    "nocertf":nocertf,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
                    req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'sub':1,
                    'subnav':subnav,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                    "nocertf":nocertf,
                    'dictemper':dictemper,
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                    "nocertf":nocertf,
                    'dictemper':dictemper,
                }

    return render(request,"mg22report.html",context)





@login_required
@role_required(urlpass='/MG22view/')
def MG22view(request):
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
    dictemper={}
    totindb=0
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'lvdate':"dd-mm-yy",
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"dd-mm-yy",
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"dd-mm-yy",
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Add':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            # staffno=request.POST.get('staff_no')
            lvdate=request.POST.get('updt_date')
            m2=MG22new.objects.filter(shop_sec=shop_sec,updt_date=lvdate).last()
            mm=0
            if m2 is not None:
                temper = {str(mm):{"name":m2.name,
                                               "ticketno":m2.ticketno,"cause":m2.cause,
                        "acdate":m2.acc_Date,"superv":m2.sec_sup,"mistry":m2.mistry,"chargeman":m2.chargeman,
                                               }}
                           
                totindb=totindb+1

                dictemper.update(copy.deepcopy(temper))
                print(dictemper)

            emp=[]
            staff_name = request.GET.get('empname')
            print(staff_name)
            empname = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname')
            if empname is not None and len(empname):
                for i in range(len(empname)):
                    emp.append(empname[i]['empname'])
            # print(emp)

            w1=M5SHEMP.objects.filter(shopsec=shop_sec).values('name').distinct()
            # print("w1",w1)
            wono=[]
            for w in range(len(w1)):
                wono.append(w1[w]['name'])
            alt_date="mm-dd-yy"
            # if obj1 is not None:
            #     ename=obj1[0].name
            #     alt_date=obj1[0].alt_date
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'names':wono,
                    'dictemper':dictemper,
                    'totindb':totindb,
                    'empname':emp,
                    # 'obj1':obj1,
                    # 'empname':ename,
                    # 'ticketno':staffno,
                    'alt_date':alt_date,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
                    req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'sub':1,
                    'subnav':subnav,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                    # 'ticket':wono[0]['staff_no'],
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                    # 'ticket':wono[0]['staff_no'],
                }
        
        # if submitvalue=='Save':
        #     print("data saved")
        #     shop_sec= request.POST.get('shop_sec')
        #     # staff_no=request.POST.get('stffno')
        #     lv_date= request.POST.get('lv_date')
        #     tot=0
        #     tot=request.POST.get('totmebs')
            
            
        #     totindb=request.POST.get('totindb')
        #     for tb in range(1,int(totindb)+1):
        #         namedb=request.POST.get('namedb'+str(tb))
        #         ticketnodb=request.POST.get('ticketnodb'+str(tb))
        #         datedb=request.POST.get('datedb'+str(tb))
        #         print("Dateindb"+str(tb),datedb)
        #         M20new.objects.filter(shop_sec=str(shop_sec),staff_no=str(ticketnodb), lv_date=str(lv_date) ).update(alt_date=str(datedb))
                
            
            
            
        #     for t in range(1,int(tot)+1):
        #         name=request.POST.get('name'+str(t))
        #         ticketno=request.POST.get('ticket'+str(t))
        #         date=request.POST.get('date'+str(t))
        #         M20new.objects.create(shop_sec=str(shop_sec),staff_no=str(ticketno), lv_date=str(lv_date), name=str(name), ticketno=str(ticketno), alt_date=str(date))
        #         print(shop_sec,lv_date,name,ticketno,date)
                
            
            # name=request.POST.get('empname')
            # ticketno = request.POST.get('stffno')
            # alt_date = request.POST.get('alt_date')

        
            # print("data saved")
            # shop_sec= request.POST.get('shop_sec')
            # # staff_no=request.POST.get('stffno')
            # lv_date= request.POST.get('lv_date')
            # tot=0
            # tot=request.POST.get('totmebs')
            
            # totindb=request.POST.get('totindb')
            # for tb in range(1,int(totindb)+1):
            #     namedb=request.POST.get('namedb'+str(tb))
            #     ticketnodb=request.POST.get('ticketnodb'+str(tb))
            #     datedb=request.POST.get('datedb'+str(tb))
            #     print("Dateindb"+str(tb),datedb)
            #     M20new.objects.filter(shop_sec=str(shop_sec),staff_no=str(ticketnodb), lv_date=str(lv_date) ).update(alt_date=str(datedb))
                
            # for t in range(1,int(tot)+1):
        if submitvalue=='Save':
            print("data saved")
             
            updt_date = request.POST.get('updt_date')
            shop_sec = request.POST.get('shop_sec')
            name=request.POST.get('name1')
            staff_no = request.POST.get('staff_no')
            ticketno = request.POST.get('ticket')
            acc_Date = request.POST.get('datename')
            cause = request.POST.get('cause')
            reason_neg = request.POST.get('reason_neg')
            reason_y_neg = request.POST.get('reason_y_neg')
            equip_check = request.POST.get('equip_check')
            suggestions = request.POST.get('suggestion')
            bgc = request.POST.get('bgc')
            bgc2 = request.POST.get('bgc2')
            sec_sup = request.POST.get('sec_sup')
            chargeman = request.POST.get('Chargeman')
            mistry = request.POST.get('Mistry')
            c1 = request.POST.get('c1')
            c2 = request.POST.get('c2')
            c3 = request.POST.get('c3')
            c4 = request.POST.get('c4')
            a1 = request.POST.get('a1')
            a2 = request.POST.get('a2')
            a3 = request.POST.get('a3')
            SSFO = request.POST.get('SSFO')
              
            
            MG22new.objects.create(updt_date=str(updt_date), shop_sec = str(shop_sec),name=str(name),staff_no=str(staff_no), ticketno=str(ticketno), acc_Date =str(acc_Date),cause = str(cause), reason_neg = str(reason_neg), reason_y_neg= str(reason_y_neg),equip_check= str(equip_check), suggestions = str(suggestions), bgc= str(bgc), bgc2= str(bgc2), sec_sup= str(sec_sup), chargeman = str(chargeman), mistry= str(mistry),c1 = str(c1), c2 = str(c2), c3 = str(c3), c4 =str(c4), a1= str(a1), a2= str(a2), a3= str(a3), ssfo= str(SSFO) )
            print(updt_date, shop_sec, name, staff_no, ticketno, acc_Date, cause, reason_neg, reason_y_neg, equip_check, suggestions, bgc, bgc2, sec_sup, chargeman, mistry, c1, c2, c3, c4, a1, a2, a3, SSFO)

            messages.success(request, 'Successfully Saved !!!, Select new values to update')
    return render(request, "MG22view.html", context)

def mg22getstaffno(request):
    if request.method == "GET" and request.is_ajax():  
        from.models import Batch      
        shop_sec = request.GET.get('shop_sec')
        name=request.GET.get('name')
        w1=M5SHEMP.objects.filter(shopsec=shop_sec,name=name).values('staff_no').distinct()
        wono = w1[0]['staff_no']
        cont ={
            "wono":wono,
        }
        # print("ths is",shop_sec)
        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg22getstaffName(request):
    if request.method == "GET" and request.is_ajax():  
        from .models import Batch     
        shop_sec = request.GET.get('shop_sec')
        staff_no = request.GET.get('staff_no')
        print(staff_no)
        w1=M5SHEMP.objects.filter(staff_no=staff_no).values('staff_no','name').distinct()
        wono = list(w1)
        print("ths is",shop_sec)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)








@login_required
@role_required(urlpass='/MG22report/')
def mg22report(request):
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
    dictemper={}
    totindb=0
    emp=[]
    empname = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname')
    if empname is not None and len(empname):
        for i in range(len(empname)):
            emp.append(empname[i]['empname'])

    w1=M5SHEMP.objects.all().values('name').distinct().exclude(name__isnull=True)
    wono=[]
    for w in range(len(w1)):
        wono.append(w1[w]['name'])
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'names':wono,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'lvdate':"yyyy-mm-dd",
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"yyyy-mm-dd",
            'names':wono,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"yyyy-mm-dd",
            'names':wono,
        }
    if request.method=="POST":
        bvalue=request.POST.get('proceed')
        shop_sec=request.POST.get('shop_sec')
        lvdate=request.POST.get('updt_date')
        empname=request.POST.get('emp_name')
        accdate=request.POST.get('accdate')
        if bvalue=='Proceed':
            m2=MG22new.objects.filter(shop_sec=shop_sec,updt_date=lvdate,name=empname,acc_Date=accdate).first()
            nocertf=0
            mm=0
            # print(m2)
            if m2 is not None:
                if m2.c1 or m2.c2 or m2.c3 or m2.c4 is not None:
                    nocertf=1
                temper = {str(mm):{"name":m2.name,
                                               "ticketno":m2.ticketno,"cause":m2.cause,"bgc2":m2.bgc2,
                        "acdate":m2.acc_Date,"superv":m2.sec_sup,"mistry":m2.mistry,"chargeman":m2.chargeman,"ssfoname":m2.ssfo,
                        "reasonneg":m2.reason_neg,"epchck":m2.equip_check,"sugg":m2.suggestions,
                        "cert1":m2.c1,"cert2":m2.c2,"cert3":m2.c3,"cert4":m2.c4,"firstacc":m2.bgc,
                        "anex1":m2.a1,"anex2":m2.a2,"anex3":m2.a3,
                                               }}

                totindb=1
                dictemper.update(copy.deepcopy(temper))
                # print("dictionary")
                # print(dictemper)
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'names':wono,
                    'dictemper':dictemper,
                    'totindb':totindb,
                    'empname':emp,
                    "nocertf":nocertf,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
                    req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'sub':1,
                    'subnav':subnav,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                    # 'ticket':wono[0]['staff_no'],
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'shopsec':shop_sec,
                    'lvdate':lvdate,
                    'empname':wono[0]['name'],
                    # 'ticket':wono[0]['staff_no'],
                }

    return render(request,"mg22report.html",context)






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






@login_required
@role_required(urlpass='/axlewheelpressing_section/')
def axlewheelpressing_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    obj2=AxleWheelPressing.objects.all().filter(dispatch_status=False).order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=AxleWheelPressing.objects.all().filter(dispatch_status=False).values('sno')
    axle=AxleMachining.objects.filter(axlefitting_status=False,axleinspection_status=True).values('axle_no')
    wheelde=WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no')
    wheelnde=WheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no')
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mywheel':wheelde,
       'myaxle':axle,
        'mysno':mysno,
       }
    if request.method=="POST":
        
        once=request.POST.get('once')
        print(once)
        submit=request.POST.get('submit')
        if submit=='Save':

            bo_no=request.POST.get('bo_no')
            bo_date=request.POST.get('bo_date')
            pt_no=request.POST.get('pt_no')
            bo_qty=request.POST.get('bo_qty')
            indate=request.POST.get('in_qty')
            outdate=request.POST.get('out_qty')
            date=request.POST.get('date')
            loco_type=request.POST.get('locos')
            axle_no=request.POST.get('axle_no')
            wheelno_de=request.POST.get('wheelno_de')
            wheelno_nde=request.POST.get('wheelno_nde')
            bullgear_no=request.POST.get('bullgear_no')
            bullgear_make=request.POST.get('bullgear_make')
            
            if bo_no and bo_date and date and loco_type and axle_no and wheelno_de and wheelno_nde and bullgear_no and bullgear_make and pt_no and bo_qty and indate and outdate:
               obj=AxleWheelPressing.objects.create()
               obj.bo_no=bo_no
               obj.bo_date=bo_date
               obj.date=date
               obj.pt_no=pt_no
               obj.bo_qty=bo_qty
               obj.in_qty=indate
               obj.out_qty=outdate
               obj.loco_type=loco_type
               obj.axle_no=axle_no
               obj.wheelno_de=wheelno_de
               obj.wheelno_nde=wheelno_nde
               obj.bullgear_no=bullgear_no
               obj.bullgear_make=bullgear_make
               obj.inspectinspection_status=False
               obj.hhpinspection_status=False
               obj.save()
               messages.success(request, 'Successfully Added!')
               AxleMachining.objects.filter(axle_no=axle_no).update(axlefitting_status=True)
               WheelMachining.objects.filter(wheel_no=wheelno_de).update(wheelfitting_status=True)  
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=AxleWheelPressing.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        # if submit=='save':
    
        #     sno=int(request.POST.get('editsno'))
        #     bo_no=request.POST.get('editbo_no')
        #     bo_date=request.POST.get('editbo_date')
        #     date=request.POST.get('editdate')
        #     loco_type=request.POST.get('editlocos')
        #     axle_no=request.POST.get('editaxle_no')
        #     wheelno_de=request.POST.get('editwheelno_nde')
        #     in_qty=request.POST.get('editin_qty')
        #     out_qty=request.POST.get('editout_qty')
        #     if bo_no and bo_date and date and loco_type and airbox_sno and airbox_make and in_qty and out_qty:
        #        AxleWheelPressing.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,airbox_sno=airbox_sno,airbox_make=airbox_make,in_qty=in_qty,out_qty=out_qty)
        #        messages.success(request, 'Successfully Edited!')
        #     else:
        #        messages.error(request,"Please Enter S.No.!")
        if submit=='Edit':
            temp=request.POST.get('editsno')
            print(temp)
            if temp is not None:
                sno=int(temp)
            else:
                sno=None
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            bo_qty=request.POST.get('editbo_qty')
            indate=request.POST.get('editin_qty')
            outdate=request.POST.get('editout_qty')
            pt_no=request.POST.get('editpt_no')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            axle_no=request.POST.get('editaxle_no')
            wheelno_de=request.POST.get('editwheelno_de')
            wheelno_nde=request.POST.get('editwheelno_nde')
            bullgear_no=request.POST.get('editbullgear_no')
            bullgear_make=request.POST.get('editbullgear_make')
            in_qty=request.POST.get('editin_qty')
            out_qty=request.POST.get('editout_qty')

            if bo_no and bo_date and date and loco_type and pt_no and bo_qty and indate and outdate and axle_no and wheelno_de and wheelno_nde and bullgear_no and bullgear_make and in_qty and out_qty:
               AxleWheelPressing.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,axle_no=axle_no,in_qty=in_qty,out_qty=out_qty,wheelno_de=wheelno_de,wheelno_nde=wheelno_nde,bullgear_no=bullgear_no,bullgear_make=bullgear_make,pt_no=pt_no,bo_qty=bo_qty)
               AxleMachining.objects.filter(axle_no=axle_no).update(axlefitting_status=True)
               WheelMachining.objects.filter(wheel_no=wheelno_de).update(wheelfitting_status=True)
               messages.success(request, 'Successfully Edited!')
            else:
               messages.error(request,"Please Enter S.No.!")

        if submit=='InspectHHP':
            sno=int(request.POST.get('sno'))
            wheelno_de=request.POST.get('hhpwheelno_de')
            wheel_de_make=request.POST.get('hhpwheel_de_make')
            wheelno_nde=request.POST.get('hhpwheelno_nde')
            wheel_nde_make=request.POST.get('hhpwheel_nde_make')
            wheel_nde_pressure=request.POST.get('hhpwheel_nde_pressure')
            axle_no=request.POST.get('hhpaxle_no')
            axle_make=request.POST.get('hhpaxle_make')
            bullgear_no=request.POST.get('hhpbuhhpllgear_no')
            bullgear_make=request.POST.get('hhpbullgear_make')
            bullgear_pressure=request.POST.get('hhpbullgear_pressure')
            msu_unit_no=request.POST.get('hhpmsu_unit_no')
            msu_unit_make=request.POST.get('hhpmsu_unit_make')
            axle_box_no=request.POST.get('hhpaxle_box_no')
            axle_box_make=request.POST.get('hhpaxle_box_make')
            axle_box_clearance=request.POST.get('hhpaxle_box_clearance')
            suspension_bearing_de_no=request.POST.get('hhpsuspension_bearing_de_no')
            suspension_bearing_de_make=request.POST.get('hhpsuspension_bearing_de_make')
            suspension_bearing_nde_no=request.POST.get('hhpsuspension_bearing_nde_no')
            suspension_bearing_nde_make=request.POST.get('hhpsuspension_bearing_nde_make')
            cru_bearing_no_de=request.POST.get('hhpcru_bearing_no_de')
            cru_bearing_make_de=request.POST.get('hhpcru_bearing_make_de')
            cru_bearing_pressure_de=request.POST.get('hhpcru_bearing_pressure_de')
            cru_bearing_no_nde=request.POST.get('hhpcru_bearing_no_nde')
            cru_bearing_make_nde=request.POST.get('hhpcru_bearing_make_nde')
            cru_bearing_pressure_nde=request.POST.get('hhpcru_bearing_pressure_nde')
            date=request.POST.get('hhpdate')
            inspector_name=request.POST.get('hhpinspector_name')
            journal_no_de=request.POST.get('hhpjournal_no_de')
            journal_make_de=request.POST.get('hhpjournal_make_de')
            journal_no_nde=request.POST.get('hhpjournal_no_nde')
            journal_make_nde=request.POST.get('hhpjournal_make_nde')
            
            if wheelno_de and wheel_de_make and wheelno_nde and wheel_nde_make and wheel_nde_pressure and axle_no and axle_make and bullgear_no and bullgear_make and bullgear_pressure and msu_unit_no and msu_unit_make and axle_box_no and axle_box_make and axle_box_clearance and suspension_bearing_de_no and suspension_bearing_de_make and suspension_bearing_nde_no and suspension_bearing_nde_make and cru_bearing_no_de and cru_bearing_make_de and cru_bearing_pressure_de and date and inspector_name and cru_bearing_no_nde and cru_bearing_pressure_nde and cru_bearing_make_nde and journal_no_de and journal_make_de and journal_no_nde and journal_make_nde:
                AxleWheelPressing.objects.filter(sno=sno).update(hhpwheelno_de=wheelno_de,hhpwheel_de_make=wheel_de_make,hhpwheel_nde_make=wheel_nde_make,hhpwheelno_nde=wheelno_nde,hhpwheel_nde_pressure=wheel_nde_pressure,hhpaxle_no=axle_no,hhpaxle_make=axle_make,hhpbull_gear_no=bullgear_no,hhpbull_gear_make=bullgear_make,hhpbullgear_pressure=bullgear_pressure,hhpmsu_unit_no=msu_unit_no,hhpmsu_unit_make=msu_unit_make,hhpaxle_box_no=axle_box_no,hhpaxle_box_make=axle_box_make,hhpaxle_box_clearance=axle_box_clearance,hhpsuspension_bearing_de_no=suspension_bearing_de_no,hhpsuspension_bearing_de_make=suspension_bearing_de_make,hhpsuspension_bearing_nde_no=suspension_bearing_nde_no,hhpsuspension_bearing_nde_make=suspension_bearing_nde_make,hhpcru_bearing_no_de=cru_bearing_no_de,hhpcru_bearing_make_de=cru_bearing_make_de,hhpcru_bearing_pressure_de=cru_bearing_pressure_de,hhpdate=date,hhpinspector_name=inspector_name,hhpcru_bearing_no_nde=cru_bearing_no_nde,hhpcru_bearing_make_nde=cru_bearing_make_nde,hhpcru_bearing_pressure_nde=cru_bearing_pressure_nde,hhpinspection_status=True,hhpjournal_no_de=journal_no_de,hhpjournal_make_de=journal_make_de,hhpjournal_no_nde=journal_no_nde,hhpjournal_make_nde=journal_make_nde)
                messages.success(request,'Successfully Edited!')
            else:
                messages.error(request,"Please Enter the all the records!")    
        if submit=='Inspect':
            sno=int(request.POST.get('sno'))
            wheelno_de=request.POST.get('inspectwheelno_de')
            wheel_de_make=request.POST.get('inspectwheel_de_make')
            wheelno_nde=request.POST.get('inspectwheelno_nde')
            wheel_nde_make=request.POST.get('inspectwheel_nde_make')
            wheel_nde_pressure=request.POST.get('inspectwheel_nde_pressure')
            axle_no=request.POST.get('inspectaxle_no')
            axle_make=request.POST.get('inspectaxle_make')
            bullgear_no=request.POST.get('inspectbullgear_no')
            bullgear_make=request.POST.get('inspectbullgear_make')
            bullgear_pressure=request.POST.get('inspectbullgear_pressure')
            msu_unit_no=request.POST.get('inspectmsu_unit_no')
            msu_unit_make=request.POST.get('inspectmsu_unit_make')
            axle_box_no=request.POST.get('inspectaxle_box_no')
            axle_box_make=request.POST.get('inspectaxle_box_make')
            axle_box_clearance=request.POST.get('inspectaxle_box_clearance')
            suspension_bearing_de_no=request.POST.get('inspectsuspension_bearing_de_no')
            suspension_bearing_de_make=request.POST.get('inspectsuspension_bearing_de_make')
            suspension_bearing_nde_no=request.POST.get('inspectsuspension_bearing_nde_no')
            suspension_bearing_nde_make=request.POST.get('inspectsuspension_bearing_nde_make')
            cru_bearing_no_de=request.POST.get('inspectcru_bearing_no_de')
            cru_bearing_make_de=request.POST.get('inspectcru_bearing_make_de')
            cru_bearing_pressure_de=request.POST.get('inspectcru_bearing_pressure_de')
            cru_bearing_no_nde=request.POST.get('inspectcru_bearing_no_nde')
            cru_bearing_make_nde=request.POST.get('inspectcru_bearing_make_nde')
            cru_bearing_pressure_nde=request.POST.get('inspectcru_bearing_pressure_nde')
            date=request.POST.get('inspectdate')
            inspector_name=request.POST.get('inspectinspector_name')
            if cru_bearing_pressure_nde and cru_bearing_make_nde and wheelno_de and wheel_de_make and wheelno_nde and wheel_nde_make and wheel_nde_pressure and axle_no and axle_make and bullgear_no and bullgear_make and bullgear_pressure and msu_unit_no and msu_unit_make and axle_box_no and axle_box_make and axle_box_clearance and suspension_bearing_de_no and suspension_bearing_de_make and suspension_bearing_nde_no and suspension_bearing_nde_make and cru_bearing_no_de and cru_bearing_make_de and cru_bearing_pressure_de and date and inspector_name and cru_bearing_no_nde:
                AxleWheelPressing.objects.filter(sno=sno).update(wheelno_de=wheelno_de,wheel_de_make=wheel_de_make,wheel_nde_make=wheel_nde_make,wheelno_nde=wheelno_nde,wheel_nde_pressure=wheel_nde_pressure,axle_no=axle_no,axle_make=axle_make,bullgear_no=bullgear_no,bullgear_make=bullgear_make,bullgear_pressure=bullgear_pressure,msu_unit_no=msu_unit_no,msu_unit_make=msu_unit_make,axle_box_no=axle_box_no,axle_box_make=axle_box_make,axle_box_clearance=axle_box_clearance,suspension_bearing_de_no=suspension_bearing_de_no,suspension_bearing_de_make=suspension_bearing_de_make,suspension_bearing_nde_no=suspension_bearing_nde_no,suspension_bearing_nde_make=suspension_bearing_nde_make,cru_bearing_no_de=cru_bearing_no_de,cru_bearing_make_de=cru_bearing_make_de,cru_bearing_pressure_de=cru_bearing_pressure_de,date=date,inspector_name=inspector_name,cru_bearing_no_nde=cru_bearing_no_nde,cru_bearing_make_nde=cru_bearing_make_nde,cru_bearing_pressure_nde=cru_bearing_pressure_nde,inspectinspection_status=True)
                messages.success(request,'Successfully Inspected!')
            else:
                messages.error(request,"Please Enter all the records!")

        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            disdate=request.POST.get('dispatch_date')
            if sno and dislocos and disdate:
                AxleWheelPressing.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_status=True,dispatch_date=disdate)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            sno=int(request.POST.get('delsno'))
            if sno:
                myval=list(AxleWheelPressing.objects.filter(sno=sno).values('axle_no'))
                myval1=list(AxleWheelPressing.objects.filter(sno=sno).values('wheel_no'))
                print(myval)
                AxleMachining.objects.filter(axle_no=myval[0]['axle_no']).update(axlefitting_status=False)
                WheelMachining.objects.filter(wheel_no=myval1[0]['wheel_no']).update(wheelfitting_status=False) 
                AxlewheelPressing.objects.filter(sno=sno).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        return HttpResponseRedirect("/axlewheelpressing_section/")

    return render(request,"axlewheelpressing_section.html",my_context)

def axlepress_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def wheelpress_inspectsno(request):
    if request.method=="GET" and request.is_ajax():
        print("hello1")
        mysno=request.GET.get('sels_no')
        print("hello")
        myval=list(AxleWheelPressing.objects.filter(sno=mysno).values('wheelno_de','wheelno_nde','axle_no','bullgear_no','bullgear_make'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)







@login_required
@role_required(urlpass='/m13insert/')
def m13insert(request):
    from .models import M13
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M13.objects.all().filter(shop=rolelist[i]).values('wo').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
        
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            part_no = request.POST.get('part_nop')
            obj = M13.objects.filter(shop=shop_sec,part_no=part_no,wo=wo_no).values('m13_no','qty_tot','qty_ins','qty_pas','qty_rej','opn','vendor_cd','fault_cd','reason','slno','m13_sn','wo_rep','m15_no','epc','rej_cat','job_no').distinct()
            obj1 = Part.objects.filter(partno=part_no).values('des','drgno').distinct()
            #obj2 = M2Doc.objects.filter(f_shopsec=shop_sec,part_no=part_no,batch_no=wo_no).values('m2sln').distinct()
            leng = obj.count()
            leng1 = obj1.count()
            print(obj)
            print(obj1)
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj': obj,
                    'obj1': obj1,
                    #'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    #'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    req = M13.objects.all().filter(shop=rolelist[i]).values('wo').distinct()
                    wo_nop =wo_nop | req
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'wo_nop':wo_nop,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    #'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    #'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    #'obj2': obj2,
                    'len': leng,
                    'len1':leng1,
                    #'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no': part_no,
                }

        if submitvalue=='Save':
                from decimal import Decimal
                m13_no=request.POST.get('m13no')  
                slno= request.POST.get('slno')
                m13_sn = request.POST.get('m13_sn')
                epc = request.POST.get('epc')
                ab=request.POST.get('qty_tot')
                if len(ab):
                    qty_tot = Decimal(ab)
                else:
                    qty_tot=0
                ab=request.POST.get('qty_ins')
                if len(ab):
                    qty_ins = Decimal(ab)
                else:
                    qty_ins=0
                ab=request.POST.get('qty_pas')
                if len(ab):
                    qty_pas = Decimal(ab)
                else:
                    qty_pas=0
                ab=request.POST.get('qty_rej')
                if len(ab):
                    qty_rej = Decimal(ab)
                else:
                    qty_rej=0
                vendor_cd = request.POST.get('vendor_cd')
                opn = request.POST.get('opn')
                job_no = request.POST.get('job_no')
                fault_cd = request.POST.get('fault_cd')
                wo_rep = request.POST.get('wo_rep')
                m13no = request.POST.get('m13no')
                m15_no = request.POST.get('m15_no')
                rej_cat = request.POST.get('rej_cat')
                reason = request.POST.get('reason')

                if m13_sn and qty_tot and qty_ins and qty_pas and qty_rej and vendor_cd and opn and job_no and fault_cd and wo_rep and m15_no and rej_cat and reason and m13no and slno and epc:
                    m13obj=M13.objects.create()
                    m13obj.m13_sn=m13_sn
                    m13obj.qty_tot=qty_tot
                    m13obj.qty_ins=qty_ins
                    m13obj.qty_pas=qty_pas
                    m13obj.qty_rej=qty_rej
                    m13obj.vendor_cd=vendor_cd
                    m13obj.opn=opn
                    m13obj.job_no=job_no 
                    m13obj.fault_cd=fault_cd
                    m13obj.wo_rep=wo_rep
                    m13obj.m15_no=m15_no 
                    m13obj.rej_cat=rej_cat
                    m13obj.reason=reason
                    m13obj.m13_no=m13no
                    m13obj.slno=slno
                    m13obj.epc=epc
                    m13obj.save()
                    messages.success(request,'Successfully Edited!')
                else:
                    messages.success(request,'Please enter all fields!')
                # print(m13obj)

    return render(request,"m13insert.html",context)







@login_required
@role_required(urlpass='/mg20view/')
def mg20view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0, len(rolelist)):
            req = Shemp.objects.all().filter(shopsec=rolelist[i]).values('staff_no').exclude(staff_no__isnull=True).distinct()
            wo_nop =wo_nop | req



        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            current_date = date.today()
            print(staff_no)
            print(shop_sec)
            obj = Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('name', 'desgn', 'cat', 'emp_type').distinct()
            print(obj)
            obj1 = MG20.objects.filter(shop_sec=shop_sec, staff_no=staff_no).values('no_of_days', 'nature', 'appr_datej').distinct()
            if len(obj1)== 0:
                obj1=range(0, 1)

            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'date' : current_date,


                        'sub': 1,

                        'staff_no': staff_no,
                        'shop_sec': shop_sec,

                        'subnav':subnav
                  }
            elif(len(rolelist)==1):
                  for i in range(0, len(rolelist)):
                      req = Shemp.objects.all().filter(shopsec=rolelist[i]).values('staff_no').exclude(staff_no__isnull=True).distinct()
                      wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'sub': 1,
                        'date': current_date,

                        'staff_no': staff_no,
                        'shop_sec': shop_sec,

                        'subnav':subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'date': current_date,
                        'sub': 1,

                        'staff_no': staff_no,
                        'shop_sec': shop_sec,

                        'subnav':subnav
                  }

        if submitvalue=='Save':

                shop_sec= request.POST.get('shop_sec1')
                staff_no = request.POST.get('staff_no1')
                name= request.POST.get('name1')
                desgn = request.POST.get('desgn1')
                cat = request.POST.get('cat1')
                emp_type = request.POST.get('emp_type1')
                no_of_days = request.POST.get('no_of_days')
                nature = request.POST.get('nature')
                appr_datej = request.POST.get('appr_datej')
                current_date=date.today()
                print(name)

                obj2 = MG20.objects.filter(shop_sec=shop_sec, staff_no=staff_no, cat=cat, current_date=current_date).distinct()
                print(len(obj2))
                if len(obj2) == 0:
                    MG20.objects.create(current_date=str(current_date), shop_sec=str(shop_sec), staff_no=str(staff_no), cat=str(cat), name=str(name), desgn=str(desgn), emp_type=str(emp_type), nature=str(nature), no_of_days=str(no_of_days), appr_datej=str(appr_datej))

                else:
                    MG20.objects.filter(shop_sec=shop_sec, staff_no=staff_no, cat=cat).update(name=str(name), desgn=str(desgn), emp_type=str(emp_type), nature=str(nature), no_of_days=str(no_of_days), appr_datej=str(appr_datej))

                wo_no=MG20.objects.all().values('staff_no').distinct()
                messages.success(request, 'Successfully Done!, Select new values to proceed')
    return render(request, "mg20view.html", context)





def mg20getstaff(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')

        staff = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
        staff_no = list(staff)
        return JsonResponse(staff_no, safe=False)
    return JsonResponse({"success": False}, status=400)






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
    return render(request,'RoleGeneration.html',context)






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
    return render(request,'RoleDelete.html',context)


@login_required
@role_required(urlpass='/m30view/')
def m30view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            req = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            #req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            staff_no = request.POST.get('staff_no')
            date = request.POST.get('date')
            req = request.POST.get('req')
            print(req)
            print(date)
            obj = Part.objects.filter(partno=part_no).values('des', 'drgno').distinct()
            rand=random.randint(0, 100000000)

            obj1= Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('name', 'desgn', 'cat', 'emp_type').distinct()
            obj2=Batch.objects.filter(part_no=part_no).values('loco_fr', 'loco_to').distinct()
            obj3 = M30.objects.filter(shop_sec=shop_sec, staff_no=staff_no, part_no=part_no, date=date).values('qty', 'dimension','spe_val','obt_val','interc', 'waiver_no', 'waiver_date','non_conf_des','reason_for_non_conf','corr_action_plan','remarks_hod','remarks_cde','remarks_cqam','request_no').distinct()

            # if len(obj1) > 1:
            #     obj1=obj1[0]
            if len(obj3) == 0:
                obj3 =range(0, 1)

            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'req': req,
                        'staff_no': staff_no,
                        'rand': rand,

                        'sub': 1,

                        'date': date,

                        'shop_sec': shop_sec,
                        'part_no': part_no,

                        'subnav':subnav
                  }
            elif(len(rolelist)==1):
                  for i in range(0,len(rolelist)):
                        # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
                        # wo_nop =wo_nop | req

                        req = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                       # req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                        wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,


                        'req': req,
                        'staff_no': staff_no,
                        'rand': rand,

                        'sub': 1,

                        'date': date,

                        'shop_sec': shop_sec,
                        'part_no': part_no,

                        'subnav':subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'req': req,
                        'staff_no': staff_no,
                        'rand': rand,

                        'sub': 1,

                        'date': date,

                        'shop_sec': shop_sec,
                        'part_no': part_no,

                        'subnav':subnav
                  }

        if submitvalue=='Save':

            shop_sec= request.POST.get('shop_sec1')
            part_no= request.POST.get('part_no1')
            staff_no = request.POST.get('staff_no1')
            req = request.POST.get('req1')
            date = request.POST.get('date1')


            qty = request.POST.get('qty')
            dimension = request.POST.get('dimension')
            spe_val = request.POST.get('spe_val')
            obt_val = request.POST.get('obt_val')
            loco_fr = request.POST.get('loco_fr1')
            loco_to = request.POST.get('loco_to1')
            interc = request.POST.get('interc')
            waiver_no = request.POST.get('waiver_no')
            waiver_date = request.POST.get('waiver_date')
            non_conf_des = request.POST.get('non_conf_des')
            reason_for_non_conf = request.POST.get('reason_for_non_conf')
            corr_action_plan = request.POST.get('corr_action_plan')
            remarks_hod = request.POST.get('remarks_hod')
            remarks_cqam = request.POST.get('remarks_cqam')
            remarks_cde = request.POST.get('remarks_cde')
            request_no = request.POST.get('rand1')
            specification_no=request.POST.get('spec_no1')
            print(obt_val)

            obj5 = M30.objects.filter(shop_sec=shop_sec, staff_no=staff_no, part_no=part_no, date=date).distinct()
            print(len(obj5))
            if len(obj5) == 0:
                M30.objects.create(shop_sec=str(shop_sec), staff_no=str(staff_no), part_no=str(part_no), specification_no=str(specification_no),  request_no=str(request_no), loco_fr=str(loco_fr), loco_to=str(loco_to), req=str(req), date=str(date), qty=str(qty), dimension=str(dimension), spe_val=str(spe_val), obt_val=str(obt_val), interc=str(interc), waiver_no=str(waiver_no), waiver_date=str(waiver_date), non_conf_des=str(non_conf_des), reason_for_non_conf=str(reason_for_non_conf),  corr_action_plan=str( corr_action_plan), remarks_hod=str(remarks_hod), remarks_cqam=str(remarks_cqam), remarks_cde=str(remarks_cde))

            else:

                M30.objects.filter(shop_sec=shop_sec, staff_no=staff_no, part_no=part_no, date=date).update(specification_no=str(specification_no),  request_no=str(request_no), loco_fr=str(loco_fr), loco_to=str(loco_to), req=str(req), qty=str(qty), dimension=str(dimension), spe_val=str(spe_val), obt_val=str(obt_val), interc=str(interc), waiver_no=str(waiver_no), waiver_date=str(waiver_date), non_conf_des=str(non_conf_des), reason_for_non_conf=str(reason_for_non_conf),  corr_action_plan=str( corr_action_plan), remarks_hod=str(remarks_hod), remarks_cqam=str(remarks_cqam), remarks_cde=str(remarks_cde))
            wo_no=M2Doc.objects.all().values('batch_no').distinct()
            messages.success(request, 'Successfully Updated!, Select new values to update')
    return render(request, "m30view.html", context)


def m30getpartno(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        partno = list(w1)
        return JsonResponse(partno, safe = False)
    return JsonResponse({"success": False}, status=400)




def m30getstaffno(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')

        staff = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
        staff_no = list(staff)
        return JsonResponse(staff_no, safe=False)
    return JsonResponse({"success": False}, status=400)



@login_required
@role_required(urlpass='/mg15view/')
def mg15view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0, len(rolelist)):
            req = Shemp.objects.all().filter(shopsec=rolelist[i]).values('staff_no').exclude(staff_no__isnull=True).distinct()
            wo_nop =wo_nop | req



        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            date = request.POST.get('date')
            # print(staff_no)
            # print(shop_sec)
            obj = Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('name', 'desgn', 'cat', 'emp_type').distinct()
            # print(obj)
            obj1 = MG15.objects.filter(shop_sec=shop_sec, staff_no=staff_no, date=date).values('remarks', 'h1a', 'h2a', 'causeofab', 'ticket_no').distinct()
            tt = Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('ticket_no').distinct()
            # print(tt)
            print("jj")
            print(obj1)
            if len(obj1)== 0:
                obj1=range(0, 1)

            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'tt': tt,

                        'date' : date,


                        'sub': 1,

                        'staff_no': staff_no,
                        'shop_sec': shop_sec,

                        'subnav':subnav
                  }
            elif(len(rolelist)==1):
                  for i in range(0, len(rolelist)):
                      req = Shemp.objects.all().filter(shopsec=rolelist[i]).values('staff_no').exclude(staff_no__isnull=True).distinct()
                      wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'tt': tt,

                        'sub': 1,
                        'date': date,

                        'staff_no': staff_no,
                        'shop_sec': shop_sec,

                        'subnav': subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'tt': tt,

                        'date': date,
                        'sub': 1,

                        'staff_no': staff_no,
                        'shop_sec': shop_sec,

                        'subnav':subnav
                  }

        if submitvalue=='Save':

                shop_sec= request.POST.get('shop_sec1')
                staff_no = request.POST.get('staff_no1')
                date = request.POST.get('date1')
                name= request.POST.get('name1')
                desgn = request.POST.get('desgn1')
                emp_type = request.POST.get('emp_type1')
                cat = request.POST.get('cat1')
                ticket_no = request.POST.get('ticket_no')
                h1a = request.POST.get('h1a')
                h2a = request.POST.get('h2a')
                remarks = request.POST.get('remarks')
                causeofab = request.POST.get('causeofab')

                print(h1a)

                obj2 = MG15.objects.filter(shop_sec=shop_sec, staff_no=staff_no, date=date, ).distinct()
                print(len(obj2))
                if len(obj2) == 0:
                    MG15.objects.create(date=str(date), shop_sec=str(shop_sec), staff_no=str(staff_no), cat=str(cat), name=str(name), desgn=str(desgn), emp_type=str(emp_type), remarks=str(remarks), causeofab=str(causeofab), ticket_no=str(ticket_no), h1a=str(h1a), h2a=str(h2a))

                else:
                    MG15.objects.filter(shop_sec=shop_sec, staff_no=staff_no, date=date).update(cat=str(cat), ticket_no=str(ticket_no), name=str(name), desgn=str(desgn), emp_type=str(emp_type), remarks=str(remarks), causeofab=str(causeofab), h1a=str(h1a), h2a=str(h2a))

                wo_no=MG15.objects.all().values('staff_no').distinct()
                messages.success(request, 'Successfully Done!, Select new values to proceed')
    return render(request, "mg15view.html", context)





def mg15getstaff(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')

        staff = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
        staff_no = list(staff)
        print(staff_no)
        return JsonResponse(staff_no, safe=False)
    return JsonResponse({"success": False}, status=400)



@login_required
@role_required(urlpass='/mg49view/')
def mg49view(request):
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
        tm=Shemp.objects.all().values('shopsec').distinct()
        
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = Shemp.objects.all().filter(shop_sec=rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'staff_no':staff_no,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
        
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            tm1=Part.objects.all().values('des').distinct()
            
            temp=Part.objects.all().values('shop_ut').distinct()
            tm2=Code.objects.filter(code__in=temp,cd_type='51').values('alpha_1').distinct()
            
            shop_sec = request.POST.get('shop_sec')
            updt_date = request.POST.get('updt_date')
            staff_no = request.POST.get('staff_no')

            obj = Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name','desgn').distinct().order_by('-yymm')[0];
            leng = 1
            if "Superuser" in rolelist:
                tm=Shemp.objects.all().values('shopsec').distinct()
                
                tmp=[]
                for on in tm:
                    tmp.append(on['shopsec'])
                context={
                    'tm1':tm1,
                    'tm2':tm2,
                    'obj': obj,
                    'len': leng,
                    'updt_date':updt_date,
                    'shop_sec': shop_sec,
                    'staff_no':staff_no,
                    'sub' : 1,
                    'lenm' :2,
                    'roles':tmp,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    req = Shemp.objects.all().filter(shop_sec=rolelist[i]).values('staff_no').distinct()
                    staff_no =staff_no | req
                context = {
                    'tm1':tm1,
                    'tm2':tm2,
                    'obj': obj,
                    'len': leng,
                    'updt_date':updt_date,
                    'shop_sec': shop_sec,
                    'staff_no':staff_no,
                    'sub' : 1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
            elif(len(rolelist)>1):
                context = {
                    'tm1':tm1,
                    'tm2':tm2,
                    'obj': obj,
                    'len': leng,
                    'updt_date':updt_date,
                    'shop_sec': shop_sec,
                    'staff_no':staff_no,
                    'sub' : 1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
        
        if submitvalue=='submit':
            updt_date = request.POST.get('update')
            shop_sec= request.POST.get('shopsec')
            staff_no = request.POST.get('staffno')
            part_no = request.POST.get('part_no')
            matdes = request.POST.get('matdes')
            quantity = request.POST.get('quantity')
            weight = request.POST.get('weight')
            unit = request.POST.get('unit')
            now = datetime.datetime.now()
            user=request.user
            # if(part_no==None or matdes==None or quantity==None or weight==None or unit==None):
            #     pass;
            # else:
            print(updt_date,shop_sec,staff_no,part_no,quantity,weight,unit,now,user)
            MG49.objects.create(shopsec=str(shop_sec), staff_no=str(staff_no), date=str(updt_date), part_no=str(part_no), desc=str(matdes), quan=str(quantity), weight=str(weight),login_id=str(user), last_modified=str(now), unit=str(unit))

            totindb=request.POST.get('totmebs')
            
            for tb in range(2,int(totindb)+1):
                part_no=request.POST.get('part_no'+str(tb))
                shop_sec= request.POST.get('shopsec')
                staff_no = request.POST.get('staffno')
                matdes=request.POST.get('matdes'+str(tb))
                quantity=request.POST.get('quan'+str(tb))
                weight=request.POST.get('weight'+str(tb))
                unit=request.POST.get('unit'+str(tb))
                now = datetime.datetime.now()
                user=request.user
                updt_date = request.POST.get('update')
                # if(part_no==None or matdes==None or quantity==None or weight==None or unit==None):
                #     pass;
                # else:
                print(updt_date,shop_sec,staff_no,part_no,quantity,weight,unit,now,user)
                MG49.objects.create(shopsec=str(shop_sec), staff_no=str(staff_no), date=str(updt_date), part_no=str(part_no),desc=str(matdes), quan=str(quantity), weight=str(weight),login_id=str(user), last_modified=str(now), unit=str(unit))

        
        ###################################
    return render(request,"mg49view.html",context)

def mg49getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        # tablecolumnname=same var name
        staff_no = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg49getpart_no(request):
    
    if request.method == "GET" and request.is_ajax():
        matdes = request.GET.get('matdes')
        # print(matdes,"matdes")
        w1 = list(Part.objects.filter(des=matdes).values('partno').distinct())
        w2 = list(Part.objects.filter(des=matdes).values('shop_ut').distinct())
        ut=w2[0]['shop_ut']

        tm2=Code.objects.filter(code=ut,cd_type='51').values('alpha_1').distinct()
        # unit=tm2[0]['alpha_1']   

        print(w1,"mat des",ut,tm2)
        print("mat des",tm2[0]['alpha_1'])
        wono = w1[0]['partno']
        if(tm2.count()==0):
            k='NULL'
        else:
            k=tm2[0]['alpha_1']


        cont ={
            "wono":wono,
            "ut":k,
        }
        
        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)


def mg49report(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    tm1=Part.objects.all().values('partno').distinct()
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    staff_no = empmast.objects.none()
    if "Superuser" in rolelist:
        tm=Shemp.objects.all().values('shopsec').distinct()
        
        tmp=[]
    
        for on in tm:
            tmp.append(on['shopsec'])
        
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'tm1':tm1,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = Shemp.objects.all().filter(shop_sec=rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'staff_no':staff_no,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            
            
            shop_sec = request.POST.get('shop_sec')
            updt_date = request.POST.get('updt_date')
            staff_no = request.POST.get('staff_no')
            part_no=request.POST.get('part_no')
            print(shop_sec,updt_date,staff_no,part_no)
            obj = Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name','desgn').distinct().order_by('-yymm')[0];
            leng = 1
            alldata = MG49.objects.filter(shopsec=shop_sec,staff_no=staff_no,date=updt_date).values('shopsec','staff_no','date','part_no','quan','weight','login_id','unit','desc').distinct();
            
            leng2 = alldata.count()
            print(obj)
            print(alldata)
            context = {
                        'tm1':tm1,
                        'alldata':alldata,
                        'tm1':tm1,
                        'obj': obj,
                        'len': leng,
                        'len2':leng2,
                        'updt_date':updt_date,
                        'shop_sec': shop_sec,
                        'staff_no':staff_no,
                        'sub' : 1,
                        'nav':nav,
                        'ip':get_client_ip(request),  
                        'subnav':subnav,
            }
    return render(request,"mg49report.html",context)


@login_required
@role_required(urlpass='/mg18view/')
def mg18view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0, len(rolelist)):
            req = Shemp.objects.all().filter(shopsec=rolelist[i]).values('staff_no').exclude(staff_no__isnull=True).distinct()
            wo_nop =wo_nop | req



        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Submit':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            to = request.POST.get('toadrr')
            date = request.POST.get('dated')
            namaddr = request.POST.get('nameadrr')
            empcode = request.POST.get('empcode')
            natindus = request.POST.get('natindus')
            addr_accdnt = request.POST.get('addraccd')
            brnchdept = request.POST.get('brdept')
            namadrr_inj = request.POST.get('injadrr')
            insur_no = request.POST.get('insur')
            sex = request.POST.get('sex')
            age_lstbrth = request.POST.get('agebirth')
            occup_inj = request.POST.get('occinj')
            dthrs_accdnt = request.POST.get('dthrsacc')
            hr_strtwrk = request.POST.get('hrwork')
            cause_accndt = request.POST.get('cosacc')
            mach_accdnt = request.POST.get('namemach')
            mach_mov = request.POST.get('movmachpwr')
            inj_doing = request.POST.get('injdoin')
            inj_extent = request.POST.get('natextinj')
            inj_off = request.POST.get('injoffwrk')
            name_doct = request.POST.get('namedoct')
            inj_evid = request.POST.get('nameprsn')
            how_accdnt = request.POST.get('howaccoccrd')
            inj_loc = request.POST.get('locinj')
            inj_retrn = request.POST.get('injretrn')
            dthr_retrn = request.POST.get('dthrrtrn')
            inj_died = request.POST.get('injdied')
            dt_death = request.POST.get('dtdeath')
            stloc_insur = request.POST.get('namstins')
            stinsur_dispns = request.POST.get('stinsdisp')
            distrct = request.POST.get('distrct')
            dt_receipt = request.POST.get('dtrct')
            accdnt_no = request.POST.get('acdntno')
            indus_no = request.POST.get('indusno')
            cause_no = request.POST.get('causno')
            sex_1 = request.POST.get('sex')
            particulars = request.POST.get('othrparti')
            dt_invstgtn = request.POST.get('dtinvest')
            rslt_invstgtn = request.POST.get('rsltinvest')
            effct_frm = request.POST.get('subj')
            print(to)


            MG18.objects.create(to=str(to),  date=str(date), namaddr=str(namaddr), empcode=str(empcode),
                                natindus=str(natindus), addr_accdnt=str(addr_accdnt), brnchdept=str(brnchdept), namadrr_inj=str(namadrr_inj),
                                insur_no=str(insur_no), sex=str(sex), age_lstbrth=str(age_lstbrth), occup_inj=str(occup_inj), dthrs_accdnt=str(dthrs_accdnt),
                                hr_strtwrk=str(hr_strtwrk), cause_accndt=str(cause_accndt), mach_accdnt=str(mach_accdnt), mach_mov=str(mach_mov),
                                inj_doing=str(inj_doing), inj_extent=str(inj_extent), inj_off=str(inj_off), name_doct=str(name_doct), inj_evid=str(inj_evid),
                                how_accdnt=str(how_accdnt), inj_loc=str(inj_loc), inj_retrn=str(inj_retrn),  dthr_retrn=str(dthr_retrn),
                                inj_died=str(inj_died), dt_death=str(dt_death), stloc_insur=str(stloc_insur), stinsur_dispns=str(stinsur_dispns),
                                distrct=str(distrct), dt_receipt=str(dt_receipt), accdnt_no=str(accdnt_no), indus_no=str(indus_no), cause_no=str(cause_no),
                                sex_1=str(sex_1), particulars=str(particulars), dt_invstgtn=str(dt_invstgtn), rslt_invstgtn=str(rslt_invstgtn),
                                effct_frm=str(effct_frm))

            messages.info(request, 'Successfully Done!, Select new values to proceed')

            # print(staff_no)
            # print(shop_sec)
            # obj = Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('name', 'desgn', 'cat', 'emp_type').distinct()
            # # print(obj)
            # obj1 = MG15.objects.filter(shop_sec=shop_sec, staff_no=staff_no, date=date).values('remarks', 'h1a', 'h2a', 'causeofab', 'ticket_no').distinct()
            # tt = Shemp.objects.filter(shopsec=shop_sec, staff_no=staff_no).values('ticket_no').distinct()
            # print(tt)
            # print("jj")
            # print(obj1)
            # if len(obj1)== 0:
            #     obj1=range(0, 1)


            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        # 'obj': obj,
                        # 'obj1': obj1,
                        # 'tt': tt,

                        'date' : date,


                        'sub': 1,

                        # 'staff_no': staff_no,
                        # 'shop_sec': shop_sec,

                        'subnav':subnav
                  }
            elif(len(rolelist)==1):
                  for i in range(0, len(rolelist)):
                      req = Shemp.objects.all().filter(shopsec=rolelist[i]).values('staff_no').exclude(staff_no__isnull=True).distinct()
                      wo_nop = wo_nop | req
                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        # 'obj': obj,
                        # 'obj1': obj1,
                        # 'tt': tt,

                        'sub': 1,
                        'date': date,

                        # 'staff_no': staff_no,
                        # 'shop_sec': shop_sec,

                        'subnav': subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        # 'obj': obj,
                        # 'obj1': obj1,
                        # 'tt': tt,

                        'date': date,
                        'sub': 1,
                        #
                        # 'staff_no': staff_no,
                        # 'shop_sec': shop_sec,

                        'subnav':subnav
                  }

        # if submitvalue=='Save':
        #
        #         shop_sec= request.POST.get('shop_sec1')
        #         staff_no = request.POST.get('staff_no1')
        #         date = request.POST.get('date1')
        #         name= request.POST.get('name1')
        #         desgn = request.POST.get('desgn1')
        #         emp_type = request.POST.get('emp_type1')
        #         cat = request.POST.get('cat1')
        #         ticket_no = request.POST.get('ticket_no')
        #         h1a = request.POST.get('h1a')
        #         h2a = request.POST.get('h2a')
        #         remarks = request.POST.get('remarks')
        #         causeofab = request.POST.get('causeofab')
        #
        #         print(h1a)
        #
        #         obj2 = MG15.objects.filter(shop_sec=shop_sec, staff_no=staff_no, date=date, ).distinct()
        #         print(len(obj2))
        #         if len(obj2) == 0:
        #             MG15.objects.create(date=str(date), shop_sec=str(shop_sec), staff_no=str(staff_no), cat=str(cat), name=str(name), desgn=str(desgn), emp_type=str(emp_type), remarks=str(remarks), causeofab=str(causeofab), ticket_no=str(ticket_no), h1a=str(h1a), h2a=str(h2a))
        #
        #         else:
        #             MG15.objects.filter(shop_sec=shop_sec, staff_no=staff_no, date=date).update(cat=str(cat), ticket_no=str(ticket_no), name=str(name), desgn=str(desgn), emp_type=str(emp_type), remarks=str(remarks), causeofab=str(causeofab), h1a=str(h1a), h2a=str(h2a))
        #
        #         wo_no=MG15.objects.all().values('staff_no').distinct()
        #         messages.success(request, 'Successfully Done!, Select new values to proceed')
    return render(request, "mg18view.html", context)


@login_required
@role_required(urlpass='/m11view/')
def m11view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
            wo_no =wo_no | req
        context = {
            'sub':0,
            'len' :len(rolelist),
            'wo_no':wo_no,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'lent':0,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'len' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'lent':0,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        print(submitvalue)
        if submitvalue=='Proceed':
            from decimal import Decimal
            month = request.POST.get('monthdrop')
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            staff_no = request.POST.get('staff_no')
            part_no = request.POST.get('part_no')
            tempcat=Shemp.objects.filter(staff_no=staff_no).values('cat','name').distinct()
            empname=tempcat[0]['name']
            tcat=tempcat[0]['cat']
            obj1 = M11.objects.filter(staff_no=staff_no,shopsec=shop_sec,month=month).values('cat','in1','out','date','total_time','detail_no','idle_time').distinct()
            print(obj1)
            obj2='None'
            obj3='None'
            leng=0
            leng1=0
            rr='None'
            amt=0
            patotal=0
            a=0 
            b=0
            t=0
            if len(obj1):
                print(obj1)
                if obj1[0]['cat'] is not None:
                    print("in if cat none")
                    t=obj1[0]['cat']
                else:
                    print("in else cat")
                    t=tempcat[0]['cat']
            else:
                t=tempcat[0]['cat']
            print("t",t)
            if t != 'None':
                obj2 = Rates.objects.filter(staff_no=staff_no).values('avg_rate').distinct()
                obj3 = M11.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('month','cat').distinct()
                if len(obj3):
                    obj3 = M11.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('month','cat')[0]
                # print(obj2)


            for op in range(len(obj1)):
                patotal=obj1[op]['total_time']
                print("patotal",patotal)
                if patotal is not None and len(str(patotal)):
                    p=patotal.split(':')
                    a=a+Decimal(p[0])
                    b=b+Decimal(p[1])
                    if (b>=60):
                        a=a+1
                        b=b%60

                rr=str(a)+':'+str(b)    
                print(rr)
            
        
                print("a",a)
                print("b",b)

            #if len(obj1):
            # print(obj1)
            tmhr=rr
            print("1",tmhr)
            if len(obj2):    
                avgrt=obj2[0]['avg_rate']
                print("2")
                if tmhr == 'None': 
                    tmhr=0
                    avgrt=0
                    print("3")
                else:
                    tmhr1=tmhr.split(':')
                    tmhr=Decimal(tmhr1[0])+(Decimal(tmhr1[1])/60)
                    print("4")
                    
            
                amt=tmhr*avgrt
            leng = obj1.count()
            leng1 = obj2.count()
            leng=obj1.count()
            amt=round(amt,2)
            print("amt1",amt)
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,'tcat':tcat,'empname':empname,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                    wo_no =wo_no | req
                context = {
                    'sub':1,
                    'len' :len(rolelist),
                    'wo_no':wo_no,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles' :rolelist,
                    'lent':0,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,'tcat':tcat,'empname':empname,
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'len' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles' :rolelist,
                    'lent':0,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,'tcat':tcat,'empname':empname,
                }


        if submitvalue=='Submit':
            # print("in submit")                               #!!!!!!!1!!!!!!!!!!!!capital S
            leng=request.POST.get('len')
            print("leng=",leng)
            shopsec= request.POST.get('shopsec')
            staff_no = request.POST.get('staff_no')
            inoutnum = request.POST.get("inoutnum")
            ename= request.POST.get('empname')
            scat=request.POST.get('tcat')
            print(scat)
            print("dadd",inoutnum)
            
            for i in range(1, int(leng)+1):
                date = request.POST.get('date'+str(i))
                month = request.POST.get('month')
                in1 = request.POST.get('in1'+str(i))
                out = request.POST.get('out'+str(i))
                total_time = request.POST.get('total_time'+str(i))
                idle_time = request.POST.get('idle_time'+str(i))
                detail_no = request.POST.get('detail_no'+str(i))
                amt = request.POST.get('amt1'+str(i))
                M11.objects.filter(shopsec=shopsec,staff_no=staff_no,date=date,month=month).update(date=str(date),name=str(ename),cat=scat,in1=str(in1),out=str(out),total_time=str(total_time),detail_no=str(detail_no),idle_time=str(idle_time), amt=str(amt))
                print("data saved")
            for i in range(1,int(inoutnum)+1):
                date = request.POST.get('dateadd'+str(i))
                month = request.POST.get('month_add'+str(i))
                in1 = request.POST.get('in1add'+str(i))
                out = request.POST.get('outadd'+str(i))
                total_time = request.POST.get('total_time_add'+str(i))
                idle_time = request.POST.get('idle_time_add'+str(i))
                detail_no = request.POST.get('detail_noadd'+str(i))    
                if date and month and in1 and out and idle_time and detail_no and total_time:
                    M11.objects.create(shopsec=shopsec,staff_no=staff_no,in1=str(in1),out=str(out),name=str(ename),cat=scat,month=str(month),total_time=str(total_time),date=str(date),idle_time=str(idle_time),detail_no=str(detail_no))
                    messages.success(request, 'Data Saved Successfully!!')
                else:
                    messages.success(request, 'Please enter all values!!')
                wo_no=Batch.objects.all().values('bo_no').distinct()

    return render(request,"m11views.html",context)                        


def m11getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2=Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
        # print(w2)
        wo_no = list(w2)                                             
        return JsonResponse(wo_no, safe = False)                    
    return JsonResponse({"success":False}, status=400)


def m11getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        # staff_no = list(M11.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        staff_no=list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m11getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        
        wo_no = request.GET.get('wo_no')
        
        part_no = list(Batch.objects.filter(bo_no=wo_no).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(urlpass='/m11report/')
def m11report(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
            wo_no =wo_no | req
        context = {
            'sub':0,
            'len' :len(rolelist),
            'wo_no':wo_no,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'lent':0,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'len' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'lent':0,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        print(submitvalue)
        if submitvalue=='Proceed':
            from decimal import Decimal
            month = request.POST.get('monthdrop')
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            staff_no = request.POST.get('staff_no')
            part_no = request.POST.get('part_no')
            tempcat=Shemp.objects.filter(staff_no=staff_no).values('cat','name').distinct()
            empname=tempcat[0]['name']
            tcat=tempcat[0]['cat']
            obj1 = M11.objects.filter(staff_no=staff_no,shopsec=shop_sec,month=month).values('month','cat','in1','out','date','total_time','detail_no','idle_time').distinct()
            print(obj1)
            obj2='None'
            obj3='None'
            leng=0
            leng1=0
            rr='None'
            amt=0
            patotal=0
            a=0 
            b=0
            t=0
            if len(obj1):
                print(obj1)
                if obj1[0]['cat'] is not None:
                    print("in if cat none")
                    t=obj1[0]['cat']
                else:
                    print("in else cat")
                    t=tempcat[0]['cat']
            else:
                t=tempcat[0]['cat']
            print("t",t)
            if t != 'None':
                obj2 = Rates.objects.filter(staff_no=staff_no).values('avg_rate').distinct()
                obj3 = M11.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('month','cat')[0]
                print(obj2)


            for op in range(len(obj1)):
                patotal=obj1[op]['total_time']
                print("patotal",patotal)
                if patotal is not None and len(str(patotal)):
                    p=patotal.split(':')
                    a=a+Decimal(p[0])
                    b=b+Decimal(p[1])
                    if (b>=60):
                        a=a+1
                        b=b%60

                rr=str(a)+':'+str(b)    
                print(rr)
            
        
                print("a",a)
                print("b",b)

            #if len(obj1):
            print(obj1)
            tmhr=rr
            print("1",tmhr)
            if len(obj2):    
                avgrt=obj2[0]['avg_rate']
                print("2")
                if tmhr == 'None': 
                    tmhr=0
                    avgrt=0
                    print("3")
                else:
                    tmhr1=tmhr.split(':')
                    tmhr=Decimal(tmhr1[0])+(Decimal(tmhr1[1])/60)
                    print("4")
                    
            
                amt=tmhr*avgrt
            leng = obj1.count()
            leng1 = obj2.count()
            leng=obj1.count()
            amt=round(amt,2)
            print("amt1",amt)
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,'tcat':tcat,'empname':empname,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                    wo_no =wo_no | req
                context = {
                    'sub':1,
                    'len' :len(rolelist),
                    'wo_no':wo_no,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles' :rolelist,
                    'lent':0,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,'tcat':tcat,'empname':empname,
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'len' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles' :rolelist,
                    'lent':0,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'lent': leng,
                    'lent2': leng1,
                    'leng':leng,
                    'amt1': amt,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'r1':rr,
                    'month': month,'tcat':tcat,'empname':empname,
                }

    return render(request,"m11report.html",context)  

@login_required
@role_required(urlpass='/mg36view/')
def mg36view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5SHEMP.objects.all().filter(shopsec=rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'staff_no':staff_no,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
        
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            obj = Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name','desgn').distinct()
            obj1 = MG36.objects.filter(shop_sec=shop_sec,staff_no=staff_no).values('shop_arr','shop_dept','time_arr','time_dept','hosp_arr','hosp_dept','dept','office','date','med_officer','resumed_time','resumed_date','date_app')
            noprint=0
            leng = obj.count()
            leng1 = obj1.count()
            if len(obj1) == 0:
                noprint=1
            
            context = {
                        'obj': obj,
                        'obj1': obj1,
                        'len': leng,
                        'len1': leng1,
                        'shop_sec': shop_sec,
                        'ran':range(1,2),
                        'staff_no': staff_no,
                        'sub' : 1,
                        'noprint':noprint,
                        'nav':nav,
                        'ip':get_client_ip(request),  
                        'subnav':subnav,
            }
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'sub':0,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'ran':range(1,2),
                    'staff_no': staff_no,
                    'noprint':noprint,
                    'sub' : 1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    req = M5SHEMP.objects.all().filter(shopsec=rolelist[i]).values('staff_no').distinct()
                    staff_no =staff_no | req
                context = {
                    'sub':0,
                    'lenm' :len(rolelist),
                    'staff_no':staff_no,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'noprint':noprint,
                    'shop_sec': shop_sec,
                    'ran':range(1,2),
                    'staff_no': staff_no,
                    'sub' : 1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
        
            elif(len(rolelist)>1):
                context = {
                    'sub':0,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'ran':range(1,2),
                    'staff_no': staff_no,
                    'noprint':noprint,
                    'sub' : 1,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
            
        if submitvalue =='Submit':
                
                leng=request.POST.get('len')
                now = datetime.datetime.now()
                shop_sec = request.POST.get('shop_sec')
                staff_no = request.POST.get('staff_no')
                #name = request.POST.get('name')
                #desgn = request.POST.get('desgn')
                shop_arr = request.POST.get('shop_arr')
                shop_dept = request.POST.get('shop_dept')
                time_arr = request.POST.get('time_arr')
                time_dept = request.POST.get('time_dept')
                hosp_arr = request.POST.get('hosp_arr')
                hosp_dept = request.POST.get('hosp_dept')
                dept = request.POST.get('dept')
                office = request.POST.get('office')
                med_officer = request.POST.get('med_officer')
                date = request.POST.get('date')
                resumed_time = request.POST.get('resumed_time')
                resumed_date = request.POST.get('resumed_date')
                date_app = request.POST.get('date_app')
                print(leng,time_arr,time_dept,hosp_dept,hosp_arr,med_officer)

                mg36obj = MG36.objects.filter(shop_sec=shop_sec,staff_no=staff_no).distinct()
                if len(mg36obj) == 0:
                    
                    MG36.objects.create(login_id=request.user,shop_sec=str(shop_sec),staff_no=str(staff_no),shop_arr=str(shop_arr),shop_dept=str(shop_dept),
                    time_arr=str(time_arr),time_dept=str(time_dept),hosp_arr=str(hosp_arr),hosp_dept=str(hosp_dept),dept=str(dept),office=str(office),med_officer=str(med_officer),
                    date=str(date),date_app=str(date_app),resumed_time=str(resumed_time),resumed_date=str(resumed_date),last_modified=str(now))

                else:
                    MG36.objects.filter(shop_sec=shop_sec,staff_no=staff_no).update(shop_arr=str(shop_arr),shop_dept=str(shop_dept),
                    time_arr=str(time_arr),time_dept=str(time_dept),hosp_arr=str(hosp_arr),hosp_dept=str(hosp_dept),dept=str(dept),office=str(office),med_officer=str(med_officer),
                    date=str(date),date_app=str(date_app),resumed_time=str(resumed_time),resumed_date=str(resumed_date),last_modified=str(now))

                staff_no=MG36.objects.all().values('staff_no').distinct()

    return render(request,"mg36view.html",context)


def mg36getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no=list(SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/m9view/')
def m9view(request):
    from .models import m9
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = Oprn.objects.all().filter(shop=rolelist[i]).values('partno').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
        
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            from datetime import date
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            part_no = request.POST.get('part_nop')
            op_no=request.POST.get('op_no')
            dt=date.today
            context = {
                        'date':dt,
                        'shop_sec': shop_sec,
                        'wo_no': wo_no,
                        'part_no': part_no,
                        'op_no':op_no,
                        'sub' : 1,
                        'nav':nav,
                        'ip':get_client_ip(request),  
                        'subnav':subnav,
            }

        if submitvalue=='Save':
                from decimal import Decimal
                chng_optr=request.POST.get('cngoptr')
                sbc= request.POST.get('sbc')
                rjc = request.POST.get('rjc')
                cit = request.POST.get('cit')
                mw = request.POST.get('mw')
                mg9 = request.POST.get('mg9')
                optno = request.POST.get('optno')
                prvopt = request.POST.get('prvopt')
                remarks = request.POST.get('remarks')
                idlecard=request.POST.get('itc')
                idle=request.POST.get('ittime')
                

                m9obj=m9.objects.create()
                m9obj.empname=chng_optr
                m9obj.sus_jbno=Decimal(sbc)
                m9obj.date=request.POST.get('ddate')
                m9obj.res_jno=Decimal(rjc)
                m9obj.cat=cit
                m9obj.mw_no=mw
                m9obj.mg9_no=mg9
                m9obj.empno=optno
                m9obj.prev_empno=prvopt
                m9obj.remark=remarks
                m9obj.idle_time_man_mac=idlecard
                m9obj.on_off=idle
                m9obj.shop_sec=request.POST.get('shopsec')
                m9obj.part_no=request.POST.get('partno')
                m9obj.wo_no=request.POST.get('wono')
                m9obj.aff_opn=request.POST.get('opnno')

                
                m9obj.save()
                print(m9obj)

    


    
    return render(request,"m9view.html",context)


def m9getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        
        part_no = list(Oprn.objects.filter(shop_sec = shop_sec).values('part_no').distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)




def m9getopno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        part_no = request.GET.get('part_nop')
        print(shop_sec)
        print(part_no)
        op_no = list(Oprn.objects.filter(shop_sec = shop_sec,part_no=part_no).values('opn').distinct())
        print(op_no)
        return JsonResponse(op_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m9getwono(request):
    if request.method == "GET" and request.is_ajax():
        
        wo_no = list(Batch.objects.values('bo_no').distinct())
        print(wo_no)
        return JsonResponse(wo_no, safe = False)
    return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/m5hwview/')
def m5hwview(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = user_master.objects.none()
    if "Superuser" in rolelist:
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    return render(request,"m5hwview.html",context)

@login_required
@role_required(urlpass='/MG33view/')
def exam_detail(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context={
            'totindb':0,
            'nav':nav,
            'ip':get_client_ip(request),
            'subnav':subnav,
        }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='View':
            ecode=request.POST.get('ecode')
            ex=exam_master.objects.all().order_by('id')
            leng=len(ex)
            context={
                'sub':1,
                'obj':ex,
                'totindb':0,
                'leng':leng,
                'nav':nav,
            'ip':get_client_ip(request),
            'subnav':subnav,
            }
        if bval=='Save':
            tot=request.POST.get('total')
            if tot=='':
                tot=0
            else:
                tot=int(tot)+1
                for i in range(1,int(tot)):
                    if (request.POST.get("ecode"+str(i))):
                        ecode=request.POST.get("ecode"+str(i))
                        etype=request.POST.get("etype"+str(i))
                        prctd=request.POST.get("practical"+str(i))
                        prcmarks=request.POST.get("pracmax"+str(i))
                        orald=request.POST.get("oral"+str(i))
                        oralmarks=request.POST.get("orlmax"+str(i))
                        edate=request.POST.get("edate"+str(i))
                        exam_master.objects.create(exam_code=ecode,exam_type=etype,exam_date=edate,prac_desc=prctd,prac_max=prcmarks,oral_desc=orald,oral_max=oralmarks)
            ex1=request.POST.get('length')
            print("exist",ex1)
            for j in range(1,len(ex1)+1):
                print(j)
                if (request.POST.get("code"+str(j))):
                    ecode=request.POST.get("code"+str(j))
                    etype=request.POST.get("type"+str(j))
                    prctd=request.POST.get("prc"+str(j))
                    prcmrk=request.POST.get("pmax"+str(j))
                    orald=request.POST.get("orl"+str(j))
                    orlmrk=request.POST.get("omax"+str(j))
                    edt=request.POST.get("date"+str(j))
                    exam_master.objects.filter(exam_code=ecode).update(exam_type=etype,prac_desc=prctd,prac_max=prcmrk,oral_desc=orald,oral_max=orlmrk,exam_date=edt)
            messages.success(request,'Successfully Saved!!')
    return render(request,"examdetail.html",context)


@login_required
@role_required(urlpass='/MG33view/')
def view_exam_data(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    context={
            'totindb':0,
            'nav':nav,
            'ip':get_client_ip(request),
            'subnav':subnav,
        }
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='View Exam Detail':
            ecode=request.POST.get('ecode')
            ex=MG33new.objects.all().order_by('id')
            leng=len(ex)
            context={
                'sub':1,
                'obj':ex,
                'totindb':0,
                'leng':leng,
                'nav':nav,
            'ip':get_client_ip(request),
            'subnav':subnav,
            }
        if bval=='Save':
            tot=request.POST.get('total')
            if tot=='':
                tot=0
            else:
                tot=int(tot)+1
                for i in range(1,int(tot)):
                    if (request.POST.get("ecode"+str(i))):
                        ecode=request.POST.get("ecode"+str(i))
                        etype=request.POST.get("etype"+str(i))
                        prctd=request.POST.get("practical"+str(i))
                        prcmarks=request.POST.get("pracmax"+str(i))
                        orald=request.POST.get("oral"+str(i))
                        oralmarks=request.POST.get("orlmax"+str(i))
                        edate=request.POST.get("edate"+str(i))
                        exam_master.objects.create(exam_code=ecode,exam_type=etype,exam_date=edate,prac_desc=prctd,prac_max=prcmarks,oral_desc=orald,oral_max=oralmarks)
            ex1=request.POST.get('length')
            print("exist",ex1)
            for j in range(1,len(ex1)+1):
                print(j)
                if (request.POST.get("code"+str(j))):
                    ecode=request.POST.get("code"+str(j))
                    etype=request.POST.get("type"+str(j))
                    prctd=request.POST.get("prc"+str(j))
                    prcmrk=request.POST.get("pmax"+str(j))
                    orald=request.POST.get("orl"+str(j))
                    orlmrk=request.POST.get("omax"+str(j))
                    edt=request.POST.get("date"+str(j))
                    exam_master.objects.filter(exam_code=ecode).update(exam_type=etype,prac_desc=prctd,prac_max=prcmrk,oral_desc=orald,oral_max=orlmrk,exam_date=edt)
            messages.success(request,'Successfully Saved!!')
    return render(request,"mg33viewdata.html",context)





# @login_required
# @role_required(urlpass='/mg33report/')
def mg33report(request):
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
    stfno=set()
    ex=MG33new.objects.all().values('staff_no')
    for i in ex:
        if i['staff_no'] is not None:
            stfno.add(i['staff_no'])
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'obj':stfno,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = empmast.objects.filter(shop_sec=rolelist[i]).values('empno').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"yyyy-mm-dd",
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'lvdate':"yyyy-mm-dd",
        }
    if request.method=="POST":
        bval=request.POST.get('proceed')
        if bval=='Proceed':
            
            stfno=set()
            

            
            ex=MG33new.objects.all().values('staff_no')
            for i in ex:
                if i['staff_no'] is not None:
                    stfno.add(i['staff_no'])
            shpsec = request.POST.get('shop_sec')
            staffno=request.POST.get('staff_no')
            update=request.POST.get('updt_date')
            ex = MG33new.objects.filter(shop_sec=shpsec,staff_no=staffno,updt_date=update).all()
            if ex:
                print("if") 
                pscore=ex[0].prac_score
                oscore=ex[0].oral_score
                result=ex[0].result
                trdadmin=ex[0].trade_test_admin
                worker=ex[0].name
                secsup=ex[0].sec_sup
                trdoff=ex[0].trade_test_officer
                print(ex)
                excode=set()
                j=0
                for i in range(len(ex)):
                    excode.add(ex[i].exam_code)
                print(excode)
                for a in excode:
                    obj1=exam_master.objects.filter(exam_code=a)
            
                
                if "Superuser" in rolelist:
                    tm=shop_section.objects.all()
                    tmp=[]
                    for on in tm:
                        tmp.append(on.section_code)
                    context={
                        'sub':1,
                        'lenm' :2,
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'shopsec':shpsec,
                        'obj':stfno,
                        'obj2':ex,
                        'obj1':obj1,
                        'pscore':pscore,'oscore':oscore,'result':result,
                        'trdadmin':trdadmin,'worker':worker,'trdoff':trdoff,'secsup':secsup,
                    }
                elif(len(rolelist)==1):
                    for i in range(0,len(rolelist)):
                        w1 = empmast.objects.filter(role__isnull=True,dept_desc='MECHANICAL').values('empname').distinct
                    context = {
                        'sub':1,
                        'subnav':subnav,
                        'lenm' :len(rolelist),
                        'wo_nop':wo_nop,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'shopsec':shpsec,
                        'obj':stfno,
                        'obj2':ex,
                        'obj1':obj1,
                        'pscore':pscore,'oscore':oscore,'result':result,
                        'trdadmin':trdadmin,'worker':worker,'trdoff':trdoff,'secsup':secsup,
                    }
                elif(len(rolelist)>1):
                    context = {
                        'sub':1,
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'shopsec':shpsec,
                        'obj':stfno,
                        'obj2':ex,
                        'obj1':obj1,
                        'pscore':pscore,'oscore':oscore,'result':result,
                        'trdadmin':trdadmin,'worker':worker,'trdoff':trdoff,'secsup':secsup,
                    }
            else:
                print("else") 
                messages.error(request,"Data Not found!")         
        
    return render(request,"mg33report.html",context)




def m3a(request):
    return render(request,"m3a.html")

def performaA(request):
    return render(request,"performaA.html")



@login_required
@role_required(urlpass='/axlemachining_section/')
def axlemachining_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    obj2=AxleMachining.objects.all().filter(dispatch_status=False).order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=AxleMachining.objects.filter(dispatch_status=False).values('sno')
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mysno':mysno,
       }
    if request.method=="POST":
        once=request.POST.get('once')
        print(once)
        submit=request.POST.get('submit')
        if submit=='Save':
        
            first=request.POST.get('bo_no')
            second=request.POST.get('bo_date')
            third=request.POST.get('date')
            fourth=request.POST.get('axlep_no')
            sixth=request.POST.get('loco_type')
            eighth=request.POST.get('axle_no')
            ninth=request.POST.get('axle_make')
            tenth=request.POST.get('axle_heatcaseno')
            eleven=request.POST.get('pt_no')
            twelve=request.POST.get('bo_qty')
            indate=request.POST.get('in_qty')
            outdate=request.POST.get('out_qty')
            if first and second and third and fourth and sixth and eighth and ninth and tenth and eleven and twelve and indate and outdate:
                obj=AxleMachining.objects.create()
                obj.bo_no=first
                obj.bo_date=second
                obj.date=third
                obj.axlep_no=fourth
                obj.loco_type=sixth
                obj.axle_no=eighth
                obj.axle_make=ninth
                obj.axle_heatcaseno=tenth
                obj.axleinspection_status=False
                obj.pt_no=eleven
                obj.bo_qty=twelve
                obj.in_qty=indate
                obj.out_qty=outdate
                obj.save()
                messages.success(request, 'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=AxleMachining.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='save':

            sno=int(request.POST.get('editsno'))
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            bo_qty=request.POST.get('editbo_qty')
            pt_no=request.POST.get('editpt_no')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            axlep_no=request.POST.get('editaxlep_no')
            axle_no=request.POST.get('editaxle_no')
            axle_make=request.POST.get('editaxle_make')
            axle_heatcaseno=request.POST.get('editaxle_heatcaseno')
            indate=request.POST.get('editin_qty')
            outdate=request.POST.get('editout_qty')
            if bo_no and bo_date and date and loco_type and axlep_no and axle_no and axle_make and axle_heatcaseno and pt_no and bo_qty and indate and outdate:
                AxleMachining.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,pt_no=pt_no,bo_qty=bo_qty,in_qty=indate,out_qty=outdate,date=date,axlep_no=axlep_no,loco_type=loco_type,axle_no=axle_no,axle_make=axle_make,axle_heatcaseno=axle_heatcaseno)
                messages.success(request, 'Successfully Edited!')
            else:
                messages.error(request,"Please Enter S.No.!")
                
        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            dispatchdate=request.POST.get('dispatch_date')
            if sno and dislocos:
                AxleMachining.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_status=True,dispatch_date=dispatchdate)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            sno=int(request.POST.get('delsno'))
            if sno:
                AxleMachining.objects.filter(sno=sno).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")

        if submit=='InspectAxle':
            
            sno=int(request.POST.get('snoaxle'))
            print("sno",sno)
            ustaxle=request.POST.get('ustaxle')
            ustaxle_date=request.POST.get('ustaxle_date')
            ustaxle_status=request.POST.get('ustaxle_status')
            axlelength=request.POST.get('axlelength')
            journalaxle=request.POST.get('journalaxle')
            throweraxle=request.POST.get('throweraxle')
            wheelseataxle=request.POST.get('wheelseataxle')
            gearseataxle=request.POST.get('gearseataxle')
            collaraxle=request.POST.get('collaraxle')
            dateaxle=request.POST.get('dateaxle')
            bearingaxle=request.POST.get('bearingaxle')
            abutmentaxle=request.POST.get('abutmentaxle')
            inspector_nameaxle=request.POST.get('inspector_nameaxle')
            journal_surfacefinishGE=request.POST.get('journal_surfacefinishGE')
            wheelseat_surfacefinishGE=request.POST.get('wheelseat_surfacefinishGE')
            gearseat_surfacefinishGE=request.POST.get('gearseat_surfacefinishGE')
            journal_surfacefinishFE=request.POST.get('journal_surfacefinishFE')
            wheelseat_surfacefinishFE=request.POST.get('wheelseat_surfacefinishFE')
            gearseat_surfacefinishFE=request.POST.get('gearseat_surfacefinishFE')
            if ustaxle_date and ustaxle_status and ustaxle and axlelength and journalaxle and throweraxle and wheelseataxle and gearseataxle and collaraxle and dateaxle and bearingaxle and abutmentaxle and inspector_nameaxle and journal_surfacefinishGE and wheelseat_surfacefinishGE and gearseat_surfacefinishGE and journal_surfacefinishFE and wheelseat_surfacefinishFE and gearseat_surfacefinishFE:
                AxleMachining.objects.filter(sno=sno).update(ustaxle_date=ustaxle_date,ustaxle_status=ustaxle_status,ustaxle=ustaxle,axlelength=axlelength,journalaxle=journalaxle,throweraxle=throweraxle,wheelseataxle=wheelseataxle,gearseataxle=gearseataxle,collaraxle=collaraxle,dateaxle=dateaxle,bearingaxle=bearingaxle,abutmentaxle=abutmentaxle,inspector_nameaxle=inspector_nameaxle,journal_surfacefinishGE=journal_surfacefinishGE,wheelseat_surfacefinishGE=wheelseat_surfacefinishGE,gearseat_surfacefinishGE=gearseat_surfacefinishGE,journal_surfacefinishFE=journal_surfacefinishFE,wheelseat_surfacefinishFE=wheelseat_surfacefinishFE,gearseat_surfacefinishFE=gearseat_surfacefinishFE,axleinspection_status=True)
                messages.success(request, 'Axle Successfully Inspected!')
            else:
                messages.error(request,"Please Enter all records!")

        
        return HttpResponseRedirect("/axlemachining_section/")

    return render(request,"axlemachining_section.html",my_context)


def axle_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def axle_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(AxleMachining.objects.filter(sno=mysno).values('bo_no','bo_date','pt_no','bo_qty','in_qty','out_qty','date','axlep_no','loco_type','axle_no','axle_make','axle_heatcaseno'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(urlpass='/wheelmachining_section/')
def wheelmachining_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    obj2=WheelMachining.objects.all().filter(dispatch_status=False).order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=WheelMachining.objects.filter(dispatch_status=False).values('sno')
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo,
       'mysno':mysno,
       }
    if request.method=="POST":
        once=request.POST.get('once')
        print(once)
        submit=request.POST.get('submit')
        if submit=='Save':
        
            first=request.POST.get('bo_no')
            second=request.POST.get('bo_date')
            third=request.POST.get('date')
            fourth=request.POST.get('wheel_no')
            fifth=request.POST.get('wheel_make')
            sixth=request.POST.get('loco_type')
            seventh=request.POST.get('wheel_heatcaseno')
            eighth=request.POST.get('wheelp_no')
            eleven=request.POST.get('pt_no')
            twelve=request.POST.get('bo_qty')
            indate=request.POST.get('in_qty')
            outdate=request.POST.get('out_qty')
            if first and second and third and fourth and fifth and sixth and seventh and eighth and eleven and twelve and indate and outdate :
                obj=WheelMachining.objects.create()
                obj.bo_no=first
                obj.bo_date=second
                obj.date=third
                obj.wheel_no=fourth
                obj.wheel_make=fifth
                obj.loco_type=sixth
                obj.wheel_heatcaseno=seventh
                obj.wheelp_no=eighth
                obj.wheelinspection_status=False
                obj.pt_no=eleven
                obj.bo_qty=twelve
                obj.in_qty=indate
                obj.out_qty=outdate
                obj.save()
                messages.success(request, 'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=WheelMachining.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='save':

            sno=int(request.POST.get('editsno'))
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            bo_qty=request.POST.get('editbo_qty')
            pt_no=request.POST.get('editpt_no')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            wheelp_no=request.POST.get('editwheelp_no')
            wheel_no=request.POST.get('editwheel_no')
            wheel_make=request.POST.get('editwheel_make')
            wheel_heatcaseno=request.POST.get('editwheel_heatcaseno')
            indate=request.POST.get('in_qty')
            outdate=request.POST.get('out_qty')
            if bo_no and bo_date and date and loco_type and wheel_make and wheel_no and wheel_heatcaseno and wheelp_no and pt_no and bo_qty and indate and outdate:
                WheelMachining.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,pt_no=pt_no,bo_qty=bo_qty,in_qyt=indate,out_qty=outdate,date=date,wheel_no=wheel_no,wheel_make=wheel_make,loco_type=loco_type,wheel_heatcaseno=wheel_heatcaseno,wheelp_no=wheelp_no)
                messages.success(request, 'Successfully Edited!')
            else:
                messages.error(request,"Please Enter S.No.!")
                
        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            dispatchdate=request.POST.get('dispatch_date')
            if sno and dislocos:
                WheelMachining.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_status=True,dispatch_date=dispatchdate)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            sno=int(request.POST.get('delsno'))
            if sno:
                WheelMachining.objects.filter(sno=sno).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")

        if submit=='InspectWheel':
    
            sno=int(request.POST.get('snowheel'))
            oustwhl=request.POST.get('ustwhl')
            oustwhl_date=request.POST.get('ustwhl_date')
            oustwhl_status=request.POST.get('ustwhl_status')
            ohub_lengthwhl=request.POST.get('hub_lengthwhl')
            otread_diawhl=request.POST.get('tread_diawhl')
            orim_thicknesswhl=request.POST.get('rim_thicknesswhl')
            obore_diawhl=request.POST.get('bore_diawhl')
            oinspector_namewhl=request.POST.get('inspector_namewhl')
            odatewhl=request.POST.get('datewhl')
            if oustwhl_status and oustwhl_date and oustwhl and ohub_lengthwhl and otread_diawhl and orim_thicknesswhl and obore_diawhl and oinspector_namewhl and odatewhl:
                WheelMachining.objects.filter(sno=sno).update(ustwhl_status=oustwhl_status,ustwhl_date=oustwhl_date,ustwhl=oustwhl,hub_lengthwhl=ohub_lengthwhl,tread_diawhl=otread_diawhl,rim_thicknesswhl=orim_thicknesswhl,bore_diawhl=obore_diawhl,inspector_namewhl=oinspector_namewhl,datewhl=odatewhl,wheelinspection_status=True)
                messages.success(request, 'Wheel Successfully Inspected!')
            else:
                messages.error(request,"Please Select S.No.!")
   
        return HttpResponseRedirect("/wheelmachining_section/")

    return render(request,"wheelmachining_section.html",my_context)

def whl_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date','part_no','batch_qty'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def whl_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(WheelMachining.objects.filter(sno=mysno).values('bo_no','bo_date','pt_no','bo_qty','in_qty','out_qty','date','wheel_no','wheel_make','loco_type','wheel_heatcaseno','wheelp_no'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/mg6views/')
def mg6views(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = user_master.objects.none()
    tool_no = Tools.objects.values('tool_code').exclude(tool_code__isnull=True).distinct()
    prtlist=[]
    for i in tool_no:
        prtlist.append(i['tool_code'])
    # print(prtlist) 
    ticket_no = empmast.objects.values('ticket_no').exclude(ticket_no__isnull=True).distinct()
    prtticket=[]
    for i in ticket_no:
        prtticket.append(i['ticket_no'])
    #print(prtticket)   
    empno = empmast.objects.filter(payrate__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtemp=[]
    for i in empno:
        prtemp.append(i['empno'])
    # print(prtemp)
    empno = empmast.objects.filter(scalecode__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtsec=[]
    for i in empno:
        prtsec.append(i['empno'])
    #print(prtsec)  
    if "Superuser" in rolelist:
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,

        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,    
            'prtemp':prtemp,
            'prtsec':prtsec,
                }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mc_no = request.POST.get('mcno')
            cd_no = request.POST.get('cd_no')
            tool_no = request.POST.get('tool_no')

           

            
            print(tool_no)
            print(mc_no)
            obj  = MG6.objects.filter(tool_no=tool_no,machine_no=mc_no,cd_no=cd_no).values('tool_no','ticket_no','tool_des','date_of_damage','machine_no','cd_no','cause_of_damage','shop_suprintendent','sec_chargeman','remarks')
            obj1 = Lc1.objects.filter(lcno=mc_no)
            
            print(obj)
        #     obj  = Oprn.objects.filter(shop_sec=shop_sec, part_no=part_no).values('qtr_accep','mat_rej','lc_no','pa','at','des').distinct()
        #     obj1 = M5DOCnew.objects.filter(batch_no=wo_no,shop_sec=shop_sec, part_no=part_no,brn_no=brn_no,m5glsn=doc_no).values('cut_shear','pr_shopsec','n_shopsec','l_fr','l_to','qty_insp','inspector','date','remarks','worker','m2slno','qty_ord','m5prtdt','rm_ut','rm_qty','tot_rm_qty','rej_qty','rev_qty').distinct()
        #     obj2 = Part.objects.filter(partno=part_no).values('drgno','des','partno').order_by('partno').distinct()
        #     obj3 = Batch.objects.filter(bo_no=wo_no,part_no=part_no).values('batch_type','part_no').order_by('part_no').distinct()
        #     obj4 = M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('shopsec','staff_no','date','flag','name','cat','in1','out','ticket_no','month_hrs','total_time_taken').distinct()
        #     obj5 = M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('shopsec','staff_no','name','ticket_no','flag')[0]
        #     print("obj1",obj1)
        #     print("obj4",obj4)
        #    # print("oj4 len",len(obj4))
        #     ticket= randint(1111,9999)
            leng = obj.count()
            leng1 = obj1.count()
            # leng1=obj1.count()
            # leng2=obj2.count()
            # leng3=obj3.count()
            # leng4=obj4.count()
            #print("lengg4",leng4)
            
            
            if "Superuser" in rolelist:
                    tm=M5SHEMP.objects.all().values('shopsec').distinct()
                    tmp=[]
                    for on in tm:
                        tmp.append(on['shopsec'])
                    context={
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,   
                        'len1':leng1,  
                        'obj':obj,
                        'obj1':obj1,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mc_no': mc_no,
                        'cd_no': cd_no,
                        'tool_no':tool_no,
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                        'prtlist':prtlist,
                        'prtticket':prtticket,
                        'prtemp':prtemp,
                        'prtsec':prtsec,



                    }
            elif(len(rolelist)==1):
                    # print("in m5 else")
                    for i in range(0,len(rolelist)):
                        req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
                        wo_nop =wo_nop | req
                    context = {
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'obj':obj,
                        'obj1':obj1,    
                        'len':leng,
                        'len1':leng1,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mc_no': mc_no,
                        'cd_no': cd_no,
                        'tool_no':tool_no,
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                    }
            elif(len(rolelist)>1):
                    context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'obj':obj,
                        'obj1':obj1,
                        'len':leng,
                        'len1':leng1,
                        'shop_sec': shop_sec,
                        'mc_no': mc_no,
                        'cd_no': cd_no,
                        'tool_no':tool_no,
                        #'assm_no':assm_no,
                        'subnav':subnav
                    }    
        if submitvalue=='submit':
                    leng=request.POST.get('len')
                    now = datetime.datetime.now()
                    # shop_sec = request.POST.get('shop_sec')
                    des=request.POST.get('tool_des')
                    tool_no = request.POST.get('tool_no')
                    ticket_no= request.POST.get('ticket_no')
                    date=request.POST.get('date_of_damage')
                    mc_no = request.POST.get('mc_no')
                    cd_no=request.POST.get('cd_no')
                    cause = request.POST.get('cause_of_damage')
                    shop_sup = request.POST.get('shop_sup')
                    sec = request.POST.get('sec_chargeman')
                    rem = request.POST.get('rem')

                    mg6obj = MG6.objects.filter(tool_no=tool_no,machine_no=mc_no,cd_no=cd_no).distinct()
                    if len(mg6obj) == 0:

                        print(now)
                        # print(shop_sec)
                        print(tool_no)
                        print(ticket_no)
                        print(date)
                        print(mc_no)
                        print(cd_no)
                        print(cause)
                        print(shop_sup)
                        print(sec)

                        MG6.objects.create(tool_no=str(tool_no),tool_des=str(des),ticket_no=str(ticket_no),date_of_damage=str(date),machine_no=str(mc_no),cd_no=str(cd_no),cause_of_damage=str(cause),last_modified=str(now),login_id=request.user,shop_suprintendent=str(shop_sup),sec_chargeman=str(sec),remarks=str(rem))

                    else:

                        MG6.objects.filter(tool_no=tool_no,machine_no=mc_no,cd_no=cd_no).update(tool_no=str(tool_no),tool_des=str(des),ticket_no=str(ticket_no),date_of_damage=str(date),machine_no=str(mc_no),cd_no=str(cd_no),cause_of_damage=str(cause),shop_suprintendent=str(shop_sup),sec_chargeman=str(sec),last_modified=str(now),remarks=str(rem))
                        print(tool_no)
                        print(ticket_no)
                        print(date)
                        print(mc_no)
                        print(cd_no)
                        print(cause)
                        print(shop_sup)
                        print(sec)

                 
                    # instrument_number=Mgr.objects.all().values('instrument_number').distinct()

        
    
        #         wo_no=M5DOCnew.objects.all().values('batch_no').distinct()


    return render(request,"mg6views.html",context)

def mg6getmc(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        # print(shop_sec)
        wono = list(Lc1.objects.filter(shop_sec = shop_sec).values('lcno').distinct())
        print("wono",wono)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg6getcd(request):
    if request.method == "GET" and request.is_ajax():
        mc_no = request.GET.get('mcno')
        shop_sec = request.GET.get('shop_sec')
        print(shop_sec)
        print(mc_no)
        cd_no = list(Oprn.objects.filter(shop_sec = shop_sec).values('part_no'))

        print("cd_no",cd_no)
        return JsonResponse(cd_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg6gettool(request):
    if request.method == "GET" and request.is_ajax():
        
        shop_sec = request.GET.get('shop_sec')
        print(shop_sec)
        tool_no=list(ms_tools_master.objects.filter(shop_code=shop_sec).values('instrument_number').distinct())
        print("tool_no",tool_no)
        return JsonResponse(tool_no, safe = False)
        print("tool_no",tool_no)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/m21view/')
def m21view(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5SHEMP.objects.all().filter(shopsec=rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'staff_no':staff_no,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
        
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':            
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            yymm = request.POST.get('yymm')
            obj = M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no,yymm=yymm).values('name','desgn','cat').distinct()
            obj1 =M21.objects.filter(shop_sec=shop_sec,staff_no=staff_no).values('in1','out','in2','out2','total_time','date')
          
            leng = obj.count()
            leng1 = obj1.count()           

            context = {
                        'obj': obj,
                        'obj1': obj1,
                        'len': leng,
                        'len1': leng1,
                        'shop_sec': shop_sec,
                        'ran':range(1,2),
                        'staff_no': staff_no,                        
                        'yymm': yymm,
                        'sub' : 1,
                        'nav':nav,
                        'ip':get_client_ip(request),  
                        'subnav':subnav,
            }
        
        if submitvalue =='Submit': 
            inoutnum         =   request.POST.get("inoutnum")   
            print("inoutnum---",inoutnum)          

            in1     =   request.POST.get('in1')
            date    =   request.POST.get('date')
            out     =   request.POST.get('out')
            outdate =   request.POST.get('outdate')
            in2     =   request.POST.get('in2')
            out2    =   request.POST.get('out2')
            total_time = request.POST.get('total_time')                  
                    

            leng                    =   request.POST.get('len')               
            #now                     =   datetime.datetime.now()
            shop_sec                =  request.POST.get('shop_sec')
            staff_no                =  request.POST.get('staff_no')
            name                    =   request.POST.get('name')
            cat                     =   request.POST.get('cat')
            desgn                   =   request.POST.get('desgn')
            lastWeekPerHour         =   request.POST.get('lastWeekPerHour')
            lastWeekPerAmount       =   request.POST.get('lastWeekPerAmount')
            baseRatePerHour         =   request.POST.get('baseRatePerHour')
            baseRatePerHourAmount   =   request.POST.get('baseRatePerHourAmount')  
            cutTimeDay              =   request.POST.get('cutTimeDay')  
            cutTimeHours            =   request.POST.get('cutTimeHours')  
            additionalWagesDay      =   request.POST.get('additionalWagesDay')  
            additionalWagesHours    =   request.POST.get('additionalWagesHours')  
            factoryHalfDay          =   request.POST.get('factoryHalfDay')  
            factoryHalfHours        =   request.POST.get('factoryHalfHours')  
            generalOTDay            =   request.POST.get('generalOTDay')  
            generalOTHours          =   request.POST.get('generalOTHours')  
            nightAllowanceDay       =   request.POST.get('nightAllowanceDay')
            nightAllowanceHours     =   request.POST.get('nightAllowanceHours')
            halfHolidayDay          =   request.POST.get('halfHolidayDay')
            halfHolidayHours        =   request.POST.get('halfHolidayHours')
            payOffLeaveDay          =   request.POST.get('payOffLeaveDay')
            payOffLeaveHours        =   request.POST.get('payOffLeaveHours')
            unusedHolidaysDay       =   request.POST.get('unusedHolidaysDay')
            unusedHolidaysHours     =   request.POST.get('unusedHolidaysHours')
            supplementaryHolidaysDay=   request.POST.get('supplementaryHolidaysDay')
            supplementaryHolidaysHours  =   request.POST.get('supplementaryHolidaysHours')
                    
            M21DOCNEW1.objects.create(shop_sec=shop_sec,staff_no=staff_no,name=str(name),cat=str(cat),desgn=str(desgn),lastWeekPerHour=str(lastWeekPerHour),lastWeekPerAmount=str(lastWeekPerAmount),baseRatePerHour=str(baseRatePerHour),baseRatePerHourAmount=str(baseRatePerHourAmount),cutTimeDay=str(cutTimeDay), cutTimeHours=str(cutTimeHours),additionalWagesDay=str(additionalWagesDay),additionalWagesHours=str(additionalWagesHours),factoryHalfDay=str(factoryHalfDay), factoryHalfHours=str(factoryHalfHours),generalOTDay=str(generalOTDay),generalOTHours=str(generalOTHours),nightAllowanceDay=str(nightAllowanceDay), nightAllowanceHours=str(nightAllowanceHours),halfHolidayDay=str(halfHolidayDay),halfHolidayHours=str(halfHolidayHours),payOffLeaveDay=str(payOffLeaveDay),payOffLeaveHours=str(payOffLeaveHours),unusedHolidaysDay=str(unusedHolidaysDay),unusedHolidaysHours=str(unusedHolidaysHours),supplementaryHolidaysDay=str(supplementaryHolidaysDay), supplementaryHolidaysHours=str(supplementaryHolidaysHours),date=str(date), in1=str(in1),out=str(out), in2=str(in2),out2=str(out2), total_time=str(total_time), outdate = str(outdate))


            for i in range(1, int(inoutnum)+1):
                    
                    in1     =   request.POST.get('in1'+str(i))
                    date    =   request.POST.get('date'+str(i))
                    out     =   request.POST.get('out'+str(i))
                    outdate =   request.POST.get('outdate'+str(i))
                    in2     =   request.POST.get('in2'+str(i))
                    out2    =   request.POST.get('out2'+str(i))
                    total_time = request.POST.get('total_time'+str(i)) 
                    print("in1 : ",in1)
                    print("date : ",date)
                    print("out : ",out)
                    print("outdate : ",outdate)
                    print("in2 : ",in2)
                    print("out2 : ",out2)
                    print("total_time : ",total_time)
                    

                    leng                    =   request.POST.get('len')               
                    #now                     =   datetime.datetime.now()
                    shop_sec                =  request.POST.get('shop_sec')
                    staff_no                =  request.POST.get('staff_no')
                    name                    =   request.POST.get('name')
                    cat                     =   request.POST.get('cat')
                    desgn                   =   request.POST.get('desgn')
                    lastWeekPerHour         =   request.POST.get('lastWeekPerHour')
                    lastWeekPerAmount       =   request.POST.get('lastWeekPerAmount')
                    baseRatePerHour         =   request.POST.get('baseRatePerHour')
                    baseRatePerHourAmount   =   request.POST.get('baseRatePerHourAmount')  
                    cutTimeDay              =   request.POST.get('cutTimeDay')  
                    cutTimeHours            =   request.POST.get('cutTimeHours')  
                    additionalWagesDay      =   request.POST.get('additionalWagesDay')  
                    additionalWagesHours    =   request.POST.get('additionalWagesHours')  
                    factoryHalfDay          =   request.POST.get('factoryHalfDay')  
                    factoryHalfHours        =   request.POST.get('factoryHalfHours')  
                    generalOTDay            =   request.POST.get('generalOTDay')  
                    generalOTHours          =   request.POST.get('generalOTHours')  
                    nightAllowanceDay       =   request.POST.get('nightAllowanceDay')
                    nightAllowanceHours     =   request.POST.get('nightAllowanceHours')
                    halfHolidayDay          =   request.POST.get('halfHolidayDay')
                    halfHolidayHours        =   request.POST.get('halfHolidayHours')
                    payOffLeaveDay          =   request.POST.get('payOffLeaveDay')
                    payOffLeaveHours        =   request.POST.get('payOffLeaveHours')
                    unusedHolidaysDay       =   request.POST.get('unusedHolidaysDay')
                    unusedHolidaysHours     =   request.POST.get('unusedHolidaysHours')
                    supplementaryHolidaysDay=   request.POST.get('supplementaryHolidaysDay')
                    supplementaryHolidaysHours  =   request.POST.get('supplementaryHolidaysHours')
                    
                    M21DOCNEW1.objects.create(shop_sec=shop_sec,staff_no=staff_no,name=str(name),cat=str(cat),desgn=str(desgn),lastWeekPerHour=str(lastWeekPerHour),lastWeekPerAmount=str(lastWeekPerAmount),baseRatePerHour=str(baseRatePerHour),baseRatePerHourAmount=str(baseRatePerHourAmount),cutTimeDay=str(cutTimeDay), cutTimeHours=str(cutTimeHours),additionalWagesDay=str(additionalWagesDay),additionalWagesHours=str(additionalWagesHours),factoryHalfDay=str(factoryHalfDay), factoryHalfHours=str(factoryHalfHours),generalOTDay=str(generalOTDay),generalOTHours=str(generalOTHours),nightAllowanceDay=str(nightAllowanceDay), nightAllowanceHours=str(nightAllowanceHours),halfHolidayDay=str(halfHolidayDay),halfHolidayHours=str(halfHolidayHours),payOffLeaveDay=str(payOffLeaveDay),payOffLeaveHours=str(payOffLeaveHours),unusedHolidaysDay=str(unusedHolidaysDay),unusedHolidaysHours=str(unusedHolidaysHours),supplementaryHolidaysDay=str(supplementaryHolidaysDay), supplementaryHolidaysHours=str(supplementaryHolidaysHours),date=str(date), in1=str(in1),out=str(out), in2=str(in2),out2=str(out2), total_time=str(total_time), outdate = str(outdate))
               
            messages.success(request, 'GATE ATTENDANCE CARD Successfully generated.')
    return render(request,"m21view.html",context)
                        
def m21getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        print("shop_sec----",shop_sec)
        staff_no=list(M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        print("staff_no----",staff_no)
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m21getyymm(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff_no = request.GET.get('staff_no')
        yymm = list(M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('yymm').distinct())
        return JsonResponse(yymm, safe = False)
    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(urlpass='/M13register/')
def M13register(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M13.objects.all().filter(shop=rolelist[i]).values('wo').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
       
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
    if request.method == "POST":
       
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
           
            shop = request.POST.get('shop_sec')
            print('SHOP is ------>',shop)
            
            month = request.POST.get('month')            
            print("MONTH is **************************",month)
            month_temp1 = month.split("-")[0]
            print("month and year---->",month_temp1)

            month_temp2 = month.split("-")[1]
            print("month and year---->",month_temp2)

            month_final = month_temp2+'-'+month_temp1
            print(month_final)
            obj = M13.objects.filter(shop=shop,m13_date__contains=month_final).values('m13_no','wo','m13_date','part_no','qty_tot','opn','fault_cd','reason','wo_rep','job_no','shop').distinct()
            
        if obj:
                  
            leng = obj.count()

            print(obj)
           
            print("Test")

            context = {

                    'sub':1,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj': obj,
                    'len': leng,
                    'shop_sec': shop,
                    'month': month_final,
                    

            }
            

        else:
                print("Data Not Found") 
                messages.error(request,"Data Not Found ! - Please select correct Shop and Month data to display data ")  
    return render(request,"M13register.html",context)



@login_required
@role_required(urlpass='/airboxreport/')
def airboxreport(request):
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
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Proceed1':
            dt=request.POST.get('datew')
            ob1=MachiningAirBox.objects.filter(in_qty=dt).values('sno','pt_no')
            ob2=MachiningAirBox.objects.filter(out_qty=dt).values('sno','pt_no')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'ob1':ob1,
            'ob2':ob2,
            'dt':dt,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            ob1=MachiningAirBox.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','in_qty').order_by('in_qty')
            ob2=MachiningAirBox.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }

    return render(request,'airboxreport.html',context)

@login_required
@role_required(urlpass='/mg9initialreportviews/')
def mg9initialreportviews(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = user_master.objects.none()
    tool_no = Tools.objects.values('tool_code').exclude(tool_code__isnull=True).distinct()
    prtlist=[]
    for i in tool_no:
        prtlist.append(i['tool_code'])
    # print(prtlist) 
    ticket_no = empmast.objects.values('ticket_no').exclude(ticket_no__isnull=True).distinct()
    prtticket=[]
    for i in ticket_no:
        prtticket.append(i['ticket_no'])
    #print(prtticket)   
    empno = empmast.objects.filter(payrate__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtemp=[]
    for i in empno:
        prtemp.append(i['empno'])
    # print(prtemp)
    empno = empmast.objects.filter(scalecode__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtsec=[]
    for i in empno:
        prtsec.append(i['empno'])
    #print(prtsec)  
    if "Superuser" in rolelist:
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
           
            'roles':tmp,
            'subnav':subnav,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,

        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,    
            'prtemp':prtemp,
            'prtsec':prtsec,
                }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mw_no = request.POST.get('mwno')
            staff_no = request.POST.get('staffno')
            
            current_yr=int(datetime.datetime.now().year)


            print("Current year",current_yr)
        
        

           

            print(mw_no)
            print(staff_no)
            print(mw_no)
            obj  = MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).values('sec','mw_no','sl_no','staff_no','handed_date','comp_date','handed_time','comp_time','handed_cmsec','comp_cmsec','handed_cmserv','comp_cmserv','complaint','action').distinct()
            obj1  = MG9Initial.objects.values('id').count()

            print("count")
            print(obj1)
            leng = obj.count()
            slno=obj1
            slno=slno+1
            print(slno)
            

            
            if "Superuser" in rolelist:
                    tm=M5SHEMP.objects.all().values('shopsec').distinct()
                    tmp=[]
                    for on in tm:
                        tmp.append(on['shopsec'])
                    context={
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,   
                        # 'len1':leng1,  
                        'obj':obj,
                        # 'obj1':obj1,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'slno':slno,

                       
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                        'prtlist':prtlist,
                        'prtticket':prtticket,
                        'prtemp':prtemp,
                        'prtsec':prtsec,



                    }
            elif(len(rolelist)==1):
                    # print("in m5 else")
                    for i in range(0,len(rolelist)):
                        req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
                        wo_nop =wo_nop | req
                    context = {
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,
                        'obj':obj,
                        'slno':slno,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                     
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                    }
            elif(len(rolelist)>1):
                    context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'len':leng,
                        'obj':obj,
                        'slno':slno,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                  
                        #'assm_no':assm_no,
                        'subnav':subnav
                    }    
        if submitvalue=='submit':
                    leng=request.POST.get('len')
                    now = datetime.datetime.now()
                    # shop_sec = request.POST.get('shop_sec')
                    shop_sec=request.POST.get('shop_sec')
                    mw_no = request.POST.get('mw_no')
                    staff_no = request.POST.get('staff_no')
                    comp= request.POST.get('complaint')
                    date_handed=request.POST.get('date_handed')
                    date_com=request.POST.get('date_com')
                    time_handed=request.POST.get('time_handed')
                    time_com=request.POST.get('time_com')
                    sec_handed = request.POST.get('sec_handed')
                    sec_com = request.POST.get('sec_com')
                    serv_com = request.POST.get('serv_com')
                    serv_handed = request.POST.get('serv_handed')
                    action= request.POST.get('action')
                    sl_no = request.POST.get('sl_no')

          

                    mg9obj = MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).distinct()
                    if len(mg9obj) == 0:

                        print(now)
                        print(sl_no)
                        print("action",action)
                        # print(shop_sec)
                        print(shop_sec)
                        print(mw_no)
                        print(staff_no)
                        print(date_handed)
                        print(date_com)
                        print(time_handed)
                        print(time_com)
                        print(sec_handed)
                        print(sec_com)
                        print(serv_handed)
                        print(serv_com)
                        print(action)
                        print(comp)

                        MG9Initial.objects.create(sec=str(shop_sec),mw_no=str(mw_no),sl_no=str(sl_no),staff_no=str(staff_no),complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=request.user)
                    else:

                        MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).update(complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now))
                       
                        print(now)
                        print(sl_no)
                        # print(shop_sec)
                        print(shop_sec)
                        print(mw_no)
                        print(staff_no)
                        print(date_handed)
                        print(date_com)
                        print(time_handed)
                        print(time_com)
                        print(sec_handed)
                        print(sec_com)
                        print(serv_handed)
                        print(serv_com)
                        
                        print(comp)
                 

        
    


    return render(request,"mg9initialreportviews.html",context)

def mg9getmw(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        print(shop_sec)
        wono = list(Lc1.objects.filter(shop_sec = shop_sec).values('lcno').distinct())
        print("wono ----- : ",wono)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def mg9getstaff(request):
    if request.method == "GET" and request.is_ajax():
        # staff_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        staff = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        print(staff)
        return JsonResponse(staff, safe = False)
    return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/mg9compreportviews/')
def mg9compreportviews(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = user_master.objects.none()
    tool_no = Tools.objects.values('tool_code').exclude(tool_code__isnull=True).distinct()
    prtlist=[]
    for i in tool_no:
        prtlist.append(i['tool_code'])
    # print(prtlist) 
    ticket_no = empmast.objects.values('ticket_no').exclude(ticket_no__isnull=True).distinct()
    prtticket=[]
    for i in ticket_no:
        prtticket.append(i['ticket_no'])
    #print(prtticket)   
    empno = empmast.objects.filter(payrate__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtemp=[]
    for i in empno:
        prtemp.append(i['empno'])
    # print(prtemp)
    empno = empmast.objects.filter(scalecode__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtsec=[]
    for i in empno:
        prtsec.append(i['empno'])
    #print(prtsec)  
    if "Superuser" in rolelist:
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
           
            'roles':tmp,
            'subnav':subnav,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,

        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,    
            'prtemp':prtemp,
            'prtsec':prtsec,
                }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mw_no = request.POST.get('mwno')
            staff_no = request.POST.get('staffno')
            
            current_yr=int(datetime.datetime.now().year)


            print("Current year",current_yr)
        

           

            print(mw_no)
            print(staff_no)
            print(mw_no)
            obj2 = MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no).values('sl_no','handed_date','handed_time','handed_cmserv','handed_cmsec','complaint').distinct()
            obj  = MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).values('sec','mw_no','staff_no','comp_date','comp_time','comp_cmsec','comp_cmserv','action','total_losthrs','cause_hrs','mp_time','mismp_time','inv_time').distinct()
            # obj1  = MG9Complete.objects.values('id').count()
            print("OBJ2")
            print(obj2)
            leng = obj.count()
            leng2 = obj2.count()
            # slno=obj1
            # slno=slno+1
            # print(slno)
            

            
            if "Superuser" in rolelist:
                    tm=M5SHEMP.objects.all().values('shopsec').distinct()
                    tmp=[]
                    for on in tm:
                        tmp.append(on['shopsec'])
                    context={
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,   
                        # 'len1':leng1,  
                        'obj':obj,
                        'obj2':obj2,
                        'len2':leng2,
                        # 'obj1':obj1,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        # 'slno':slno,
                        'cyear':current_yr,
                       
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                        'prtlist':prtlist,
                        'prtticket':prtticket,
                        'prtemp':prtemp,
                        'prtsec':prtsec,



                    }
            elif(len(rolelist)==1):
                    # print("in m5 else")
                    for i in range(0,len(rolelist)):
                        req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
                        wo_nop =wo_nop | req
                    context = {
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,
                        'obj':obj,
                        'obj2':obj2,
                        'len2':leng2,
                        # 'slno':slno,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'cyear':current_yr,
                     
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                    }
            elif(len(rolelist)>1):
                    context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'len':leng,
                        'obj':obj,
                        'obj2':obj2,
                        'len2':leng2,
                        # 'slno':slno,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'cyear':current_yr,
                  
                        #'assm_no':assm_no,
                        'subnav':subnav
                    }    
        if submitvalue=='submit':
                    leng=request.POST.get('len')
                    now = datetime.datetime.now()
                    shop_sec=request.POST.get('shop_sec')
                    mw_no = request.POST.get('mw_no')
                    staff_no = request.POST.get('staff_no')
                    comp= request.POST.get('complaint')
                    date_handed=request.POST.get('date_handed')
                    date_com=request.POST.get('date_com')
                    time_handed=request.POST.get('time_handed')
                    time_com=request.POST.get('time_com')
                    sec_handed = request.POST.get('sec_handed')
                    sec_com = request.POST.get('sec_com')
                    serv_com = request.POST.get('serv_com')
                    serv_handed = request.POST.get('serv_handed')
                    action= request.POST.get('action')
                    sl_no = request.POST.get('sl_no')
                    lost_hrs = request.POST.get('lost_hrs')
                    elec = request.POST.get('elec')
                    mech = request.POST.get('mech')
                    mech_ele = request.POST.get('mech_ele')
                    mp = request.POST.get('mp')
                    inv = request.POST.get('inv')
                    mismp = request.POST.get('mismp')
                    # time_hrs=request.POST.get('time_hrs')
                    inv_time = request.POST.get('inv_time')
                    mismp_time = request.POST.get('mismp_time')
                    mp_time=request.POST.get('mp_time')



                   

                    print(sl_no)
                    print(shop_sec)
                    print(mw_no)
                    print(staff_no)
                    print(date_handed)
                    print(date_com)
                    print(time_handed)
                    print(time_com)
                    print(sec_handed)
                    print(sec_com)
                    print(serv_handed)
                    print(serv_com)
                    print(action)
                    print(comp)
                    print(lost_hrs)
                    print(elec)
                    print(mech)
                    print(mech_ele)
                    print(mp)
                    print(inv)
                    print(mismp)
                    print("mp_time",mp_time)
                    print("mismp_time",mismp_time)
                    print("inv_time",inv_time)
                    tmp=""
                    if(elec is not None):
                        tmp=str(elec)+str("   ")
                    if(mech is not None):
                        tmp=tmp+str(mech)+str("   ")
                    if(mech_ele is not None):
                        tmp=tmp+str(mech_ele)+str("   ")
                    if(mp is not None):
                        tmp=tmp+str(mp)+str("   ")
                    if(inv is not None):
                        tmp=tmp+str(inv)+str("   ")
                    print(tmp)
                    if(mp_time is None):
                        mp_time='00:00'
                        print("mp_time",mp_time)
                    if(inv_time is None):
                        inv_time='00:00'
                        print("inv_time",inv_time) 
                    if(mismp_time is None):
                        mismp_time='00:00'
                        print("mismp_time",mismp_time)        
                   

                    mg9obj = MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).distinct()
                    if len(mg9obj) == 0:

        #                 print(now)
        #                 print(sl_no)
        #                 # print(shop_sec)
        #                 print(shop_sec)
        #                 print(mw_no)
        #                 print(staff_no)
        #                 print(date_handed)
        #                 print(date_com)
        #                 print(time_handed)
        #                 print(time_com)
        #                 print(sec_handed)
        #                 print(sec_com)
        #                 print(serv_handed)
        #                 print(serv_com)
        #                 print(action)
        #                 print(comp)

                    
                        MG9Complete.objects.create(sec=str(shop_sec),mw_no=str(mw_no),sl_no=str(sl_no),staff_no=str(staff_no),complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=request.user,total_losthrs=str(lost_hrs),cause_hrs=str(tmp),mp_time=str(mp_time),inv_time=str(inv_time),mismp_time=str(mismp_time))
                    else:
                        cause=request.POST.get('cause_hrs')

                        MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).update(complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=str(request.user),total_losthrs=str(lost_hrs),cause_hrs=str(cause),mp_time=str(mp_time),inv_time=str(inv_time),mismp_time=str(mismp_time))
                       
        #                 print(now)
        #                 print(sl_no)
        #                 # print(shop_sec)
        #                 print(shop_sec)
        #                 print(mw_no)
        #                 print(staff_no)
        #                 print(date_handed)
        #                 print(date_com)
        #                 print(time_handed)
        #                 print(time_com)
        #                 print(sec_handed)
        #                 print(sec_com)
        #                 print(serv_handed)
        #                 print(serv_com)
        #                 print(action)
        #                 print(comp)
                 

        
    

    return render(request,"mg9compreportviews.html",context)

def mg9getmwno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(Lc1.objects.filter(shop_sec = shop_sec).values('lcno').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)


def mg9getstaffno(request):
    if request.method == "GET" and request.is_ajax():
        # staff_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        staff = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        print(staff)
        return JsonResponse(staff, safe = False)
    return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/miscreport/')
def miscreport(request):
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
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Proceed1':
            dt=request.POST.get('datew')
            ob1=MiscellSection.objects.filter(in_qty=dt).values('sno','pt_no')
            ob2=MiscellSection.objects.filter(out_qty=dt).values('sno','pt_no')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'ob1':ob1,
            'ob2':ob2,
            'dt':dt,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            ob1=MiscellSection.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','in_qty').order_by('in_qty')
            ob2=MiscellSection.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }

    return render(request,'miscreport.html',context)



@login_required
@role_required(urlpass='/axlereport/')
def axlereport(request):
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
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Axle Make Report(date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':5,
            }
        if bval=='No. of Axle (date wise)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':6,
            }
        if bval=='No. of Axle (date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':7,
            }
        if bval=='Month Wise Detail':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':10,
            }
        if bval=='Proceed1':
            dt=request.POST.get('datew')
            ob1=AxleMachining.objects.filter(in_qty=dt).values('sno','pt_no')
            ob2=AxleMachining.objects.filter(out_qty=dt).values('sno','pt_no')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'ob1':ob1,
            'ob2':ob2,
            'dt':dt,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            xyz=request.POST.get('axlemake')
            ob1=AxleMachining.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','in_qty').order_by('in_qty')
            ob2=AxleMachining.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }
        if bval=='Proceed3':
            dt1=request.POST.get('date3')
            dt2=request.POST.get('date4')
            ob1=AxleMachining.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','axle_no','ustaxle_status','in_qty').order_by('in_qty')
            ob2=AxleMachining.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','axle_no','ustaxle_status','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':4,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }
        if bval=='Proceed6':
            dt1=request.POST.get('datea')
            ob1=AxleMachining.objects.filter(in_qty=dt1).values('sno','axle_no','in_qty').order_by('in_qty')
            ob2=AxleMachining.objects.filter(out_qty=dt1).values('sno','axle_no','out_qty').order_by('out_qty')
            l1=len(ob1)
            l2=len(ob2)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':8,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,
            'l1':l1,'l2':l2,
            }
        if bval=='Proceed7':
            dt1=request.POST.get('datea1')
            dt2=request.POST.get('datea2')
            ob1=AxleMachining.objects.filter(in_qty__range=(dt1,dt2)).values('sno','axle_no','in_qty').order_by('in_qty')
            ob2=AxleMachining.objects.filter(out_qty__range=(dt1,dt2)).values('sno','axle_no','out_qty').order_by('out_qty')
            l1=len(ob1)
            l2=len(ob2)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':9,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            'l1':l1,'l2':l2,
            }
        if bval=='Proceed10':
            mon=request.POST.get('month')
            ob1=AxleMachining.objects.filter(date__contains=mon).values('sno','axle_no','in_qty','out_qty','pt_no','date').order_by('date')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':11,
            'ob1':ob1,
            'mon':mon,
            }

    return render(request,'axlereport.html',context)




@login_required
@role_required(urlpass='/wheelreport/')
def wheelreport(request):
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
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Wheel Make Report(date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':5,
            }
        if bval=='No. of Wheel (date wise)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':6,
            }
        if bval=='No. of Wheel (date range)':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':7,
            }
        if bval=='Month Wise Detail':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':10,
            }
        if bval=='Proceed1':
            dt=request.POST.get('datew')
            ob1=WheelMachining.objects.filter(in_qty=dt).values('sno','pt_no')
            ob2=WheelMachining.objects.filter(out_qty=dt).values('sno','pt_no')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'ob1':ob1,
            'ob2':ob2,
            'dt':dt,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            ob1=WheelMachining.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','in_qty').order_by('in_qty')
            ob2=WheelMachining.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }
        if bval=='Proceed3':
            dt1=request.POST.get('date3')
            dt2=request.POST.get('date4')
            ob1=WheelMachining.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','wheel_no','ustwhl_status','in_qty').order_by('in_qty')
            ob2=WheelMachining.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','wheel_no','ustwhl_status','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':4,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }
        if bval=='Proceed6':
            dt1=request.POST.get('datea')
            ob1=WheelMachining.objects.filter(in_qty=dt1).values('sno','wheel_no','in_qty').order_by('in_qty')
            ob2=WheelMachining.objects.filter(out_qty=dt1).values('sno','wheel_no','out_qty').order_by('out_qty')
            l1=len(ob1)
            l2=len(ob2)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':8,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,
            'l1':l1,'l2':l2,
            }
        if bval=='Proceed7':
            dt1=request.POST.get('datea1')
            dt2=request.POST.get('datea2')
            ob1=WheelMachining.objects.filter(in_qty__range=(dt1,dt2)).values('sno','wheel_no','in_qty').order_by('in_qty')
            ob2=WheelMachining.objects.filter(out_qty__range=(dt1,dt2)).values('sno','wheel_no','out_qty').order_by('out_qty')
            l1=len(ob1)
            l2=len(ob2)
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':9,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            'l1':l1,'l2':l2,
            }
        if bval=='Proceed10':
            mon=request.POST.get('month')
            ob1=WheelMachining.objects.filter(date__contains=mon).values('sno','wheel_no','in_qty','out_qty','pt_no','date').order_by('date')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':11,
            'ob1':ob1,
            'mon':mon,
            }

    return render(request,'wheelreport.html',context)




@login_required
@role_required(urlpass='/bogiereport/')
def bogiereport(request):
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
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=='Month Wise Detail':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':10,
            }
        if bval=='Proceed1':
            dt=request.POST.get('datew')
            ob1=BogieAssembly.objects.filter(in_date=dt).values('sno','pt_no')
            ob2=BogieAssembly.objects.filter(out_qty=dt).values('sno','pt_no')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'ob1':ob1,
            'ob2':ob2,
            'dt':dt,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            ob1=BogieAssembly.objects.filter(in_date__range=(dt1,dt2)).values('sno','pt_no','in_date').order_by('in_date')
            ob2=BogieAssembly.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }
        if bval=='Proceed10':
            mon=request.POST.get('month')
            ob1=BogieAssembly.objects.filter(date__contains=mon).values('sno','axle_no','in_qty','out_qty','pt_no','date').order_by('date')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':11,
            'ob1':ob1,
            'mon':mon,
            }

    return render(request,'bogiereport.html',context)



@login_required
@role_required(urlpass='/pinionreport/')
def pinionreport(request):
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
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=="Traction Motor Detail":
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':4,
            }
        if bval=='Month Wise Detail':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':10,
            }
        if bval=='Proceed1':
            dt=request.POST.get('datew')
            ob1=PinionPressing.objects.filter(in_qty=dt).values('sno','pt_no')
            ob2=PinionPressing.objects.filter(out_qty=dt).values('sno','pt_no')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'ob1':ob1,
            'ob2':ob2,
            'dt':dt,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            ob1=PinionPressing.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','in_qty').order_by('in_qty')
            ob2=PinionPressing.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }
        if bval=='Proceed3':
            dt1=request.POST.get('tmno')
            ob1=PinionPressing.objects.filter(tm_no=dt1).all()
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':5,
            'ob1':ob1,
            'dt1':dt1,'tmno':dt1,
            }
        if bval=='Proceed10':
            mon=request.POST.get('month')
            ob1=PinionPressing.objects.filter(date__contains=mon).values('sno','tm_no','in_qty','out_qty','pt_no','date').order_by('date')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':11,
            'ob1':ob1,
            'mon':mon,
            }

    return render(request,'pinionreport.html',context)




@login_required
@role_required(urlpass='/axlepressreport/')
def axlepressreport(request):
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
    if request.method=="POST":
        bval=request.POST.get('btn')
        if bval=='Date Wise Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':0,
            }
        if bval=='Date Range Report':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':2,
            }
        if bval=="Axle No. Detail":
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':4,
            }
        if bval=='Month Wise Detail':
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':10,
            }
        if bval=='Proceed1':
            dt=request.POST.get('datew')
            ob1=AxleWheelPressing.objects.filter(in_qty=dt).values('sno','pt_no')
            ob2=AxleWheelPressing.objects.filter(out_qty=dt).values('sno','pt_no')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':1,
            'ob1':ob1,
            'ob2':ob2,
            'dt':dt,
            }
        if bval=='Proceed2':
            dt1=request.POST.get('date1')
            dt2=request.POST.get('date2')
            ob1=AxleWheelPressing.objects.filter(in_qty__range=(dt1,dt2)).values('sno','pt_no','in_qty').order_by('in_qty')
            ob2=AxleWheelPressing.objects.filter(out_qty__range=(dt1,dt2)).values('sno','pt_no','out_qty').order_by('out_qty')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':3,
            'ob1':ob1,
            'ob2':ob2,
            'dt1':dt1,'dt2':dt2,
            }
        if bval=='Proceed3':
            dt1=request.POST.get('tmno')
            ob1=AxleWheelPressing.objects.filter(axle_no=dt1).all()
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':5,
            'ob1':ob1,
            'dt1':dt1,'tmno':dt1,
            }
        if bval=='Proceed10':
            mon=request.POST.get('month')
            ob1=AxleWheelPressing.objects.filter(date__contains=mon).values('sno','axle_no','wheel_no','in_qty','out_qty','pt_no','date').order_by('date')
            context={
            'nav':nav,
            'subnav':subnav,
            'usermaster':usermaster,
            'ip':get_client_ip(request),
            'sub':11,
            'ob1':ob1,
            'mon':mon,
            }

 
    return render(request,'axlepress.html',context)



@login_required
@role_required(urlpass='/mgrview/')
def mgrview(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = ms_tools_master.objects.all().filter(shop_code=rolelist[i]).values('instrument_number').distinct()
            instrument_number = instrument_number | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'instrument_number':instrument_number,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
        
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            
            shop_sec = request.POST.get('shop_sec')
            instrument_number = request.POST.get('ins_no')
            print(shop_sec,instrument_number)
            obj = ms_tools_master.objects.filter(shop_code=shop_sec,instrument_number=instrument_number).values('calibration_frequency','employee','user_id').distinct()
            obj1 = Mgr.objects.filter(instrument_number=instrument_number).values('tool_des','type_mme','least_count')
            noprint=0
            print(obj)
            leng = obj.count()
            leng1 = obj1.count()
            if len(obj1) == 0:
                noprint=1
            
            context = {
                        'obj': obj,
                        'obj1': obj1,
                        'len': leng,
                        'len1': leng1,
                        'shop_sec': shop_sec,
                        'instrument_number':instrument_number,
                        'sub' : 1,
                        #'noprint':noprint,
                        'nav':nav,
                        'ip':get_client_ip(request),  
                        'subnav':subnav,
            }
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                    #'noprint':noprint,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    req = ms_tools_master.objects.all().filter(shop_code=rolelist[i]).values('instrument_number').distinct()
                    instrument_number = instrument_number | req
                context = {
                    
                    'lenm' :len(rolelist),
                    'instrument_number':instrument_number,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                    #'noprint':noprint,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
        
            elif(len(rolelist)>1):
                context = {
                    
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                    #'noprint':noprint,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
        if submitvalue =='Submit':
                
                leng=request.POST.get('len')
                now = datetime.datetime.now()
                shop_sec = request.POST.get('shop_sec')
                instrument_number = request.POST.get('ins_no')
                tool_des = request.POST.get('tool_des')
                type_mme = request.POST.get('type_mme')
                least_count = request.POST.get('least_count')
                calibration_frequency = request.POST.get('calibration_frequency')
                employee = request.POST.get('employee')
                #range = request.POST.get('range')
                #periodicity_check = request.POST.get('periodicity_check')
                #date_calibration = request.POST.get('date_calibration')
                #calibration_status = request.POST.get('calibration_status')
                #calibration_due_date = request.POST.get('calibration_due_date')

                mgrobj = Mgr.objects.filter(shop_sec=shop_sec,instrument_number=instrument_number).distinct()
                if len(mgrobj) == 0:
                    
                    Mgr.objects.create(login_id=request.user,shop_sec=str(shop_sec),instrument_number=str(instrument_number),tool_des=str(tool_des),type_mme=str(type_mme),
                    least_count=str(least_count),calibration_frequency=str(calibration_frequency),employee=str(employee),last_modified=str(now))
                
                else:
                    Mgr.objects.filter(shop_sec=shop_sec,instrument_number=instrument_number).update(tool_des=str(tool_des),type_mme=str(type_mme),
                    least_count=str(least_count),calibration_frequency=str(calibration_frequency),employee=str(employee),last_modified=str(now))

                instrument_number=Mgr.objects.all().values('instrument_number').distinct()

        if submitvalue =='Proceed to Report':
            return mgrreports(request)
        

    return render(request,"mgrview.html",context)

def mgrgetinsno(request):
    if request.method == "GET" and request.is_ajax():
        
        shop_sec = request.GET.get('shop_sec')
        instrument_number=list(ms_tools_master.objects.filter(shop_code=shop_sec).values('instrument_number').distinct())
        return JsonResponse(instrument_number, safe = False)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/mgrview/')
def mgrreports(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = ms_tools_master.objects.all().filter(shop_code=rolelist[i]).values('instrument_number').distinct()
            instrument_number = instrument_number | req
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'instrument_number':instrument_number,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
        
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'subnav':subnav,
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed to Report':
            
            shop_sec = request.POST.get('shop_sec')
            instrument_number = request.POST.get('ins_no')
            print(shop_sec,instrument_number)
            obj = Mgr.objects.filter(shop_sec=shop_sec).values('instrument_number').distinct()
            obj1 = mgrreport.objects.filter(shop_sec=shop_sec,instrument_number=instrument_number).values('tool_des','range','periodicity_check','date_calibration','calibration_status','calibration_due_date')
            noprint=0
            print(obj)
            leng = obj.count()
            leng1 = obj1.count()
            if len(obj1) == 0:
                noprint=1
            
            context = {
                        'obj': obj,
                        'obj1': obj1,
                        'len': leng,
                        'len1': leng1,
                        'shop_sec': shop_sec,
                        'instrument_number':instrument_number,
                        'sub' : 1,
                        'noprint':noprint,
                        'nav':nav,
                        'ip':get_client_ip(request),  
                        'subnav':subnav,
            }
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                    'noprint':noprint,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    req = ms_tools_master.objects.all().filter(shop_code=rolelist[i]).values('instrument_number').distinct()
                    instrument_number = instrument_number | req
                context = {
                    
                    'lenm' :len(rolelist),
                    'instrument_number':instrument_number,
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                    'noprint':noprint,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
        
            elif(len(rolelist)>1):
                context = {
                    
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'obj': obj,
                    'obj1': obj1,
                    'len': leng,
                    'len1': leng1,
                    'shop_sec': shop_sec,
                    'instrument_number':instrument_number,
                    'sub' : 1,
                    'noprint':noprint,
                    'nav':nav,
                    'ip':get_client_ip(request),  
                    'subnav':subnav,
                }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Submit':
            now = datetime.datetime.now()
            shop_sec = request.POST.get('shop_sec')
            instrument_number = request.POST.get('ins_no')
            tool_des = request.POST.get('tool_des')
            range = request.POST.get('range')
            periodicity_check = request.POST.get('periodicity_check')
            date_calibration = request.POST.get('date_calibration')
            calibration_status = request.POST.get('calibration_status')
            calibration_due_date = request.POST.get('calibration_due_date')
            

            mgrobj1 = mgrreport.objects.filter(shop_sec=shop_sec,instrument_number=instrument_number).distinct()
            if len(mgrobj1) == 0:
                    
                    mgrreport.objects.create(login_id=request.user,range=str(range),tool_des=str(tool_des),periodicity_check=str(periodicity_check),shop_sec=str(shop_sec),instrument_number=str(instrument_number),
                    date_calibration=str(date_calibration),calibration_status=str(calibration_status),last_modified=str(now),calibration_due_date=str(calibration_due_date))

            else:

                    mgrreport.objects.filter(shop_sec=shop_sec,instrument_number=instrument_number).update(tool_des=str(tool_des),range=str(range),periodicity_check=str(periodicity_check),
                    date_calibration=str(date_calibration),login_id=request.user,last_modified=str(now),calibration_status=str(calibration_status),calibration_due_date=str(calibration_due_date))

            instrument_number=Mgr.objects.all().values('instrument_number').distinct()

        

    return render(request,"mgrREPORT.html",context)





def mg21getstaff(request):
    if request.method == "GET" and request.is_ajax():

        shop_sec = request.GET.get('shop_sec')

        staff = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
        staff_no = list(staff)
        return JsonResponse(staff_no, safe=False)
    return JsonResponse({"success": False}, status=400)
 
@login_required
@role_required(urlpass='/mg21report/')
def mg21report(request):
    
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    a=0
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = empmast.objects.none()
    if "Superuser" in rolelist:
        obj = list(MG21TAB.objects.values('reportno').distinct())

        context={
            'a':a,
            'sub':0,
            'lenm' :2,
            'obj': obj,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
        }
    
    if request.method == "POST":
        
        submitvalue = request.POST.get('Proceed')
        if submitvalue=='Proceed':
            a=1
            shop_sec = request.POST.get('shop_sec')
            staffNo = request.POST.get('staffNo')
            staffName = request.POST.get('staffName')
            staffDesg = request.POST.get('staffDesg')
            reportdate = request.POST.get('reportdate')
            resumedate = request.POST.get('resumedate')
            sse = request.POST.get('sse')
            reportNumber = request.POST.get('reportNumber')
            login_id = request.POST.get('login_id')
            current_date = request.POST.get('current_date')
           
            obj = list(MG21TAB.objects.filter(reportno=reportNumber).values('reportno','shop_sec','staffNo','staffName','staffDesg','reportdate','resumedate','sse','current_date').distinct())
            
            context = {
                        
                        'a':a,
                        'obj': obj,
                        'shop_sec': shop_sec,
                        'staffNo' :staffNo,
                        'staffName' : staffName,
                        'staffDesg':staffDesg,
                        'reportNumber':reportNumber,
                        'resumedate':resumedate,
                        'reportdate':reportdate,
                        'sse':sse,
                        'login_id':login_id,
                        'current_date' : current_date,
                        'subnav':subnav,
            }                       
    return render(request,"mg21report.html",context)




@login_required
@role_required(urlpass='/mg9initialreportviews/')
def mg9initialreportviews(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = user_master.objects.none()
    tool_no = Tools.objects.values('tool_code').exclude(tool_code__isnull=True).distinct()
    prtlist=[]
    for i in tool_no:
        prtlist.append(i['tool_code'])
    # print(prtlist) 
    ticket_no = empmast.objects.values('ticket_no').exclude(ticket_no__isnull=True).distinct()
    prtticket=[]
    for i in ticket_no:
        prtticket.append(i['ticket_no'])
    #print(prtticket)   
    empno = empmast.objects.filter(payrate__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtemp=[]
    for i in empno:
        prtemp.append(i['empno'])
    # print(prtemp)
    empno = empmast.objects.filter(scalecode__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtsec=[]
    for i in empno:
        prtsec.append(i['empno'])
    #print(prtsec)  
    if "Superuser" in rolelist:
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
           
            'roles':tmp,
            'subnav':subnav,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,

        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,    
            'prtemp':prtemp,
            'prtsec':prtsec,
                }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mw_no = request.POST.get('mwno')
            staff_no = request.POST.get('staffno')
        

           

            print(mw_no)
            print(staff_no)
            print(mw_no)
            obj  = MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).values('sec','mw_no','sl_no','staff_no','handed_date','comp_date','handed_time','comp_time','handed_cmsec','comp_cmsec','handed_cmserv','comp_cmserv','complaint','action').distinct()
            obj1  = MG9Initial.objects.values('id').count()

            print("count")
            print(obj1)
            leng = obj.count()
            slno=obj1
            slno=slno+1
            print(slno)
            

            
            if "Superuser" in rolelist:
                    tm=M5SHEMP.objects.all().values('shopsec').distinct()
                    tmp=[]
                    for on in tm:
                        tmp.append(on['shopsec'])
                    context={
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,   
                        # 'len1':leng1,  
                        'obj':obj,
                        # 'obj1':obj1,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'slno':slno,
                       
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                        'prtlist':prtlist,
                        'prtticket':prtticket,
                        'prtemp':prtemp,
                        'prtsec':prtsec,



                    }
            elif(len(rolelist)==1):
                    # print("in m5 else")
                    for i in range(0,len(rolelist)):
                        req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
                        wo_nop =wo_nop | req
                    context = {
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,
                        'obj':obj,
                        'slno':slno,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                     
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                    }
            elif(len(rolelist)>1):
                    context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'len':leng,
                        'obj':obj,
                        'slno':slno,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                  
                        #'assm_no':assm_no,
                        'subnav':subnav
                    }    
        if submitvalue=='submit':
                    leng=request.POST.get('len')
                    now = datetime.datetime.now()
                    # shop_sec = request.POST.get('shop_sec')
                    shop_sec=request.POST.get('shop_sec')
                    mw_no = request.POST.get('mw_no')
                    staff_no = request.POST.get('staff_no')
                    comp= request.POST.get('complaint')
                    date_handed=request.POST.get('date_handed')
                    date_com=request.POST.get('date_com')
                    time_handed=request.POST.get('time_handed')
                    time_com=request.POST.get('time_com')
                    sec_handed = request.POST.get('sec_handed')
                    sec_com = request.POST.get('sec_com')
                    serv_com = request.POST.get('serv_com')
                    serv_handed = request.POST.get('serv_handed')
                    action= request.POST.get('action')
                    sl_no = request.POST.get('sl_no')

          

                    mg9obj = MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).distinct()
                    if len(mg9obj) == 0:

                        print(now)
                        print(sl_no)
                        # print(shop_sec)
                        print(shop_sec)
                        print(mw_no)
                        print(staff_no)
                        print(date_handed)
                        print(date_com)
                        print(time_handed)
                        print(time_com)
                        print(sec_handed)
                        print(sec_com)
                        print(serv_handed)
                        print(serv_com)
                        print(action)
                        print(comp)

                        MG9Initial.objects.create(sec=str(shop_sec),mw_no=str(mw_no),sl_no=str(sl_no),staff_no=str(staff_no),complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=request.user)
                    else:

                        MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).update(complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now))
                       
                        print(now)
                        print(sl_no)
                        # print(shop_sec)
                        print(shop_sec)
                        print(mw_no)
                        print(staff_no)
                        print(date_handed)
                        print(date_com)
                        print(time_handed)
                        print(time_com)
                        print(sec_handed)
                        print(sec_com)
                        print(serv_handed)
                        print(serv_com)
                        print(action)
                        print(comp)

    return render(request,"mg9initialreportviews.html",context)

def mg9getmw(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(Lc1.objects.filter(shop_sec = shop_sec).values('lcno').distinct())
        return JsonResponse(wono, safe = False)        
    return JsonResponse({"success":False}, status=400)

def mg9getstaff(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        staff = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(staff, safe = False)
    return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/mg9compreportviews/')
def mg9compreportviews(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = user_master.objects.none()
    tool_no = Tools.objects.values('tool_code').exclude(tool_code__isnull=True).distinct()
    prtlist=[]
    for i in tool_no:
        prtlist.append(i['tool_code'])
    # print(prtlist) 
    ticket_no = empmast.objects.values('ticket_no').exclude(ticket_no__isnull=True).distinct()
    prtticket=[]
    for i in ticket_no:
        prtticket.append(i['ticket_no'])
    #print(prtticket)   
    empno = empmast.objects.filter(payrate__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtemp=[]
    for i in empno:
        prtemp.append(i['empno'])
    # print(prtemp)
    empno = empmast.objects.filter(scalecode__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtsec=[]
    for i in empno:
        prtsec.append(i['empno'])
    #print(prtsec)  
    if "Superuser" in rolelist:
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
           
            'roles':tmp,
            'subnav':subnav,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,

        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,    
            'prtemp':prtemp,
            'prtsec':prtsec,
                }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mw_no = request.POST.get('mwno')
            staff_no = request.POST.get('staffno')
            
            current_yr=int(datetime.datetime.now().year)


            print("Current year",current_yr)

            print(mw_no)
            print(staff_no)
            print(mw_no)
            obj  = MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).values('sec','mw_no','sl_no','staff_no','handed_date','comp_date','handed_time','comp_time','handed_cmsec','comp_cmsec','handed_cmserv','comp_cmserv','complaint','action','total_losthrs','cause_hrs','mp_time','mismp_time','inv_time').distinct()
            obj1  = MG9Complete.objects.values('id').count()
            print("OBJ")
            print(obj)
            print("count")
            print(obj1)
            leng = obj.count()
            slno=obj1
            slno=slno+1
            print(slno)
     
            if "Superuser" in rolelist:
                    tm=M5SHEMP.objects.all().values('shopsec').distinct()
                    tmp=[]
                    for on in tm:
                        tmp.append(on['shopsec'])
                    context={
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,   
                        # 'len1':leng1,  
                        'obj':obj,
                        # 'obj1':obj1,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'slno':slno,
                        'cyear':current_yr,
                       
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                        'prtlist':prtlist,
                        'prtticket':prtticket,
                        'prtemp':prtemp,
                        'prtsec':prtsec,



                    }
            elif(len(rolelist)==1):
                    # print("in m5 else")
                    for i in range(0,len(rolelist)):
                        req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
                        wo_nop =wo_nop | req
                    context = {
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        'len':leng,
                        'obj':obj,
                        'slno':slno,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'cyear':current_yr,
                     
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                    }
            elif(len(rolelist)>1):
                    context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'len':leng,
                        'obj':obj,
                        'slno':slno,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'staff_no': staff_no,
                        'cyear':current_yr,
                  
                        #'assm_no':assm_no,
                        'subnav':subnav
                    }    
        if submitvalue=='submit':
                    leng=request.POST.get('len')
                    now = datetime.datetime.now()
                    shop_sec=request.POST.get('shop_sec')
                    mw_no = request.POST.get('mw_no')
                    staff_no = request.POST.get('staff_no')
                    comp= request.POST.get('complaint')
                    date_handed=request.POST.get('date_handed')
                    date_com=request.POST.get('date_com')
                    time_handed=request.POST.get('time_handed')
                    time_com=request.POST.get('time_com')
                    sec_handed = request.POST.get('sec_handed')
                    sec_com = request.POST.get('sec_com')
                    serv_com = request.POST.get('serv_com')
                    serv_handed = request.POST.get('serv_handed')
                    action= request.POST.get('action')
                    sl_no = request.POST.get('sl_no')
                    lost_hrs = request.POST.get('lost_hrs')
                    elec = request.POST.get('elec')
                    mech = request.POST.get('mech')
                    mech_ele = request.POST.get('mech_ele')
                    mp = request.POST.get('mp')
                    inv = request.POST.get('inv')
                    mismp = request.POST.get('mismp')
                    # time_hrs=request.POST.get('time_hrs')
                    inv_time = request.POST.get('inv_time')
                    mismp_time = request.POST.get('mismp_time')
                    mp_time=request.POST.get('mp_time')



                   

                    print(sl_no)
                    print(shop_sec)
                    print(mw_no)
                    print(staff_no)
                    print(date_handed)
                    print(date_com)
                    print(time_handed)
                    print(time_com)
                    print(sec_handed)
                    print(sec_com)
                    print(serv_handed)
                    print(serv_com)
                    print(action)
                    print(comp)
                    print(lost_hrs)
                    print(elec)
                    print(mech)
                    print(mech_ele)
                    print(mp)
                    print(inv)
                    print(mismp)
                    print("mp_time",mp_time)
                    print("mismp_time",mismp_time)
                    print("inv_time",inv_time)
                    tmp=""
                    if(elec is not None):
                        tmp=str(elec)+str("   ")
                    if(mech is not None):
                        tmp=tmp+str(mech)+str("   ")
                    if(mech_ele is not None):
                        tmp=tmp+str(mech_ele)+str("   ")
                    if(mp is not None):
                        tmp=tmp+str(mp)+str("   ")
                    if(inv is not None):
                        tmp=tmp+str(inv)+str("   ")
                    print(tmp)
                    if(mp_time is None):
                        mp_time='00:00'
                        print("mp_time",mp_time)
                    if(inv_time is None):
                        inv_time='00:00'
                        print("inv_time",inv_time) 
                    if(mismp_time is None):
                        mismp_time='00:00'
                        print("mismp_time",mismp_time)        
                   

                    mg9obj = MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).distinct()
                    if len(mg9obj) == 0:

        #                 print(now)
        #                 print(sl_no)
        #                 # print(shop_sec)
        #                 print(shop_sec)
        #                 print(mw_no)
        #                 print(staff_no)
        #                 print(date_handed)
        #                 print(date_com)
        #                 print(time_handed)
        #                 print(time_com)
        #                 print(sec_handed)
        #                 print(sec_com)
        #                 print(serv_handed)
        #                 print(serv_com)
        #                 print(action)
        #                 print(comp)

                    
                        MG9Complete.objects.create(sec=str(shop_sec),mw_no=str(mw_no),sl_no=str(sl_no),staff_no=str(staff_no),complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=request.user,total_losthrs=str(lost_hrs),cause_hrs=str(tmp),mp_time=str(mp_time),inv_time=str(inv_time),mismp_time=str(mismp_time))
                    else:
                        cause=request.POST.get('cause_hrs')

                        MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).update(complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=str(request.user),total_losthrs=str(lost_hrs),cause_hrs=str(cause),mp_time=str(mp_time),inv_time=str(inv_time),mismp_time=str(mismp_time))
                       
        #                 print(now)
        #                 print(sl_no)
        #                 # print(shop_sec)
        #                 print(shop_sec)
        #                 print(mw_no)
        #                 print(staff_no)
        #                 print(date_handed)
        #                 print(date_com)
        #                 print(time_handed)
        #                 print(time_com)
        #                 print(sec_handed)
        #                 print(sec_com)
        #                 print(serv_handed)
        #                 print(serv_com)
        #                 print(action)
        #                 print(comp)

    return render(request,"mg9compreportviews.html",context)

# def mg9getmwno(request):
#     if request.method == "GET" and request.is_ajax():
#         shop_sec = request.GET.get('shop_sec')
#         # print(shop_sec)
#         wono = list(Mnp.objects.filter(shopsec = shop_sec).values('mwno').distinct())
#         print("wono",wono)
#         return JsonResponse(wono, safe = False)
#     return JsonResponse({"success":False}, status=400)


def mg9getstaffno(request):
    if request.method == "GET" and request.is_ajax():
        # staff_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        staff = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        print(staff)
        return JsonResponse(staff, safe = False)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/partallotement/')
def partallotement(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist) 
    partnew = list(Partnew.objects.all().values('part_no').distinct())
    partgrp = list(Ngr.objects.all().values('mgr').distinct())
    subgrp2 = list(Ngr.objects.all().values('sgr2','sln'))
    it_cat = list(GmCode.objects.filter(cd_type='IT').values('alpha_1').distinct())
    unit = list(GmCode.objects.filter(cd_type='UT').values('alpha_1').distinct())
    MB = list(GmCode.objects.filter(cd_type='MB').values('alpha_1').distinct())

    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
            'partnew' : partnew,
            'partgrp' : partgrp,
            'it_cat' : it_cat,
            'unit' : unit,
            'mb' : MB,
            'subgrp2': subgrp2, 
        }
   
    return render(request,"partallotement.html",context)


def getpartnewdetails(request):
    if request.method == "GET" and request.is_ajax():        
        partno_temp = request.GET.get("partno_temp")
        
        partnew = list(Partnew.objects.filter(part_no=partno_temp).values('gm_ptno','rev','des','mb','unit','size_pc','mat_specn','ind_buy','it_cat','unit_wt').distinct())

        print('partnew : ----',partnew)
        return JsonResponse(partnew, safe = False)
    return JsonResponse({"success":False}, status=400)

def getpartnewdetails123(request):
    if request.method == "GET" and request.is_ajax():        
        partgrp_temp = request.GET.get("maj_grp_temp")        
        partgrp = list(Ngr.objects.filter(mgr = partgrp_temp).values('sgr1').distinct())
        return JsonResponse(partgrp, safe = False)
    return JsonResponse({"success":False}, status=400)

def getsubgrp2(request):
    if request.method == "GET" and request.is_ajax():
        subgrp_temp_temp = request.GET.get("subgrp_temp_temp")  
        subgrp2 = list(Ngr.objects.filter(sgr1 = subgrp_temp_temp).values('sgr2').exclude(sgr2__isnull=True))
        print("subgrp2 : ", subgrp2)
        return JsonResponse(subgrp2, safe = False)
    return JsonResponse({"success":False}, status=400)

def getDiscription(request):
    if request.method == "GET" and request.is_ajax():
        SUB_GROUP2_temp = request.GET.get("SUB_GROUP2_temp")  
        subgrpDesc = list(Ngr.objects.filter(sgr2 = SUB_GROUP2_temp).values('sln','gdes').exclude(sgr2__isnull=True))
        print("subgrpDesc : ", subgrpDesc)
        return JsonResponse(subgrpDesc, safe = False)
    return JsonResponse({"success":False}, status=400)

def getpartdecription(request):
    if request.method == "GET" and request.is_ajax():        
        subgrp_temp_temp = request.GET.get("subgrp_temp")        
        partgrp = list(Ngr.objects.filter(gdes = subgrp_temp_temp).values('gdes'))
        print("partgrp : ", partgrp)
        return JsonResponse(partgrp, safe = False)
    return JsonResponse({"success":False}, status=400)

def GenerateNewPartNo(request):
    if request.method == "GET" and request.is_ajax():        
        majg = request.GET.get("majg")  
        subg1= request.GET.get("subg1")
        subg2= request.GET.get("subg2")
        sl_no= request.GET.get("sl_no")
        lst=[majg,subg1,subg2,sl_no]
        part=''.join(map(str,lst))
        lst=[]
        for i in range(0,len(part)):
            lst.insert(i,int(part[i]))
        sum=0 
        cal=8
        for i in range(0,7):
            sum=sum + (lst[i] * cal)
            cal= cal - 1
        mod = sum % 11
        lst.insert(len(lst),mod) 
        part=''.join(map(str,lst)) 
        print(part)   
        print("new part no generated: ")
        return JsonResponse(part, safe = False)
    return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/staff_auth_view/')
def staff_auth_view(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    tm1=empmast.objects.all().filter(payrate__gt='4200').values('empno').distinct()

    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    staff_no = empmast.objects.none()
    if "Superuser" in rolelist:
        tm=Shemp.objects.all().values('shopsec').distinct()
        sh=Shemp.objects.all().values('staff_no','name').distinct()
        
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sh':sh,
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'tm1':tm1,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = Shemp.objects.all().filter(shop_sec=rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'staff_no':staff_no,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')

        if submitvalue=='submit':
            shop_sec = request.POST.get('shop_sec')
            totauth = request.POST.get('totauth')
            totstaff = request.POST.get('totstaff')
            empno_shop_mang = request.POST.get('empno_shop_mang')
            empno_sse = request.POST.get('empno_sse')
            date_shop_mang = request.POST.get('date_shop_mang')
            date_sse = request.POST.get('date_sse')
            now = datetime.datetime.now()
            user=request.user
            form=staff_auth.objects.all().values('form_id').distinct().order_by('-form_id')
            if(form.count()==0):
                formid=1
            else:
                formid=form[0]['form_id']
                formid=int(formid)+1
            print("form ",formid)
            
            print(shop_sec,totauth,empno_shop_mang,empno_sse,totstaff)
            j=0
            auth=""
            for i in range(0,int(totauth)+1):
                auth1 = request.POST.get('auth'+str(i))
                if(auth1!=None):
                    auth=auth1+", "
                    print("auth ",auth)
                    j=i
                    break
                   
                
            for i in range(j+1,int(totauth)+1):
                auth1 = request.POST.get('auth'+str(i))
                auth=auth+auth1+", "
            auth=auth[:len(auth)-2]
            print("auth",auth)
            k=0
            no=0
            for i in range(0,int(totstaff)+1):
                staff_no = request.POST.get('staff_no'+str(i))
                staff_name = request.POST.get('staff_name'+str(i))
                staff_sec = request.POST.get('staff_sec'+str(i))
                mwnoj=""
                for j in range(1,3):
                    mwnoj1 = request.POST.get('mwno'+str(i)+str(j))
                    if mwnoj1 !=None:
                        mwnoj=mwnoj1+", "
                        k=j
                        break
                for j in range(k+1,10):
                    mwnoj1 = request.POST.get('mwno'+str(i)+str(j))
                    if mwnoj1!=None:
                        mwnoj=str(mwnoj)+str(mwnoj1)+", "
                mwnoj=mwnoj[:len(mwnoj)-2]
                # print(shop_sec,staff_no,auth,"fdc",mwnoj,empno_shop_mang,date_shop_mang ,empno_sse,date_sse)
                if(staff_no!=None):
                    no=no+1
                    staff_auth.objects.create(form_id=str(formid), srno=str(no), shopsec=str(shop_sec),staff_no=str(staff_no),staff_name=str(staff_name), auth=str(auth), mwno=str(mwnoj), empno_shop_mang=str(empno_shop_mang), date_shop_mang=str(date_shop_mang), empno_sse=str(empno_sse), date_sse=str(date_sse), psnt_date=str(now)     ,login_id=str(user), last_modified=str(now))
                
    return render(request,"staff_auth_view.html",context)    
  
def staff_auth_viewgetshop_name(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        # tablecolumnname=same var name
        shop_name = Shop.objects.filter(shop=shop_sec).values('sh_desc').distinct()
        wono =(shop_name[0].get('sh_desc')).strip()

        mnno=list(Mnp.objects.filter(location=wono).values('mwno').distinct())
        # print("mnno",mnno,wono,type(wono))
        cont ={
            "wono":wono,
            "mno":mnno,
        }
        
        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)
def staff_auth_viewgetstaff_name(request):
    if request.method == "GET" and request.is_ajax():
        staff_no = request.GET.get('staff_no')
        name = list(Shemp.objects.filter(staff_no=staff_no).values('name').distinct())
        wono = name[0]['name']
        cont ={
            "wono":wono,
        }

        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)

def staff_auth_viewgetemp_name(request):
    if request.method == "GET" and request.is_ajax():
        emp_no = request.GET.get('emp_no')
        
        name = list(empmast.objects.filter(empno=emp_no).values('empname','desig_longdesc').distinct())
        wono1 = name[0]['empname']
        wono2= name[0]['desig_longdesc']
        print(emp_no)
        cont ={
            "wono1":wono1,
            "wono2":wono2,
        }

        return JsonResponse({"cont":cont}, safe = False)
    return JsonResponse({"success":False}, status=400)


    

@login_required
@role_required(urlpass='/staff_auth_report_view/')
def staff_auth_report_view(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    tm1=empmast.objects.all().filter(payrate__gt='4200').values('empno').distinct()

    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    staff_no = empmast.objects.none()
    if "Superuser" in rolelist:
        tm=Shemp.objects.all().values('shopsec').distinct()
        sh=Shemp.objects.all().values('staff_no','name').distinct()
        formno=staff_auth.objects.all().values('form_id').distinct().order_by('form_id')
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sh':sh,
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'tm1':tm1,
            'formno':formno,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = Shemp.objects.all().filter(shop_sec=rolelist[i]).values('staff_no').distinct()
            staff_no =staff_no | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'staff_no':staff_no,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        print("xs",submitvalue)
        if(submitvalue=='Proceed'):
            shop_sec = request.POST.get('shop_sec')
            formno = request.POST.get('formno1')
            shop_name = Shop.objects.filter(shop=shop_sec).values('sh_desc').distinct()
            wono =(shop_name[0].get('sh_desc')).strip()
            alldata=staff_auth.objects.filter(form_id=formno,shopsec=shop_sec).values('srno','shopsec','staff_no','staff_name','auth','mwno','empno_shop_mang','date_shop_mang','empno_sse','date_sse').distinct().order_by('form_id')
            print("all", alldata,formno,shop_sec)
            auth=alldata[0]['auth']
            empnomanager=alldata[0]['empno_shop_mang']
            datemanager=alldata[0]['date_shop_mang']
            sse=alldata[0]['empno_sse']
            datesse=alldata[0]['date_sse']

            mana =empmast.objects.filter(empno=empnomanager).values('empname').distinct()[0]
            ss =empmast.objects.filter(empno=sse).values('empname').distinct()[0]
            
            # wono1 = name[0]['empname']
            context = {
                'alldata':alldata,
                'auth':auth,
                'nav':nav,
                'subnav':subnav,
                'ip':get_client_ip(request),
                'roles' :rolelist,
                'wono':wono,
                'manager':mana,
                'datemanager':datemanager,
                'sse':ss,
                'datesse':datesse,
                'form':formno,
            }
                        
            
    return render(request,"staff_auth_report_view.html",context) 


@login_required
@role_required(urlpass='/logbook_record/')
def logbook_record(request):
    from .models import logbook_record


    if request.method=="POST":
        #m_w_no=request.POST.get(m_w_no)
        #obj=logbook_record.objects.filter(m_w_no=m_w_no)
        obj=logbook_record.objects.create()
        obj.m_w_no=request.POST.get('m_w_no')
        obj.job_booked=request.POST.get('job_booked')
        obj.staff_no=request.POST.get('staff_no')
        obj.attandance=request.POST.get('attandance')
        obj.out_turn=request.POST.get('out_turn')
        obj.remarks=request.POST.get('remarks')
        obj.save()
    return render(request,"logbook_record.html",{})

@login_required
@role_required(urlpass='/logbook_delete/')
def logbook_delete(request):
    from .models import logbook_record

    if request.method=="POST":
        var=request.POST.get('del1')
        obj=logbook_record.objects.filter(m_w_no=var)
        obj.delete()
    return render(request,"logbook_delete.html",{}) 

@login_required
@role_required(urlpass='/logbook_update/')
def logbook_update(request):

    if request.method=="POST":
        
        obj=logbook_record.objects.create()
        obj.m_w_no=request.POST.get('m_w_no')
        obj.job_booked=request.POST.get('job_booked')
        obj.staff_no=request.POST.get('staff_no')
        obj.attandance=request.POST.get('attandance')
        obj.out_turn=request.POST.get('out_turn')
        obj.remarks=request.POST.get('remarks')
        obj.save()
        logbook_record.objects.filter(m_w_no=obj.m_w_no).update(job_booked=obj.job_booked,staff_no=obj.staff_no,attandance=obj.attandance,out_turn=obj.out_turn,remarks=obj.remarks)
        
    return render(request,"logbook_update.html",{})




@login_required
@role_required(urlpass='/m2hwview/')
def m2hwview(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = user_master.objects.none()  
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]        
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):        

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
            context = {
                'sub':0,
                'subnav':subnav,
                'lenm' :len(rolelist),
                'wo_nop':wo_nop,
                'nav':nav,
                'ip':get_client_ip(request),
                'usermaster':usermaster,
                'ip':get_client_ip(request),
                'usermaster':usermaster,
                'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            brn_no = request.POST.get('br_no')
            assembly_no = request.POST.get('assm_no')
            doc_no = request.POST.get('doc_no')
            kkk=Oprn.objects.all()
            obj1 = Part.objects.filter(partno=part_no).values('des', 'drgno').distinct()
            obj2 = Part.objects.filter(partno=assembly_no).values('des').distinct()          
            obj3 = Batch.objects.filter(bo_no=wo_no,brn_no=brn_no,part_no=assembly_no).values('batch_type')
            check_obj=Oprn.objects.all().filter(shop_sec=shop_sec)            
            obj = Oprn.objects.filter(part_no=part_no).values('opn', 'shop_sec', 'lc_no', 'des','pa','at','lot','mat_rej','qtr_accep', 'qty_prod','work_rej').order_by('opn')
            date = M2Doc.objects.filter(m2sln=doc_no).values('m2prtdt','qty').distinct()
            leng = obj.count()
            datel= date.count()

            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'len': leng,
                        'date': date,
                        'datel': datel,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'brn_no': brn_no,
                        'assembly_no': assembly_no,
                        'doc_no': doc_no,
                        'subnav':subnav
                  }
            elif(len(rolelist)==1):
                  for i in range(0,len(rolelist)):                        

                        w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                        req = M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
                        wo_nop = wo_nop | req

                  context = {
                        'wo_nop':wo_nop,
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'len': leng,
                        'date': date,
                        'datel': datel,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'brn_no': brn_no,
                        'assembly_no': assembly_no,
                        'doc_no': doc_no,
                        'subnav':subnav
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'len': leng,
                        'date': date,
                        'datel': datel,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        'brn_no': brn_no,
                        'assembly_no': assembly_no,
                        'doc_no': doc_no,
                        'subnav':subnav
                  }
        
        rand = random.choice('0123456789') 
        rand1 = random.choice('0123456789')
        rand2 = random.choice('0123456789')
        rand3 = random.choice('0123456789')
        rand4 = random.choice('0123456789')
        rand5 = random.choice('0123456789')
        num = rand + rand1 + rand2 + rand3 + rand4 + rand5    
        print(rand + rand1 + rand2 + rand3 + rand4 + rand5)

        if submitvalue=='Save':
            leng=request.POST.get('len')
              
            for i in range(1, int(leng)+1):           
                
                shopsec= request.POST.get('shopsec')
                partno= request.POST.get('partno')
                prtDate     = request.POST.get('prtDate')                                          
                monthTemp = prtDate.split(' ')[0]            
                dateTemp = prtDate.split(' ')[1]                    
                final1 = monthTemp[0:3]+' '+dateTemp.split(',')[0]+' '+prtDate.split(' ')[2]                              
                date_time_str = final1
                date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y')
                print('Date:', date_time_obj.date())

                workOrdNo   = request.POST.get('workOrdNo')
                brnNo       = request.POST.get('brnNo')
                orderQuantity= request.POST.get('orderQuantity')
                asmlyPartNo = request.POST.get('asmlyPartNo')
                asmlyDesc   = request.POST.get('asmlyDesc')
                shopSection = request.POST.get('shopSection')
                partNum     = request.POST.get('partNum')
                partDescription= request.POST.get('partDescription')
                drawingNum  = request.POST.get('drawingNum')
                documentNum = request.POST.get('documentNum')
                orderType   = request.POST.get('orderType')          
                number   = num  
                causesofHW  =   request.POST.get('causesofHW')    

                operationNum=request.POST.get('operationNum'+str(i)) 
                shopSecTemp=request.POST.get('shopSecTemp'+str(i)) 
                loadCenter=request.POST.get('loadCenter'+str(i)) 
                operationDescription=request.POST.get('operationDescription'+str(i)) 
                paTemp=request.POST.get('paTemp'+str(i)) 
                taTemp=request.POST.get('taTemp'+str(i))
                noTemp=request.POST.get('noTemp'+str(i))    
                qtypr=request.POST.get('qtypr'+str(i))
                qtyac = request.POST.get('qtyac'+str(i))
                wrrej = request.POST.get('wrrej'+str(i))
                matrej = request.POST.get('matrej'+str(i))               

                M2HW.objects.create(prtDate=str(date_time_obj.date()),workOrdNo=str(workOrdNo),brnNo=str(brnNo),orderQuantity=str(orderQuantity),asmlyPartNo=str(asmlyPartNo),asmlyDesc=str(asmlyDesc),shopSection=str(shopSection),partNum=str(partNum),partDescription=str(partDescription),drawingNum=str(drawingNum),documentNum=str(documentNum),orderType=str(orderType),operationNum=str(operationNum),shopSecTemp=str(shopSecTemp),loadCenter=str(loadCenter),operationDescription=str(operationDescription),paTemp=str(paTemp),taTemp=str(taTemp),noTemp=str(noTemp),qtypr=str(qtypr),qtyac=str(qtyac),wrrej=str(wrrej),matrej=str(matrej),number=str(number),causesofHW=str(causesofHW))

            messages.success(request, 'M2 Card Hand Written generated Successfully, Your Reference number is : '+number)
    return render(request, "m2hwview.html", context)



def m2getwonohw(request):
    if request.method == "GET" and request.is_ajax():
        from.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1=Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2=M2Doc.objects.filter(part_no__in=w1).values('batch_no').distinct()
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)

def m2getbrhw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        br_no = list(M2Doc.objects.filter(batch_no =wo_no).values('brn_no').distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m2getasslyhw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        w2=M2Doc.objects.filter(batch_no=wo_no).values('assly_no').distinct()
        w1=Oprn.objects.filter(part_no__in=w2).values('shop_sec', 'part_no').distinct()
        print(w1)
        w3=w1.filter(shop_sec=shop_sec).values('part_no').distinct()
        w4=M2Doc.objects.filter(batch_no=wo_no, f_shopsec=shop_sec, brn_no=br_no).values('assly_no').distinct()
        w5=w3.union(w4)
        w6=w5.distinct()
        print(w6)
        assm_no = list(w6)
        return JsonResponse(assm_no, safe=False)
    return JsonResponse({"success":False}, status=400)    

def m2getpart_nohw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        w2 = M2Doc.objects.filter(batch_no=wo_no).values('part_no').distinct()
        w1 = Oprn.objects.filter(part_no__in=w2).all().distinct()
        w3= w1.filter(shop_sec=shop_sec).values('part_no').distinct()
        w4 = M2Doc.objects.filter(batch_no=wo_no, f_shopsec=shop_sec, brn_no=br_no,assly_no=assembly_no).values('part_no').distinct()
        w5=w3.union(w4)
        w6=w5.distinct()
        part_no = list(w6)
        return JsonResponse(part_no, safe=False)
    return JsonResponse({"success":False}, status=400)    

def m2getdoc_nohw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        # br_no = request.GET.get('brn_no')
        # shop_sec = request.GET.get('shop_sec')
        # assembly_no = request.GET.get('assm_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M2Doc.objects.filter(batch_no=wo_no,part_no=part_no).values('m2sln').distinct())

        return JsonResponse(doc_no, safe=False)
    return JsonResponse({"success": False}, status=400) 








@login_required
@role_required(urlpass='/m18aview/')
def m18aview(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()

    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)

    wo_nop = user_master.objects.none()
  
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,

            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,

            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    if request.method == "POST":
        #print("hi")
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            from decimal import Decimal
            #print("ii")
            shop_sec = request.POST.get('shop_sec')
            wo_no = request.POST.get('wo_no')
            br_no= request.POST.get('br_no')
            part_no = request.POST.get('part_nop')
            month = request.POST.get('month')
            staff_no = request.POST.get('sse')
            ticket_no = request.POST.get('ticket_no')
            oprn_no = request.POST.get('oprn_no')

            ty=str(staff_no)
            staff=ty[6:11]
            staff=Shemp.objects.filter(shopsec=shop_sec,staff_no=staff).values('cat').exclude(staff_no__isnull=True)[0]
            print(staff,"staff")
           
        
            
            print(shop_sec)
            print(wo_no)
            print(month)
            print(part_no)
            print(staff_no,"sse")
            obj3=0
            obj2=0
            p=None
            obj1=M18DOC.objects.filter(shopsec=shop_sec,month=month,staff_no=staff_no).all()
            if len(obj1):
              obj3=M18DOC.objects.filter(shopsec=shop_sec,month=month,staff_no=staff_no).values('req_no')[0]
            obj4=0
            obj2=Oprn.objects.filter(shop_sec=shop_sec,part_no=part_no).values('opn').distinct()
            # obj4=Shemp.objects.filter(staff_no=staff).values('cat')[0]

            emp=empmast.objects.filter(empno=staff_no).values('empno').distinct()
            empno=[]
            for i in emp:
                empno.append(i['empno'])

         


            print(obj2)
            print(obj1)
            print(obj3)
            print(obj4)
            leng=obj1.count()
            leng2=obj2.count()
           # print(obj1[0]['total_time'])
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context={
                    'len' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles':tmp,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'obj4':obj4,
                    'len2':leng2,
                    'p':p,
                    'lent': leng,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'part_no':part_no,
                    'staff':staff,
                    # 'prtstaff':prtstaffno,
                    'ticket_no':ticket_no,
                    'month': month,
                    'empno':empno,
                    'oprn_no':oprn_no,
                    'sub':1,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):
                    w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
                    wo_no =wo_no | req
                context = {
                    'len' :len(rolelist),
                    'wo_no':wo_no,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles' :rolelist,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'obj4':obj4,
                    'lent': leng,
                    'len2':leng2,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff':staff,
                    'oprn_no':oprn_no,
                    'empno':empno,
                    'part_no':part_no,
                    'p':p,
                    # 'prtstaff':prtstaffno,
                    'ticket_no':ticket_no,
                    'month': month,
                    'sub':1,
                }
            elif(len(rolelist)>1):
                context = {
                    'len' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'roles' :rolelist,
                    'obj1': obj1,
                    'obj2':obj2,
                    'obj3':obj3,
                    'obj4':obj4,
                    'len2':leng2,
                    'lent': leng,
                    # 'prtstaff':prtstaffno,
                    'shop_sec': shop_sec,
                    'wo_no': wo_no,
                    'staff_no':staff_no, 
                    'staff':staff,
                    'p':p,
                    'oprn_no':oprn_no,
                    'ticket_no':ticket_no,
                    'part_no':part_no,
                    'month': month,
                    'empno':empno,
                    'sub':1,
                }

        if submitvalue=='submit':
            leng=request.POST.get('len')
            shopsec = request.POST.get('shopsec')
            month1= request.POST.get('month')
            req_no=request.POST.get('req_no')

            # shopsec= request.POST.get('shopsec')
            # staff_no = request.POST.get('staff_no')
            # month = request.POST.get('month')
            inoutnum=request.POST.get("inoutnum")
            print(inoutnum)
            print(month1,"month")
            print(shopsec)
            print("jjj",req_no)
           
            # for i in range(1, int(leng)+1):
            #     in1 = request.POST.get('in1'+str(i))
            #     out = request.POST.get('out'+str(i))
            #     in_date = request.POST.get('in_date'+str(i))
            #     month = request.POST.get('month'+str(i))
               
            #     total_time = request.POST.get('total_time'+str(i))
            #     time_hrs = request.POST.get('total_time'+str(i))
            #     idle_time = request.POST.get('idle_time'+str(i))
            #     reasons_for_idle_time = request.POST.get('reasons_for_idle_time'+str(i))
            #     M12DOC1.objects.filter(shopsec=shopsec,staff_no=staff_no,date=date,month=month).update(in_date=str(date),in1=str(in1),out=str(out),month=str(month),total_time=str(total_time),idle_time=str(idle_time),reasons_for_idle_time=str(reasons_for_idle_time),time_hrs=str(time_hrs),amt=str(amt))
               

            for i in range(1, int(inoutnum)+1):
                in1 = request.POST.get('in1add'+str(i))
                
                out = request.POST.get('outadd'+str(i))
                month = request.POST.get('month_add'+str(i))
                total_time = request.POST.get('total_time_add'+str(i))
                in_date = request.POST.get('in_dateadd'+str(i))
                out_date = request.POST.get('out_dateadd'+str(i))
                cat = request.POST.get('catadd'+str(i))
                # time_hrs = request.POST.get('total_time_add'+str(i))
                total_time = request.POST.get('total_time_takenadd'+str(i))
                # reasons_for_idle_time = request.POST.get('reasons_for_idle_timeadd'+str(i))
                shift=request.POST.get('shiftadd'+str(i))
                staff_no=request.POST.get('staff_noadd'+str(i))
                staff_name=request.POST.get('staff_nameadd'+str(i))
                ticket_no=request.POST.get('ticket_noadd'+str(i))
                req_no = request.POST.get('req_no')

                # if len(cat)==1:
                #     cat="0"+cat
                 

                print(staff_no)
                print(staff_name)
                print(in1)
                print(out)
                print(in_date)
                print(out_date)
                print(shift)
                print(total_time)
                print(ticket_no)
                print(cat)
                print(month)
                print(shopsec)
                print(req_no)

                M18DOC.objects.create(shift_typename=str(shift),shopsec=str(shopsec),name=str(staff_name),staff_no=str(staff_no),in1=str(in1),out=str(out),month=str(month1),in_date=str(in_date),cat=str(cat),total_time_taken=str(total_time),out_date=str(out_date),ticket_no=str(ticket_no),req_no=str(req_no))

    #             wo_no=Batch.objects.all().values('bo_no').distinct()
    return render(request,"m18aview.html",context)

def m18getempname(request):
    if request.method == "GET" and request.is_ajax():  
        examcode= request.GET.get('two')
        ex= empmast.objects.filter(empno=examcode).all()
        # print("ONKJJ",obj10[0]['ticket_no'])
        # print(obj10[0].get("ticket_no"))
        
        # print(obj10)
        exam ={
            "exam_type":ex[0].empname,
            
             
           
           
        }    
        print(ex[0].empname)    

        return JsonResponse({"exam":exam}, safe = False)
    return JsonResponse({"success":False}, status=400)   

def m18getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        # print(shop_sec)
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').exclude(batch_no__isnull=True).distinct())
        # print(wono)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)
 


def m18getpart_no(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        # br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        part_no = list(M5DOCnew.objects.filter(batch_no =wo_no,shop_sec=shop_sec).values('part_no').exclude(part_no__isnull=True).distinct())
        print(part_no)
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m18getoprn_no(request):
    if request.method == "GET" and request.is_ajax():
        # wo_no = request.GET.get('wo_no')
        # br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        part_no = request.GET.get('part_nop')
        print(shop_sec)
        print(part_no)
        oprn_no = list(Oprn.objects.filter(part_no=part_no).values('opn').exclude(opn__isnull=True).distinct())
        print(oprn_no)
        return JsonResponse(oprn_no, safe = False)
    return JsonResponse({"success":False}, status=400)  


def m18getticket_no(request):
    if request.method == "GET" and request.is_ajax():
        sse=request.GET.get('sse')
        print(sse,"sse")
        ticket_no = list(empmast.objects.filter(empno=sse).values('ticket_no').exclude(ticket_no__isnull=True).distinct())
        print(ticket_no)
        return JsonResponse(ticket_no, safe = False)
    return JsonResponse({"success":False}, status=400)  


def m18getsse(request):
    if request.method == "GET" and request.is_ajax():
        # wo_no = request.GET.get('wo_no')
        # br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        # staff = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        staff=Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
        prtstaff=[]
        for i in staff:
           ty=i['staff_no']
           pop=empmast.objects.filter(empno__contains=ty).values('empno')
           for i in pop:
            prtstaff.append(i['empno'])

        print("LOST")
        print(prtstaff)   

        context={
            'prt':prtstaff,
        }
        return JsonResponse({'context':context}, safe = False)
    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(urlpass='/M24views/')
def M24views(request):
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
    staff_no = Shemp.objects.values('staff_no').exclude(staff_no__isnull=True).distinct()
    prtlist=[]
    for i in staff_no:
        prtlist.append(i['staff_no'])
    # print(prtlist)    
    
    desgn = Shemp.objects.values('desgn').exclude(desgn__isnull=True).distinct()
    prtdesgn=[]
    for i in desgn:
        prtdesgn.append(i['desgn'])

    payrate = empmast.objects.values('payrate').exclude(payrate__isnull=True).distinct()
    prtpay=[]
    for i in payrate:
        prtpay.append(i['payrate'])

    superv = empmast.objects.values('empno').exclude(scalecode__isnull=True).distinct()
    prtemp=[]
    for i in superv:
        prtemp.append(i['empno'])
    # print(prtemp)

    
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        # print(tm)
        tmp=[]
        
        for on in tm:
            tmp.append(on.section_code)
            # print(tmp)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = M24.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
            # print("role==1 ",rolelist)
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
    elif(len(rolelist)>1):
        print("role > 1 ",rolelist)
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
        
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
       
        if submitvalue=='Proceed':
            fr_date = request.POST.get('fr_date')
            to_date = request.POST.get('to_date')
            shop_sec = request.POST.get('shop_sec')
            ssfo = request.POST.get('ssfo')
            timekeep = request.POST.get('timekeep')
            workshop = request.POST.get('workshop')
            # staff_no = request.POST.get('staff_no')
            # part_no = request.POST.get('part_no')
            print("fr_date: ----------",fr_date)
            
            obj1 = M24.objects.filter(shop_sec=shop_sec,staff_no=ssfo).values('sno','fr_date','to_date','timekeep','workshop','staff_no','desgn','payrate','supervise_chrgmn','hrs_wrked','rsn_ovrtym').distinct()
            print(timekeep)
            
            #     leng = obj1.count()
            #     # leng1 = obj2.count()
            
            
            leng=obj1.count()
            
            context = {
                'obj1': obj1,
                'mytry':"rimjhim",
                'lent': leng,
                # 'lent2': leng1,
                'leng':leng,
                'shop_sec': shop_sec,
                'to_date': to_date,
                'staff_no':staff_no, 
                'ssfo':ssfo,
                'prtlist':prtlist,
                'prtpay':prtpay,
                'prtdesgn':prtdesgn,
                'prtemp':prtemp,
                'timekeep':timekeep,
                'workshop':workshop,
                'fr_date':fr_date,
                'sub': 1, 
                      
            }
    
        print("ghjkl;'",submitvalue)
        if submitvalue=='submit':
            # print("in submit")                               
            leng=request.POST.get('len')
            print("leng=",leng)
            #shop_sec= request.POST.get('shop_sec')
            #staff_no = request.POST.get('staff_no')
            #name = request.Post.get('name')
            tot= request.POST.get('total')
            

            tot = int(tot)+1
            for i in range(1,int(tot)):

                print("aaya1")
                fr_date = request.POST.get('fr_date')
                #print("fr_date  :------- ",fr_date)
                to_date = request.POST.get('to_date')
                #print("to_date  :------- ",to_date)
                shop_sec= request.POST.get('shop_sec')
                ssfo = request.POST.get('ssfo')    
                timekeep = request.POST.get('timekeep')      
                workshop = request.POST.get('workshop')
                #test = request.POST.get('staff_no'+str(i))
                #print("test  : ------------",test)
                sno = request.POST.get('sno'+str(i))
                staff_no = request.POST.get('staff_no')
                designation = request.POST.get('designation')
                payrate = request.POST.get('payrate')
                supervise = request.POST.get('supervise') 
                             
                hrs_wrkd = request.POST.get('hrs_wrkd'+str(i))
                reason = request.POST.get('reason'+str(i))

                print("print here")
                print(fr_date)
                print(to_date)
                print(shop_sec)
                print(staff_no)
                print(designation)
                print(payrate)
                print(supervise)
                print(timekeep)
                print(reason)
                print("hours worked------------",hrs_wrkd)
                M24.objects.create(shop_sec=str(shop_sec),ssfo=str(ssfo),timekeep=str(timekeep),workshop=str(workshop),sno=str(sno),staff_no=str(staff_no),desgn=str(designation),payrate=str(payrate),supervise_chrgmn=str(supervise),hrs_wrked=str(hrs_wrkd),rsn_ovrtym=str(reason),fr_date=str(fr_date),to_date=str(to_date))

    return render(request,"M24views.html",context)                        


def m24getssfo(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        w1=list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())                             
        return JsonResponse(w1, safe = False)
    return JsonResponse({"success":False}, status=400)


def m24getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        #wo_no = request.GET.get('wo_no')
        staff_no = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        #staff_no=list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m24getdesgn(request):
    if request.method == "GET" and request.is_ajax():
        #shop_sec = request.GET.get('shop_sec')
        staff_no = request.GET.get('staff_no')
        w2=list(Shemp.objects.filter(staff_no=staff_no).values('designation').distinct())
        #w2=list(Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('designation').distinct())
        return JsonResponse(w2, safe = False)
    return JsonResponse({"success":False}, status=400)


def m24getsuprvsr(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        #wo_no = request.GET.get('wo_no')
        ss_fo = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        #staff_no=list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(ss_fo, safe = False)
    return JsonResponse({"success":False}, status=400)


# def m24getpayrate(request):
#     if request.method == "GET" and request.is_ajax():
#         shop_sec = request.GET.get('shop_sec')

#         #wo_no = request.GET.get('wo_no')
#         py_rt = list(dlw_empmast.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
#         #staff_no=list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
#         return JsonResponse(staff_no, safe = False)
#     return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/m24report/')
def m24report(request):
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
    staff_no = Shemp.objects.values('staff_no').exclude(staff_no__isnull=True).distinct()
    prtlist=[]
    for i in staff_no:
        prtlist.append(i['staff_no'])
    # print(prtlist)    
    
    desgn = Shemp.objects.values('desgn').exclude(desgn__isnull=True).distinct()
    prtdesgn=[]
    for i in desgn:
        prtdesgn.append(i['desgn'])

    payrate = empmast.objects.values('payrate').exclude(payrate__isnull=True).distinct()
    prtpay=[]
    for i in payrate:
        prtpay.append(i['payrate'])

    superv = empmast.objects.values('empno').exclude(scalecode__isnull=True).distinct()
    prtemp=[]
    for i in superv:
        prtemp.append(i['empno'])
    # print(prtemp)

    
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        # print(tm)
        tmp=[]
        
        for on in tm:
            tmp.append(on.section_code)
            # print(tmp)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = M24.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
            # print("role==1 ",rolelist)
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
    elif(len(rolelist)>1):
        print("role > 1 ",rolelist)
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtpay':prtpay,
            'prtdesgn':prtdesgn,
            'prtemp':prtemp,
        }
        
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
       
        if submitvalue=='Proceed':
            fr_date = request.POST.get('fr_date')
            to_date = request.POST.get('to_date')
            shop_sec = request.POST.get('shop_sec')
            ssfo = request.POST.get('ssfo')
            #timekeep = request.POST.get('timekeep')
            #workshop = request.POST.get('workshop')
            # staff_no = request.POST.get('staff_no')
            obj1=0
            obj2=0
            leng2=0
            obj = M24.objects.filter(shop_sec=shop_sec,ssfo=ssfo).values('timekeep','workshop').distinct()
            #obj1 = M24.objects.filter(shop_sec=shop_sec,staff_no=ssfo).values('sno','fr_date','to_date','timekeep','workshop','desgn','payrate','supervise_chrgmn','hrs_wrked','rsn_ovrtym').distinct()
            obj1 = M24.objects.filter(shop_sec=shop_sec,ssfo=ssfo).values('sno','staff_no','desgn','payrate','supervise_chrgmn','hrs_wrked','rsn_ovrtym').distinct()
            print(obj1)
            if len(obj1):
                staff=obj1[0]['supervise_chrgmn']
                print(staff)
                obj2 = empmast.objects.filter(empno=staff).values('empname').distinct()
                print(obj2)
                leng2=obj2.count()
            #     leng = obj1.count()
            #     # leng1 = obj2.count()
            
            leth=obj.count()
            leng=obj1.count()
            
            
            context = {
                'obj1': obj1,
                'obj': obj,
                'obj2':obj2,
                'leth':leth,
                'len2':leng2,
                'mytry':"rimjhim",
                'lent': leng,
                # 'lent2': leng1,
                'leng':leng,
                'shop_sec': shop_sec,
                'to_date': to_date,
                'staff_no':staff_no, 
                'ssfo':ssfo,
                'prtlist':prtlist,
                'prtpay':prtpay,
                'prtdesgn':prtdesgn,
                'prtemp':prtemp,
                # 'timekeep':timekeep,
                # 'workshop':workshop,
                'fr_date':fr_date,
                'sub': 1, 
                      
            }
    
    return render(request,"m24report.html",context)

 
@login_required
@role_required(urlpass='/machineviews/')
def machineviews(request):
    cuser=request.user
    usermaster=user_master.objects.filter(emp_id=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    wo_nop = user_master.objects.none()
    tool_no = Tools.objects.values('tool_code').exclude(tool_code__isnull=True).distinct()
    prtlist=[]
    for i in tool_no:
        prtlist.append(i['tool_code'])
    # print(prtlist) 
    ticket_no = empmast.objects.values('ticket_no').exclude(ticket_no__isnull=True).distinct()
    prtticket=[]
    for i in ticket_no:
        prtticket.append(i['ticket_no'])
    #print(prtticket)   
    empno = empmast.objects.filter(payrate__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtemp=[]
    for i in empno:
        prtemp.append(i['empno'])
    # print(prtemp)
    empno = empmast.objects.filter(scalecode__gt=4200).values('empno').exclude(empno__isnull=True).distinct()
    prtsec=[]
    for i in empno:
        prtsec.append(i['empno'])
    #print(prtsec)  
    if "Superuser" in rolelist:
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
           
            'roles':tmp,
            'subnav':subnav,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,

        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,
            'prtemp':prtemp,
            'prtsec':prtsec,
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist,
            'prtlist':prtlist,
            'prtticket':prtticket,    
            'prtemp':prtemp,
            'prtsec':prtsec,
                }

    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            mw_no = request.POST.get('mwno')
            cause=request.POST.get('cause')
            lost=request.POST.get('losthrs')
            # date_fr=request.POST.get('date_fr')
            # date_to=request.POST.get('date_to')
    #         staff_no = request.POST.get('staffno')
            
            current_yr=int(datetime.datetime.now().year)


            print("Current year",current_yr)
        

           
            # cause=cause+str("  ")
            tmp=str(cause)+str("   ")
            print(mw_no)
            print(shop_sec)
            # print(date_fr)
            # print(date_to)
            print(tmp,"cause")
            print(lost)
            # date_fr=datetime(date_fr)
            # t=date_fr.split('-')
            # print(t[0],t[1],t[2])
            
            obj = Shop.objects.filter(shop=shop_sec).values('sh_desc')[0]
            obj2  = Lc1.objects.filter(shop_sec=shop_sec,lcno=mw_no).values('des')[0]
            obj1 = MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,cause_hrs=tmp,total_losthrs__gte=lost).values('sl_no','complaint','handed_date','handed_time','comp_date','comp_time','action','total_losthrs').distinct()
            obj3 = MG9Initial.objects.filter(sec=shop_sec,mw_no=mw_no).values('sl_no','complaint','handed_date','handed_time').distinct()
            pending='pending'
            
            # ff=obj1[0]['handed_date']
            # print(ff)
            # ff=str(ff)
            # if ff<date_fr:
            #     print("yaya")
            # ff=d(ff)
            # print(ff)
            # temp_date = to_date(ff,'YYYY-MM-DD')
            # print(temp_date)
            # if ff<date_fr:
            #     print("hello")
            # print(ff)
            # obj1  = MG9Complete.objects.values('id').count()
            # print("OBJ2")
            # print(obj2)
            print("OBJ#")
            print(obj3)
            print("obj1")
            print(obj1)
            # leng = obj.count()
            # leng2 = obj2.count()
            leng1 = obj1.count()
            leng3 = obj3.count()
            # slno=obj1
            # slno=slno+1
            # print(slno)
            

            
            if "Superuser" in rolelist:
                    tm=M5SHEMP.objects.all().values('shopsec').distinct()
                    tmp=[]
                    for on in tm:
                        tmp.append(on['shopsec'])
                    context={
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        # 'len':leng,   
                        # 'len1':leng1,  
                        'obj':obj,
                        'obj2':obj2,
                        'obj1':obj1,
                        'obj3':obj3,
                        'len3':leng3,
                        # 'len2':leng2,
                        'len1':leng1,
                        'p':pending,
                        # 'obj1':obj1,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        'cause':cause,
                        # 'staff_no': staff_no,
                        # 'slno':slno,
                        'cyear':current_yr,
                       
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                        'prtlist':prtlist,
                        'prtticket':prtticket,
                        'prtemp':prtemp,
                        'prtsec':prtsec,



                    }
            elif(len(rolelist)==1):
                    # print("in m5 else")
                    for i in range(0,len(rolelist)):
                        req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
                        wo_nop =wo_nop | req
                    context = {
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'roles':tmp,
                        # 'len':leng,
                        'obj':obj,
                        'obj2':obj2,
                        'obj1':obj1,
                        'p':pending,
                        # 'len2':leng2,
                        'obj3':obj3,
                        'len3':leng3,
                        'len1':leng1,
                        'cause':cause,
                        # 'slno':slno,
                        'sub': 1,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        # 'staff_no': staff_no,
                        'cyear':current_yr,
                     
                        #'assm_no':assm_no,
                      
                        'subnav':subnav,
                    }
            elif(len(rolelist)>1):
                    context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'subnav':subnav,
                        'ip':get_client_ip(request),
                        'roles' :rolelist,
                        'len':leng,
                        'obj':obj,
                        'obj1':obj1,
                        'obj3':obj3,
                        'len3':leng3,
                        'obj2':obj2,
                        'len2':leng2,
                        'p':pending,
                        'len1':leng1,
                        'cause':cause,
                        # 'slno':slno,
                        'shop_sec': shop_sec,
                        'mw_no': mw_no,
                        # 'staff_no': staff_no,
                        'cyear':current_yr,
                  
                        #'assm_no':assm_no,
                        'subnav':subnav
                    }    
    #     if submitvalue=='submit':
    #                 leng=request.POST.get('len')
    #                 now = datetime.datetime.now()
    #                 shop_sec=request.POST.get('shop_sec')
    #                 mw_no = request.POST.get('mw_no')
    #                 staff_no = request.POST.get('staff_no')
    #                 comp= request.POST.get('complaint')
    #                 date_handed=request.POST.get('date_handed')
    #                 date_com=request.POST.get('date_com')
    #                 time_handed=request.POST.get('time_handed')
    #                 time_com=request.POST.get('time_com')
    #                 sec_handed = request.POST.get('sec_handed')
    #                 sec_com = request.POST.get('sec_com')
    #                 serv_com = request.POST.get('serv_com')
    #                 serv_handed = request.POST.get('serv_handed')
    #                 action= request.POST.get('action')
    #                 sl_no = request.POST.get('sl_no')
    #                 lost_hrs = request.POST.get('lost_hrs')
    #                 elec = request.POST.get('elec')
    #                 mech = request.POST.get('mech')
    #                 mech_ele = request.POST.get('mech_ele')
    #                 mp = request.POST.get('mp')
    #                 inv = request.POST.get('inv')
    #                 mismp = request.POST.get('mismp')
    #                 # time_hrs=request.POST.get('time_hrs')
    #                 inv_time = request.POST.get('inv_time')
    #                 mismp_time = request.POST.get('mismp_time')
    #                 mp_time=request.POST.get('mp_time')



                   

    #                 print(sl_no)
    #                 print(shop_sec)
    #                 print(mw_no)
    #                 print(staff_no)
    #                 print(date_handed)
    #                 print(date_com)
    #                 print(time_handed)
    #                 print(time_com)
    #                 print(sec_handed)
    #                 print(sec_com)
    #                 print(serv_handed)
    #                 print(serv_com)
    #                 print(action)
    #                 print(comp)
    #                 print(lost_hrs)
    #                 print(elec)
    #                 print(mech)
    #                 print(mech_ele)
    #                 print(mp)
    #                 print(inv)
    #                 print(mismp)
    #                 print("mp_time",mp_time)
    #                 print("mismp_time",mismp_time)
    #                 print("inv_time",inv_time)
    #                 tmp=""
    #                 if(elec is not None):
    #                     tmp=str(elec)+str("   ")
    #                 if(mech is not None):
    #                     tmp=tmp+str(mech)+str("   ")
    #                 if(mech_ele is not None):
    #                     tmp=tmp+str(mech_ele)+str("   ")
    #                 if(mp is not None):
    #                     tmp=tmp+str(mp)+str("   ")
    #                 if(inv is not None):
    #                     tmp=tmp+str(inv)+str("   ")
    #                 print(tmp)
    #                 if(mp_time is None):
    #                     mp_time='00:00'
    #                     print("mp_time",mp_time)
    #                 if(inv_time is None):
    #                     inv_time='00:00'
    #                     print("inv_time",inv_time) 
    #                 if(mismp_time is None):
    #                     mismp_time='00:00'
    #                     print("mismp_time",mismp_time)        
                   

    #                 mg9obj = MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).distinct()
    #                 if len(mg9obj) == 0:

    #     #                 print(now)
    #     #                 print(sl_no)
    #     #                 # print(shop_sec)
    #     #                 print(shop_sec)
    #     #                 print(mw_no)
    #     #                 print(staff_no)
    #     #                 print(date_handed)
    #     #                 print(date_com)
    #     #                 print(time_handed)
    #     #                 print(time_com)
    #     #                 print(sec_handed)
    #     #                 print(sec_com)
    #     #                 print(serv_handed)
    #     #                 print(serv_com)
    #     #                 print(action)
    #     #                 print(comp)

                    
    #                     MG9Complete.objects.create(sec=str(shop_sec),mw_no=str(mw_no),sl_no=str(sl_no),staff_no=str(staff_no),complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=request.user,total_losthrs=str(lost_hrs),cause_hrs=str(tmp),mp_time=str(mp_time),inv_time=str(inv_time),mismp_time=str(mismp_time))
    #                 else:
    #                     cause=request.POST.get('cause_hrs')

    #                     MG9Complete.objects.filter(sec=shop_sec,mw_no=mw_no,staff_no=staff_no).update(complaint=str(comp),handed_date=str(date_handed),comp_date=str(date_com),handed_time=str(time_handed),comp_time=str(time_com),handed_cmsec=str(sec_handed),comp_cmsec=str(sec_com),handed_cmserv=str(serv_handed),comp_cmserv=str(serv_com),action=str(action),last_modified=str(now),login_id=str(request.user),total_losthrs=str(lost_hrs),cause_hrs=str(cause),mp_time=str(mp_time),inv_time=str(inv_time),mismp_time=str(mismp_time))
                       
    #     #                 print(now)
    #     #                 print(sl_no)
    #     #                 # print(shop_sec)
    #     #                 print(shop_sec)
    #     #                 print(mw_no)
    #     #                 print(staff_no)
    #     #                 print(date_handed)
    #     #                 print(date_com)
    #     #                 print(time_handed)
    #     #                 print(time_com)
    #     #                 print(sec_handed)
    #     #                 print(sec_com)
    #     #                 print(serv_handed)
    #     #                 print(serv_com)
    #     #                 print(action)
    #     #                 print(comp)
                 

        
    


    return render(request,"machineviews.html",context)

def machinegetcause(request):
    if request.method == "GET" and request.is_ajax():
        mwno = request.GET.get('mwno')
        print(mwno)
        # print(shop_sec)
        wono = list(MG9Complete.objects.filter(mw_no = mwno).values('cause_hrs').distinct())
        print("wono",wono)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)  


@login_required
@role_required(urlpass='/m4hwview/')
def m4hwview(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = M14M4.objects.filter(assly_no__in=w1).values('bo_no').distinct()
            wo_nop = wo_nop | req

        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            part_no = request.POST.get('part_nop')
            wo_no = request.POST.get('wo_no')
            brn_no = request.POST.get('br_no')
            assembly_no = request.POST.get('assm_no')
            doc_no = request.POST.get('doc_no')
            kkk=Oprn.objects.all()
            obj1 = Part.objects.filter(partno=part_no).values('des', 'drgno').distinct()
            obj2 = Part.objects.filter(partno=assembly_no).values('des').distinct()
            obj3 = Batch.objects.filter(bo_no=wo_no,brn_no=brn_no,part_no=assembly_no).values('batch_type')
            check_obj=Oprn.objects.all().filter(shop_sec=shop_sec)
            obj = M14M4.objects.filter(doc_no=doc_no,assly_no=assembly_no,brn_no=brn_no,part_no=part_no).values('received_mat', 'issued_qty', 'received_qty', 'laser_pst', 'line', 'closing_bal', 'remarks', 'posted_date', 'wardkp_date', 'shopsup_date', 'posted1_date')
            print("hh")
            print(obj)
            if len(obj) == 0:
                obj = range(0,1)
            date = M14M4.objects.filter(doc_no=doc_no,assly_no=assembly_no,brn_no=brn_no,part_no=part_no).values('prtdt','qty').distinct()
            leng = obj.count()
            datel = date.count()           
           
            if "Superuser" in rolelist:
                tm=shop_section.objects.all()
                tmp=[]
                for on in tm:
                    tmp.append(on.section_code)
                context = {
                    'roles':tmp,
                    'lenm' :2,
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }
            elif(len(rolelist)==1):
                for i in range(0,len(rolelist)):                    

                    w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
                    req = M14M4.objects.filter(assly_no__in=w1).values('bo_no').distinct()
                    wo_nop = wo_nop | req

                context = {
                    'wo_nop':wo_nop,
                    'roles' :rolelist,
                    'subnav':subnav,
                    'usermaster':usermaster,
                    'lenm' :len(rolelist),
                    'nav': nav,
                    'ip': get_client_ip(request),
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }
            elif(len(rolelist)>1):
                context = {
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist,
                    'obj': obj,
                    'obj1': obj1,
                    'obj2': obj2,
                    'obj3': obj3,
                    'sub': 1,
                    'len': leng,
                    'date': date,
                    'datel': datel,
                    'shop_sec': shop_sec,
                    'part_no': part_no,
                    'wo_no': wo_no,
                    'brn_no': brn_no,
                    'assembly_no': assembly_no,
                    'doc_no': doc_no,
                }
        if submitvalue=='Save':
            rand  = random.choice('0123456789')           
            rand1 = random.choice('0123456789')        
            rand2 = random.choice('0123456789')           
            rand3 = random.choice('0123456789')         
            rand4 = random.choice('0123456789')          
            rand5 = random.choice('0123456789')           
            num = rand + rand1 + rand2 + rand3 + rand4 + rand5           
            number = num

            prtDate= request.POST.get('prtdt')              
            monthTemp = prtDate.split(' ')[0]            
            dateTemp = prtDate.split(' ')[1]                    
            final1 = monthTemp[0:3]+' '+dateTemp.split(',')[0]+' '+prtDate.split(' ')[2]
            print("final1 : ",final1)                
            date_time_str = final1
            date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %Y')
            print('Date:', date_time_obj.date())
            
            wo_no= request.POST.get('wo_no')          
            brn_no=request.POST.get('brn_no')         
            qty=request.POST.get('qty')  
            end_prod = request.POST.get('end_prod')         
            epdes = request.POST.get('epdes')        
            shop_section_temp = request.POST.get('shop_section_temp')        
            part_no = request.POST.get('part_no')        
            partdes= request.POST.get('partdes')        
            drgno = request.POST.get('drgno')           
            doc_no = request.POST.get('doc_no')         
            batch_type = request.POST.get('batch_type')          
            received_mat = request.POST.get('received_mat')        
            issued_qty = request.POST.get('issued_qty')        
            received_qty = request.POST.get('received_qty')      
            laser_pst = request.POST.get('laser_pst')        
            line = request.POST.get('line')                  
            closing_bal = request.POST.get('closing_bal')          
            remarks = request.POST.get('remarks')       
            posted_date = request.POST.get('posted_date')        
            wardkp_date = request.POST.get('wardkp_date')            
            shopsup_date = request.POST.get('shopsup_date')        
            posted1_date = request.POST.get('posted1_date')
            causesofHW = request.POST.get('causesofHW')        
            
            M4HW.objects.create(prtdt=str(date_time_obj.date()),doc_no=str(doc_no),part_no=str(part_no),wo_no=str(wo_no),brn_no=str(brn_no),qty=str(qty),end_prod=str(end_prod),epdes=str(epdes),shop_section_temp=str(shop_section_temp),partdes=str(partdes),drgno=str(drgno),batch_type=str(batch_type),received_mat=str(received_mat),issued_qty=str(issued_qty),received_qty=str(received_qty),laser_pst=str(laser_pst),line=str(line),closing_bal=str(closing_bal),remarks=str(remarks),posted_date=str(posted_date),wardkp_date=str(wardkp_date),shopsup_date=str(shopsup_date),posted1_date=str(posted1_date),number=str(number),causesofHW=str(causesofHW))         
            messages.success(request, 'M4 Card Hand Written generated Successfully, Your Reference number is : '+number)
           
    return render(request,"m4hwview.html",context)         


def m4getbrhw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = list(M14M4.objects.filter(bo_no =wo_no).values('brn_no').exclude(brn_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m4getwonohw(request):
    if request.method == "GET" and request.is_ajax():
        from.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1 = Oprn.objects.filter(shop_sec=shop_sec).values('part_no').distinct()
        w2 = M14M4.objects.filter(assly_no__in=w1).values('bo_no').exclude(bo_no__isnull=True).distinct()
        # print(w2)
        wono = list(w2)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)








def m4getasslyhw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assm_no = list(M14M4.objects.filter(bo_no =wo_no,brn_no=br_no).values('assly_no').exclude(assly_no__isnull=True).distinct())
        return JsonResponse(assm_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m4getpart_nohw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        assembly_no = request.GET.get('assm_no')
        part_no = list(M14M4.objects.filter(brn_no=br_no,assly_no=assembly_no,bo_no=wo_no).values('part_no').exclude(part_no__isnull=True).distinct())
        return JsonResponse(part_no, safe = False)
    return JsonResponse({"success":False}, status=400)



def m4getdoc_nohw(request):
    if request.method == "GET" and request.is_ajax():
        wo_no = request.GET.get('wo_no')
        br_no = request.GET.get('brn_no')
        shop_sec = request.GET.get('shop_sec')
        assembly_no = request.GET.get('assm_no')
        part_no = request.GET.get('part_no')
        doc_no = list(M14M4.objects.filter(bo_no =wo_no,brn_no=br_no,assly_no=assembly_no,part_no=part_no).values('doc_no').exclude(doc_no__isnull=True).distinct())
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)




@login_required
@role_required(urlpass='/mg5view/')
def mg5view(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    idcard_no = empmast.objects.none()
    obj=empmast.objects.all().values('idcard_no').distinct()
    objj=empmast.objects.filter(idcard_no=idcard_no).values('ticket_no').distinct()
    if "Superuser" in rolelist:
        # tm=shop_section.objects.all()
        # tmp=[]
        # for on in tm:
        #     tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            # 'roles':tmp,
            'obj':obj,
            # 'objj':objj
        }
    elif(len(rolelist)==1):
        for i in range(0, len(rolelist)):
            req = empmast.objects.all().filter(idcard_no=rolelist[i]).distinct()
            idcard_no =idcard_no | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'idcard_no':idcard_no,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            ti_no = request.POST.get('t_no')
            print("ti_no : ",ti_no)
            id_no = request.POST.get('id_no')
            instrument_number= request.POST.get('t_id')
            print(id_no)
            from datetime import date
            today = date.today()
            obj = empmast.objects.filter( idcard_no=id_no,ticket_no=ti_no).values('empname','emptype','shopno','empno').distinct()
            obj1 = MG5.objects.filter(id_no=id_no,t_no=ti_no).values('optr','chkr').distinct()
            obj2 = ms_tools_master.objects.values('instrument_number','make').distinct()
            obj3=ms_tools_master.objects.filter(instrument_number=instrument_number).values('make').distinct()
        
            print(obj1)
            if len(obj1)== 0:
                obj1=range(0, 1)
            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'date':today,
                        'ticket_no': ti_no,
                        'id_no': id_no,
                        'subnav':subnav,
                  }
            elif(len(rolelist)==1):
                  for i in range(0, len(rolelist)):
                      req = empmast.objects.all().filter(idcard_no=rolelist[i]).distinct()
                      idcard_no =idcard_no | req
                      
                  context = {
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj3': obj3,
                        'sub': 1,
                        'idcard_no': idcard_no,
                        'subnav':subnav,
                        'date':today, 
                        'ticket_no': ti_no,
                        'obj2': obj2,
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'ticket_no': ti_no,
                        'id_no': id_no,
                        'subnav':subnav,
                        'date':today, 

                  }
        # print(obj3)
        if submitvalue=='Save':
                shopno= request.POST.get('shop_no')
                empno = request.POST.get('staff_no')
                emp_name= request.POST.get('name')
                super_in = request.POST.get('emptype')
                print("super_in 123 : ",super_in)
                id_no=request.POST.get('id_no')
                ticket_no=request.POST.get('t_no')
                print("ticket_no 123 : ",ticket_no)
                t_id=request.POST.get('t_id')
                date=request.POST.get('date')
                t_desc=request.POST.get('make1')
                optr=request.POST.get('optr')
                chkr=request.POST.get('chkr')
                # to_no=request.POST.get('to_no')

                from datetime import datetime
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                # print(to_no)
                # obj3 = MG5.objects.filter( id_no=id_no).distinct()
                # print(len(obj2))
                # if len(obj3) == 0:
                MG5.objects.create(id_no=str(id_no),t_id=str(t_id),t_desc=str(t_desc), t_no=str(ticket_no), shop_sec=str(shopno), staff_no=str(empno), name=str(emp_name), super_in=str(super_in), date=str(date), optr=str(optr), chkr=str(chkr), last_modified=str(dt_string) )
                # else:
                #     MG21.objects.filter(shop_sec=shop_sec, staff_no=staff_no).update(to_the=str(to_the),last_modified=str(dt_string))
                # wo_no=empmast.objects.all().values('idcard_no').distinct()
                messages.success(request, 'Successfully Done!, Select new values to proceed')

        if submitvalue=='Generate report':
            return mg5report(request)
            
    return render(request, "mg5view.html", context)


def mg5getticket(request):
    if request.method == "GET" and request.is_ajax():

        idcard_no = request.GET.get('id_no')

        ticket = empmast.objects.filter(idcard_no=idcard_no).values('ticket_no').exclude(ticket_no__isnull=True).distinct()
        ticket_no = list(ticket)
        return JsonResponse(ticket_no, safe=False)
    return JsonResponse({"success": False}, status=400)

def mg5gettooldesc(request):
    if request.method == "GET" and request.is_ajax():

        make = request.GET.get('make')

        tool_desc = list(ms_tools_master.objects.filter(instrument_number=make).values('make'))
        print('TOOL MAKe ---->',tool_desc)
        return JsonResponse(tool_desc, safe=False)
    return JsonResponse({"success": False}, status=400)


@login_required
@role_required(urlpass='/mg5report/')
def mg5report(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    idcard_no = empmast.objects.none()
    obj=empmast.objects.all().values('idcard_no').distinct()
    objj=empmast.objects.filter(idcard_no=idcard_no).values('ticket_no').distinct()
    if "Superuser" in rolelist:
        # tm=shop_section.objects.all()
        # tmp=[]
        # for on in tm:
        #     tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            # 'roles':tmp,
            'obj':obj,
            # 'objj':objj
        }
    elif(len(rolelist)==1):
        for i in range(0, len(rolelist)):
            req = empmast.objects.all().filter(idcard_no=rolelist[i]).distinct()
            idcard_no =idcard_no | req

        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'idcard_no':idcard_no,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            ti_no = request.POST.get('t_no')
            id_no = request.POST.get('id_no')
            instrument_number= request.POST.get('t_id')
            print(id_no)
            from datetime import date
            today = date.today()
            #obj = empmast.objects.filter( idcard_no=id_no,ticket_no=ti_no).values('empname','emptype','shopno','empno').distinct()
            obj = MG5.objects.filter( id_no=id_no,t_no=ti_no).values('shop_sec','staff_no', 'name', 'date', 'super_in', 'optr', 'chkr', 'id_no', 't_no', 't_id', 'last_modified', 'to_no', 't_desc').distinct()
            obj1 = MG5.objects.filter(id_no=id_no,t_no=ti_no).values('optr','chkr').distinct()
            obj2 = ms_tools_master.objects.values('instrument_number','make').distinct()
            obj3=  ms_tools_master.objects.filter(instrument_number=instrument_number).values('make').distinct()
        
            print(obj1)
            if len(obj1)== 0:
                obj1=range(0, 1)
            if "Superuser" in rolelist:
                  tm=shop_section.objects.all()
                  tmp=[]
                  for on in tm:
                      tmp.append(on.section_code)
                  context = {
                        'roles':tmp,
                        'lenm' :2,
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'date':today,
                        'ticket_no': ti_no,
                        'id_no': id_no,
                        'subnav':subnav,
                  }
            elif(len(rolelist)==1):
                  for i in range(0, len(rolelist)):
                      req = empmast.objects.all().filter(idcard_no=rolelist[i]).distinct()
                      idcard_no =idcard_no | req
                      
                  context = {
                        'roles' :rolelist,
                        'usermaster':usermaster,
                        'lenm' :len(rolelist),
                        'nav': nav,
                        'ip': get_client_ip(request),
                        'obj': obj,
                        'obj1': obj1,
                        'obj3': obj3,
                        'sub': 1,
                        'idcard_no': idcard_no,
                        'subnav':subnav,
                        'date':today, 
                        'ticket_no': ti_no,
                        'obj2': obj2,
                  }
            elif(len(rolelist)>1):
                  context = {
                        'lenm' :len(rolelist),
                        'nav':nav,
                        'ip':get_client_ip(request),
                        'usermaster':usermaster,
                        'roles' :rolelist,
                        'obj': obj,
                        'obj1': obj1,
                        'obj2': obj2,
                        'obj3': obj3,
                        'sub': 1,
                        'ticket_no': ti_no,
                        'id_no': id_no,
                        'subnav':subnav,
                        'date':today, 

                  }
        # print(obj3)
        if submitvalue=='Save':
                shopno= request.POST.get('shop_no')
                empno = request.POST.get('staff_no')
                emp_name= request.POST.get('name')
                super_in = request.POST.get('emptype')
                id_no=request.POST.get('id_no')
                ticket_no=request.POST.get('t_no')
                t_id=request.POST.get('t_id')
                
                date=request.POST.get('date')
                t_desc=request.POST.get('make1')
                optr=request.POST.get('optr')
                chkr=request.POST.get('chkr')
                # to_no=request.POST.get('to_no')

                print('tool id---->',t_id)
                print('empno---->',empno)
                print('emp_name---->',emp_name)
                print('super_in--->',super_in)
                print('id_no---->',id_no)
                print('ticket_no---->',ticket_no)
                print('date---->',date)
                print('t_desc---->',t_desc)
                print('optr---->',optr)
               



                from datetime import datetime
                now = datetime.now()
                dt_string = now.strftime("%H:%M:%S")
                tot = request.POST.get('totaltools')
                
                  
                MG5.objects.create(id_no=str(id_no),t_id=str(t_id),t_desc=str(t_desc), t_no=str(ticket_no), shop_sec=str(shopno), staff_no=str(empno), name=str(emp_name), super_in=str(super_in), date=str(date), optr=str(optr), chkr=str(chkr), last_modified=str(dt_string) )
                
                print(id_no,t_id,t_desc,ticket_no,shopno,empno,emp_name,super_in,date,optr,chkr,dt_string)
                # else:
                #     MG21.objects.filter(shop_sec=shop_sec, staff_no=staff_no).update(to_the=str(to_the),last_modified=str(dt_string))
                # wo_no=empmast.objects.all().values('idcard_no').distinct()
                messages.success(request, 'Successfully Done!, Select new values to proceed')

        if submitvalue=='Generate report':
            return mg5report(request)
            
    return render(request, "mg5report.html", context)



@login_required
@role_required(urlpass='/mg10views/')
def mg10views(request):
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
    #----for name 
    name = empmast.objects.values('empname').exclude(empname__isnull=True).distinct()
    prtname=[]
    for i in name:
        prtname.append(i['empname'])
        
    # print(prtlist)
    #------end name  
    shop_sec = request.GET.get('shop_sec')
    w1 = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
    prtticket=[] 
    for i in w1:
        ty=i['staff_no']
        pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
        prtticket.append(pop)

    # print(prtticket)
    

    # cat = empmast.objects.values('desgn').exclude(desgn__isnull=True).distinct()
    # prtdesgn=[]
    # for i in desgn:
    #     prtdesgn.append(i['desgn'])

    payrate = empmast.objects.values('payrate').exclude(payrate__isnull=True).distinct()
    prtpay=[]
    for i in payrate:
        prtpay.append(i['payrate'])

    # superv = empmast.objects.values('empno').exclude(scalecode__isnull=True).distinct()
    # prtemp=[]
    # for i in superv:
    #     prtemp.append(i['empno'])
    # # print(prtemp)

    
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        # print(tm)
        tmp=[]
        
        for on in tm:
            tmp.append(on.section_code)
            #print(tmp)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'prtname':prtname,
            'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = mg10.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
            print("role===========1 ",rolelist)
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtname':prtname,
            'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
    elif(len(rolelist)>1):
        print("role >>>>>>>>>>>>>>>>> 1 ",rolelist)
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtname':prtname,
            'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
        
    if request.method == "POST":

        submitvalue = request.POST.get('proceed')

        if submitvalue=='Proceed':
            date = request.POST.get('date')
            #to_date = request.POST.get('to_date')
            shop_sec = request.POST.get('shop_sec')
            month = request.POST.get('month')
            ticket = request.POST.get('ticket')

            obj1 = mg10.objects.filter(shop_sec=shop_sec).values('sno','date','ticket_no','name','payrate','cat','remarks').distinct()
            print(date)
            print(shop_sec)
            print(month)
            print("fgghuhjeeiueehjeduedeh")
            obj3=mg10.objects.all().count()
            print(obj3)
            wer=obj3+1
            print("wer------>",wer)
            # #m21 se date validation--------------------------------------*******
            # d1 = M21.objects.filter(shop_sec=shop_sec).values('date').distinct()
            # print("d1 date m21",d1)
            # #mydate = d1[0]['date']
            # dtdate = mg10.objects.filter(eiwdate__contains=d1).values('ticket_no')


            w1 = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()) 
            print("w1",w1)
            print("jgjuj")
            prtticket=[]
            for i in w1:
                ty=i['staff_no']
                pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
                for i in pop:
                    prtticket.append(i['ticket_no'])

            #leng=obj1.count()
            ticket = request.POST.get('ticket')
            print(ticket)

            context = {
            #'obj1': obj1,
            'mytry':"rimjhim",
            #'lent': leng,
            # 'lent2': leng1,
            #'leng':leng,
            'shop_sec': shop_sec,
            'month':month,
            'date':date,
            'wer':wer,
            'prtname':prtname,
            'prtpay':prtpay,
            'prt':prtticket,
            'prtticket':prtticket,
            'ticket':ticket,
            # 'prtemp':prtemp,
            # 'timekeep':timekeep,
            # 'workshop':workshop,
            # 'fr_date':fr_date,
            'sub': 1, 
                    
        }

        print("ghjkl;'",submitvalue)
        if submitvalue=='submit':
            # print("in submit")                               
            leng=request.POST.get('len')
            print("leng=",leng)
            #shop_sec= request.POST.get('shop_sec')
            #staff_no = request.POST.get('staff_no')
            #name = request.Post.get('name')
            tot= request.POST.get('total')
            tot = int(tot)+1

            for i in range(1,int(tot)):
                print("aaya1")
                date = request.POST.get('date')
                shop_sec = request.POST.get('shop_sec')
                month = request.POST.get('month')
                sno = request.POST.get('sno'+str(i))
                ticket = request.POST.get('ticket'+str(i))
                name = request.POST.get('name'+str(i))
                payrate = request.POST.get('payrate')
                category = request.POST.get('category'+str(i)) 
                eiwdate = request.POST.get('eiwdate'+str(i))
                remark = request.POST.get('remark'+str(i))

                
                print("print here")
                print(date)
                print(month)
                print(shop_sec)
                print(ticket)
                print(name)
                print(payrate)
                print(category)
                print(eiwdate)
                print(remark)
                print("over n out !!!!!")
                mg10.objects.create(shop_sec=str(shop_sec),month=str(month),date=str(date),sno=str(sno),ticket_no=str(ticket),name=str(name),payrate=str(payrate),cat=str(category),eiwdate=str(eiwdate),remarks=str(remark))


    return render(request,"mg10views.html",context)

# def mg10checkdate(request):
#    if request.method == "GET" and request.is_ajax():
#        shop_sec = request.GET.get('shop_sec')
#        ticket = request.GET.get('ticket')
#        d1 = M21.objects.filter(shop_sec=shop_sec).values('date').distinct()
#        print("d1 date m21",d1)
#        # #mydate = d1[0]['date']
#        dtdate = mg10.objects.filter(eiwdate__contains=d1).values('ticket_no')


def mg10checkdate(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        ticket = request.GET.get('ticket')
        d1 = M21.objects.filter(shop_sec=shop_sec).values('date').distinct()
        date_values = []
        print("d1 date m21",d1)
        for i in d1:
            if not mg10.objects.get(eiwdate__contains=d1).exists():
                print("Select a valid date")
            else:
                print("good")
        return JsonResponse(d1, safe = False)
    return JsonResponse({"success":False}, status=400)
    
        




    


#def mg10getticketno(request):
#     if request.method == "GET" and request.is_ajax():
#         shop_sec = request.GET.get('shop_sec')
#         # w1 = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()) 
#         # print("w1",w1)
#         # print("jgjuj")
#         # prtticket=[]
#         # for i in w1:
#         #     ty=i['staff_no']
#         #     pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
#         #     for i in pop:
#         #         prtticket.append(i['ticket_no'])
#         context={
#             'prt':prtticket,
#         }
#         print("prtticket----------",context)                     
#         return JsonResponse({'cont':context}, safe = False)
#     return JsonResponse({"success":False}, status=400)


# def mg10getname(request):
#     if request.method == "GET" and request.is_ajax():
#         shop_sec = request.GET.get('shop_sec')
#         ticket = request.GET.get('ticket')
#         w2 = empmast.objects.filter(ticket_no=ticket).values('empname').distinct()
#         print("w2--",w2)
#         return JsonResponse(w2, safe = False)
#     return JsonResponse({"success":False}, status=400)


def mg10getname(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        #ticket = request.GET.get('ticket')
        ticket = request.GET.get('two')
        wname = empmast.objects.filter(ticket_no=ticket).values('empname').distinct()
        myname = wname[0]['empname']
        #print("wname--",wname)
        context={
            'prt':myname,
        }
        print("prtname******--",myname)
        return JsonResponse({'cont':context}, safe = False)
    return JsonResponse({"success":False}, status=400)


def mg10getpayrate(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        ticket = request.GET.get('ticket')
        ticket = list(empmast.objects.filter(ticket_no=ticket).values('payrate').distinct())
        #staff_no=list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(ticket, safe = False)
    return JsonResponse({"success":False}, status=400)


def mg10getcat(request):
    if request.method == "GET" and request.is_ajax():
        # shop_sec = request.GET.get('shop_sec')
        ticket = request.GET.get('two')
        print(ticket)
        w1 = list(empmast.objects.filter(ticket_no=ticket).values('empno').exclude(empno__isnull=True).distinct())
        print("w1***********",w1)
        t=w1[0]['empno']
        print("t",t)
        w2=str(t)
        print("w2---",w2)
        w4=w2[6:11]
        print("w4---",w4)
        w3= list(Shemp.objects.filter(staff_no=w4).values('cat').exclude(cat__isnull=True).distinct())[0]
        print("w3",w3)
        context={
            'prt':w3['cat'],
        }
        print("prtcat----------------------",context)
        return JsonResponse({'cont':context}, safe = False)
    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(urlpass='/mg10report/')
def mg10report(request):
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
    #----for name 
    name = empmast.objects.values('empname').exclude(empname__isnull=True).distinct()
    prtname=[]
    for i in name:
        prtname.append(i['empname'])
        
    # print(prtlist)
    #------end name  
    shop_sec = request.GET.get('shop_sec')
    w1 = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
    prtticket=[] 
    for i in w1:
        ty=i['staff_no']
        pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
        prtticket.append(pop)

    # print(prtticket)
    

    # cat = empmast.objects.values('desgn').exclude(desgn__isnull=True).distinct()
    # prtdesgn=[]
    # for i in desgn:
    #     prtdesgn.append(i['desgn'])

    payrate = empmast.objects.values('payrate').exclude(payrate__isnull=True).distinct()
    prtpay=[]
    for i in payrate:
        prtpay.append(i['payrate'])

    # superv = empmast.objects.values('empno').exclude(scalecode__isnull=True).distinct()
    # prtemp=[]
    # for i in superv:
    #     prtemp.append(i['empno'])
    # # print(prtemp)

    
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        # print(tm)
        tmp=[]
        
        for on in tm:
            tmp.append(on.section_code)
            #print(tmp)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'prtname':prtname,
            'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = mg10.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
            print("role===========1 ",rolelist)
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtname':prtname,
            'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
    elif(len(rolelist)>1):
        print("role >>>>>>>>>>>>>>>>> 1 ",rolelist)
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtname':prtname,
            'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
        
    if request.method == "POST":

        submitvalue = request.POST.get('proceed')

        if submitvalue=='Proceed':
            date = request.POST.get('date')
            #to_date = request.POST.get('to_date')
            shop_sec = request.POST.get('shop_sec')
            month = request.POST.get('month')
            ticket = request.POST.get('ticket')

            obj1 = mg10.objects.filter(shop_sec=shop_sec).values('sno','date','ticket_no','name','payrate','cat','eiwdate','remarks').distinct()
            print("obj 1 ---",obj1)
            print(date)
            print(shop_sec)
            print(month)
            


            w1 = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()) 
            print("w1",w1)
            print("jgjuj")
            prtticket=[]
            for i in w1:
                ty=i['staff_no']
                pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
                for i in pop:
                    prtticket.append(i['ticket_no'])

            leng=obj1.count()
            ticket = request.POST.get('ticket')
            print(ticket)

            context = {
            'obj1': obj1,
            'mytry':"rimjhim",
            #'lent': leng,
            # 'lent2': leng1,
            'leng':leng,
            'shop_sec': shop_sec,
            'month':month,
            'date':date,
            'prtname':prtname,
            'prtpay':prtpay,
            'prt':prtticket,
            'prtticket':prtticket,
            'ticket':ticket,
            # 'prtemp':prtemp,
            # 'timekeep':timekeep,
            # 'workshop':workshop,
            # 'fr_date':fr_date,
            'sub': 1, 
                    
        }

    return render(request,"mg10report.html",context)


@login_required
@role_required(urlpass='/mg11views/')
def mg11views(request):
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
    #----for name 
    name = empmast.objects.values('empname').exclude(empname__isnull=True).distinct()
    prtname=[]
    for i in name:
        prtname.append(i['empname'])
        
    # print(prtlist)
    #------end name  
    shop_sec = request.GET.get('shop_sec')
    w1 = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
    prtticket=[] 
    for i in w1:
        ty=i['staff_no']
        pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
        prtticket.append(pop)
    
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        # print(tm)
        tmp=[]
        
        for on in tm:
            tmp.append(on.section_code)
            #print(tmp)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'prtname':prtname,
            #'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = mg11.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
            print("role===========1 ",rolelist)
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtname':prtname,
            #'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
    elif(len(rolelist)>1):
        print("role >>>>>>>>>>>>>>>>> 1 ",rolelist)
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtname':prtname,
            #'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
        
    if request.method == "POST":

        submitvalue = request.POST.get('proceed')

        if submitvalue=='Proceed':
            date = request.POST.get('date')
            #to_date = request.POST.get('to_date')
            shop_sec = request.POST.get('shop_sec')
            month = request.POST.get('month')
            #ticket = request.POST.get('ticket')

            obj1 = mg11.objects.filter(shop_sec=shop_sec).values('sno','date','ticket_no','name','remarks').distinct()
            print(date)
            print(shop_sec)
            print(month)
            print("fgghuhjeeiueehjeduedeh")
            obj3=mg11.objects.all().count()
            print(obj3)
            wer=obj3+1
            print("wer------>",wer)


            w1 = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()) 
            print("w1",w1)
            print("jgjuj")
            prtticket=[]
            for i in w1:
                ty=i['staff_no']
                pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
                for i in pop:
                    prtticket.append(i['ticket_no'])

            # #leng=obj1.count()   comment
            ticket = request.POST.get('ticket')
            print(ticket)

            context = {
            #'obj1': obj1,
            'mytry':"rimjhim",
            #'lent': leng,
            # 'lent2': leng1,
            #'leng':leng,
            'shop_sec': shop_sec,
            'month':month,
            'date':date,
            'wer':wer,
            'prtname':prtname,
            #'prtpay':prtpay,
            'prt':prtticket,
            'prtticket':prtticket,
            'ticket':ticket,
            # 'prtemp':prtemp,
            # 'timekeep':timekeep,
            # 'workshop':workshop,
            # 'fr_date':fr_date,
            'sub': 1, 
                    
        }

        print("ghjkl;'",submitvalue)
        if submitvalue=='submit':
            # print("in submit")                               
            leng=request.POST.get('len')
            print("leng=",leng)
            shop_sec= request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            name = request.POST.get('name')
            tot= request.POST.get('total')
            tot = int(tot)+1

            for i in range(1,int(tot)):
                print("aaya1")
                date = request.POST.get('date')
                shop_sec = request.POST.get('shop_sec')
                month = request.POST.get('month')
                sno = request.POST.get('sno'+str(i))
                ticket = request.POST.get('ticket'+str(i))
                name = request.POST.get('name'+str(i))
                remark = request.POST.get('remark'+str(i))


                print("print here")
                print(date)
                print(month)
                print(shop_sec)
                print(ticket)
                print(name)
                print(remark)
                print("over n out !!!!!")
                mg11.objects.create(shop_sec=str(shop_sec),month=str(month),date=str(date),sno=str(sno),ticket_no=str(ticket),name=str(name),remarks=str(remark))


    return render(request,"mg11views.html",context)

def mg11getname(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        #ticket = request.GET.get('ticket')
        ticket = request.GET.get('two')
        wname = empmast.objects.filter(ticket_no=ticket).values('empname').distinct()
        myname = wname[0]['empname']
        #print("wname--",wname)
        context={
            'prt':myname,
        }
        print("prtname******--",myname)
        return JsonResponse({'cont':context}, safe = False)
    return JsonResponse({"success":False}, status=400)



@login_required
@role_required(urlpass='/mg11report/')
def mg11report(request):
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
    #----for name 
    name = empmast.objects.values('empname').exclude(empname__isnull=True).distinct()
    prtname=[]
    for i in name:
        prtname.append(i['empname'])
        
    # print(prtlist)
    #------end name  
    shop_sec = request.GET.get('shop_sec')
    w1 = Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()
    prtticket=[] 
    for i in w1:
        ty=i['staff_no']
        pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
        prtticket.append(pop)

    # print(prtticket)
    

    
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        # print(tm)
        tmp=[]
        
        for on in tm:
            tmp.append(on.section_code)
            #print(tmp)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'prtname':prtname,
            #'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            # req = M2Doc.objects.all().filter(f_shopsec=rolelist[i]).values('batch_no').distinct()
            # wo_nop =wo_nop | req

            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = mg11.objects.filter(part_no__in=w1).values('batch_no').distinct()
            wo_nop = wo_nop | req
            print("role===========1 ",rolelist)
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtname':prtname,
            #'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
    elif(len(rolelist)>1):
        print("role >>>>>>>>>>>>>>>>> 1 ",rolelist)
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'usermaster':usermaster,
            'roles' :rolelist,
            'prtname':prtname,
            #'prtpay':prtpay,
            #'ticket':ticket,
            'prtticket':prtticket,
            # 'prtemp':prtemp,
        }
        
    if request.method == "POST":

        submitvalue = request.POST.get('proceed')

        if submitvalue=='Proceed':
            date = request.POST.get('date')
            #to_date = request.POST.get('to_date')
            shop_sec = request.POST.get('shop_sec')
            month = request.POST.get('month')
            ticket = request.POST.get('ticket')

            obj1 = mg11.objects.filter(shop_sec=shop_sec).values('sno','date','ticket_no','name','remarks').distinct()
            # print(date)
            # print(shop_sec)
            # print(month)
            print("obj1+++++++",obj1)
            obj3=mg11.objects.all().count()
            print("obj3-------",obj3)
            wer=obj3+1
            print("wer------>",wer)


            w1 = list(Shemp.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct()) 
            print("w1++++",w1)
            #print("jgjuj")
            prtticket=[]
            for i in w1:
                ty=i['staff_no']
                pop=empmast.objects.filter(empno__contains=ty).values('ticket_no')
                for i in pop:
                    prtticket.append(i['ticket_no'])

            leng=obj1.count()   
            #ticket = request.POST.get('ticket')
            #print(ticket)

            context = {
            'obj1': obj1,
            'mytry':"rimjhim",
            #'lent': leng,
            # 'lent2': leng1,
            'leng':leng,
            'shop_sec': shop_sec,
            'month':month,
            'date':date,
            'wer':wer,
            'prtname':prtname,
            'prt':prtticket,
            'prtticket':prtticket,
            #'ticket':ticket,
            'sub': 1, 
                    
        }

    return render(request,"mg11report.html",context)


@login_required
@role_required(urlpass='/m14hwview/')
def m14hwview(request):   
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist) 
    batch1 = list(Batch.objects.filter(status = 'R' , rel_date__isnull=False).values('bo_no').distinct())
    m13ref = list(M13.objects.filter(rej_cat='M14').values('slno').order_by('slno').distinct())
    if "Superuser" in rolelist:
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)

        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
            'm13ref' :m13ref,
            'batch1' :batch1, 
                   
        }
    return render(request,'m14hwview.html', context)

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




@login_required
@role_required(urlpass='/m338view/')
def m338view(request):
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
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
            
        context = {
            'obj1' : obj1,
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='proceed':
            from datetime import date
            shop_sec = request.GET.get('shop_sec')
            staff_no = request.GET.get('staff_no')
            obj1 = list(empmast.objects.filter(empno = staff_no).values('empname','desig_longdesc','payrate').distinct())
            noprint=0
            context = {
                'obj1': obj1,
                'ran':range(1,32),
                'len': 31,
                'shop_sec': shop_sec,
                'noprint':noprint,
                'staff_no': staff_no,
                'sub':1,
                'nav':nav,
                
                'ip':get_client_ip(request),  
                'subnav':subnav,     
            }



        submitvalue = request.POST.get('final')
        if submitvalue=='final':
             
            obj = Intershop338()
    
            obj.shop_sec        = request.POST.get('shop_sec')
            obj.staffNo          = request.POST.get('staffNo')
            obj.staffName        = request.POST.get('staffName')
            obj.staffDesg      = request.POST.get('staffDesg')
            obj.reference_authority = request.POST.get('reference_authority')
            obj.staffRate = request.POST.get('staffRate')
            obj.toshop_sec    = request.POST.get('toshop_sec')
            d = request.POST.get('date1')
            s = d.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]

            date =  year1 + "-" + month1 + "-" + day1
            obj.date1 = datetime.strptime(date, '%Y-%m-%d')

            obj.login_id = str(request.user)
            obj.status = 'f'

            td = datetime.now()
            obj.current_date = td.strftime('%Y-%m-%d')
 
            obj.save()
            
        submitvalue = request.POST.get('draft')
        if submitvalue=='draft':
            # Date_f = ('%d-%m-%Y , %Y-%m-%d')
            # date_of = DateField(input_formats=settings.Date_f)
            obj = Intershop338()          
            obj.shop_sec        = request.POST.get('shop_sec')
            obj.staffNo          = request.POST.get('staffNo')
            obj.staffName        = request.POST.get('staffName')
            obj.staffDesg      = request.POST.get('staffDesg')
            obj.reference_authority = request.POST.get('reference_authority')
            obj.staffRate = request.POST.get('staffRate')
            obj.toshop_sec    = request.POST.get('toshop_sec')
            d = request.POST.get('date1')
            s = d.split('-')
            month1 = s[1]
            day1 = s[0]
            year1 = s[2]

            date =  year1 + "-" + month1 + "-" + day1
            obj.date1 = datetime.strptime(date, '%Y-%m-%d')

            obj.login_id = str(request.user)
            obj.status = 'd'

            td = datetime.now()
            obj.current_date = td.strftime('%Y-%m-%d')
 
            obj.save()
    

        submitvalue = request.POST.get('viewdraft')
       
        if submitvalue =='viewdraft':      
            
            shop_sec        = request.POST.get('shop_sec')
            staffNo          = request.POST.get('staffNo')
            staffName        = request.POST.get('staffName')
            staffDesg      = request.POST.get('staffDesg')
            reference_authority = request.POST.get('reference_authority')
            staffRate = request.POST.get('staffRate')
            toshop_sec    = request.POST.get('toshop_sec')
            date1        = request.POST.get('date1')
           
            submitvalue = request.POST.get('i.staffNo')
            obj = list(Intershop338.objects.filter(status = 'd').values('shop_sec', 'staffNo','staffName', 'staffDesg', 'reference_authority','staffRate', 'toshop_sec','date1').distinct())
           
            context = {
                        
                        
                        'obj': obj,
                        'shop_sec': shop_sec,
                        'staffNo' :staffNo,
                        'staffName' : staffName,
                        'staffDesg':staffDesg,
                        'reference_authority':reference_authority,
                        'staffRate':staffRate,
                        'toshop_sec':toshop_sec,
                        'date1':date1,
                        
                        'subnav':subnav,
            }

    return render(request,"m338view.html",context)

def m338getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        #wo_no = request.GET.get('wo_no')
        staff_no=list(M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def m338authority(request):
    if request.method == "GET" and request.is_ajax():
        reference_authority = request.GET.get('reference_authority')        
        return JsonResponse(reference_authority, safe = False)
    return JsonResponse({"success":False}, status=400)

def edit_status(request):
  
    if request.method == "GET" and request.is_ajax():
       
        id = request.GET.get('id1')
        
        Intershop338.objects.filter(staffNo = id).update(status = 'f')
        return JsonResponse(id, safe = False)
    return JsonResponse({"success":False}, status = 400)
def m338report(request):
    if request.method == "GET" and request.is_ajax():
        obj2 = Intershop338.objects.all()
        return JsonResponse(id, safe = False)
    return JsonResponse({"success":False}, status = 400)


def gen_report(request):
    if request.method == "GET" and request.is_ajax():
        dfrom = request.GET.get('date1')
        dto = request.GET.get('date2')
       
        a = []
        for i in Intershop338.objects.raw('SELECT "SHOP_SEC", "STAFF_NO", "STAFF_NO", "STAFF_DESG", "REFERENCE_AUTHORITY", "STAFF_RATE", "TOSHOP_SEC", "DATE1" FROM "dlw_intershop338" WHERE "DATE1" >=%s and "DATE1" <=%s;',[dfrom,dto]):
            a.append({'shop_sec':i.shop_sec, 'staffNo' : i.staffNo, 'staffName' : i.staffName,'staffDesg' : i.staffDesg, 'staffRate' : i.staffRate, 'reference_authority' : i.reference_authority, 'toshop_sec' : i.toshop_sec, 'date' : i.date1 })          

        return JsonResponse(a, safe = False)
    return JsonResponse({"success":False}, status = 400)








@login_required
@role_required(urlpass='/sanction_rollview/')

def sanction_rollview(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    if "Superuser" in rolelist:
        tm=Shemp.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
            context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        print(submitvalue)
        if submitvalue=='Proceed':
            shop_sec= request.POST.get('shop_sec')
            reqf=list(sanctionSSE.objects.filter(shopsec=shop_sec).values('shopsec','desig','sanc'))
            shopname=list(Shop.objects.filter(shop=shop_sec).values('sh_desc').distinct())
            print("shopname : ",len(shopname))
            sub=empmast.objects.annotate(emp=Substr("empno",7,5)).distinct() 
            for i in range(0,len(reqf)):
                c=0
                for j in Shemp.objects.filter(staff_no__in=Subquery(sub.values('emp')),shopsec='2303',desgn__startswith=reqf[i]['desig']).values('name','staff_no').distinct():
                    c=c+1
                reqf[i].update({'roll':c})
            if "Superuser" in rolelist:
                tm=Shemp.objects.all().values('shopsec').distinct()  
                tmp=[]
                for on in tm:
                    tmp.append(on['shopsec'])
                context={
                    'sub':1,
                    'reqf':reqf,
                    'nav':nav,
                    'shop_sec':shop_sec,
                    'lenm' :2,
                    'roles':tmp,
                    'ip':get_client_ip(request),
                    'subnav':subnav,
                    'shopname':shopname,
                    
                }
            elif(len(rolelist)==1):
                context = {
                    'sub':1,
                    'reqf':reqf,
                    'nav':nav,
                    'shop_sec':shop_sec,
                    'lenm' :2,
                    'roles':tmp,
                    'ip':get_client_ip(request),
                    'subnav':subnav,
                    'shopname':shopname,
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'reqf':reqf,
                    'nav':nav,
                    'shop_sec':shop_sec,
                    'lenm' :2,
                    'roles':tmp,
                    'ip':get_client_ip(request),
                    'subnav':subnav,
                    'shopname':shopname,
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
                    'nav':nav,
                    'lenm' :2,
                    'roles':tmp,
                    'ip':get_client_ip(request),
                    'subnav':subnav,
                    'shop_sec':shop_sec,
                    'reqf':reqf,
                    'date':date,
                    'shopname':shopname,
                }
    return render(request,"sanction_rollview.html",context)  




@login_required
@role_required(urlpass='/sanction_formview/')

def sanction_formview(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    if "Superuser" in rolelist:
        tm=Shemp.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
            # first_person = Person.objects.raw('SELECT * FROM myapp_person')[0]

        # for p in empmast.objects.raw('SELECT * FROM public."dlw_empmast" '):
        #     print(p)

        # for p in Shemp.objects.raw("SELECT 1 as id ,"
        #     " (SELECT * FROM public.""SHEMP"" "  ):
        #     print(p)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    if request.method == "POST":
        submitvalue = request.POST.get('proceed')
        if submitvalue=='submit':
            shop_sec= request.POST.get('shop_sec')
            print(shop_sec)
            totindb=request.POST.get('totmebs')
            now = datetime.datetime.now()
            user=request.user
            # print(totindb)
            for tb in range(1,int(totindb)+1):
                desig=request.POST.get('desig1'+str(tb))
                san_no=request.POST.get('san_no'+str(tb))
                pre=list(sanctionSSE.objects.filter(shopsec=shop_sec,desig=desig).values('id'))
                print(pre)
                if(shop_sec==None or desig==None or san_no==None or now==None or user==None):
                    pass
                else:
                    if len(pre)>0:
                        sanctionSSE.objects.filter(shopsec=shop_sec,desig=desig).update(sanc=str(san_no),login_id=str(user), last_modified=str(now))
                    else:
                        sanctionSSE.objects.create(shopsec=str(shop_sec), desig=str(desig), sanc=str(san_no),login_id=str(user), last_modified=str(now))          
    return render(request,"sanction_formview.html",context) 


@login_required
@role_required(urlpass='/IDcertificate/')
def IDcertificate(request):
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
        
        # print(tm)
        d_id=list(empmast.objects.filter(~Q(desig_longdesc__startswith='CONTRACT'),dept_desc="MEDICAL",decode_paycategory='GAZ').values('empno').distinct())
        print(d_id)
        tmp=[]
        for on in d_id:
            tmp.append(on['empno'])
        #print(tmp)
        context = {
            'sub':0,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'doctors':tmp
        }
    #if request.method =="POST":

        #submitvalue = request.POST.get('submit')
     

        #if submitvalue =='submit':
            #form_no=request.POST.get('icerti')
            #eno=request.POST.get('emp_no')
            #eno=request.GET["emp_no"]
            #print("eno:=",eno)
            #dno=request.POST.get('demp_no')
            #print("dno:=",dno)
            #bno=request.POST.get('book_no')
            #mcno=request.POST.get('mc_no')
            #pb=request.POST.get('inj_part')
            #n=request.POST.get('nature')
            #dc=request.POST.get('contd')
            #ad=request.POST.get('acc_date')
            #table1_id.objects.raw('')
            #a=table1_id.objects.create(bookno=bno,medical=mcno,empno=eno,demp_no=dno)
            #table2_id.objects.create(accdient=ad,part=pb,nature=n,disability=dc,medicalcno=a)
    
    return render(request,"IDcertificate.html",context)        

    




def certificate(request):
    if request.method == "GET" and request.is_ajax():
        emp= request.GET.get('emp_no')
        #print("emp:  ",emp)
        obj=list(empmast.objects.filter(empno=emp).values('empname','desig_longdesc','ticket_no').distinct())
        #print("obj----",obj)
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success":False}, status=400)       

def certificate1(request):
    if request.method == "GET" and request.is_ajax():
        demp= request.GET.get('emp_no')
        #print("doctor empNo:  ",demp)
        obj=list(empmast.objects.filter(empno=demp).values('empname','desig_longdesc').distinct())
        return JsonResponse(obj,safe=False)
    
    return JsonResponse({"success":False}, status=400)

def certificate2(request):
    #d={}
    l=[]
    if request.method == "GET" and request.is_ajax():
        no= request.GET.get('mc_no')
        print("medical no:  ",no)
        obj=list(table1_id.objects.filter(medical=no).values('empno','demp_no','bookno').distinct())
        obj1=list(table2_id.objects.filter(medicalcno=no).values('accdient','part','nature','disability').distinct())
        #d={'table1':obj,'table2':obj1}
        #obj=table2_id.objects.select_related().filter(medical=no)
        #obj=table2_id.objects.all().values('empno','demp_no','bookno','accdient','part','nature','disability')
        l.append(obj)
        l.append(obj1)
        print(l)
        print(len(l))
        return JsonResponse(l,safe=False)
    
    return JsonResponse({"success":False}, status=400)

def save_s(request):
    context={}
    if request.method == "GET" and request.is_ajax():
            eno=request.GET.get('emp_no')

            #eno=request.GET["emp_no"]
            print("eno:=",eno)
            dno=request.GET.get('demp_no')
            print("dno:=",dno)
            bno=request.GET.get('book_no')
            print("bno:=",bno)
            mcno=request.GET.get('mc_no')
            print("mc_no:=",mcno)
            pb=request.GET.get('inj_part')
            print("inj_part:=",pb)
            n=request.GET.get('nature')
            print("nature:=",n)
            dc=request.GET.get('contd')
            print("contd:=",dc)
            ad=request.GET.get('acc_date')
            print("acc_date:=",ad)
            a=table1_id.objects.create(bookno=str(bno),medical=str(mcno),empno=str(eno),demp_no=str(dno))
            table2_id.objects.create(accdient=str(ad),part=str(pb),nature=str(n),disability=dc,medicalcno=a)
            return JsonResponse(context,safe=False)
    return JsonResponse({"success":False}, status=400)

def GenPdf(request, *args, **kwargs):
    date1 = request.GET.get('date1')
    book_no = request.GET.get('book_no')
    mc_no = request.GET.get('mc_no')
    acc_date = request.GET.get('acc_date')
    t_no=request.GET.get('t_no')
    emp_no = request.GET.get('emp_no')
    emp_name = request.GET.get('emp_name')
    emp_des = request.GET.get('emp_des')
    demp_no = request.GET.get('demp_no')
    dname = request.GET.get('dname')
    d_des = request.GET.get('d_des')
    inj_part = request.GET.get('inj_part')
    nature = request.GET.get('nature')
    contd = request.GET.get('contd')
   
   # m14_date=datetime.datetime.now().strftime ("%d-%m-%Y")
    data = {
        'date1':date1,
        'book_no':book_no,
        'mc_no':mc_no,
        'acc_date':acc_date,
        'emp_no':emp_no,
        't_no':t_no,
        'emp_name':emp_name,
        'emp_des':emp_des,
        'demp_no':demp_no,
        'dname':dname,
        'd_des':d_des,
        'inj_part':inj_part,
        'nature':nature,
        'contd':contd,
           
        }
    pdf = render_to_pdf('certi.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
    

@login_required
@role_required(urlpass='/partqry/')
def partqry(request):
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
        tm=shop_section.objects.all()
        tmp=[]
        for on in tm:
            tmp.append(on.section_code)
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles':tmp
        }
    return render(request,'partqry.html',context)


def partqry1(request):
    if request.method == 'GET' and request.is_ajax():  
    
        part= request.GET.get('Txtpart_no')
        data_list=list(Partnew.objects.filter(gm_ptno=part).values('gm_ptno','des','part_no','it_cat','um','mb').distinct())        
        if(len(data_list)>0):
            return JsonResponse(data_list,safe = False)
        else:
            data_list=list(Partnew.objects.filter(part_no=part).values('gm_ptno','des','part_no','it_cat','um','mb').distinct())
            if(len(data_list)>0):
                return JsonResponse(data_list,safe = False)                          
    return JsonResponse({"success":False},status=400)




@login_required
@role_required(urlpass='/fitcertificate/')
def fitcertificate(request):
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
        tm=MG36.objects.all().values('shop_sec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shop_sec'])
        d_id=empmast.objects.filter(~Q(desig_longdesc__startswith='CONTRACT'),dept_desc="MEDICAL",decode_paycategory='GAZ').values('empno').distinct()
        tmp1=[]
        for on in d_id:
            tmp1.append(on['empno'])
        form=list(FitCertificate.objects.all().values('id').distinct().order_by('-id'))
        
        if(form==[]):
            formid=1
        else:
            formid=form[0]['id']
            formid=int(formid)+1

        context={
            'sub':0,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'doctors':tmp1,
            'subnav':subnav,
            'formid':formid,
        }
    elif(len(rolelist)==1):        
        context = {
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),            
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
       
    return render(request,"fitcertificate.html",context)        


def fitCertificateGetEmp(request):
    if request.method == "GET" and request.is_ajax():  
        
        shop_sec = request.GET.get('shop_sec')
        staff_no = list(MG36.objects.filter(shop_sec = shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no,safe = False)
    return JsonResponse({"success":False}, status=400)


def fitCertificateGetEmpAllDetails(request):
    if request.method == "GET" and request.is_ajax():   
        shop_sec = request.GET.get('shop_sec')
        
        staff_no = request.GET.get('staff_no')
              
        obj = empmast.objects.all().values('empno')
        
        for staff in obj:
            if staff['empno'][-5:] == staff_no:
                var = staff['empno']
                obj1 =list(empmast.objects.filter(empno=var).values('empname','desig_longdesc','dept_desc','station_des').distinct())

        return JsonResponse(obj1,safe = False)
    return JsonResponse({"success":False}, status=400)

def fitCertificateGetDoctor(request):
    if request.method == "GET" and request.is_ajax():  
        doctor_id = request.GET.get('doctor_id') 
        obj =list(empmast.objects.filter(empno=doctor_id).values('desig_longdesc','empname').distinct())
        return JsonResponse(obj,safe = False)
    return JsonResponse({"success":False}, status=400)

def FitcertificateGetDate(request):
    if request.method == "GET" and request.is_ajax():  
        staff_no = request.GET.get('staff_no')       
        dat=list(MG36.objects.filter(staff_no=staff_no).values('date_app').distinct())
        s=list(dat[0]['date_app'])
        date=''.join(map(str,s))
        date = date[8:10]+"-"+date[5:7]+"-"+date[0:4]
        return JsonResponse(date,safe = False)
    return JsonResponse({"success":False}, status=400)

def FitCertificatePdf(request, *args, **kwargs):
    formno = request.GET.get('formno')
    opdno = request.GET.get('opdno')
    wardno = request.GET.get('wardno')
    namep = request.GET.get('namep')
    desig = request.GET.get('desig')
    dept = request.GET.get('dept')
    station = request.GET.get('station')
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    date3 = request.GET.get('date3')
    date4 = request.GET.get('date4')
    date5 = request.GET.get('date5')
    date6 = request.GET.get('date6')
    date7 = request.GET.get('date7')
    design = request.GET.get('design')
    named = request.GET.get('named')
    data = {
        'formno':formno,
        'opdno':opdno,
        'wardno':wardno,
        'namep':namep,
        'desig':desig,
        'dept':dept,
        'station':station,
        'date1':date1,
        'date2':date2,
        'date3':date3,
        'date4': date4,
        'date5':date5,
        'date6':date6,
        'date7':date7,
        'design':design, 
        'named':named,
        }
    pdf = render_to_pdf('fitcertificatereport.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


def FitInfoSave(request):
    context={}
    if request.method == "GET" and request.is_ajax():
            form_no=request.GET.get('form_no')
            opd_no=request.GET.get('opd_no')
            ward_no=request.GET.get('ward_no')   
            shop_section=request.GET.get('shop_section')     
            staff_no=request.GET.get('staff_no')         
            date1=request.GET.get('date1')        
            date2=request.GET.get('date2')
            date3=request.GET.get('date3')
            date4=request.GET.get('date4')
            date5=request.GET.get('date5')
            date6=request.GET.get('date6')
            doc_id=request.GET.get('doc_id')
            doc_name=request.GET.get('doc_name')
            desg_doc=request.GET.get('desg_doc')
            date7=request.GET.get('date7')
            formno=str(form_no)+"/"+opd_no+"/"+ward_no
            cuser=request.user
            now = datetime.datetime.now()

            fitcertiobj =FitCertificate.objects.filter(form_no=formno).distinct()
            if len(fitcertiobj) == 0:
                    
                fitcertiobj=FitCertificate.objects.create(form_no=str(formno),shop_section=shop_section,staff_no=staff_no,treatement_start_date=date1,treatement_end_date=date2,
                leave_from =date3 ,leave_to=date4,fail_to_avail_from=date5,fail_to_avail_to=date6,desg_doc=desg_doc,
                date_of_fitcertificate=date7,login_id=str(cuser),doc_employee_id=doc_id,doctor_name=doc_name,last_modified=now)
            else:
                FitCertificate.objects.filter(form_no=formno).update(form_no=str(formno),shop_section=shop_section,staff_no=staff_no,treatement_start_date=date1,treatement_end_date=date2,
                leave_from =date3 ,leave_to=date4,fail_to_avail_from=date5,fail_to_avail_to=date6,desg_doc=desg_doc,
                date_of_fitcertificate=date7,login_id=str(cuser),doc_employee_id=doc_id,doctor_name=doc_name,last_modified=now)
                staff_no=FitCertificate.objects.all().values('staff_no').distinct()

            return JsonResponse(context,safe=False)
    return JsonResponse({"success":False}, status=400)

def FitDetails(request):
    if request.method == "GET" and request.is_ajax():  
        form_no = request.GET.get('formno') 
        l=[]
        obj =list(FitCertificate.objects.filter(form_no = form_no).values('treatement_start_date','treatement_end_date','staff_no','shop_section','leave_from','leave_to','fail_to_avail_from','fail_to_avail_to','doc_employee_id','doctor_name','desg_doc').distinct())
        for i in obj:
            s = i['staff_no']
        temp = empmast.objects.all().values('empno')
        for staff in temp:
            if staff['empno'][-5:] == s:
                var = staff['empno']
                obj1 =list(empmast.objects.filter(empno=var).values('empname','desig_longdesc','dept_desc','station_des').distinct())
        
        l.append(obj)
        l.append(obj1)
        return JsonResponse(l,safe = False)
    return JsonResponse({"success":False}, status=400)

@login_required
@role_required(urlpass='/mg21views/')
def mg21views(request):
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
        tm=M5SHEMP.objects.all().values('shopsec').distinct()
        tmp=[]
        for on in tm:
            tmp.append(on['shopsec'])
        context={
            'sub':0,
            'lenm' :2,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles':tmp,
            'subnav':subnav,
        }
    elif(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            req = M5DOCnew.objects.all().filter(shop_sec=rolelist[i]).values('batch_no').distinct()
            wo_nop =wo_nop | req
            
        context = {
            'obj1' : obj1,
            'sub':0,
            'subnav':subnav,
            'lenm' :len(rolelist),
            'wo_nop':wo_nop,
            'nav':nav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'lenm' :len(rolelist),
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'roles' :rolelist
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('save')
        if submitvalue=='proceed':
            from datetime import date
            shop_sec = request.GET.get('shop_sec')
            staff_no = request.GET.get('staff_no')
            obj1 = list(empmast.objects.filter(empno = staff_no).values('empname','desig_longdesc','payrate').distinct())
            noprint=0
            context = {
                'obj1': obj1,
                'ran':range(1,32),
                'len': 31,
                'shop_sec': shop_sec,
                'noprint':noprint,
                'staff_no': staff_no,
                'sub':1,
                'nav':nav,
                'ip':get_client_ip(request),  
                'subnav':subnav,     
            }


        submitvalue = request.POST.get('SAVE')
        if submitvalue=='SAVE':
             
            obj = MG21TAB()
    
            obj.shop_sec        = request.POST.get('shop_sec')
            obj.staffNo          = request.POST.get('staffNo')
            obj.staffName        = request.POST.get('staffName')
            obj.staffDesg      = request.POST.get('staffDesg')
            obj.reportno      = request.POST.get('sse1')
            obj.reportdate = request.POST.get('date1')
            obj.resumedate = request.POST.get('date2')
            obj.sse    = request.POST.get('sse')
            obj.login_id            = str(request.user)
            obj.current_date     = datetime.datetime.now().strftime("%d-%m-%Y")
            obj.save()

            context = {
                        'obj': obj,
                        'subnav':subnav,
            }

    return render(request,"mg21views.html",context)

def mg21getreportno(request):
    if request.method == "GET" and request.is_ajax():
        reportno = request.GET.get('reportno')
        #wo_no = request.GET.get('wo_no')
        reportno=list(MG21TAB.objects.filter(reportno=reportno).values('staffNo').distinct())
        return JsonResponse(reportno, safe = False)
    return JsonResponse({"success":False}, status=400)

def m27getWorkOrder(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        print(shop_sec)
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').distinct())
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)





def m338get_details(request):
    if request.method == "GET" and request.is_ajax():
        staff_no = request.GET.get('staff_no') 
        shop_sec = request.GET.get('shop_sec')
        obj = empmast.objects.all().values('empno','empname','desig_longdesc') 
        obj1=[]  
        # getdetail = list(M5SHEMP.objects.filter(staff_no = staffNo).values('name').exclude(name__isnull=True).distinct())
        for staff in obj:
            
            if staff['empno'][-5:] == staff_no:
                var = staff['empno']
                obj1 = list(empmast.objects.filter(empno = var).values('empno','empname','desig_longdesc', 'payrate').distinct())
                print(obj1)
        return JsonResponse(obj1, safe = False)
    return JsonResponse({"success":False}, status=400)

