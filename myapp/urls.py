from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.rooms_list, name='rooms_list'),

    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('tenant/pay/', views.submit_payment, name='submit_payment'),
    path('tenant/maintenance/', views.submit_maintenance, name='maintenance'),
    path('tenant/payments/', views.tenant_payments, name='payments'),

    path('myadmin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('myadmin/maintenance/', views.admin_maintenance_list, name='admin_maintenance'),
    path('myadmin/payment/approve/<int:payment_id>/', views.approve_payment, name='approve_payment'),
    path('myadmin/rooms/', views.admin_rooms, name='admin_rooms'),
    path('myadmin/tenants/', views.admin_tenants, name='admin_tenants'),
    path('myadmin/announcements/', views.admin_announcements, name='admin_announcements'),
]
