from django.contrib import admin

from payment import models


admin.site.register(models.Transaction)
