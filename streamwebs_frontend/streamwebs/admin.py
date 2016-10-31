from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from models import UserProfile

from .models import Site
from .models import Water_Quality
from .models import WQ_Sample
from .models import Macroinvertebrates
from .models import TransectZone
from .models import RiparianTransect
from .models import Canopy_Cover
from .models import CC_Cardinal
from .models import School
from .models import CameraPoint
from .models import PhotoPoint, PhotoPointImage
from .models import Soil_Survey

admin.site.register(Site)
admin.site.register(Water_Quality)
admin.site.register(WQ_Sample)
admin.site.register(Macroinvertebrates)
admin.site.register(TransectZone)
admin.site.register(RiparianTransect)
admin.site.register(Canopy_Cover)
admin.site.register(CC_Cardinal)
admin.site.register(School)
admin.site.register(CameraPoint)
admin.site.register(PhotoPoint)
admin.site.register(PhotoPointImage)
admin.site.register(Soil_Survey)


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
