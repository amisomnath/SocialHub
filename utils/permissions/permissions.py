from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions

class IsOwnerOrSuperuser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is a superuser or the owner of the post.
        return obj.author == request.user or request.user.is_superuser
    

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the post.
        if obj.author == request.user:
            return True

        raise PermissionDenied("You don't own this content.")
    

class IsSuperuserOrAuthor(permissions.BasePermission):
    """
    Custom permission to allow superusers to have full access to all posts
    and restrict non-superuser regular users to CRUD their own posts.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is a superuser
        if request.user.is_superuser:
            return True

        # Check if the user is the author of the post
        return obj.author == request.user