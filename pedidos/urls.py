from django.urls import path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from pedidos.serializers import ItemsViewSet

router = routers.SimpleRouter()
router.register(r'items', ItemsViewSet)

urlpatterns = router.urls
urlpatterns += [
    path(r'docs/', include_docs_urls(title='Zapatos Bernini API')),
    path('openapi', get_schema_view(
        title="Zapatos Bernini",
        description="Retrieve Zapatos Bernini products"
    ), name='openapi-schema'),
]
