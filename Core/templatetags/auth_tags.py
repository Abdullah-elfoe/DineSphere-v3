# Custom template tags for authorization-related checks in Django templates.

from django import template
from UsersHandling.models import RestaurantStaff

register = template.Library()

@register.filter
def is_owner(user):
    return RestaurantStaff.objects.filter(
        user=user,
        role='OWNER'
    ).exists()


@register.filter
def is_staff(user):
    return RestaurantStaff.objects.filter(
        user=user,
        role='STAFF'
    ).exists()