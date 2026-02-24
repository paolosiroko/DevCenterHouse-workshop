from django.db import models
from django.contrib.auth.models import User


class County(models.Model):
    name = models.CharField(max_length=100)
    reference = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Counties"

    def __str__(self):
        return self.name


class CountyArea(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="areas")
    name = models.CharField(max_length=150)
    reference = models.SlugField()

    def __str__(self):
        return self.name


class SellerType(models.Model):
    PRIVATE = 1
    AGENT = 2
    TYPE_CHOICES = [(PRIVATE, "Private"), (AGENT, "Agent/Broker")]

    id = models.IntegerField(primary_key=True, choices=TYPE_CHOICES)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    profile_id = models.SlugField(unique=True)
    seller_type = models.ForeignKey(SellerType, on_delete=models.PROTECT)
    picture = models.URLField(blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    phone_code = models.CharField(max_length=10, default="+353")
    is_verified = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    has_business_profile = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    """Top-level category: Properties FOR RENT, FOR SALE, etc."""
    reference = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    translation_key = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Aisle(models.Model):
    """Sub-category under Section: Rent Residential, Rent Commercial, etc."""
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="aisles")
    reference = models.SlugField()
    name = models.CharField(max_length=100)
    translation_key = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class PropertySizeUnit(models.Model):
    name = models.CharField(max_length=50)
    reference = models.SlugField(unique=True)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol


class Property(models.Model):
    RENTAL_PERIOD_CHOICES = [
        ("Monthly", "Monthly"),
        ("Weekly", "Weekly"),
        ("Daily", "Daily"),
    ]

    BER_CHOICES = [
        ("A1", "A1"), ("A2", "A2"), ("A3", "A3"),
        ("B1", "B1"), ("B2", "B2"), ("B3", "B3"),
        ("C1", "C1"), ("C2", "C2"), ("C3", "C3"),
        ("D1", "D1"), ("D2", "D2"),
        ("E1", "E1"), ("E2", "E2"),
        ("F", "F"), ("G", "G"),
        ("Exempt", "Exempt"),
    ]

    PROPERTY_TYPE_CHOICES = [
        ("apartment", "Apartment"),
        ("house", "House"),
        ("terraced-house", "Terraced House"),
        ("semi-detached", "Semi-Detached"),
        ("detached", "Detached"),
        ("bungalow", "Bungalow"),
        ("studio", "Studio"),
        ("duplex", "Duplex"),
        ("townhouse", "Townhouse"),
    ]

    section = models.ForeignKey(Section, on_delete=models.PROTECT)
    aisle = models.ForeignKey(Aisle, on_delete=models.PROTECT)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="properties")
    county = models.ForeignKey(County, on_delete=models.PROTECT)
    county_area = models.ForeignKey(CountyArea, on_delete=models.PROTECT, null=True, blank=True)

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default="apartment")
    bedroom_count = models.PositiveSmallIntegerField(default=0)
    bathroom_count = models.PositiveSmallIntegerField(default=0)

    # Pricing
    price_currency = models.CharField(max_length=5, default="EUR")
    price_symbol = models.CharField(max_length=5, default="€")
    price_min_value = models.DecimalField(max_digits=12, decimal_places=2)
    is_price_on_application = models.BooleanField(default=False)
    rental_period = models.CharField(max_length=20, choices=RENTAL_PERIOD_CHOICES, default="Monthly")

    # Property details
    ber = models.CharField(max_length=10, choices=BER_CHOICES, blank=True)
    ber_number = models.CharField(max_length=50, blank=True)
    property_size_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    property_size_unit = models.ForeignKey(
        PropertySizeUnit, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Location
    ad_address = models.CharField(max_length=500)
    eir_code = models.CharField(max_length=20, blank=True)

    # Status
    is_featured = models.BooleanField(default=False)
    available_from = models.DateField(null=True, blank=True)
    ad_link = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    url = models.URLField()
    is_cover = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["-is_cover", "order"]

    def __str__(self):
        return f"Image for {self.property.title}"


class Enquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="enquiries")
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    sender_phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"Enquiry from {self.sender_name} for {self.property.title}"