import secrets
from django.contrib.auth.backends import BaseBackend
from django.utils import timezone
from django.http import HttpRequest

from .models import User


class ExpiredCodeException(Exception):
    def __str__(self) -> str:
        return "code is expired"


class InvalidCodeException(Exception):
    def __str__(self) -> str:
        return "code is invalid"


class OTP:
    _DT_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
    _KEY_NAME = "verification_token"
    _DURATION_SECONDS = 120

    def __init__(self, request: HttpRequest) -> None:
        self.session = request.session
        token = self.session.get(self._KEY_NAME, None)
        if not token:
            token = self._make_token()
            self.session[self._KEY_NAME] = token
            self.session.save()

        self._code = token["code"].strip()
        self._expire_at = timezone.datetime.strptime(
            token["expire_at"], self._DT_FORMAT
        )

    @property
    def code(self):
        return self._code

    @property
    def expire_at(self):
        return self._expire_at

    def _generate_code(self):
        alphabets = "0123456789"
        return "".join(secrets.choice(alphabets) for i in range(5))

    def _expire_at(self):
        expire = timezone.now() + timezone.timedelta(seconds=self._DURATION_SECONDS)
        return expire.strftime(self._DT_FORMAT)

    def _make_token(self):
        """
        Returns {code, expire_at}
        """
        return {
            "code": self._generate_code(),
            "expire_at": self._expire_at(),
        }

    def is_expired(self):
        """
        Returns True if timeout is expired
        """
        dt = timezone.now().replace(tzinfo=None)

        return self._expire_at < dt

    def validate_code(self, code):
        return self._code == code.strip()

    def check(self, code):

        if self.is_expired():
            raise ExpiredCodeException()

        if not self.validate_code(code):
            raise InvalidCodeException()

        return True

    def clear(self):
        del self.session[self._KEY_NAME]
        self.session.save()


class OTPAuthenticationBackend(BaseBackend):
    def authenticate(self, request: HttpRequest, phone_num):
        u, _ = User.objects.get_or_create(phone_num=phone_num)
        return u

    def get_user(self, user_id):
        try:
            u = User.objects.get(pk=user_id)
            return u
        except User.DoesNotExist:
            return None
