from django.urls import path

from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    # path("get_all_codes", views.get_all_codes, name="get_all_codes"),
    # path("add_new_code", views.add_new_code, name="add_new_code"),
    path("", views.get_user_data, name="get_user_data"),
    path("get_all_redemptions", views.get_all_redemptions, name="get_all_redemptions"),
]
