from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from dlw.models import empmast,empmast




# def roleslist(request,oldstr):
#     newstr=oldstr.replace("'","")
#     length=len(newstr)
#     newstrfin=newstr[1:length-1]
#     newlength=len(newstrfin)
#     rolelist=newstrfin.split(", ")
#     return rolelist




def role_required(allowed_roles=[]):
    def decorator(func):
        def wrap(request,*args,**kwargs):
            cuser=request.user
            usermaster=empmast.objects.get(empno=cuser)
            rolelist=usermaster.role.split(", ")
            if(all (x in allowed_roles for x in rolelist)):
                return func(request,*args,**kwargs)
            else:
                raise PermissionDenied
        return wrap
    return decorator



