from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.http import Http404
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.utils.encoding import force_bytes

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = BlogAuthorUpdateForm(request.POST,
                                      request.FILES,
                                      instance=request.user.blogauthor)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = BlogAuthorUpdateForm(instance=request.user.blogauthor)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/profile.html', context)


def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            user = User.objects.filter(email=data).first()
            if user:
                subject = "Reset requested"
                email_template_name = "registration/password_reset_email.txt"
                context = {
                    "email": user.email,
                    "user": user,
                    "domain": "127.0.0.1:8000",
                    "site_name": "kursach_blog",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                email = render_to_string(email_template_name, context)
                try:
                    send_mail(subject, email, "admin@kursach.com", [user.email], fail_silently=False)
                except BadHeaderError:
                    return Http404
                return redirect("/accounts/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset_form.html",
                  context={"form": password_reset_form})


def godmode(request):
    """
    Create and/or user admin user.
    """
    if not settings.DEBUG:
        raise Http404

    try:
        user = User.objects.get(username='admin', is_superuser=1, is_staff=1)
        print(user)
    except User.DoesNotExist:
        user = User(username='admin', email='admin@gmail.com', password='admin', is_superuser=1, is_staff=1)
        user.save(force_insert=False)
    login(request, user)
    return redirect('/accounts/profile', permanent=True)
