from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from packages.models import Package
from .models import Booking
from .forms import BookingForm
from django.core.mail import send_mail
import stripe
import threading

stripe.api_key = settings.STRIPE_SECRET_KEY

def send_booking_mail_async(user, booking):
    """Send booking confirmation email asynchronously"""
    thread = threading.Thread(target=send_booking_mail, args=(user, booking))
    thread.start()

@login_required
def create_booking(request, package_slug):
    package = get_object_or_404(Package, slug=package_slug)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            person_count = form.cleaned_data['person_count']
            total_amount = float(pkg_price(package)) * int(person_count)
            # Create booking with pending status
            booking = Booking.objects.create(
                user=request.user,
                package=package,
                person_count=person_count,
                total_amount=total_amount,
                status='pending'
            )
            # Create Stripe PaymentIntent
            intent = stripe.PaymentIntent.create(
                amount=int(total_amount * 100),  # Stripe expects paise/cents
                currency="inr",  # or "usd"
                metadata={'booking_id': booking.id, 'user_id': request.user.id},
                description=f"Booking Triplicity: {package.title} for {person_count}x person",
            )
            booking.payment_intent_id = intent['id']
            booking.save()
            return render(request, 'bookings/booking_payment.html', {
                'package': package,
                'booking': booking,
                'client_secret': intent['client_secret'],
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            })
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'package': package, 'form': form})

def pkg_price(package):
    # always returns per person price as float
    return float(package.price)

@csrf_exempt
def payment_complete(request):
    # Called by JS after successful payment, update status and send mail
    if request.method == "POST":
        import json
        data = json.loads(request.body.decode())
        booking_id = data.get('booking_id')
        payment_intent_id = data.get('payment_intent_id')
        booking = get_object_or_404(Booking, id=booking_id, payment_intent_id=payment_intent_id)
        try:
            pi = stripe.PaymentIntent.retrieve(payment_intent_id)
            if pi['status'] == 'succeeded':
                booking.status = 'paid'
                booking.save()
                
                # Send booking confirmation email asynchronously (non-blocking)
                send_booking_mail_async(booking.user, booking)
                
                return render(request, 'bookings/booking_success.html', {'booking': booking})
        except Exception:
            booking.status = 'failed'
            booking.save()
        return render(request, 'bookings/booking_fail.html', {'booking': booking})
    # fallback if someone GETs this URL
    return redirect("home:homepage")

def send_booking_mail(user, booking):
    subject = f'Your Triplicity Booking #{booking.booking_id} is Confirmed!'
    message = f"""Dear {user.get_full_name()},

Thank you for booking "{booking.package.title}" ({booking.person_count} person(s), total ₹{booking.total_amount}).

Booking ID: {booking.booking_id}
Package: {booking.package.title}
Persons: {booking.person_count}
Total Paid: ₹{booking.total_amount}
Booking Date: {booking.created_at.date()}
Status: Confirmed

We look forward to being a part of your journey!
- Triplicity Team
"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        print(f"Booking confirmation email sent to {user.email}")
    except Exception as e:
        print(f"Error sending booking confirmation email: {e}")

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('package')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})
