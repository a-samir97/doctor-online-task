from rest_framework.permissions import BasePermission

class IsPatient(BasePermission):
    
    message = 'You are not a patient.'

    def has_permission(self, request, view):
        return request.user.user_type == 'P'

class IsDoctor(BasePermission):
    
    message = 'You are not a doctor.'
    
    def has_permission(self, request, view):
        return request.user.user_type == 'D'

class IsOwner(BasePermission):

    message = 'you are not owned this session.'

    def has_object_permission(self, request, view, obj):
        return obj.doctor == request.user