from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기 요청에 대한 권한 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 요청자(request.user)가 객체의 user와 동일한지 확인
        return obj.author == request.user


class IsOwnerOrReadOnlySub(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기 요청에 대한 권한 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 요청자(request.user)가 객체의 user와 동일한지 확인
        return obj.post.author == request.user