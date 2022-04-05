from django.contrib import admin

from apps.user.models import CustomUser, UserAccount, UserPermissions

admin.site.register(CustomUser)
admin.site.register(UserAccount)
admin.site.register(UserPermissions)
