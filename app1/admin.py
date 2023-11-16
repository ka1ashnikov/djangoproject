from django.contrib import admin
from .models import links_db, users, codes

admin.site.register(links_db)
admin.site.register(users)
admin.site.register(codes)