
from .models import User, HairProfile, Company
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, HairProfileSerializer, CompanySerializer
from .filters import HairProfileFilter

from rest_framework import viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Creates, updates and retrives user info
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAdminUser, ]
        # elif self.action == 'retrieve':
        #     self.permission_classes = [IsOwnerOrReadOnly]
        return super(self.__class__, self).get_permissions()


class HairProfileViewSet(viewsets.ModelViewSet):

    """
    Viewset for creating, listing all of the hair profiles
    """
    queryset = HairProfile.objects.all()
    serializer_class = HairProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = HairProfileFilter

    def get_queryset(self):
        """
        Queryset changes based on parameters specified. If none, returns approved hair profiles
        There are other filters in filters.py
        """
        queryset = HairProfile.objects.all()

        user = self.request.query_params.get('user', None)
        user__email = self.request.query_params.get('user__email', None)
        access_code = self.request.query_params.get('access_code', None)

        if user__email and access_code is not None:
            queryset = queryset.filter(user__email=user__email, access_code=access_code)
            return queryset

        if user is not None:
            return queryset.filter(user=self.request.user)

        else:
            queryset = queryset.filter(user=self.request.user)
            return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Creates, updates and retrives company info
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)

    # def perform_create(self, request, serializer, *args, **kwargs):
    def perform_create(self, serializer):
        serializer.save(user_set=[self.request.user])


class ObtainAuthTokenView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'pk': user.id,
            'auth_token': token.key,
            'is_active': user.is_active,
            'is_stylist': user.is_stylist,
            'first_name': user.first_name,
            'email': user.email

        })
