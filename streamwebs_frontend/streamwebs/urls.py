from django.conf.urls import include, url
from . import views

app_name = 'streamwebs'
urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', views.index, name='index'),

    url(r'^sites/new/$', views.create_site, name='create_site'),

    url(r'^sites/$', views.sites, name='sites'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/$', views.site, name='site'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/water/$',
        views.graph_water, name='graph_water'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/macros/$',
        views.graph_macros, name='graph_macros'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/water/(?P<data_id>\d+)/',
        views.water_quality, name='water_quality'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/delete/', views.deactivate_site,
        name='deactivate_site'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/edit/', views.update_site,
        name='update_site'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/water/edit/',
        views.water_quality_edit, name='water_quality_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/macro/(?P<data_id>\d+)/$',
        views.macroinvertebrate, name='macroinvertebrate_view'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/macro/edit/$',
        views.macroinvertebrate_edit, name='macroinvertebrate_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/macros/$',
        views.graph_macros, name='graph_macros'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/transect/(?P<data_id>\d+)/',
        views.riparian_transect_view, name='riparian_transect'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/transect/edit/',
        views.riparian_transect_edit, name='riparian_transect_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/canopy/(?P<data_id>\d+)/',
        views.canopy_cover_view, name='canopy_cover'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/(?P<cp_id>\d+)/photo/' +
        '(?P<pp_id>\d+)/?$', views.view_pp_and_add_img, name='photo_point'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/(?P<cp_id>\d+)/photo/' +
        'edit/?$', views.add_photo_point, name='photo_point_add'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/(?P<cp_id>\d+)/$',
        views.camera_point_view, name='camera_point'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/edit/',
        views.add_camera_point, name='camera_point_add'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/canopy/edit',
        views.canopy_cover_edit, name='canopy_cover_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/soil/edit',
        views.soil_survey_edit, name='soil_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/soil/(?P<data_id>\d+)/$',
        views.soil_survey, name='soil'),

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout')
]
