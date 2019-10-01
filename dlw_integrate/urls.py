"""dlw_integrate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dlw.views import m2getwono,m2getdoc_no,m2getpart_no,m2getassly,m2getbr,m2view,insert_machining_of_air_box,shiftsave,test,getshopempinfo,update_emp_shift_admin,update_emp_shift,update_permission_incharge,update_permission,getPermissionInfo,login_request,logout_request,homeadmin,create,homeuser,ChartData,dynamicnavbar,getEmpInfo,delete_user,forget_password,forget_path,getauthempInfo,checkloco,jpo,getYrDgp,bprodplan
from dlw.views import dpo,dpoinput,checktotal,m1getpano,m1view,m5getwono,m5getdoc_no,m5getpart_no,m5getbr,m5view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_request,name='loginurl'),
    path('logout/',logout_request,name='logout'),
    path('homeadmin/',homeadmin,name='homeadmin'),
    path('createuser/',create,name='create'),
    path('dynamic/',dynamicnavbar),
    path('homeuser/', homeuser, name='homeuser'),
    path('api/chart/data/',ChartData.as_view()),
    path('password_change/done/',auth_views.PasswordChangeView.as_view(template_name='password_reset_inside_complete.html'),name='password_reset_internal_complete'),
    path('password_reset_inside/',auth_views.PasswordChangeView.as_view(template_name='password_reset_inside.html'),name='password_reset_inside'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    path('', include('django.contrib.auth.urls')),
    path('ajax/get_emp_info/',getEmpInfo,name='get_emp_info'),
    path('ajax/get_permission_info/',getPermissionInfo,name='get_permission_info'),
    path('ajax/get_auth_emp_info/',getauthempInfo,name='get_auth_emp_info'),
    path('ajax/get_shopemp_info/',getshopempinfo,name='get_shopemp_info'),
    path('ajax/shiftsave/',shiftsave,name='shiftsave'),
    path('delete_user/',delete_user,name='delete_user'),
    path('forget_password/', forget_password, name='forget_password'),
    path('forget_password_path/',forget_path,name='forget_password_path'),
    path('update_permission/',update_permission,name='update_permission'),
    path('update_permission_incharge/',update_permission_incharge,name='update_permission_incharge'),
    path('update_emp_shift/',update_emp_shift,name='update_emp_shift'),
    path('update_emp_shift_admin/',update_emp_shift_admin,name='update_emp_shift_admin'),
    path('test/',test,name='test'),
    path('m2view/',m2view,name='m2view'),
    path('ajax/m2getbr/',m2getbr,name='m2getbr'),
    path('ajax/m2getassly/',m2getassly,name='m2getassly'),
    path('ajax/m2getpart_no/',m2getpart_no,name='m2getpart_no'),
    path('ajax/m2getdoc_no/',m2getdoc_no,name='m2getdoc_no'),
    path('ajax/m2getwono',m2getwono,name='m2getwono'),
    path('ajax/get_yr_dgp/',getYrDgp,name='get_yr_dgp'),
    path('ajax/check_loco/',checkloco,name='check_loco'),
    path('ajax/check_total/',checktotal,name='check_total'),
    path('aprodplan/',bprodplan,name='aprodplan'),
    path('jpo/',jpo,name='jpo'),
    path('machining_of_air_box/',insert_machining_of_air_box,name='machining_of_air_box'),
    path('dpoinput/',dpoinput,name='dpoinput'),
    path('dpo/',dpo,name='dpo'),
    path('m1view/',m1view,name='m1view'),
    path('ajax/m1getpano/',m1getpano,name='m1getpano'),
    path('m5view/',m5view,name='m5view'),
    path('ajax/m5getbr/',m5getbr,name='m5getbr'),
    path('ajax/m5getpart_no/',m5getpart_no,name='m5getpart_no'),
    path('ajax/m5getdoc_no/',m5getdoc_no,name='m5getdoc_no'),
    path('ajax/m5getwono',m5getwono,name='m5getwono'),

]
