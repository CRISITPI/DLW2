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
# Create your views here.
#
#
#
#
#
#
#


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
        else:
            messages.error(request,'error')
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
        else:
            messages.error(request,'error')
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
        else:
            messages.error(request,'error')
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
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
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
            shopsec= request.POST.get('shopsec')
            partno= request.POST.get('partno')
            print("this is part no:",partno)
            return m1genrept1(request,partno,shopsec)
    

    return render(request,"m1view.html",context)


def m1getpano(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        print(shop_sec)
        pano = list(Oprn.objects.filter(shop_sec = shop_sec).values('part_no').distinct())
        print(pano)
        return JsonResponse(pano, safe = False)
    return JsonResponse({"success":False}, status=400)





@login_required
@role_required(urlpass='/m1view/')
def m1genrept1(request,prtno,shopsec):
    from .models import Part,Partalt,Nstr
    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")
    # print("d1 =", d1)
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    epcv=0
    ptcv=0
    rmpart=0
    obj=Part.objects.filter(partno=prtno).values('des','drgno','drg_alt','size_m','spec','weight').distinct()
    print(obj)
    obj3=Nstr.objects.filter(pp_part=prtno).values('epc','ptc','cp_part').distinct()
    print(obj3[0])
    if len(obj3):
        epcv=obj3[0]['epc']
        ptcv=obj3[0]['ptc']
        rmpart=obj3[0]['cp_part']
    obj2 = Oprn.objects.filter(part_no=prtno).values('opn','shop_sec','lc_no','des','pa','at','ncp_jbs','lot','m5_cd','updt_dt').order_by('shop_sec','opn')
    patotal=0
    attotal=0
    if len(obj2):
        for op in obj2:
            patotal=patotal+op['pa']
            attotal=attotal+op['at']
    context={
        'obj1':obj,
        'prtno':prtno,
        'dtl':obj2,
        'nav':nav,
        'subnav':subnav,
        'obj3':obj3,
        'ip':get_client_ip(request),
        'roles' :rolelist,
        'pttl':patotal,
        'attl':attotal,
        'dt':d1,
        'epcv':epcv,'ptcv':ptcv,'rmpart':rmpart,
    }
    if request.method=='POST':
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

           # print(doc_no)
            
            obj  = Oprn.objects.filter(shop_sec=shop_sec, part_no=part_no).values('qtr_accep','mat_rej','lc_no','pa','at','des').distinct()
            obj1 = M5DOCnew.objects.filter(batch_no=wo_no,shop_sec=shop_sec, part_no=part_no,brn_no=brn_no,m5glsn=doc_no).values('cut_shear','pr_shopsec','n_shopsec','l_fr','l_to','qty_insp','inspector','date','remarks','worker','m2slno','qty_ord','m5prtdt','rm_ut','rm_qty','tot_rm_qty','rej_qty','rev_qty').distinct()
            obj2 = Part.objects.filter(partno=part_no).values('drgno','des','partno').order_by('partno').distinct()
            obj3 = Batch.objects.filter(bo_no=wo_no,part_no=part_no).values('batch_type','part_no').order_by('part_no').distinct()
            obj4 = M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('shopsec','staff_no','date','flag','name','cat','in1','out','ticket_no','month_hrs','total_time_taken').distinct()
            obj5 = M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('shopsec','staff_no','name','ticket_no','flag')[0]
            print("obj1",obj1)
            print("obj4",obj4)
           # print("oj4 len",len(obj4))
            ticket= randint(1111,9999)
            leng = obj.count()
            leng1=obj1.count()
            leng2=obj2.count()
            leng3=obj3.count()
            leng4=obj4.count()
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
            
                        'obj5':obj5,
                        'ticket1':ticket,
                        'sub': 1,
                        'len': leng,
                        'len1':leng1,
                        'len2':leng2,
                        'len3':leng3,
                        'len4':leng4,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        #'assm_no':assm_no,
                        'brn_no': brn_no,
                        'doc_no': doc_no,
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
                        'sub': 1,
                        'len': leng,
                        'len1':leng1,
                        'len2':leng2,
                        'len3':leng3,
                        'len4':leng4,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        #'assm_no':assm_no,
                        'brn_no': brn_no,
                        'doc_no': doc_no,
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
                        'sub': 1,
                        'len': leng,
                        'len1':leng1,
                        'len2':leng2,
                        'len3':leng3,
                        'len4':leng4,
                        'shop_sec': shop_sec,
                        'part_no': part_no,
                        'wo_no': wo_no,
                        #'assm_no':assm_no,
                        'brn_no': brn_no,
                        'doc_no': doc_no,
                        'staff_no':staff_no,
                        'subnav':subnav
                    }    
        if submitvalue=='submit':
            leng=request.POST.get('len')
            shopsec= request.POST.get('shopsec')
            partno= request.POST.get('partno')
            brn_no = request.POST.get('brn_no')
            inoutnum=request.POST.get("inoutnum")
            len4=request.POST.get('len4')
            qty_insp = request.POST.get('qty_insp')
            inspector = request.POST.get('inspector')
            date = request.POST.get('date')
            remarks = request.POST.get('remarks')
            worker = request.POST.get('worker')
            
            in1 = request.POST.get('in1')
            out = request.POST.get('out')
            cat = request.POST.get('cat')
            staff_no = request.POST.get('staff_no')
            ticket_no = request.POST.get('ticket_no')
            month_hrs = request.POST.get('month_hrs')
            total_time_taken = request.POST.get('total_time_taken')
            date =  request.POST.get('date1')
            rm_ut =  request.POST.get('rm_ut')
            rev_qty=request.POST.get('rev_qty')
            rej_qty=request.POST.get('rej_qty')
            print("revqty",rev_qty)
            print("rejqty",rej_qty)


           # print(remarks)
           # print(qty_insp)
           # print(inspector)
           # print(worker)
            print(date)

            print("@")
            #print(in1)
            #print(out)
           # print(date)

            M5DOCnew.objects.filter(shop_sec=shopsec,part_no=partno,brn_no=brn_no).update(qty_insp=int(qty_insp),inspector=int(inspector),date=str(date),remarks=str(remarks),rev_qty=int(rev_qty),rej_qty=int(rej_qty),worker=str(worker))             
            staff_no = request.POST.get('staff_nohid')
            name = request.POST.get('namehid')
            ticket_no = request.POST.get('ticket_nohid')
            cat = request.POST.get('cat1')
            m5upd=M5SHEMP.objects.filter(shopsec=shopsec,staff_no=staff_no,cat=cat)
            print("m5upd",m5upd)
            
            for i in range(1, int(len4)+1):

                print("i",i)
                in1 = request.POST.get('in1'+str(i))

                

                out = request.POST.get('out'+str(i))
                lc_no = request.POST.get('lc_no'+str(i))
               # brn_no = request.POST.get('brn_no'+str(i))
                cat = request.POST.get('cat'+str(i))
                # staff_no = request.POST.get('staff_no'+str(i))
                # ticket_no = request.POST.get('ticket_no'+str(i))
                month_hrs = request.POST.get('month_hrs'+str(i))
                total_time_taken = request.POST.get('total_time_taken'+str(i))
                # name = request.POST.get('name'+str(i))
                date = request.POST.get('date'+str(i))

                # M5SHEMP.objects.filter(shopsec=shopsec,staff_no=staff_no,cat=cat).update(in1=str(in1),out=str(out),month_hrs=int(month_hrs),total_time_taken=str(total_time_taken),date=str(date),ticket_no=int(ticket_no))

           # print(worker)
           # print(date)
            print("leng",leng)
            
            for i in range(1, int(leng)+1):
                qtyac = request.POST.get('qtyac'+str(i))
                matrej = request.POST.get('matrej'+str(i))
                lc_no = request.POST.get('lc_no'+str(i))
                pa = request.POST.get('pa'+str(i))
                at = request.POST.get('at'+str(i))
                
               
                print("staff No",staff_no)
                print(lc_no)
                print(qtyac)
                print(matrej)
                print(at)
                print(pa)
                Oprn.objects.filter(shop_sec=shopsec, part_no=partno,lc_no=lc_no,pa=pa,at=at).update(qtr_accep=int(qtyac),mat_rej=int(matrej))
                
               
                 

            print("len4",len4,"inoutnum",inoutnum)
            
            for i in range(int(len4)+1, int(inoutnum)+1):
                in1 = request.POST.get('in1add'+str(i))
                out = request.POST.get('outadd'+str(i))
                lc_no = request.POST.get('lc_no'+str(i))
               # brn_no = request.POST.get('brn_no'+str(i))
                cat = request.POST.get('catadd'+str(i))
                # staff_no = request.POST.get('staff_no'+str(i))
                # ticket_no = request.POST.get('ticket_noadd'+str(i))
                month_hrs = request.POST.get('month_hrsadd'+str(i))
                total_time_taken = request.POST.get('total_time_takenadd'+str(i))
                # name = request.POST.get('name'+str(i))
                date = request.POST.get('dateadd'+str(i))
                print("j",i)
               
                if len(cat)==1:
                    cat="0"+cat
                print(name)
                print(in1)
                print(out) 
                print(month_hrs)   
                print(cat,staff_no,ticket_no,total_time_taken)
                print("Create new row")
                M5SHEMP.objects.create(shopsec=shopsec,staff_no=staff_no,name=name,in1=str(in1),out=str(out),month_hrs=int(month_hrs),total_time_taken=str(total_time_taken),cat=int(cat),date=str(date),ticket_no=int(ticket_no))
               
                
                wo_no=M5DOCnew.objects.all().values('batch_no').distinct()

    return render(request,"m5view.html",context)


