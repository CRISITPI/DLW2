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
from django.contrib.auth import views as auth_views
from dlw.views import m14getwono,m14getdoc_no,m14getpart_no,m14getassly,m14getbr,m14view,m4getwono,m4getdoc_no,m4getpart_no,m4getassly,m4getbr,m4view,m2getwono,m2getdoc_no,m2getpart_no,m2getassly,m2getbr,m2view,insert_machining_of_air_box,shiftsave,test,getshopempinfo,update_emp_shift_admin,update_emp_shift,update_permission_incharge,update_permission,getPermissionInfo,login_request,logout_request,homeadmin,create,homeuser,ChartData,dynamicnavbar,getEmpInfo,delete_user,forget_password,forget_path,getauthempInfo,checkloco,jpo,getYrDgp,bprodplan
from dlw.views import dpo,dpoinput,checktotal,m1getpano,m1view,m5getwono,m5getdoc_no,m5getpart_no,m5getbr,m5view,m5getstaff_no,airbox_addbo,getcumino
from dlw.views import m1genrept1,miscellaneous_section,miscell_addbo,axle_addbo,axlewheelmachining_section,m3sub,m3getdoc_no,m3getpart_no,m3getassly,m3shopsec,m3getbr,m3view,m3getwono
from dlw.views import m7getwono,m7view,m7getempno,m7getpart_no,pinion_editsno,pinionpressing_section,pinion_addbo,airbox_editsno,axlepress_addbo,axlewheelpressing_section,M20view,m20getstaffno,m18view,m26view,m27view


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
    path('m4view/', m4view, name='m4view'),
    path('ajax/m4getbr/',m4getbr,name='m4getbr'),
    path('ajax/m4getassly/',m4getassly,name='m4getassly'),
    path('ajax/m4getpart_no/',m4getpart_no,name='m4getpart_no'),
    path('ajax/m4getdoc_no/',m4getdoc_no,name='m4getdoc_no'),
    path('ajax/m4getwono',m4getwono,name='m4getwono'),
    path('m14view/', m14view, name='m14view'),
    path('ajax/m14getbr/',m14getbr,name='m14getbr'),
    path('ajax/m14getassly/',m14getassly,name='m14getassly'),
    path('ajax/m14getpart_no/',m14getpart_no,name='m14getpart_no'),
    path('ajax/m14getdoc_no/',m14getdoc_no,name='m14getdoc_no'),
    path('ajax/m14getwono',m14getwono,name='m14getwono'),
    path('ajax/get_yr_dgp/',getYrDgp,name='get_yr_dgp'),
    path('ajax/check_loco/',checkloco,name='check_loco'),
    path('ajax/check_total/',checktotal,name='check_total'),
    path('aprodplan/',bprodplan,name='aprodplan'),
    path('miscellaneous_section/',miscellaneous_section,name='miscellaneous_section'),
    path('jpo/',jpo,name='jpo'),
    path('machining_of_air_box/',insert_machining_of_air_box,name='machining_of_air_box'),
    path('dpoinput/',dpoinput,name='dpoinput'),
    path('dpo/',dpo,name='dpo'),
    path('ajax/getcumino/',getcumino,name='getcumino'),
    path('m1view/',m1view,name='m1view'),
    path('ajax/m1getpano/',m1getpano,name='m1getpano'),
    path('m5view/',m5view,name='m5view'),
    path('m3view/',m3view,name='m3view'),
    path('ajax/m5getbr/',m5getbr,name='m5getbr'),
    path('ajax/submitprod/',bprodplan,name="submitprod"),
    path('ajax/m5getpart_no/',m5getpart_no,name='m5getpart_no'),
    path('ajax/m5getdoc_no/',m5getdoc_no,name='m5getdoc_no'),
    path('ajax/m5getwono',m5getwono,name='m5getwono'),
    path('ajax/airbox_addbo',airbox_addbo,name='airbox_addbo'),
    path('ajax/miscell_addbo',miscell_addbo,name='miscell_addbo'),
    path('ajax/axle_addbo',axle_addbo,name='axle_addbo'),
    path('m1genrept1/',m1genrept1,name='m1genrept1'),
    path('axlewheelmachining_section/',axlewheelmachining_section,name='axlewheelmachining_section'),
    path('ajax/m3getbr/', m3getbr, name='m3getbr'),
    path('ajax/m3shopsec/', m3shopsec, name='m3shopsec'),
    path('ajax/m3getassly/', m3getassly, name='m3getassly'),
    path('ajax/m3getpart_no/', m3getpart_no, name='m3getpart_no'),
    path('ajax/m3getdoc_no/', m3getdoc_no, name='m3getdoc_no'),
    path('ajax/m3getwono/', m3getwono, name='m3getwono'),
    path('m3sub/', m3sub, name='m3sub'),
    path('ajax/m5getstaff_no/',m5getstaff_no,name='m5getstaff_no'),
    path('m7view/', m7view, name='m7view'),
    path('ajax/m7getwono/', m7getwono, name='m7getwono'),
    path('ajax/m7getempno/', m7getempno, name='m7getempno'),
    path('ajax/m7getpart_no/', m7getpart_no, name='m7getpart_no'),
    path('ajax/airbox_editsno',airbox_editsno,name='airbox_editsno'),
    path('ajax/pinion_addbo',pinion_addbo,name='pinion_addbo'),
    path('PinionPress/',pinionpressing_section,name='PinionPress'),
    path('ajax/pinion_editsno',pinion_editsno,name='pinion_editsno'),
    path('ajax/axlepress_addbo',axlepress_addbo,name='axlepress_addbo'),
    path('axlewheelpressing_section/',axlewheelpressing_section,name='axlewheelpressing_section'),
    path('M20view/',M20view,name='M20view'),
    path('m20getstaffno/',m20getstaffno,name='m20getstaffno'),
    path('m18view/', m18view, name='m18view'),
    path('m26view/', m26view, name='m26view'),
    path('m27view/', m27view, name='m27view'),

]
