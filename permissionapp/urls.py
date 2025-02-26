from django.urls import path 
from . import views

app_name = 'authcheck'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('h2/',views.only_for_hasin, name='only_for_hasin'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('manager-panel/', views.manager_dashboard, name='manager_dashboard'),
    path('editor-panel/', views.editor_workspace, name='editor_workspace'),
    path('editor-permission/', views.editor_permission_check, name='editor_permission'),
    path('permissions/', views.permission_list, name='permission_list'),

]