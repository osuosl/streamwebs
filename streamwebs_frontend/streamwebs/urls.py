from django.conf.urls import include, url
from . import views

app_name = 'streamwebs'
urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', views.index, name='index'),

    url(r'^create_site/$', views.create_site, name='create_site'),

    url(r'^sites$', views.sites, name='sites'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)$', views.site, name='site'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/water$',
        views.graph_water, name='graph_water'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/macros$',
        views.graph_macros, name='graph_macros'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/water/(?P<data_id>\d+)',
        views.water_quality, name='water_quality'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/delete/', views.deactivate_site,
        name='deactivate_site'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/update/', views.update_site,
        name='update_site'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/water/edit',
        views.water_quality_edit, name='water_quality_edit'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/macro/(?P<data_id>\d+)$',
        views.macroinvertebrate, name='macroinvertebrate_view'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/macro/edit$',
        views.macroinvertebrate_edit, name='macroinvertebrate_edit'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/macros$',
        views.graph_macros, name='graph_macros'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/transect/(?P<data_id>\d+)',
        views.riparian_transect_view, name='riparian_transect'),

    url(r'^site/(?P<site_slug>[0-9a-zA-Z-]+)/transect/edit',
        views.riparian_transect_edit, name='riparian_transect_edit'),

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout')
]
