from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from config.settings import STATIC_ROOT, STATIC_URL, MEDIA_URL, MEDIA_ROOT
from . import views
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

schema_view = get_schema_view(openapi.Info(title="BtrrMe API documentation.",default_version='v1',),public=True,permission_classes=(permissions.AllowAny,),)


urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', views.index, name='home'),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("nutrition/", include("nutrition.urls")),
    path("workout/", include("workout.urls")),
    path("supplement/", include("supplement.urls")),
    path("blog/", include("blog.urls")),
    path("chat/", include("chat.urls")),
    path("program/", include("program.urls")),
    path("contact/", include("contact.urls")),
]
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
