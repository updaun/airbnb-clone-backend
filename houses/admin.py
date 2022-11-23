from django.contrib import admin
from .models import House

# admin.site.register(House)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):

    # fields = (
    #     "name",
    #     "address",
    #     ("price_per_night", "pets_allowed"),
    # )

    list_display = ("name", "price_per_night", "address", "pets_allowed")
    list_filter = ("price_per_night", "pets_allowed")
    # search_fields = ["address__startwith"]
    # search_fields = ("address",)
    # exclude = ("price_per_night", )
    # list_display_links = ("name", "address")
    # list_editable = ("pets_allowed",)
