from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from .forms import SimpleRegistrationForm, SimpleLoginForm, UserProfileForm
from .models import User



class RegisterView(View):
    template_name = 'accounts/register.html'
    form_class = SimpleRegistrationForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:homepage')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Send simple welcome email
            self.send_welcome_email(user)
            
            # Auto login the user
            login(request, user)
            
            messages.success(request, f'Welcome to Triplicity, {user.get_full_name()}! A confirmation email has been sent to {user.email}.')
            return redirect('home:homepage')
        
        return render(request, self.template_name, {'form': form})

    def send_welcome_email(self, user):
        """Send enhanced welcome email"""
        subject = 'Welcome to Triplicity! 🛫'
        
        # HTML email content
        html_message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                .btn {{ display: inline-block; padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🛫 Welcome to Triplicity!</h1>
                    <p>Your Travel Adventure Begins Here</p>
                </div>
                <div class="content">
                    <h2>Hello {user.get_full_name()}!</h2>
                    <p>Thank you for joining Triplicity! We're excited to help you discover amazing travel destinations and create unforgettable memories.</p>
                    
                    <p><strong>Your Account Details:</strong></p>
                    <ul>
                        <li><strong>Email:</strong> {user.email}</li>
                        <li><strong>Account Status:</strong> Active ✅</li>
                        <li><strong>Registration Date:</strong> {user.created_at.strftime('%B %d, %Y')}</li>
                    </ul>
                    
                    <p>What's next?</p>
                    <ul>
                        <li>🏨 Browse our amazing hotel deals</li>
                        <li>✈️ Discover exciting travel packages</li>
                        <li>🗺️ Plan your dream vacation</li>
                        <li>📱 Book with confidence</li>
                    </ul>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://127.0.0.1:8000/accounts/dashboard/" class="btn">
                            Go to Your Dashboard
                        </a>
                    </div>
                    
                    <p>If you have any questions, feel free to contact our support team.</p>
                    
                    <p>Happy travels!<br>
                    <strong>The Triplicity Team</strong></p>
                </div>
                <div class="footer">
                    <p>© 2025 Triplicity. All rights reserved.</p>
                    <p>This email was sent to {user.email}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        plain_message = f"""
        Welcome to Triplicity, {user.get_full_name()}!
        
        Thank you for joining our travel community. Your account has been successfully created.
        
        Account Details:
        - Email: {user.email}
        - Status: Active
        - Registration: {user.created_at.strftime('%B %d, %Y')}
        
        Visit your dashboard: http://127.0.0.1:8000/accounts/dashboard/
        
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
            email.send()
            
            return True
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            return False


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = SimpleLoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home:homepage')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            
            # Redirect to next parameter or dashboard
            next_url = request.GET.get('next', 'home:homepage')
            return redirect(next_url)
        
        return render(request, self.template_name, {'form': form})


@login_required
def dashboard_view(request):
    user = request.user
    # Define required fields
    required_fields = [
        'first_name', 'last_name', 'phone', 'address', 'city',
        'state', 'country', 'postal_code', 'date_of_birth'
    ]
    # Check which fields are missing or blank
    missing_fields = [field for field in required_fields if not getattr(user, field)]
    missing_details = bool(missing_fields)

    return render(request, 'accounts/dashboard.html', {
        'user': user,
        'missing_details': missing_details,
        'missing_fields': missing_fields,   
    })

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'accounts/edit_profile.html', {'form': form, 'user': user})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home:homepage')
