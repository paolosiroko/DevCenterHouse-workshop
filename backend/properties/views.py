from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

from .models import Property, County, CountyArea, Section, Aisle, Enquiry
from .serializers import (
    PropertyListSerializer, PropertyDetailSerializer,
    CountySerializer, CountyAreaSerializer, EnquirySerializer,
    SectionSerializer, AisleSerializer,
)


class PropertyFilter(django_filters.FilterSet):
    section = django_filters.CharFilter(field_name="section__reference")
    aisle = django_filters.CharFilter(field_name="aisle__reference")
    county = django_filters.CharFilter(field_name="county__reference")
    county_area = django_filters.CharFilter(field_name="county_area__reference")
    property_type = django_filters.CharFilter(field_name="property_type")
    bedrooms = django_filters.NumberFilter(field_name="bedroom_count")
    bedrooms_min = django_filters.NumberFilter(field_name="bedroom_count", lookup_expr="gte")
    bedrooms_max = django_filters.NumberFilter(field_name="bedroom_count", lookup_expr="lte")
    price_min = django_filters.NumberFilter(field_name="price_min_value", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price_min_value", lookup_expr="lte")
    ber = django_filters.CharFilter(field_name="ber")
    available_from = django_filters.DateFilter(field_name="available_from", lookup_expr="gte")

    class Meta:
        model = Property
        fields = []


class PropertyListView(generics.ListAPIView):
    """
    GET /api/properties/
    Supports filters: section, aisle, county, county_area, property_type,
                      bedrooms, bedrooms_min, bedrooms_max, price_min, price_max, ber
    Supports search: ?search=<keyword>  (searches title, description, address)
    Supports ordering: ?ordering=price_min_value | -price_min_value | created_at | -created_at
    Supports pagination: ?page=1&page_size=6 (default page_size=6)
    """
    serializer_class = PropertyListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ["title", "description", "ad_address", "county__name", "county_area__name"]
    ordering_fields = ["price_min_value", "created_at", "bedroom_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Property.objects
            .select_related("section", "aisle", "seller", "county", "county_area", "property_size_unit")
            .prefetch_related("images")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated = self.get_paginated_response(serializer.data)
            # Add meta similar to FindQo API format
            paginated.data["meta"] = {
                "total": self.paginator.page.paginator.count,
                "per_page": self.paginator.page_size,
                "current_page": self.paginator.page.number,
                "total_pages": self.paginator.page.paginator.num_pages,
            }
            return paginated
        serializer = self.get_serializer(queryset, many=True)
        return Response({"kind": "ads#list", "data": serializer.data})


class PropertyDetailView(generics.RetrieveAPIView):
    """GET /api/properties/<id>/"""
    serializer_class = PropertyDetailSerializer
    queryset = (
        Property.objects
        .select_related("section", "aisle", "seller", "county", "county_area", "property_size_unit")
        .prefetch_related("images")
    )


class SimilarPropertiesView(generics.ListAPIView):
    """GET /api/properties/<id>/similar/ — same county, same section, different property"""
    serializer_class = PropertyListSerializer

    def get_queryset(self):
        prop = Property.objects.get(pk=self.kwargs["pk"])
        return (
            Property.objects
            .filter(county=prop.county, section=prop.section)
            .exclude(pk=prop.pk)
            .select_related("section", "aisle", "seller", "county", "county_area", "property_size_unit")
            .prefetch_related("images")
            .order_by("-is_featured", "-created_at")[:6]
        )


class EnquiryCreateView(generics.CreateAPIView):
    """POST /api/enquiries/"""
    serializer_class = EnquirySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"success": True, "message": "Enquiry sent successfully.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


class CountyListView(generics.ListAPIView):
    """GET /api/counties/"""
    serializer_class = CountySerializer
    queryset = County.objects.all().order_by("name")


class CountyAreaListView(generics.ListAPIView):
    """GET /api/counties/<county_id>/areas/"""
    serializer_class = CountyAreaSerializer

    def get_queryset(self):
        return CountyArea.objects.filter(county_id=self.kwargs["county_id"]).order_by("name")


@api_view(["GET"])
def sections_view(request):
    """GET /api/sections/ — returns sections and their aisles for nav/filter"""
    sections = Section.objects.prefetch_related("aisles").all()
    data = []
    for s in sections:
        data.append({
            "id": s.id,
            "reference": s.reference,
            "name": s.name,
            "aisles": AisleSerializer(s.aisles.all(), many=True).data,
        })
    return Response(data)


@api_view(["GET"])
def filter_options_view(request):
    """GET /api/filter-options/ — returns all filter dropdown options"""
    property_types = [
        {"value": k, "label": v}
        for k, v in Property.PROPERTY_TYPE_CHOICES
    ]
    bedroom_options = [
        {"value": i, "label": f"{i}+" if i == 5 else str(i)}
        for i in range(1, 6)
    ]
    price_ranges = {
        "rent": [
            {"min": 0, "max": 1000, "label": "Up to €1,000"},
            {"min": 1000, "max": 1500, "label": "€1,000 – €1,500"},
            {"min": 1500, "max": 2000, "label": "€1,500 – €2,000"},
            {"min": 2000, "max": 2500, "label": "€2,000 – €2,500"},
            {"min": 2500, "max": 3000, "label": "€2,500 – €3,000"},
            {"min": 3000, "max": None, "label": "€3,000+"},
        ],
        "sale": [
            {"min": 0, "max": 200000, "label": "Up to €200k"},
            {"min": 200000, "max": 300000, "label": "€200k – €300k"},
            {"min": 300000, "max": 500000, "label": "€300k – €500k"},
            {"min": 500000, "max": 750000, "label": "€500k – €750k"},
            {"min": 750000, "max": None, "label": "€750k+"},
        ],
    }
    return Response({
        "property_types": property_types,
        "bedroom_options": bedroom_options,
        "price_ranges": price_ranges,
    })