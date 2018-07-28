from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.routers import DefaultRouter


from .users.views import UserViewSet, HairProfileViewSet, CompanyViewSet, CompanyUpdateViewSet, ObtainAuthTokenView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hairprofiles', HairProfileViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'companiesupdate', CompanyUpdateViewSet)

urlpatterns = [
    # Admin views
    path('admin/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),

    # Api views
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', ObtainAuthTokenView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Web views
    # path('', HomePageView.as_view(), name='home'),
    # path('test/', TestPageView.as_view(), name='test'),
    # path('profile/', UserProfileView.as_view(), name='usr_profile')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
