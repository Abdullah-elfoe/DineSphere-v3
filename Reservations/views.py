from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from Restaurants.models import Restaurant, Table
from .services import (
    create_booking,
    view_all_booking
)
from Restaurants.models import Restaurant, Review
from .utils import  replace_with_space
from .models import Booking


def booking_view(request, Restaurant_name):
    """
    Handles restaurant table reservations.

    GET: Display only available tables for the selected date and time.
    POST: Submit the booking form (simpler, just submits data).

    GET parameters (optional):
        - date
        - start_time
        - end_time

    POST parameters:
        - date, start_time, end_time, table_ids, required_capacity
    """
    Restaurant_name = replace_with_space(Restaurant_name)
    restaurant = get_object_or_404(Restaurant, name=Restaurant_name)

    if request.method == "GET":
        # Call service function to get tables
        booking_data = view_all_booking(
            restaurant,
            date_str=request.GET.get("date"),
            start_time_str=request.GET.get("start_time"),
            end_time_str=request.GET.get("end_time")
        )
        booking_data['reviews'] = Review.objects.filter(restaurant=restaurant)
        return render(request, "Reservations/reservation.html", booking_data)

    elif request.method == "POST":
        context = create_booking(request, Restaurant_name)
        return render(request, "Reservations/checkout.html", context)



@login_required
def checkout_view(request):
    return render(request, "Reservations/checkout.html") if request.method == "GET" else placeOrder_view(request)



def placeOrder_view(request):
    s_time = request.POST.get("s_time")
    date = request.POST.get("date")
    # Combine and parse datetime
    naive_dt = datetime.strptime(
        f"{date} {s_time}",
        "%Y-%m-%d %H:%M"
    )

    # Convert to timezone-aware datetime
    start_datetime = timezone.make_aware(naive_dt)
    card_name = request.POST.get("card-name")
    card_number = request.POST.get("cn")
    if all([s_time, date, naive_dt, card_name, card_number]):
        print("hey Debug statement")
    Booking.objects.filter(customer=request.user, status=Booking.STATUS_PENDING, booking_start_datetime=start_datetime).update(
        name_on_the_card=card_name,
        card_number=card_number,
    )
    return redirect("/")


@login_required
def post_review(request, Restaurant_name):
    print(request.method)
    if request.method == "GET":
        print(Restaurant_name, "RESTAURANT NAME get")  # Debug print
    if request.method == "POST":
        print(Restaurant_name, "RESTAURANT NAME")  # Debug print
        rating = request.POST.get("rating")
        text = request.POST.get("text")
        # Validate data
        if not rating:
            return JsonResponse({"success": False, "error": "Rating required"})
        
        # Save review to your model
        restaurant = Restaurant.objects.get(name=Restaurant_name.replace("_", " "))
        Review.objects.create(
            restaurant=restaurant,
            user=request.user,
            rating=rating,
            comment=text,
            on_display=False
        )
        print(type(Restaurant_name), "HOYE HOYE")

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request method"})



# from django.http import JsonResponse
from django.utils.dateparse import parse_date
# from .models import Booking
# from Restaurants.models import Restaurant

def get_unavailable_tables(request):
    restaurant_name = request.GET.get("restaurant")
    date_str = request.GET.get("date")
    print(restaurant_name, date_str, "PARAMS")  # Debug print

    if not restaurant_name or not date_str:
        return JsonResponse({"error": "Missing params"}, status=400)

    restaurant = Restaurant.objects.get(name=restaurant_name.replace("_", " "))
    selected_date = parse_date(date_str)

    # Get bookings for that restaurant + date
    bookings = Booking.objects.filter(
        restaurant=restaurant,
        booking_start_datetime__date=selected_date,
        status=Booking.STATUS_PENDING
    ).prefetch_related('tables')

    # Collect booked table IDs
    booked_table_ids = set()
    for booking in bookings:
        for table in booking.tables.all():
            booked_table_ids.add(table.id)

    return JsonResponse({
        "booked_tables": list(booked_table_ids)
    })


def cancel_booking(request, booking_id):
    if not request.user.is_authenticated:
        return redirect("login")

    booking = Booking.objects.filter(id=booking_id, customer=request.user).first()
    if booking.status == Booking.STATUS_PENDING:
        booking.status = Booking.STATUS_CANCELLED
        booking.save()
    return redirect("profile")