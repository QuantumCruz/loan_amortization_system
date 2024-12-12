from django.urls import path
from .views import *

urlpatterns = [
    path('users/', get_users, name="get_profiles"),
    path('users/trans', get_all_transactions, name="get_all_transactions"),
    path('users/trans/<int:pk>', get_profile_transactions, name="get_transactions_for_a_profile"),
    path('users/create/', create_profile, name="create_profile"),
    path('users/create/trans/<int:pk>', add_transaction, name="add_transactions"),
    path('users/<int:pk>', profile_detail, name="profile_details"),
    path('users/authenticate', auth_user, name="authenticate_profile"),
]
