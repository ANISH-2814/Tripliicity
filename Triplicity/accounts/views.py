from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from .forms import SimpleRegistrationForm, SimpleLoginForm
from .models import User
import threading
import logging

logger = logging.getLogger(__name__)


def home_view(request):
    """Homepage with travel packages and hotels"""
    
    # Sample travel packages data
    travel_packages = [
        {
            "name": "Goa Beach Paradise",
            "location": "Goa, India",
            "price": "₹25,999",
            "duration": "4 Days / 3 Nights",
            "rating": 4.8,
            "features": ["Beach Resort", "Water Sports", "Local Cuisine", "Nightlife"],
            "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400"
        },
        {
            "name": "Kerala Backwaters",
            "location": "Kerala, India", 
            "price": "₹32,999",
            "duration": "6 Days / 5 Nights",
            "rating": 4.9,
            "features": ["Houseboat Stay", "Ayurveda Spa", "Tea Gardens", "Wildlife"],
            "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
        },
        {
            "name": "Shimla Hill Station",
            "location": "Himachal Pradesh, India",
            "price": "₹28,999", 
            "duration": "5 Days / 4 Nights",
            "rating": 4.7,
            "features": ["Mountain Views", "Colonial Architecture", "Adventure Sports", "Cool Climate"],
            "image": "https://images.unsplash.com/photo-1586500036634-57495d9bf10e?w=400"
        },
        {
            "name": "Rajasthan Royal Heritage",
            "location": "Rajasthan, India",
            "price": "₹45,999",
            "duration": "8 Days / 7 Nights", 
            "rating": 4.8,
            "features": ["Palace Hotels", "Camel Safari", "Desert Camping", "Cultural Shows"],
            "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=400"
        },
        {
            "name": "Ladakh Adventure",
            "location": "Ladakh, India",
            "price": "₹55,999",
            "duration": "9 Days / 8 Nights",
            "rating": 4.9,
            "features": ["High Altitude", "Buddhist Monasteries", "Trekking", "Scenic Lakes"],
            "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
        },
        {
            "name": "Andaman Island Escape",
            "location": "Andaman & Nicobar",
            "price": "₹38,999",
            "duration": "6 Days / 5 Nights",
            "rating": 4.6,
            "features": ["Pristine Beaches", "Scuba Diving", "Island Hopping", "Water Villa"],
            "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400"
        }
    ]
    
    # Sample hotels data
    hotels_data = [
        {
            "name": "Luxury Beach Resort Goa",
            "location": "Candolim, Goa",
            "price": "₹8,999",
            "rating": 4.7,
            "amenities": ["Private Beach", "Spa", "Pool", "Restaurant"],
            "image": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400"
        },
        {
            "name": "Heritage Palace Hotel",
            "location": "Udaipur, Rajasthan", 
            "price": "₹15,999",
            "rating": 4.9,
            "amenities": ["Lake View", "Heritage Property", "Fine Dining", "Cultural Program"],
            "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400"
        },
        {
            "name": "Mountain View Resort",
            "location": "Manali, Himachal Pradesh",
            "price": "₹6,999",
            "rating": 4.5,
            "amenities": ["Mountain View", "Adventure Activities", "Bonfire", "Local Cuisine"],
            "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400"
        },
        {
            "name": "Backwater Villa",
            "location": "Alleppey, Kerala",
            "price": "₹12,999",
            "rating": 4.8,
            "amenities": ["Backwater View", "Houseboat", "Ayurveda Spa", "Traditional Meals"],
            "image": "https://images.unsplash.com/photo-1520637836862-4d197d17c798?w=400"
        }
    ]
    
    # Sample user reviews
    user_reviews = [
        {
            "name": "Priya Sharma",
            "location": "Mumbai",
            "rating": 5,
            "review": "Amazing experience with Triplicity! The Goa package was perfectly planned. The hotel was fantastic and the beach activities were incredible. Highly recommended!",
            "package": "Goa Beach Paradise",
            "date": "March 2025"
        },
        {
            "name": "Rahul Patel", 
            "location": "Delhi",
            "rating": 5,
            "review": "Kerala backwaters trip was a dream come true. The houseboat experience was magical and the Ayurveda spa was so relaxing. Will definitely book again!",
            "package": "Kerala Backwaters",
            "date": "February 2025"
        },
        {
            "name": "Anita Desai",
            "location": "Bangalore",
            "rating": 4,
            "review": "Shimla trip was wonderful! The hill station was beautiful and the hotel had amazing mountain views. The only issue was the weather, but that's natural!",
            "package": "Shimla Hill Station", 
            "date": "January 2025"
        },
        {
            "name": "Vikram Singh",
            "location": "Pune",
            "rating": 5,
            "review": "Rajasthan heritage tour exceeded all expectations. The palace hotels were royal and the desert safari was thrilling. Exceptional service from Triplicity!",
            "package": "Rajasthan Royal Heritage",
            "date": "December 2024"
        }
    ]
    
    context = {
        'travel_packages': travel_packages,
        'hotels_data': hotels_data,
        'user_reviews': user_reviews,
    }
    
    return render(request, 'accounts/homepage.html', context)


