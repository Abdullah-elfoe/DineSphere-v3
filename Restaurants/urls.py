from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("registration/", views.registration, name="restaurant_registration"),
    path("staff-management/", views.staff_management, name="staff_management"),
    path("reservations/", views.reservations, name="reservations"),
    path("tables/", views.tables, name="tables"),
    path("holidays/", views.holidays, name="holidays"),
    path("business-info/", views.business_info, name="business_info"),
    path("reviews/", views.reviews, name="reviews"),


    path("switch/", views.switch_business, name="switch_business"),
    path("markfinish/", views.markfinish),
    path("markcancel/", views.markcancel),
    path("hide/", views.hide),
    path("unhide/", views.unhide),

    # Business
    path('business-info/update/<int:id>/', views.updateBusiness, name='update_business'),
    path('business-info/delete/<int:id>/', views.deleteBusiness, name='delete_business'),
    
    # Tables
    path('tables/update/<int:id>/', views.updateTables, name='update_tables'),
    path('tables/delete/<int:id>/', views.deleteTables, name='delete_tables'),
    
    # Holidays
    path('holidays/update/<int:id>/', views.updateHolidays, name='update_holidays'),
    path('holidays/delete/<int:id>/', views.deleteHolidays, name='delete_holidays'),

    
    path("", views.analytics, name="analytics"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
