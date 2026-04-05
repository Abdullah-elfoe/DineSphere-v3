from django.utils import timezone
from datetime import timedelta, datetime, time
from django.db import transaction
from .utils import group_tables_by_seating
from django.utils.dateparse import parse_date, parse_time
from Restaurants.models import Table, SpecialDay, Restaurant
from .models import Booking  


LOCK_DURATION_MINUTES = 5


def check_special_day(restaurant, date):
    """
    Validate if restaurant is open on selected date.

    Raises:
        Exception if closed
    """
    special = SpecialDay.objects.filter(
        restaurant=restaurant,
        date=date
    ).first()

    if special and special.closed_full_day:
        raise Exception("Restaurant is closed on selected date")

    return special


def get_available_tables(restaurant, date, start_time, end_time):
    """
    Returns available tables excluding:
    - already booked tables
    - locked tables

    Lock logic:
        Any table locked within last 5 minutes is unavailable
    """
    now = timezone.now()

    booked_tables = Booking.objects.filter(
        restaurant=restaurant,
        date=date,
        start_time__lt=end_time,
        end_time__gt=start_time,
        is_confirmed=True
    ).values_list('tables__id', flat=True)

    locked_tables = Booking.objects.filter(
        locked_at__gte=now - timedelta(minutes=LOCK_DURATION_MINUTES),
        is_confirmed=False
    ).values_list('tables__id', flat=True)

    return Table.objects.filter(
        restaurant=restaurant,
        is_available=True
    ).exclude(id__in=booked_tables).exclude(id__in=locked_tables)


@transaction.atomic
def lock_tables(user, restaurant, tables, date, start_time, end_time):
    """
    Lock selected tables for 5 minutes.

    This prevents race conditions.

    Returns:
        booking instance (temporary)
    """
    now = timezone.now()

    # Re-check availability inside transaction (IMPORTANT)
    available_tables = get_available_tables(restaurant, date, start_time, end_time)
    available_ids = set(available_tables.values_list('id', flat=True))

    for table in tables:
        if table.id not in available_ids:
            raise Exception(f"Table {table.name} just got booked!")

    booking = Booking.objects.create(
        user=user,
        restaurant=restaurant,
        date=date,
        start_time=start_time,
        end_time=end_time,
        locked_at=now,
        is_confirmed=False
    )

    booking.tables.set(tables)
    return booking


def calculate_booking_price(tables, duration_hours):
    """
    Calculate total booking price.

    Includes:
    - table price
    - duration multiplier
    """
    total = 0

    for table in tables:
        table_price = table.calculate_price()
        total += table_price * duration_hours

    return total


def confirm_booking(booking):
    """
    Final confirmation of booking.

    After confirmation:
    - Lock removed
    - Booking becomes permanent
    """
    booking.is_confirmed = True
    booking.locked_at = None
    booking.save()

    return booking



def create_booking(request, Restaurant_name):
    # Fetch form data
    date_str = request.POST.get("date")  # 'YYYY-MM-DD'
    start_time_str = request.POST.get("start_time")  # 'HH:MM'
    duration = int(request.POST.get("end_time", 0))  # convert to int safely
    price = request.POST.get("price")
    table_ids = request.POST.getlist("table_ids")

    # Get restaurant object
    restaurant = Restaurant.objects.get(name=Restaurant_name)

    # Combine date + time and make timezone-aware
    naive_start = datetime.strptime(f"{date_str.strip()} {start_time_str.strip()}", "%Y-%m-%d %H:%M")
    start_datetime = timezone.make_aware(naive_start, timezone.get_current_timezone())

    # Calculate end datetime
    end_datetime = start_datetime + timedelta(hours=duration)

    # Create booking
    booking = Booking.objects.create(
        restaurant=restaurant,
        booking_start_datetime=start_datetime,
        booking_end_datetime=end_datetime,
        customer=request.user
    )

    # Set tables
    booking.tables.set(table_ids)

    # Calculate total price
    booking.total_price = sum(table.calculate_price() for table in booking.tables.all())
    booking.save()

    # Render checkout
    return  {
        "price": price,
        "name": restaurant.name,
        "start_time": start_time_str,
        "end_time": end_datetime.strftime("%H:%M"),
        "date": date_str,
        "tables": booking.tables.all()
    }


def mark_todays_booked_tables_unavailable(restaurant):
    """
    Fetches all of today's bookings for a given restaurant and marks
    all tables in those bookings as unavailable.
    
    Args:
        restaurant (Restaurant): Restaurant instance.
    
    Returns:
        int: Number of tables updated
    """

    # Get current timezone-aware now
    now = timezone.localtime(timezone.now())
    today_start = datetime.combine(now.date(), time.min)  # 00:00 today
    today_end = datetime.combine(now.date(), time.max)    # 23:59:59.999999 today

    # Make them timezone-aware if needed
    today_start = timezone.make_aware(today_start, timezone.get_current_timezone())
    today_end = timezone.make_aware(today_end, timezone.get_current_timezone())

    # Fetch today's bookings for this restaurant
    todays_bookings = Booking.objects.filter(
        restaurant=restaurant,
        booking_start_datetime__lte=today_end,
        booking_end_datetime__gte=today_start,
        status=Booking.STATUS_PENDING  # Only pending bookings occupy tables
    )

    # Collect all tables in these bookings
    tables_to_update = Table.objects.filter(bookings__in=todays_bookings).distinct()

    # Bulk update availability
    updated_count = tables_to_update.update(is_available=False)

    return updated_count



def view_all_booking(restaurant: Restaurant, date_str=None, start_time_str=None, end_time_str=None):
    """
    Fetch available tables for a restaurant, optionally filtering by date/time.
    
    Args:
        restaurant (Restaurant): Restaurant instance
        date_str (str, optional): 'YYYY-MM-DD'
        start_time_str (str, optional): 'HH:MM'
        end_time_str (str, optional): 'HH:MM'
    
    Returns:
        dict: Contains restaurant and tables data
    """

    # Reset availability and mark booked tables
    restaurant.tables.update(is_available=True)
    mark_todays_booked_tables_unavailable(restaurant)

    available_tables = restaurant.tables.filter(is_available=True)

    if date_str and start_time_str and end_time_str:
        # Parse strings into Python objects
        try:
            date = parse_date(date_str)
            start_time = parse_time(start_time_str)
            end_time = parse_time(end_time_str)

            # Check if restaurant is open on that date
            check_special_day(restaurant, date)

            # Filter tables that are available for the given date/time
            available_tables = get_available_tables(restaurant, date, start_time, end_time)

        except Exception as e:
            # Return empty tables and error for view to handle
            return {
                "restaurant": restaurant,
                "tables": {},
                "selected_date": date_str,
                "start_time": start_time_str,
                "end_time": end_time_str,
                "error": str(e)
            }

    # Group tables by seating type
    grouped = group_tables_by_seating(available_tables)
    tables_data = {
        key: [
            {"id": t.id, "name": t.name, "capacity": t.capacity, "price": float(t.calculate_price())}
            for t in value
        ]
        for key, value in grouped.items()
    }

    return {
        "restaurant": restaurant,
        "tables": tables_data,
        "selected_date": date_str,
        "start_time": start_time_str,
        "end_time": end_time_str
    }