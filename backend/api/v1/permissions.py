from rest_framework import permissions


class IsRecipeOwner(permissions.BasePermission):
    """
    Пользователь может редактировать или удалять только свои рецепты.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PATCH']:
            print(request.user)
            print(obj.author)
            return obj.author == request.user
        return True
