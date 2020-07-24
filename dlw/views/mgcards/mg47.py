from dlw.views import *
import dlw.views.globals as g
@login_required
@role_required(urlpass='/mg47view/')
def mg47view(request):
    cuser=request.user
    usermaster=empmast.objects.filter(empno=cuser).first()
    wo_nop = empmast.objects.none()
    shopno = list(empmast.objects.filter(empno=cuser).values('shopno').distinct())  
    tmp2=''
    for on in shopno:
        tmp2=on['shopno']
    shop =list(shop_section.objects.filter(shop_id=tmp2).values('shop_code').distinct()) 
    tm = ''
    for on in shop:
        tm= on['shop_code']
    tm1=tm[:-2]
    cursor=connection.cursor()
    cursor.execute('''select "Sr.No."::int from "MG47_table1" order by "Sr.No."::int desc''')
    form=cursor.fetchall()
    
    if(len(form)==0):
        formid=1
    else:
        formid=form[0][0]
        formid=int(formid)+1

    
    context={
            'sub':0,
            'lenm' :2,
            'nav':g.nav,
            'ip':get_client_ip(request),
            'subnav':g.subnav,        
            'sno' : formid,
            'shopno' : tm1,
        }   
    return render(request,'MGCARD/MG47CARD/mg47view.html',context)
def mg47SaveDetails(request):
    if request.method == "GET" and request.is_ajax():
            shop = request.GET.get('shop')
            num = request.GET.get('num')
            to_sse= request.GET.get('to_sse')
            date = request.GET.get('date')
            allocable_to = request.GET.get('allocable_to')
            issued_on = request.GET.get('issued_on')
            empno = request.GET.get('empno')
            from_sse = request.GET.get('from_sse')
            empname = request.GET.get('empname')
            hidtext=request.GET.get('hidtext')
            arr=request.GET.get('arr')
            arr=arr.split(",")
            l=[]
            obj =MG47_table1.objects.filter(num=num).distinct()
            b=num
            if len(obj) == 0:
                try:
                   b=MG47_table1.objects.create(shop=str(shop), num=str(num), to_sse=str(to_sse), date=str(date), allocable_to=str(allocable_to), issued_on=str(issued_on), empno=str(empno), from_sse=str(from_sse), empname=str(empname))
                except:
                    print("Insertion not Successful : MG47_table1")
            else:
                try:
                    MG47_table1.objects.filter(num=num).update(shop=str(shop), num=str(num), to_sse=str(to_sse), date=str(date), allocable_to=str(allocable_to), issued_on=str(issued_on), empno=str(empno), from_sse=str(from_sse), empname=str(empname))  
                except:
                    print("Updation not Successful : MG47_table1")
            obj1 =list(MG47_table2.objects.values('id').filter(num=num).distinct())
            a=1
            if len(obj1) == 0:
                try:    
                    for i in range(1,int(hidtext)+1):
                        c=MG47_table2.objects.create(num=b,desc=str(arr[a]), demand=str(arr[a+1]), issued=str(arr[a+2]))
                        a=a+3
                except:
                    print("Insertion not Successful : MG47_table2")
            else:
                try:
                    for i in range(1,int(hidtext)+1):
                        MG47_table2.objects.filter(id=obj1[i-1]['id']).update(num=b, desc=str(arr[a]), demand=str(arr[a+1]), issued=str(arr[a+2]))   
                        a=a+3
                except:
                    print("Updation not Successful : MG47_table2")
            return JsonResponse(l,safe = False)
    return JsonResponse({"success":False}, status=400)
def mg47getfrom_sse(request):
    if request.method == "GET" and request.is_ajax():          
        empno = request.GET.get('empno')
        obj1=list(emp_details.objects.filter(empno= empno).values('desgn','shop_code','empname').distinct()) 
        lst=[]
        for i in range(len(obj1)):
            for j in range(len(obj1)):
                lst.append(obj1[i]['desgn']+'/'+obj1[j]['shop_code']) 
        lst.append(obj1) 
        return JsonResponse(lst,safe = False)
    return JsonResponse({"success":False}, status=400)
def mg47reportview(request, *args, **kwargs):
    to_sse = request.GET.get('to_sse')
    num = request.GET.get('num')
    date = request.GET.get('date')
    allocable_to = request.GET.get('allocable_to')
    issued_on = request.GET.get('issued_on')
    from_sse = request.GET.get('from_sse')
    arr=request.GET.get('arr')
    arr=arr.split(",")
    lst=[]
    i=1
    a=1
    while(i<len(arr)):
        lst.append({'sl':a,'des':arr[i],'dem':arr[i+1],'iss':arr[i+2]})
        a=a+1
        i=i+3
    context = {
        'to_sse':to_sse,
        'num':num,
        'date':date,
        'allocable_to':allocable_to,
        'issued_on':issued_on,
        'from_sse':from_sse,
        'arr':lst,
        }
    pdf = render_to_pdf('MGCARD/MG47CARD/mg47reportview.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def ExistingNumDetails(request):
    l=[]
    if request.method=="GET" and request.is_ajax():
        num=request.GET.get('num')
        obj=list(MG47_table1.objects.filter(num=num).values('shop','to_sse','date','allocable_to','issued_on','empno','from_sse','empname').distinct())
        obj1=list(MG47_table2.objects.filter(num=num).values('desc','demand','issued').distinct())
        l.append(obj)
        l.append(obj1)
        return JsonResponse(l,safe=False)
    return JsonResponse({"success":False}, status=400)
    
def mg47to_SseDetails(request):
    if request.method=="GET" and request.is_ajax():
        obj1=list(emp_details.objects.values('desgn','shop_code').distinct())
        print(obj1) 
        lst=[]
        for i in range(len(obj1)):
            for j in range(len(obj1)):
                lst.append(str(obj1[i]['desgn'])+'/'+str(obj1[j]['shop_code'])) 
        return JsonResponse(lst,safe=False)
    return JsonResponse({"success":False}, status=400)

def mg47DescDetails(request):
    if request.method=="GET" and request.is_ajax():
        obj1=list(MG47_table2.objects.values('desc').distinct())  
        return JsonResponse(obj1,safe=False)
    return JsonResponse({"success":False}, status=400)

def mg47EmpnoDetails(request):
    if request.method=="GET" and request.is_ajax():
        obj=list(emp_details.objects.values('empno').distinct())  
        return JsonResponse(obj,safe=False)
    return JsonResponse({"success":False}, status=400)
