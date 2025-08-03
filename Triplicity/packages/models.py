from django.db import models

# Create your models here.
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Package(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='packages')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='package_images/')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50, help_text="e.g., 4 Days / 3 Nights")

    include_meals = models.BooleanField(default=False)
    include_hotels = models.BooleanField(default=False)
    include_flights = models.BooleanField(default=False)
    include_sightseeing = models.BooleanField(default=False)
    custom_includes = models.TextField(blank=True, help_text="Other things included")

    short_itinerary = models.TextField(blank=True)
    # (extend: add a related Itinerary model later)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_inclusions(self):
        inclusions = []
        if self.include_meals: inclusions.append("Meals")
        if self.include_hotels: inclusions.append("Hotels")
        if self.include_flights: inclusions.append("Flights")
        if self.include_sightseeing: inclusions.append("Sightseeing")
        if self.custom_includes: inclusions.append(self.custom_includes)
        return inclusions
