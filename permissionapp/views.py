from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .decorators import hasin_required, admin_required, editor_required, manager_required
# Create your views here.
from django.contrib.auth.models import Permission

@login_required
def dashboard(request):
    return render(request, "authcheck/dashboard.html",{
        'user': request.user,
        'groups': request.user.groups.all()
    })

@hasin_required
def only_for_hasin(request):
    return render(request, "authcheck/hasin_only.html")

@admin_required
def admin_panel(request):
    return render(request, 'authcheck/admin_panel.html', {
        'message': 'Welcome to Admin Panel'
    })

@manager_required
def manager_dashboard(request):
    return render(request, 'authcheck/manager_dashboard.html', {
        'message': 'Welcome to Manager Dashboard'
    })

@editor_required
def editor_workspace(request):
    return render(request, 'authcheck/editor_dashboard.html', {
        'message': 'Welcome to Editor Workspace'
    })


@login_required
def editor_permission_check(request):
    # Check if user belongs to editors group
    is_editor = request.user.groups.filter(name='editors').exists()
    # Check if user has the required permission
    has_permission = request.user.has_perm('auth.view_user')
    
    # User must be both an editor and have the permission
    is_authorized = is_editor and has_permission
    
    return render(request, 'authcheck/editor_permission_check.html', {
        'message': 'Editor with special permission page',
        'is_editor': is_editor,
        'has_permission': has_permission,
        'is_authorized': is_authorized
    })

@login_required
def permission_list(request):
    # Get all permissions and organize them by content type
    permissions = Permission.objects.all().select_related('content_type')
    permissions_by_type = {}
    
    for permission in permissions:
        content_type = permission.content_type.app_label
        if content_type not in permissions_by_type:
            permissions_by_type[content_type] = []
        permissions_by_type[content_type].append(permission)
    
    # Get user's permissions
    user_perms = [perm.codename for perm in request.user.user_permissions.all()]
    # Add permissions from groups
    user_perms.extend([perm.codename for perm in Permission.objects.filter(group__user=request.user)])
    
    return render(request, 'authcheck/permission_list.html', {
        'permissions_by_type': permissions_by_type,
        'user_perms': user_perms
    })