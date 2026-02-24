from django.contrib import admin
from .models import (
    County, CountyArea, SellerType, Seller, Section, Aisle,
    Property, PropertyImage, PropertySizeUnit, Enquiry
)


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ["name", "reference"]
    prepopulated_fields = {"reference": ("name",)}


@admin.register(CountyArea)
class CountyAreaAdmin(admin.ModelAdmin):
    list_display = ["name", "county", "reference"]
    list_filter = ["county"]


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ["name", "seller_type", "email", "is_verified", "is_disabled"]
    list_filter = ["seller_type", "is_verified"]
    search_fields = ["name", "email"]


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        "title", "property_type", "bedroom_count", "price_min_value",
        "county", "county_area", "is_featured", "created_at"
    ]
    list_filter = ["section", "aisle", "county", "property_type", "is_featured", "ber"]
    search_fields = ["title", "ad_address", "description"]
    inlines = [PropertyImageInline]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "description", "section", "aisle", "property_type", "seller")
        }),
        ("Specifications", {
            "fields": ("bedroom_count", "bathroom_count", "ber", "ber_number",
                       "property_size_value", "property_size_unit")
        }),
        ("Pricing", {
            "fields": ("price_min_value", "price_currency", "price_symbol",
                       "is_price_on_application", "rental_period")
        }),
        ("Location", {
            "fields": ("county", "county_area", "ad_address", "eir_code")
        }),
        ("Status", {
            "fields": ("is_featured", "available_from", "ad_link", "created_at", "updated_at")
        }),
    )


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ["sender_name", "sender_email", "property", "created_at"]
    readonly_fields = ["created_at"]


admin.site.register(Section)
admin.site.register(Aisle)
admin.site.register(SellerType)
admin.site.register(PropertySizeUnit)