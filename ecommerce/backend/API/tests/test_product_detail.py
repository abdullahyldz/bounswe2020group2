import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from API.models import Product, Category, Subcategory, User, Vendor, Brand
from API.serializers.product_serializer import ProductSerializer
from API.views.product import product_detail

client = Client()
product_id_for_test = 1

class ProductDetail(TestCase):
    def setUp(self):
        c = Category.objects.create(id=4, name="Clothing")
        s = Subcategory.objects.create(id=10, category = c, name="Men's Fashion")
        b = Brand.objects.create(id=1, name="Mavi")
        u = User.objects.create(id=1, username="omer", email="omer@gmail.com", role = 2)
        v = Vendor.objects.create(id=1, user = u, first_name="omerfaruk", last_name="deniz")
        Product.objects.create(id=product_id_for_test, name = "Mavi T-shirt", price = 100, 
            creation_date = "2019-08-20T07:22:34Z", image_url = "image_url1", total_rating = 4, 
            rating_count = 20, stock_amount = 10, description = "yaza özel", subcategory = s, brand = b, vendor = v)

    def test_product_detail(self):
        response = client.get(reverse(product_detail, args = [product_id_for_test]))
        product = Product.objects.filter(id = product_id_for_test)
        serializer = ProductSerializer(product, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)