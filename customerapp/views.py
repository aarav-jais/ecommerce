from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#for logout
from django.contrib.auth import logout

import razorpay
# Create your views here.
from django.conf import settings
C_URL = settings.CURL
from demoproject.models import Customer,ProductDetail,ProductImage,AddToCart,Order

media_url=settings.MEDIA_URL

def sessioncheckcustomer_middleware(get_response):
    def middleware(request):
        print("============= request=====:",request.path)
        strpath = request.path
        list1 = strpath.split("/")
        if len(list1)>2:
            print("if wala part chala")
            strnewpath = "/"+list1[1]+"/"+list1[2]+"/"
            print("===========",strnewpath)
            if strnewpath=='/customerapp//' or strnewpath=='/customerapp/cart/' or strnewpath=='/customerapp/editprofile/' or strnewpath == '/customerapp/changepassword/' :
                if 'emailid' not in request.session:   
                    print("EmailID aaya kya")         
                    response=redirect('http://localhost:8000/login')
                else:
                    response=get_response(request)
            else:
                response=get_response(request)
        else:
            print("else wala part chala")
            return get_response(request)        
        return response   
    return middleware 

#Remove the authenticated user's ID from the request and flush their session data.
def Logout(request):
    print("calling logout=============")
    logout(request)
    return redirect('http://localhost:8000/login/')

def home(request):
    if request.method == "GET":
        prod_details=ProductDetail.objects.all().values()
        print(prod_details)
        prod_img = ProductImage.objects.all().values("product_img","product_id")
        print(prod_img)

        prod_images=[] 
        for dic in prod_details:
            for imgdic in prod_img:
                if dic["product_id"] == imgdic["product_id"]:
                    print(imgdic["product_img"],imgdic["product_id"]) 
                    prod_images.append(imgdic)
                    break
        
        print(prod_images)  
        return render(request,'CustomerHome.html',{'curl':C_URL,'prod_details':prod_details,'prod_images':prod_images,'media_url':media_url})
    if request.method == "POST":
        result = request.POST.get('search')
        print("Search data:",result)
        prod_details=ProductDetail.objects.filter(product_brand=result).values()
        print(prod_details)
        prod_img = ProductImage.objects.all().values("product_img","product_id")
        prod_images=[] 
        for dic in prod_details:
            for imgdic in prod_img:
                if dic["product_id"] == imgdic["product_id"]:
                    print(imgdic["product_img"],imgdic["product_id"]) 
                    prod_images.append(imgdic)
                    break
        return render(request,'CustomerHome.html',{'curl':C_URL,'prod_details':prod_details,'prod_images':prod_images,'media_url':media_url})
    

def cart(request):
    if request.method == "GET":
        #==============session
        customer_id=request.session.get("customer_id")
        #==============session  
        cust_id=Customer.objects.filter(customer_id=customer_id)
        print(cust_id[0].customer_id)
        addtocart=AddToCart.objects.filter(customer_id=cust_id[0].customer_id).values()
        print("Add to Cart:===========>",addtocart)
        sum=0
        for dic in addtocart:
            print(dic["product_total_price"])
            sum+=dic["product_total_price"]

        return render(request,'Cart.html',{'curl':C_URL,'addtocart':addtocart,'sum':sum,'media_url':media_url})

def delete(request):
    product_id = request.GET.get("id")
    print("Product ID:==>",product_id)
    AddToCart.objects.filter(product_id=product_id).delete()
    return redirect(C_URL+'customerapp/cart/') 

def customerdetails(request):
    # ==============session
    emailid=request.session.get("emailid")
    password=request.session.get("password")
    # ==============session 
    
    cust=Customer.objects.filter(email=emailid,password=password).values()
    print(cust)
    fullname=cust[0]["name"]
    list=fullname.split(" ")
    firstname=list[0]
    lastname=list[1]
    #===========session
    customer_id=request.session.get("customer_id")
    #============
    cartdetails=AddToCart.objects.filter(customer_id=customer_id).values("product_total_price")

    print(cartdetails)

    return render(request,'CustomerDetails.html',{'curl':C_URL,"customer":cust[0],"firstname":firstname,"lastname":lastname,"total_price":cartdetails[0]["product_total_price"]})

