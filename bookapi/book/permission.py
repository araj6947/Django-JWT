from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsWriterOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method is SAFE_METHODS:
            return True
        return obj.writer == request.user