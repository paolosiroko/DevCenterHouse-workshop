from django.urls import path
from . import views

urlpatterns = [
    # Properties
    path("properties/", views.PropertyListView.as_view(), name="property-list"),
    path("properties/<int:pk>/", views.PropertyDetailView.as_view(), name="property-detail"),
    path("properties/<int:pk>/similar/", views.SimilarPropertiesView.as_view(), name="property-similar"),

    # Enquiries
    path("enquiries/", views.EnquiryCreateView.as_view(), name="enquiry-create"),

    # Reference data
    path("counties/", views.CountyListView.as_view(), name="county-list"),
    path("counties/<int:county_id>/areas/", views.CountyAreaListView.as_view(), name="county-area-list"),
    path("sections/", views.sections_view, name="sections"),
    path("filter-options/", views.filter_options_view, name="filter-options"),
]