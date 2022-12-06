from django.contrib import admin
from django.contrib.auth.models import User, Group

from upload.models import carts, pictures

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(carts)
admin.site.register(pictures)