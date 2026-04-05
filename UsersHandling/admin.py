from django.contrib import admin
from .models import User, CustomerProfile, RestaurantStaff



admin.site.register(
    [
        User, 
        CustomerProfile,
        RestaurantStaff
    ]
)