def m5getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        # print(shop_sec)
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').distinct())
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
        doc_no = list(M5DOCnew.objects.filter(batch_no =wo_no,brn_no=br_no,shop_sec=shop_sec,part_no=part_no).values('m5glsn').exclude(m2slno__isnull=True).distinct())
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m5getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        # staff_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        br_no = list(M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m12view(request):
    
    rolelist=[2301,2302,2303,304]
    wo_no = user_master.objects.none()
    if(len(rolelist)==1):
        for i in range(0,len(rolelist)):
            w1 = Oprn.objects.filter(shop_sec=rolelist[i]).values('part_no').distinct()
            req = Batch.objects.filter(part_no__in=w1).values('bo_no').distinct()
            wo_no =wo_no | req
        context = {
            'sub':0,
            'len' :len(rolelist),
            'wo_no':wo_no,
            #'nav':nav,
            'ip':get_client_ip(request),
            #'usermaster':usermaster,
            'roles' :rolelist,
            'lent':0,
        }
        # return render(request,"m2view.html",context)
    elif(len(rolelist)>1):
        context = {
            'sub':0,
            'len' :len(rolelist),
            #'nav':nav,
            #'ip':get_client_ip(request),
            #'usermaster':usermaster,
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
                    print(obj2)
                   
           
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
            #obj2 = Shemp.objects.filter(shopsec=shop_sec).values('staff_no','name','cat').distinct()
           # amt=0
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
                
                

            #amt=0    
            #patotal=0
            #attotal=0
            #if len(obj2):
            #for op in obj2:
            #patotal=patotal+op['pa']
            #attotal=attotal+op['at']
            #print(obj2)
            
            #leng2 = obj3.count()
           
            #leng2 = obj2.count()

            context = {
                'obj1': obj1,
                'obj2':obj2,
                'obj3':obj3,
                'lent': leng,
                'lent2': leng1,
                #'lent3':leng2,
                'amt1': amt,
                #'obj2': obj2,
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
           

            #name = request.Post.get('name')
            
            for i in range(1, int(leng)+1):
                in1 = request.POST.get('in1'+str(i))
                out = request.POST.get('out'+str(i))
                date = request.POST.get('date'+str(i))
                month = request.POST.get('month'+str(i))
               
                total_time = request.POST.get('total_time'+str(i))
                time_hrs = request.POST.get('total_time'+str(i))
                idle_time = request.POST.get('idle_time'+str(i))
                reasons_for_idle_time = request.POST.get('reasons_for_idle_time'+str(i))
               # cat = request.POST.get('cat')
               # amt = request.POST.get('amt1'+str(i))
                # x=datetime.datetime.now()
                # max_year = M12DOC.objects.latest('updt_date').updt_date
#if len(cat)==1:
 #                   cat="0"+cat
              
                # print(total_time)
                # print(x)    
                # print("MAX DATE",max_year)
                # print(month)
                # print(amt)
                # print(date)
                # print(reasons_for_idle_time)
                M12DOC.objects.filter(shopsec=shopsec,staff_no=staff_no,date=date,month=month).update(date=str(date),in1=str(in1),out=str(out),month=str(month),total_time=str(total_time),idle_time=str(idle_time),reasons_for_idle_time=str(reasons_for_idle_time),time_hrs=str(time_hrs),amt=str(amt))
               
                print(reasons_for_idle_time)
                print(total_time)
                #print(total_hrs)

            for i in range(1, int(inoutnum)+1):
                in1 = request.POST.get('in1add'+str(i))
                out = request.POST.get('outadd'+str(i))
                month = request.POST.get('month_add'+str(i))
                total_time = request.POST.get('total_time_add'+str(i))
                #name = request.POST.get('name'+str(i))
                date = request.POST.get('dateadd'+str(i))
                cat = request.POST.get('catadd'+str(i))
                time_hrs = request.POST.get('total_time_add'+str(i))
                idle_time = request.POST.get('idle_time_add'+str(i))
              # detail_no = request.POST.get('detail_noadd'+str(i))
                reasons_for_idle_time = request.POST.get('reasons_for_idle_timeadd'+str(i))
                #if len(cat)==1:
                 #   cat="0"+cat
                
                print(in1)
                print(cat)
                print(out)
                print(month)
                print(reasons_for_idle_time)
               # print(detail_no)
               
              
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
            date=request.POST.get('date')
            loco_type=request.POST.get('locos')
            airbox_sno=request.POST.get('airbox_sno')
            airbox_make=request.POST.get('airbox_make')
            in_qty=request.POST.get('in_qty')
            out_qty=request.POST.get('out_qty')
            print(bo_no,bo_date,date,loco_type,in_qty,out_qty,airbox_make,airbox_sno)
            if bo_no and bo_date and date and loco_type and airbox_sno and airbox_make and in_qty and out_qty:
               obj=MachiningAirBox.objects.create()
               obj.bo_no=bo_no
               obj.bo_date=bo_date
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
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            airbox_sno=request.POST.get('editairbox_sno')
            airbox_make=request.POST.get('editairbox_make')
            in_qty=request.POST.get('editin_qty')
            out_qty=request.POST.get('editout_qty')
            if bo_no and bo_date and date and loco_type and airbox_sno and airbox_make and in_qty and out_qty:
               MachiningAirBox.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,airbox_sno=airbox_sno,airbox_make=airbox_make,in_qty=in_qty,out_qty=out_qty)
               messages.success(request, 'Successfully Edited!')
            else:
               messages.error(request,"Please Enter S.No.!")

        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            if sno and dislocos:
                MachiningAirBox.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_status=True)
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
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def airbox_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(MachiningAirBox.objects.filter(sno=mysno).values('bo_no','bo_date','airbox_sno','airbox_make','in_qty','out_qty','date','loco_type'))
        print(myval)
        return JsonResponse(myval, safe=False)
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
            third=request.POST.get('date')
            fourth=request.POST.get('locos')
            fifth=request.POST.get('shaft_m')
            sixth=request.POST.get('in_qty')
            seventh=request.POST.get('out_qty')
            if first and second and third and fourth and fifth and sixth and seventh:
                obj=MiscellSection.objects.create()
                obj.bo_no=first
                obj.bo_date=second
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
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            shaft_m=request.POST.get('editshaft_m')
            in_qty=request.POST.get('editin_qty')
            out_qty=request.POST.get('editout_qty')
            if sno and bo_no and bo_date and date and loco_type and shaft_m and in_qty and out_qty:
                MiscellSection.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,shaft_m=shaft_m,in_qty=in_qty,out_qty=out_qty)
                messages.success(request, 'Successfully Edited!')
            else:
               messages.error(request,"Please Enter S.No.!")
        
        if submit=="Dispatch":
            
            first=int(request.POST.get('dissno'))
            second=request.POST.get('dislocos')
            if first and second:
               MiscellSection.objects.filter(sno=first).update(dispatch_to=second,dispatch_status=True)
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
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def miscell_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(MiscellSection.objects.filter(sno=mysno).values('bo_no','bo_date','shaft_m','in_qty','out_qty','date','loco_type'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400) 







@login_required
@role_required(urlpass='/axlewheelmachining_section/')
def axlewheelmachining_section(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    rolelist=usermaster.role.split(", ")
    nav=dynamicnavbar(request,rolelist)
    menulist=set()
    for ob in nav:
        menulist.add(ob.navitem)
    menulist=list(menulist)
    subnav=subnavbar.objects.filter(parentmenu__in=menulist)
    obj2=AxleWheelMachining.objects.all().filter(dispatch_status=False).order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=AxleWheelMachining.objects.filter(dispatch_status=False).values('sno')
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
            eighth=request.POST.get('axle_no')
            ninth=request.POST.get('axle_make')
            tenth=request.POST.get('axle_heatcaseno')
            if first and second and third and fourth and fifth and sixth and seventh and eighth and ninth and tenth:
                obj=AxleWheelMachining.objects.create()
                obj.bo_no=first
                obj.bo_date=second
                obj.date=third
                obj.wheel_no=fourth
                obj.wheel_make=fifth
                obj.loco_type=sixth
                obj.wheel_heatcaseno=seventh
                obj.axle_no=eighth
                obj.axle_make=ninth
                obj.axle_heatcaseno=tenth
                obj.wheelinspection_status=False
                obj.axleinspection_status=False
                obj.save()
                messages.success(request, 'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=AxleWheelMachining.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='save':

            sno=int(request.POST.get('editsno'))
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            wheel_no=request.POST.get('editwheel_no')
            wheel_make=request.POST.get('editwheel_make')
            wheel_heatcaseno=request.POST.get('editwheel_heatcaseno')
            axle_no=request.POST.get('editaxle_no')
            axle_make=request.POST.get('editaxle_make')
            axle_heatcaseno=request.POST.get('editaxle_heatcaseno')
            if bo_no and bo_date and date and loco_type and wheel_make and wheel_no and wheel_heatcaseno and axle_no and axle_make and axle_heatcaseno:
                AxleWheelMachining.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,wheel_no=wheel_no,wheel_make=wheel_make,loco_type=loco_type,wheel_heatcaseno=wheel_heatcaseno,axle_no=axle_no,axle_make=axle_make,axle_heatcaseno=axle_heatcaseno)
                messages.success(request, 'Successfully Edited!')
            else:
                messages.error(request,"Please Enter S.No.!")
                
        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            if sno and dislocos:
                AxleWheelMachining.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_status=True)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            sno=int(request.POST.get('delsno'))
            if sno:
                AxleWheelMachining.objects.filter(sno=sno).delete()
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
                AxleWheelMachining.objects.filter(sno=sno).update(ustwhl_status=oustwhl_status,ustwhl_date=oustwhl_date,ustwhl=oustwhl,hub_lengthwhl=ohub_lengthwhl,tread_diawhl=otread_diawhl,rim_thicknesswhl=orim_thicknesswhl,bore_diawhl=obore_diawhl,inspector_nameaxle=oinspector_namewhl,datewhl=odatewhl,wheelinspection_status=True)
                messages.success(request, 'Wheel Successfully Inspected!')
            else:
                messages.error(request,"Please Select S.No.!")

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
                AxleWheelMachining.objects.filter(sno=sno).update(ustaxle_date=ustaxle_date,ustaxle_status=ustaxle_status,ustaxle=ustaxle,axlelength=axlelength,journalaxle=journalaxle,throweraxle=throweraxle,wheelseataxle=wheelseataxle,gearseataxle=gearseataxle,collaraxle=collaraxle,dateaxle=dateaxle,bearingaxle=bearingaxle,abutmentaxle=abutmentaxle,inspector_nameaxle=inspector_nameaxle,journal_surfacefinishGE=journal_surfacefinishGE,wheelseat_surfacefinishGE=wheelseat_surfacefinishGE,gearseat_surfacefinishGE=gearseat_surfacefinishGE,journal_surfacefinishFE=journal_surfacefinishFE,wheelseat_surfacefinishFE=wheelseat_surfacefinishFE,gearseat_surfacefinishFE=gearseat_surfacefinishFE,axleinspection_status=True)
                messages.success(request, 'Axle Successfully Inspected!')
            else:
                messages.error(request,"Please Enter all records!")

        
        return HttpResponseRedirect("/axlewheelmachining_section/")

    return render(request,"axlewheelmachining_section.html",my_context)

def axle_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def axle_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(AxleWheelMachining.objects.filter(sno=mysno).values('bo_no','bo_date','date','wheel_no','wheel_make','loco_type','wheel_heatcaseno','axle_no','axle_make','axle_heatcaseno'))
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
            # context = {
            #     'obj1': obj1,
            #     'obj2': obj2,
            #     'ran':range(1,2),
            #     'len': 31,
            #     'len2': leng2,
            #     'shop_sec': shop_sec,
            #     'wo_no': wo_no,
            #     'staff_no': staff_no,
            #     'part_no': part_no, 
            #     'mon': mon,
            #     'sub':1,
            #     'nav':nav,
            #     'ip':get_client_ip(request),  
            #     'subnav':subnav,     
            # }
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
                print("hi")
                leng=request.POST.get('len')
                shop_sec= request.POST.get('shop_sec')
                staff_no = request.POST.get('staff_no')
                wo_no = request.POST.get('wo_no')
                part_no = request.POST.get('part_no')
                inoutnum=request.POST.get("inoutnum")
            
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
                    
                # reasons_for_idle_time = request.POST.get('reasons_for_idle_time'+str(i))
                    #print(shopsec)
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
                    #print(in1)
                    #print(date)

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
            if first and second and third and fourth and fifth and sixth:
                obj=PinionPressing.objects.create()
                obj.bo_no=first
                obj.bo_date=second
                obj.date=third
                obj.tm_make=fourth
                obj.tm_no=fifth
                obj.loco_type=sixth
                obj.inspection_status=False
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
            if sno and bo_no and bo_date and date and tm_make and tm_no:
                PinionPressing.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,tm_make=tm_make,tm_no=tm_no)
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
            if sno and dislocos:
                PinionPressing.objects.filter(sno=sno).update(dispatch_to=dislocos)
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
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)
        
