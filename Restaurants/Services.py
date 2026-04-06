from .models import Restaurant, ReviewSummary
from UsersHandling.models import RestaurantStaff, User
from django.db.models import ForeignKey, ManyToManyField, BooleanField, FileField, IntegerField, Count
from Reservations.models import Booking
from django.db.models import Sum, Count, Q

from .forms import *
def create_restaurant(data):
    restaurant = Restaurant.objects.create(
        name=data["name"],
        title=data["title"],
        image=data.get("image"),
        about_restaurant=data.get("about"),
        city=data["city"],
        address=data.get("address", "Earth - The only known habitable planet"),
        phone_number=data.get("phone"),
        cool_down=data.get("cooldown", 30),
        default_opening_hour=data["opening_hour"],
        default_closing_hour=data["closing_hour"],
        slot_duration_minutes=data.get("slot_duration", 60),
        allow_advance_booking_days=data.get("advance_days", 30),
        fb_link=data.get("fb_link"),
        website_link=data.get("web_link"),
        is_approved=False
    )

    # Create review summary
    ReviewSummary.objects.create(restaurant=restaurant)

    # ManyToMany seating types
    if data.get("seating_types"):
        restaurant.seating_types.set(data["seating_types"])

    return restaurant



def create_restaurant_for_user(user, data):
    # Step 1: Create restaurant
    restaurant = create_restaurant(data)

    # Step 2: Check if user already owner
    is_already_owner = RestaurantStaff.objects.filter(
        user=user,
        role="OWNER"
    ).exists()

    # Step 3: Assign ownership
    RestaurantStaff.objects.create(
        user=user,
        restaurant=restaurant,
        role="OWNER"
    )

    # Step 4: Upgrade only if first time
    if not is_already_owner:
        user.role = "OWNER"
        user.save()
    
    return restaurant


"""Services that are called from business dashboard direclty"""

# -------------------------------
# Add Table
# -------------------------------
def add_table(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)

    if request.method == 'POST':
        form = TableForm(request.POST, restaurant=restaurant)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.restaurant = restaurant
            obj.save()
    else:
        form = TableForm(restaurant=restaurant)

    return form, form.is_bound and form.is_valid()


# -------------------------------
# Add Table Size (TableType)
# -------------------------------
def add_tabletype(request, restaurant=None):
    # restaurant not needed, but kept for consistency

    if request.method == 'POST':
        form = TableSizeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TableSizeForm()

    return form, form.is_bound and form.is_valid()


# -------------------------------
# Add Seating Type (optional but useful)
# -------------------------------
def add_seating_type(request, restaurant=None):
    if request.method == 'POST':
        form = SeatingTypeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = SeatingTypeForm()

    return form, form.is_bound and form.is_valid()


# -------------------------------
# Add Holiday / Special Day
# -------------------------------
def add_holiday(request, restaurant):
    if request.method == 'POST':
        form = SpecialDayForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.restaurant = restaurant
            obj.save()
    else:
        form = SpecialDayForm()

    return form, form.is_bound and form.is_valid()


# -------------------------------
# Add Restaurant
# -------------------------------
def add_restaurant(request, restaurant=None):
    # restaurant param unused, just for consistent signature

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = RestaurantForm()

    return form, form.is_bound and form.is_valid()



