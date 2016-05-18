from django.contrib import admin
from .models import UserProfile

from .models import Site

admin.site.register(Site)
admin.site.register(UserProfile)
