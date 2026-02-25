from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Category, Product


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            slug="test-product",
            description="A test product",
            price=19.99,
            stock=10,
            available=True
        )

    def test_cart_page_loads(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        response = self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 1, 'override': False}
        )
        self.assertIn(response.status_code, [200, 302])

    def test_remove_from_cart(self):
        # Add first then remove
        self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 1, 'override': False}
        )
        response = self.client.post(
            reverse('cart:cart_remove', args=[self.product.id])
        )
        self.assertIn(response.status_code, [200, 302])

    def test_empty_cart_displays(self):
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
