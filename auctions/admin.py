from django.contrib import admin

# Register your models here.

from .models import Listing, Bids, ListingImage

admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(ListingImage)

