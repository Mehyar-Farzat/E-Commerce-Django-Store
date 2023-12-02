from django.shortcuts import render, redirect
from .forms import SignupForm, ActivationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required    

from .models import Profile

from products.models import Product,Brand,Review
from orders.models import Order


# Create your views here.



def signup(request):    # create signup view 
    if request.method == 'POST':      # check if request method is POST 
        form = SignupForm(request.POST)   # create form instance with POST data 
        if form.is_valid():        # check if form is valid 
            username = form.cleaned_data['username']   # get username from form 
            email = form.cleaned_data['email']         # get email from form 
            
            # prevent user from signing up with an existing username or email without activating his account
            user = form.save(commit=False)
            user.is_active = False


            form.save()                          # save form

            profile = Profile.objects.get(user__username=username)   # get profile by username 

            send_email(

                "Activate Your Account",
                f"WELOCOME {username} TO OUR WEBSITE \nuse this code {profile.code} to activate your account",
                "mehyar.farzat@gmail.com",
                [email],
                fail_silently=False,
            )

            return redirect(f'/accounts/{username}/activate')    # redirect to activate view with username as argument

    else:                                                        # if request method is GET
        form = SignupForm()                                      # create form instance 

    return render(request,'registration/signup.html', {'form':form})         # render signup template with form instance as context 

        

def activate(request, username):                                            # create activate view 
    profile = Profile.objects.get(user__username=username)                 # get profile by username 
    if request.method == 'POST':                                           # check if request method is POST
        form = ActivationForm(request.POST)                                # create form instance with POST data 
        if form.is_valid():                                                # check if form is valid 
            code = form.cleaned_data['code']                               # get code from form 
            if code == profile.code:                                       # check if code is equal to profile code
                profile.code = ''                                          # set profile code to empty string 


                # the user is activated
                user = User.objects.get(username=profile.user.username)    # get user by username
                user.is_active = True                                      # set user is_active field to True 
                user.save()                                                # save user
                profile.save()                                             # save profile

                return redirect('/accounts/login')                         # redirect to login view

    else:                                                                  # if request method is GET
        form = ActivationForm()                                            # create form instance
 
    return render(request,'registration/activate.html', {'form':form})     # render activate template with form instance as context

@login_required
def dashboard(request):
    new_products = Product.objects.filter(flag='New').count()
    sale_products = Product.objects.filter(flag='Sale').count()
    feature_products = Product.objects.filter(flag='Feature').count()

    users = User.objects.all().count()
    orders = Order.objects.all().count()
    products = Product.objects.all().count()
    brands = Brand.objects.all().count()
    reviews = Review.objects.all().count()

    return render(request,'accounts/dashboard.html',{
        'new_products':new_products,
        'sale_products':sale_products,
        'feature_products':feature_products,
            
        'users':users,
        'orders':orders,
        'products':products,
        'brands':brands,
        'reviews':reviews,
    })
    


       



            
                                                         