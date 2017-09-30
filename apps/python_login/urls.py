from django.conf.urls import url
from django.conf.urls import include
from . import views

urlpatterns = [
    url(r'^$', views.home),
	url(r'^check_login$', views.check_login),
	url(r'^check_register$', views.check_register),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.travels_add),
	url(r'^check_travel$', views.check_travel),
    url(r'^travels/destination/(?P<id>\d+)$', views.show),
	url(r'^travels/join/(?P<id>\d+)$', views.add_trip),
    url(r'^logout$', views.logout),
]
