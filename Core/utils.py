"""
Utility/Helper functions for views.py file.
"""

from Restaurants.models import ReviewSummary



def get_min_price(restaurant):
    """
    Compute the minimum table price for a given restaurant.

    Iterates over all tables associated with the restaurant and calculates
    each table's price using the Table.calculate_price() method.

    Args:
        restaurant (Restaurant): The restaurant instance.

    Returns:
        Decimal | None: The lowest table price if tables exist, otherwise None.
    """

    prices = (table.calculate_price() for table in restaurant.tables.all())
    return min(prices, default=None)


def build_combined(restaurants):
    """
    Build a combined dataset of restaurant details, review summaries,
    and minimum table prices.

    For each restaurant, this function retrieves its associated review
    summary and computes the minimum price across its tables.

    Args:
        restaurants (Iterable[Restaurant]): A list or queryset of restaurants.

    Returns:
        list[tuple]: A list of tuples in the format:
            (Restaurant, ReviewSummary | None, Decimal | None)
    """
    # t = [
    #     (
    #         r,
    #         ReviewSummary.objects.filter(restaurant=r).first(),
    #         get_min_price(r)
    #     )
    #     for r in restaurants
    # ]
    # print(t)

    return [
        (
            r,
            ReviewSummary.objects.filter(restaurant=r).first(),
            # If you want to uncomment this feature than handle the template accordingly, cuz then there would be 3 things to unpack now there are 2
            get_min_price(r)
        )
        for r in restaurants
    ]


