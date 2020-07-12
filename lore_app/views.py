from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render

from lore_app.models import Attack

from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


###index####d
def index(request):
    return render(request, "lore_app/index.html")
###USER LOGIN###

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = "/lore_app/user_login/"
    return HttpResponse("You are logged in. Great!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse("index"))

def register(request):

    registered = False

    if request.method == "POST":

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can"t commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if "profile_pic" in request.FILES:
                print("found it")
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES["profile_pic"]

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors, profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,"lore_app/registration.html",
                          {"user_form":user_form,
                           "profile_form":profile_form,
                           "registered":registered})

def user_login(request):

    if request.method == "POST":
        # First get the username and password supplied
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Django"s built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse("index"))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, "lore_app/login.html", {})

###views for data###

@login_required
def attacks_view(request):
    return render(request, "lore_app/attacks.html")

@login_required
def attack_protocol_data(request):
    count_by_protocol = list(Attack.objects.values("proto").annotate(total=Count("proto")))
    title = "Attacks per protocol"
    return JsonResponse({"data": count_by_protocol, "title": title}, safe=False)

@login_required
def attack_host_data(request):
    count_by_host = list(Attack.objects.values("host").annotate(total=Count("host")))
    title = "Attacks per host"
    return JsonResponse({"data": count_by_host, "title": title}, safe=False)

@login_required
def attack_protocol_host_data(request):
    count_by_host = list(Attack.objects \
                         .values("host") \
                         .annotate(icmp_count=Count("proto", filter=Q(proto="ICMP")),
                                    udp_count=Count("proto", filter=Q(proto="UDP")),
                                    tcp_count=Count("proto", filter=Q(proto="TCP"))))
    title = "Attacks per host & protocol"
    return JsonResponse({"data": count_by_host, "title": title}, safe=False)


