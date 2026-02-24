from rest_framework import serializers
from .models import (
    Property, PropertyImage, Seller, County, CountyArea,
    Section, Aisle, Enquiry, PropertySizeUnit
)


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = ["id", "name", "reference"]


class CountyAreaSerializer(serializers.ModelSerializer):
    county = CountySerializer(read_only=True)

    class Meta:
        model = CountyArea
        fields = ["id", "name", "reference", "county"]


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "reference", "name", "translation_key"]


class AisleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aisle
        fields = ["id", "reference", "name", "translation_key"]


class SellerSerializer(serializers.ModelSerializer):
    seller_type_name = serializers.CharField(source="seller_type.name", read_only=True)

    class Meta:
        model = Seller
        fields = [
            "id", "name", "profile_id", "seller_type_name",
            "picture", "tagline", "description", "is_verified",
        ]


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "url", "is_cover", "active"]


class PropertyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing view."""
    section = SectionSerializer(read_only=True)
    aisle = AisleSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    county_name = serializers.CharField(source="county.name", read_only=True)
    county_area_name = serializers.CharField(source="county_area.name", read_only=True)

    price = serializers.SerializerMethodField()
    property_size = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    contact = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            "id", "section", "aisle", "seller", "images",
            "title", "description", "property_type",
            "bedroom_count", "bathroom_count",
            "is_featured", "available_from", "rental_period",
            "county_name", "county_area_name",
            "ber", "ber_number", "ad_address", "ad_link",
            "price", "property_size", "location", "contact",
            "created_at", "updated_at",
        ]

    def get_price(self, obj):
        return {
            "currency": obj.price_currency,
            "symbol": obj.price_symbol,
            "min_value": str(obj.price_min_value),
            "is_price_on_application": obj.is_price_on_application,
        }

    def get_property_size(self, obj):
        unit = obj.property_size_unit
        return {
            "value": str(obj.property_size_value),
            "parameter": unit.symbol if unit else "m²",
            "unit": {
                "name": unit.name if unit else "Square Meters",
                "symbol": unit.symbol if unit else "m²",
            } if unit else None,
        }

    def get_location(self, obj):
        return {
            "county": obj.county.name if obj.county else "",
            "county_area": obj.county_area.name if obj.county_area else "",
            "eir_code": obj.eir_code,
            "address": obj.ad_address,
        }

    def get_contact(self, obj):
        seller = obj.seller
        return {
            "name": seller.name,
            "email": seller.email,
            "phone": seller.phone,
            "phone_code": seller.phone_code,
            "is_email_only": False,
        }


class PropertyDetailSerializer(PropertyListSerializer):
    """Full serializer for detail view."""
    class Meta(PropertyListSerializer.Meta):
        fields = PropertyListSerializer.Meta.fields + ["description"]


class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ["id", "property", "sender_name", "sender_email", "sender_phone", "message", "created_at"]
        read_only_fields = ["id", "created_at"]