from .models import Restaurant
from UsersHandling.models import RestaurantStaff

def owner_context(request):
    """
    Injects owner-related data globally into templates
    """

    # Not logged in → nothing
    if not request.user.is_authenticated:
        return {}

    user = request.user

    # Get ONLY OWNER roles for this user
    owner_staff = RestaurantStaff.objects.filter(
        user=user,
        role='OWNER'
    )

    # Get all restaurants owned by this user
    owners_restaurants = Restaurant.objects.filter(
        restaurantstaff__in=owner_staff
    ).distinct()
    # print(len(owners_restaurants), owners_restaurants)

    # Get selected restaurant from session
    selected_id = request.session.get("selected_restaurant_id")
    selected_restaurant = None
    # print(selected_id)
    if selected_id:
        selected_restaurant = owners_restaurants.filter(id=selected_id).first()
    
    # Fallback
    # print(selected_restaurant)
    if not selected_restaurant and len(owners_restaurants) != 0:
        selected_restaurant = owners_restaurants.first()
        selected_id = Restaurant.objects.filter(name=selected_restaurant.name, city=selected_restaurant.city, address=selected_restaurant.address).first().id
        print(selected_restaurant, selected_id)
        request.session.get("selected_restaurant_id")
        request.session['selected_restaurant_id'] = selected_id

    return {
        "CP__OwnerProfile": user,  # keep original user (important)
        "CP__Restaurants": owners_restaurants,
        "CP__Selected": selected_restaurant,
    }