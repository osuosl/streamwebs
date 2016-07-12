from django.conf.urls import include, url

from . import views

app_name = 'streamwebs'

# Riparrian and Aquatic Survey:
RAS_patterns = [
    url(r'^(?P<data_id>\d+)', views.RAS, name='water_quality'),
    url(r'^edit', views.RAS_edit, name='water_quality_edit'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sites$', views.sites, name='sites'),
    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)$', views.site, name='site'),
    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)/water/(?P<data_id>\d+)',
        views.water_quality, name='water_quality'),
    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)/water/edit',
        views.water_quality_edit, name='water_quality_edit'),
    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)/ras/',
        include(RAS_patterns), name='ras'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout')
]