def pinion_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(PinionPressing.objects.filter(sno=mysno).values('bo_no','bo_date','loco_type','date','tm_make','tm_no'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)  

def airbox_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(MachiningAirBox.objects.filter(sno=mysno).values('bo_no','bo_date','airbox_sno','airbox_make','in_qty','out_qty','date','loco_type'))
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400) 


def axlepress_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(AxleWheelPressing.objects.filter(sno=mysno).values('bo_no','bo_date','loco_type','date','axle_no','wheelno_de','wheelno_nde','bullgear_no','bullgear_make'))
        AxleWheelMachining.objects.filter(axle_no=myval[0]['axle_no']).update(axlefitting_status=False)
        AxleWheelMachining.objects.filter(wheel_no=myval[0]['wheelno_de']).update(wheelfitting_status=False)
        return JsonResponse(myval, safe=False)
    return JsonResponse({"success":False}, status=400)  

def wheelnde(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('wheel_no')
        print("wheel no:",mybo)
        myval = list(AxleWheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no').exclude(wheel_no=mybo))
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
                print(shop_sec,lv_date,name,ticketno,date)
            messages.success(request, 'Successfully Saved !!!, Select new values to update')
    return render(request, "M20view.html", context)



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
                print(shop_sec,lv_date,name,ticketno,date)
            messages.success(request, 'Successfully Saved !!!, Select new values to update')
    return render(request, "MG33view.html", context)







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
    return render(request,'m27view.html',context)    








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

            M18.objects.create(shopIncharge=str(shopIncharge),shop_sec=str(shop_sec),wo_no=str(wo_no),part_nop=str(part_nop), extraTimePartNo=str(extraTimePartNo), reasonSpecialAllowance=str(reasonSpecialAllowance), forSpecialAllowance=str(forSpecialAllowance), totalExtraTime=str(totalExtraTime),opno=str(opno),opdesc=str(opdesc), discription=str(discription), quantity=str(quantity), setExtraTime=str(setExtraTime), setno=str(setno))
            messages.success(request, 'Successfully Saved ! Select new values to update')    
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
                rupees = request.POST.get('rs')
                paise = request.POST.get('p')
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
                    mat_rec_date=str(mat_rec_date),last_modified=str(now),login_id=request.user,posted_date=str(posted_date),metric_ton_returned=str(metric_ton_returned),metric_ton_received=str(metric_ton_received),m13_no=str(m13_no),des=str(des),doc_no=str(doc_no),c_d_no=str(c_d_no),qty_ret=str(qty_ret),qty_rec_inward=str(qty_rec_inward))
            
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



def ShowLeaf(request,part,res,code):
    obj1 = Nstr.objects.filter(pp_part=part).filter(cp_part__isnull=False,ptc=code,l_to='9999').values('cp_part').distinct()
    final = obj1
    if final is not None and len(final):
        for i in range(len(final)):
            if final[i]['cp_part'] not in res:
                res.append(final[i]['cp_part'])
                print(len(res))
                ShowLeaf(request,final[i]['cp_part'],res,code)
    return res
    





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
    assmno = EpcCode.objects.all().values('num_1').distinct()
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
                obj1 = ShowLeaf(request,asmno,res,'M')
                print("len = ",obj1)
                # try:
                #     for j in range(len(obj1)):
                #         cstr_buffer.objects.create(pp_part=asmno,cp_part=obj1[j])
                #     messages.success(request, 'Successfully Done!')
                # except:
                #     messages.error(request,'Some Error Occurred')
            elif bval=="Generate Cards" and card=="M4":
                res = []
                obj1 = ShowLeaf(request,asmno,res)
                print("len = ",obj1)
                # try:
                #     for j in range(len(obj1)):
                #         cstr_buffer.objects.create(pp_part=asmno,cp_part=obj1[j])
                #     messages.success(request, 'Successfully Done!')
                # except:
                #     messages.error(request,'Some Error Occurred')
            elif bval=="Generate Cards" and card=="M5":
                res = []
                obj1 = ShowLeaf(request,asmno,res)
                print("len = ",obj1)
                # try:
                #     for j in range(len(obj1)):
                #         cstr_buffer.objects.create(pp_part=asmno,cp_part=obj1[j])
                #     messages.success(request, 'Successfully Done!')
                # except:
                #     messages.error(request,'Some Error Occurred')
            elif bval=="Generate Cards" and card=="M14":
                res = []
                obj1 = ShowLeaf(request,asmno,res)
                print("len = ",obj1)
                # try:
                #     for j in range(len(obj1)):
                #         cstr_buffer.objects.create(pp_part=asmno,cp_part=obj1[j])
                #     messages.success(request, 'Successfully Done!')
                # except:
                #     messages.error(request,'Some Error Occurred')
            else:
                messages.error(request,'Enter all values!')
    return render(request,'CardGeneration.html',context)








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
            'roles' :rolelist
        }
    if request.method == "POST":
        
        submitvalue = request.POST.get('proceed')
        if submitvalue=='Proceed':
            shop_sec = request.POST.get('shop_sec')
            staff_no = request.POST.get('staff_no')
            obj1 =  M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name').distinct()
            obj2=m23doc.objects.filter(emp_no=staff_no,shop_no=shop_sec).values('date','purpose','from_time','to_time').distinct()
            if len(obj2) == 0:
                obj2=range(1,2)
           # obj2 = Shemp.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('name','cat').distinct()
            leng = obj1.count()
            print(obj2)
            #leng2 = obj2.count()
           # print(obj1,"obj1")
            #print(obj2,"obj2")
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
            }
        if submitvalue =='Save':
                    leng=request.POST.get('len')
                    print("HH")
                    
                    from_time = request.POST.get('from_time')
                    to_time = request.POST.get('to_time')
                    purpose = request.POST.get('pur')
                    shops=request.POST.get('shopsec')
                    staffn=request.POST.get('staffno')
                    date=request.POST.get('date')
                    name=request.POST.get('employeename')
                    print(name)
                    m23obj = m23doc.objects.filter(shop_no=shops,emp_no=staffn).distinct()
                    if len(m23obj) == 0:

                        m23doc.objects.create(shop_no=str(shops),emp_no=str(staffn),emp_name=str(name), from_time=str(from_time), to_time=str(to_time), purpose=str(purpose),date=str(date))
                        print("create")
                     
                    else:
                        m23doc.objects.filter(shop_no=shops,emp_no=staffn).update(purpose=str(purpose),from_time=str(from_time),to_time=str(to_time),date=str(date))
                    wo_nop=M5SHEMP.objects.all().values('staff_no').distinct()

    return render(request,"m23view.html",context)
                        

