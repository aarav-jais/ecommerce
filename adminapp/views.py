from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from demoproject.models import ProductDetail,ProductImage,Customer
from django.conf import settings
#for file uploading
from django.core.files.storage import FileSystemStorage

#for logout
from django.contrib.auth import logout

C_URL = settings.CURL
media_url=settings.MEDIA_URL

def sessioncheckadmin_middleware(get_response):
    def middleware(request):
        print("============= request=====:",request.path)
        strpath = request.path
        list1 = strpath.split("/")
        if len(list1)>2:
            strnewpath = "/"+list1[1]+"/"+list1[2]+"/"
            if strnewpath=='/adminapp//' or strnewpath=='/adminapp/managecustomer/' or strnewpath=='/adminapp/addproduct/' or strnewpath == '/adminapp/addproductimage/' or strnewpath == '/adminapp/changepassword/' or strnewpath == '/adminapp/editprofile/' :
                if 'emailid' not in request.session:            
                    response=redirect('http://localhost:8000/login')
                else:
                    response=get_response(request)
            else:
                response=get_response(request)
        else:
            return get_response(request)        
        return response
        
    return middleware 

def Logout(request):
    logout(request)
    return redirect('http://localhost:8000/login/')



def home(request):
    return render(request,'Adminhome.html',{"curl":C_URL})


def addproduct(request):
    if request.method == "GET":
        return render(request,'AddProduct.html',{'curl':C_URL})
    elif request.method == "POST":
        p_brand=request.POST.get("p_brand")
        p_price=request.POST.get("p_price")
        p_old_price=request.POST.get("p_old_price")
        p_discount=request.POST.get("p_discount")
        p_size=request.POST.get("p_size")
        p_description=request.POST.get("p_description")
        p_quantity=request.POST.get("p_quantity")
        p_availability=request.POST.get("p_availability")

        print(p_brand,p_price,p_old_price,p_discount,p_size,p_description,p_quantity,p_availability)
        msg=""
        try:
            add_prod_detail=ProductDetail(product_brand=p_brand,product_price=p_price,product_old_price=p_old_price,product_discount=p_discount,product_size=p_size,product_description=p_description,product_quantity=p_quantity,product_availability=p_availability)
            add_prod_detail.save()
            msg="Product Added Successfully!!"
        except:  
            msg="Product Not Added !!"
  
        return render(request,'AddProduct.html',{'curl':C_URL,"msg":msg})

def addproductimage(request):
    if request.method == "GET":
        qs=ProductDetail.objects.all().values("product_id","product_brand")
        print(qs)
        return render(request,'AddProductImage.html',{'curl':C_URL,"listofproduct":qs})
    
    elif request.method == "POST":
        product_id=request.POST.get("product_id")
        print(product_id)
        files = request.FILES.getlist('product_img')
        print(files,len(files))
        file_list = [] 
        msg=""
        try:  
            prod_detail = ProductDetail.objects.get(product_id=product_id)
            # print("Product Details:===>",prod_detail)
            for file in files:
                print(file)
                #for file uploading .............................
                fs=FileSystemStorage()
                fs.save(file.name,file)  
                #......................................
                new_file = ProductImage(product_img=file,product_id=prod_detail)
                new_file.save()
                file_list.append(new_file.product_img)
            msg="Product Images Uploaded Successfully"  
        except:
            msg="Product Images Not Uploaded!!"      
        
        return render(request,'AddProductImage.html',{'curl':C_URL,"msg":msg,'new_url':str(new_file.product_img),'list_img':file_list})    
        
def managecustomer(request):
    customers=Customer.objects.filter(role="customer").values()
    print(customers)
    return render(request,'ManageCustomer.html',{'curl':C_URL,'customers':customers})

def managecustomer(request):
    customers=Customer.objects.filter(role="customer").values()
    print(customers)
    return render(request,'ManageCustomer.html',{'curl':C_URL,'customers':customers})
        
def managecustomerstatus(request):
    if request.method=="GET":
        id=request.GET.get('id')
        status=request.GET.get('status')
        print(id,status)
        if status == "0":
           Customer.objects.filter(customer_id=id).update(status=1)
           
        elif status == "1":
           Customer.objects.filter(customer_id=id).update(status=0)
          
        return redirect(C_URL+'adminapp/managecustomer/')    

def deletecustomer(request):
    if request.method=="GET":
        id=request.GET.get('id')
        print("Customer Id:",id)
        Customer.objects.filter(customer_id=id).delete()
        return redirect(C_URL+'adminapp/managecustomer/') 
