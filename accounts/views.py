from django.shortcuts import render
from .forms import SignupForm, ActivationForm
from django.contrib.auth.models import User
from .models import Profile


# Create your views here.



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            form.save()

            profile = Profile.objects.get(user__username=username)

            send_email(

                "Activate Your Account",
                f"WELOCOME {username} TO OUR WEBSITE \nuse this code {profile.code} to activate your account",
                "mehyar.farzat@gmail.com",
                [email],
                fail_silently=False,
            )

            return redirect(f'/accounts/{username}/activate')

    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form':form})

        



            
                                                         