from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from ..models import *

class NotificationTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        body = {
            "username": "newvendor",
            "password": "12345678",
            "email": "newvendor@vendor.com",
            "firstname": "my",
            "lastname": "vendor",
            "phonenumber": "+905517217180",
            "address": {
                "title": "main address",
                "address": "adkmakdksadsakdsaldad",
                "name": "umut",
                "surname": "oksuz",
                "city": "İstanbul",
                "province": "Sarıyer",
                "country": "Türkiye",
                "phone": {
                    "country_code": "+90",
                    "number": "+90551727180"
                },
                "zip_code": "34347"
            }
        }
        response = self.client.post(reverse('vendor_signup'), body, 'json')
        self.u = User.objects.filter(username="newvendor").first()
        self.v = Vendor.objects.filter(user=self.u).first()
        self.c = Category.objects.create(id=4, name="Clothing")
        self.b = Brand.objects.create(id=1, name="Mavi")
        self.s = Subcategory.objects.create(id=10, category = self.c, name="Men's Fashion")
        self.s2 = Subcategory.objects.create(id=11, category = self.c, name="Sports")
        p1 = Product.objects.create(id=10, name = "Mavi T-shirt", price = 799.9, discount= 0.1,
            creation_date = "2019-08-20T07:22:34Z", total_rating = 4, 
            rating_count = 20, stock_amount = 10, short_description = "yaza özel", subcategory = self.s, brand = self.b, vendor = self.v)
        body = {
            'username': 'newvendor',
            'password': '12345678'
        }
        response = self.client.post(reverse('login'), body, 'json')
        token = response.data["user"]["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        self.c_user =  User.objects.create(id = 2, email="customer@mailcom", password_hash="", password_salt="", google_register=False,is_verified=False, role=1,username="mycustomer")
        self.customer = Customer.objects.create(user = self.c_user, first_name= "customer", last_name = "user")
        product_list = ProductList.objects.create(user = self.c_user, name="I will buy !!")
        ProductListItem.objects.create(product=p1, product_list=product_list)


    def test_price_change_notification(self):
        body = {
            "id": 10,
            "name": "Los Angeles Lakers Old School v3",
            "price": 799.9,
            "stock_amount": 450,
            "short_description": "Sarı mor içsaha forması LA LAKERS",
            "long_description": "anoacnancacnoewcnwocnoınvroeı3vnoıwvnroeıvnıoernvoernvoernvoıenvoıernvoerınvıernvoıernvoıernvroeınvoıernvorıenvoeırnvoıernvoıernvenvoernvoıernverı",
            "discount": 0.18,
            "brand_id": 1,
            "subcategory_id": 11,
            "images": [],
            "image_urls_delete": []
        }
        response = self.client.put(reverse('vendor_product'), body, 'json')
        notification = Notification.objects.filter(user=self.c_user).first()
        self.assertNotEqual(notification, None)