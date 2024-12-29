from django.urls import path
from . import views
urlpatterns = [
path('', views.home),
path('addproduct/',views.addproduct),
path('addproductimage/',views.addproductimage),
path('managecustomer/',views.managecustomer),
path('managecustomerstatus',views.managecustomerstatus),
path('managecustomer/delete',views.deletecustomer),
path('logout/',views.Logout),

]