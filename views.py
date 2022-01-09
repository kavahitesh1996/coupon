import datetime

from django.shortcuts import render

from django.http import HttpResponse

from .models import *

from .forms import *


from django.shortcuts import redirect, render, reverse


def index(request):
    return HttpResponse("Hello, Hd")


# def get_all_codes(request):
#     """
#     Return all code with all details.
#     """

#     codes = Coupon.objects.all()

#     return render(
#         request=request, template_name="promocode/codes.html", context={"codes": codes}
#     )


def get_all_redemptions(request):
    """
    Return all code with all details.
    """

    codes = CouponRedemption.objects.all()

    return render(
        request=request,
        template_name="promocode/redemptions.html",
        context={"codes": codes},
    )


# def add_new_code(request):
#     """
#     Add new Code form.
#     """
#     context = {}
#     context["form"] = CouponForm()

#     if request.method == "POST":

#         form = CouponForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("get_all_codes"))
#         else:
#             context["form"] = form
#             return render(request, "promocode/new_code.html", context)

#     return render(request, "promocode/new_code.html", context)


def get_user_data(request):
    """
    Add User Details View.
    """
    context = {}

    if request.POST:
        data = request.POST
        user_id = data.get("user_id")
        birthdate = data.get("birthdate")
        gender = data.get("gender")
        order_amount = data.get("order_amount")
        order_code = data.get("order_code")

        try:
            if User.objects.filter(id=user_id).exists():
                user = User.objects.get(id=user_id)
                profile, created = UserProfile.objects.get_or_create(user=user)
                profile.date_of_birth = datetime.datetime.strptime(birthdate, "%m/%d/%Y")
                profile.gender = gender
                profile.save()
                if not int(order_amount) in range(100, 1500000):
                    context["msg"] = "Order amount must be  between 100 to 1500001"
                    return render(request, "promocode/user_data.html", context)
                redemption_msg = CouponRedemption.add_coupon_redemption(
                    user, order_code, int(order_amount)
                )
                context["msg"] = redemption_msg
                return render(request, "promocode/user_data.html", context)
            else:
                context["msg"] = "User ID does not exist."
                return render(request, "promocode/user_data.html", context)    
        except Exception as e:
            context["msg"] = e.__str__()
            return render(request, "promocode/user_data.html", context)

    return render(request, "promocode/user_data.html", context)
