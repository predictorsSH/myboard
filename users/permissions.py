from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):
    # GET : 누구나, POST, PATCH : 해당 유저

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # permissions.SAFE_METHOD : 데이터에 영향을 미치지 않는 요청(GET)
            return True
        return obj.user == request.user
