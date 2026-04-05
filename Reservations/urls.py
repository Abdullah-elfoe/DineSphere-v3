from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('placeOrder/', views.placeOrder_view, name='place-order'),
    path('<slug:Restaurant_name>/', views.booking_view, name='booking'),
    path('<slug:Restaurant_name>/postReview/', views.post_review, name='post-review')
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    




