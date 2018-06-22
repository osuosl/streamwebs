from django.conf.urls import include, url
import views

app_name = 'streamwebs'
urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', views.index, name='index'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^about/$', views.about, name='about'),


    url(r'^sites/new/$', views.create_site, name='create_site'),

    url(r'^sites/$', views.sites, name='sites'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/$', views.site, name='site'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/image/add/$',
        views.add_gallery_image, name='add_gallery_image'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/album/add/$',
        views.add_gallery_album, name='add_gallery_album'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/file/add/$',
        views.add_gallery_file, name='add_gallery_file'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/journal/add/$',
        views.add_gallery_journal, name='add_gallery_journal'),
    #url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/video/add/$',
    #    views.add_gallery_video, name='add_gallery_video'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/image/(?P<image_id>[0-9]+)/$',
        views.gallery_image, name='gallery_image'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/album/(?P<album_id>[0-9]+)/$',
        views.gallery_album, name='gallery_album'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/file/(?P<file_id>[0-9]+)/$',
        views.gallery_file, name='gallery_file'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/journal/' +
        '(?P<journal_id>[0-9]+)/$',
        views.gallery_journal, name='gallery_journal'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/video/(?P<video_id>[0-9]+)/$',
        views.gallery_video, name='gallery_video'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/image/(?P<image_id>[0-9]+)/' +
        'delete/$',
        views.delete_gallery_image, name='delete_gallery_image'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/album/(?P<album_id>[0-9]+)/' +
        'delete/$',
        views.delete_gallery_album, name='delete_gallery_album'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/file/(?P<file_id>[0-9]+)/' +
        'delete/$',
        views.delete_gallery_file, name='delete_gallery_file'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/journal/' +
        '(?P<journal_id>[0-9]+)/delete/$',
        views.delete_gallery_journal, name='delete_gallery_journal'),
    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/video/(?P<video_id>[0-9]+)/' +
        'delete/$',
        views.delete_gallery_video, name='delete_gallery_video'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/edit/', views.update_site,
        name='update_site'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/delete/', views.deactivate_site,
        name='deactivate_site'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/water/$',
        views.graph_water, name='graph_water'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/water/data/$',
        views.water_graph_site_data, name='water_graph_site_data'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/water/(?P<data_type>[a-zA-Z-_]+)'
        r'/(?P<date>\d{4}-\d{2}-\d{2})/',
        views.water_histogram, name='water_quality_histogram'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/macros/$',
        views.graph_macros, name='graph_macros'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/water/(?P<data_id>\d+)/$',
        views.water_quality, name='water_quality'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/water/(?P<data_id>\d+)/delete/$',
        views.water_quality_delete, name='water_quality_delete'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/water/edit/',
        views.water_quality_edit, name='water_quality_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/water/export/$',
        views.export_wq, name='export_wq'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/macro/(?P<data_id>\d+)/$',
        views.macroinvertebrate_view, name='macroinvertebrate_view'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/macro/(?P<data_id>\d+)/delete/$',
        views.macroinvertebrate_delete, name='macroinvertebrate_delete'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/macro/edit/$',
        views.macroinvertebrate_edit, name='macroinvertebrate_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/macro/export/$',
        views.export_macros, name='export_macros'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/rip_aqua/edit/$',
        views.riparian_aquatic_edit, name='rip_aqua_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/rip_aqua/(?P<data_id>\d+)/$',
        views.riparian_aquatic_view, name='rip_aqua_view'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/rip_aqua/(?P<ra_id>\d+)/' +
        'delete/$', views.riparian_aquatic_delete, name='rip_aqua_delete'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/rip_aqua/export/$',
        views.export_rip_aqua, name='export_rip_aqua'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/transect/(?P<data_id>\d+)/$',
        views.riparian_transect_view, name='riparian_transect'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/transect/(?P<data_id>\d+)/' +
        'delete/$',
        views.riparian_transect_delete, name='riparian_transect_delete'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/transect/edit/$',
        views.riparian_transect_edit, name='riparian_transect_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/transect/export/$',
        views.export_ript, name='export_transects'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/canopy/(?P<data_id>\d+)/$',
        views.canopy_cover_view, name='canopy_cover'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/canopy/(?P<data_id>\d+)/' +
        'delete/$', views.canopy_cover_delete, name='canopy_cover_delete'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/canopy/edit',
        views.canopy_cover_edit, name='canopy_cover_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/canopy/export/$',
        views.export_cc, name='export_cc'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/(?P<cp_id>\d+)/photo/' +
        '(?P<pp_id>\d+)/$', views.view_pp_and_add_img, name='photo_point'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/(?P<cp_id>\d+)/photo/' +
        'edit/?$', views.add_photo_point, name='photo_point_add'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/(?P<cp_id>\d+)/photo/' +
        '(?P<pp_id>\d+)/delete/$',
        views.delete_photo_point, name='photo_point_delete'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/(?P<cp_id>\d+)/$',
        views.camera_point_view, name='camera_point'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/(?P<cp_id>\d+)/delete/$',
        views.camera_point_delete, name='camera_point_delete'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/edit/$',
        views.add_camera_point, name='camera_point_add'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/camera/$',
        views.site_camera, name='site_camera'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/soil/(?P<data_id>\d+)/$',
        views.soil_survey, name='soil'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/soil/(?P<data_id>\d+)/delete/$',
        views.soil_survey_delete, name='soil_delete'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/soil/edit',
        views.soil_survey_edit, name='soil_edit'),

    url(r'^sites/(?P<site_slug>[0-9a-zA-Z-]+)/soil/export/$',
        views.export_soil, name='export_soil'),

    url(r'^statistics/$', views.admin_site_statistics, name='stats'),

    url(r'^register/$', views.register, name='register'),

    url(r'^new_org_request/(?P<school_id>[0-9]+)/$', views.new_org_request,
        name='new_org_request'),

    url(r'^register/confirm', views.confirm_registration,
        name='confirm_registration'),
    url(r'^account/$', views.account, name='account'),
    url(r'^account/update_email/$', views.update_email, name='update_email'),
    url(r'^account/update_password/$', views.update_password,
        name='update_password'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^resources/$', views.resources, name='resources'),
    url(r'^resources/data-sheets/', views.resources_data_sheets,
        name='resources-data-sheets'),
    url(r'^resources/curriculum-guides/', views.resources_publications,
        name='resources-publications'),
    url(r'^resources/tutorial-videos/', views.resources_tutorial_videos,
        name='resources-tutorial_videos'),
    url(r'^resources/new/', views.resources_upload, name='resources-upload'),

    url(r'^schools/$', views.schools, name='schools'),
    url(r'^schools/(?P<school_id>[0-9]+)/$',
        views.school_detail, name='school_detail'),
    url(r'^get_manage_accounts/(?P<user_id>[0-9]+)$',
        views.get_manage_accounts, name='get_manage_accounts'),
    url(r'^schools/(?P<school_id>[0-9]+)/manage_accounts/$',
        views.manage_accounts, name='manage_accounts'),
    url(r'^schools/(?P<school_id>[0-9]+)/add_account/$',
        views.add_account, name='add_account'),
    url(r'^schools/(?P<school_id>[0-9]+)/edit_account/(?P<user_id>[0-9]+)/$',
        views.edit_account, name='edit_account'),

    url(r'^approve_accounts/$',
        views.approve_accounts, name='approve_accounts'),

    # This is used to view a backend variable
    url(r'^var_debug/(?P<value>.*)/$',
        views.var_debug, name='var_debug')
]