def m23getempno(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        #wo_no = request.GET.get('wo_no')
        staff_no=list(M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').distinct())
        return JsonResponse(staff_no, safe = False)
    return JsonResponse({"success":False}, status=400)








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
    myaxle=AxleWheelMachining.objects.all().values('axle_no')
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
            loco_type=request.POST.get('locos')
            in_date=request.POST.get('in_date')
            frameserial_no=request.POST.get('frameserial_no')
            frame_make=request.POST.get('frame_make')
            frame_type=request.POST.get('frame_type')
            print(bo_no,bo_date,date,loco_type,in_date,frame_make,frame_type,frameserial_no)
            

            if bo_no and bo_date and date and loco_type and frameserial_no and frame_make and frame_type and in_date:
               obj=BogieAssembly.objects.create()
               obj.bo_no=bo_no
               obj.bo_date=bo_date
               obj.date=date
               obj.loco_type=loco_type
               obj.in_date=in_date
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
            frameserial_no=request.POST.get('editframeserial_no')
            frame_make=request.POST.get('editframe_make')
            frame_type=request.POST.get('editframe_type')
            print(bo_no,bo_date,date,loco_type,in_date,frame_make,frame_type,frameserial_no)
        
            if bo_no and bo_date and date and loco_type and frameserial_no and frame_make and frame_type and in_date:
               BogieAssembly.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,frameserial_no=frameserial_no,frame_make=frame_make,frame_type=frame_type,in_date=in_date)
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
            if sno and dislocos:
                BogieAssembly.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_status=True)
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
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)

