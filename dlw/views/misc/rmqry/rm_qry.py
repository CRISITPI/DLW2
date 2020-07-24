from dlw.views import *
import dlw.views.globals as g

@login_required
@role_required(urlpass='/rmqry/')
def rmqry(request):  
    return render(request,"MISC/RMQUERY/rmqry.html")  

def rm_part_no_checkpartno(request): 
    if request.method == "GET" and request.is_ajax():
        part_no = request.GET.get('rm_part_no')     
        
        rm_part_no=list(Part.objects.filter(partno= part_no).values('des').distinct())
        rm_nstr=list(Nstr.objects.filter(ptc ='R').values('cp_part').distinct() | Nstr.objects.filter(ptc ='Q').values('cp_part').distinct()) 
      
        flag=0
        if(len(rm_part_no)==0):
            rm_part_no.insert(0,'N')
            
        else:
            rm_part_no.insert(0,'P')
            
        if(len(rm_nstr)==0):
            rm_nstr.insert(0,'X')
        else:
            rm_nstr.insert(0, 'W')
        rm_part_no.insert(2, rm_nstr)
        
        return JsonResponse(rm_part_no, safe = False)
    return JsonResponse({"success":False}, status=400)

def rmqry_proceed(request):  
    if request.method == "GET" and request.is_ajax():
        part_no =request.GET.get('proceed')    
        proceed=list(Part.objects.filter(partno=part_no).values('shop_ut').distinct())
        name=proceed[0]
        val=name.get('shop_ut')       
        proceed1=list(Code.objects.filter(code=val).values('alpha_1').distinct() & Code.objects.filter(cd_type='51').values('alpha_1').distinct())
        return JsonResponse(proceed,safe = False)
    return JsonResponse({"success":False}, status=400)


 
def rmqry_rpt(request):
            part_no = request.GET.get('rm_part_no')
            des= request.GET.get('des')   
            epcc=request.GET.get('epc')


            tem_list=[]
            tem_list_des=[]
            tem_list_drgno=[]
            tem_list_shop_ut=[]
            pp_part_from_t_table=[]
            qty_from_t_table=[]
            e_tem_list=[]
            e_tem_list_des=[]
            e_tem_list_drgno=[]
            e_tem_list_shop_ut=[]
            e_pp_part_from_t_table=[]
            e_qty_from_t_table=[]
            unit_list=[]
            
            ls=[]
            
            tt_tables=list(Nstr.objects.filter( ~Q(del_fl ='Y'),cp_part=part_no, l_to='9999').values('pp_part','epc','qty' ).order_by('epc','pp_part').distinct())
            for i in range(len(tt_tables)):
                val1=tt_tables[i].get('pp_part')
                val2=tt_tables[i].get('epc')
                val3=tt_tables[i].get('qty')
                t_tables.objects.create(pp_part=val1,epc=val2,qty=val3) 
            for z in range(len(tt_tables)):
                pp_part_from_t_table.append(tt_tables[z].get('pp_part'))
                
                length_pp_part_ttable=len(pp_part_from_t_table)
           
            for y in range(len(tt_tables)):
                qty_from_t_table.append(tt_tables[y].get('qty') )
                len_qty_from_t_table= len(qty_from_t_table)
            part_table = list(Part.objects.values('partno').distinct())
  
            for k in range(len(pp_part_from_t_table)):
                pp_part_val=pp_part_from_t_table[k]
                final1=list(Part.objects.filter(partno=pp_part_val).values('ptc','des','shop_ut','drgno' ))
            
            for i in range(len(final1)):
                var=final1[i]
                tem=var.get('ptc')
                tem_list.append(tem)
            len_tem_list=len(tem_list)

            for a in range(len(final1)):
                var11=final1[a]
                tem11=var11.get('des')
                tem_list_des.append(tem11)
            len_tem_list_des=len(tem_list_des)

            for s in range(len(final1)):
                var12=final1[s]
                tem12=var12.get('drgno')
                tem_list_drgno.append(tem12)
            len_tem_list_drgno=len(tem_list_drgno)

            for ss in range(len(final1)):
                var13=final1[ss]
                tem13=var13.get('shop_ut')
                tem_list_shop_ut.append(tem13)
            len_tem_list_shop_ut=len(tem_list_shop_ut)       
            for ss in range(len(final1)):
                unit=list(Code.objects.filter(code=tem_list_shop_ut[i]).values('alpha_1').distinct() & Code.objects.filter(cd_type='51').values('alpha_1').distinct())        
                for i in range(len(unit)):
                    f=unit[i].get('alpha_1')

                unit_list.append(f)
                 
            epc=list(Nstr.objects.filter( ~Q(del_fl ='Y'),cp_part=part_no,l_to='9999').values('epc').distinct())
            ct=len(epc)
            for i in range(len(epc)):
                val=epc[i].get('epc')

                ls.append(val)  
            context={
                'rm_part_no':part_no,
                'des': des,
                'epc':ls,
                'count':len_tem_list_des,
                'pp_part_from_t_table': pp_part_from_t_table,
                'length_pp_part_ttable': length_pp_part_ttable,
                'tem_list': tem_list,
                'len_tem_list': len_tem_list,
                'tem_list_des': tem_list_des,
                'len_tem_list_des': len_tem_list_des,
                'tem_list_drgno':tem_list_drgno,
                'len_tem_list_drgno': len_tem_list_drgno,
                'tem_list_shop_ut': tem_list_shop_ut,
                'len_tem_list_shop_ut' : len_tem_list_shop_ut,
                'qty_from_t_table': qty_from_t_table,
                'len_qty_from_t_table': len_qty_from_t_table,
                'unit_list':unit_list,
            } 
            return render(request,"MISC/RMQUERY/rmqry_rpt.html",context) 
