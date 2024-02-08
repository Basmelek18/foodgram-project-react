from rest_framework import permissions


class IsRecipeOwner(permissions.BasePermission):
    """
    User can update or delete only his recipe.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
