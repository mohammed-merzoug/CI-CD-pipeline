from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Category, Product
from .models import Order, OrderItem


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='orderuser', password='TestPass123!'
        )
        self.category = Category.objects.create(name="OrderCategory")
        self.product = Product.objects.create(
            category=self.category,
            name="Order Product",
            slug="order-product",
            description="Product for order test",
            price=50.00,
            stock=5,
            available=True
        )
        self.order = Order.objects.create(
            user=self.user,
            shipping_full_name="John Doe",
            shipping_phone="0600000000",
            shipping_address_line1="1 Rue de la Paix",
            shipping_city="Paris",
            shipping_postal_code="75001",
            total_amount=50.00
        )

    def test_order_creation(self):
        self.assertIsNotNone(self.order.order_number)
        self.assertEqual(self.order.status, "pending")

    def test_order_str(self):
        self.assertIn("Commande", str(self.order))

    def test_order_item_creation(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=50.00,
            quantity=1
        )
        self.assertEqual(item.quantity, 1)
        self.assertEqual(float(item.get_cost()), 50.00)


class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='viewuser', password='TestPass123!'
        )

    def test_order_list_requires_login(self):
        response = self.client.get(reverse('orders:order_list'))
        self.assertIn(response.status_code, [302, 403])

    def test_authenticated_user_can_view_orders(self):
        self.client.login(username='viewuser', password='TestPass123!')
        response = self.client.get(reverse('orders:order_list'))
        self.assertEqual(response.status_code, 200)

    def test_order_create_page_loads(self):
        self.client.login(username='viewuser', password='TestPass123!')
        response = self.client.get(reverse('orders:order_create'))
        self.assertIn(response.status_code, [200, 302])
