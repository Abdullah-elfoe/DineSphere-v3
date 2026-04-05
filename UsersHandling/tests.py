from django.test import TestCase
from .models import User, CustomerProfile

class UserModelTest(TestCase):

    def setUp(self):
        # Create CUSTOMER user
        self.customer = User.objects.create_user(
            username='customer1',
            email='customer@test.com',
            password='pass1234',
            role='CUSTOMER',
            phone='1234567890'
        )

        self.customer_profile = CustomerProfile.objects.create(
            user=self.customer,
            tier='BLUE',
            total_spent=500.00,
            total_reservations=3
        )

        # Create OWNER user
        self.owner = User.objects.create_user(
            username='owner1',
            email='owner@test.com',
            password='pass1234',
            role='OWNER',
            phone='9876543210'
        )

    def test_users_created(self):
        self.assertEqual(User.objects.count(), 2)

    def test_customer_role(self):
        self.assertEqual(self.customer.role, 'CUSTOMER')

    def test_owner_role(self):
        self.assertEqual(self.owner.role, 'OWNER')

    def test_customer_profile_created(self):
        self.assertEqual(self.customer_profile.user, self.customer)

    def test_customer_tier(self):
        self.assertEqual(self.customer_profile.tier, 'BLUE')

    def test_password_check(self):
        self.assertTrue(self.customer.check_password('pass1234'))