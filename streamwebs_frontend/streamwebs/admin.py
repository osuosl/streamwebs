from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from models import UserProfile

from .models import Site

admin.site.register(Site)
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
