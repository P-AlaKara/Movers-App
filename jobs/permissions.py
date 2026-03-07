from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    message = "Only customers can perform this action."

    def has_permission(self, request, view):
        #although unlikely for a user to have no profile, check existence to avoid attribute errors
        return hasattr(request.user, 'profile') and request.user.profile.role == 'customer'


class IsMover(BasePermission):
    message = "Only movers can perform this action."

    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.role == 'mover'