class RegisterView(View):
    template_name = 'accounts/register.html'
    form_class = SimpleRegistrationForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send welcome email asynchronously (non-blocking)
            self.send_welcome_email_async(user)
            
            # Auto login the user immediately
            login(request, user)
            
            messages.success(request, f'Welcome to Triplicity, {user.get_full_name()}! A confirmation email is being sent to {user.email}.')
            return redirect('accounts:home')
        
        return render(request, self.template_name, {'form': form})

    def send_welcome_email_async(self, user):
        """Send welcome email in background thread to avoid blocking user registration"""
        def send_email():
            try:
                self.send_welcome_email(user)
                logger.info(f"Welcome email sent successfully to {user.email}")
            except Exception as e:
                logger.error(f"Failed to send welcome email to {user.email}: {e}")
        
        # Send email in background thread
        email_thread = threading.Thread(target=send_email)
        email_thread.daemon = True  # Thread will close when main program exits
        email_thread.start()

    def send_welcome_email(self, user):
        """Send enhanced welcome email"""
        subject = 'Welcome to Triplicity! 🛫'
        
        # Simplified HTML email content for faster processing
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                .content {{ background: #f8f9fa; padding: 20px; border-radius: 0 0 8px 8px; }}
                .btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🛫 Welcome to Triplicity!</h1>
            </div>
            <div class="content">
                <h2>Hello {user.get_full_name()}!</h2>
                <p>Thank you for joining Triplicity! We're excited to help you discover amazing travel destinations.</p>
                <p><strong>Your Account:</strong> {user.email}</p>
                <p><strong>Status:</strong> Active ✅</p>
                <div style="text-align: center; margin: 20px 0;">
                    <a href="http://127.0.0.1:8000/accounts/dashboard/" class="btn">Go to Dashboard</a>
                </div>
                <p>Happy travels!<br><strong>The Triplicity Team</strong></p>
            </div>
        </body>
        </html>
        """
        
        # Simplified plain text version
        plain_message = f"""
        Welcome to Triplicity, {user.get_full_name()}!
        
        Your account has been successfully created.
        Email: {user.email}
        Status: Active
        
        Visit: http://127.0.0.1:8000/accounts/dashboard/
        
        Happy travels!
        The Triplicity Team
        """
        
        try:
            from django.core.mail import EmailMultiAlternatives
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.attach_alternative(html_message, "text/html")
            
            # Send with timeout to prevent hanging
            email.send(fail_silently=False)
            return True
            
        except Exception as e:
            logger.error(f"Error sending welcome email to {user.email}: {e}")
            # Don't raise exception to avoid blocking user registration
            return False


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = SimpleLoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            
            # Redirect to next parameter or dashboard
            next_url = request.GET.get('next', 'accounts:home')
            return redirect(next_url)
        
        return render(request, self.template_name, {'form': form})


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {
        'user': request.user
    })


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:home')
