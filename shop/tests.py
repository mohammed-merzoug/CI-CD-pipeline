from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic devices"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Electronics")

    def test_category_slug_auto_generated(self):
        self.assertEqual(self.category.slug, "electronics")

    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            slug="laptop",
            description="A powerful laptop",
            price=999.99,
            stock=10,
            available=True
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(float(self.product.price), 999.99)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Laptop")

    def test_product_category_relationship(self):
        self.assertEqual(self.product.category.name, "Electronics")


class ShopViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Books")
        self.product = Product.objects.create(
            category=self.category,
            name="Python Book",
            slug="python-book",
            description="Learn Python",
            price=29.99,
            stock=5,
            available=True
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('shop:home'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Book")

    def test_product_detail_view(self):
        response = self.client.get(
            reverse('shop:product_detail', args=[self.product.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Book")
