from django import forms

from .models import *


class CouponForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Coupon
        fields = "__all__"
