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
import datetime
from array import array
from django.contrib.sessions.models import Session
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import View
from dlw.models import empmast,M14M4,Cst,testc,navbar,PinionPressing,roles,AxleWheelPressing,shift_history,shift,M2Doc,M5Doc,M5DOCnew,M5SHEMP,Batch,Hwm5,Part,dpo,Oprn,testing_purpose,shop_section,MachiningAirBox,MiscellSection,AxleWheelMachining,subnavbar,Shemp,M7
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
import math
# Create your views here.
#
#
#
#
#
#
#

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
@role_required(allowed_roles=["Superuser"])
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
@role_required(allowed_roles=["Wheel_shop_incharge","Bogie_shop_incharge","2301","2302","Dy_CME/Plg","Dy_CME_Spares","Dy_CMgm","0401","0402","0403"])
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
@role_required(allowed_roles=["Superuser"])
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
@role_required(allowed_roles=["Superuser"])
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
@role_required(allowed_roles=["Wheel_shop_incharge","Bogie_shop_incharge"])
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
@role_required(allowed_roles=["Wheel_shop_incharge","Bogie_shop_incharge"])
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
@role_required(allowed_roles=["Superuser"])
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
@role_required(allowed_roles=["Superuser"])
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
@role_required(allowed_roles=["Superuser"])
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
@role_required(allowed_roles=["Superuser","2301","2302","0401","0402","0403"])
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
                    Oprn.objects.filter(shop_sec=shopsec, part_no=partno, opn=opn).update(qty_prod=int(qtypr),qtr_accep=int(qtyac),work_rej=int(wrrej),mat_rej=int(matrej))
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
@role_required(allowed_roles=["Superuser","2301","2302","0401","0402","0403"])
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
            doc_no= request.POST.get('doc_no')
            part_no= request.POST.get('part_no')
            wo_no=request.POST.get('wo_no')
            brn_no=request.POST.get('brn_no')
            # print("hh")
            # print(doc_no)
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
@role_required(allowed_roles=["Superuser","2301","2302","0401","0402","0403"])
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
            doc_no= request.POST.get('doc_no')
            part_no= request.POST.get('part_no')
            wo_no=request.POST.get('wo_no')
            brn_no=request.POST.get('brn_no')
            # print("hh")
            # print(doc_no)
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
@role_required(allowed_roles=["Superuser","Dy_CME/Plg","Dy_CMgm","Dy_CME_Spares"])
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
@role_required(allowed_roles=["Superuser","Dy_CME/Plg","Dy_CMgm","Dy_CME_Spares"])
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
@role_required(allowed_roles=["Superuser","Dy_CME/Plg","Dy_CMgm","Dy_CME_Spares"])
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
@role_required(allowed_roles=["Superuser","Dy_CME/Plg","Dy_CMgm","Dy_CME_Spares"])
def dpoinput(request):
    from .models import annual_production,barrelfirst
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
        'locolist':locos
    }
    if request.method=="POST":
        submit=request.POST.get('submit')
        if submit=='Proceed':
            b1=0
            loco=request.POST.get('loco')
            b2=request.POST.get('barl2')
            cm=225
            cm2=300
            obj1=barrelfirst.objects.filter(locotype=loco)
            b1=obj1[0].code
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
        } 

        if submit=='Save':
            sub=request.POST.get('sub')
            refn=request.POST.get('refn')
            summary=request.POST.get('summary')
            copyto=request.POST.get('copyto')
            datee=request.POST.get('xTime')
            
            
            locot=request.POST.get('loco')
            ordno=request.POST.get('barl2')
            totbaches=request.POST.get('totbaches')
         
            
            print("locot",locot)
            print("ordno",ordno)
            temp1="loconame"
            idname=[]
            lcname=[]
            ttlcnt=request.POST.get('cm2')
            for i in range(1,int(ttlcnt)+1):
                temp1=temp1+str(i)
                idname.append(temp1)
                temp1="loconame"
            for key in request.POST:
                for temp1 in idname:
                    if key==temp1:
                        lcname.append(request.POST[key])
            
            print("lcname",lcname)
            
            
            for i in range(1,int(totbaches)+1):
               bno=request.POST.get("bno"+str(i))
               qty=request.POST.get("qty"+str(i))
               typ=request.POST.get("typ"+str(i))               
               cumino=request.POST.get("cumino"+str(i))
            
               
            context={
            'nav':nav,
            'subnav':subnav,
            'ip':get_client_ip(request),
            'Role':rolelist[0],
            'cyear':ctp,
            'locolist':locos
        } 

    return render(request, 'dpof.html', context)



