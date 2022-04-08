import imp
from django.urls import path
from .views import StripeCheckOutView
from .views import StripeCheckout
from .views import StripeNewCheckout


urlpatterns = [
    path('stripe-checkout/', StripeCheckout.as_view()),
    path('stripe-new-checkout/', StripeNewCheckout.as_view())
]