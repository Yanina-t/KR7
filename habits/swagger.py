from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path

schema_view = get_schema_view(
   openapi.Info(
      title="Habits Tracker API",
      default_version='v1',
      description="API для отслеживания привычек",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
