from django.contrib import admin


from .models import *

admin.site.register(Review)
admin.site.register(Report)
admin.site.register(RecentAction)
admin.site.register(Like)
admin.site.register(Dislike)
