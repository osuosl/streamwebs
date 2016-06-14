from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sites$', views.sites, name='sites'),
    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)$', views.site, name='site'),
]
