# from django.test import TestCase
# from datetime import date, time
# from decimal import Decimal
# from .models import TableSize, SeatingType, Restaurant, Table, SpecialDay


# class RestaurantModelsTest(TestCase):

#     def setUp(self):
#         # -------------------------------
#         # Create Table Sizes
#         # -------------------------------
#         self.small_size = TableSize.objects.create(capacity=2, size="Small", price_factor=1.0, additional_charges=5.0)
#         self.medium_size = TableSize.objects.create(capacity=4, size="Medium", price_factor=1.5, additional_charges=10.0)

#         # -------------------------------
#         # Create Seating Types
#         # -------------------------------
#         self.indoor = SeatingType.objects.create(name="Indoor")
#         self.outdoor = SeatingType.objects.create(name="Outdoor")

#         # -------------------------------
#         # Create a Restaurant
#         # -------------------------------
#         self.restaurant = Restaurant.objects.create(
#             name="Kaboom Bistro",
#             title="Best Bistro in Town",
#             city="Metropolis",
#             address="123 Food St",
#             default_opening_hour=time(18,0),
#             default_closing_hour=time(23,0),
#             slot_duration_minutes=60,
#             cool_down=15
#         )
#         self.restaurant.seating_types.add(self.indoor, self.outdoor)

#         # -------------------------------
#         # Create Tables
#         # -------------------------------
#         self.table1 = Table.objects.create(
#             restaurant=self.restaurant,
#             name="T1",
#             table_size=self.small_size,
#             seating_type=self.indoor,
#             base_price=100
#         )
#         self.table2 = Table.objects.create(
#             restaurant=self.restaurant,
#             name="T2",
#             table_size=self.medium_size,
#             seating_type=self.outdoor,
#             base_price=200
#         )

#         # -------------------------------
#         # Create Special Day
#         # -------------------------------
#         self.special_day = SpecialDay.objects.create(
#             restaurant=self.restaurant,
#             date=date.today(),
#             closed_full_day=False,
#             adjusted_opening_hour=17,
#             adjusted_closing_hour=22
#         )

#     # -------------------------------
#     # TableSize Tests
#     # -------------------------------
#     def test_table_size_str_and_price(self):
#         self.assertEqual(str(self.small_size), "Small (2 seats)")
#         self.assertEqual(self.small_size.calculate_price(100), Decimal('105.0'))  # 100*1 + 5
#         self.assertEqual(self.medium_size.calculate_price(200), Decimal('310.0'))  # 200*1.5 + 10

#     # -------------------------------
#     # SeatingType Tests
#     # -------------------------------
#     def test_seating_type_str(self):
#         self.assertEqual(str(self.indoor), "Indoor")

#     # -------------------------------
#     # Restaurant Tests
#     # -------------------------------
#     def test_restaurant_creation(self):
#         self.assertEqual(self.restaurant.name, "Kaboom Bistro")
#         self.assertIn(self.indoor, self.restaurant.seating_types.all())
#         self.assertIn(self.outdoor, self.restaurant.seating_types.all())

#     # -------------------------------
#     # Table Tests
#     # -------------------------------
#     def test_table_creation_and_properties(self):
#         self.assertEqual(self.table1.capacity, 2)
#         self.assertEqual(self.table1.size, "Small")
#         self.assertTrue(self.table1.is_available)
#         self.assertEqual(self.table1.calculate_price(), Decimal('105.0'))

#         self.assertEqual(self.table2.capacity, 4)
#         self.assertEqual(self.table2.size, "Medium")
#         self.assertEqual(self.table2.calculate_price(), Decimal('310.0'))

#     def test_table_uniqueness_per_restaurant(self):
#         from django.db import IntegrityError
#         with self.assertRaises(IntegrityError):
#             Table.objects.create(
#                 restaurant=self.restaurant,
#                 name="T1",  # duplicate name
#                 table_size=self.small_size
#             )

