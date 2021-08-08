from django.urls import path
from . import views

urlpatterns = [
    path('',views.store,name='store'),
    path('cart/',views.cart,name='cart'),
    path('main/',views.main,name='main'),
    path('checkout/',views.checkout,name='checkout'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process-order/',views.processOrder,name='process-order'),
    path('login/',views.loginpage,name='login'),
    path('register/',views.registerpage,name='register'),
    path('logout/',views.logoutpage,name='logout'),
    path('uzi/',views.apioverview,name='uzi'),
    path('task-list/',views.tasklist,name='task-list')
   
    

]
