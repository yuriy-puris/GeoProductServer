from django.urls import path

from .views import AddressView, CoordinatesView, ParseLocationView

urlpatterns = [
  path('/address', AddressView.as_view(), name='address'),
  path('/coordinates', CoordinatesView.as_view(), name='coordinate'),
  path('/post_location', ParseLocationView.as_view(), name='post_location'),
]
