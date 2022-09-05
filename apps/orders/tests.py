from django.test import TestCase
from django.utils import timezone

from catalogue.models import Product, Shop
from promotions.models import Coupon, Discount
from users.models import User


class AddOrderItemTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User(phone_num="09179827587")
        cls.user.save()
        cls.shop = Shop(owner=cls.user, name="abc")
        cls.shop.save()
        cls.product_1 = Product(
            shop=cls.shop, name="product1", price=1500, quantity=10
        )
        cls.product_2 = Product(
            shop=cls.shop, name="product2", price=2500, quantity=10
        )
        cls.product_1.save()
        cls.product_2.save()
        cls.coupon_1 = Coupon
        return super().setUpClass()

    def test_add_existing_product_to_order_with_available_quantity(self):
        self.client.force_login(self.user)
        res = self.client.post("/cart/add", {"product": 1, "quantity": 20})
        self.assertEqual(res.status_code, 400)  # bad requset

    def test_add_existing_product_to_order_with_out_of_range_quantity(self):
        self.client.force_login(self.user)
        res = self.client.post("/cart/add", {"product": 1, "quantity": 2})
        self.assertJSONEqual(
            res.content, {"status": "added", "final_price": 3000}
        )

    def test_add_two_products_to_order(self):
        self.client.force_login(self.user)
        res_1 = self.client.post("/cart/add", {"product": 1, "quantity": 2})
        res_2 = self.client.post("/cart/add", {"product": 2, "quantity": 1})

        self.assertJSONEqual(
            res_1.content, {"status": "added", "final_price": 3000}
        )

        self.assertJSONEqual(
            res_2.content, {"status": "added", "final_price": 5500}
        )

    def test_add_non_existing_product_to_order(self):
        self.client.force_login(self.user)
        res_1 = self.client.post("/cart/add", {"product": 4, "quantity": 2})
        self.assertEqual(res_1.status_code, 400)

    def test_add_discounted_product_to_order(self):
        self.client.force_login(self.user)
        nw = timezone.now()

        discount = Discount(
            percent=10,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=20000,
        )
        discount.save()
        self.product_1.discount = discount
        self.product_1.save()
        discount_2 = Discount(
            percent=50,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=20000,
        )
        discount_2.save()
        self.product_2.discount = discount_2
        self.product_2.save()

        res = self.client.post("/cart/add", {"product": 1, "quantity": 2})
        res_2 = self.client.post("/cart/add", {"product": 2, "quantity": 1})
        self.assertJSONEqual(
            res.content, {"status": "added", "final_price": 2700}
        )

        self.assertJSONEqual(
            res_2.content, {"status": "added", "final_price": 3950}
        )

    def test_add_coupon_to_order(self):
        self.client.force_login(self.user)
        nw = timezone.now()
        discount = Discount(
            percent=10,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=20000,
        )
        discount.save()
        self.product_1.discount = discount
        self.product_1.save()
        discount_2 = Discount(
            percent=50,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=20000,
        )
        discount_2.save()
        self.product_2.discount = discount_2
        self.product_2.save()

        coupon = Coupon(
            type=Coupon.TYPE.PERCENT,
            percent=10,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=10000,
        )
        coupon.save()

        res = self.client.post("/cart/add", {"product": 1, "quantity": 2})
        res_2 = self.client.post("/cart/add", {"product": 2, "quantity": 1})
        res_3 = self.client.post(
            "/cart/coupon/add", {"code": coupon.code, "order_id": 1}
        )
        self.assertJSONEqual(
            res.content, {"status": "added", "final_price": 2700}
        )

        self.assertJSONEqual(
            res_2.content, {"status": "added", "final_price": 3950}
        )
        print(res_3.content)
        self.assertJSONEqual(
            res_3.content, {"status": "set", "final_price": 3555}
        )

    def test_delete_order_item(self):
        self.client.force_login(self.user)
        nw = timezone.now()
        discount = Discount(
            percent=10,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=20000,
        )
        discount.save()
        self.product_1.discount = discount
        self.product_1.save()
        discount_2 = Discount(
            percent=50,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=20000,
        )
        discount_2.save()
        self.product_2.discount = discount_2
        self.product_2.save()

        res = self.client.post("/cart/add", {"product": 1, "quantity": 2})
        res_2 = self.client.post("/cart/add", {"product": 2, "quantity": 1})

        res_3 = self.client.get("/cart/delete/1", {})
        self.assertJSONEqual(
            res.content, {"status": "added", "final_price": 2700}
        )

        self.assertJSONEqual(
            res_2.content, {"status": "added", "final_price": 3950}
        )
        self.assertJSONEqual(
            res_3.content, {"status": "deleted", "final_price": 1250}
        )

    def test_delete_coupon_of_order(self):
        self.client.force_login(self.user)
        nw = timezone.now()
        discount = Discount(
            percent=10,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=20000,
        )
        discount.save()
        self.product_1.discount = discount
        self.product_1.save()
        discount_2 = Discount(
            percent=50,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=20000,
        )
        discount_2.save()
        self.product_2.discount = discount_2
        self.product_2.save()

        coupon = Coupon(
            type=Coupon.TYPE.PERCENT,
            percent=10,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=10000,
        )
        coupon.save()

        res = self.client.post("/cart/add", {"product": 1, "quantity": 2})
        res_2 = self.client.post("/cart/add", {"product": 2, "quantity": 1})
        res_3 = self.client.post(
            "/cart/coupon/add", {"code": coupon.code, "order_id": 1}
        )
        res_4 = self.client.post("/cart/coupon/delete", {"order_id": 1})
        self.assertJSONEqual(
            res.content, {"status": "added", "final_price": 2700}
        )

        self.assertJSONEqual(
            res_2.content, {"status": "added", "final_price": 3950}
        )

        self.assertJSONEqual(
            res_3.content, {"status": "set", "final_price": 3555}
        )
        self.assertJSONEqual(
            res_4.content, {"status": "deleted", "final_price": 3950}
        )

    def test_delete_coupon_and_discount(self):
        self.client.force_login(self.user)
        nw = timezone.now()
        discount = Discount(
            percent=10,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=20000,
        )
        discount.save()
        self.product_1.discount = discount
        self.product_1.save()
        discount_2 = Discount(
            percent=50,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=20000,
        )
        discount_2.save()

        self.product_2.discount = discount_2
        self.product_2.save()

        coupon = Coupon(
            type=Coupon.TYPE.PERCENT,
            percent=10,
            start_date=nw,
            end_date=nw + timezone.timedelta(days=1),
            max_amount=10000,
        )
        coupon.save()

        res = self.client.post("/cart/add", {"product": 1, "quantity": 2})
        res_2 = self.client.post("/cart/add", {"product": 2, "quantity": 1})
        res_3 = self.client.post(
            "/cart/coupon/add", {"code": coupon.code, "order_id": 1}
        )

        self.product_2.discount = None
        self.product_2.save()
        # card is expired so refresh it
        self.client.get("/cart/refresh", {"id": 1})

        res_4 = self.client.post("/cart/coupon/delete", {"order_id": 1})

        self.assertJSONEqual(
            res.content, {"status": "added", "final_price": 2700}
        )

        self.assertJSONEqual(
            res_2.content, {"status": "added", "final_price": 3950}
        )

        self.assertJSONEqual(
            res_3.content, {"status": "set", "final_price": 3555}
        )
        self.assertJSONEqual(
            res_4.content, {"status": "deleted", "final_price": 5200}
        )
