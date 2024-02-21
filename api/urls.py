from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('Supervisor/home',views.SuperVisorHome,name="supervisor_home"),

    path('Employee/home',views.EmployeeHome,name="employee_home"),


    path('Getkeeper/home',views.GetKeeperHome,name="getkeeper_home"),

    path('base',views.base, name="base"),
    path('createAccount',views.createAccount, name="create_account"),
    path('',views.Login, name="login_form"),
    path('doLogin',views.doLogin, name="do_login"),
    path('doLogout',views.doLogout, name="do_logout"),
    path('GuestRequestForm',views.GuestRequestForm, name="guest_request"),
    #employee form
    path('get_responsible_persons/',views.Get_responsible_persons,name='get_responsible_persons'),
    path('ViewGuestRequest',views.ViewGuestRequest, name="view_guest_request"),
    path('ManageRequest/<str:id>',views.ManageRequest, name="manage_guest_request"),
    path('Invitation/',views.Invites, name="invitation"),
     path('Deligation/',views.Deligation, name="deligate"),

    #Supervisor urls
    path('ViewInvitation',views.ViewInvitation, name="view_invitation"),
    path('ManageInvitation/<str:id>',views.ManageInvitation, name="manage_invitation"),
    
    
    #Getkeeper urls
    path('CheckBadge',views.CheckBadge, name="check_badge"),
    path('BadgeDiteil/<str:id>',views.BadgeDiteil, name="badge_deteil"),
    path('BadgeDiteil2/<str:id>',views.BadgeDiteil2, name="badge_deteil2"),
    
]
