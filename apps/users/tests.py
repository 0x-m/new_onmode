import random
from django.test import TestCase
from django.test.utils import override_settings

from apps.users.models import User


class TestUserRegistration(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.phone_no = "09179912121"
        cls.user = User.objects.create(phone_num=cls.phone_no)

    def test_user_signup_with_invalid_phoneno(self):
        for _ in range(10):
            # create random 11 length string as invalid phone_no
            phone_no = "".join(random.choice("0123456789abcdef-*!@") for _ in range(11))
            resp = self.client.post("/users/signup/", {"phone_number": phone_no})
            self.assertEqual(resp.status_code, 400)

    @override_settings(DEBUG=True)
    def test_user_signup_with_valid_phoneno(self):
        for _ in range(10):
            phone_no = "091" + "".join(random.choice("123456789") for _ in range(8))
            resp = self.client.post("/users/signup/", {"phone_num": phone_no})
            self.assertEqual(resp.status_code, 200)
            self.assertContains(resp, "code")

    @override_settings(DEBUG=True)
    def test_user_signup_with_valid_verification_code(self):
        phone_no = "09174561259"
        resp = self.client.post("/users/signup/", {"phone_num": phone_no})
        self.assertEqual(resp.status_code, 200)

        verification_code = resp.json()[
            "code"
        ]  # Get the verification code from the response
        resp_1 = self.client.post("/users/verify/", {"code": verification_code})
        self.assertRedirects(resp_1, "/")

    @override_settings(DEBUG=True)
    def test_user_signup_with_invalid_verification_code(self):
        phone_no = "09174561259"
        resp = self.client.post("/users/signup/", {"phone_num": phone_no})
        self.assertEqual(resp.status_code, 200)
        resp_1 = self.client.post("/users/verify/", {"code": "avv"})
        self.assertEqual(resp_1.status_code, 400)  # Bad request

    @override_settings(DEBUG=True)
    def test_user_with_valid_phone_login(self):
        resp = self.client.post("/users/signup/", {"phone_num": self.phone_no})
        self.assertEqual(resp.status_code, 200)
        code = resp.json()["code"]
        resp_1 = self.client.post("/users/verify/", {"code": code})
        self.assertRedirects(resp_1, "/")


# WARN: Zarinpay developer api is not working!
# SUG: Use mocking....
class TestUserWallet(TestCase):
    def test_wallet_deposit(self):
        pass

    def test_wallet_withdraw_while_amount_more_than_available_balance(self):
        pass

    def test_wallet_withdraw_while_amount_less_than_available_balance(self):
        pass
