from django.urls import path
from .views import StripeCheckOutView
from .views import StripeCheckout

urlpatterns = [
    path('create-checkout-session/', StripeCheckOutView.as_view()),
    path('stripe-checkout/', StripeCheckout.as_view())
]