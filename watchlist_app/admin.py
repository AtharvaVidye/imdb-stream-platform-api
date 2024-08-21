from django.contrib import admin
from .models import Review, Watchlist, StreamPlatform

admin.site.register(Watchlist)
admin.site.register(StreamPlatform)
admin.site.register(Review)
