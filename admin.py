from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "profile"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class CouponForm(forms.ModelForm):
    """Form for adding entitlement support details, exists mostly for testing purposes"""

    def clean(self):
        """
        Validation for Coupon start date
        """
        # form_data = self.cleaned_data
        # if self.instance.id and form_data.get('start_date'):
        #     if timezone.now() > form_data.get('start_date'):
        #         raise ValidationError("You can't change the code after the code start date is started.")
        # return form_data

    class Meta:
        fields = "__all__"
        model = Coupon


class CouponAdmin(admin.ModelAdmin):
    """Admin Interface for Coupon model."""

    form = CouponForm
    list_display = [
        "code",
        "display_gender",
        "start_date",
        "expiration_date",
        "discount",
        "max_discount_amout",
        "number_of_uses",
    ]
    search_fields = ["code"]


class CouponRedemptionAdmin(admin.ModelAdmin):
    """Admin Interface for Coupon model."""

    list_display = ["user", "coupon", "order_amount", "actual_price"]
    search_fields = ["user__username"]


admin.site.register(Coupon, CouponAdmin)
admin.site.register(CouponRedemption, CouponRedemptionAdmin)
