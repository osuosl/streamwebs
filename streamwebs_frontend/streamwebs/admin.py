from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    Site,
    Water_Quality, WQ_Sample, Macroinvertebrates, TransectZone,
    RiparianTransect, Canopy_Cover, School, CameraPoint,
    PhotoPoint, PhotoPointImage, Soil_Survey, Resource, UserProfile,
    GalleryImage, GalleryFile, GalleryAlbum
)

admin.site.register(Site)
admin.site.register(Water_Quality)
admin.site.register(WQ_Sample)
admin.site.register(Macroinvertebrates)
admin.site.register(TransectZone)
admin.site.register(RiparianTransect)
admin.site.register(Canopy_Cover)
admin.site.register(School)
admin.site.register(CameraPoint)
admin.site.register(PhotoPoint)
admin.site.register(PhotoPointImage)
admin.site.register(Soil_Survey)
admin.site.register(Resource)
admin.site.register(GalleryImage)
admin.site.register(GalleryFile)
admin.site.register(GalleryAlbum)

# The following will add a profile model's files to the user page in the
# admin panel


# Define an inline admin descriptor for normal profile model
# which acts a bit like a singleton
# refed from: https://docs.djangoproject.com/en/1.9/topics/auth/customizing/
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profiles'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
