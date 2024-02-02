from rest_framework import permissions


class IsRecipeOwner(permissions.BasePermission):
    """
    Пользователь может редактировать или удалять только свои рецепты.
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            obj.author == request.user
        )


class IsSubscriber(permissions.BasePermission):
    """
    Пользователь не может подписаться на самого себя.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user != request.user
