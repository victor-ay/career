from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from jobs_app.models import Company
from jobs_app.serializers.companies import CompaniesSerializer

class CompaniesPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.id == obj.user_id:
                return True

        return False

class CompaniesPaginationClass(PageNumberPagination):
    page_size = 50

class CompaniesViewSet(
                    mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   # mixins.UpdateModelMixin,
                   # mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = Company.objects.all()
    serializer_class = CompaniesSerializer
    # permission_classes = [CompaniesPermissions, IsAuthenticated, IsAdminUser]
    permission_classes = [CompaniesPermissions]

    pagination_class = CompaniesPaginationClass

    def get_queryset(self):
        qs = self.queryset

        # Do not list the company if 'list_my_jobs' = False, for request from not staff
        if not self.request.user.is_staff:
            qs = qs.filter(list_my_jobs = True)

        return qs