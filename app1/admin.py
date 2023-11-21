from django.contrib import admin
from .models import links_db, users, codes, gmail_tokens

admin.site.register(links_db)
admin.site.register(users)
admin.site.register(codes)
admin.site.register(gmail_tokens)