def bogieassemb_editsno(request):
    if request.method=="GET" and request.is_ajax():
        mysno=request.GET.get('sels_no')
        myval=list(BogieAssembly.objects.filter(sno=mysno).values('bo_no','bo_date','loco_type','date','frameserial_no','frame_make','frame_type','in_date'))
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
            ticketno = request.POST.get('ticket1')
            acc_Date = request.POST.get('date1')
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
    axle=AxleWheelMachining.objects.filter(axlefitting_status=False,axleinspection_status=True).values('axle_no')
    wheelde=AxleWheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no')
    wheelnde=AxleWheelMachining.objects.filter(wheelfitting_status=False,wheelinspection_status=True).values('wheel_no')
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
            date=request.POST.get('date')
            loco_type=request.POST.get('locos')
            axle_no=request.POST.get('axle_no')
            wheelno_de=request.POST.get('wheelno_de')
            wheelno_nde=request.POST.get('wheelno_nde')
            bullgear_no=request.POST.get('bullgear_no')
            bullgear_make=request.POST.get('bullgear_make')
            
            if bo_no and bo_date and date and loco_type and axle_no and wheelno_de and wheelno_nde and bullgear_no and bullgear_make:
               obj=AxleWheelPressing.objects.create()
               obj.bo_no=bo_no
               obj.bo_date=bo_date
               obj.date=date
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
               AxleWheelMachining.objects.filter(axle_no=axle_no).update(axlefitting_status=True)
               AxleWheelMachining.objects.filter(wheel_no=wheelno_de).update(wheelfitting_status=True)  
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
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            axle_no=request.POST.get('editaxle_no')
            wheelno_de=request.POST.get('editwheelno_de')
            wheelno_nde=request.POST.get('editwheelno_nde')
            bullgear_no=request.POST.get('editbullgear_no')
            bullgear_make=request.POST.get('editbullgear_make')
            in_qty=request.POST.get('editin_qty')
            out_qty=request.POST.get('editout_qty')

            if bo_no and bo_date and date and loco_type and axle_no and wheelno_de and wheelno_nde and bullgear_no and bullgear_make and in_qty and out_qty:
               AxleWheelPressing.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,axle_no=axle_no,in_qty=in_qty,out_qty=out_qty,wheelno_de=wheelno_de,wheelno_nde=wheelno_nde,bullgear_no=bullgear_no,bullgear_make=bullgear_make)
               AxleWheelMachining.objects.filter(axle_no=axle_no).update(axlefitting_status=True)
               AxleWheelMachining.objects.filter(wheel_no=wheelno_de).update(wheelfitting_status=True)
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
            if sno and dislocos:
                AxleWheelPressing.objects.filter(sno=sno).update(dispatch_to=dislocos,dispatch_status=True)
                messages.success(request, 'Successfully Dispatched!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        if submit=='Delete':

            sno=int(request.POST.get('delsno'))
            if sno:
                myval=list(AxleWheelMachining.objects.filter(sno=sno).values('wheel_no','axle_no'))
                print(myval)
                AxleWheelMachining.objects.filter(axle_no=myval[0]['axle_no']).update(axlefitting_status=False)
                AxleWheelMachining.objects.filter(wheel_no=myval[0]['wheel_no']).update(wheelfitting_status=False) 
                AxlewheelPressing.objects.filter(sno=sno).delete()
                messages.success(request, 'Successfully Deleted!')
            else:
                messages.error(request,"Please Enter S.No.!")
        
        return HttpResponseRedirect("/axlewheelpressing_section/")

    return render(request,"axlewheelpressing_section.html",my_context)

def axlepress_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date'))
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
                # print(wo_rep)
                m13no = request.POST.get('m13no')
                # print(m13no)
                m15_no = request.POST.get('m15_no')
                print(m15_no)
                rej_cat = request.POST.get('rej_cat')
                print(rej_cat)
                reason = request.POST.get('reason')
                print(reason)
                if m13_sn and qty_tot and qty_ins and qty_pas and qty_rej and vendor_cd and opn and job_no and fault_cd and wo_rep and m15_no and rej_cat and reason and m13no and slno and epc:
                    print("in if cond")
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
            tm1=Part.objects.all().values('partno').distinct()
            
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
            


            # context = {
            #             'tm1':tm1,
            #             'tm2':tm2,
            #             'obj': obj,
            #             'len': leng,
            #             'updt_date':updt_date,
            #             'shop_sec': shop_sec,
            #             'staff_no':staff_no,
            #             'sub' : 1,
            #             'nav':nav,
            #             'ip':get_client_ip(request),  
            #             'subnav':subnav,
            # }
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
            if(part_no==None or matdes==None or quantity==None or weight==None or unit==None):
                pass;
            else:
                # print(updt_date,shop_sec,staff_no,part_no,quantity,weight,unit,now,user)
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
                if(part_no==None or matdes==None or quantity==None or weight==None or unit==None):
                    pass;
                else:
                    # print(updt_date,shop_sec,staff_no,part_no,quantity,weight,unit,now,user)
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

def mg49getmat_des(request):
    
    if request.method == "GET" and request.is_ajax():
        part_no = request.GET.get('part_no')
        print(part_no,"part_no")
        w1 = list(Part.objects.filter(partno=part_no).values('des').distinct())
        wono = w1[0]['des']
        cont ={
            "wono":wono,
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