from rest_framework import permissions

class CreateEventPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.user.is_authenticated:
                return request.user.is_club()
            return False
        return True