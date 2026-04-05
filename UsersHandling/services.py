from .models import User, CustomerProfile, RestaurantStaff

def create_customer_user(username, email, password, dob=None, gender=None, image=None):
    if User.objects.filter(username=username).exists():
        raise ValueError("Username already taken")

    if User.objects.filter(email=email).exists():
        raise ValueError("Email already exists")

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role='CUSTOMER'  # 🔒 FORCE ROLE
    )

    user.date_of_birth = dob
    user.gender = gender
    user.image = image
    user.save()

    # create customer profile automatically
    CustomerProfile.objects.create(user=user)

    return user



def add_staff(owner_user, email, restaurant):
    is_owner = RestaurantStaff.objects.filter(
        user=owner_user,
        restaurant=restaurant,
        role='OWNER'
    ).exists()

    if not is_owner:
        raise PermissionError("Only owner can add staff")

    user = User.objects.get(email=email)
    
    RestaurantStaff.objects.create(
        user=user,
        restaurant=restaurant,
        role='STAFF'
    )

    return user