#     # -------------------------------
#     # SpecialDay Tests
#     # -------------------------------
#     def test_special_day_creation(self):
#         self.assertEqual(str(self.special_day), f"{self.restaurant.name} - {date.today()}")
#         self.assertFalse(self.special_day.closed_full_day)
#         self.assertEqual(self.special_day.adjusted_opening_hour, 17)
#         self.assertEqual(self.special_day.adjusted_closing_hour, 22)

#     # -------------------------------
#     # Relationships Tests
#     # -------------------------------
#     def test_table_restaurant_relationship(self):
#         self.assertEqual(self.table1.restaurant, self.restaurant)
#         self.assertIn(self.table1, self.restaurant.tables.all())
#         self.assertIn(self.table2, self.restaurant.tables.all())

#     def test_table_seating_type_relationship(self):
#         self.assertEqual(self.table1.seating_type, self.indoor)
#         self.assertEqual(self.table2.seating_type, self.outdoor)

#     def test_tables_by_size_query(self):
#         small_tables = Table.objects.filter(table_size__size="Small")
#         self.assertIn(self.table1, small_tables)
#         self.assertNotIn(self.table2, small_tables)

#     def test_available_tables_count(self):
#         available_count = self.restaurant.tables.filter(is_available=True).count()
#         self.assertEqual(available_count, 2)

#         # mark one unavailable
#         self.table1.is_available = False
#         self.table1.save()
#         available_count = self.restaurant.tables.filter(is_available=True).count()
#         self.assertEqual(available_count, 1)



"""
What This Test Suite Covers
1. TableSize
String representation, price calculation with price_factor and additional_charges.
2. SeatingType
String representation.
3. Restaurant
Creation, seating types assignment.
4. Table
Capacity and size properties, price calculation, uniqueness constraint, availability.
5. SpecialDay
Creation, adjusted hours, string representation.
6. Relationships
Table → Restaurant, Table → SeatingType.
7. Queries
Filter tables by size, check available tables count.
"""


from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import time

from Restaurants.models import Restaurant, ReviewSummary
from UsersHandling.models import RestaurantStaff
from Restaurants.services import create_restaurant_for_user

User = get_user_model()


class RestaurantServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="pass123",
            role="CUSTOMER"
        )

        self.valid_data = {
            "name": "Test Restaurant",
            "title": "Best Food",
            "city": "Karachi",
            "opening_hour": time(18, 0),
            "closing_hour": time(23, 0),
        }

    def log(self, message):
        """Helper to print a beautifully marked log."""
        print("\n" + "=" * 60)
        print(f"🚀 {message}")
        print("=" * 60 + "\n")

    def test_customer_becomes_owner_on_first_restaurant(self):
        self.log("TEST 1: Customer signs up and creates first restaurant (should become OWNER)")

        restaurant = create_restaurant_for_user(self.user, self.valid_data)
        self.user.refresh_from_db()

        print(f"User role after first restaurant creation: {self.user.role}")
        print(f"Restaurant created: {restaurant.name}")
        print(f"RestaurantStaff entry exists: {RestaurantStaff.objects.filter(user=self.user, restaurant=restaurant, role='OWNER').exists()}")

        assert self.user.role == "OWNER"
        assert RestaurantStaff.objects.filter(user=self.user, restaurant=restaurant, role="OWNER").exists()
        self.log("TEST 1 done ✅ Customer successfully upgraded to OWNER and restaurant created")

    def test_owner_can_create_multiple_restaurants(self):
        self.log("TEST 2: Owner creates second restaurant (role should remain OWNER)")

        # First restaurant
        create_restaurant_for_user(self.user, self.valid_data)

        # Second restaurant
        data2 = self.valid_data.copy()
        data2["name"] = "Second Restaurant"
        restaurant2 = create_restaurant_for_user(self.user, data2)
        self.user.refresh_from_db()

        print(f"User role after second restaurant: {self.user.role}")
        print(f"Second restaurant created: {restaurant2.name}")
        print(f"Total OWNER entries in RestaurantStaff: {RestaurantStaff.objects.filter(user=self.user, role='OWNER').count()}")

        assert self.user.role == "OWNER"
        assert RestaurantStaff.objects.filter(user=self.user, role="OWNER").count() == 2
        self.log("TEST 2 done ✅ Owner successfully added second restaurant without role change")

    def test_restaurant_is_created(self):
        self.log("TEST 3: Verify restaurant is actually created")
        restaurant = create_restaurant_for_user(self.user, self.valid_data)
        print(f"Total restaurants in DB: {Restaurant.objects.count()}")
        print(f"Created restaurant name: {restaurant.name}")

        assert Restaurant.objects.count() == 1
        assert restaurant.name == "Test Restaurant"
        self.log("TEST 3 done ✅ Restaurant creation verified")

    def test_review_summary_created(self):
        self.log("TEST 4: Verify ReviewSummary is auto-created")
        restaurant = create_restaurant_for_user(self.user, self.valid_data)
        exists = ReviewSummary.objects.filter(restaurant=restaurant).exists()
        print(f"ReviewSummary exists: {exists}")

        assert exists
        self.log("TEST 4 done ✅ ReviewSummary created successfully")

    def test_restaurant_always_has_owner(self):
        self.log("TEST 5: Ensure Restaurant always has an OWNER")
        restaurant = create_restaurant_for_user(self.user, self.valid_data)
        staff_entry = RestaurantStaff.objects.filter(restaurant=restaurant, role="OWNER").first()
        print(f"Owner of restaurant {restaurant.name}: {staff_entry.user.username}")

        assert staff_entry is not None
        assert staff_entry.user == self.user
        self.log("TEST 5 done ✅ Restaurant ownership confirmed")

    def test_multiple_users_have_separate_ownership(self):
        self.log("TEST 6: Multiple users creating restaurants")
        user2 = User.objects.create_user(
            username="user2",
            email="user2@test.com",
            password="pass123",
            role="CUSTOMER"
        )

        res1 = create_restaurant_for_user(self.user, self.valid_data)
        data2 = self.valid_data.copy()
        data2["name"] = "User2 Restaurant"
        res2 = create_restaurant_for_user(user2, data2)

        count_user1 = RestaurantStaff.objects.filter(user=self.user).count()
        count_user2 = RestaurantStaff.objects.filter(user=user2).count()
        print(f"{self.user.username} owns {count_user1} restaurant(s)")
        print(f"{user2.username} owns {count_user2} restaurant(s)")

        assert count_user1 == 1
        assert count_user2 == 1
        self.log("TEST 6 done ✅ Multi-user ownership isolation confirmed")

    def test_missing_required_fields_raises_error(self):
        self.log("TEST 7: Missing required fields should raise KeyError")
        bad_data = {
            "title": "No Name Restaurant",
            "city": "Karachi",
            "opening_hour": time(18, 0),
            "closing_hour": time(23, 0),
        }
        try:
            create_restaurant_for_user(self.user, bad_data)
        except KeyError as e:
            print(f"Caught expected KeyError: {e}")
        else:
            assert False, "Expected KeyError not raised"

        self.log("TEST 7 done ✅ KeyError raised as expected for missing fields")

    def test_role_not_overwritten_unnecessarily(self):
        self.log("TEST 8: Role should not be overwritten unnecessarily")
        create_restaurant_for_user(self.user, self.valid_data)

        # simulate weird state
        self.user.role = "OWNER"
        self.user.save()

        create_restaurant_for_user(self.user, self.valid_data)
        self.user.refresh_from_db()
        print(f"User role after creating second restaurant: {self.user.role}")

        assert self.user.role == "OWNER"
        self.log("TEST 8 done ✅ Role unchanged as expected for existing OWNER")