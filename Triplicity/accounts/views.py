from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from .forms import SimpleRegistrationForm, SimpleLoginForm
from .models import User


def home_view(request):
    """Simple home page"""
    return render(request, 'accounts/home.html')


class RegisterView(View):
    template_name = 'accounts/register.html'
    form_class = SimpleRegistrationForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
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
            return redirect('accounts:dashboard')
        
        return render(request, self.template_name, {'form': form})

    def send_welcome_email(self, user):
        """Send simple welcome email"""
        subject = 'Welcome to Triplicity!'
        message = f"""
        Hello {user.get_full_name()},

        Welcome to Triplicity! Your account has been successfully created.

        Email: {user.email}
        
        You can now start exploring amazing travel packages and book your next adventure!

        Happy Travels,
        The Triplicity Team
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending welcome email: {e}")


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = SimpleLoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:dashboard')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            
            # Redirect to next parameter or dashboard
            next_url = request.GET.get('next', 'accounts:dashboard')
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