def perform_dynamic_update(instance, data):
    field_dict = {f.name: f for f in instance._meta.get_fields() if not f.auto_created}
    
    for key, value in data.items():
        if key == 'id' or key not in field_dict:
            continue
            
        field = field_dict[key]

        # ❌ NEW: Skip Image/File fields in JSON updates
        # JSON cannot send files; it only sends the path/filename as a string.
        # Assigning a string to an ImageField breaks Django's save() method.
        if isinstance(field, FileField):
            continue

        if isinstance(field, IntegerField):
            if value in ['', 'None', None]:
                value = None

        # 1. Many-to-Many
        if isinstance(field, ManyToManyField):
            if isinstance(value, list):
                getattr(instance, key).set(value)
            elif isinstance(value, str):
                ids = [v.strip() for v in value.split(',') if v.strip()]
                getattr(instance, key).set(ids)
            continue 

        # 2. Foreign Keys
        if isinstance(field, ForeignKey) and value:
            related_model = field.remote_field.model
            try:
                value = related_model.objects.get(id=value)
            except (related_model.DoesNotExist, ValueError):
                continue

        # 3. Booleans
        if isinstance(field, BooleanField):
            value = str(value).lower() in ['true', 'on', '1', 'yes']

        # 4. Standard Assignment (only if value isn't empty for numeric fields)
        if value is not None:
            setattr(instance, key, value)
    
    instance.save()
    return instance



def getAnalytics(restaurant_id):
    customers = User.objects.filter(
        bookings__restaurant_id=restaurant_id
    ).distinct()
    
    total_customers = customers.count()

    # 2. Group by gender
    gender_counts = customers.values('gender').annotate(count=Count('id'))
    
    # Initialize counts
    male_count = 0
    female_count = 0
    other_count = 0

    for entry in gender_counts:
        if entry['gender'] == 'M':
            male_count = entry['count']
        elif entry['gender'] == 'F':
            female_count = entry['count']
        else:
            other_count += entry['count']

    # 3. Calculate Percentages for the SVG (Avoid division by zero)
    female_percent = (female_count / total_customers * 100) if total_customers > 0 else 0
    male_percent = (male_count / total_customers * 100) if total_customers > 0 else 0

    order_stats = Booking.objects.filter(restaurant_id=restaurant_id).aggregate(
        pending_count=Count('id', filter=Q(status__iexact='pending')),
        finished_count=Count('id', filter=Q(status__iexact='finished')),
        cancelled_count=Count('id', filter=Q(status__iexact='cancelled')),
        total_bookings=Count('id')
    )

    # 2. Calculate Total Revenue
    # Revenue only comes from FINISHED bookings.
    # Note: If your price logic is complex (properties/methods), 
    # we usually store the "final_price" on the Booking model at time of completion.
    # If you don't have a 'total_price' field on Booking, you'll need to sum the 
    # base_price of the related tables:
    
    revenue_data = Booking.objects.filter(
        restaurant_id=restaurant_id, 
        status__iexact='finished'
    ).aggregate(
        total_revenue=Sum('total_price') # Or 'total_price' if you added that field
    )

    context = {
        
        
    }
    print(order_stats)

    return {
        'total_customers': total_customers,
        'female_count': female_count,
        'male_count': male_count,
        'other_count': other_count,
        'female_percent': round(female_percent),
        'male_percent': round(male_percent),
        'revenue': revenue_data['total_revenue'] or 0,
        'stats': order_stats,
    }


def isStaff(user):
    return RestaurantStaff.objects.filter(
        user=user,
        role="STAFF"
    ).exists()


def getForm(tab:str, data=None):

    match tab.lower():
        case "seatingtype":
            return SeatingTypeForm(data=data)
        case "tablesize":
            return TableSizeForm(data=data)
        case _:
            raise ValueError("Invalid tab name")
        


from django.http import JsonResponse

def get_items(request):
    item_type = request.GET.get('type', '').lower()
    items = []

    try:
        if item_type == 'seatingtype':
            data = SeatingType.objects.all()
            # SeatingType only has 'name'
            items = [{'primary': obj.name, 'secondary': 'Area Type'} for obj in data]
            
        elif item_type == 'tablesize':
            data = TableSize.objects.all()
            # TableSize has 'size' and 'capacity'
            items = [
                {
                    'primary': f"{obj.size}" if obj.size else "Standard", 
                    'secondary': f"{obj.capacity} Seats"
                } for obj in data
            ]

        return JsonResponse({'items': items})
    except Exception as e:
        return JsonResponse({'items': [], 'error': str(e)}, status=400)