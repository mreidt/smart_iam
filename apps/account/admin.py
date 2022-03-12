from django.contrib import admin

from apps.account.models import AccountProducts, IAMAccount

admin.site.register(IAMAccount)
admin.site.register(AccountProducts)