def getcumino(request):
    from .models import dpo
    print("dpogetcumi")
    if request.method == "GET" and request.is_ajax():
        print("in")
        cmno=0
       
        loco=request.GET.get('loco')
        locot=request.GET.get('locot')
        ordno=request.GET.get('ordno')
        try:
            print("hell")
            emp=dpo.objects.filter(loconame=loco,locotype=locot,orderno=ordno).exists()
            print("emp",emp)
        except:
            print("hello")
            return JsonResponse({"success":False}, status=400)
       
        if emp is not None:
            cmno=emp.endcumno
        else:
            if loco=='WAP7':
                cmno=111
            else:
                cmno=225
        
        dpo_info={
            "cumino":cmno,
         }
        
        return JsonResponse({"dpo_info":dpo_info}, status=200)

    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(allowed_roles=["Superuser","2301","2302","0401","0402","0403"])
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
                    'obj': obj,
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
                    'obj': obj,
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
@role_required(allowed_roles=["Superuser","2301","2302","0401","0402","0403"])
def m1genrept1(request,prtno,shopsec):
    from .models import Part,Partalt
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
    obj=Part.objects.filter(partno=prtno).values('des','drgno','drg_alt','size_m','spec','weight','ptc').distinct()
    obj3=Partalt.objects.filter(partno=prtno).values('epc').distinct()
    # print(obj)
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
    }
    return render(request,"M1report.html",context)

@login_required
@role_required(allowed_roles=["Superuser","2301","2302","0401","0402","0403"])
def m5view(request):
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
            obj  = Oprn.objects.filter(shop_sec=shop_sec, part_no=part_no).values('qtr_accep','mat_rej','lc_no','pa','at','des').order_by('opn')
            obj1 = M5DOCnew.objects.filter(shop_sec=shop_sec, part_no=part_no).values('cut_shear','pr_shopsec','n_shopsec','l_fr','l_to','qty_insp','inspector','date','remarks','worker','m5prtdt','qty_ord').order_by('opn')
            obj2 = Part.objects.filter(partno=part_no).values('drgno','des').order_by('partno')
            obj3 = Batch.objects.filter(part_no=part_no).values('batch_type').order_by('part_no').distinct()
            obj4 = M5SHEMP.objects.filter(shopsec=shop_sec,staff_no=staff_no).values('shopsec','staff_no','name','cat','in1','out','ticket_no','month_hrs','total_time_taken').distinct()
            leng = obj.count()
            leng1=obj1.count()
            leng2=obj2.count()
            leng3=obj3.count()
            leng4=obj4.count()
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
                    }    
        if submitvalue=='submit':
            leng=request.POST.get('len')
            shopsec= request.POST.get('shopsec')
            partno= request.POST.get('partno')
            brn_no = request.POST.get('brn_no')
            #name = request.Post.get('name')
            
            for i in range(1, int(leng)+1):
                qtyac = request.POST.get('qtyac'+str(i))
                matrej = request.POST.get('matrej'+str(i))
                qtyinsp = request.POST.get('qtyinsp'+str(i))
                inspector = request.POST.get('inspector'+str(i))
                date = request.POST.get('date'+str(i))
                remarks = request.POST.get('remarks'+str(i))
                worker = request.POST.get('worker'+str(i))
                in1 = request.POST.get('in1'+str(i))
                out = request.POST.get('out'+str(i))
                lc_no = request.POST.get('lc_no'+str(i))
               # brn_no = request.POST.get('brn_no'+str(i))
                cat = request.POST.get('cat'+str(i))
                staff_no = request.POST.get('staff_no'+str(i))
                ticket_no = request.POST.get('ticket_no'+str(i))
                month_hrs = request.POST.get('month_hrs'+str(i))
                total_time_taken = request.POST.get('total_time_taken'+str(i))
                Oprn.objects.filter(shop_sec=shopsec, part_no=partno,lc_no=lc_no).update(qtr_accep=int(qtyac),mat_rej=int(matrej))
              
                M5DOCnew.objects.filter(shop_sec=shopsec,part_no=partno,brn_no=brn_no).update(qty_insp=int(qtyinsp),inspector=int(inspector),date=str(date),remarks=str(remarks),worker=str(worker))
                print(date)
                M5SHEMP.objects.filter(shopsec=shopsec,staff_no=staff_no,cat=cat ).update(in1=str(in1),ticket_no=int(ticket_no),out=str(out),month_hrs=int(month_hrs),total_time_taken=int(total_time_taken))
                print(in1)
                print(total_time_taken)
                wo_no=M5DOCnew.objects.all().values('batch_no').distinct()

    return render(request,"m5view.html",context)

