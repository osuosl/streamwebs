from django.conf.urls import include, url

from . import views

app_name = 'streamwebs'
urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', views.index, name='index'),
    url(r'^sites$', views.sites, name='sites'),
    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)$', views.site, name='site'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)/water/(?P<data_id>\d+)',
        views.water_quality, name='water_quality'),
    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)/water/edit',
        views.water_quality_edit, name='water_quality_edit'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)/macro/(?P<data_id>\d+)$',
        views.macroinvertebrate, name='macroinvertebrate_view'),
    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)/macro/edit$',
        views.macroinvertebrate_edit, name='macroinvertebrate_edit'),


#    url(r'^site/(?P<site_slug>[0-9a-zA-Z]+)/riparian_transect/edit',
#        views.riparian_transect_edit, name='riparian_transect_edit'),
    url(r'^riparian_transect_edit/$', views.riparian_transect_edit, name='riparian_transect_edit'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout')
]
