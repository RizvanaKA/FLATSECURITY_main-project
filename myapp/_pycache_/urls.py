"""
URL configuration for FlatSecurity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from . import views
urlpatterns = [

    path('login/', views.main),
    path('logout/', views.logout),
    path('login_get/', views.login_get),
    path('home/', views.home),
    path('add_camera_POST/', views.add_camera_POST),
    path('view_camera/', views.view_camera),
    path('delete_camera/<id>', views.delete_camera),
    path('add_notification/', views.add_notification),
    path('add_staff/', views.add_staff),
    path('edit_staff/<id>', views.edit_staff),
    path('view_complaint/', views.view_complaint),
    path('view_notification/', views.view_notification),
    path('view_staff/', views.view_staff),
    path('view_visitor/', views.view_visitor),
    path('edit_notification/<id>', views.edit_notification),
    path('send_replay/<id>', views.send_replay),
    path('add_notification_POST/', views.add_notification_POST),
    path('add_staff_POST/', views.add_staff_POST),
    path('edit_notification_POST/', views.edit_notification_POST),
    path('send_replay_POST/', views.send_replay_POST),
    path('edit_staff_POST/',views.edit_staff_POST),
    path('delete_staff/<id>',views.delete_staff),
    path('delete_notification/<id>',views.delete_notification),
    path('loginpost',views.loginpost),
    path('user_registration',views.user_registration),
    path('send_complaint',views.send_complaint),
    path('user_view_reply',views.user_view_reply),
    path('user_add_visitor_schedule',views.user_add_visitor_schedule),
    path('user_View_visitor_schedule',views.user_View_visitor_schedule),
    path('user_delete_visitor_schedule',views.user_delete_visitor_schedule),
    path('user_view_notification',views.user_view_notification),
    path('User_viewchat',views.User_viewchat),
    path('user_add_emergency_notification',views.user_add_emergency_notification),
    path('user_view_emergency_notification',views.user_view_emergency_notification),
    path('user_delete_emergency_notification',views.user_delete_emergency_notification),
    path('user_view_notification_other',views.user_view_notification_other),
    path('security_scan_validate_QR_entry_exit',views.security_scan_validate_QR_entry_exit),
    path('security_view_notification',views.security_view_notification),
    path('security_respond_emergency_alert',views.security_respond_emergency_alert),
    path('security_unknown_person',views.security_unknown_person),
    path('user_view_profile',views.user_view_profile),
    path('edit_profile/',views.edit_profile),
    path('user_view_notification/',views.user_view_notification),
    path('User_sendchat',views.User_sendchat),
    path('user_view_security',views.user_view_security),
    path("ragging-alert/", views.ragging_alert_api),
    path("forgot/", views.forgot),
    path("forgotPassword_otp/", views.forgotPassword_otp),
    path("verifyOtp/", views.verifyOtp),
    path("verifyOtpPost/", views.verifyOtpPost),
    path("new_password/", views.new_password),
    path("changePassword/", views.changePassword),
    path("forgotpasswordflutter/", views.forgotpasswordflutter),
    path("verifyOtpflutterPost/", views.verifyOtpflutterPost),
    path("changePasswordflutter/", views.changePasswordflutter),


    path("security_view_violence_detection/", views.security_view_violence_detection),

     path('security_scan_validate_QR',        views.security_scan_validate_QR,        name='security_scan_validate_QR'),
    path('security_view_today_visitors',     views.security_view_today_visitors,     name='security_view_today_visitors'),
    path('security_view_emergency',          views.security_view_emergency,          name='security_view_emergency'),
    path('security_view_profile',            views.security_view_profile,            name='security_view_profile'),
    path('user_edit_profile',            views.edit_profile,            name='edit_profile'),
    path('security_view_all_visitors',       views.security_view_all_visitors,       name='security_view_all_visitors'),
    path('security_view_dangerous_person',       views.security_view_dangerous_person,       name='security_view_dangerous_person'),
    path('add_dangerous_person',       views.add_dangerous_person,       name='add_dangerous_person'),
    path('delete_dangerous_person',       views.delete_dangerous_person,       name='delete_dangerous_person'),
    path('security_user_user',       views.security_user_user,       name='security_user_user'),
    path('detect_noti/',       views.detect_noti,       name='detect_noti'),
    path('check_stranger_api/',       views.check_stranger_api,       name='detect_dangerous'),
    path('security_view_camera_notification',       views.security_view_camera_notification,       name='security_view_camera_notification'),
    path('user_view_dangerous_person',       views.user_view_dangerous_person,       name='user_view_dangerous_person'),

    path('get_notifications_dangerous',       views.get_notifications_dangerous,       name='get_notifications_dangerous'),
    path('get_notifications_violence',       views.get_notifications_violence,       name='get_notifications_violence'),
    path('get_notifications_emergency',       views.get_notifications_emergency,       name='get_notifications_emergency'),


]