def m5getwono(request):
    if request.method == "GET" and request.is_ajax():
        shop_sec = request.GET.get('shop_sec')
        wono = list(M5DOCnew.objects.filter(shop_sec = shop_sec).values('batch_no').distinct())
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
        doc_no = list(M5DOCnew.objects.filter(batch_no =wo_no,brn_no=br_no,shop_sec=shop_sec,part_no=part_no).values('m2slno').exclude(m2slno__isnull=True).distinct())
        return JsonResponse(doc_no, safe = False)
    return JsonResponse({"success":False}, status=400)


def m5getstaff_no(request):
    if request.method == "GET" and request.is_ajax():
        # staff_no = request.GET.get('wo_no')
        shop_sec = request.GET.get('shop_sec')
        br_no = list(M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').exclude(staff_no__isnull=True).distinct())
        return JsonResponse(br_no, safe = False)
    return JsonResponse({"success":False}, status=400)




@login_required
@role_required(allowed_roles=["Superuser","2301","2302"])
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
    obj2=MachiningAirBox.objects.all().order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    my_context={
       'object':obj2,
       'nav':nav,
        'usermaster':usermaster,
        'ip':get_client_ip(request),
        'mybo':mybo,
        'subnav':subnav,
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
                MachiningAirBox.objects.filter(sno=sno).update(dispatch_to=dislocos)
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

@login_required
@role_required(allowed_roles=["Superuser","2301","2302"])
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
    obj2=MiscellSection.objects.all().order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    my_context={
       'object':obj2,
       'nav':nav,
        'usermaster':usermaster,
        'ip':get_client_ip(request),
        'mybo':mybo,
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
               MiscellSection.objects.filter(sno=first).update(dispatch_to=second)
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


@login_required
@role_required(allowed_roles=["Superuser","2301","2302"])
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
    obj2=AxleWheelMachining.objects.all().order_by('sno')
    mybo=Batch.objects.all().values('bo_no')
    mysno=AxleWheelMachining.objects.all().values('sno')
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
            fourth=request.POST.get('wheel_no')
            fifth=request.POST.get('wheel_make')
            sixth=request.POST.get('locos')
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
                obj.locos=sixth
                obj.wheel_heatcaseno=seventh
                obj.axle_no=eighth
                obj.axle_make=ninth
                obj.axle_heatcaseno=tenth
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
            wheel_no=request.POST.get('editwheel_no')
            wheel_make=request.POST.get('editwheel_make')
            loco_type=request.POST.get('editlocos')
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
                AxleWheelMachining.objects.filter(sno=sno).update(dispatch_to=dislocos)
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
            ohub_lengthwhl=request.POST.get('hub_lengthwhl')
            otread_diawhl=request.POST.get('tread_diawhl')
            orim_thicknesswhl=request.POST.get('rim_thicknesswhl')
            obore_diawhl=request.POST.get('bore_diawhl')
            oinspector_namewhl=request.POST.get('inspector_namewhl')
            odatewhl=request.POST.get('datewhl')
            if oustwhl and ohub_lengthwhl and otread_diawhl and orim_thicknesswhl and obore_diawhl and oinspector_namewhl and odatewhl:
                AxleWheelMachining.objects.filter(sno=sno).update(ustwhl=oustwhl,hub_lengthwhl=ohub_lengthwhl,tread_diawhl=otread_diawhl,rim_thicknesswhl=orim_thicknesswhl,bore_diawhl=obore_diawhl,inspector_nameaxle=oinspector_namewhl,datewhl=odatewhl)
                messages.success(request, 'Wheel Successfully Inspected!')
            else:
                messages.error(request,"Please Select S.No.!")

        if submit=='InspectAxle':
            
            sno=int(request.POST.get('snoaxle'))
            ustaxle=request.POST.get('ustaxle')
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
            if ustaxle and axlelength and journalaxle and throweraxle and wheelseataxle and gearseataxle and collaraxle and dateaxle and bearingaxle and abutmentaxle and inspector_nameaxle and journal_surfacefinishGE and wheelseat_surfacefinishGE and gearseat_surfacefinishGE and journal_surfacefinishFE and wheelseat_surfacefinishFE and gearseat_surfacefinishFE:
                AxleWheelMachining.objects.filter(sno=sno).update(ustaxle=ustaxle,axlelength=axlelength,journalaxle=journalaxle,throweraxle=throweraxle,wheelseataxle=wheelseataxle,gearseataxle=gearseataxle,collaraxle=collaraxle,dateaxle=dateaxle,bearingaxle=bearingaxle,abutmentaxle=abutmentaxle,inspector_nameaxle=inspector_nameaxle,journal_surfacefinishGE=journal_surfacefinishGE,wheelseat_surfacefinishGE=wheelseat_surfacefinishGE,gearseat_surfacefinishGE=gearseat_surfacefinishGE,journal_surfacefinishFE=journal_surfacefinishFE,wheelseat_surfacefinishFE=wheelseat_surfacefinishFE,gearseat_surfacefinishFE=gearseat_surfacefinishFE)
                messages.success(request, 'Axle Successfully Inspected!')
            else:
                messages.error(request,"Please Select S.No.!")

        
        return HttpResponseRedirect("/axlewheelmachining_section/")

    return render(request,"axlewheelmachining_section.html",my_context)

def axle_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(allowed_roles=["Superuser","2301","2302","0401","0402","0403"])
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
@role_required(allowed_roles=["Superuser","2301","2302","0401","0402","0403"])
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
            'roles':tmp
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
            context = {
                'obj1': obj1,
                'obj2': obj2,
                'ran':range(1,32),
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
@role_required(allowed_roles=["Superuser","2301","2302"])
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
                PinionPressing.objects.filter(sno=sno).update(pinion_no=pinion_no,pinion_make=pinion_make,pinion_travel=pinion_travel,pinion_pressure=pinion_pressure,blue_match=blue_match) 
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


@login_required
@role_required(allowed_roles=["Superuser","2301","2302"])
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
    my_context={
       'object':obj2,
       'nav':nav,
       'subnav':subnav,
       'usermaster':usermaster,
       'ip':get_client_ip(request),
       'mybo':mybo
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
               obj.bullgear_no=bullg_no
               obj.bullgear_make=bullg_make
               obj.save()
               messages.success(request, 'Successfully Added!')
            else:
                messages.error(request,"Please Enter All Records!")

            obj2=AxleWheelPressing.objects.all().order_by('sno')
            my_context={
            'object':obj2,
            }

        if submit=='save':
    
            sno=int(request.POST.get('editsno'))
            bo_no=request.POST.get('editbo_no')
            bo_date=request.POST.get('editbo_date')
            date=request.POST.get('editdate')
            loco_type=request.POST.get('editlocos')
            axle_no=request.POST.get('editaxle_no')
            wheelno_de=request.POST.get('editwheelno_nde')
            in_qty=request.POST.get('editin_qty')
            out_qty=request.POST.get('editout_qty')
            if bo_no and bo_date and date and loco_type and airbox_sno and airbox_make and in_qty and out_qty:
               AxleWheelPressing.objects.filter(sno=sno).update(bo_no=bo_no,bo_date=bo_date,date=date,loco_type=loco_type,airbox_sno=airbox_sno,airbox_make=airbox_make,in_qty=in_qty,out_qty=out_qty)
               messages.success(request, 'Successfully Edited!')
            else:
               messages.error(request,"Please Enter S.No.!")

        if submit=="Dispatch":
            
            sno=int(request.POST.get('dissno'))
            dislocos=request.POST.get('dislocos')
            if sno and dislocos:
                MachiningAirBox.objects.filter(sno=sno).update(dispatch_to=dislocos)
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
        
        return HttpResponseRedirect("/axlewheelpressing_section/")

    return render(request,"axlewheelpressing_section.html",my_context)

def axlepress_addbo(request):
    if request.method=="GET" and request.is_ajax():
        mybo = request.GET.get('selbo_no')
        myval = list(Batch.objects.filter(bo_no=mybo).values('ep_type','rel_date'))
        return JsonResponse(myval, safe = False)
    return JsonResponse({"success":False}, status=400)


@login_required
@role_required(allowed_roles=["Superuser","2301","2302","0401","0402","0403"])
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
        if submitvalue=='Add':
            rolelist=usermaster.role.split(", ")
            wo_nop = empmast.objects.none()
            shop_sec = request.POST.get('shop_sec')
            staffno=request.POST.get('staff_no')
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
                    'roles':tmp
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
                    'roles' :rolelist
                }
            elif(len(rolelist)>1):
                context = {
                    'sub':1,
                    'lenm' :len(rolelist),
                    'nav':nav,
                    'subnav':subnav,
                    'ip':get_client_ip(request),
                    'usermaster':usermaster,
                    'roles' :rolelist
                }
    return render(request,'M20view.html',context)


def m20getstaffno(request):
    if request.method == "GET" and request.is_ajax():
        from.models import Batch
        shop_sec = request.GET.get('shop_sec')
        w1=M5SHEMP.objects.filter(shopsec=shop_sec).values('staff_no').distinct()
        wono = list(w1)
        print("ths is",shop_sec)
        return JsonResponse(wono, safe = False)
    return JsonResponse({"success":False}, status=400)



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
    context={
        'nav':nav,
        'subnav':subnav,
        'usermaster':usermaster,
        'ip':get_client_ip(request),
    }
    return render(request,'m18view.html',context)  
	
	
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
    return render(request,'m26view.html',context)  
	