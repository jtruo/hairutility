from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from .users.views import UserViewSet, HairProfileViewSet, CompanyViewSet, ObtainAuthTokenView
from .webapp.views import HomePageView, AboutUsPageView, FAQView, WorkInProgressView, single_hair_profile, HairProfilesView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'hairprofiles', HairProfileViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    # Admin views
    path('v4e8S3UoTmbcFqB7/', admin.site.urls),
    path('nested_admin/', include('nested_admin.urls')),

    # Api views
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', ObtainAuthTokenView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Web views
    path('', HomePageView.as_view(), name='home'),
    path('about-us/', AboutUsPageView.as_view(), name='about-us'),
    path('hair-profiles/', HairProfilesView.as_view(), name='hair-profiles'),
    path('single-hair-profile/<thumbnail_key>/', single_hair_profile, name='single-hair-profile'),

    path('faq/', FAQView.as_view(), name='faq'),
    path('salons', WorkInProgressView.as_view(), name='salons'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
