# pip install django-model-utils
# pip install django==2.0

from django.db import models

from django.contrib.auth.models import User, AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from model_utils.models import TimeStampedModel

from django.utils import timezone

# from django.utils.translation import ugettext_lazy as _


DISCOUNT_CHOICES = (("percentage", "Percentage"), ("flat", "Flat"))

GENDER_CHOICES = (("m", "Male"), ("f", "Female"))


class Coupon(TimeStampedModel):
    """
    This table contains coupon codes
    A user can get a discount offer on course if provide coupon code
    """

    class Meta(object):
        app_label = "promocode"

    code = models.CharField(
        max_length=32,
        help_text="Only uppercase letters & numbers are allowed.",
        validators=[
            RegexValidator(
                "^[A-Z0-9]*$", "Only uppercase letters & numbers are allowed."
            )
        ],
    )

    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    start_date = models.DateTimeField()
    expiration_date = models.DateTimeField()

    discount_type = models.CharField(max_length=32, choices=DISCOUNT_CHOICES)

    discount = models.PositiveIntegerField()

    max_discount_amout = models.PositiveIntegerField(
        help_text="This is max amount users will get after the promo code is applied."
    )

    number_of_uses = models.PositiveIntegerField(
        help_text="How many times this coupon will be used.", default=1
    )

    is_active = models.BooleanField(default=True)

    # is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def __enumerable_to_display(self, enumerables, enum_value):
        """Get the human readable value from an enumerable list of key-value pairs."""
        return dict(enumerables)[enum_value]

    @property
    def display_gender(self):
        """
        return coupon gender
        """
        return self.__enumerable_to_display(GENDER_CHOICES, self.gender)


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(
        User,
        unique=True,
        db_index=True,
        related_name="profile",
        on_delete=models.CASCADE,
    )
    date_of_birth = models.DateField(blank=False, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    class Meta(object):
        app_label = "promocode"

    def __str__(self):
        return "{}".format(self.user.username)


class CouponRedemption(TimeStampedModel):
    """
    This table contain coupon redemption info
    """

    class Meta(object):
        app_label = "promocode"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    order_amount = models.PositiveIntegerField()
    actual_price = models.PositiveIntegerField(
        help_text="Order total amount after code redemption applied."
    )

    def __str__(self):
        return "{} - {}".format(self.user.username, self.coupon.code)

    @classmethod
    def add_coupon_redemption(cls, user, coupon, order_amount):
        """
        add coupon info into coupon_redemption model
        """

        if not Coupon.objects.filter(code=coupon, gender=user.profile.gender).exists():
            return "Coupon code does not exist."

        coupon = Coupon.objects.get(code=coupon)

        if (
            timezone.now() > coupon.start_date
            and timezone.now() < coupon.expiration_date
        ):
            if coupon.number_of_uses > 0:
                if not cls.objects.filter(user=user, coupon=coupon).exists():
                    if coupon.discount_type == "percentage":
                        discount_amout = (order_amount * coupon.discount) / 100
                        amount = order_amount - discount_amout
                        # Check Birthdate
                        if timezone.now().date().strftime("%m/%d") == user.profile.date_of_birth.strftime("%m/%d"):
                            amount = amount - (amount * 10) / 100

                        if coupon.max_discount_amout < amount:
                            amount = order_amount - coupon.max_discount_amout
                    else:
                        amount = order_amount - coupon.discount
                    coupon.number_of_uses = coupon.number_of_uses - 1
                    coupon.save()
                    cls.objects.create(
                        user=user,
                        coupon=coupon,
                        order_amount=order_amount,
                        actual_price=amount,
                    )
                    return "{username} is successfully applied this {coupon_code} coupon.".format(
                        username=user.username, coupon_code=coupon.code
                    )
                else:
                    return "User has already used this."
            else:
                return "Coupon code max limit used."
        else:
            return "Coupon code expiried or not activate yet."


    @property
    def discount_amout(self):
        """
        return coupon gender
        """
        return self.order_amount - self.actual_price