@csrf_exempt
def payment(request):
    #==============session
    emailid=request.session.get("emailid")
    password=request.session.get("password")
    customer_id=request.session.get("customer_id")
    #==============session  
    listofdic=Customer.objects.filter(email=emailid,password=password).values()
    print(listofdic[0])

    # authorize razorpay client with API Keys.
    client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    
    data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" ,"payment_capture":'0'}
    payment = client.order.create(data=data)
    print("============== Payment:",payment)

    price=request.GET.get('price')
    
    # Create a Razorpay Order
    razorpay_order = client.order.create(data=data)
    print(razorpay_order)
 
    #return render(request, 'index.html', context=context)
    return render(request,'Payment.html',{'price':price,'customer':listofdic[0],'curl':C_URL,"customer_id":customer_id})

@csrf_exempt
def paymentstatus(request):
    
    if request.method=="POST":
    #   #==============session
      customer_id=request.GET.get('id')
      print("customer_id aagai kya?",customer_id)
    #   #==============session  
      addtocart = AddToCart.objects.filter(customer_id=customer_id).values()
      print("===========addtocart:",addtocart)
      print(addtocart[0]["product_brand"])
      product_brand=addtocart[0]["product_brand"]
      product_price=addtocart[0]["product_price"]
      product_size=addtocart[0]["product_size"]
      product_description=addtocart[0]["product_description"]
      product_quantity=addtocart[0]["product_quantity"]
      product_img=addtocart[0]["product_img_name"]
      product_id=addtocart[0]["product_id"]
      customer_id=addtocart[0]["customer_id"]
      product_img_id=addtocart[0]["product_img_id"]
      print(product_brand,product_price,product_size,product_description,product_quantity,product_img,product_id,customer_id,product_img_id)

      #============
    #   cust_details = Customer.objects.get(customer_id=customer_id)
    #   prod_details = ProductDetail.objects.get(product_id=product_id)
    #   prod_img_details = ProductImage.objects.get(product_img_id=product_img_id)
    #   #===============

      #===Order
      
      order = Order(product_brand=product_brand,product_price=product_price,product_size=product_size,product_description=product_description,product_quantity=product_quantity,product_image=product_img,customer_id=customer_id,product_id=product_id,product_img_id=product_img_id)
      order.save()

      addtocart = AddToCart.objects.filter(customer_id=customer_id)
      addtocart.delete()
      
    
    return render(request,'PaymentSuccess.html',{'curl':C_URL})

def changepassword(request):
    if request.method == "GET":
        return render(request,'CustomerChangePassword.html',{"curl":C_URL})
    
    elif request.method == "POST":
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')
        print(oldpassword,newpassword,confirmpassword)
        # #==============session
        emailid=request.session.get("emailid")
        # #==============session  
        customer = Customer.objects.filter(email=emailid,password=oldpassword)
        print(customer)
        msg=""
        if customer.exists():
            print("==========Hiii")
            if newpassword==confirmpassword:
              Customer.objects.filter(email=emailid,password=oldpassword).update(password=confirmpassword)
              msg="Customer Password Changed Successfully"  
            else:
              msg="New Password & Confirm Password are mismatch"
        else:
            print("============Hello")
            msg="Please enter correct old password!!"             
                
    return render(request,'CustomerChangePassword.html',{'curl':C_URL,'msg':msg})

def editprofile(request):
    if request.method == "GET":
        #==============session
        emailid=request.session.get("emailid")
        password=request.session.get("password")
        #==============session  
        cust=Customer.objects.filter(email=emailid,password=password).values()
        print(cust[0])
        return render(request,'CustomerEditProfile.html',{'curl':C_URL,'record':cust[0]})
    
    elif request.method == "POST":
        customer_id = request.POST.get('customer_id')
        name = request.POST.get('name')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        print(customer_id,name,mobile,address,city,pincode)
        Customer.objects.filter(customer_id=customer_id).update(name=name,city=city,pincode=pincode,address=address,mobile=mobile)
        msg="Record Updated Successfully"
        return render(request,'Message.html',{'curl':C_URL,'msg':msg})


