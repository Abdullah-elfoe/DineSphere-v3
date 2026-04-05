from django.test import TestCase
from datetime import datetime, timedelta
from decimal import Decimal
from Restaurants.models import Restaurant, SeatingType, Table, TableSize
from UsersHandling.models import User
from Reservations.models import Booking


class BookingModelTest(TestCase):

    def setUp(self):
        # -------------------------------
        # Create Table Sizes
        # -------------------------------
        self.small_size = TableSize.objects.create(capacity=2, size="Small", price_factor=1.0, additional_charges=5.0)
        self.medium_size = TableSize.objects.create(capacity=4, size="Medium", price_factor=1.5, additional_charges=10.0)

        # -------------------------------
        # Create Seating Types
        # -------------------------------
        self.indoor = SeatingType.objects.create(name="Indoor")
        self.outdoor = SeatingType.objects.create(name="Outdoor")

        # -------------------------------
        # Create Restaurant
        # -------------------------------
        self.restaurant = Restaurant.objects.create(
            name="Kaboom Bistro",
            title="Best Bistro",
            city="Metropolis",
            default_opening_hour="18:00",
            default_closing_hour="23:00"
        )
        self.restaurant.seating_types.add(self.indoor, self.outdoor)

        # -------------------------------
        # Create Tables
        # -------------------------------
        self.table1 = Table.objects.create(
            restaurant=self.restaurant,
            name="T1",
            table_size=self.small_size,
            seating_type=self.indoor,
            base_price=100
        )
        self.table2 = Table.objects.create(
            restaurant=self.restaurant,
            name="T2",
            table_size=self.medium_size,
            seating_type=self.outdoor,
            base_price=200
        )

        # -------------------------------
        # Create a User
        # -------------------------------
        self.user = User.objects.create(username="testuser", email="test@example.com", password="password123")

        # -------------------------------
        # Booking times
        # -------------------------------
        self.start_time = datetime.now() + timedelta(days=1)
        self.end_time = self.start_time + timedelta(hours=2)

    # -------------------------------
    # Test Booking Creation
    # -------------------------------
    def test_booking_creation_and_price(self):
        booking = Booking.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            booking_start_datetime=self.start_time,
            booking_end_datetime=self.end_time,
            card_number="1234123412341234",
            name_on_the_card="John Doe"
        )
        # Assign tables
        booking.tables.set([self.table1, self.table2])
        booking.save()

        # Check relationships
        self.assertEqual(booking.restaurant, self.restaurant)
        self.assertEqual(booking.customer, self.user)
        self.assertIn(self.table1, booking.tables.all())
        self.assertIn(self.table2, booking.tables.all())

        # Check total price calculation
        expected_price = self.table1.calculate_price() + self.table2.calculate_price()
        self.assertEqual(booking.total_price, expected_price)

    # -------------------------------
    # Test Status Transitions
    # -------------------------------
    def test_booking_cancel_and_finish(self):
        booking = Booking.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            booking_start_datetime=self.start_time,
            booking_end_datetime=self.end_time,
            card_number="1234123412341234",
            name_on_the_card="John Doe"
        )
        booking.tables.set([self.table1])
        booking.save()

        # Cancel booking
        booking.cancel()
        self.assertEqual(booking.status, Booking.STATUS_CANCELLED)

        # Attempting to mark finished after cancel should raise error if logic is expanded
        with self.assertRaises(ValueError):
            booking.mark_finished()

        # New booking to mark finished
        booking2 = Booking.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            booking_start_datetime=self.start_time,
            booking_end_datetime=self.end_time,
            card_number="5678567856785678",
            name_on_the_card="Jane Doe"
        )
        booking2.tables.set([self.table2])
        booking2.save()
        booking2.mark_finished()
        self.assertEqual(booking2.status, Booking.STATUS_FINISHED)

    # -------------------------------
    # Test Table Availability Queries
    # -------------------------------
    def test_table_booking_relationship(self):
        booking = Booking.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            booking_start_datetime=self.start_time,
            booking_end_datetime=self.end_time,
            card_number="1234567890123456",
            name_on_the_card="Alice"
        )
        booking.tables.set([self.table1, self.table2])
        booking.save()

        # Check tables reflect the booking
        self.assertIn(booking, self.table1.bookings.all())
        self.assertIn(booking, self.table2.bookings.all())

    # -------------------------------
    # Test Edge Case: No tables assigned
    # -------------------------------
    def test_booking_without_tables(self):
        booking = Booking.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            booking_start_datetime=self.start_time,
            booking_end_datetime=self.end_time,
            card_number="1111222233334444",
            name_on_the_card="Bob"
        )
        booking.save()
        # No tables → total price should be zero
        self.assertEqual(booking.total_price, 0)

    # -------------------------------
    # Test total_price recalculation after table assignment
    # -------------------------------
    def test_total_price_update_after_adding_table(self):
        booking = Booking.objects.create(
            restaurant=self.restaurant,
            customer=self.user,
            booking_start_datetime=self.start_time,
            booking_end_datetime=self.end_time,
            card_number="9999888877776666",
            name_on_the_card="Charlie"
        )
        booking.tables.set([self.table1])
        booking.save()
        price_after_first_table = booking.total_price
        self.assertEqual(price_after_first_table, self.table1.calculate_price())

        # Add another table
        booking.tables.add(self.table2)
        booking.save()
        price_after_second_table = booking.total_price
        expected_total = self.table1.calculate_price() + self.table2.calculate_price()
        self.assertEqual(price_after_second_table, expected_total)