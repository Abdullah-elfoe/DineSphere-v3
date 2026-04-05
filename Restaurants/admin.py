from django.contrib import admin
from .models import Restaurant, SeatingType, TableSize, Table, FavouriteRestaurant, ReviewSummary, Testimonials, Review, SpecialDay



admin.site.register(
    [
        Restaurant, 
        SeatingType, 
        TableSize, 
        Table, 
        FavouriteRestaurant,
        Review,
        SpecialDay
    ]
)