from django.conf.urls import include, url
from rest_framework import routers
from zipcode.views import ZipcodeView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'', ZipcodeView)

urlpatterns = [
    url(r'^', include(router.urls))
]
