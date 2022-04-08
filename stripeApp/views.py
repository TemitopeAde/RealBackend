import imp
import json
from urllib import response
import django
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeCheckOutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        try: 
            checkout_session = stripe.checkout.Session.create(
                line_items = [
                    {
                        'price': 'price_1Kld0HEqayskyY1L9K4p297F',
                        'quantity': 1
                    },

                ],
                payment_method_types = ['card'],
                mode='payment',
                success_url = settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url = settings.SITE_URL + '?canceled=true'
            )
            return redirect(checkout_session.url)
        except:
            return Response(
                {'error': 'Something went wrong'},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StripeCheckout(APIView):
    permission_classes = [permissions.AllowAny]


    def post(self,request):
        try:
            data = request.data
            print(data)

            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=data['amount'],
                currency=data['currency'],
                automatic_payment_methods={
                'enabled': True,
            },
            )
            datas = intent.client_secret
            print(datas)
            return Response(datas,status=status.HTTP_200_OK)
           
            

        except stripe.error.CardError as e:
            print('Status is: %s' % e.http_status)
            print('Code is: %s' % e.code)
            # param is '' in this case
            print('Param is: %s' % e.param)
            print('Message is: %s' % e.user_message)



class StripeNewCheckout(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        try:
            customer = stripe.Customer.create()
            # print(customer.id)
            data = self.request.data
            print(data)
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                customer=customer['id'],
                setup_future_usage='off_session',
                amount=data['amount'],
                currency=data['currency'],
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            datas = intent.client_secret
            print(datas)
            return Response(datas,status=status.HTTP_200_OK)

            
        except stripe.error.CardError as e:
            err = e.error
            # Error code will be authentication_required if authentication is needed
            print('Code is: %s' % err.code)
            payment_intent_id = err.payment_intent['id']
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
