from django.shortcuts import render
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework import status
from .models import Booking
from .selializers import BookingSerializer
from services.models import Service
from customer.models import Customer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

class BookingListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        bookings = Booking.objects.all()
        
        query = request.query_params.get('search', None)
        
        if query:
            bookings = bookings.filter(Q(service__name__icontains=query) | Q(service__category__name__icontains=query))
        
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    

class BookingCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required."}, status=401)
        
        payment_method = request.data.get('payment_method', 'cash')
        service_id = request.data.get('service')
        # print(service_id)
        # print(request.user)
        
        try:
            service = Service.objects.get(id=service_id)
            customer = Customer.objects.get(user=request.user)
            # customer = Customer.objects.get(id=1)

        except (Service.DoesNotExist, Customer.DoesNotExist):
            return Response({"error": "Invalid service or customer."}, status=status.HTTP_400_BAD_REQUEST)
        
        if payment_method == 'cash':
            data = request.data.copy()
            data['service'] = service.id
            data['customer'] = customer.id
            data['status'] = 'pending'
            
            serializer = BookingSerializer(data=data)
            if serializer.is_valid():
                serializer.save(is_paid=False, service=service, customer=customer, status='pending')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif payment_method == 'pay_now':
            checkout_session = stripe.checkout.Session.create(
                line_items = [
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': service.name,
                            },
                            'unit_amount': int(service.price * 100),
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=f"{settings.DOMAIN}/bookings/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.DOMAIN}/bookings/payment-cancel",
                metadata = {
                    'service_id': service.id,
                    'customer_id': customer.id,
                    'phone': request.data.get('phone', ''),
                    'address': request.data.get('address', ''),
                    'preferred_date': request.data.get('preferred_date', ''),
                    'preferred_time': request.data.get('preferred_time', ''),
                    'payment_method': payment_method,
                    'status' : 'pending',
                    'note': request.data.get('note', ''),
                }
            )
            print("Checkout Session Created:")
            return Response({"checkout_url": checkout_session.url}, status=status.HTTP_200_OK)
        
        else:
            return Response({"error": "Invalid payment method."}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    permission_classes = [AllowAny]
    print("Webhook received")
    def post(self, request):
        print("Webhook hit")
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            
            # print("Session metadata:", session['metadata']) 

            service_id = int(session['metadata']['service_id'])
            customer_id = int(session['metadata']['customer_id'])
            phone = session['metadata']['phone']
            address = session['metadata']['address']
            note = session['metadata']['note']
            status = session['metadata']['status']
            
            preferred_date = session['metadata'].get('preferred_date')
            preferred_time = session['metadata'].get('preferred_time')

            preferred_date = datetime.strptime(preferred_date, '%Y-%m-%d').date() if preferred_date else None
            preferred_time = datetime.strptime(preferred_time, '%H:%M').time() if preferred_time else None

            service = Service.objects.get(id=service_id)
            customer = Customer.objects.get(id=customer_id)

            Booking.objects.create(
                service=service,
                customer=customer,
                phone=phone,
                address=address,
                preferred_date=preferred_date,
                preferred_time=preferred_time,
                note=note,
                payment_method='pay_now',
                status=status,
                is_paid=True,  # ✅ Stripe payment complete হলে paid
            )
            print("Booking created successfully.")

        return Response(status=200)


class PaymentSuccessView(View):
    def get(self, request):
        return render(request, 'bookings/payment_success.html')

class PaymentCancelView(View):
    def get(self, request):
        return render(request, 'bookings/payment_cancel.html')


class customerBookingListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            bookings = Booking.objects.filter(customer=customer)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer profile not found'}, status=404)