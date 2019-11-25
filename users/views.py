from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from users.forms import CustomUserCreationForm
from users.models import CustomUser
from users.tokens import account_activation_token


def index(request):
    return render(request, 'index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = CustomUserCreationForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            registered = True
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, 'mailtodeepak321@gmail.com', [user.email],)
            # user.email_user(subject, message)
            # return redirect('index')
        else:
            print(user_form.errors)
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'signup.html',
                  {'user_form': user_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.email_confirmed:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your email confirmation is pending.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(email, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=int(uid))
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'account_activation_invalid.html')
