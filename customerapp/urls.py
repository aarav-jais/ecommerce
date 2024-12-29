from django.urls import path
from . import views
urlpatterns = [
path('', views.home),
path('cart/',views.cart),
path('cart/delete',views.delete),
path('customerdetails/',views.customerdetails),
path('payment/',views.payment),
path('paymentstatus/',views.paymentstatus),
path('changepassword/',views.changepassword),
path('editprofile/',views.editprofile),
path('logout/',views.Logout),
]