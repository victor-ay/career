# from rest_framework import mixins
# from rest_framework.permissions import BasePermission
# from rest_framework.viewsets import GenericViewSet
#
# from jobs_app.models import Application
# from jobs_app.serializers.applications import ApplicationsSerializer
#
#
# class ApplicationsPermissions(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ['GET'] and request.user.is_staff:
#             return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         pass
#
# class ApplicationsViewSet(
#                     mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    # mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet
# ):
#     queryset = Application.objects.all()
#     permission_classes = [AuthenticationPermission ,ApplicationsPermissions]
#     serializer_class = ApplicationsSerializer