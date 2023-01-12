from django.urls import include, path
from rest_framework import routers

from api.views import CartModelViewSet, ProductModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'carts', CartModelViewSet, basename='Cart')

urlpatterns = [
    path('', include(router.urls)),
]
